import os
from dotenv import load_dotenv
load_dotenv(override=True)
# Import the OpenAI API client
from openai import AsyncOpenAI 
# Import the Agent class to create and manage AI agents
# Import the Runner class, which is used to run an agent and get its output
from agents import Agent, Runner, OpenAIChatCompletionsModel
from IPython.display import display, Markdown
from langsmith import traceable, wrappers
import asyncio
from pydantic import BaseModel, Field

class FactCheckResult(BaseModel):
    is_true: bool = Field(description="True if the statement is factually correct, False otherwise")
    explanation: str = Field(description="A brief, one-sentence explanation justifying the conclusion")

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

print("OpenAI client successfully configured.")


# A Function used to Show the given text using Markdown formatting in a Jupyter notebook
def print_markdown(text):
    """Displays text as Markdown in Jupyter."""
    display(Markdown(text))

# Define the instructions for the fact-checker AI Agent
fact_checker_instructions = f"""
Context:
You are a fact-checker who verifies the accuracy of statements.

Instructions:
When given a statement, carefully analyze its factual accuracy using your knowledge.

Input:
You will receive a statement that requires fact-checking.

"""

agent_model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini", 
    openai_client=client
)

# Create a new agent called "Fact Checker"
fact_checker_agent = Agent(name = "Fact_Checker",   # Name of the agent
                           instructions = fact_checker_instructions, # The rules and behavior for the agent
                           model = agent_model,
                           output_type=FactCheckResult) # The AI model (LLM) to use

# Print a confirmation message that the agent was created
print(f"Agent '{fact_checker_agent.name}' created successfully!")

# A statement we want the Fact Checker agent to verify
# statement = "The Great Wall of China is visible from space with the naked eye."
statement = input("Enter a statement to fact-check: ")

# Display the statement we're going to check (in markdown format for nicer formatting)
print(f"Asking the Fact Checker to verify: '{statement}'")

# Run the Fact Checker agent on the input statement
# 'await' is used because running the agent is an asynchronous operation (it might take time)

@traceable(name="fact_checker_run")
async def test():
    response = await Runner.run(
        starting_agent = fact_checker_agent,  # The agent we created earlier
        input = statement                 # The statement we want it to fact-check
    )

    # Display the agent's response
    result = response.final_output

    print("\n🤖 Agent's Response:\n")
    print(f"Verdict: {result.is_true}")
    print(f"Explanation: {result.explanation}")
    
asyncio.run(test())    