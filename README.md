<p align="center">
  <h1 align="center">Agent Skill Kit</h1>
  <p align="center">
    <strong>18 Claude Code skills for the full AI agent development lifecycle</strong>
  </p>
  <p align="center">
    <a href="#quick-start">Quick Start</a> &middot;
    <a href="#skills-catalog">Skills Catalog</a> &middot;
    <a href="#workflow-chains">Workflows</a> &middot;
    <a href="#contributing">Contributing</a>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/skills-18-blue" alt="18 Skills">
    <img src="https://img.shields.io/badge/references-75-green" alt="75 References">
    <img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT License">
    <img src="https://img.shields.io/badge/claude--code-compatible-blueviolet" alt="Claude Code Compatible">
  </p>
</p>

---

Stop prompting from scratch every time you build an AI agent. This kit gives Claude Code **deep, actionable knowledge** — structured workflows, implementation patterns, and 75 reference files — so it automatically activates the right skill for your request and produces production-grade code.

## Why Use This?

| Without skills | With Agent Skill Kit |
|---|---|
| Generic LLM responses | Domain-specific AI/agent patterns |
| Manual prompt engineering | Auto-triggered workflows |
| Reinventing patterns each session | 75 battle-tested reference files |
| No consistency across projects | Unified conventions (LiteLLM, eval-first, complexity ladder) |

## Quick Start

**Option 1: Project-level** (recommended)

```bash
git clone https://github.com/ncphu/agent-skill-kit.git
cp -r agent-skill-kit/.claude/skills/ your-project/.claude/skills/
```

**Option 2: Personal skills** (available across all projects)

```bash
git clone https://github.com/ncphu/agent-skill-kit.git
cp -r agent-skill-kit/.claude/skills/ ~/.claude/skills/
```

**Option 3: Additional directory** (no file copying)

```bash
git clone https://github.com/ncphu/agent-skill-kit.git
# Then run Claude Code with:
claude --add-dir /path/to/agent-skill-kit/.claude/skills
```

Once installed, just ask naturally — skills trigger automatically:

```
"Design an agent for claim processing"     → designing-agent-system
"Build a RAG pipeline with Pinecone"       → building-rag-pipeline
"Set up evals with promptfoo"              → evaluating-and-benchmarking
```

## Skills Catalog

### A: Research & Design

| Skill | What it does | Trigger phrases |
|-------|-------------|-----------------|
| **researching-ai-topics** | Paper search, framework comparison, benchmark analysis | "research", "compare frameworks", "which model", "find papers" |
| **designing-agent-system** | Architecture design using Anthropic's complexity ladder | "design agent", "agent architecture", "multi-agent", "context engineering" |
| **planning-and-breaking-down** | Break projects into executable task lists with file paths | "plan this", "break down", "brainstorm", "create tasks" |

### B: Build

| Skill | What it does | Trigger phrases |
|-------|-------------|-----------------|
| **setting-up-ai-dev-env** | Python env, GPU/CUDA, API keys, Ollama, Docker, MCP | "setup environment", "install Ollama", "configure API keys", "GPU setup" |
| **scaffolding-ai-project** | Project structure with configs, Docker, CI skeleton | "scaffold", "new project", "bootstrap", "project structure" |
| **building-agent-core** | LLM integration, tool calling, memory, multi-agent, guardrails | "build agent", "LLM integration", "tool calling", "LangGraph", "guardrails" |
| **building-rag-pipeline** | Embeddings, vector DB, chunking, hybrid search, reranking | "RAG pipeline", "vector search", "embeddings", "knowledge base" |
| **building-mcp-server** | MCP server with FastMCP or TypeScript SDK | "MCP server", "MCP tools", "build MCP" |
| **building-backend-api** | FastAPI with streaming SSE, rate limiting, model routing | "FastAPI", "backend", "API server", "streaming endpoint", "SSE" |
| **building-ai-frontend** | React/Next.js chat UI, dashboards, streaming display | "chat UI", "AI frontend", "dashboard", "React for AI" |

### C: Test & Evaluate

| Skill | What it does | Trigger phrases |
|-------|-------------|-----------------|
| **testing-ai-systems** | Unit tests with LLM mocking, agent behavior tests | "write tests", "test agent", "unit test", "mock LLM" |
| **evaluating-and-benchmarking** | Prompt eval with promptfoo/DeepEval, red-teaming, CI gates | "evaluate prompt", "eval pipeline", "benchmark", "promptfoo" |
| **reviewing-ai-code** | Code review: prompt quality, safety audit, cost optimization | "review code", "safety audit", "cost optimization" |

### D: Deploy & Observe

| Skill | What it does | Trigger phrases |
|-------|-------------|-----------------|
| **deploying-ai-systems** | Docker, CI/CD with eval gates, Kubernetes, model serving | "deploy", "Dockerfile", "CI/CD", "GitHub Actions", "Kubernetes" |
| **instrumenting-observability** | Tracing (Langfuse/LangSmith), cost tracking, alerts | "add tracing", "Langfuse", "cost tracking", "monitoring" |

### E: Document

| Skill | What it does | Trigger phrases |
|-------|-------------|-----------------|
| **documenting-ai-systems** | API docs, Mermaid diagrams, agent flow docs, runbooks | "generate docs", "architecture diagram", "Mermaid", "runbook" |

### F: Meta

| Skill | What it does | Trigger phrases |
|-------|-------------|-----------------|
| **creating-and-managing-skills** | Create and test new Claude Code skills | "create skill", "new skill", "test skill" |
| **extracting-patterns** | Extract reusable patterns from completed work | "extract skill from this", "save as pattern", "learn from this" |

