# Tool Design Patterns (ACI)

Agent-Computer Interface design: how agents interact with the world through tools.

## Naming Convention

Use `verb_noun` format. Be specific and consistent.

| Good | Bad |
|---|---|
| `get_customer` | `customer` |
| `create_order` | `makeNewOrder` |
| `search_documents` | `docs` |
| `update_ticket_status` | `modify` |
| `delete_draft_email` | `remove` |

Common verbs: `get`, `list`, `search`, `create`, `update`, `delete`, `validate`, `calculate`, `send`, `export`.

## Consolidation Rules

- Keep total tools under 50 per agent (ideally under 20)
- Group related CRUD operations logically
- Prefer fewer powerful tools over many narrow ones
- If an agent has too many tools, consider splitting into multiple agents

## Description Guidelines

Tool descriptions are the primary way the LLM decides which tool to use. Write them carefully.

- Start with what the tool does in one sentence
- List parameter constraints and valid values
- Include what the tool returns
- Mention side effects if any
- Add examples of when to use vs not use

```python
def search_documents(query: str, max_results: int = 10, doc_type: str | None = None) -> list[dict]:
    """Search the document repository by semantic similarity.

    Args:
        query: Natural language search query. Be specific for better results.
        max_results: Number of results to return (1-100, default 10).
        doc_type: Filter by type: 'contract', 'invoice', 'memo', or None for all.

    Returns:
        List of {id, title, snippet, score, doc_type} sorted by relevance.

    Use this tool when the user asks about document contents. Do NOT use
    for listing all documents (use list_documents instead).
    """
```

## Risk Rating System

Classify every tool by risk level to determine execution policy.

| Risk Level | Policy | Examples |
|---|---|---|
| **read-only** | Auto-execute without confirmation | `get_customer`, `search_documents`, `list_orders` |
| **reversible** | Execute with logging, can undo | `update_ticket_status`, `create_draft`, `add_tag` |
| **irreversible** | Require explicit user confirmation | `delete_account`, `send_email`, `process_payment` |

Annotate tools with risk metadata:

```python
from enum import Enum
from pydantic import BaseModel, Field

class RiskLevel(str, Enum):
    READ_ONLY = "read_only"
    REVERSIBLE = "reversible"
    IRREVERSIBLE = "irreversible"

class ToolMeta(BaseModel):
    risk: RiskLevel
    requires_confirmation: bool = False
    idempotent: bool = False
```

## Pydantic Schemas for Tool I/O

Always define input and output schemas. This enables validation, documentation, and structured tool_use.

```python
from pydantic import BaseModel, Field, constr, conint
from enum import Enum
from typing import Literal


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CreateTicketInput(BaseModel):
    """Input schema for create_ticket tool."""
    title: constr(min_length=1, max_length=200) = Field(
        description="Short summary of the issue"
    )
    description: str = Field(
        description="Detailed description of the issue"
    )
    priority: TicketPriority = Field(
        default=TicketPriority.MEDIUM,
        description="Ticket priority level"
    )
    assignee_email: str | None = Field(
        default=None,
        description="Email of the assignee, or null for unassigned"
    )


class CreateTicketOutput(BaseModel):
    """Output schema for create_ticket tool."""
    ticket_id: str = Field(description="Unique ticket identifier")
    url: str = Field(description="URL to view the ticket")
    status: Literal["open"] = Field(description="Initial ticket status")


# Tool implementation with full error handling
class ToolError(Exception):
    """Actionable error returned to the agent."""
    def __init__(self, message: str, suggestion: str):
        self.message = message
        self.suggestion = suggestion


TOOL_RISK = RiskLevel.REVERSIBLE


def create_ticket(input: CreateTicketInput) -> CreateTicketOutput:
    """Create a new support ticket in the tracking system.

    Risk: reversible (tickets can be closed/deleted).
    """
    try:
        # ... API call ...
        return CreateTicketOutput(
            ticket_id="TICK-1234",
            url="https://tracker.example.com/TICK-1234",
            status="open",
        )
    except ConnectionError:
        raise ToolError(
            message="Cannot connect to ticket system",
            suggestion="Check if the ticket system is accessible. Retry in 30 seconds.",
        )
    except PermissionError:
        raise ToolError(
            message="Insufficient permissions to create ticket",
            suggestion="Verify the API key has 'tickets:write' scope.",
        )
```

## Error Handling Rules

1. **Return actionable messages** -- tell the agent what went wrong and how to fix it
2. **Never expose stack traces** -- wrap exceptions into user-friendly errors
3. **Suggest next steps** -- "Try with a different query" or "Check permissions"
4. **Use error codes** -- enable programmatic error handling by the agent
5. **Distinguish retryable vs fatal** -- let the agent decide whether to retry

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Tool name is a noun (`customer`) | Use verb_noun: `get_customer` |
| Giant tool that does 5 things | Split into focused tools |
| No parameter descriptions | Add Field(description=...) for every param |
| Returns raw API response | Map to a clean output schema |
| Swallows errors silently | Raise ToolError with suggestion |
| 100+ tools on one agent | Consolidate or split into multi-agent |
