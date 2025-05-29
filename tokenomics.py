"""Utilities for analyzing token usage with OpenAI chat models.

This module provides functions to compute token usage for a list of
OpenAI chat messages using ``tiktoken``. It supports caching of results
so repeated calls with the same parameters are fast. Optionally the
number of tokens for a predicted output can be included in the report.

Example
-------
>>> messages = [
...     {"role": "user", "content": "Hello"},
...     {"role": "assistant", "content": "Hi"},
... ]
>>> report = tokenomics_report(messages)
>>> print(report["input_tokens"])
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Iterable, List, Dict, Optional

import tiktoken

CACHE_PATH = os.path.expanduser("~/.cache/tactictoolkit/tokenomics_cache.json")


def _load_cache() -> Dict[str, dict]:
    if not os.path.exists(CACHE_PATH):
        return {}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(cache: Dict[str, dict]) -> None:
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def _cache_key(model: str, messages: Iterable[dict], predicted_output: Optional[str]) -> str:
    payload = {"model": model, "messages": list(messages), "predicted_output": predicted_output}
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _encoding_for_model(model: str):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base for unknown models
        return tiktoken.get_encoding("cl100k_base")


def _message_token_count(message: dict, encoding, tokens_per_message: int, tokens_per_name: int) -> int:
    count = tokens_per_message
    count += len(encoding.encode(message.get("role", "")))
    count += len(encoding.encode(message.get("content", "")))
    if "name" in message:
        count += tokens_per_name
        count += len(encoding.encode(message.get("name", "")))
    return count


def tokenomics_report(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    predicted_output: Optional[str] = None,
    use_cache: bool = True,
) -> dict:
    """Return a detailed token usage report for ``messages``.

    Parameters
    ----------
    messages:
        Sequence of chat completion messages. Each message must contain a
        ``"role"`` and ``"content"`` key following the OpenAI format.
    model:
        Model name used for token encoding. Defaults to ``"gpt-3.5-turbo"``.
    predicted_output:
        Optional text representing a predicted assistant response. When
        provided, the token count of this text will be included in the
        report under ``"predicted_output_tokens"``.
    use_cache:
        If ``True`` (default), results are cached on disk keyed by the
        combination of ``messages``, ``model`` and ``predicted_output``.

    Returns
    -------
    dict
        Dictionary with the keys ``"model"``, ``"input_tokens"`` and
        optionally ``"predicted_output_tokens"``.
    """

    cache_key = _cache_key(model, messages, predicted_output)
    if use_cache:
        cache = _load_cache()
        if cache_key in cache:
            return cache[cache_key]
    else:
        cache = {}

    encoding = _encoding_for_model(model)

    # Heuristics taken from OpenAI documentation
    tokens_per_message = 3
    tokens_per_name = 1
    if model in {"gpt-3.5-turbo-0301"}:
        tokens_per_message = 4
        tokens_per_name = -1

    detail = []
    input_tokens = 0
    for message in messages:
        msg_tokens = _message_token_count(message, encoding, tokens_per_message, tokens_per_name)
        detail.append({"message": message, "tokens": msg_tokens})
        input_tokens += msg_tokens

    # Every reply is primed with <|start|>assistant<|message|>
    input_tokens += 3

    predicted_tokens = 0
    if predicted_output:
        predicted_tokens = len(encoding.encode(predicted_output))

    report = {
        "model": model,
        "input_tokens": input_tokens,
        "messages_detail": detail,
    }
    if predicted_output is not None:
        report["predicted_output_tokens"] = predicted_tokens

    if use_cache:
        cache[cache_key] = report
        _save_cache(cache)

    return report


__all__ = ["tokenomics_report"]
