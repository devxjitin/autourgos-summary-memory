"""
autourgos-summary-memory — LLM-compressed rolling summary memory for Autourgos agents.

    from autourgos_summary_memory import SummaryBufferedMemory
"""
from .memory import SummaryBufferedMemory

from autourgos_core import package_version

__version__ = package_version("autourgos-summary-memory", fallback="2.0.6")

__all__ = ["SummaryBufferedMemory"]
