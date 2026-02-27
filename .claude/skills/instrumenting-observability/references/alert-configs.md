# Alert Configurations

Rules and notification patterns for AI system monitoring.

## Alert Rules

```python
ALERT_RULES = {
    "high_latency": {
        "condition": "p95_latency_ms > 5000", "window": "5m",
        "severity": "warning", "message": "Agent p95 latency exceeds 5s",
    },
    "error_spike": {
        "condition": "error_rate > 0.05", "window": "10m",
        "severity": "critical", "message": "Error rate exceeds 5%",
    },
    "llm_timeout": {
        "condition": "timeout_count > 10", "window": "15m",
        "severity": "warning", "message": "LLM timeouts spiking",
    },
    "hourly_cost_spike": {
        "condition": "hourly_cost_usd > 50", "severity": "critical",
        "action": "disable_expensive_models",
    },
    "daily_budget": {
        "condition": "daily_cost_usd > 200", "severity": "critical",
        "action": "switch_to_fallback_model",
    },
}
```

## Slack Notification

```python
import httpx

async def send_slack_alert(webhook_url: str, rule_name: str, details: str):
    payload = {
        "text": f":rotating_light: *Alert: {rule_name}*\n{details}",
        "channel": "#ai-alerts",
    }
    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json=payload)
```

## Email Notification (SMTP)

```python
import smtplib, os
from email.message import EmailMessage

def send_email_alert(to: str, rule_name: str, details: str):
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = f"[AI Alert] {rule_name}", "alerts@myapp.com", to
    msg.set_content(details)
    with smtplib.SMTP("smtp.myapp.com", 587) as s:
        s.starttls()
        s.login("alerts@myapp.com", os.environ["SMTP_PASSWORD"])
        s.send_message(msg)
```
