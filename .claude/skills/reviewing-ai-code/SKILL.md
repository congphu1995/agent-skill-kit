---
name: reviewing-ai-code
description: >
  Review AI/agent code with specialized lenses: prompt quality, safety audit, architecture review,
  cost optimization, injection resistance. Use when user says "review code", "review prompt",
  "safety audit", "architecture review", "optimize costs", "token optimization",
  "review my agent", "security review for AI", "prompt injection check".
  Do NOT use for writing tests (use testing-ai-systems).
  Do NOT use for prompt evaluation/benchmarking (use evaluating-and-benchmarking).
---

# Reviewing AI Code

AI/agent code review with specialized lenses beyond standard code review.

## Steps

### 1. Identify review scope

Determine what the user wants reviewed:
- **Full agent review** — end-to-end review of an agent system
- **Single prompt review** — focused review of one prompt template
- **Architecture review** — system design, agent topology, tool integration
- **Security audit** — prompt injection, data leakage, excessive agency

Ask the user to clarify scope if ambiguous. Default to full agent review if the user says "review my code" on an agent project.

### 2. Read the code

Understand before judging:
- What is the agent's purpose?
- What is the control flow (single-turn, multi-turn, agentic loop, multi-agent)?
- What tools/APIs does it call?
- Where are the prompts defined?
- What models are used and how are they configured?
- How is user input handled?

### 3. Apply review lenses

Run through each applicable checklist. Read the reference file, then evaluate the code against it.

| Lens | Reference file | When to apply |
|------|---------------|---------------|
| Prompt quality | `references/prompt-review-checklist.md` | Always |
| Safety & security | `references/safety-audit.md` | Always |
| Anti-patterns | `references/ai-code-antipatterns.md` | Always |
| Cost optimization | `references/cost-optimization.md` | When user mentions cost, or for production systems |

For each lens:
1. Read the reference checklist
2. Evaluate the code against each item
3. Note findings with severity: critical / important / minor
4. Note strengths — what the code does well

### 4. Produce review report

Write the report to `.claude/artifacts/reviewing-{name}.md` where `{name}` is a slug of the project or file being reviewed.

Report structure:

```markdown
# AI Code Review: {name}

## Summary
1-2 sentence overview of the codebase and its overall quality.

## Critical Issues (must fix)
- [ ] Issue description — file:line — why it matters

## Important Issues (should fix)
- [ ] Issue description — file:line — recommendation

## Minor Issues (nice to fix)
- [ ] Issue description — file:line — suggestion

## Strengths
- What the code does well
- Good patterns worth preserving

## Review Metadata
- Scope: {full agent | prompt | architecture | security}
- Lenses applied: {list}
- Files reviewed: {count}
```

### Guidelines

- Be specific: reference exact file paths and line numbers.
- Be actionable: every issue should have a concrete fix suggestion.
- Be balanced: always include strengths alongside issues.
- Prioritize: critical issues are security risks or correctness bugs; important issues affect reliability; minor issues improve quality.
- Do NOT rewrite the code — provide review feedback only.
