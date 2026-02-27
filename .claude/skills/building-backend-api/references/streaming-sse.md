# Streaming SSE Patterns

Server-Sent Events for token-by-token LLM streaming over HTTP.

## FastAPI SSE Endpoint

```python
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.models import ChatRequest
from app.dependencies import LLMClient, get_llm

router = APIRouter(tags=["chat"])

@router.post("/chat/completions")
async def chat_stream(req: ChatRequest, llm: LLMClient = Depends(get_llm)):
    async def event_generator():
        try:
            response = await llm.complete(
                model=req.model, messages=req.messages,
                temperature=req.temperature, max_tokens=req.max_tokens,
                stream=True,
            )
            async for chunk in response:
                delta = chunk.choices[0].delta
                if delta.content:
                    payload = json.dumps({"content": delta.content})
                    yield f"data: {payload}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

## Client-Side: fetch + ReadableStream

```javascript
async function streamChat(messages) {
  const res = await fetch("/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages, stream: true }),
  });
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop();
    for (const line of lines) {
      const data = line.replace(/^data: /, "");
      if (data === "[DONE]") return;
      const parsed = JSON.parse(data);
      if (parsed.error) throw new Error(parsed.error);
      document.getElementById("output").textContent += parsed.content;
    }
  }
}
```

## Collect Full Response While Streaming

```python
async def stream_and_collect(llm, messages, model="gpt-4o"):
    full = ""
    response = await llm.complete(model=model, messages=messages, stream=True)
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            full += delta.content
            yield delta.content
    # full now holds complete text for logging/billing
```

## Error Handling Notes

Once headers are sent (status 200), you cannot change the status code.
Send errors as SSE data events; the client checks for `error` field before processing `content`.
