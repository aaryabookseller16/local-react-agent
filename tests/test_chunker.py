"""Invariant tests for chunker.py. Standard library only: python3 test_chunker.py"""

import random
import string

from jarvis.chunker import chunk_text, pack_greedy, split_recursive


def make_pages(n_pages, seed=0):
    """Build fake extracted text plus its page_starts, like extract_pdf_text."""
    rng = random.Random(seed)
    pages = []
    for _ in range(n_pages):
        paras = []
        for _ in range(rng.randint(1, 6)):
            sents = []
            for _ in range(rng.randint(1, 8)):
                words = ["".join(rng.choices(string.ascii_lowercase, k=rng.randint(2, 10)))
                         for _ in range(rng.randint(3, 15))]
                sents.append(" ".join(words) + ".")
            paras.append(" ".join(sents))
        pages.append("\n\n".join(paras))
    starts, offset = [], 0
    for p in pages:
        starts.append(offset)
        offset += len(p) + 1
    return "\n".join(pages), starts



def make_pages_no_paragraphs(n_pages, seed=0, target_chars=1800):
    """Pages of single spaced lines, like most extracted PDF text.

    No blank lines anywhere, so "\\n\\n" appears only where pages are joined,
    and each page is close to `target_chars` long. Pass a target just under
    `size` to reproduce the case that broke overlap: the first separator
    yields page sized pieces, which are too coarse for packing to overlap.
    """
    rng = random.Random(seed)
    pages = []
    for _ in range(n_pages):
        lines, length = [], 0
        while length < target_chars:
            words = ["".join(rng.choices(string.ascii_lowercase, k=rng.randint(2, 10)))
                     for _ in range(rng.randint(6, 12))]
            line = " ".join(words)
            lines.append(line)
            length += len(line) + 1
        # pypdf leaves a trailing newline on each page, so joining pages
        # produces "\n\n" at every page boundary. That detail is what makes
        # the first separator split into page sized pieces.
        pages.append("\n".join(lines) + "\n")
    starts, offset = [], 0
    for p in pages:
        starts.append(offset)
        offset += len(p) + 1
    return "\n".join(pages), starts


def check(text, page_starts, size, overlap):
    chunks = chunk_text(text, page_starts, size=size, overlap=overlap)
    assert chunks, "no chunks produced"

    for c in chunks:
        assert len(c["text"]) <= size, f"chunk {c['id']} is {len(c['text'])} > {size}"
        assert c["text"] == text[c["start"]:c["end"]], "text does not match its span"
        assert c["start"] < c["end"], "empty chunk"
        assert c["page_start"] <= c["page_end"], "pages inverted"
        assert 1 <= c["page_start"] <= len(page_starts)
        assert 1 <= c["page_end"] <= len(page_starts)

    assert chunks[0]["start"] == 0, "first chunk does not start at 0"
    assert chunks[-1]["end"] == len(text), "last chunk does not reach the end"

    for prev, nxt in zip(chunks, chunks[1:]):
        assert nxt["start"] > prev["start"], "no forward progress"
        assert nxt["start"] <= prev["end"], "gap between chunks: text was lost"
        assert nxt["page_start"] >= prev["page_start"], "page numbers went backwards"

    assert [c["id"] for c in chunks] == list(range(len(chunks))), "ids not sequential"
    return chunks


def main():
    # 1. realistic multi page text, several size/overlap settings
    for seed in range(5):
        text, starts = make_pages(random.Random(seed).randint(2, 12), seed=seed)
        for size, overlap in [(2000, 200), (500, 50), (300, 0), (5000, 1000)]:
            check(text, starts, size, overlap)

    # 2. text shorter than one chunk
    c = check("one short page.", [0], 2000, 200)
    assert len(c) == 1 and c[0]["page_start"] == 1 == c[0]["page_end"]

    # 3. no separators at all, forces the hard cut path
    c = check("x" * 1000, [0], 300, 30)
    assert len(c) == 4, f"expected 4 hard cut chunks, got {len(c)}"

    # 4. an empty page in the middle: offsets must survive it
    pages = ["first page text.", "", "third page text."]
    starts, o = [], 0
    for p in pages:
        starts.append(o)
        o += len(p) + 1
    text = "\n".join(pages)
    c = check(text, starts, 2000, 100)
    assert c[0]["page_start"] == 1 and c[0]["page_end"] == 3

    # 5. empty text
    assert chunk_text("", [0]) == []

    # 6. a chunk that crosses a page boundary reports both pages
    text, starts = make_pages(4, seed=42)
    chunks = check(text, starts, 2000, 200)
    assert any(x["page_start"] != x["page_end"] for x in chunks), \
        "no chunk crossed a page boundary; the test text is too small"

    # 7. overlap actually overlaps
    text, starts = make_pages(6, seed=7)
    chunks = check(text, starts, 1000, 200)
    overlaps = [p["end"] - n["start"] for p, n in zip(chunks, chunks[1:])]
    assert any(v > 0 for v in overlaps), "no chunk overlapped its neighbour"
    assert all(v <= 200 for v in overlaps), f"overlap exceeded 200: {max(overlaps)}"

    # 8. bad parameters are rejected
    for bad in [dict(size=0), dict(overlap=-1), dict(overlap=2000)]:
        try:
            chunk_text("abc", [0], **bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad}")

    # 9. split_recursive is lossless and respects the size limit
    text, starts = make_pages(3, seed=3)
    spans = split_recursive(text, 0, len(text), 400)
    assert "".join(text[s:e] for s, e in spans) == text, "split lost characters"
    assert all(e - s <= 400 for s, e in spans), "split produced an oversized piece"

    # 10. overlap must survive text with no paragraph breaks, and chunks
    #     must actually use most of the size budget
    for size, overlap in [(2000, 200), (3000, 300), (5000, 500)]:
        # pages just under `size`: the shape that broke overlap
        text, starts = make_pages_no_paragraphs(6, seed=11,
                                                target_chars=int(size * 0.9))
        chunks = check(text, starts, size, overlap)
        gaps = [p["end"] - n["start"] for p, n in zip(chunks, chunks[1:])]
        assert min(gaps) > 0, f"lost overlap at size={size}: {gaps}"
        assert max(gaps) <= overlap, f"overlap too large at size={size}: {gaps}"
        fill = sum(len(c["text"]) for c in chunks) / (len(chunks) * size)
        assert fill > 0.75, f"chunks only {fill:.0%} of size at size={size}"

    print("all chunker tests passed")


if __name__ == "__main__":
    main()
