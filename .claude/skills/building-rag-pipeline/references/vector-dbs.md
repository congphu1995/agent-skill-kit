# Vector Databases

Setup and usage patterns for each supported vector DB.

## Decision Table

| DB | Best For | Persistence | Managed Cloud | Filtering |
|----|----------|------------|---------------|-----------|
| **Chroma** | Dev/prototype | In-memory or local | No | Metadata |
| **Qdrant** | Production self-host | Disk | Yes (Qdrant Cloud) | Payload filters |
| **Pinecone** | Managed cloud | Cloud | Yes (only) | Metadata |
| **pgvector** | Existing Postgres | Postgres | Via cloud PG | SQL WHERE |

## Chroma (Quick Start)

```bash
pip install chromadb
```

```python
import chromadb

# In-memory (dev)
client = chromadb.Client()

# Persistent (keeps data across restarts)
client = chromadb.PersistentClient(path="./chroma_data")

# Create collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # cosine | l2 | ip
)

# Add documents with embeddings
collection.add(
    ids=["doc1", "doc2"],
    documents=["First document text", "Second document text"],
    embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    metadatas=[{"source": "web"}, {"source": "pdf"}]
)

# Query
results = collection.query(
    query_embeddings=[[0.1, 0.2, ...]],
    n_results=5,
    where={"source": "pdf"}  # Metadata filter
)
print(results["documents"])  # [[matched docs]]
print(results["distances"])  # [[similarity scores]]
```

## Qdrant (Production)

```bash
# Docker setup
docker run -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant

pip install qdrant-client
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

client = QdrantClient(host="localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Upsert documents
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(id=1, vector=[0.1, 0.2, ...], payload={"source": "web", "text": "Doc 1"}),
        PointStruct(id=2, vector=[0.3, 0.4, ...], payload={"source": "pdf", "text": "Doc 2"}),
    ]
)

# Search with filter
results = client.query_points(
    collection_name="documents",
    query=[0.1, 0.2, ...],
    query_filter=Filter(must=[FieldCondition(key="source", match=MatchValue(value="pdf"))]),
    limit=5
)
for point in results.points:
    print(f"Score: {point.score}, Text: {point.payload['text']}")
```

## Pinecone (Managed Cloud)

```python
# pip install pinecone
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-api-key")
pc.create_index(name="documents", dimension=1536, metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"))
index = pc.Index("documents")

index.upsert(vectors=[
    {"id": "doc1", "values": [0.1, 0.2, ...], "metadata": {"source": "web"}},
])
results = index.query(vector=[0.1, 0.2, ...], top_k=5, include_metadata=True,
                      filter={"source": {"$eq": "pdf"}})
```

## pgvector (PostgreSQL Extension)

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE documents (
    id SERIAL PRIMARY KEY, content TEXT, source VARCHAR(50), embedding vector(1536)
);
INSERT INTO documents (content, source, embedding) VALUES ('Doc text', 'pdf', '[0.1,0.2,...]');

-- Cosine similarity search
SELECT id, content, 1 - (embedding <=> '[0.1,0.2,...]'::vector) AS similarity
FROM documents WHERE source = 'pdf'
ORDER BY embedding <=> '[0.1,0.2,...]'::vector LIMIT 5;

CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

## Choosing a Vector DB

```
Prototyping / small dataset?
├─ Yes → Chroma (zero config, in-process)
└─ No → Already using Postgres?
    ├─ Yes → pgvector (no new infra)
    └─ No → Want managed cloud?
        ├─ Yes → Pinecone (serverless)
        └─ No → Qdrant (self-hosted, production-ready)
```
