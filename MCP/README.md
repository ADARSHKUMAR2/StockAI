# AI Tutor MCP Toolkit

A small learning stack built with **Gradio**, the **Model Context Protocol (MCP)**, and the **OpenAI Agents SDK** (`agents`). Four tutor actions—explain concepts, summarize text, generate flashcards, and run quizzes—call **OpenRouter** (`openai/gpt-4o-mini`) via an async OpenAI client, stream tokens in the UI, and are also exposed as **MCP tools** when Gradio’s MCP server is enabled.

## Surfaces

| Surface | Description |
|--------|-------------|
| **Gradio demo** (`tutor_app.py`) | Tabs for Explain, Summarize, Flashcards, and Quiz. |
| **MCP over SSE** | Same functions as tools for any MCP client at the Gradio MCP URL (below). |
| **Agents CLI** (`openai_agents_integration.py`) | An `Agent` + `Runner` loop that connects to the Gradio MCP server and calls those tools in chat. |

Implementation details: `mcp_server.py` configures `AsyncOpenAI` against OpenRouter, registers it with `set_default_openai_client`, and wraps the model in `OpenAIChatCompletionsModel`. Handlers in `actions/` are **async generators** that stream completion chunks.

## Requirements

- Python 3.10+ (recommended)
- Core packages:

```bash
pip install gradio openai python-dotenv openai-agents
```

`mcp_client.py` also imports `requests`, `httpx`, `ipython`, and `pillow`; keep them if you reuse that module as a notebook-style client.

## Configuration

Create a `.env` in the **`MCP`** directory (or export variables in your shell):

| Variable | Purpose |
|----------|---------|
| `OPENROUTER_API_KEY` | **Required** by `mcp_server.py` for the async client and for `MODEL_NAME`; missing key prevents startup. |

`mcp_client.py` still loads `OPENAI_API_KEY` for compatibility with other snippets; the tutor server path does not require it.

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

That script defines an `Agent` wired to `MCPServerSse` (see `mcp_client.py`), connects on startup, runs a `input()` loop, and disconnects on exit. Type `exit` or `quit` to leave the loop.

## Project layout

| Path | Role |
|------|------|
| `tutor_app.py` | Gradio UI; `launch(..., mcp_server=True)`. |
| `mcp_server.py` | `load_dotenv`, `OPENROUTER_API_KEY`, `AsyncOpenAI` → OpenRouter, `set_default_openai_client`, `OpenAIChatCompletionsModel` as `MODEL_NAME`. |
| `actions/*.py` | Async streaming tool implementations (`explain_concept`, `summarize_text`, `generate_flashcards`, `quiz_me`). |
| `mcp_client.py` | `MCPServerSse` config pointing at the local Gradio MCP URL. |
| `openai_agents_integration.py` | Agent instructions + `Runner` REPL using the MCP tools. |

## Troubleshooting

- **`OPENROUTER_API_KEY not found`**: Set it in `.env` under `MCP/` before importing `mcp_server` or running `tutor_app.py` / `openai_agents_integration.py`.
- **Import errors**: Run scripts from the `MCP` folder or adjust `PYTHONPATH`.
- **Agent cannot reach tools**: Ensure `tutor_app.py` is running first and that `MCP_BASE` matches your Gradio URL (including port).
- **OpenRouter errors**: Confirm the model is allowed for your key and that billing/limits are OK.
