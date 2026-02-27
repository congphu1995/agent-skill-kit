# Next.js + AI Frontend Template

## Directory Structure
```
<project-name>/
  src/
    app/
      layout.tsx, page.tsx
      api/chat/route.ts    # Chat streaming endpoint
      api/agent/route.ts   # Agent endpoint
    components/chat/ChatWindow.tsx, ui/
    lib/ai.ts, agents/index.ts, tools/index.ts
    models/schemas.ts      # Zod schemas
    hooks/useChat.ts
  tests/unit/, e2e/
  evals/
  public/
  .env.example, package.json, tsconfig.json, next.config.ts, Dockerfile
```

## package.json
```json
{
  "name": "<project-name>",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest run"
  },
  "dependencies": {
    "next": "^15.1",
    "react": "^19.0",
    "react-dom": "^19.0",
    "ai": "^4.1",
    "@ai-sdk/openai": "^1.1",
    "@ai-sdk/anthropic": "^1.1",
    "zod": "^3.24"
  },
  "devDependencies": {
    "typescript": "^5.7",
    "@types/react": "^19.0",
    "vitest": "^2.1",
    "tailwindcss": "^4.0"
  }
}
```

## src/app/api/chat/route.ts
```typescript
import { streamText } from "ai";
import { openai } from "@ai-sdk/openai";

export async function POST(req: Request) {
  const { messages } = await req.json();
  const result = streamText({
    model: openai("gpt-4o"),
    system: "You are a helpful assistant.",
    messages,
  });
  return result.toDataStreamResponse();
}
```

## .env.example
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
