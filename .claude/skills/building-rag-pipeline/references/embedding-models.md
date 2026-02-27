# Embedding Models

Unified embedding via LiteLLM. Choose by cost, dimension, and deployment needs.

## Model Comparison

| Model | Dims | Max Tokens | Cost/1M tokens | Best For |
|-------|------|-----------|-----------------|----------|
| text-embedding-3-small | 1536 | 8191 | $0.02 | Default choice, good quality/cost |
| text-embedding-3-large | 3072 | 8191 | $0.13 | Max quality, large corpora |
| Cohere embed-v3 | 1024 | 512 | $0.10 | Multilingual, search-optimized |
| nomic-embed-text (Ollama) | 768 | 8192 | Free (local) | Privacy, offline, no API costs |

## LiteLLM Embedding (Unified Interface)

```python
from litellm import embedding

# OpenAI
response = embedding(model="text-embedding-3-small", input=["Your text here"])
vector = response.data[0]["embedding"]  # List[float], len=1536

# Cohere
response = embedding(model="cohere/embed-english-v3.0", input=["Your text here"])

# Ollama (local) — requires: ollama pull nomic-embed-text
response = embedding(
    model="ollama/nomic-embed-text",
    input=["Your text here"],
    api_base="http://localhost:11434"
)
```

## Batch Embedding

```python
from litellm import embedding

def embed_batch(texts: list[str], model: str = "text-embedding-3-small",
                batch_size: int = 100) -> list[list[float]]:
    """Embed texts in batches to avoid API limits."""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = embedding(model=model, input=batch)
        batch_embeddings = [r["embedding"] for r in response.data]
        all_embeddings.extend(batch_embeddings)
    return all_embeddings

# Usage
texts = ["chunk 1", "chunk 2", "chunk 3"]
vectors = embed_batch(texts)
print(f"Embedded {len(vectors)} texts, dim={len(vectors[0])}")
```

## Dimension Reduction (Cost Saving)

OpenAI text-embedding-3 supports native dimension reduction:

```python
from litellm import embedding

# Reduce to 256 dims (saves storage, minor quality loss)
response = embedding(
    model="text-embedding-3-small",
    input=["Your text here"],
    dimensions=256  # Default 1536 -> reduced to 256
)
small_vector = response.data[0]["embedding"]  # len=256
```

## Choosing a Model

```
Need max quality?
├─ Yes → text-embedding-3-large (3072d)
└─ No → Need to run locally?
    ├─ Yes → nomic-embed-text via Ollama (free, 768d)
    └─ No → Need multilingual?
        ├─ Yes → Cohere embed-v3 (1024d)
        └─ No → text-embedding-3-small (1536d) ← default
```
