---
name: deploying-ai-systems
description: >
  Deploy AI systems: containerization, CI/CD with eval gates, K8s/serverless, durable execution, model serving.
  Use when user says "deploy", "Dockerfile", "CI/CD", "GitHub Actions", "containerize", "model serving",
  "production", "Temporal", "durable execution", "Docker compose", "Kubernetes".
  Do NOT use for observability (use instrumenting-observability) or for building code (use building-agent-core).
user-invocable: true
disable-model-invocation: true
---
# Deploying AI Systems

Containerize, set up CI/CD with eval gates, and deploy to production.

## Instructions

### Step 1: Identify deployment target
Route to the correct reference:
- Local Docker compose → `references/docker-ai-stacks.md`
- CI/CD pipeline → `references/cicd-with-eval-gates.md`
- Kubernetes → `references/k8s-configs.md`
- Model serving → `references/model-serving.md`
- Durable execution → `references/durable-execution.md`
- Managed platforms → `references/managed-deployment.md`

If unclear, default to Docker compose for development, CI/CD + Docker for production.

### Step 2: Read relevant reference
Load ONLY the needed reference. Do not load all 6 unless comparing approaches.

### Step 3: Generate Dockerfile
Every AI service needs a multi-stage Dockerfile:

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/
ENV PATH="/app/.venv/bin:$PATH"

# AI-specific: never bake secrets into image
# Pass API keys via environment at runtime
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key patterns:
- Multi-stage build to keep image small
- Never bake API keys or model credentials into images
- Always include HEALTHCHECK for container orchestrators
- Pin Python version and use `--frozen` for reproducible builds

### Step 4: Generate CI/CD with eval gates
Every CI pipeline MUST include eval gates. Minimal GitHub Actions example:

```yaml
name: AI Deploy Pipeline
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run pytest tests/ -x

  eval-gate:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx promptfoo@latest eval --ci
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      # Blocks merge if eval score drops below threshold

  deploy:
    needs: eval-gate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t myapp:${{ github.sha }} .
      - run: docker push myapp:${{ github.sha }}
```

### Step 5: Environment and secrets management
- Use `.env.example` (committed) + `.env` (gitignored) for local dev
- Use GitHub Secrets / AWS SSM / GCP Secret Manager for production
- Required env vars for AI services:
  - `LLM_API_KEY` — LLM provider key (never hardcode)
  - `MODEL_NAME` — model identifier (allows switching without redeploy)
  - `EMBEDDING_MODEL` — if RAG is used
  - `VECTOR_DB_URL` — if RAG is used
  - `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` — if observability is used

### Step 6: Verify deployment
```bash
# Build locally
docker build -t myapp:test .
docker run --env-file .env -p 8000:8000 myapp:test

# Test health endpoint
curl http://localhost:8000/health

# Test a sample request
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'

# Check logs for LLM connectivity
docker logs <container_id> 2>&1 | grep -i "error\|connected\|ready"
```

### Step 7: Produce deployment artifact
Write deployment configs to `.claude/artifacts/deploying-{project-name}.md` including:
- Dockerfile
- docker-compose.yml (if applicable)
- CI/CD pipeline YAML
- Environment variable list
- Deployment commands

## Checklist
- [ ] Dockerfile uses multi-stage build
- [ ] No secrets baked into images
- [ ] Health check endpoint exists and is configured
- [ ] CI pipeline includes eval gate (promptfoo or DeepEval)
- [ ] Environment variables documented
- [ ] Verified locally with docker build + run
