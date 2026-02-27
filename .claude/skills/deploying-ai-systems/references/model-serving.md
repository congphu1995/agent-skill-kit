# Model Serving

## vLLM (Recommended for Production)

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

Uses PagedAttention for efficient GPU memory management. 2-4x throughput vs naive serving.

```bash
# Docker
docker run --gpus all -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.1-8B-Instruct

# Access via OpenAI-compatible API
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "meta-llama/Llama-3.1-8B-Instruct", "prompt": "Hello"}'
```

## Ollama (Development / Edge)

```bash
ollama serve  # Runs on port 11434
ollama pull llama3.1
# OpenAI-compatible: http://localhost:11434/v1/
```

## HF TGI (Deprecated — Use vLLM Instead)

Hugging Face Text Generation Inference. Still works but vLLM has better performance.

## Decision

| Use Case | Tool |
|----------|------|
| Production API serving | vLLM |
| Development / testing | Ollama |
| Cloud API (no self-hosting) | LiteLLM Proxy → OpenAI/Anthropic |
