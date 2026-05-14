import os
from dotenv import load_dotenv

load_dotenv(override = True)
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, set_default_openai_client

"""AI Tutor MCP Toolkit
======================

A compact server that exposes **four** powerful learning‑oriented tools via the
Model‑Context‑Protocol (MCP). All functions are OpenAI‑powered, and most stream
partial tokens for low‑latency UX.
"""


if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file.")

# Set up the OpenRouter client with wrapping
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key
)

set_default_openai_client(client)

MODEL_NAME = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini", 
    openai_client=client
)