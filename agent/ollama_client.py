"""The single place this project talks to Ollama.

Two things every call has to get right:
  num_ctx  Ollama defaults to 4096 tokens and silently truncates anything
           longer, returning HTTP 200 with quietly worse output.
  the tail Truncation keeps the END of the prompt, so the instruction is
           repeated last, where it survives.
"""

import ollama

DEFAULT_MODEL = "qwen2.5:14b"
DEFAULT_NUM_CTX = 8192          # confirm with `ollama show qwen2.5:14b` and your RAM
RESERVED_TOKENS = 1024          # room for the instruction plus the model's answer
FALLBACK_CHARS_PER_TOKEN = 3.5  # conservative until real counts arrive

# Updated from real prompt_eval_count values as calls happen.
_calibration = {"chars": 0, "tokens": 0}


def reset_calibration():
    """Forget measured token statistics. Used by tests."""
    _calibration["chars"] = 0
    _calibration["tokens"] = 0


def chars_per_token():
    """Measured characters per token, or a conservative default before any call."""
    if _calibration["tokens"] < 200:      # too little data to trust yet
        return FALLBACK_CHARS_PER_TOKEN
    return _calibration["chars"] / _calibration["tokens"]


def input_budget_chars(num_ctx=DEFAULT_NUM_CTX):
    """Characters of input that fit once the instruction and output are reserved."""
    return max(1, int((num_ctx - RESERVED_TOKENS) * chars_per_token()))


class TruncationError(RuntimeError):
    """The model saw less than we sent, so its answer covers partial input."""


def _field(response, name, default=0):
    """Read a field whether the client returns a dict or a response object."""
    if isinstance(response, dict):
        return response.get(name, default)
    return getattr(response, name, default)


def llm_call(text, instruction, model=DEFAULT_MODEL, num_ctx=DEFAULT_NUM_CTX,
             strict=True):
    """Send text plus an instruction and return the reply.

    Raises TruncationError when the reported prompt token count suggests the
    input did not fit: either it sits at the context ceiling, or it is far
    below what we estimate we sent.
    """
    prompt = f"{text}\n\n---\n{instruction}"

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": prompt},
        ],
        options={"temperature": 0, "num_ctx": num_ctx},
    )

    prompt_tokens = _field(response, "prompt_eval_count", 0) or 0
    if prompt_tokens > 0:
        estimated = len(prompt) / chars_per_token()
        _calibration["chars"] += len(prompt)
        _calibration["tokens"] += prompt_tokens

        # Ollama reports the count AFTER truncating, so two symptoms matter:
        # the count sits at the ceiling, or it is far under what we sent.
        at_ceiling = prompt_tokens >= num_ctx - 8
        far_under = prompt_tokens < 0.9 * estimated
        if strict and (at_ceiling or far_under):
            raise TruncationError(
                f"sent about {estimated:.0f} tokens, model evaluated "
                f"{prompt_tokens} with num_ctx={num_ctx}"
            )

    message = _field(response, "message", None)
    content = message["content"] if isinstance(message, dict) else message.content
    return content.strip()
