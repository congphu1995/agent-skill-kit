# Chat UI Patterns

React component patterns for AI chat interfaces.

## Message Types

```typescript
type Message =
  | { id: string; role: "user" | "assistant"; content: string; createdAt: Date }
  | { id: string; role: "tool"; toolName: string; args: Record<string, unknown>;
      result?: string; status: "pending" | "success" | "error"; createdAt: Date };
```

## Message List with Auto-Scroll

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  const bottomRef = useRef<HTMLDivElement>(null);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((msg) => <MessageBubble key={msg.id} message={msg} />)}
      <div ref={bottomRef} />
    </div>
  );
}
```

## Message Bubble with Markdown

```tsx
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function MessageBubble({ message }: { message: Message }) {
  if (message.role === "tool") return <ToolCallCard message={message} />;
  const isUser = message.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[80%] rounded-lg px-4 py-2 ${
        isUser ? "bg-blue-600 text-white" : "bg-gray-100 dark:bg-gray-800"}`}>
        {isUser ? <p className="whitespace-pre-wrap">{message.content}</p>
          : <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>}
      </div>
    </div>
  );
}
```

## Tool Call Visualization (Collapsible)

```tsx
function ToolCallCard({ message }: { message: Extract<Message, { role: "tool" }> }) {
  const [open, setOpen] = useState(false);
  const icon = { pending: "...", success: "ok", error: "err" }[message.status];
  return (
    <div className="border rounded-lg p-3 bg-gray-50 dark:bg-gray-900 text-sm font-mono">
      <button onClick={() => setOpen(!open)} className="flex items-center gap-2 w-full">
        <span>[{icon}]</span>
        <span className="font-semibold">{message.toolName}</span>
      </button>
      {open && (
        <div className="mt-2 text-xs space-y-1">
          <pre className="bg-white dark:bg-gray-800 p-2 rounded overflow-x-auto">
            {JSON.stringify(message.args, null, 2)}
          </pre>
          {message.result && (
            <pre className="bg-white dark:bg-gray-800 p-2 rounded overflow-x-auto">
              {message.result}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
```

## Chat Input

```tsx
function ChatInput({ onSend, disabled }: { onSend: (text: string) => void; disabled: boolean }) {
  const [input, setInput] = useState("");
  const submit = () => { const t = input.trim(); if (t && !disabled) { onSend(t); setInput(""); } };
  return (
    <div className="border-t p-4 flex gap-2">
      <textarea value={input} onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(); } }}
        placeholder="Type a message..." rows={1}
        className="flex-1 resize-none rounded-lg border p-2 focus:outline-none focus:ring-2"
        disabled={disabled} />
      <button onClick={submit} disabled={disabled || !input.trim()}
        className="rounded-lg bg-blue-600 px-4 py-2 text-white disabled:opacity-50">Send</button>
    </div>
  );
}
```

## Thinking Indicator

```tsx
function ThinkingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-2 flex items-center gap-1">
        {[0, 150, 300].map((d) => (
          <span key={d} className={`h-2 w-2 bg-gray-400 rounded-full animate-bounce`}
            style={{ animationDelay: `${d}ms` }} />
        ))}
      </div>
    </div>
  );
}
```
