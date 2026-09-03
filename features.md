# autourgos-summary-memory — Features

LLM-compressed rolling summary memory for Autourgos agents. Keeps the last N messages in full; once the buffer overflows, older messages are fed to an LLM (any object with `.invoke(prompt)`) and merged into a single rolling summary, so both the summary and the recent window are included in every prompt.

## Full Feature List

### Core behavior
- **`SummaryBufferedMemory`** — recent-window buffer (`max_messages`) plus a single evolving `moving_summary` string
- Rolling compression: on overflow, older messages are summarized by an LLM and merged into the existing summary (not discarded, not just concatenated)
- **Works without an LLM** — if none is supplied, overflow messages fall back to verbatim concatenation; still bounds growth, just without AI compression
- Seedable summary (`moving_summary=` constructor arg) to start from existing context
- `format_for_llm` produces a clearly-delimited two-part prompt block: a "Summary of Past Conversation" section and a "Recent Conversation Context" section with per-message timestamps/roles

### Ecosystem fit
- Designed to pair with `autourgos-summarizer` (which compresses an agent's reasoning scratchpad) — different jobs, explicitly documented as safe to use together
- Drop-in `memory=` object for `autourgos_agent.Agent`, same shape as other Autourgos memory packages

### Dependencies
- No hard dependency on a specific LLM provider — any object exposing `.invoke(prompt)` works (e.g. `autourgos-openaichat`'s `OpenAIChatModel`, or a hand-written wrapper)

## Full Feature List — limitations noted honestly

- Summarization quality and cost are fully dependent on whichever LLM is passed in — the package does not itself provide retries, cost tracking, or prompt-engineering beyond the summarize-and-merge loop.
- No selective/relevance-based retrieval — this is a linear compression strategy (keep recent + summarize the rest), not a search/rank strategy like `autourgos-semantic-memory` or `autourgos-vector-memory`.

---

## Competitor Comparison

This module's closest peers are LangChain's summarization-based conversation memories and the memory layers of newer "agent memory" products that also do compression/consolidation.

| Capability | **autourgos-summary-memory** | LangChain `ConversationSummaryMemory` | LangChain `ConversationSummaryBufferMemory` | Mem0 | Zep |
|---|---|---|---|---|---|
| Strategy | Recent window kept verbatim + rolling LLM summary of overflow | Entire history replaced by a running LLM summary | Recent window (token-bounded) + running LLM summary of overflow — closest direct analog | Extracted facts + vector/graph memory, LLM-driven consolidation | Progressive summarization + entity/fact extraction, semantic + temporal search |
| Recent messages kept verbatim | Yes, last `max_messages` | No — everything gets summarized immediately | Yes, up to a token budget | Not verbatim by design (fact-based) | Not verbatim by design (fact-based) |
| Works without an LLM | Yes — verbatim concatenation fallback | No — summary IS the memory, requires an LLM | No — requires an LLM for the summary step | No | No |
| Provider-agnostic LLM | Yes, any `.invoke(prompt)` object | Tied to LangChain's `BaseLanguageModel` interface | Tied to LangChain's `BaseLanguageModel` interface | Configurable LLM backend, but a full service | Configurable LLM backend, but a full service |
| Requires external infrastructure | No — in-process, no DB/service | No | No | Optional self-host, or hosted SaaS | Yes — dedicated memory server/service |
| Bounds context growth | Yes, `max_messages` window + single summary string | Yes, but loses granularity of individual turns quickly | Yes, token-budget-based | Yes, via selective fact storage | Yes, via progressive summarization |
| Multi-user / cross-session scoping | No — single conversation object | No | No | Yes, first-class | Yes, first-class |
| Setup complexity | `pip install`, pass any LLM object | `pip install`, pass a LangChain LLM | `pip install`, pass a LangChain LLM | Requires running/hosting or SaaS account | Requires running/hosting or SaaS account |
| Cost model | One summarization LLM call per overflow batch, size controlled by caller | One summarization call per turn or batch (config-dependent) | One summarization call per overflow batch | Multiple calls: extraction + consolidation | Multiple calls: extraction + consolidation + graph updates |

### How to read this

- **vs. LangChain's `ConversationSummaryBufferMemory`**: functionally the nearest match — both keep a token/message-bounded recent window plus a rolling LLM summary of the rest. The real differences are ecosystem coupling (this package takes any `.invoke()`-shaped object, not a LangChain `BaseLanguageModel`) and the explicit no-LLM fallback mode this package documents, which LangChain's summary memories don't have (they need an LLM to function at all).
- **vs. plain `ConversationSummaryMemory`**: that discards per-turn granularity from the very first message; this package always keeps the last N turns verbatim, which is usually better for immediate-context accuracy.
- **vs. Mem0/Zep**: those are heavier, service-shaped memory systems doing fact/entity extraction and multi-session, multi-user scoping — a different tier of complexity and infrastructure commitment. This package is a single-process, single-conversation compression strategy with no moving parts beyond "call an LLM to summarize."
- **When this package is the right choice**: agents where conversation length threatens the context window, a summarization-capable LLM is already available (even a cheap one), and there's no need for cross-session/multi-user fact storage — i.e. most single-session long-running agents.

Sources:
- [ConversationSummaryBufferMemory | langchain_classic | LangChain Reference](https://reference.langchain.com/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory)
- [The 6 Best AI Agent Memory Frameworks You Should Try in 2026 - MachineLearningMastery.com](https://machinelearningmastery.com/the-6-best-ai-agent-memory-frameworks-you-should-try-in-2026/)
- [LangChain Memory vs Mem0 vs Zep: AI Memory Systems 2026](https://www.index.dev/skill-vs-skill/ai-mem0-vs-zep-vs-langchain-memory)
- [Best AI Agent Memory Frameworks in 2026: Compared and Ranked](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/)
- [Long-Term Memory LangChain Agents: LangGraph and LangMem Guide](https://atlan.com/know/long-term-memory-langchain-agents/)
