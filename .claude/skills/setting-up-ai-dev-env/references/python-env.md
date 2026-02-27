# Python Environment Setup

## pyenv (Recommended for version management)

```bash
# Install pyenv
curl https://pyenv.run | bash

# Add to shell (add to ~/.bashrc or ~/.zshrc)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Install Python
pyenv install 3.11.9
pyenv local 3.11.9    # Set for current directory
pyenv global 3.11.9   # Set as default

# Verify
python --version  # Python 3.11.9
```

## Virtual Environment (venv)

```bash
# Create
python -m venv .venv

# Activate
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows

# Verify
which python                 # Should show .venv path
pip list                     # Should be minimal

# Deactivate
deactivate
```

## conda

```bash
# Install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Create environment
conda create -n agent-dev python=3.11 -y
conda activate agent-dev

# Verify
python --version
conda list
```

## uv (Fast pip replacement)

```bash
# Install
pip install uv

# Create venv + install (10-100x faster than pip)
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Or single command
uv pip install litellm langchain-core pydantic
```

## Common AI Dependencies

```bash
# Core
pip install litellm instructor pydantic python-dotenv

# Frameworks (pick one)
pip install langgraph                    # LangGraph
pip install crewai                       # CrewAI
pip install pydantic-ai                  # PydanticAI

# Tools
pip install chromadb qdrant-client       # Vector DBs
pip install langfuse                     # Observability
pip install promptfoo                    # Eval (or use npx)
```

## Troubleshooting
- **`python` not found**: Check PATH, restart shell, `which python3`
- **Wrong Python version**: `pyenv versions` to check, `pyenv local X.Y.Z` to set
- **Permission errors**: Don't use `sudo pip install`, use venv instead
- **Package conflicts**: Use separate venvs per project
