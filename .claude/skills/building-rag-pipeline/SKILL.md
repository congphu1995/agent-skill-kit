---
name: building-rag-pipeline
description: >
  Build RAG pipelines: embeddings, vector DB integration, chunking, hybrid search, reranking, agentic RAG, graph RAG.
  Use when user says "RAG pipeline", "vector search", "embeddings", "retrieval system", "knowledge base",
  "vector database", "chunking strategy", "agentic RAG", "graph RAG", "semantic search", "document retrieval".
  Do NOT use for general agent logic (use building-agent-core).
---
# Building RAG Pipelines

Generate RAG systems: embeddings, vector storage, chunking, retrieval, reranking, and evaluation.

## Instructions

### Step 1: Identify data sources
Ask the user:
- What documents/data will be ingested? (PDFs, web pages, code, structured data)
- How large is the corpus? (hundreds, thousands, millions of documents)
- How often does the data change? (static, daily, real-time)
- What query patterns are expected? (keyword, semantic, hybrid)

Do not proceed until data sources are clear.

### Step 2: Choose embedding model
Read `references/embedding-models.md`. Select based on:
- Cloud API (OpenAI, Cohere) vs local (Ollama/nomic-embed-text)
- Dimension requirements and cost constraints
- Language support needs

### Step 3: Setup vector database
Read `references/vector-dbs.md`. Choose based on:
- **Prototyping**: Chroma (in-process, zero config)
- **Production**: Qdrant (self-hosted, high performance)
- **Managed cloud**: Pinecone (zero ops)
- **Existing Postgres**: pgvector (no new infra)

### Step 4: Implement chunking strategy
Read `references/chunking-strategies.md`. Decide:
- Chunk size (512-1024 tokens optimal for retrieval)
- Overlap amount (10-20% of chunk size)
- Splitting method (recursive, semantic, or document-aware)

### Step 5: Build retrieval pipeline
Read `references/retrieval-patterns.md`. Choose pattern:
- **Basic**: vector similarity search (start here)
- **Hybrid**: BM25 + vector search (better recall)
- **Reranked**: add Cohere reranker (better precision)
- **Agentic**: LLM decides when and what to retrieve
- **Graph RAG**: entity relationships via Neo4j

### Step 6: Evaluate with RAGAS
Read `references/rag-evaluation.md`. Measure:
- Faithfulness (answer grounded in context?)
- Answer relevancy (answer addresses the question?)
- Context precision/recall (right chunks retrieved?)

Run evaluation before deploying. Integrate into CI with promptfoo.

## Quick Start (Minimal RAG)

```python
# pip install litellm chromadb langchain-text-splitters
from litellm import embedding
import chromadb

client = chromadb.Client()
collection = client.create_collection("docs")

texts = ["Your document chunks here"]
resp = embedding(model="text-embedding-3-small", input=texts)
embeddings = [r["embedding"] for r in resp.data]

collection.add(ids=["1"], documents=texts, embeddings=embeddings)

query_resp = embedding(model="text-embedding-3-small", input=["user query"])
results = collection.query(query_embeddings=[query_resp.data[0]["embedding"]], n_results=3)
```
