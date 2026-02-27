---
name: designing-agent-system
description: >
  Design AI agent systems using Anthropic's complexity ladder — start simple, scale only when needed.
  Use when user says "design agent", "agent architecture", "multi-agent", "system design for AI",
  "how should I build this agent", "design prompt", "structured output schema", "design tools for agent",
  "context engineering", "agent workflow", "handoff protocol".
  Do NOT use for building/coding agents (use building-agent-core) or for RAG pipelines (use building-rag-pipeline).
---

# Designing Agent Systems

Guide users through a structured design process. Always start at the simplest complexity level and escalate only with justification.

## 8-Step Design Flow

### Step 1: Gather Requirements

Ask the user:
- What task should the agent perform? Be specific.
- What are the inputs and expected outputs?
- What is the quality bar? (e.g., "good enough" vs "expert-level")
- What are the latency and cost constraints?
- Who are the end users?
- What failure modes are acceptable?

Do not proceed until requirements are clear. Summarize back to the user before continuing.

### Step 2: Determine Complexity Level

Read [references/complexity-ladder.md](references/complexity-ladder.md).

Start at Level 1 (single LLM call). Walk the decision tree upward. Only escalate when the current level demonstrably cannot meet requirements. Document the justification for the chosen level.

**Default bias**: Most tasks can be solved at Level 1-3. Resist the urge to over-engineer.

### Step 3: Design Tools (ACI)

Read [references/tool-design-patterns.md](references/tool-design-patterns.md).

For each tool the agent needs:
- Define name (verb_noun format), description, parameters
- Assign risk rating: read-only / reversible / irreversible
- Define input/output schemas with Pydantic models
- Specify error handling behavior

Keep total tools under 50 per agent. Consolidate related operations.

### Step 4: Design Context Strategy

Read [references/context-engineering.md](references/context-engineering.md).

Determine:
- What information must always be in the system prompt (critical tier)
- What information is loaded conditionally (important tier)
- What information is retrieved on demand via RAG or tools (supplementary tier)
- Which memory tier applies: working, episodic, or long-term
- Whether few-shot examples or explicit rules work better for this domain

### Step 5: Design Output Schemas

Read [references/output-schemas.md](references/output-schemas.md).

Define Pydantic models for every structured output the agent produces. Include:
- Field types with constraints (Literal, Enum, constr, conint)
- Nested models for hierarchical data
- Validation rules and default values
- Choose output mechanism: Instructor, PydanticAI, or Anthropic tool_use

### Step 6: Design State Management

Skip if the agent is stateless (most Level 1-3 designs).

If stateful, read [references/state-machine-patterns.md](references/state-machine-patterns.md).

Define:
- State schema (TypedDict or Pydantic model)
- Valid state transitions
- Checkpointing strategy (for resumability)
- Human-in-the-loop interrupt points (if any)

Draw a Mermaid state diagram.

### Step 7: Design Agent Patterns

Skip if single-agent (Level 1-5 without delegation).

If multi-agent, read [references/agent-patterns.md](references/agent-patterns.md).

Define:
- Agent roles and responsibilities
- Which pattern applies: supervisor, pipeline, router, peer handoff, or crew
- Handoff protocol: what context is passed between agents
- Error isolation boundaries

### Step 8: Produce Design Artifact

Write the final design document to `.claude/artifacts/designing-agent-system-{name}.md` with these sections:

```markdown
# Agent System Design: {name}

## 1. Complexity Level & Justification
[Level N -- why this level, why not N-1]

## 2. Requirements Summary
[Task, inputs, outputs, quality bar, constraints]

## 3. Tool Specifications
[For each tool: name, description, parameters, risk rating, schema]

## 4. Context Strategy
[System prompt contents, retrieval strategy, memory tier, few-shot examples]

## 5. Output Schemas
[Pydantic models with field definitions]

## 6. State Diagram
[Mermaid diagram if stateful, or "Stateless" if not]

## 7. Agent Roles & Handoffs
[If multi-agent: roles, pattern, handoff protocol. Otherwise "Single agent"]

## 8. Recommended Framework
[Framework recommendation with justification: Claude API direct, LangGraph, PydanticAI, CrewAI, etc.]
```
