from mcp_server import client, MODEL_NAME
from actions.explanation import EXPLANATION_LEVELS
from typing import AsyncGenerator
from langsmith import wrappers, traceable

# Define the Quiz Me function

@traceable(name="Quiz Me Tool")
async def quiz_me(topic: str, level: int = 3, num_questions: int = 5) -> AsyncGenerator[str, None]:
    """Stream a quiz with numbered Qs then reveal answers after all questions."""
    if num_questions < 1 or num_questions > 15:
        yield "Error: num_questions must be between 1 and 15."
        return
    if not topic.strip():
        yield "Error: topic cannot be blank."
        return

    level_desc = EXPLANATION_LEVELS.get(level, "at an intermediate level")
    system_prompt = (
        "You are an AI quiz master. Generate a quiz of multiple‑choice questions "
        f"about {topic} {level_desc}. Number the questions. After listing all Qs, "
        "add an \nANSWER KEY section with the correct options."
    )

    try:
        _stream = await client.chat.completions.create(
            model=MODEL_NAME.model,
            messages=[{"role": "system", "content": system_prompt}],
            stream=True,
            temperature=0.7,
        )

        # The Safe Chunk Loop
        async for chunk in _stream:
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                delta = getattr(chunk.choices[0].delta, "content", None)
                if delta:
                    yield delta
                    
    # If ANYTHING goes wrong, yield the error so the Agent doesn't hang for 5 seconds!
    except Exception as e:
        yield f"\n[TOOL ERROR]: {str(e)}\n"
