# Streaming Client Patterns

Client-side streaming for AI chat frontends.

## Fetch + ReadableStream

```typescript
async function streamChat(
  messages: { role: string; content: string }[],
  onToken: (token: string) => void, signal?: AbortSignal
) {
  const res = await fetch("/api/chat", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }), signal,
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    for (const line of decoder.decode(value, { stream: true }).split("\n")) {
      if (line.startsWith("data: ") && line.slice(6) !== "[DONE]") onToken(line.slice(6));
    }
  }
}
```

## React Hook: useStreamingChat

```typescript
export function useStreamingChat() {
  const [messages, setMessages] = useState<{ id: string; role: string; content: string }[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const send = useCallback(async (input: string) => {
    const userMsg = { id: crypto.randomUUID(), role: "user", content: input };
    const asstMsg = { id: crypto.randomUUID(), role: "assistant", content: "" };
    setMessages((prev) => [...prev, userMsg, asstMsg]);
    setIsStreaming(true);
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    try {
      await streamChat(
        [...messages, userMsg].map(({ role, content }) => ({ role, content })),
        (token) => setMessages((prev) => {
          const u = [...prev];
          u[u.length - 1] = { ...u[u.length - 1], content: u[u.length - 1].content + token };
          return u;
        }), ctrl.signal
      );
    } catch (e) {
      if ((e as Error).name !== "AbortError")
        setMessages((p) => { const u=[...p]; u[u.length-1]={...u[u.length-1], content:"Error: request failed."}; return u; });
    }
    setIsStreaming(false);
  }, [messages]);

  const stop = useCallback(() => { abortRef.current?.abort(); setIsStreaming(false); }, []);
  return { messages, isStreaming, send, stop };
}
```

## Vercel AI SDK (Simpler Alternative)

```tsx
import { useChat } from "@ai-sdk/react"; // npm install ai @ai-sdk/react

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, stop } = useChat({
    api: "/api/chat",
  });
  return (
    <div>
      {messages.map((m) => <div key={m.id}>{m.role}: {m.content}</div>)}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        {isLoading ? <button onClick={stop}>Stop</button> : <button type="submit">Send</button>}
      </form>
    </div>
  );
}
```

## Reconnection with Backoff

```typescript
async function streamWithRetry(msgs: { role: string; content: string }[], onToken: (t: string) => void, retries = 3) {
  for (let i = 0; i <= retries; i++) {
    try { await streamChat(msgs, onToken); return; }
    catch (e) { if (i === retries) throw e; await new Promise(r => setTimeout(r, 1000 * 2 ** i)); }
  }
}
```
