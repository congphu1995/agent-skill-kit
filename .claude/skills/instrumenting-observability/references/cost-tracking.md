# Cost Tracking

Track and enforce LLM costs per user, session, and model.

## LiteLLM Cost Calculation

```python
import litellm

response = litellm.completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
)
cost = litellm.completion_cost(completion_response=response)
print(f"Cost: ${cost:.6f}")

# Manual calculation for known token counts
cost = litellm.completion_cost(
    model="anthropic/claude-sonnet-4-20250514",
    prompt_tokens=1000, completion_tokens=500,
)
```

## Per-User / Per-Session Tracking

```python
from collections import defaultdict
from dataclasses import dataclass, field
import litellm

@dataclass
class CostTracker:
    user_costs: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    session_costs: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    model_costs: dict[str, float] = field(default_factory=lambda: defaultdict(float))

    def record(self, user_id: str, session_id: str, model: str, cost: float):
        self.user_costs[user_id] += cost
        self.session_costs[session_id] += cost
        self.model_costs[model] += cost

tracker = CostTracker()

def tracked_completion(user_id: str, session_id: str, **kwargs):
    response = litellm.completion(**kwargs)
    cost = litellm.completion_cost(completion_response=response)
    tracker.record(user_id, session_id, kwargs["model"], cost)
    return response
```

## Budget Enforcement

```python
class BudgetExceeded(Exception):
    pass

USER_DAILY_BUDGET = 5.00   # $5/user/day
SESSION_BUDGET = 1.00      # $1/session

def enforce_budget(user_id: str, session_id: str):
    """Call before each LLM request."""
    if tracker.user_costs[user_id] >= USER_DAILY_BUDGET:
        raise BudgetExceeded(f"User {user_id} exceeded daily budget")
    if tracker.session_costs[session_id] >= SESSION_BUDGET:
        raise BudgetExceeded(f"Session {session_id} exceeded budget")

def safe_completion(user_id: str, session_id: str, **kwargs):
    enforce_budget(user_id, session_id)
    return tracked_completion(user_id, session_id, **kwargs)
```

## Cost Report

```python
def cost_report(t: CostTracker) -> str:
    lines = [f"  {m}: ${c:.4f}" for m, c in sorted(t.model_costs.items(), key=lambda x: -x[1])]
    return f"By Model:\n" + "\n".join(lines) + f"\nTotal: ${sum(t.model_costs.values()):.4f}"
```
