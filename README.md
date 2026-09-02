# autourgos-summary-memory

[![Framework: Autourgos](https://img.shields.io/badge/Framework-Autourgos-orange.svg)](https://github.com/devxjitin)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/autourgos-summary-memory/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/devxjitin/autourgos-summary-memory/blob/main/LICENSE)
[![Author](https://img.shields.io/badge/Author-Jitin%20Kumar%20Sengar-blue.svg)](https://github.com/devxjitin)
[![Contributor](https://img.shields.io/badge/Contributor-Sonia-blueviolet.svg)](https://github.com/dahiyasonia)
[![Contributor](https://img.shields.io/badge/Contributor-Vishwanil%20Suman-blueviolet.svg)]()

LLM-compressed rolling summary memory for [Autourgos](https://github.com/devxjitin) agents. Keeps the last N
messages in full. When the buffer overflows, older messages are fed to an LLM for compression and merged
into a rolling summary. The summary + recent messages are both included in every LLM prompt.

```python
from autourgos_summary_memory import SummaryBufferedMemory
from autourgos_openaichat import OpenAIChatModel
from autourgos_agent import Agent

summarizer_llm = OpenAIChatModel(model="gpt-4o-mini")  # needs OPENAI_API_KEY set
memory = SummaryBufferedMemory(llm=summarizer_llm, max_messages=10)
agent = Agent(llm=summarizer_llm, memory=memory)
agent.invoke("Start a long research task...")
```

---

## Features

- **Rolling LLM compression** — older messages are summarized, not dropped, so context survives long
  conversations
- **Works without an LLM too** — falls back to verbatim concatenation, still prevents unbounded growth
- **Pairs with `autourgos-summarizer`** — that package compresses the agent's reasoning scratchpad, this one
  compresses conversation history; different jobs, safe to use together

---

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [Without an LLM](#without-an-llm)
- [Parameters](#parameters)
- [What format_for_llm Returns](#what-format_for_llm-returns)
- [License](#license)

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
from autourgos_agent import Agent

# Use a cheap model for summarization
summarizer_llm = OpenAIChatModel(model="gpt-4o-mini")  # needs OPENAI_API_KEY set
my_llm = summarizer_llm  # or any other chat-model instance for the main agent

memory = SummaryBufferedMemory(
    llm=summarizer_llm,
    max_messages=10,   # keep last 10 messages in full; compress the rest
)
agent = Agent(llm=my_llm, memory=memory)
agent.invoke("Start a long research task...")
```

---

## Without an LLM

If no LLM is provided, overflow messages are concatenated verbatim (no AI compression). Still prevents
unbounded growth:

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

## What format_for_llm Returns

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

## License

Apache License 2.0, Copyright (c) 2026 Jitin Kumar Sengar
