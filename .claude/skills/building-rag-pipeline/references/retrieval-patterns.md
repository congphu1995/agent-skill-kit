# Retrieval Patterns

From basic vector search to agentic and graph RAG.

## Pattern 1: Basic Vector Search

```python
import chromadb
from litellm import embedding, completion

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection("docs")

def retrieve_and_generate(query: str, n_results: int = 5) -> str:
    """Basic RAG: retrieve chunks, stuff into prompt, generate."""
    query_emb = embedding(model="text-embedding-3-small", input=[query])
    results = collection.query(
        query_embeddings=[query_emb.data[0]["embedding"]],
        n_results=n_results
    )
    context = "\n\n---\n\n".join(results["documents"][0])
    response = completion(
        model="claude-sonnet-4-20250514",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n\n{context}"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content
```

## Pattern 2: Hybrid Search (BM25 + Vector)

Combines keyword matching with semantic search for better recall.

```python
# pip install rank-bm25 numpy
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, docs: list[str], embeds: list[list[float]], alpha: float = 0.5):
        self.docs, self.embeds = docs, np.array(embeds)
        self.alpha = alpha  # 0=BM25 only, 1=vector only
        self.bm25 = BM25Okapi([d.lower().split() for d in docs])

    def search(self, query: str, query_emb: list[float], top_k: int = 5) -> list[dict]:
        bm25 = self.bm25.get_scores(query.lower().split())
        bm25_norm = bm25 / (bm25.max() + 1e-8)
        qv = np.array(query_emb)
        cos = np.dot(self.embeds, qv) / (np.linalg.norm(self.embeds, axis=1) * np.linalg.norm(qv) + 1e-8)
        combined = self.alpha * cos + (1 - self.alpha) * bm25_norm
        top_idx = combined.argsort()[-top_k:][::-1]
        return [{"text": self.docs[i], "score": float(combined[i])} for i in top_idx]
```

## Pattern 3: Reranking with Cohere

Retrieve broadly, then rerank for precision.

```python
import cohere
from litellm import embedding

co = cohere.ClientV2(api_key="your-cohere-key")

def retrieve_and_rerank(query: str, documents: list[str],
                        query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """Two-stage: retrieve top-20 by vector, rerank to top-k."""
    # Stage 1: broad vector retrieval (cheap)
    # ... (retrieve top 20 candidates from vector DB)

    # Stage 2: rerank with Cohere (precise)
    reranked = co.rerank(
        model="rerank-v3.5",
        query=query,
        documents=documents[:20],  # Candidates from stage 1
        top_n=top_k
    )
    return [
        {"text": documents[r.index], "relevance": r.relevance_score}
        for r in reranked.results
    ]
```

## Pattern 4: Agentic RAG

The LLM decides when and what to retrieve, using retrieval as a tool.

```python
import json
from litellm import completion, embedding
import chromadb

collection = chromadb.PersistentClient(path="./chroma_data").get_or_create_collection("docs")

tools = [{"type": "function", "function": {
    "name": "search_kb", "description": "Search knowledge base for facts you don't know.",
    "parameters": {"type": "object", "properties": {
        "query": {"type": "string", "description": "Search query"}}, "required": ["query"]}
}}]

def search_kb(query: str) -> list[str]:
    emb = embedding(model="text-embedding-3-small", input=[query])
    return collection.query(query_embeddings=[emb.data[0]["embedding"]], n_results=5)["documents"][0]

def agentic_rag(user_query: str) -> str:
    messages = [{"role": "system", "content": "Use search tool when you need information."},
                {"role": "user", "content": user_query}]
    for _ in range(5):
        resp = completion(model="claude-sonnet-4-20250514", messages=messages, tools=tools)
        msg = resp.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content
        for tc in msg.tool_calls:
            results = search_kb(**json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(results)})
    return messages[-1].content
```

## Pattern 5: Graph RAG (Neo4j)

Enrich vector results with knowledge graph relationships.

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def graph_enhanced_retrieval(vector_results: list[str], entities: list[str]) -> list[str]:
    """Enrich vector results with related entities from knowledge graph."""
    with driver.session() as session:
        result = session.run("""
            MATCH (e:Entity)-[r]->(related:Entity)
            WHERE e.name IN $entities
            RETURN e.name, type(r) AS rel, related.name, related.description LIMIT 10
        """, entities=entities)
        enriched = [f"{r['e.name']} -{r['rel']}-> {r['related.name']}" for r in result]
    return vector_results + enriched
```

## Choosing a Pattern

```
Simple Q&A over documents?
├─ Yes → Pattern 1 (basic vector search)
└─ No → Need keyword + semantic?
    ├─ Yes → Pattern 2 (hybrid BM25 + vector)
    └─ No → Need high precision on top results?
        ├─ Yes → Pattern 3 (reranking)
        └─ No → Agent decides when to retrieve?
            ├─ Yes → Pattern 4 (agentic RAG)
            └─ No → Need entity relationships?
                └─ Yes → Pattern 5 (graph RAG)
```
