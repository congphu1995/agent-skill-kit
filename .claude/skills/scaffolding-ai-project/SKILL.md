---
name: scaffolding-ai-project
description: >
  Scaffold complete AI/agent project structures: directory layout, configs, Docker, CI skeleton, dependencies.
  Use when user says "scaffold", "new project", "bootstrap", "init AI project", "project structure",
  "create project", "project template", "setup new agent project".
  Do NOT use for environment setup (use setting-up-ai-dev-env) or for building agent code (use building-agent-core).
---
# Scaffolding AI Project

Generate full project structure: directories, configs, Docker, CI, dependencies.

## Instructions

### Step 1: Ask framework choice
Ask the user (if not already specified):
- **FastAPI** backend agent service → `references/stack-fastapi.md`
- **Next.js** AI frontend/fullstack → `references/stack-nextjs.md`
- **LangChain/LangGraph** agent project → `references/stack-langchain.md`

Also ask:
- Project name?
- Need Docker setup? (default: yes)
- Need CI/CD skeleton? (default: yes)
- Vector DB needed? (default: no, suggest if RAG mentioned)

### Step 2: Read relevant stack reference
Load ONLY the chosen stack reference. Do not load all of them.

### Step 3: Generate directory structure
Create the canonical directory layout from the reference. Always include:
```
<project-name>/
  src/
    agents/          # Agent definitions
    rag/             # RAG pipeline (if needed)
    tools/           # Tool/function definitions
    models/          # Pydantic models / schemas
  tests/
    unit/
    integration/
  evals/             # LLM evaluation datasets and scripts
  docs/              # Project documentation
  scripts/           # Utility scripts (seed, migrate, etc.)
```

### Step 4: Create config files
Generate from templates in the stack reference:
- `pyproject.toml` or `package.json` (with AI dependencies)
- `.env.example` (with placeholder API keys)
- `.gitignore` (include model artifacts, .env, __pycache__)
- `Dockerfile` → read `references/docker-templates.md` for the right template
- `docker-compose.yml` (if vector DB or Redis needed)
- `Makefile` or `justfile` with common commands

### Step 5: Create entry point and README skeleton
- Main entry point (`main.py` / `app/page.tsx`) with minimal boilerplate
- `README.md` with: project name, setup instructions, architecture overview placeholder

### Step 6: Verify structure
Run `find <project-name> -type f | head -30` to confirm all files were created.
Run linter/formatter if configured to ensure generated files are valid.

## CI Skeleton (GitHub Actions)
Always generate `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -e ".[dev]"
      - run: pytest tests/
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check .
```

## .gitignore essentials
```
__pycache__/
*.pyc
.env
.venv/
*.egg-info/
dist/
models/*.bin
models/*.gguf
.chroma/
node_modules/
.next/
```
