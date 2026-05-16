# MCP Cursor setup

## Prerequisites

- Private clone of `ohlcx-light` or `ohlcx` with `composer install`
- PHP on PATH
- Cursor with MCP enabled

## Workspace folder

Cursor loads `.cursor/mcp.json` from the **opened workspace root**.

| Workspace root | `artisan` path in MCP config |
|----------------|------------------------------|
| `ohlcx-light/` | `${workspaceFolder}/artisan` |
| Monorepo parent | `${workspaceFolder}/ohlcx-light/artisan` or `${workspaceFolder}/ohlcx/artisan` |

**Recommended:** Open **`ohlcx-light`** as the workspace for the richest dev tooling.

## Example `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "laravel-boost": {
      "command": "php",
      "args": ["${workspaceFolder}/artisan", "boost:mcp"]
    },
    "ohlcx": {
      "command": "php",
      "args": ["${workspaceFolder}/artisan", "mcp:start", "ohlcx"]
    }
  }
}
```

For monorepo layout, replace `${workspaceFolder}` paths with `${workspaceFolder}/ohlcx-light` (or `ohlcx` for Pro).

## Enable servers in Cursor

1. Command palette → **MCP: Open Settings** (or “Open MCP Settings”)
2. Enable toggles for `laravel-boost` and `ohlcx`
3. Restart Cursor after editing `mcp.json`

## Verify

- Invoke MCP tool `ping` → expect `pong`
- Try `search-knowledge-base` without auth
- Authenticated session: list strategies, run `run-trading-agent` with a short message

## Web transport (optional)

With the app running locally:

- Endpoint: `/mcp/ohlcx`
- Auth: Sanctum session or API token as configured in your deployment

## Troubleshooting

| Issue | Check |
|-------|--------|
| No OHLCX tools | Workspace root vs `mcp.json` paths |
| Stale tool list | Restart Cursor; compare [tool catalog](tools/README.md) |
| LLM errors on agent tools | `OPENAI_API_KEY` / `GEMINI_API_KEY` in `.env`, `config/ai.php` |
| 401 on trading tools | Log in; trading agent requires authenticated MCP session |

See [Laravel Boost](https://laravel.com/docs/12.x/boost) and [AI: Cursor and Boost](../ai/cursor-and-boost.md).
