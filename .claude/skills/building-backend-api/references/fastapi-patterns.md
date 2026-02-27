# FastAPI Patterns for AI Backends
## Project Structure

```
app/
  main.py          # App factory, lifespan, routers
  config.py        # Settings via pydantic-settings
  dependencies.py  # DI providers (LLM client)
  models.py        # Pydantic request/response schemas
  routers/
    chat.py        # Chat / completion endpoints
    health.py      # Health + readiness
  middleware.py    # Request-ID, logging, error handler
```

## Pydantic Models

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    messages: list[dict[str, str]] = Field(..., min_length=1)
    model: str = Field(default="gpt-4o")
    stream: bool = False
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=16384)

class ChatResponse(BaseModel):
    id: str
    content: str
    model: str
    usage: dict[str, int]
```

## Dependency Injection for LLM Client

```python
# app/dependencies.py
from litellm import acompletion

class LLMClient:
    async def complete(self, **kwargs):
        return await acompletion(**kwargs)

_llm = LLMClient()

def get_llm() -> LLMClient:
    return _llm
```

## App Factory with Lifespan + CORS

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, health
from app.middleware import add_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # startup / shutdown logic here

def create_app() -> FastAPI:
    app = FastAPI(title="AI Backend", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"],
        allow_methods=["*"], allow_headers=["*"],
    )
    add_middleware(app)
    app.include_router(health.router)
    app.include_router(chat.router, prefix="/v1")
    return app

app = create_app()
```

## Async Endpoint with LLM Call

```python
# app/routers/chat.py
import uuid
from fastapi import APIRouter, Depends
from app.models import ChatRequest, ChatResponse
from app.dependencies import LLMClient, get_llm

router = APIRouter(tags=["chat"])

@router.post("/chat/completions", response_model=ChatResponse)
async def chat_completion(req: ChatRequest, llm: LLMClient = Depends(get_llm)):
    response = await llm.complete(
        model=req.model, messages=req.messages,
        temperature=req.temperature, max_tokens=req.max_tokens,
    )
    c = response.choices[0]
    return ChatResponse(
        id=str(uuid.uuid4()), content=c.message.content,
        model=response.model, usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
        },
    )
```

## Error Handling & Request-ID Middleware

```python
# app/middleware.py
import uuid, time, logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
logger = logging.getLogger("ai_backend")

async def error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={
        "type": "about:blank", "title": "Internal Server Error", "status": 500,
        "detail": "An unexpected error occurred.",
    })

def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def request_id_mw(request: Request, call_next):
        rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        logger.info("req", extra={"path": request.url.path,
            "ms": round((time.perf_counter() - start) * 1000, 1)})
        return response
    app.add_exception_handler(Exception, error_handler)
```

## Health Check

```python
# app/routers/health.py
from fastapi import APIRouter
router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok"}
```
## Running

```bash
pip install "fastapi[standard]" litellm pydantic-settings
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
