---
name: documenting-ai-systems
description: >
  Generate documentation for AI systems: API docs, architecture diagrams (Mermaid), agent flow docs, READMEs, runbooks.
  Use when user says "generate docs", "API documentation", "architecture diagram", "Mermaid",
  "README", "runbook", "document agent flow", "create docs", "system documentation".
  Do NOT use for code review (use reviewing-ai-code) or for planning (use planning-and-breaking-down).
---
# Documenting AI Systems

Generate comprehensive documentation for AI agent systems.

## Instructions

### Step 1: Identify documentation scope
Route to the correct reference:
- API documentation → `references/api-doc-templates.md`
- Architecture diagrams → `references/mermaid-patterns.md`
- Agent flow documentation → `references/agent-flow-docs.md`
- Operations runbook → `references/runbook-template.md`

If user asks for "full docs" or "document the system", generate all four.

### Step 2: Read relevant reference
Load the needed template. Then analyze the codebase — read source files to understand agents, tools, API endpoints, data flows, and dependencies.

### Step 3: Generate architecture diagram
Every AI system doc should include at least one Mermaid diagram. Example agent flow:

```mermaid
graph TD
    User[User Request] --> Router{Router Agent}
    Router -->|research| ResearchAgent[Research Agent]
    Router -->|code| CodeAgent[Code Agent]
    ResearchAgent --> Tools1[Web Search<br/>Paper Lookup]
    CodeAgent --> Tools2[File Read<br/>Code Execute]
    ResearchAgent --> Synthesizer[Synthesizer]
    CodeAgent --> Synthesizer
    Synthesizer --> Response[Final Response]
```

Sequence diagram for tool calling:
```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant L as LLM
    participant T as Tool

    U->>A: Send message
    A->>L: Forward with context
    L->>A: tool_call(search, query="...")
    A->>T: Execute tool
    T->>A: Tool result
    A->>L: Result + continue
    L->>A: Final response
    A->>U: Display response
```

### Step 4: Generate documentation content
For each doc type, include:

**README** — Project overview, quickstart, architecture diagram, API summary, env vars
**API docs** — Endpoints, request/response examples, error codes, auth, rate limits
**Agent flow** — Agent roles, tool list, handoff logic, state transitions, failure modes
**Runbook** — Common operations, troubleshooting, monitoring, incident response

### Step 5: Write docs
- Place in `docs/` directory alongside the project
- Or write to `.claude/artifacts/documenting-{name}.md`
- Use Mermaid for all diagrams (renders in GitHub, most doc platforms)
- Include concrete examples (API request/response, sample agent interaction)

## Documentation quality checklist
- [ ] Architecture diagram present (Mermaid)
- [ ] All agents and their roles documented
- [ ] Tool list with descriptions and risk levels
- [ ] API endpoints with request/response examples
- [ ] Environment variables documented
- [ ] Setup instructions that actually work
- [ ] Failure modes and recovery steps covered
- [ ] No stale information (matches current codebase)
