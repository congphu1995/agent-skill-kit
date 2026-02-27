# AI Agent Skill Catalog

> 18 skills across 6 categories for full AI/agent development lifecycle.

## Category A: Research & Design

| ID | Skill | Triggers | Exclusions |
|----|-------|----------|------------|
| A1 | `researching-ai-topics` | "research", "compare frameworks", "which model", "find papers" | Not for designing or building |
| A2 | `designing-agent-system` | "design agent", "agent architecture", "multi-agent", "context engineering" | Not for coding (→ B3) |
| A3 | `planning-and-breaking-down` | "plan this", "break down", "brainstorm", "create tasks" | Not for design (→ A2) |

## Category B: Code Generation

| ID | Skill | Triggers | Exclusions |
|----|-------|----------|------------|
| B1 | `setting-up-ai-dev-env` | "setup environment", "install Ollama", "configure API keys", "GPU setup" | Not for scaffolding (→ B2) |
| B2 | `scaffolding-ai-project` | "scaffold", "new project", "bootstrap", "project structure" | Not for env setup (→ B1) |
| B3 | `building-agent-core` | "build agent", "LLM integration", "tool calling", "LangGraph", "guardrails" | Not for RAG (→ B4) |
| B4 | `building-rag-pipeline` | "RAG pipeline", "vector search", "embeddings", "knowledge base" | Not for agent logic (→ B3) |
| B5 | `building-mcp-server` | "MCP server", "MCP tools", "build MCP" | |
| B6 | `building-backend-api` | "FastAPI", "backend", "API server", "streaming endpoint", "SSE" | Not for frontend (→ B7) |
| B7 | `building-ai-frontend` | "chat UI", "AI frontend", "dashboard", "React for AI" | Not for backend (→ B6) |

## Category C: Testing & Evaluation

| ID | Skill | Triggers | Exclusions |
|----|-------|----------|------------|
| C1 | `testing-ai-systems` | "write tests", "test agent", "unit test", "mock LLM" | Not for eval (→ C2) |
| C2 | `evaluating-and-benchmarking` | "evaluate prompt", "eval pipeline", "benchmark", "promptfoo" | Not for unit tests (→ C1) |
| C3 | `reviewing-ai-code` | "review code", "review prompt", "safety audit", "cost optimization" | Not for tests (→ C1) |

## Category D: Deployment & Observability

| ID | Skill | Triggers | Exclusions |
|----|-------|----------|------------|
| D1 | `deploying-ai-systems` | "deploy", "Dockerfile", "CI/CD", "GitHub Actions", "Kubernetes" | Not for tracing (→ D2) |
| D2 | `instrumenting-observability` | "add tracing", "observability", "Langfuse", "cost tracking" | Not for deploy (→ D1) |

## Category E: Documentation

| ID | Skill | Triggers | Exclusions |
|----|-------|----------|------------|
| E1 | `documenting-ai-systems` | "generate docs", "architecture diagram", "Mermaid", "runbook" | Not for review (→ C3) |

## Category F: Meta

| ID | Skill | Triggers | Exclusions |
|----|-------|----------|------------|
| F1 | `creating-and-managing-skills` | "create skill", "new skill", "test skill" | |
| F2 | `extracting-patterns` | "extract skill from this", "save as pattern", "learn from this" | Not for new skills (→ F1) |

## Workflow Chains

```
Research → Design → Plan → Setup → Eval → Build → Test → Review → Deploy → Observe
A1 → A2 → A3 → B1 → B2 → C2 → B3/B4/B5/B6/B7 → C1 → C3 → D1 → D2
```
