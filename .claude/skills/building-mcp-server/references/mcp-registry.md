# MCP Server Discovery and Registration

How MCP servers are discovered, registered, and connected to by clients.

---

## MCP Registry

The official MCP registry is hosted at:

```
https://registry.modelcontextprotocol.io
```

The registry serves as a central directory where MCP servers can be published and discovered. It provides:
- A searchable catalog of available MCP servers
- Server metadata (name, version, capabilities, transport types)
- Installation instructions and configuration details

---

## .well-known Discovery

MCP supports automatic server discovery via the `.well-known` convention:

```
https://example.com/.well-known/mcp.json
```

This file allows any domain to advertise its MCP server capabilities. The `mcp.json` file contains:
- Server endpoint URL
- Supported transport types
- Available capabilities (tools, resources, prompts)
- Authentication requirements

Clients can probe a domain's `.well-known/mcp.json` to automatically detect and configure MCP server connections.

---

## Server Identity

Every MCP server declares its identity during the `initialize` handshake:

- **name**: Human-readable server name (e.g., `github-mcp-server`)
- **version**: Semantic version string (e.g., `1.2.0`)
- **capabilities**: Declared feature support:
  - `tools` - server provides callable tools
  - `resources` - server exposes readable resources
  - `prompts` - server offers prompt templates

Clients use this identity information to verify compatibility and display server details to users.

---

## Publishing a Server

To publish an MCP server to the registry:

1. **Prepare metadata**: Define server name, description, version, supported transports, and capabilities
2. **Ensure discoverability**: Host a `.well-known/mcp.json` file on your domain if applicable
3. **Submit to the registry**: Follow the submission process at `registry.modelcontextprotocol.io`
4. **Provide documentation**: Include clear setup instructions, required environment variables, and authentication details
5. **Maintain versioning**: Use semantic versioning and update the registry entry for new releases

---

## Discovery Patterns

Clients find and connect to MCP servers through several patterns:

- **Local configuration**: User specifies servers in a config file (e.g., `claude_desktop_config.json` or `.mcp.json` in a project)
- **Registry search**: Client queries the MCP registry to find servers by name or capability
- **Well-known probing**: Client checks a domain's `/.well-known/mcp.json` for server information
- **Direct URL**: User provides a Streamable HTTP endpoint URL directly

Once discovered, the client initiates the MCP handshake (`initialize` request), negotiates protocol version and capabilities, and begins issuing requests.
