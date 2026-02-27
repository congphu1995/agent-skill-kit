# Dashboard Components

React components for AI agent monitoring and observability.

## Cost Tracking
```tsx
interface UsageData { model: string; inputTokens: number; outputTokens: number; cost: number }
function CostTracker({ usage }: { usage: UsageData[] }) {
  const total = usage.reduce((s, u) => s + u.cost, 0);
  const byModel = Object.groupBy(usage, (u) => u.model);
  return (
    <div className="rounded-lg border p-4">
      <p className="text-3xl font-bold">${total.toFixed(4)}</p>
      {Object.entries(byModel).map(([m, e]) => (
        <div key={m} className="flex justify-between text-sm mt-1">
          <span className="font-mono">{m}</span>
          <span>${e!.reduce((s, x) => s + x.cost, 0).toFixed(4)}</span>
        </div>))}
    </div>);
}
```

## Trace Viewer
```tsx
interface Span { id: string; name: string; duration_ms: number; status: "ok"|"error"; children: Span[] }
function SpanNode({ span, depth }: { span: Span; depth: number }) {
  const [open, setOpen] = useState(true);
  return (
    <div style={{ marginLeft: depth * 16 }}>
      <button onClick={() => setOpen(!open)} className="flex gap-2 w-full hover:bg-gray-100 rounded px-1">
        {span.children.length > 0 && <span>{open ? "v" : ">"}</span>}
        <span className={span.status === "error" ? "text-red-600" : ""}>{span.name}</span>
        <span className="text-gray-400 ml-auto">{span.duration_ms}ms</span>
      </button>
      {open && span.children.map((c) => <SpanNode key={c.id} span={c} depth={depth + 1} />)}
    </div>);
}

function TraceViewer({ spans }: { spans: Span[] }) {
  return (
    <div className="rounded-lg border p-4 font-mono text-sm">
      {spans.map((s) => <SpanNode key={s.id} span={s} depth={0} />)}
    </div>);
}
```

## Model Comparison (recharts)
```tsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
function ModelComparison({ data }: { data: { model: string; p50: number; p99: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={data}>
        <XAxis dataKey="model" /><YAxis /><Tooltip />
        <Bar dataKey="p50" name="P50 (ms)" fill="#3b82f6" />
        <Bar dataKey="p99" name="P99 (ms)" fill="#f59e0b" />
      </BarChart>
    </ResponsiveContainer>);
}
```

## Agent Performance
```tsx
function AgentPerformance({ metrics }: { metrics: {
  totalRequests: number; successRate: number; avgLatencyMs: number;
  toolUsage: { name: string; count: number }[];
}}) {
  return (
    <div className="rounded-lg border p-4">
      <div className="grid grid-cols-3 gap-4 text-center mb-3">
        {[["Requests", metrics.totalRequests.toLocaleString()],
          ["Success", `${(metrics.successRate*100).toFixed(1)}%`],
          ["Latency", `${metrics.avgLatencyMs.toFixed(0)}ms`],
        ].map(([l,v]) => <div key={l}><p className="text-2xl font-bold">{v}</p><p className="text-xs text-gray-500">{l}</p></div>)}
      </div>
      {metrics.toolUsage.map((t) => (
        <div key={t.name} className="flex justify-between text-sm"><span className="font-mono">{t.name}</span><span>{t.count}</span></div>))}
    </div>);
}
```
