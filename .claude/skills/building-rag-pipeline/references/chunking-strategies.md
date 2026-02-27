# Chunking Strategies

How you split documents directly impacts retrieval quality.

## Chunk Size Guidelines

| Chunk Size | Use Case | Trade-off |
|-----------|----------|-----------|
| 256 tokens | Q&A, precise retrieval | High precision, may miss context |
| 512 tokens | General RAG (default) | Good balance |
| 1024 tokens | Summarization, complex topics | More context, lower precision |

**Overlap**: 10-20% of chunk size (e.g., 100 tokens overlap for 512 token chunks).

## Recursive Character Splitting (Default)

Splits on natural boundaries: paragraphs, sentences, then characters.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]
)

text = open("document.txt").read()
chunks = splitter.split_text(text)
print(f"Created {len(chunks)} chunks")
```

## Markdown-Aware Splitting

Respects heading boundaries for structured documents.

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

headers_to_split_on = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]
md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_chunks = md_splitter.split_text(markdown_text)

# Further split large sections
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
final_chunks = text_splitter.split_documents(md_chunks)
```

## Semantic Chunking

Groups sentences by embedding similarity. Better boundaries, higher cost.

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

semantic_splitter = SemanticChunker(
    OpenAIEmbeddings(model="text-embedding-3-small"),
    breakpoint_threshold_type="percentile", breakpoint_threshold_amount=95
)
chunks = semantic_splitter.split_text(text)
```

## Code Splitting

```python
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=1000, chunk_overlap=100
)
chunks = python_splitter.split_text(open("module.py").read())
```

## Complete Chunking Pipeline

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from litellm import embedding

def chunk_and_embed(text: str, model: str = "text-embedding-3-small",
                    chunk_size: int = 512, chunk_overlap: int = 50
                    ) -> list[dict]:
    """Split text into chunks and embed each chunk."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)

    response = embedding(model=model, input=chunks)
    return [
        {"text": chunk, "embedding": r["embedding"], "index": i}
        for i, (chunk, r) in enumerate(zip(chunks, response.data))
    ]

# Usage
results = chunk_and_embed(open("document.txt").read())
print(f"Chunked into {len(results)} pieces, dim={len(results[0]['embedding'])}")
```

## Choosing a Strategy

```
Structured docs (Markdown, HTML)?
├─ Yes → Markdown/HTML-aware splitting
└─ No → Source code?
    ├─ Yes → Language-aware splitting
    └─ No → Need best boundaries?
        ├─ Yes (budget allows) → Semantic chunking
        └─ No → Recursive character splitting (default)
```
