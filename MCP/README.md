# AI Tutor MCP Toolkit

A small learning stack built with **Gradio**, the **Model Context Protocol (MCP)**, and the **OpenAI Agents SDK** (`agents`). Four tutor actions—explain concepts, summarize text, generate flashcards, and run quizzes—stream completion tokens in the UI and are exposed as **MCP tools** when Gradio’s MCP server is enabled.

The LLM client is an **`AsyncOpenAI`** instance aimed at **[GitHub Models / Azure AI Inference](https://models.inference.ai.azure.com)** (`gpt-4o-mini`), wrapped with **LangSmith**’s `wrap_openai` for optional observability. `mcp_server.py` calls **`set_tracing_disabled(True)`** on the Agents SDK so built-in agent tracing stays off unless you change that.

## Surfaces

| Surface | Description |
|--------|-------------|
| **Gradio demo** (`tutor_app.py`) | Tabs for Explain, Summarize, Flashcards, and Quiz. |
| **MCP over SSE** | Same functions as tools for any MCP client at the Gradio MCP URL (below). |
| **Agents CLI** (`openai_agents_integration.py`) | An `Agent` + `Runner` loop that connects to the Gradio MCP server and uses those tools in chat. |

Implementation details: `mcp_server.py` loads env, builds the wrapped async client, **`set_default_openai_client`**, and **`OpenAIChatCompletionsModel`** as `MODEL_NAME`. Handlers in `actions/` are **async generators** with **`@traceable`** (LangSmith) on each tool.

## Requirements

- Python 3.10+ (recommended)
- Core packages:

```bash
pip install gradio openai python-dotenv openai-agents langsmith
```

`mcp_client.py` also imports `requests`, `httpx`, `ipython`, and `pillow` if you reuse it outside a minimal CLI.

## Configuration

Create a `.env` in the **`MCP`** directory (or export variables in your shell):

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` | **Required** for chat completions: used as the API key for `https://models.inference.ai.azure.com`. If unset, `mcp_server.py` raises on import. |

For LangSmith dashboards (when you enable tracing or use `@traceable` spans), set **`LANGSMITH_API_KEY`** (and related LangSmith env vars) per [LangSmith docs](https://docs.smith.langchain.com/). Agent SDK tracing is disabled in `mcp_server.py` via `set_tracing_disabled(True)`.

`mcp_client.py` may still load `OPENAI_API_KEY` for older snippets; the tutor server path shown here does not use it.

## Run the Gradio + MCP server

From the **`MCP`** directory so imports resolve:

```bash
python tutor_app.py
```

Gradio binds to **127.0.0.1** by default (see `tutor_app.py`); HTTP is usually on port **7860** unless you change it.

### MCP endpoint

With the app running:

```text
http://127.0.0.1:7860/gradio_api/mcp/sse
```

[MCP Inspector](https://github.com/modelcontextprotocol/inspector) example:

```bash
npx @modelcontextprotocol/inspector http://127.0.0.1:7860/gradio_api/mcp/sse
```

If you change host or port, update `MCP_BASE` in `mcp_client.py` to match.

## Run the Agents + MCP chat client

1. Start the Gradio app in one terminal (`python tutor_app.py`).
2. In another terminal, from **`MCP`**:

```bash
python openai_agents_integration.py
```

That script **`await mcp_tool.connect()`** before the REPL, runs **`Runner.run`** in a loop with conversation context from **`result.to_input_list()`**, and exits on **`exit`** / **`quit`**. (Add **`await mcp_tool.disconnect()`** in a `finally` block if you want a clean teardown when leaving the loop.)

## Project layout

| Path | Role |
|------|------|
| `tutor_app.py` | Gradio UI; `launch(..., mcp_server=True)`. |
| `mcp_server.py` | Env load, **`GITHUB_TOKEN`**, wrapped **`AsyncOpenAI`** → Azure inference base URL, **`set_default_openai_client`**, **`OpenAIChatCompletionsModel`** (`gpt-4o-mini`), **`set_tracing_disabled(True)`**. |
| `actions/*.py` | Async streaming tools (`explain_concept`, `summarize_text`, `generate_flashcards`, `quiz_me`) with **`@traceable`** and safe chunk handling. |
| `mcp_client.py` | **`MCPServerSse`** config pointing at the local Gradio MCP URL. |
| `openai_agents_integration.py` | Agent instructions + **`Runner`** REPL using MCP tools. |

## Troubleshooting

- **Startup error about a missing API key**: Set **`GITHUB_TOKEN`** in `.env` under `MCP/` (see `mcp_server.py`).
- **401 / model access from inference host**: Confirm the token is valid for GitHub Models / Azure AI inference and that **`gpt-4o-mini`** is available to that endpoint.
- **Import errors**: Run scripts from the `MCP` folder or adjust **`PYTHONPATH`**.
- **Agent cannot reach tools**: Start **`tutor_app.py`** first; align **`MCP_BASE`** with your Gradio URL and port.
- **Streaming / empty deltas**: Tools guard **`chunk.choices`** before reading **`delta`**; persistent empty streams usually mean API or model errors—check the yielded **`[TOOL ERROR]`** text from **`quiz_me`** (and similar) or exceptions in logs.
