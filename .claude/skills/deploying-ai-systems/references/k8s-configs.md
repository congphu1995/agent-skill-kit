# Kubernetes Configs for AI Systems

## Agent Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agent-api
  template:
    metadata:
      labels:
        app: agent-api
    spec:
      containers:
        - name: agent-api
          image: myregistry/agent-api:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: agent-secrets
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "1Gi"
              cpu: "1"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: agent-api
spec:
  selector:
    app: agent-api
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
```

## GPU Pod (NVIDIA GPU Operator)

```yaml
spec:
  containers:
    - name: model-server
      image: myregistry/model-server:latest
      resources:
        limits:
          nvidia.com/gpu: 1
```

## Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: agent-secrets
type: Opaque
stringData:
  OPENAI_API_KEY: "sk-..."
  ANTHROPIC_API_KEY: "sk-ant-..."
```

## Micro-Agents per Pod
Deploy each agent as a separate deployment for independent scaling:
- `classifier-agent` (1 replica, CPU)
- `researcher-agent` (2 replicas, CPU)
- `writer-agent` (1 replica, GPU optional)
