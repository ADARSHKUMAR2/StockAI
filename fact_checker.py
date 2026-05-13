import os
from dotenv import load_dotenv
load_dotenv(override=True)
# Import the OpenAI API client
from openai import AsyncOpenAI 
# Import the Agent class to create and manage AI agents
# Import the Runner class, which is used to run an agent and get its output
from agents import Agent, Runner, OpenAIChatCompletionsModel, Tool, function_tool, SQLiteSession
from IPython.display import display, Markdown
from langsmith import traceable, wrappers
import asyncio
from pydantic import BaseModel, Field
from datetime import datetime
from ddgs import DDGS
from typing_extensions import TypedDict
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_memory")
memory_collection = chroma_client.get_or_create_collection(name="market_research")

class MarketShareResult(BaseModel):
    company: str
    market_share: str
    source: str
    explanation: str

# Get the OpenAI API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Let's configure the OpenAI Client using our key
# client = AsyncOpenAI(
#         base_url="https://models.inference.ai.azure.com",
#         api_key=os.environ.get("GITHUB_TOKEN"),
#     )
client = wrappers.wrap_openai(AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
))

#Short term memory
session = SQLiteSession(
    session_id="market_share_chat", 
    db_path="agent_memory.db"
)

print("OpenAI client successfully configured.")
@function_tool
def search_the_web(query: str) -> str:
    """Use this tool to search the live internet for up-to-date facts, current events, and statistics."""
    print(f"🌍 Agent is searching the web for: {query}")
    try:
        results = DDGS().text(query, max_results=3)
        # Combine the top 3 snippets into a single string for the AI to read
        return "\n".join([f"- {r['body']}" for r in results])
    except Exception as e:
        return "Search failed."

        # Tool to Save Data to Long-Term Memory ---
@function_tool
def save_to_memory(fact: str) -> str:
    """Use this tool to permanently save an important statistic or fact to your long-term memory."""
    import uuid
    print(f"🧠 Saving to Vector DB: {fact[:50]}...")
    memory_collection.add(
        documents=[fact],
        ids=[str(uuid.uuid4())] # Give the memory a unique ID
    )
    return "Fact successfully saved to long-term memory."

# --- Tool to Retrieve Data from Long-Term Memory ---
@function_tool
def search_memory(query: str) -> str:
    """Use this tool to search your long-term memory for previously researched facts before searching the web."""
    print(f"🧠 Searching Vector DB for: {query}")
    results = memory_collection.query(
        query_texts=[query],
        n_results=2 # Grab the top 2 most relevant past memories
    )
    # If memories exist, return them!
    if results['documents'] and results['documents'][0]:
        return "\n".join(results['documents'][0])
    return "No relevant memories found."

current_date = datetime.now().strftime("%Y-%m-%d")
# Define the instructions for the fact-checker AI Agent
stock_instructions = f"""
Context:
You are a fact-checker who verifies the accuracy of statements. Today's date is {current_date}. 

Instructions:
1. When asked about a company, FIRST use 'search_memory' to check if you have already researched and saved data about them.
2. If the data is not in your memory, use 'search_the_web' to find the most recent market share data.
3. Once you find new data via the web, you MUST immediately use 'save_to_memory' to store it for future use.
4. Output the final verdict.
"""

agent_model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini", 
    openai_client=client
)

# Create a new agent called "Fact Checker"
fact_checker_agent = Agent(name = "Fact_Checker",   # Name of the agent
                           instructions = stock_instructions, # The rules and behavior for the agent
                           model = agent_model,
                           tools=[search_the_web, save_to_memory, search_memory],
                           output_type=MarketShareResult) # The AI model (LLM) to use

# Print a confirmation message that the agent was created
print(f"Agent '{fact_checker_agent.name}' created successfully!")

# A statement we want the Fact Checker agent to verify
statement = "What about Ford?"
# statement = input("Enter a statement to fact-check: ")

# Display the statement we're going to check (in markdown format for nicer formatting)
print(f"Asking the Fact Checker to verify: '{statement}'")

# Run the Fact Checker agent on the input statement
# 'await' is used because running the agent is an asynchronous operation (it might take time)

@traceable(name="fact_checker_run")
async def test():
    response = await Runner.run(
        starting_agent = fact_checker_agent,  # The agent we created earlier
        input = statement,  
        session=session,
        max_turns=15             
        # tool_choice="required"
    )

    # Display the agent's response
    result = response.final_output

    print("\n🤖 Agent's Response:\n")
    print(f"company: {result.company}")
    print(f"market_share: {result.market_share}")
    print(f"source: {result.source}")
    print(f"explanation: {result.explanation}")
    
asyncio.run(test())    