## Workflow Chains

Skills chain together through the development lifecycle. Pick the chain that matches your situation:

```
Research ─→ Design ─→ Plan ─→ Setup ─→ Scaffold ─→ Eval ─→ Build ─→ Test ─→ Review ─→ Deploy ─→ Observe
  A1         A2       A3      B1        B2         C2    B3-B7     C1       C3       D1        D2
```

<details>
<summary><strong>Common chains</strong></summary>

| Chain | Skills | When to use |
|-------|--------|-------------|
| **Greenfield** | A1 → A2 → A3 → B1 → B2 → B3 → C1 → D1 | Starting a new agent project from scratch |
| **Eval-first** | C2 → B3 → C1 → C3 | Building with eval-driven development |
| **Full-stack agent** | B3 → B6 → B7 → D1 → D2 | Agent + API + frontend + deployment |
| **Existing codebase** | C3 → A2 → B3 → C1 | Adding agent capabilities to existing code |
| **RAG system** | A2 → B4 → B6 → C2 → D1 | Building a retrieval-augmented generation system |

</details>

## Flagship Skills

<details>
<summary><strong>designing-agent-system</strong> — 8-step design flow with 6 reference files</summary>

The backbone skill. Walks through Anthropic's complexity ladder (start simple, escalate only with justification), tool design (ACI patterns), context engineering, output schemas, state machines, and multi-agent patterns. Produces a complete design artifact.

**References:** `complexity-ladder.md`, `tool-design-patterns.md`, `context-engineering.md`, `output-schemas.md`, `state-machine-patterns.md`, `agent-patterns.md`

</details>

<details>
<summary><strong>building-agent-core</strong> — framework-agnostic with 10 reference files</summary>

The largest skill. Covers LLM integration via LiteLLM, tool calling, memory patterns, multi-agent orchestration, streaming, and guardrails. Includes framework-specific references for LangGraph, CrewAI, and OpenAI Agents SDK.

**References:** `llm-integration.md`, `framework-decision.md`, `langgraph-patterns.md`, `crewai-patterns.md`, `openai-agents-sdk.md`, `tool-calling.md`, `memory-patterns.md`, `multi-agent.md`, `streaming.md`, `guardrails-patterns.md`

</details>

<details>
<summary><strong>evaluating-and-benchmarking</strong> — eval-first development with 6 reference files</summary>

Runs _before_ building in the recommended workflow. Sets up promptfoo or DeepEval pipelines, generates eval datasets, implements three-tier evaluation (unit/integration/end-to-end), and adds CI eval gates.

**References:** `promptfoo-setup.md`, `eval-dataset-generation.md`, `three-tier-eval.md`, `deepeval-setup.md`, `red-teaming.md`, `performance-benchmarks.md`

</details>

## Architecture

```
agent-skill-kit/
├── .claude/
│   └── skills/                     # The 18 skills
│       ├── SKILL_CATALOG.md        # Central routing catalog
│       └── {skill-name}/
│           ├── SKILL.md            # Workflow + instructions
│           └── references/         # Implementation patterns (1-10 per skill)
├── tests/
│   ├── test_skills.py              # Structural validation
│   └── test_skills_behavioral.py   # Behavioral tests
├── README.md
└── LICENSE
```

Each skill follows a consistent structure:

```yaml
# SKILL.md
---
name: skill-name
description: >
  [What it does]. Use when [triggers]. Do NOT use for [exclusions].
allowed-tools: Read, Write, Bash, Grep, Glob
---
# Step-by-step instructions
# References loaded on demand
# Output written to .claude/artifacts/
```

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **LiteLLM as unified LLM layer** | Provider-agnostic from day one (100+ providers) |
| **Complexity ladder in A2** | Always start with the simplest viable architecture |
| **Eval-first workflow** | C2 runs before B3 — define success criteria before building |
| **Framework-agnostic B3** | One skill, 10 references for different frameworks |
| **Trigger exclusions** | Prevents cross-triggering between similar skills (B3 vs B4, C1 vs C2) |

## Testing

```bash
# Structural validation (YAML frontmatter, references, catalog completeness)
python3 tests/test_skills.py

# Behavioral tests (triggering, routing, description quality)
python3 tests/test_skills_behavioral.py
```

Requires: `pip install pyyaml`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run both test suites before submitting
4. Open a pull request

<details>
<summary><strong>Skill authoring conventions</strong></summary>

- Place skills in `.claude/skills/{skill-name}/SKILL.md`
- Use YAML frontmatter with `name`, `description`, `allowed-tools`
- Include trigger phrases AND exclusions in the description
- Add reference files in a `references/` subdirectory
- Register the skill in `SKILL_CATALOG.md`

</details>

## FAQ

<details>
<summary>Do I need all 18 skills?</summary>

No. Copy only the skills you need. Each skill is self-contained with its own references. The catalog and workflow chains are optional.

</details>

<details>
<summary>Will these conflict with existing skills?</summary>

Unlikely. Each skill has explicit trigger phrases and exclusion rules to prevent cross-triggering. If you have a custom skill that overlaps, adjust the `description` field in the SKILL.md frontmatter.

</details>

<details>
<summary>What's the token cost impact?</summary>

Skills are loaded on-demand — Claude only reads a skill's SKILL.md and references when it's triggered. Idle skills add zero token overhead.

</details>

<details>
<summary>Can I use these with other AI coding tools?</summary>

These skills use Claude Code's SKILL.md format. Other tools (Cursor, Windsurf, Copilot) use different configuration formats, so direct compatibility is not guaranteed.

</details>

## License

MIT — see [LICENSE](LICENSE).
