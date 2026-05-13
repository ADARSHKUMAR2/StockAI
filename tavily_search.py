# Import the Agent class to create and manage AI agents
# Import the Runner class, which is used to run an agent and get its output
from agents import Agent, Runner, OpenAIChatCompletionsModel, Tool, function_tool, SQLiteSession
from typing_extensions import TypedDict
import os
import requests

# A TypedDict describes the expected keys and value types for a dict.
# Here: a search "query" (string) and "max_results" (int).
class TavilySearchParams(TypedDict):
    query: str
    max_results: int

print("OpenAI client successfully configured.")
@function_tool
def tavily_search(params: TavilySearchParams) -> str:
    """Use this tool to search the web for the latest information on a topic."""
    # Tavily search endpoint
    url = "https://api.tavily.com/search"

    # Tell the API we're sending JSON
    headers = {"Content-Type": "application/json"}

    # Build the request body:
    # api_key: your Tavily API key (assumed defined elsewhere as tavily_api_key)
    # query: taken from the params dict
    # max_results: use provided value or default to 3 if missing
    payload = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": params["query"],
        "max_results": params.get("max_results", 3),
    }

    # Send the POST request with JSON body and headers
    response = requests.post(url, json = payload, headers = headers)
    if response.status_code == 200:
        results = response.json().get("results", [])
        summary = "\n".join([f"- {r['title']}: {r['content']}" for r in results])
        return summary if summary else "No relevant results found."
    else:
        return f"Tavily API error: {response.status_code}"

print("✅ Tavily search tool ready.")

