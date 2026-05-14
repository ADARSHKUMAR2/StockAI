# Learn

Small Python workspace for experimenting with **OpenAI Agents** (`openai-agents`): a **research → analysis → writing** pipeline backed by **OpenRouter** for chat and **Tavily** for web search.

## Main flow: `mainAgents.py`

`mainAgents.py` runs three agents in sequence:

1. **Researcher** — uses the Tavily search tool, returns a short structured summary (`AnalysisSummary`).
2. **Analyst** — reads the research summary and returns trends, risks, and insights (same `AnalysisSummary` shape).
3. **Writer** — combines the original query, research, and analysis into a `FinalReport` (executive summary, long markdown report, follow-up questions).

The default query is set in the `if __name__ == "__main__":` block; change `query = ...` to try other topics.

```bash
python mainAgents.py
```

### Related modules

| File | Role |
|------|------|
| `research_agent.py` | Researcher instructions + `AnalysisSummary` model |
| `analyst_agent.py` | Analyst instructions |
| `writer_agent.py` | Writer instructions + `FinalReport` model |
| `tavily_search.py` | `@function_tool` `tavily_search` — POSTs to Tavily’s search API |

There is commented-out code for a single **manager** agent that would call the three workers as tools; the active code uses an explicit `async` pipeline instead.

## Requirements

- Python **3.12+**
- **`OPENROUTER_API_KEY`** — used with `AsyncOpenAI` + `https://openrouter.ai/api/v1` and model `openai/gpt-4o-mini`
- **`TAVILY_API_KEY`** — used by `tavily_search` in `tavily_search.py`
- **`requests`** — used by the Tavily tool (install with `pip install requests` if it is not already available in your environment)

Optional **LangSmith** tracing is enabled via `@traceable` on `run_pipeline`; set the usual LangSmith env vars if you want traces in LangSmith.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
pip install requests        # if needed for Tavily
```

Create a `.env` in the project root (do not commit real keys):

```env
OPENROUTER_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

Optional tracing:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=your_project_name
```

## Chroma utilities (optional)

If you use the local Chroma store under `chroma_memory/` (collection `market_research`):

- **`view_memory.py`** — lists stored documents and IDs.
- **`export_for_projector.py`** — writes `vectors.tsv` and `metadata.tsv` for embedding visualization tools.

## Other scripts

- **`main.py`** — minimal “Hello from learn!” entrypoint.
- **`test.py`** — small OpenAI client / env sanity check (not part of the main pipeline).
