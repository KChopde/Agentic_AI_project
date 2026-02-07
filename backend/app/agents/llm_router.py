from __future__ import annotations

import random
import time
from typing import Any


class LLMRouter:
    def __init__(self, primary: str = "openai", fallback: str = "anthropic") -> None:
        self.primary = primary
        self.fallback = fallback

    def chat(self, messages: list[dict], tools: list[dict] | None = None, stream: bool = False) -> dict:
        _ = tools, stream
        provider = self._choose_provider()
        return {
            "provider": provider,
            "response": "LLM call placeholder",
        }

    def _choose_provider(self) -> str:
        return self.primary

    def retry_with_backoff(self, attempt: int) -> None:
        delay = min(2 ** attempt, 8) + random.random()
        time.sleep(delay)
