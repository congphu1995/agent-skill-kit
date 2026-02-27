# MCP Configuration

## .mcp.json Structure

Place `.mcp.json` in project root or `~/.claude/` for global config.

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

## stdio Transport (Local Servers)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "my-python-server": {
      "command": "python",
      "args": ["src/mcp_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

## HTTP Transport (Remote Servers)

```json
{
  "mcpServers": {
    "remote-api": {
      "url": "https://mcp.example.com/sse",
      "headers": {
        "Authorization": "Bearer ${MCP_API_KEY}"
      }
    }
  }
}
```

## Common Server Configs

### GitHub
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### PostgreSQL
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

### Custom Python Server
```json
{
  "mcpServers": {
    "my-agent-tools": {
      "command": "python",
      "args": ["-m", "src.mcp_server"],
      "cwd": "/path/to/project"
    }
  }
}
```

## Verification
1. Add config to `.mcp.json`
2. Restart Claude Code
3. Check tools are loaded: the MCP server's tools should appear in available tools
4. Test a tool call to verify connectivity
