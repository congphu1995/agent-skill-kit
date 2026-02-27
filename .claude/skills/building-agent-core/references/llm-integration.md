# LLM Integration via LiteLLM

Unified interface for 100+ LLM providers.

## Basic Usage

```python
from litellm import completion

# OpenAI
response = completion(model="gpt-4o", messages=[{"role": "user", "content": "Hello"}])

# Anthropic
response = completion(model="claude-sonnet-4-20250514", messages=[{"role": "user", "content": "Hello"}])

# Ollama (local)
response = completion(model="ollama/llama3.1", messages=[{"role": "user", "content": "Hello"}],
                      api_base="http://localhost:11434")

# Google
response = completion(model="gemini/gemini-2.0-flash", messages=[{"role": "user", "content": "Hello"}])

print(response.choices[0].message.content)
```

## Environment Variables
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
# LiteLLM reads these automatically
```

## Fallback Chains

```python
from litellm import completion
import litellm

# Try models in order, fall back on failure
litellm.set_verbose = False

response = completion(
    model="gpt-4o",
    messages=messages,
    fallbacks=["claude-sonnet-4-20250514", "ollama/llama3.1"],
    num_retries=2
)
```

## Structured Output with Instructor

```python
import instructor
from litellm import completion
from pydantic import BaseModel

client = instructor.from_litellm(completion)

class Classification(BaseModel):
    category: str
    confidence: float

result = client.chat.completions.create(
    model="gpt-4o",
    response_model=Classification,
    messages=[{"role": "user", "content": "Classify: I was charged twice"}],
    max_retries=3
)
print(result.category, result.confidence)
```

## Caching

```python
import litellm
from litellm.caching.caching import Cache

# In-memory cache
litellm.cache = Cache()

# Redis cache (production)
litellm.cache = Cache(type="redis", host="localhost", port=6379)

# Same request hits cache (60%+ cost savings)
response = completion(model="gpt-4o", messages=messages)
```

## Cost Tracking

```python
from litellm import completion_cost

response = completion(model="gpt-4o", messages=messages)
cost = completion_cost(response)
print(f"Cost: ${cost:.6f}")
```

## Async Usage

```python
from litellm import acompletion
import asyncio

async def main():
    response = await acompletion(model="gpt-4o", messages=messages)
    return response

asyncio.run(main())
```

## Model Routing (Cost Optimization)

```python
# Use cheap model for easy tasks, expensive for hard
def smart_route(task_complexity: str, messages: list):
    if task_complexity == "simple":
        return completion(model="claude-haiku-4-5-20251001", messages=messages)
    elif task_complexity == "medium":
        return completion(model="gpt-4o-mini", messages=messages)
    else:
        return completion(model="claude-sonnet-4-20250514", messages=messages)
```

## LiteLLM Proxy (Team Use)

```bash
# Start proxy with config
litellm --config config.yaml --port 4000

# All team members use OpenAI-compatible endpoint
# OPENAI_API_BASE=http://localhost:4000
```
