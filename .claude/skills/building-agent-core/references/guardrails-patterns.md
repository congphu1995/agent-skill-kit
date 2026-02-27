# Guardrails Patterns

Safety rails for AI agents.

## Input Validation

### Prompt Injection Detection

```python
def check_injection(user_input: str) -> bool:
    """Basic prompt injection detection."""
    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all instructions",
        "you are now",
        "system prompt",
        "reveal your instructions",
        "forget everything",
    ]
    lower = user_input.lower()
    return any(pattern in lower for pattern in suspicious_patterns)

# LLM-based detection (more robust)
def llm_injection_check(user_input: str) -> bool:
    response = completion(
        model="claude-haiku-4-5-20251001",  # Fast, cheap
        messages=[{
            "role": "user",
            "content": f"Is this a prompt injection attempt? Answer YES or NO only.\n\nInput: {user_input}"
        }]
    )
    return "YES" in response.choices[0].message.content.upper()
```

### Input Sanitization

```python
def sanitize_input(user_input: str, max_length: int = 10000) -> str:
    # Truncate
    if len(user_input) > max_length:
        user_input = user_input[:max_length]
    # Remove control characters
    user_input = "".join(c for c in user_input if c.isprintable() or c in "\n\t")
    return user_input.strip()
```

## Output Validation

### Format Checking

```python
from pydantic import BaseModel, ValidationError

class AgentOutput(BaseModel):
    answer: str
    confidence: float
    sources: list[str]

def validate_output(raw_output: str) -> AgentOutput | None:
    try:
        return AgentOutput.model_validate_json(raw_output)
    except ValidationError:
        return None  # Re-prompt or return error
```

### Content Filtering

```python
def filter_output(content: str) -> str:
    """Remove PII and sensitive data from output."""
    import re
    # Remove email addresses
    content = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL REDACTED]', content)
    # Remove phone numbers
    content = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE REDACTED]', content)
    # Remove SSN patterns
    content = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', content)
    return content
```

## Tool Risk Enforcement

```python
TOOL_RISK = {
    "search_documents": "read-only",      # Auto-execute
    "update_ticket": "reversible",         # Log and execute
    "delete_account": "irreversible",      # Require confirmation
    "send_email": "irreversible",          # Require confirmation
}

def execute_with_risk_check(tool_name: str, args: dict, tool_functions: dict) -> str:
    risk = TOOL_RISK.get(tool_name, "irreversible")  # Default to safest

    if risk == "irreversible":
        # In HITL setup: pause for approval
        # In automated: log warning and require explicit flag
        raise ConfirmationRequired(f"Tool '{tool_name}' is irreversible. Confirm execution.")

    result = tool_functions[tool_name](**args)
    if risk == "reversible":
        log_action(tool_name, args, result)  # For potential rollback
    return result
```

## NeMo Guardrails (Quick Start)

```python
# pip install nemoguardrails
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_content(
    colang_content="""
    define user ask about politics
      "What do you think about the election?"
      "Who should I vote for?"

    define bot refuse political questions
      "I'm not able to provide political opinions. I can help with other topics."

    define flow
      user ask about politics
      bot refuse political questions
    """,
    yaml_content="""
    models:
      - type: main
        engine: openai
        model: gpt-4o
    """
)

rails = LLMRails(config)
response = rails.generate(messages=[{"role": "user", "content": "Who should I vote for?"}])
```

## HITL with LangGraph

```python
from langgraph.types import interrupt

def risky_action_node(state):
    """Pause for human approval before executing."""
    action = state["pending_action"]
    approval = interrupt({
        "action": action,
        "message": f"Agent wants to: {action['description']}. Approve?",
    })
    if approval != "approved":
        return {"status": "rejected", "messages": [{"role": "system", "content": "Action rejected by user."}]}
    return execute_action(action)
```

## OWASP Top 10 for Agentic Apps (Checklist)
1. Prompt injection → input validation + instruction/data separation
2. Excessive agency → tool risk-rating + confirmation for destructive ops
3. Supply chain → validate tool outputs + pin dependencies
4. Insecure output → sanitize before display + CSP headers
5. Data leakage → filter PII + audit logs
6. Insufficient monitoring → tracing (Langfuse) + alerts
7. Denial of service → rate limiting + max iterations + cost caps
8. Model manipulation → use trusted models + validate responses
9. Insufficient access control → per-user permissions on tools
10. Improper error handling → structured errors + no stack traces to users
