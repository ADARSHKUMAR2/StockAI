from mcp_server import client, MODEL_NAME
from typing import AsyncGenerator
from langsmith import wrappers, traceable

# Define the summarize text function
@traceable(name="Summarize Text Tool")
async def summarize_text(text: str, compression_ratio: float = 0.3) -> AsyncGenerator[str, None]:
    """Stream a summary of *text* compressed to roughly *compression_ratio* length.

    *compression_ratio* should be between 0.1 and 0.8.
    """
    if not text.strip():
        yield "Error: text cannot be blank."
        return
    ratio = max(0.1, min(compression_ratio, 0.8))
    system_prompt = (
        "You are a world‑class summarizer. Reduce the following text to about "
        f"{int(ratio*100)}% of its original length while preserving key ideas."
    )
    _stream = await client.chat.completions.create(
        model = MODEL_NAME.model,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        stream = True,
        temperature = 0.5,
    )

    async for chunk in _stream:
        # 1. Check if choices actually exists and is not empty
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            # 2. Now it is safe to access choices[0]
            delta = getattr(chunk.choices[0].delta, "content", None)
            if delta:
                yield delta
