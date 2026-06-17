"""
autourgos-summary-memory — LLM-compressed rolling summary memory for Autourgos agents.

    from autourgos_summary_memory import SummaryBufferedMemory
"""
from .memory import SummaryBufferedMemory

try:
    from importlib.metadata import version as _v
    __version__ = _v("autourgos-summary-memory")
except Exception:
    __version__ = "1.0.1"

__all__ = ["SummaryBufferedMemory"]
