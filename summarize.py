"""Map reduce PDF summarization, cached per PDF.

Map and reduce are the same operation with different prompts and different
inputs, so both go through one function: llm_call.
"""

from cache import cache_dir, load_or_build_chunks, read_manifest, write_manifest
from ollama_client import (DEFAULT_MODEL, DEFAULT_NUM_CTX, TruncationError,
                           input_budget_chars, llm_call)
from tool import resolve_in_project

PROMPT_VERSION = 2

MAP_PROMPT = (
    "Summarize the excerpt above in 2 to 4 sentences. Cover only what it "
    "actually says. Do not speculate about the rest of the document. No preamble."
)

REDUCE_PROMPT = (
    "The text above is a set of summaries of consecutive excerpts from one "
    "document. Merge them into a single coherent summary that keeps the main "
    "claims, findings, and structure. Add nothing. No preamble."
)


def summarize_text(text, instruction, model=DEFAULT_MODEL, num_ctx=DEFAULT_NUM_CTX):
    """One summarizing call, halving the input when the model reports truncation."""
    budget = input_budget_chars(num_ctx)
    while True:
        try:
            return llm_call(text[:budget], instruction, model, num_ctx)
        except TruncationError:
            if budget <= 500:
                # Stop being strict rather than loop forever on a bad estimate.
                return llm_call(text[:budget], instruction, model, num_ctx,
                                strict=False)
            budget //= 2


def group_by_budget(texts, budget, sep="\n\n"):
    """Pack consecutive texts into groups that each fit within `budget` chars."""
    groups, current, size = [], [], 0
    for text in texts:
        if current and size + len(sep) + len(text) > budget:
            groups.append(current)
            current, size = [], 0
        current.append(text)
        size += len(text) + len(sep)
    if current:
        groups.append(current)
    return groups


def summarize_chunks(chunks, model=DEFAULT_MODEL, num_ctx=DEFAULT_NUM_CTX,
                     progress=None):
    """Map every chunk to a summary, then reduce until one summary is left."""
    if not chunks:
        return ""

    summaries = []
    for i, chunk in enumerate(chunks):
        if progress:
            progress(f"map {i + 1}/{len(chunks)}")
        summaries.append(summarize_text(chunk["text"], MAP_PROMPT, model, num_ctx))

    round_number = 0
    while True:
        # Recomputed each round: the budget improves as real token counts arrive.
        groups = group_by_budget(summaries, input_budget_chars(num_ctx))
        if len(groups) == 1:
            if progress:
                progress("reduce final")
            return summarize_text("\n\n".join(groups[0]), REDUCE_PROMPT,
                                  model, num_ctx)
        round_number += 1
        if progress:
            progress(f"reduce round {round_number}: {len(groups)} groups")
        summaries = [
            summarize_text("\n\n".join(g), REDUCE_PROMPT, model, num_ctx)
            for g in groups
        ]


def summarize_pdf_cached(requested_path, model=DEFAULT_MODEL,
                         num_ctx=DEFAULT_NUM_CTX, force=False, progress=None):
    """Return the cached summary for a PDF, computing it when missing or stale."""
    full = resolve_in_project(requested_path)
    chunks = load_or_build_chunks(full)      # clears a stale summary if it rebuilds
    directory = cache_dir(full)
    summary_file = directory / "summary.txt"
    manifest = read_manifest(directory)

    fresh = (
        not force
        and summary_file.exists()
        and manifest.get("summary_model") == model
        and manifest.get("summary_prompt_version") == PROMPT_VERSION
    )
    if fresh:
        return summary_file.read_text(encoding="utf-8")

    summary = summarize_chunks(chunks, model, num_ctx, progress=progress)
    summary_file.write_text(summary, encoding="utf-8")
    write_manifest(directory, {
        "summary_model": model,
        "summary_prompt_version": PROMPT_VERSION,
        "summary_num_ctx": num_ctx,
    })
    return summary
