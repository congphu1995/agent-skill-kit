# Docker Templates for AI/Agent Projects

## Python Agent Dockerfile (Multi-Stage)
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ src/
RUN useradd -m agent
USER agent
EXPOSE 8000
HEALTHCHECK --interval=30s CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## docker-compose: Agent + Vector DB + Redis
```yaml
services:
  agent:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on:
      chromadb: { condition: service_healthy }
      redis: { condition: service_healthy }
    restart: unless-stopped

  chromadb:
    image: chromadb/chroma:0.5.23
    ports: ["8100:8000"]
    volumes: [chroma_data:/chroma/chroma]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes: [redis_data:/data]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      retries: 3
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

volumes:
  chroma_data:
  redis_data:
```

## GPU-Enabled Dockerfile
```dockerfile
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir . && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu124
COPY src/ src/
RUN useradd -m agent
USER agent
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Next.js Dockerfile
```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```
