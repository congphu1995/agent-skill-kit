# FastAPI + Agent Project Template

## Directory Structure
```
<project-name>/
  src/
    __init__.py
    main.py              # FastAPI entry point
    config.py            # pydantic-settings config
    agents/__init__.py, base.py, chat_agent.py
    tools/__init__.py
    rag/__init__.py
    models/schemas.py
    routers/agent_router.py, health.py
  tests/unit/, integration/, conftest.py
  evals/datasets/, eval_runner.py
  docs/
  scripts/
  .env.example, .gitignore, pyproject.toml, Dockerfile, Makefile
```

## pyproject.toml
```toml
[project]
name = "<project-name>"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "litellm>=1.50",
    "pydantic>=2.9",
    "pydantic-settings>=2.6",
    "httpx>=0.28",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.24", "ruff>=0.8", "httpx"]
rag = ["chromadb>=0.5", "sentence-transformers>=3.3"]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## main.py
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routers import agent_router, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # Startup/shutdown hooks

app = FastAPI(title="Agent Service", lifespan=lifespan)
app.include_router(health.router)
app.include_router(agent_router.router, prefix="/api/agent")
```

## config.py
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    llm_model: str = "gpt-4o"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    redis_url: str = "redis://localhost:6379"
    log_level: str = "INFO"
    model_config = {"env_file": ".env"}
```

## .env.example
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_MODEL=gpt-4o
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
```

## Makefile
```makefile
dev:
	uvicorn src.main:app --reload --port 8000
test:
	pytest tests/ -v
lint:
	ruff check . && ruff format --check .
docker:
	docker compose up --build
```
