# Tool Installation

## Ollama (Local LLM)

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.1        # 8B general purpose
ollama pull nomic-embed-text # Embeddings
ollama pull codellama        # Code generation

# Verify
ollama list
ollama run llama3.1 "Hello, world"

# API endpoint (default)
curl http://localhost:11434/api/tags
```

LiteLLM usage: `completion(model="ollama/llama3.1", api_base="http://localhost:11434")`

## Docker

```bash
# Install (Ubuntu)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker  # Or logout/login

# Verify
docker --version
docker run hello-world
docker ps
```

## Chroma (Vector DB)

```bash
# Option 1: pip (embedded, for development)
pip install chromadb

# Python usage
import chromadb
client = chromadb.Client()  # In-memory
# client = chromadb.PersistentClient(path="./chroma_data")  # Persistent

# Option 2: Docker (server mode)
docker run -d -p 8000:8000 --name chromadb chromadb/chroma

# Verify
curl http://localhost:8000/api/v1/heartbeat
```

## Qdrant (Vector DB)

```bash
# Docker
docker run -d -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  --name qdrant qdrant/qdrant

# Verify
curl http://localhost:6333/healthz

# Python client
pip install qdrant-client

# Usage
from qdrant_client import QdrantClient
client = QdrantClient("localhost", port=6333)
print(client.get_collections())
```

## LiteLLM Proxy (Multi-provider gateway)

```bash
# Install
pip install 'litellm[proxy]'

# Quick start (single model)
litellm --model gpt-4o --port 4000

# With config file
cat > litellm_config.yaml << 'EOF'
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
  - model_name: claude-sonnet
    litellm_params:
      model: claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: local-llama
    litellm_params:
      model: ollama/llama3.1
      api_base: http://localhost:11434
EOF

litellm --config litellm_config.yaml --port 4000

# Verify
curl http://localhost:4000/health
curl http://localhost:4000/v1/models
```

## Redis (Caching)

```bash
docker run -d -p 6379:6379 --name redis redis:alpine
# Verify
docker exec redis redis-cli ping  # PONG
```
