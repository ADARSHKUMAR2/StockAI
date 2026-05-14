from mcp_server import client, MODEL_NAME
from typing import Generator

# Define the summarize text function
def summarize_text(text: str, compression_ratio: float = 0.3) -> Generator[str, None, None]:
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
    _stream = client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        stream = True,
        temperature = 0.5,
    )
    partial = ""
    for chunk in _stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            partial += delta
            yield partial

