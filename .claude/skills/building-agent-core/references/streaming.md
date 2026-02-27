# Streaming Patterns

Stream LLM responses for real-time UX.

## LiteLLM Streaming

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
```

## Async Streaming

```python
from litellm import acompletion
import asyncio

async def stream_response(messages):
    response = await acompletion(model="gpt-4o", messages=messages, stream=True)
    async for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

async def main():
    async for token in stream_response([{"role": "user", "content": "Hello"}]):
        print(token, end="", flush=True)

asyncio.run(main())
```

## SSE (Server-Sent Events) for Web

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from litellm import completion

app = FastAPI()

@app.post("/chat")
async def chat(message: str):
    async def generate():
        response = completion(
            model="gpt-4o",
            messages=[{"role": "user", "content": message}],
            stream=True
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield f"data: {content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

## Collecting Full Response While Streaming

```python
def stream_and_collect(messages):
    full_content = ""
    response = completion(model="gpt-4o", messages=messages, stream=True)
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            full_content += content
            yield content  # Stream to client
    # full_content now has complete response for logging/storage
    return full_content
```

## Tool Calls in Streaming

Tool calls arrive as deltas across multiple chunks. Accumulate them:

```python
tool_calls = {}
for chunk in response:
    delta = chunk.choices[0].delta
    if delta.tool_calls:
        for tc in delta.tool_calls:
            idx = tc.index
            if idx not in tool_calls:
                tool_calls[idx] = {"id": tc.id, "name": tc.function.name, "args": ""}
            if tc.function.arguments:
                tool_calls[idx]["args"] += tc.function.arguments
```
