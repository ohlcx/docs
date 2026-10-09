# MCP Cursor setup

This page connects Cursor to the OHLCX MCP server of a local checkout. For what the server offers once connected, see the [MCP overview](overview.md).

Using Claude or an agent instead? See [Claude setup](claude-setup.md) and [Agents setup](agents-setup.md).

## Prerequisites

- A private clone of `ohlcx-light` or `ohlcx` with `composer install` done
- PHP on your `PATH`
- Cursor with MCP enabled

## Workspace folder

Cursor loads `.cursor/mcp.json` from the root of the workspace you opened.

| Workspace root | `artisan` path in the MCP config |
|----------------|----------------------------------|
| `ohlcx-light/` | `${workspaceFolder}/artisan` |
| Monorepo parent | `${workspaceFolder}/ohlcx-light/artisan` or `${workspaceFolder}/ohlcx/artisan` |

Open `ohlcx-light` as the workspace when you can: it has the fullest development tooling.

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

For the monorepo layout, replace `${workspaceFolder}` with `${workspaceFolder}/ohlcx-light` (or `${workspaceFolder}/ohlcx` for Pro).

## Enable the servers in Cursor

1. Open the command palette and choose **MCP: Open Settings**.
2. Switch on `laravel-boost` and `ohlcx`.
3. Restart Cursor after you edit `mcp.json`.

## Check the connection

1. Call `ping`. It answers `pong`.
2. Call `search-knowledge-base` with a `q`, for example `dashboard`. This works without a signed-in user.
3. With a signed-in user, call `list-strategies` and `list-accounts`.

## Which tools you will see

The tool list depends on who is signed in. See [Transports and sign-in](overview.md#transports-and-sign-in).

| Connection | Tools listed |
|------------|--------------|
| Stdio, no signed-in user | `ping`, `run-support-agent`, `search-knowledge-base`, `get-knowledge-base-article` |
| Web (`/mcp/ohlcx`), signed in | The tools for a signed-in user, plus the admin tools for an admin |

`list-strategy-accounts` and `set-strategy-accounts` are listed only on OHLCX Pro. The five server backtest tools and the four support ticket tools are listed only where the app has those features switched on.

## Web transport

With the app running locally:

- Endpoint: `/mcp/ohlcx`
- Sign-in: a Sanctum session or API token, as configured in your deployment

## Before you let a client act

The server can switch a strategy's orders on and choose the brokerage accounts that receive them. Set your client to ask before it calls a tool that writes, and never approve these automatically: `set-strategy-accounts`, `set-strategy-flag`, `set-strategy-status`, `deploy-strategy`, `retain-strategy`, `update-strategy-settings`, and any tool that deletes. See [What needs the user's confirmation](overview.md#what-needs-the-users-confirmation).

## Troubleshooting

| Issue | Check |
|-------|-------|
| No OHLCX tools | The workspace root against the paths in `mcp.json` |
| Only four tools | No user is signed in on this connection. Use the web transport with a signed-in user |
| A tool from the reference is missing | Compare the [tool reference](tools/reference.md): each tool says who is offered it |
| Stale tool list | Restart Cursor, or disconnect and reconnect the `ohlcx` server |
| The assistant tools fail | The language model keys in `.env` (`OPENAI_API_KEY` or `GEMINI_API_KEY`) and `config/ai.php` |
| `User not authenticated.` | Sign in. See [Errors and refusals](errors.md#not-signed-in) |

See [Laravel Boost](https://laravel.com/docs/12.x/boost) and [AI: Cursor and Boost](../ai/cursor-and-boost.md).
