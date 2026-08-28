"""
Direct Anthropic API client — replaces every
`emergentintegrations.llm.chat.LlmChat` call site in server.py.

Emergent's `emergentintegrations` package routes model calls through
Emergent's own proprietary billing gateway (`EMERGENT_LLM_KEY`), which only
works while hosted on Emergent's platform. Since this app is being merged
onto its own hosting for theteachkit.com, every AI call goes straight to
Anthropic instead, mirroring the pattern already proven in the local
engine's `proxy.js` (a real `ANTHROPIC_API_KEY` kept server-side).

Centralizes what used to be duplicated per-call-site in server.py: client
construction, streaming-to-text collection, and rate-limit/error handling.
"""
import logging
import os
from typing import List, Optional

import anthropic

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-5"

_client: Optional[anthropic.AsyncAnthropic] = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        api_key = os.environ["ANTHROPIC_API_KEY"]
        _client = anthropic.AsyncAnthropic(api_key=api_key)
    return _client


class AnthropicGenerationError(Exception):
    pass


async def generate(system: str, prompt: str, max_tokens: int = 4096) -> str:
    """Send one system+user prompt to Claude, return the full text response.

    Streams internally (matches the long-generation timeout behavior the
    local engine's proxy.js and the prior emergentintegrations call sites
    both relied on) but collects and returns the complete text — callers
    don't need to know it was streamed.
    """
    client = _get_client()
    try:
        text_parts: List[str] = []
        async with client.messages.stream(
            model=MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for text in stream.text_stream:
                text_parts.append(text)
        return "".join(text_parts)
    except anthropic.APIStatusError as e:
        logger.error(f"Anthropic API error {e.status_code}: {e.message}")
        raise AnthropicGenerationError(f"AI generation failed ({e.status_code}): {e.message}") from e
    except anthropic.APIError as e:
        logger.error(f"Anthropic API error: {e}")
        raise AnthropicGenerationError(f"AI generation failed: {e}") from e
