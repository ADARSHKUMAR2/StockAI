# tutor_mcp_server.py
"""AI Tutor MCP Toolkit
======================

A compact server that exposes **four** powerful learning‑oriented tools via the
Model‑Context‑Protocol (MCP). All functions are OpenAI‑powered, and most stream
partial tokens for low‑latency UX.
"""

import os
import io
from typing import Generator, List
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Environment & OpenAI client setup
# -----------------------------------------------------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file. Server cannot start.")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL_NAME = "openai/gpt-4o-mini"