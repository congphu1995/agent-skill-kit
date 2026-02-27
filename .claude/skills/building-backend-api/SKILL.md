---
name: building-backend-api
description: >
  Build FastAPI backends with AI patterns: streaming SSE, async LLM calls, rate limiting, model routing, webhooks.
  Use when user says "FastAPI", "backend", "API server", "streaming endpoint", "SSE", "webhook",
  "REST API for agent", "API wrapper", "backend for AI".
  Do NOT use for frontend (use building-ai-frontend) or for agent logic (use building-agent-core).
---
# Building Backend API

Generate FastAPI backends for AI-powered applications with production patterns.

## Instructions

### Step 1: Identify API requirements
Ask (if not clear):
- What LLM operations does the API expose? (chat, completion, embeddings, agent runs)
- Does the client need streaming (SSE)?
- What auth/rate-limiting model? (API key, JWT, per-user quotas)
- Any webhook or callback needs?

### Step 2: Scaffold FastAPI app
Read `references/fastapi-patterns.md`. Minimal structure:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import litellm

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str
    model: str = "anthropic/claude-sonnet-4-20250514"

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(req: ChatRequest):
    response = await litellm.acompletion(model=req.model, messages=[{"role": "user", "content": req.message}])
    return {"response": response.choices[0].message.content}
```

Build on this with: app factory/lifespan, DI for LLM client, Pydantic response models.

### Step 3: Add streaming (if needed)
Read `references/streaming-sse.md`. Implement:
- `StreamingResponse` with `text/event-stream`
- Token-by-token yield from async LLM call
- `[DONE]` sentinel and error events inside the stream
- Client-side EventSource reconnection guidance

### Step 4: Add rate limiting
Read `references/rate-limiting.md`. Configure:
- slowapi per-route limits (e.g., `10/minute` for heavy LLM calls)
- Token-budget limiting for cost control
- Redis backend for multi-worker deployments

### Step 5: Add health checks and middleware
- `GET /health` returning `{"status": "ok"}` and model reachability
- Request-ID middleware (propagate to LLM calls for tracing)
- Structured JSON logging with request duration
- Global exception handler returning RFC 7807 problem+json

### Step 6: Verify
- Run `uvicorn app.main:app --reload` and hit `/docs`
- Confirm streaming endpoint with `curl -N`
- Confirm rate limiter returns 429 after threshold

## Reference files
- `references/fastapi-patterns.md` -- App structure, models, DI, error handling
- `references/streaming-sse.md` -- SSE endpoints and client patterns
- `references/rate-limiting.md` -- slowapi, token budgets, Redis
