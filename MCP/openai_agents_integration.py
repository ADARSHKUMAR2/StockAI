# Let's Build the AI agent
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled
from mcp_client import mcp_tool
from mcp_server import MODEL_NAME, client
import asyncio

agent = Agent(
    name = "Smart Assistant",
    instructions = """
    Context
    -------
    You are an AI assistant with access to an MCP server exposing **four streaming tools**:

    1. **explain_concept**  
    Arguments: { "question": <str>, "level": <int 1‑5> }  
    • Streams an explanation of any concept at the requested depth.

    2. **summarize_text**  
    Arguments: { "text": <str>, "compression_ratio": <float 0.1‑0.8> }  
    • Streams a concise summary ~compression_ratio × original length.

    3. **generate_flashcards**  
    Arguments: { "topic": <str>, "num_cards": <int 1‑20> }  
    • Streams JSON‑lines flashcards: one card per line `{ "q":…, "a":… }`.

    4. **quiz_me**  
    Arguments: { "topic": <str>, "level": <int 1‑5>, "num_questions": <int 1‑15> }  
    • Streams an MC‑question quiz, then an ANSWER KEY section.

    5. **send_email**.
    Arguments: { "to_address": <str>, "subject": <str>, "body": <str> }
    
    If a user asks you to explain a concept or generate a quiz AND email it to them, follow these steps:
    1. Call the appropriate learning tool (e.g., `explain_concept`).
    2. Wait for the response.
    3. Take the content generated from step 1, and call the `send_email` tool.

    Objective
    ---------
    Help users learn by:
    • Explaining concepts at the depth they request.  
    • Summarising long passages.  
    • Generating flashcards for self‑study.  
    • Quizzing them interactively.

    How to respond
    --------------
    • For each user request, decide which tool (if any) fulfils it best.  
    • Call the tool via MCP by returning *only* the JSON with `"tool"` and `"arguments"` (no extra text).  
    • If a follow‑up conversation is needed (e.g., clarification), ask the user first.  
    • If no tool fits, answer directly in plain language.

    Examples
    --------
    User: “Explain quantum tunnelling like I’m 10.”  
    → Call `explain_concept` with { "question": "quantum tunnelling", "level": 2 }

    User: “Summarise this article to 20 %.” + <article text>  
    → Call `summarize_text` with { "text": "...", "compression_ratio": 0.2 }

    Chat capability
    ---------------
    After each tool call completes (streaming back to the user), remain in the chat loop ready for the next user turn.
    """,
    model = MODEL_NAME,
    mcp_servers = [mcp_tool],
)

# This code snippet is implementing a conversational loop with an AI agent that uses MCP tools.

# Opens a connection with an MCP tool. 
# This lets our AI agent interact with an external tool (e.g., image generator, calculator, etc.) over a standard protocol using SSE (Server-Sent Events).
# open SSE channels

# This is the core AI agent execution step. It runs your agent with the new_input.
async def main():
    await mcp_tool.connect() 

    result = None

    while True:
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit"}:
            break
            
        # If there was a previous interaction (result is not None), it appends the new user message to the past messages (maintaining conversation context).
        if result is not None:
            new_input = result.to_input_list() + [{"role": "user", "content": user_input}]
        else:
            new_input = [{"role": "user", "content": user_input}]
        
        result = await Runner.run(starting_agent = agent, input = new_input)
        print("\nAssistant:")
        print(result.final_output)
        # await viewTools(result)

    
async def viewTools(res):
    # Let's view the list of tools that have been called
    for i in res.to_input_list():
        for key in i.keys():
            if key == 'arguments':
                print("Tool: ", i['name'])
                print("Arguments: ", i['arguments'])


asyncio.run(main())