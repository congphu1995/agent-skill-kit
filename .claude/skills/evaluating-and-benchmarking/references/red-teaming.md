# Red-Teaming AI Systems

> Stub -- expand after first project using extracting-patterns (F2)

## Tools

- **Garak:** LLM vulnerability scanner -- automated probes for prompt injection, data leakage, encoding attacks
- **PyRIT:** Microsoft's Python Risk Identification Toolkit -- multi-turn adversarial conversation testing
- **DeepTeam:** Adversarial testing framework built on DeepEval -- 40+ attack types with automated scoring

## OWASP Top 10 for LLMs

Key vulnerabilities to test for:

1. **Prompt injection** -- Direct and indirect injection that overrides system instructions
2. **Insecure output handling** -- LLM output used unsafely in downstream systems (SQL, shell, HTML)
3. **Training data poisoning** -- Manipulated training data influencing model behavior
4. **Denial of service** -- Resource-exhausting prompts that degrade availability
5. **Supply chain vulnerabilities** -- Compromised plugins, tools, or model weights
6. **Sensitive information disclosure** -- Model leaking PII, credentials, or system prompts
7. **Insecure plugin design** -- Tools with excessive permissions or insufficient input validation
8. **Excessive agency** -- Model taking actions beyond intended scope without human approval
9. **Overreliance** -- Insufficient validation of model outputs before acting on them
10. **Model theft** -- Extraction of model weights or capabilities through API queries

## Quick Start with Garak

```bash
pip install garak
garak --model_type openai --model_name gpt-4o --probes all
```

## Quick Start with PyRIT

```bash
pip install pyrit
# See Microsoft docs for multi-turn attack orchestration setup
```

## Minimum Red-Team Checklist

- [ ] System prompt extraction attempts
- [ ] Direct prompt injection ("ignore previous instructions")
- [ ] Indirect prompt injection via user-supplied content
- [ ] PII leakage probes
- [ ] Tool misuse scenarios (if agent has tool access)
- [ ] Encoding-based bypasses (base64, rot13, unicode)
