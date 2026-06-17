"""
memory.py — LLM-compressed rolling summary memory.
"""
from __future__ import annotations

import logging
import threading
from datetime import datetime, timezone
from typing import Any, List, Optional

from autourgos_memory import BaseMemory, MemoryMessage

logger = logging.getLogger(__name__)


class SummaryBufferedMemory(BaseMemory):
    """Memory that compresses older history into a rolling LLM summary.

    Keeps the last ``max_messages`` messages in full. When the buffer
    overflows, excess messages are fed to the LLM for summarization and
    merged into ``moving_summary``. If no LLM is provided, raw
    concatenation is used as a fallback.

    Parameters
    ----------
    llm : any, optional
        LLM with ``.invoke(prompt: str)`` method. If omitted, history is
        concatenated verbatim (no compression).
    max_messages : int
        Number of recent messages to keep in full. Default 10.
    moving_summary : str
        Seed summary to start with (optional).
    """

    def __init__(
        self,
        llm: Optional[Any] = None,
        max_messages: int = 10,
        moving_summary: str = "",
    ) -> None:
        if not isinstance(max_messages, int) or max_messages < 1:
            raise ValueError("max_messages must be an integer >= 1")
        self.llm = llm
        self.max_messages = max_messages
        self.moving_summary = moving_summary
        self._messages: List[MemoryMessage] = []
        self._lock = threading.RLock()

    def _update_summary(self, to_summarize: List[MemoryMessage]) -> None:
        if not to_summarize:
            return
        if not self.llm:
            lines = [f"[{m.role}]: {m.content}" for m in to_summarize]
            prefix = f"{self.moving_summary}\n" if self.moving_summary else ""
            self.moving_summary = prefix + "\n".join(lines)
            return
        prompt = (
            "You are a conversation summarizer.\n"
            "Compress the conversation below and integrate it with the existing summary.\n\n"
            f"Existing Summary:\n{self.moving_summary or 'No existing summary.'}\n\n"
            "New messages to summarize:\n"
        )
        for m in to_summarize:
            prompt += f"[{m.role}]: {m.content}\n"
        prompt += "\nProvide a concise, updated summary of the entire conversation so far."
        try:
            response = self.llm.invoke(prompt)
            if isinstance(response, dict):
                summary = response.get("response", response.get("content", ""))
            else:
                summary = response
            self.moving_summary = str(summary).strip()
        except Exception as exc:
            logger.warning("Summary compression failed: %s. Falling back to raw concatenation.", exc)
            lines = [f"[{m.role}]: {m.content}" for m in to_summarize]
            prefix = f"{self.moving_summary}\n" if self.moving_summary else ""
            self.moving_summary = prefix + "\n".join(lines)

    def add_message(self, role: str, content: str, timestamp: Optional[datetime] = None) -> MemoryMessage:
        with self._lock:
            msg = MemoryMessage(role=role, content=content, timestamp=timestamp or datetime.now(timezone.utc))
            self._messages.append(msg)
            if len(self._messages) > self.max_messages:
                overflow = self._messages[:-self.max_messages]
                self._messages = self._messages[-self.max_messages:]
                self._update_summary(overflow)
            return msg

    def add_user_message(self, content: str) -> MemoryMessage:
        return self.add_message("user", content)

    def add_agent_message(self, content: str) -> MemoryMessage:
        return self.add_message("agent", content)

    def add_tool_message(self, tool_name: str, result: str) -> MemoryMessage:
        return self.add_message("tool", f"[{tool_name} returned]: {result}")

    def get_messages(self) -> List[MemoryMessage]:
        with self._lock:
            return list(self._messages)

    def format_for_llm(self, query: Optional[str] = None) -> str:
        with self._lock:
            parts = []
            if self.moving_summary:
                parts.append(
                    "--- Summary of Past Conversation ---\n"
                    f"{self.moving_summary}\n"
                    "------------------------------------"
                )
            if self._messages:
                recent = "\n".join(f"[{m.timestamp.isoformat()}] {m.role}: {m.content}" for m in self._messages)
                parts.append(
                    "--- Recent Conversation Context ---\n"
                    f"{recent}\n"
                    "-----------------------------------"
                )
            return "\n\n".join(parts)

    def clear(self) -> None:
        with self._lock:
            self._messages.clear()
            self.moving_summary = ""
