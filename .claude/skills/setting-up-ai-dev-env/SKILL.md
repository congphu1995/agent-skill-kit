---
name: setting-up-ai-dev-env
description: >
  Set up AI/agent development environments: Python, GPU/CUDA, API keys, tools (Ollama, Docker, LiteLLM),
  MCP config, and IDE setup. Use when user says "setup environment", "install Ollama", "configure API keys",
  "GPU setup", "dev environment for AI", "setup MCP", "install dependencies", "setup LiteLLM",
  "Python environment", "virtual env", "conda setup".
  Do NOT use for project scaffolding (use scaffolding-ai-project) or for building agents (use building-agent-core).
---
# Setting Up AI Dev Environment

Router-style skill: identify need, read reference, execute, verify.

## Instructions

### Step 1: Identify need
What does the user need?
- Python environment → `references/python-env.md`
- GPU/CUDA setup → `references/gpu-cuda.md`
- API key management → `references/api-keys.md`
- Tool installation (Ollama, Docker, Chroma, Qdrant, LiteLLM) → `references/tool-install.md`
- MCP server config → `references/mcp-config.md`

### Step 2: Read relevant reference
Load ONLY the needed reference file. Do not load all of them.

### Step 3: Execute setup
Run commands from the reference with verification at each step.
Always check existing state first (`python --version`, `which python`, `docker ps`).

Minimal Python AI environment (most common path):
```bash
# Create venv
python3 -m venv .venv && source .venv/bin/activate

# Install core AI dependencies
pip install litellm pydantic python-dotenv

# Create .env for API keys
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
EOF
echo ".env" >> .gitignore
```

### Step 4: Verify
Run verification commands from the reference. Confirm success before moving on.
If verification fails, check troubleshooting section in reference.

Common issues:
- **Wrong Python version**: Use `python3.12` explicitly if system has multiple versions
- **pip not found**: Install with `python -m ensurepip` or use `uv` instead
- **CUDA mismatch**: Check `nvidia-smi` CUDA version matches PyTorch CUDA version

## Quick Verification Commands
```bash
python --version          # Python
nvidia-smi                # GPU
echo $ANTHROPIC_API_KEY   # API keys
ollama list               # Ollama
docker ps                 # Docker
```
