# AI Research Assistant

A multi-agent system that automates deep research using Claude, LangGraph, and Tavily — turning hours of manual searching into minutes of structured, cited output.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) ![LangGraph](https://img.shields.io/badge/LangGraph-0.2-orange) ![Claude](https://img.shields.io/badge/Claude-Sonnet%204-purple) ![Tavily](https://img.shields.io/badge/Tavily-Search%20API-green)

---

## The Problem

Manual research is slow and prone to hallucination. A typical deep-research task takes a skilled analyst 2–4 hours. LLMs alone make this faster but introduce citation errors and stale knowledge. This project solves both: it pairs Claude's reasoning with live web retrieval, and uses a dedicated Quality Agent to validate every citation before output reaches the user.

---

## Architecture

```
[User Question]
       ↓
[Planning Agent]    → decomposes the question into a research plan
       ↓
[Search Agent]      → calls Tavily API for live, trusted sources
       ↓
[Synthesis Agent]   → merges retrieved chunks using hybrid RAG
       ↓
[Quality Agent]     → validates citations, flags hallucinations
       ↓
[Final Answer + Sources]
```

Agents are orchestrated by **LangGraph**, managing state transitions, parallel execution, and error-recovery branches. Each agent is a discrete node — independently testable and swappable.

---

## Technical Stack

| Layer | Choice | Why |
|---|---|---|
| Agent orchestration | LangGraph | Stateful graph execution with branching and cycles |
| LLM | Claude Sonnet 4 | Strong reasoning and instruction-following |
| Web search | Tavily API | Real-time, relevance-ranked results |
| Retrieval | Hybrid RAG (hybrid_rag.py) | Dense semantic search + BM25 keyword matching for higher recall |
| Error handling | errors.py | Graceful fallback when APIs are unavailable |

---

## Key Design Decisions

- **Parallel agent execution** — Search and Planning agents run concurrently where dependencies allow, cutting latency.
- **Hybrid retrieval** — Pure vector search misses exact-match queries (product names, version numbers). BM25 covers the gap.
- **Citation validation** — The Quality Agent cross-checks every claim against its source URL before output. Responses that fail validation are re-synthesised rather than surfaced to the user.
- **Modular agents** — Each agent is a single-responsibility class, making it easy to swap in a different LLM or search provider.

---

## Results

- Reduces a typical research task from **2–4 hours to under 5 minutes**
- All responses include **verified source citations**
- Hallucination risk reduced vs. single-LLM baseline by catching unsupported claims at the Quality Agent stage

---

## Getting Started

```bash
git clone https://github.com/mrskinzo/ai-research-assistant.git
cd ai-research-assistant
pip install -r requirements.txt
```

Create a `.env` file:

```
ANTHROPIC_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

Run the assistant:

```bash
python app.py
```

---

## File Overview

| File | Purpose |
|---|---|
| `app.py` | Entry point and CLI interface |
| `agents.py` | Planning, Search, Synthesis, and Quality agent definitions |
| `hybrid_rag.py` | Hybrid BM25 + semantic retrieval pipeline |
| `tavily.py` | Tavily API wrapper and result normalisation |
| `errors.py` | Custom exceptions and fallback logic |

---

## What's Next

- [ ] Streaming output for real-time progress updates
- [ ] Persistent memory across sessions
- [ ] Support for document upload as a research source
- [ ] Evaluation harness to benchmark citation accuracy
