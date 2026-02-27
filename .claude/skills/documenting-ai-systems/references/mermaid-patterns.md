# Mermaid Diagram Patterns for AI Systems

## Agent Flow (Flowchart)

```mermaid
flowchart TD
    U[User Input] --> R[Router Agent]
    R -->|billing| B[Billing Agent]
    R -->|technical| T[Tech Agent]
    R -->|general| G[General Agent]
    B --> O[Output]
    T --> O
    G --> O
```

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Intake
    Intake --> Processing: classify
    Processing --> Review: needs_approval
    Processing --> Complete: auto_approved
    Review --> Complete: approved
    Review --> Processing: revision_needed
    Complete --> [*]
```

## Sequence Diagram (Agent-Tool Interaction)

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant T as Tool
    participant L as LLM

    U->>A: Query
    A->>L: Generate plan
    L-->>A: Use search_docs tool
    A->>T: search_docs(query)
    T-->>A: Results
    A->>L: Generate response with context
    L-->>A: Final answer
    A-->>U: Response
```

## System Architecture

```mermaid
graph TB
    subgraph Frontend
        UI[Chat UI]
    end
    subgraph Backend
        API[FastAPI]
        Agent[Agent Core]
    end
    subgraph Data
        VDB[(Vector DB)]
        DB[(PostgreSQL)]
        Redis[(Redis Cache)]
    end
    subgraph External
        LLM[LLM Provider]
        Langfuse[Langfuse]
    end

    UI -->|SSE| API
    API --> Agent
    Agent --> LLM
    Agent --> VDB
    Agent --> DB
    Agent --> Redis
    Agent --> Langfuse
```

## RAG Pipeline

```mermaid
flowchart LR
    D[Documents] --> C[Chunker]
    C --> E[Embedder]
    E --> V[(Vector DB)]
    Q[Query] --> E2[Embedder]
    E2 --> V
    V -->|Top-K| R[Reranker]
    R --> G[Generator LLM]
    G --> A[Answer]
```

## Tips
- Use `flowchart` for agent routing and data flow
- Use `stateDiagram-v2` for state machines
- Use `sequenceDiagram` for request/response flows
- Use `graph TB/LR` for system architecture
- Keep diagrams focused — one concept per diagram
