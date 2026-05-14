from mcp_server import client, MODEL_NAME
from typing import AsyncGenerator
from langsmith import wrappers, traceable

# Let's define the mapping from integers (1-5) to explanation levels
EXPLANATION_LEVELS = {
    1: "like I'm 5 years old",
    2: "like I'm 10 years old",
    3: "like a high school student",
    4: "like a college student",
    5: "like an expert in the field",
}

# In the MCP Server.ipynb file, update the docstring as shown below
@traceable(name="Explain Concept Tool")
async def explain_concept(question: str, level: int) -> AsyncGenerator[str, None]:
    """Stream an explanation of *question* at the requested *level* (1‑5). If 1, explanation would be like we are talking to a 5 year old and if 5, explanation would be technical and complex."""
    if not question.strip():
        yield "Error: question cannot be blank."
        return

    level_desc = EXPLANATION_LEVELS.get(level, "clearly and concisely")
    system_prompt = "You are a helpful AI Tutor. Explain the following concept " f"{level_desc}."
    try:
        _stream = await client.chat.completions.create(
            model=MODEL_NAME.model, 
            messages=[
                {"role": "system", "content": f"Explain this {EXPLANATION_LEVELS.get(level)}"},
                {"role": "user", "content": question}
            ],
            stream=True
        )
        async for chunk in _stream:
            # 1. Check if choices actually exists and is not empty
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                # 2. Now it is safe to access choices[0]
                delta = getattr(chunk.choices[0].delta, "content", None)
                if delta:
                    yield delta
    except Exception as e:
        yield f"Tool Error: {str(e)}"