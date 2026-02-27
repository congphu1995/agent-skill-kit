# Memory Patterns

Three-tier memory for agents.

## Tier 1: Working Memory (Context Window)

The conversation itself. Cheapest, fastest, most reliable.

```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's my order status?"},
    {"role": "assistant", "content": "Your order #123 shipped yesterday."},
    {"role": "user", "content": "When will it arrive?"},  # Has context from above
]
```

### Conversation Buffer with Limit

```python
class ConversationBuffer:
    def __init__(self, max_messages: int = 20):
        self.messages: list[dict] = []
        self.max_messages = max_messages

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_messages(self, system_prompt: str) -> list[dict]:
        return [{"role": "system", "content": system_prompt}] + self.messages
```

### Conversation Summary (for long sessions)

```python
from litellm import completion

def summarize_old_messages(messages: list[dict], keep_recent: int = 10) -> list[dict]:
    if len(messages) <= keep_recent:
        return messages

    old = messages[:-keep_recent]
    recent = messages[-keep_recent:]

    summary_response = completion(
        model="claude-haiku-4-5-20251001",  # Cheap model for summarization
        messages=[{
            "role": "user",
            "content": f"Summarize this conversation concisely:\n{old}"
        }]
    )
    summary = summary_response.choices[0].message.content

    return [{"role": "system", "content": f"Previous conversation summary: {summary}"}] + recent
```

## Tier 2: Episodic Memory (Session/User)

Per-user or per-session memories that persist across conversations.

### Using Mem0

```python
from mem0 import Memory

m = Memory()

# Store memories
m.add("User prefers dark mode and metric units", user_id="alice")
m.add("User is working on an eKYC project", user_id="alice")

# Retrieve relevant memories
memories = m.search("What does the user prefer?", user_id="alice")
# Inject into system prompt
```

### Simple File-Based Memory

```python
import json
from pathlib import Path

class UserMemory:
    def __init__(self, storage_dir: str = ".memory"):
        self.dir = Path(storage_dir)
        self.dir.mkdir(exist_ok=True)

    def remember(self, user_id: str, fact: str):
        path = self.dir / f"{user_id}.json"
        facts = json.loads(path.read_text()) if path.exists() else []
        facts.append(fact)
        path.write_text(json.dumps(facts))

    def recall(self, user_id: str) -> list[str]:
        path = self.dir / f"{user_id}.json"
        return json.loads(path.read_text()) if path.exists() else []
```

## Tier 3: Long-Term Memory (Vector DB)

Knowledge base for retrieval. See `building-rag-pipeline` skill for full implementation.

## When to Read / Write / Forget

| Action | When |
|--------|------|
| **Read** | Every turn — inject relevant memories into context |
| **Write** | User states preference, completes task, or corrects agent |
| **Forget** | User requests deletion, memory contradicts newer info, or stale data |

## Memory Decision Tree

```
Does the agent need to remember across turns?
├─ No → Tier 1 (working memory) is sufficient
└─ Yes → Does it need to persist across sessions?
    ├─ No → Tier 1 with conversation buffer
    └─ Yes → Is it user-specific?
        ├─ Yes → Tier 2 (Mem0, Zep, or custom)
        └─ No → Tier 3 (vector DB / RAG)
```
