# API Documentation Templates

## OpenAPI / FastAPI Auto-Docs

FastAPI generates OpenAPI schema automatically. Enhance with:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Agent API",
    description="AI agent backend with streaming support",
    version="1.0.0",
)

@app.post("/chat", response_model=ChatResponse, summary="Send message to agent")
async def chat(request: ChatRequest):
    """Send a message to the agent and receive a response.

    - **message**: User's input message
    - **session_id**: Optional session ID for conversation continuity
    - Returns agent response with sources and metadata
    """
```

## REST API Documentation Template

```markdown
# API Reference

## Base URL
`https://api.example.com/v1`

## Authentication
Bearer token in Authorization header:
`Authorization: Bearer <token>`

## Endpoints

### POST /chat
Send a message to the agent.

**Request:**
```json
{
  "message": "What is our refund policy?",
  "session_id": "sess_abc123",
  "stream": false
}
```

**Response:**
```json
{
  "response": "Our refund policy allows...",
  "sources": ["policy.md#section-3"],
  "tokens_used": 245,
  "model": "gpt-4o",
  "latency_ms": 1230
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 400  | Invalid request body |
| 401  | Missing or invalid token |
| 429  | Rate limit exceeded |
| 500  | Internal server error |
```

## Agent Tool Documentation

For each tool the agent uses, document:
- **Name**: verb_noun format
- **Description**: what it does
- **Parameters**: with types and constraints
- **Returns**: expected output shape
- **Risk level**: read-only / reversible / irreversible
- **Example**: input/output pair
