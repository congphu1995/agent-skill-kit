# API Key Management

## .env File Pattern

```bash
# .env (NEVER commit this file)
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
COHERE_API_KEY=...
GOOGLE_API_KEY=...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

## .env.example (Commit this)

```bash
# .env.example — copy to .env and fill in values
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
COHERE_API_KEY=
```

## .gitignore

```
.env
.env.local
.env.*.local
```

## Loading in Python

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set. Copy .env.example to .env and fill in values.")
```

## LiteLLM Auto-Detection
LiteLLM reads standard env vars automatically:
- `ANTHROPIC_API_KEY` → Claude models
- `OPENAI_API_KEY` → GPT models
- `COHERE_API_KEY` → Cohere models
- `OLLAMA_API_BASE` → Ollama (default: http://localhost:11434)

## Verification

```bash
# Check key is set (show first 10 chars only)
python -c "import os; k=os.getenv('ANTHROPIC_API_KEY','NOT SET'); print(f'{k[:10]}...' if len(k)>10 else k)"

# Test API connection
python -c "
from litellm import completion
r = completion(model='claude-haiku-4-5-20251001', messages=[{'role':'user','content':'Hi'}], max_tokens=5)
print('OK:', r.choices[0].message.content)
"
```

## Key Providers

| Provider | Env Var | Get Key |
|----------|---------|---------|
| Anthropic | `ANTHROPIC_API_KEY` | console.anthropic.com |
| OpenAI | `OPENAI_API_KEY` | platform.openai.com |
| Cohere | `COHERE_API_KEY` | dashboard.cohere.com |
| Google AI | `GOOGLE_API_KEY` | aistudio.google.com |
