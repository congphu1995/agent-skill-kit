# Context Engineering

Systematic design of all information fed to the LLM. The context window is the single most important input to agent quality.

## Context Window Budget

Everything must fit within the model's context window:

```
System Prompt + Conversation History + Tool Definitions + Retrieved Docs + Output Space
= Total Context Window Usage
```

**Budget allocation guideline:**
- System prompt: 10-20% of context window
- Tool definitions: 5-15%
- Retrieved documents: 20-40%
- Conversation history: 20-30%
- Reserved for output generation: 10-20%

Monitor token usage. If you are near the limit, summarize conversation history or reduce retrieved documents.

## Information Hierarchy

Classify every piece of information by tier:

### Critical (always in system prompt)
- Agent identity and role
- Core behavioral rules and constraints
- Output format requirements
- Safety guardrails

### Important (include when relevant)
- Domain-specific knowledge for the current task
- Relevant few-shot examples
- Active tool definitions (only tools needed for current context)

### Supplementary (retrieve on demand)
- Reference documentation
- Historical data
- Detailed examples for edge cases
- User preference history

**Rule: Never put supplementary information in the system prompt.** Retrieve it dynamically via tools or RAG.

## Retrieval Strategy Decision

```
Is the knowledge static and small (<5 examples)?
  Yes -> Few-shot examples in system prompt
  No  -> Is the knowledge domain-specific and stable?
           Yes -> Is it <50k tokens?
                    Yes -> Reference file loaded on demand
                    No  -> RAG with vector DB
           No  -> Is it user-specific or session-specific?
                    Yes -> Conversation history + memory tools
                    No  -> Web search or API tools
```

## Memory Tiers

### Working Memory (context window)
- Current conversation turn
- System prompt
- Active tool definitions
- Most recent retrieved documents

### Episodic Memory (conversation history)
- Previous turns in current session
- Strategy: summarize older turns, keep recent turns verbatim
- Implementation: sliding window with summary of older context

### Long-Term Memory (external storage)
- User preferences and history across sessions
- Domain knowledge base
- Implementation: vector DB (Pinecone, Chroma, pgvector), key-value store

**Pattern: Memory escalation**
```
User query -> Check working memory (already in context?)
           -> Check episodic memory (earlier in conversation?)
           -> Check long-term memory (retrieve from DB?)
           -> Fall back to general knowledge
```

## Few-Shot vs Exhaustive Rules

**Prefer 3-5 well-chosen examples over 50 explicit rules.**

| Approach | When to Use |
|---|---|
| Few-shot examples | Pattern-based tasks, format matching, style mimicking |
| Explicit rules | Safety constraints, hard business rules, compliance requirements |
| Hybrid | Complex domains: rules for constraints + examples for style |

**Few-shot example template:**
```
Here are examples of correct outputs:

Input: "The product broke after 2 days"
Output: {"category": "defect", "urgency": "high", "department": "quality"}

Input: "When will my order arrive?"
Output: {"category": "shipping", "urgency": "medium", "department": "logistics"}

Input: "I'd like to change my subscription plan"
Output: {"category": "billing", "urgency": "low", "department": "accounts"}
```

## Hybrid Context Design

Combine static and dynamic context sources:

```
System Prompt (static)
  |-- Agent role and identity
  |-- Core rules and constraints
  |-- Output format specification
  +-- Few-shot examples (if <5)

Dynamic Context (loaded per query)
  |-- Retrieved documents (RAG)
  |-- Tool outputs from previous steps
  |-- User profile/preferences (from memory)
  +-- Relevant conversation history
```

## Context Strategy Template

Use this template when designing a context strategy:

```markdown
## Context Strategy for: {agent_name}

### System Prompt Contents
- Role: [agent role description]
- Rules: [list of hard constraints]
- Format: [output format specification]
- Examples: [few-shot examples if <5]

### Dynamic Retrieval
- Source: [vector DB / API / file system]
- Trigger: [when to retrieve -- every query, keyword match, etc.]
- Volume: [max tokens to retrieve per query]

### Memory Design
- Working: [what stays in context window]
- Episodic: [conversation history strategy -- full, summarized, sliding window]
- Long-term: [persistent storage -- what, where, how retrieved]

### Token Budget
- Model: [model name and context window size]
- System prompt: [estimated tokens]
- Tools: [estimated tokens]
- Retrieval: [max tokens]
- History: [max tokens]
- Output reserve: [tokens]
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Context stuffing | Dump everything into system prompt | Use information hierarchy, retrieve on demand |
| Irrelevant examples | Few-shot examples unrelated to current task | Select examples dynamically based on input |
| Conflicting instructions | Rules that contradict each other | Audit system prompt for consistency |
| No token budgeting | Context overflow causes truncation | Set explicit limits per category |
| Stale context | Old conversation history confuses the model | Summarize or drop old turns |
| Duplicate information | Same fact in system prompt and retrieved docs | Single source of truth per fact |
