# Output Schemas

Structured output design for reliable LLM responses.

## Why Structured Output
- Predictable format for downstream processing
- Validation catches LLM errors
- Type safety in application code
- Self-documenting API contracts

## Pydantic Models

```python
from pydantic import BaseModel, Field
from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class TicketClassification(BaseModel):
    category: str = Field(description="One of: billing, technical, general")
    priority: int = Field(ge=1, le=5, description="1=lowest, 5=critical")
    sentiment: Sentiment
    summary: str = Field(max_length=200, description="One-sentence summary")
    requires_human: bool = Field(description="True if agent cannot handle alone")
```

## Instructor (Structured Output via Tool Calling)

```python
import instructor
from litellm import completion

client = instructor.from_litellm(completion)

result = client.chat.completions.create(
    model="gpt-4o",
    response_model=TicketClassification,
    messages=[
        {"role": "system", "content": "Classify support tickets."},
        {"role": "user", "content": ticket_text}
    ],
    max_retries=3  # Auto-retry on validation failure
)
# result is a validated TicketClassification instance
print(result.category, result.priority)
```

## PydanticAI Native Structured Output

```python
from pydantic_ai import Agent

agent = Agent(
    "openai:gpt-4o",
    result_type=TicketClassification,
    system_prompt="Classify support tickets."
)
result = agent.run_sync("I was charged twice for my subscription")
print(result.data)  # TicketClassification instance
```

## Anthropic Tool Use for Structured Output

```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[{
        "name": "classify_ticket",
        "description": "Classify a support ticket",
        "input_schema": TicketClassification.model_json_schema()
    }],
    tool_choice={"type": "tool", "name": "classify_ticket"},
    messages=[{"role": "user", "content": ticket_text}]
)
data = TicketClassification(**response.content[0].input)
```

## Nested Models

```python
class Action(BaseModel):
    tool: str = Field(description="Tool to invoke")
    args: dict = Field(description="Tool arguments")
    reason: str = Field(description="Why this action")

class AgentPlan(BaseModel):
    goal: str
    steps: list[Action]
    estimated_calls: int = Field(ge=1, le=20)
```

## Best Practices
- Use `Enum` for categorical fields (prevents hallucinated categories)
- Set `max_length` on string fields (controls verbosity)
- Use `Field(description=...)` (guides the LLM)
- Use `max_retries` with Instructor (auto-fixes validation errors)
- Keep schemas flat when possible (nested = harder for LLM)
- Test with edge cases (empty input, very long input, ambiguous input)
