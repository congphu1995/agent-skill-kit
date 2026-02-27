---
name: building-ai-frontend
description: >
  Build React/Next.js frontends with AI components: streaming chat UI, tool visualization, reasoning display, dashboards.
  Use when user says "chat UI", "AI frontend", "dashboard", "monitoring UI", "React for AI",
  "chat interface", "streaming UI", "agent dashboard", "build UI for agent".
  Do NOT use for backend API (use building-backend-api) or for general frontend without AI (use other frontend skills).
---
# Building AI Frontend

Build React/Next.js frontends with AI-powered components: chat interfaces, streaming displays, and agent dashboards.

## Instructions

### Step 1: Identify UI requirements
Ask the user what they need:
- Chat interface (conversational UI with messages)
- Agent dashboard (monitoring, traces, costs)
- Both (full-stack AI app with chat + observability)

### Step 2: Choose stack
Default to Next.js App Router + TypeScript + Tailwind CSS. Alternatives:
- Vite + React if no SSR needed
- Vercel AI SDK (`ai` package) for built-in streaming hooks
- `react-markdown` + `remark-gfm` for LLM output rendering

### Step 3: Implement chat component
Read `references/chat-ui-patterns.md`. Minimal chat component:

```tsx
"use client";
import { useChat } from "ai/react";
import ReactMarkdown from "react-markdown";

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat();
  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m) => (
          <div key={m.id} className={m.role === "user" ? "text-right" : "text-left"}>
            <div className={`inline-block p-3 rounded-lg ${
              m.role === "user" ? "bg-blue-500 text-white" : "bg-gray-100"
            }`}>
              <ReactMarkdown>{m.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {isLoading && <div className="animate-pulse text-gray-400">Thinking...</div>}
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t flex gap-2">
        <input value={input} onChange={handleInputChange}
          className="flex-1 border rounded-lg px-4 py-2"
          placeholder="Ask something..." />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-lg">
          Send
        </button>
      </form>
    </div>
  );
}
```

Build on this with:
- Tool call visualization (collapsible panels showing name, args, result)
- Message type indicators (user / assistant / tool-result)
- Loading / thinking indicators

### Step 4: Add streaming
Read `references/streaming-client.md`. Integrate:
- SSE or fetch + ReadableStream from backend
- Token-by-token rendering with `useChat` hook or custom hook
- Reconnection and error handling
- Abort controller for canceling in-flight requests

### Step 5: Add dashboard components (if needed)
Read `references/dashboard-components.md`. Add:
- Cost tracking (token usage, spend per model)
- Trace viewer (span tree for agent steps)
- Model comparison charts
- Agent performance metrics (latency, success rate, tool usage)

### Step 6: Polish UX
- Auto-scroll to latest message
- Optimistic UI for user messages
- Skeleton loaders during initial fetch
- Mobile-responsive layout
- Keyboard shortcuts (Ctrl+Enter for submit, Escape to cancel)
- Dark mode support via Tailwind `dark:` variants

### Step 7: Connect to backend
Wire up to the agent backend API:
- `POST /chat` for new messages (streaming SSE response)
- `GET /conversations` for history
- `GET /traces` for dashboard data
- Add auth headers if authentication is configured
