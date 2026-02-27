# Rate Limiting for AI APIs

Protect LLM backends from abuse and control costs.

## slowapi -- Per-Route Limits

```python
# app/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)

async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={
        "title": "Too Many Requests", "status": 429,
        "detail": f"Rate limit exceeded: {exc.detail}",
    })
```

Wire into app and apply to endpoints:

```python
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

@router.post("/chat/completions")
@limiter.limit("10/minute")
async def chat_completion(request: Request, req: ChatRequest):
    ...
```

## Per-User Limits (API key)

```python
def get_api_key(request: Request) -> str:
    return request.headers.get("Authorization", "anonymous")

limiter = Limiter(key_func=get_api_key)
```

## Token-Budget Limiting

```python
from collections import defaultdict
from fastapi import HTTPException

_budgets: dict[str, int] = defaultdict(lambda: 100_000)  # tokens/day

async def check_budget(user_id: str, prompt_tokens: int):
    if _budgets[user_id] < prompt_tokens:
        raise HTTPException(429, "Daily token budget exhausted.")

async def deduct(user_id: str, usage: dict):
    _budgets[user_id] -= usage["prompt_tokens"] + usage["completion_tokens"]
```

Usage: call `check_budget` before the LLM call, `deduct` after.

## Redis Backend (production)

```python
limiter = Limiter(key_func=get_api_key, storage_uri="redis://localhost:6379/0")
```

```bash
pip install slowapi "slowapi[redis]"
```

Gives atomic counters shared across all uvicorn workers.
