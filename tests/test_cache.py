"""Cache and summarizer tests. No Ollama and no real PDF needed.

Two fakes make this run anywhere:
  - a fake `ollama` module installed in sys.modules before agent.ollama_client
    imports it, so llm_call can be driven and counted;
  - a fake extractor patched over agent.cache.extract_pdf_text, so the cache
    logic is tested without pypdf. The real extractor has its own PDF tests.

Run: python -m tests.test_cache
"""

import sys
import tempfile
import types

from pathlib import Path


class FakeOllama:
    """Stands in for the ollama module. Records calls, returns canned replies."""

    def __init__(self):
        self.calls = []
        self.reply = "SUMMARY"
        self.prompt_tokens = None      # None means "a plausible, non truncated count"

    def chat(self, model, messages, options):
        prompt = messages[-1]["content"]
        self.calls.append({"model": model, "prompt": prompt, "options": options})
        tokens = (self.prompt_tokens if self.prompt_tokens is not None
                  else max(1, int(len(prompt) / 3.5)))
        return {"message": {"role": "assistant", "content": self.reply},
                "prompt_eval_count": tokens}


fake_ollama = FakeOllama()
sys.modules["ollama"] = types.SimpleNamespace(chat=fake_ollama.chat)

from agent import cache, ollama_client, summarize          # noqa: E402
from agent.ollama_client import TruncationError            # noqa: E402
from agent.tool import PROJECT_ROOT                        # noqa: E402

FIXTURE = "tests/fixtures/fake_doc.pdf"


