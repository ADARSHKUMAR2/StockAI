# Market Share Fact Checker Agent

This project runs an AI fact-checking agent that:
- checks previously saved company market-share facts from local vector memory,
- searches the web when memory is missing data,
- stores new facts back into memory for future use.

It also includes utility scripts to inspect and export the stored memory.

## What Is Included

- `fact_checker.py`  
  Runs the agent with short-term memory (`agent_memory.db`) and long-term vector memory (`chroma_memory/`).
- `view_memory.py`  
  Prints all saved facts from the Chroma collection.
- `export_for_projector.py`  
  Exports embeddings and text metadata to `vectors.tsv` and `metadata.tsv` (for tools like TensorFlow Embedding Projector).

## Requirements

- Python `3.12+`
- An API key for the model backend used in `fact_checker.py` (`OPENROUTER_API_KEY`)
- (Optional but recommended) LangSmith keys if you want tracing enabled

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .
```

3. Create a `.env` file in the project root with at least:

```env
OPENROUTER_API_KEY=your_key_here
```

Optional tracing variables used by the current script:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=your_project_name
```

## Run

Run the fact-checking agent:

```bash
python fact_checker.py
```

Inspect all stored vector memories:

```bash
python view_memory.py
```

Export embeddings + metadata for visualization:

```bash
python export_for_projector.py
```

## How Memory Works

- **Short-term memory**: `SQLiteSession` stored in `agent_memory.db` (conversation/session context).
- **Long-term memory**: ChromaDB collection `market_research` in `chroma_memory/` (saved facts).

Agent behavior in `fact_checker.py`:
1. Search long-term memory first.
2. If not found, search web.
3. Save newly found facts into long-term memory.
4. Return a structured result (`company`, `market_share`, `source`, `explanation`).
