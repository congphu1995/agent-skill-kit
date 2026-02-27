---
name: planning-and-breaking-down
description: >
  Plan and break down AI/agent projects into executable task lists with file paths,
  acceptance criteria, and skill references. Use when user says "plan this", "break down",
  "brainstorm", "what should I build", "create tasks", "project roadmap", "implementation plan".
  Do NOT use for designing agent architecture (use designing-agent-system) or
  for writing code (use building-agent-core).
---
# Planning and Breaking Down

Turn ideas into executable task lists with skill references, file paths, and acceptance criteria.

## Phase 1: Brainstorm & Design

### Step 1: Explore project context
- Check existing files, docs, recent commits
- Identify constraints, dependencies, existing patterns

### Step 2: Ask clarifying questions (one at a time)
- What is the goal? Who is the user?
- What are the inputs and outputs?
- What are the quality and performance requirements?
- What existing infrastructure must be used?

### Step 3: Propose 2-3 approaches
- Present trade-offs and your recommendation
- Consider complexity ladder (prefer simpler approaches)
- Get user approval before proceeding to breakdown

## Phase 2: Break Down into Tasks

### Step 4: Create task list
Each task MUST include all of these fields:

````markdown
### Task N: [Component Name]
**Skill:** /skill-name (e.g., /building-agent-core, /evaluating-and-benchmarking)
**Input:** path to upstream artifact if any
**Output:** file path for deliverable
**Acceptance criteria:**
- [ ] Specific pass/fail condition 1
- [ ] Specific pass/fail condition 2
**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py`
- Test: `tests/exact/path/to/test_file.py`

**Steps:**
1. [2-5 minute action]
2. [2-5 minute action]
3. Verify: [exact command with expected output]
4. Commit: `git commit -m "feat: description"`
````

### Step 5: Follow convention directory structure
```
project-root/
├── src/
│   ├── agents/          ← /building-agent-core
│   ├── rag/             ← /building-rag-pipeline
│   ├── tools/           ← /building-agent-core, /building-mcp-server
│   ├── api/             ← /building-backend-api
│   └── frontend/        ← /building-ai-frontend
├── tests/               ← /testing-ai-systems
├── evals/               ← /evaluating-and-benchmarking
├── docs/                ← /documenting-ai-systems
├── .claude/artifacts/   ← design/review artifacts
├── Dockerfile           ← /deploying-ai-systems
└── .github/workflows/   ← /deploying-ai-systems
```

### Step 6: Order tasks correctly
Recommended chain: Design → Eval → Build → Test → Review
1. A2 design (if not done)
2. C2 create evals BEFORE building
3. B1 setup environment
4. B3/B4/B5/B6/B7 build components
5. C1 write tests
6. C3 review code

### Step 7: Save plan
Output to `.claude/artifacts/planning-{name}.md`

## After Planning

Offer execution choice:

**1. Subagent-Driven (this session)** — dispatch fresh subagent per task, review between tasks

**2. Parallel Session (separate)** — open new session, batch execution with checkpoints

## Key Principles
- Each task is one action (2-5 minutes)
- Exact file paths always
- Complete code in plan, not "add validation"
- Eval before build (eval-driven development)
- DRY, YAGNI, frequent commits
