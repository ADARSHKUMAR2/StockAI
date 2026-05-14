# Import libraries for the notebook client
import os
import requests  # For making HTTP requests
import httpx  # An alternative async-friendly HTTP client (good practice)
import json  # For handling JSON data (manifests, action responses)
from dotenv import load_dotenv
from IPython.display import display, Markdown, Image  # To display results nicely
from openai import OpenAI  # or litellm, groq, etc.

from PIL import Image
import asyncio, pathlib

# Load environment variables (needed for the Gradio apps when they run)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Let's define the URL where our Gradio MCP servers will be running
# IMPORTANT: Make sure these match the ports you use when running the server scripts!
MCP_BASE = "http://localhost:7860/gradio_api/mcp/sse"  # text tutor demo you built

# MCPServerSse: A class that sets up a server using Server-Sent Events (SSE) to serve MCP-compatible tools or agents.
# MCPServerSse allows your tool (e.g., an AI model wrapped with Gradio) to be served as an MCP tool endpoint.
# It allows Communication via SSE, which is a way to push updates from server to client (used in real-time AI applications).
from agents.mcp import MCPServerSse


# timeout: 30
# This controls how long (in seconds) the server waits for a single tool execution (i.e., an action call) before giving up.

# client_session_timeout_seconds: 60
# This sets how long an entire client session is kept alive without activity before it's considered expired or disconnected.
# If the client doesn’t send any requests or interact for 60 seconds, the session times out.

mcp_tool = MCPServerSse({
    "name": "AI Tutor",
    "url": MCP_BASE,
    "timeout": 30,
    "client_session_timeout_seconds":60
})
