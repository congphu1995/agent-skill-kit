---
name: extracting-patterns
description: >
  Extract reusable patterns from completed work into skills or reference files.
  Use when user says "extract skill from this", "save as pattern", "learn from this session",
  "what patterns did we use", "create a reusable template from this".
  Do NOT use for creating new skills from scratch (use creating-and-managing-skills).
---
# Extracting Patterns

Extract reusable patterns from completed work into skills, reference files, or templates.

## Instructions

### Step 1: Analyze completed work
- Read recent files changed: `git diff --name-only HEAD~5`
- Read conversation context for decisions made
- Identify the project type and domain

### Step 2: Identify reusable patterns
Look for:
- **Coding patterns** — recurring code structures, helper functions, class hierarchies
- **Architectural decisions** — why X was chosen over Y, trade-offs evaluated
- **Tool configurations** — configs that took iteration to get right
- **Prompt templates** — system prompts, few-shot examples that worked well
- **Workflow sequences** — multi-step processes that could be repeated

### Step 3: Classify each pattern

| Type | Destination | When |
|------|-------------|------|
| Skill candidate | New SKILL.md via `/creating-and-managing-skills` | Reusable multi-step workflow |
| Reference file | Add to existing skill's `references/` | Domain knowledge, API patterns |
| Code template | `assets/` in relevant skill | Boilerplate, scaffolding |
| Workflow snippet | Append to existing reference | Small reusable procedure |

### Step 4: Extract and format
Write each pattern to `.claude/artifacts/extracting-patterns-{descriptive-name}.md` using this template:

```markdown
## Pattern: [Name]
**Context:** What project/task produced this pattern
**Problem:** What recurring problem does this solve
**Solution:** The reusable approach
**Code Example:**
[Minimal working code]
**When to Use:** Conditions where this pattern applies
**When NOT to Use:** Conditions where this pattern is wrong
**Related Skills:** Which skills should absorb this pattern
```

### Step 5: Integration recommendation
For each extracted pattern, recommend:
1. Which existing skill should receive it (e.g., "Add to `building-agent-core/references/langgraph-patterns.md`")
2. Or if a new skill should be created (invoke `/creating-and-managing-skills`)
3. Priority: critical (use immediately) / useful (add when convenient) / archive (save for reference)

## Example
After building a LangGraph agent with custom checkpointing:
- Extract the checkpointing pattern → add to `building-agent-core/references/langgraph-patterns.md`
- Extract the state schema design → add to `designing-agent-system/references/state-machine-patterns.md`
- Extract the test mocking approach → add to `testing-ai-systems/references/llm-mocking.md`
