# Managed Deployment Platforms

## LangGraph Cloud

Deploy LangGraph agents as managed services.

```bash
# Install CLI
pip install langgraph-cli

# Create langgraph.json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.py:graph"
  }
}

# Deploy
langgraph deploy
```

Features: managed checkpointing, auto-scaling, built-in monitoring.

## Modal (Serverless GPU)

```python
import modal

app = modal.App("my-agent")

@app.function(gpu="A10G", timeout=300)
def run_agent(prompt: str):
    from vllm import LLM
    llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct")
    return llm.generate(prompt)
```

Features: pay-per-use GPU, auto-scaling to zero, simple deployment.

## Railway / Render / Fly.io

Generic container hosting. Good for FastAPI agent backends:
```bash
# Fly.io
fly launch
fly deploy

# Railway
railway up
```

## Decision

| Need | Platform |
|------|----------|
| LangGraph agents | LangGraph Cloud |
| GPU inference | Modal |
| Simple container hosting | Railway / Fly.io |
| Full control | Self-hosted K8s |