def fake_extract(n_pages=4, page_chars=1500):
    """Return an extractor producing deterministic text, and a call counter."""
    calls = []

    def extract(path):
        calls.append(str(path))
        pages, starts, offset = [], [], 0
        for i in range(n_pages):
            body = f"page {i + 1} " + "lorem ipsum dolor sit amet " * (page_chars // 27)
            lines = [body[j:j + 70] for j in range(0, len(body), 70)]
            page = "\n".join(lines) + "\n"
            starts.append(offset)
            pages.append(page)
            offset += len(page) + 1
        return "\n".join(pages), starts

    return extract, calls


def fresh_cache_root():
    """Point the cache at a throwaway directory outside the repo."""
    cache.CACHE_ROOT = Path(tempfile.mkdtemp(prefix="jarvis-cache-"))
    return cache.CACHE_ROOT


def main():
    import hashlib
    import json

    assert (PROJECT_ROOT / FIXTURE).is_file(), f"missing fixture {FIXTURE}"

    # 1. hashing: content decides identity, not the name
    fresh_cache_root()
    full = PROJECT_ROOT / FIXTURE
    expected = hashlib.sha256(full.read_bytes()).hexdigest()
    assert cache.file_sha256(full) == expected
    assert cache.file_sha256(full, block_size=7) == expected, "block size changed the hash"
    print("OK file_sha256")

    # 2. build once, then hit the cache
    root = fresh_cache_root()
    extract, calls = fake_extract()
    cache.extract_pdf_text = extract
    chunks = cache.load_or_build_chunks(FIXTURE)
    assert chunks and len(calls) == 1
    directory = root / expected
    manifest = json.loads((directory / "manifest.json").read_text())
    assert manifest["chunk_size"] == cache.CHUNK_SIZE
    assert manifest["n_chunks"] == len(chunks)
    again = cache.load_or_build_chunks(FIXTURE)
    assert again == chunks and len(calls) == 1, "second call re-extracted"
    print(f"OK cache hit ({len(chunks)} chunks, {manifest['n_pages']} pages)")

    # 3. changed settings invalidate even though the file is identical
    old_size = cache.CHUNK_SIZE
    cache.CHUNK_SIZE = 900
    try:
        rebuilt = cache.load_or_build_chunks(FIXTURE)
        assert len(calls) == 2, "settings change did not rebuild"
        assert len(rebuilt) > len(chunks)
    finally:
        cache.CHUNK_SIZE = old_size
    cache.load_or_build_chunks(FIXTURE)            # back to the original setting
    assert len(calls) == 3
    print("OK manifest invalidates on settings change")

    # 4. rebuilding chunks clears a stale summary
    (directory / "summary.txt").write_text("stale", encoding="utf-8")
    cache.write_manifest(directory, {"chunk_size": -1})
    cache.load_or_build_chunks(FIXTURE)
    assert not (directory / "summary.txt").exists(), "stale summary survived a rebuild"
    print("OK stale summary cleared")

    # 5. a corrupt manifest is treated as absent
    (directory / "manifest.json").write_text("{not json", encoding="utf-8")
    assert cache.read_manifest(directory) == {}
    cache.load_or_build_chunks(FIXTURE)
    assert cache.read_manifest(directory)["manifest_version"] == cache.MANIFEST_VERSION
    print("OK corrupt manifest recovers")

    # 6. llm_call: truncation detection and calibration
    ollama_client.reset_calibration()
    assert ollama_client.chars_per_token() == ollama_client.FALLBACK_CHARS_PER_TOKEN
    fake_ollama.prompt_tokens = None
    ollama_client.llm_call("x" * 4000, "instruction", num_ctx=8192)
    assert 3.0 < ollama_client.chars_per_token() < 4.5, ollama_client.chars_per_token()
    sent = fake_ollama.calls[-1]
    assert sent["options"]["num_ctx"] == 8192, "num_ctx not passed"
    assert sent["prompt"].rstrip().endswith("instruction"), "instruction not at the tail"

    fake_ollama.prompt_tokens = 8192               # sitting at the ceiling
    try:
        ollama_client.llm_call("x" * 100000, "instruction", num_ctx=8192)
        raise AssertionError("ceiling count did not raise")
    except TruncationError:
        pass
    fake_ollama.prompt_tokens = 10                 # far under what we sent
    try:
        ollama_client.llm_call("x" * 100000, "instruction", num_ctx=8192)
        raise AssertionError("undercount did not raise")
    except TruncationError:
        pass
    ollama_client.llm_call("x" * 100000, "instruction", num_ctx=8192, strict=False)
    fake_ollama.prompt_tokens = None
    print("OK truncation detection and calibration")

    # 7. group_by_budget packs without exceeding the budget or losing items
    texts = ["a" * 300, "b" * 300, "c" * 900, "d" * 50]
    groups = summarize.group_by_budget(texts, budget=700)
    assert [t for g in groups for t in g] == texts, "items lost or reordered"
    for g in groups:
        assert len(g) == 1 or len("\n\n".join(g)) <= 700
    print(f"OK group_by_budget ({len(groups)} groups)")

    # 8. summarize_text stops halving instead of looping forever
    ollama_client.reset_calibration()
    fake_ollama.prompt_tokens = 4                  # always looks truncated
    before = len(fake_ollama.calls)
    out = summarize.summarize_text("z" * 50000, "sum", num_ctx=8192)
    assert out == "SUMMARY"
    assert len(fake_ollama.calls) - before < 25, "halving loop ran too long"
    fake_ollama.prompt_tokens = None
    print("OK summarize_text terminates under repeated truncation")

    # 9. multi round reduce: many chunks, small context
    ollama_client.reset_calibration()
    fake_ollama.reply = "s" * 400
    many = [{"text": "t" * 1000} for _ in range(40)]
    before = len(fake_ollama.calls)
    result = summarize.summarize_chunks(many, num_ctx=2048)
    made = len(fake_ollama.calls) - before
    assert result == "s" * 400
    assert made > len(many), "reduce rounds never happened"
    print(f"OK map reduce over 40 chunks in {made} calls")
    fake_ollama.reply = "SUMMARY"

    # 10. summarize_pdf_cached: compute once, reuse, invalidate on model change
    fresh_cache_root()
    extract, calls = fake_extract()
    cache.extract_pdf_text = extract
    ollama_client.reset_calibration()
    before = len(fake_ollama.calls)
    first = summarize.summarize_pdf_cached(FIXTURE, model="fake-model")
    cost = len(fake_ollama.calls) - before
    assert first == "SUMMARY" and cost > 0

    before = len(fake_ollama.calls)
    second = summarize.summarize_pdf_cached(FIXTURE, model="fake-model")
    assert second == first and len(fake_ollama.calls) == before, "cached summary recomputed"

    summarize.summarize_pdf_cached(FIXTURE, model="fake-model", force=True)
    assert len(fake_ollama.calls) > before, "force=True did not recompute"

    before = len(fake_ollama.calls)
    summarize.summarize_pdf_cached(FIXTURE, model="other-model")
    assert len(fake_ollama.calls) > before, "model change did not invalidate"
    print(f"OK summarize_pdf_cached (first run {cost} calls, then cached)")

    print("all cache and summarizer tests passed")


if __name__ == "__main__":
    main()
