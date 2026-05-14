import json
import httpx
from mcp_client import MCP_BASE
# Let's use httpx for modern async-friendly requests (though requests works fine too)
client = httpx.Client()  # Create an HTTP client instance

#This is just to return the list of tools
def fetch_schema(server_url):
    """Fetches and parses the MCP schema from a server."""
    schema_url = server_url.replace("/sse", "/schema")
    print(f"Fetching schema from: {schema_url}")
    response = client.get(schema_url, timeout=10)  # Add a timeout
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    schema_data = response.json()
    print("Schema fetched successfully!")
    return schema_data


# Fetch manifest from the AI Tutor server
print("--- Fetching AI Tutor Schema ---")
tutor_schema = fetch_schema(MCP_BASE)

if tutor_schema:
    print("\nAI Tutor Schema Contents:")
    # Pretty print the JSON manifest
    print(json.dumps(tutor_schema, indent=2))

print("\n" + "=" * 50 + "\n")  # Separator
