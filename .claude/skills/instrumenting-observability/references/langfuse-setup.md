# Langfuse Setup

Open-source LLM observability. Self-hostable, prompt versioning, cost tracking built-in.

## Installation

```bash
pip install langfuse litellm
```

## Environment Variables

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://cloud.langfuse.com"  # or self-hosted URL
```

## Tracing with @observe

```python
from langfuse.decorators import observe, langfuse_context
import litellm

@observe()
def my_agent(user_input: str) -> str:
    """Automatically traced: latency, input/output, nested spans."""
    context = retrieve_context(user_input)
    return generate_response(user_input, context)

@observe()
def retrieve_context(query: str) -> str:
    # Child span of my_agent
    return vector_db.search(query, limit=5)

@observe()
def generate_response(query: str, context: str) -> str:
    response = litellm.completion(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": query},
        ],
    )
    langfuse_context.score_current_trace(name="user_feedback", value=1.0)
    return response.choices[0].message.content
```

## LiteLLM Callback Integration

```python
import litellm

# One-line setup: all LiteLLM calls traced automatically
litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]

response = litellm.completion(
    model="anthropic/claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Hello"}],
    metadata={
        "trace_name": "my-agent-call",
        "trace_user_id": "user-42",
        "tags": ["production"],
    },
)
```

## Prompt Versioning

```python
from langfuse import Langfuse
client = Langfuse()

# Create prompt (in CI or admin script)
client.create_prompt(
    name="agent-system-prompt",
    prompt="You are a helpful assistant. Context: {{context}}",
    labels=["production"],
)

# Fetch and use (cached, auto-links to traces)
prompt = client.get_prompt("agent-system-prompt", label="production")
compiled = prompt.compile(context="relevant info here")
```

## Docker Self-Host

```yaml
# docker-compose.yml
version: "3.8"
services:
  langfuse:
    image: langfuse/langfuse:2
    ports: ["3000:3000"]
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/langfuse
      NEXTAUTH_SECRET: your-secret-here
      NEXTAUTH_URL: http://localhost:3000
      SALT: your-salt-here
    depends_on: [db]
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: langfuse
    volumes: [langfuse_data:/var/lib/postgresql/data]
volumes:
  langfuse_data:
```

```bash
docker compose up -d
# Access at http://localhost:3000, set LANGFUSE_HOST=http://localhost:3000
```

## Complete Working Example

```python
"""Full agent with Langfuse observability."""
import litellm
from langfuse.decorators import observe, langfuse_context

litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]

@observe()
def run_agent(user_id: str, session_id: str, query: str) -> str:
    langfuse_context.update_current_trace(
        user_id=user_id, session_id=session_id, tags=["production"],
    )
    tool_result = use_tool(query)
    response = litellm.completion(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f"Tool: {tool_result}"},
                  {"role": "user", "content": query}],
    )
    langfuse_context.score_current_trace(name="completed", value=1.0)
    return response.choices[0].message.content

@observe()
def use_tool(query: str) -> str:
    return "Weather: 72F, sunny" if "weather" in query.lower() else "No tool"

if __name__ == "__main__":
    print(run_agent("user-1", "sess-1", "What is the weather?"))
```
