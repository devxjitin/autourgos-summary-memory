# autourgos-summary-memory

LLM-compressed rolling summary memory for [Autourgos](https://github.com/devxjitin) agents.

Keeps the last N messages in full. When the buffer overflows, older messages are fed to an LLM for compression and merged into a rolling summary. The summary + recent messages are both included in every LLM prompt.

---

## Install

```bash
pip install autourgos-summary-memory
```

---

## Quick Start

```python
from autourgos_summary_memory import SummaryBufferedMemory
from autourgos_openaichat import OpenAIChatModel
from autourgos_react_agent import ReactAgent

# Use a cheap model for summarization
summarizer_llm = OpenAIChatModel(model="gpt-4o-mini")

memory = SummaryBufferedMemory(
    llm=summarizer_llm,
    max_messages=10,   # keep last 10 messages in full; compress the rest
)
agent = ReactAgent(llm=my_llm, memory=memory)
agent.invoke("Start a long research task...")
```

---

## Without an LLM

If no LLM is provided, overflow messages are concatenated verbatim (no AI compression). Still prevents unbounded growth:

```python
memory = SummaryBufferedMemory(max_messages=10)
```

---

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `llm` | any | `None` | LLM with `.invoke(prompt)`. Falls back to raw concat if not set. |
| `max_messages` | int | `10` | Recent messages kept in full before compression triggers. |
| `moving_summary` | str | `""` | Seed summary to start with (optional). |

---

## What format_for_llm returns

```
--- Summary of Past Conversation ---
[compressed history here]
------------------------------------

--- Recent Conversation Context ---
[2024-...] user: latest messages
[2024-...] agent: in full
-----------------------------------
```

---

## Pair with autourgos-summarizer

For scratchpad compression (not memory), see [autourgos-summarizer](https://pypi.org/project/autourgos-summarizer/) — it compresses the agent's reasoning chain, not the conversation history.

---

## Links

- PyPI: https://pypi.org/project/autourgos-summary-memory/
- GitHub: https://github.com/devxjitin/autourgos-summary-memory
- Issues: https://github.com/devxjitin/autourgos-summary-memory/issues

---

## License

MIT — see [LICENSE](LICENSE)
