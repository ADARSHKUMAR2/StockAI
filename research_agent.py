from pydantic import BaseModel

class AnalysisSummary(BaseModel):
    summary: str

research_instructions = """
## Context
You are a research agent with access to the Tavily search tool.

## Instruction
Given a user query, use the Tavily search tool to find relevant information and summarize the key findings.

## Input
- A research query from the user.

## Output
- A summary of key findings in a maximum of 5 bullet points.
"""

print("✅ Researcher AI agent is now ready")
