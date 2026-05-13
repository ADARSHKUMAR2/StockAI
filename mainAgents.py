import os
from dotenv import load_dotenv
import asyncio
load_dotenv(override=True)

from agents import Agent, Runner, OpenAIChatCompletionsModel
from langsmith import traceable, wrappers
from openai import AsyncOpenAI

from tavily_search import tavily_search
from research_agent import research_instructions, AnalysisSummary
from analyst_agent import analyst_instructions
from writer_agent import writer_instrcutions, FinalReport

# Get the OpenAI API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

client = wrappers.wrap_openai(AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
))

agent_model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini", 
    openai_client=client
)

# Create an AI agent called "Researcher"
researcher_agent = Agent(
    name = "Researcher",
    instructions = research_instructions,
    model = agent_model,
    tools = [tavily_search],
    output_type = AnalysisSummary)

analyst_agent = Agent(
    name = "Analyst",
    instructions = analyst_instructions,
    model = agent_model,
    output_type = AnalysisSummary,
)

# Create an AI agent called "Writer"
writer_agent = Agent(
    name = "Writer",
    instructions = writer_instrcutions,
    model = agent_model,
    output_type = FinalReport,
)

# manager_agent = Agent(
#     name="Manager",
#     instructions="""
#     You are a Project Manager. Your job is to fulfill the user's research request by coordinating your team:
#     1. Call the 'Researcher' to gather raw data.
#     2. Pass the researcher's output to the 'Analyst' to find insights.
#     3. Pass both the research and the analysis to the 'Writer' to create the final report.
#     4. Review the final report and return it to the user.
#     """,
#     model="openai/gpt-4o-mini",
#     # The Manager has all three workers as tools
#     tools=[researcher_agent, analyst_agent, writer_agent],
#     output_type=FinalReport
# )

# --- 3. Execution ---
@traceable(name="manager_orchestration")
async def run_pipeline(query: str):
    print(f"\n🚀 Starting pipeline for: '{query}'\n")
    
    # Step 1: Research
    print("🔎 Step 1: Researcher is gathering facts...")
    res_result = await Runner.run(researcher_agent, input=query)
    research_notes = res_result.final_output.summary
    
    # Step 2: Analyze
    print("📊 Step 2: Analyst is identifying trends...")
    ana_result = await Runner.run(analyst_agent, input=research_notes)
    analysis_notes = ana_result.final_output.summary
    
    # Step 3: Write
    print("✍️ Step 3: Writer is drafting the final report...")
    # We combine the previous outputs into one clean prompt for the writer
    writer_input = f"""
    Original Query: {query}
    
    Research Findings:
    {research_notes}
    
    Analysis & Trends:
    {analysis_notes}
    """
    
    writer_result = await Runner.run(writer_agent, input=writer_input)
    report = writer_result.final_output

    print("\n" + "="*50)
    print("🎯 FINAL REPORT GENERATED")
    print("="*50 + "\n")
    print(f"--- EXECUTIVE SUMMARY ---\n{report.short_summary}\n")
    print(f"--- FULL REPORT ---\n{report.markdown_report}\n")
    print(f"--- NEXT STEPS ---\n{', '.join(report.follow_up_questions)}\n")

if __name__ == "__main__":
    # You can change the query here to test different topics!
    query = "Why is Labubu so popular and what are the rarest Labubu collectibles?"
    asyncio.run(run_pipeline(query))