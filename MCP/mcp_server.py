import os
from dotenv import load_dotenv

load_dotenv(override = True)
github_token = os.getenv("GITHUB_TOKEN")

from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled
from langsmith import wrappers

"""AI Tutor MCP Toolkit
======================

A compact server that exposes **four** powerful learning‑oriented tools via the
Model‑Context‑Protocol (MCP). All functions are OpenAI‑powered, and most stream
partial tokens for low‑latency UX.
"""
set_tracing_disabled(True)
if not github_token:
    raise ValueError("GITHUB_TOKEN not found in .env file.")

# Set up the OpenRouter client with wrapping
client = wrappers.wrap_openai(AsyncOpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=github_token
))

set_default_openai_client(client)

MODEL_NAME = OpenAIChatCompletionsModel(
    model="gpt-4o-mini", 
    openai_client=client
)