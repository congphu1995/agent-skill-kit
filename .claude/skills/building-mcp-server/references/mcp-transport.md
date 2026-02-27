# MCP Transport Mechanisms

MCP supports multiple transport mechanisms for communication between clients and servers. Choose the right transport based on your deployment scenario.

---

## stdio (Standard I/O)

Simple pipe-based communication for local servers. The client spawns the server as a child process and communicates via stdin/stdout.

**Use for:** CLI tools, local integrations, development, desktop applications.

**Configuration example:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["server.py"],
      "type": "stdio"
    }
  }
}
```

**Characteristics:**
- No network setup required
- Client manages the server process lifecycle
- Simple to debug (stderr available for logging)
- No authentication needed (inherits process permissions)
- Single client per server instance

---

## Streamable HTTP

The recommended transport for remote and production servers. Replaces the deprecated SSE transport.

**Use for:** Production deployments, remote servers, multi-client scenarios, cloud-hosted services.

**Key features:**
- **Stateless JSON request/response**: Each tool call is an independent HTTP POST request, making it simple to scale horizontally behind load balancers
- **Server-Sent Events (SSE) for streaming**: Servers can upgrade responses to SSE streams for long-running operations or progress notifications
- **Session management**: Optional session tokens for stateful interactions when needed
- **Better scaling characteristics**: Stateless design works well with container orchestration and auto-scaling

**Configuration example:**

```json
{
  "mcpServers": {
    "my-remote-server": {
      "url": "https://my-server.example.com/mcp",
      "type": "streamable-http"
    }
  }
}
```

**Characteristics:**
- Works across network boundaries
- Supports authentication headers
- Multiple clients can connect simultaneously
- Compatible with standard HTTP infrastructure (proxies, load balancers, CDNs)

---

## SSE (Server-Sent Events) - Deprecated

Legacy transport that used a persistent SSE connection for server-to-client messages and HTTP POST for client-to-server messages.

**Status:** Deprecated. Migrate existing SSE implementations to Streamable HTTP.

**Migration notes:**
- Streamable HTTP supports SSE streaming as an optional upgrade, preserving streaming capabilities
- The stateless default mode of Streamable HTTP is simpler to operate
- Most MCP SDKs now default to Streamable HTTP

---

## Choosing a Transport

| Scenario | Transport | Reason |
|---|---|---|
| Local CLI tool | stdio | No network overhead, simple setup |
| Development/testing | stdio | Easy to debug, no server config |
| Desktop app integration | stdio | Client controls server lifecycle |
| Production API service | Streamable HTTP | Scalable, multi-client support |
| Remote/cloud server | Streamable HTTP | Network accessible, load-balanced |
| Existing SSE server | Streamable HTTP | Migrate from deprecated SSE |

**Rule of thumb:** Use stdio for local development, Streamable HTTP for anything production or remote.
