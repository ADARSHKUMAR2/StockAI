# AI Tutor MCP Toolkit

A small learning toolkit built with **Gradio** and the **Model Context Protocol (MCP)**. Four tutor-style actions—explain concepts, summarize text, generate flashcards, and run quizzes—are implemented as streaming LLM calls (via OpenRouter) and exposed both in a web UI and as MCP tools when Gradio’s MCP server is enabled.

## Features

| Surface | Description |
|--------|-------------|
| **Gradio demo** | Tabs for Explain, Summarize, Flashcards, and Quiz with sliders for difficulty, length, and counts. |
| **MCP over SSE** | Same functions are available to MCP clients at the Gradio MCP endpoint (see below). |

Underlying actions live in `actions/` and stream tokens for responsive output.

## Requirements

- Python 3.10+ (recommended)
- Packages used by this folder (install as needed):

```bash
pip install gradio openai python-dotenv
```

If you use `mcp_client.py` as written, you also need `requests`, `httpx`, `ipython`, `pillow`, and the OpenAI **Agents** SDK package that provides `agents.mcp.MCPServerSse` (see that file’s imports).

## Configuration

Create a `.env` file in this directory (or ensure these variables are set in your environment):

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Required at import time by `mcp_server.py` (startup check). |
| `OPENROUTER_API_KEY` | Used for actual API calls; client is configured with `base_url=https://openrouter.ai/api/v1`. |

The model is set in `mcp_server.py` as `MODEL_NAME = "openai/gpt-4o-mini"` on OpenRouter.

## Run the Gradio + MCP server

From the **`MCP`** directory (so `actions` and `mcp_server` imports resolve):

```bash
python tutor_app.py
```

By default Gradio listens on **127.0.0.1** (see `tutor_app.py`). The usual HTTP port is **7860** unless you change it.

### MCP endpoint

After the app is running, the MCP SSE URL is:

```text
http://127.0.0.1:7860/gradio_api/mcp/sse
```

You can connect with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector), for example:

```bash
npx @modelcontextprotocol/inspector http://127.0.0.1:7860/gradio_api/mcp/sse
```

## Project layout

| Path | Role |
|------|------|
| `tutor_app.py` | Builds the Gradio UI and launches with `mcp_server=True`. |
| `mcp_server.py` | Loads env vars, configures the OpenRouter OpenAI client and `MODEL_NAME`. |
| `actions/explanation.py` | Stream explanations by level (1–5). |
| `actions/summary.py` | Stream summaries with a compression ratio. |
| `actions/flashcards.py` | Stream JSON-line flashcards for a topic. |
| `actions/quiz.py` | Stream a multiple-choice quiz with an answer key. |
| `mcp_client.py` | Example wiring for `MCPServerSse` pointing at the local Gradio MCP URL (requires the Agents SDK). |

## Troubleshooting

- **`OPENAI_API_KEY not found`**: Add `OPENAI_API_KEY` to `.env` or the environment before starting.
- **Import errors**: Run `python tutor_app.py` from the `MCP` folder, not from the repo root, unless you adjust `PYTHONPATH`.
- **API errors from OpenRouter**: Confirm `OPENROUTER_API_KEY` and that the chosen model is enabled for your OpenRouter account.
