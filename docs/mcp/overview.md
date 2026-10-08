# MCP overview

The **OHLCX MCP server** (version 1.1.0) exposes tools, prompts and a resource for the trading platform: strategies, backtests, signals, trades, Workspaces, markets, sectors, news, conditions, knowledge base, messaging, billing, and user administration.

Implementation lives in the private **`ohlcx/trading-app`** package (`OHLCX\TradingApp\Mcp`).

## Transports

| Transport | How to use | Auth |
|-----------|------------|------|
| **Web** | `GET/POST` `/mcp/ohlcx` while app is running | Laravel Sanctum (session/token) |
| **Stdio** | `php artisan mcp:start ohlcx` | Optional; some tools require authenticated session |

## Prompts

| Name | Description |
|------|-------------|
| `user-info` | Current user summary (authenticated sessions) |
| `trading-terminology` | TSP, OCO, TRIM, order types |
| `support-knowledge-base` | Support answers from KB |

## Resources

| URI | Description |
|-----|-------------|
| `ohlcx://strategy-settings` | Every strategy setting by section, with its allowed values. Read it before `create-strategy` or `update-strategy-settings` |

## What's new in 1.1.0

| Area | Tools |
|------|-------|
| Saved backtests | `list-backtests`, `get-backtest`, `rename-backtest`, `delete-backtest` |
| Server-side backtests | `run-backtest`, `run-backtest-sweep`, `list-backtest-jobs`, `get-backtest-job`, `cancel-backtest-job` |
| Strategy insight | `get-strategy-statistics`, `get-strategy-performance`, `get-strategy-timeline`, `list-strategy-signals`, `list-strategy-trades`, `get-strategy-flags`, `get-strategies-statistics`, `get-strategies-performance` |
| Strategy control | `set-strategy-status`, `set-strategy-flag`, `set-strategy-schedule`, `update-strategy-settings`, `clear-strategy-data` |
| Trades | `list-trades`, `get-trade`, `delete-trade` |
| Signals | `get-signal`, `delete-signal`, `set-signal-action`, `get-signal-actions` |
| Workspaces | `get-workspaces`, `save-workspaces` |

Notes:

- **Server-side backtests** are listed only when the app has server backtests switched on (`TRADING_APP_BACKTEST_SERVER_RUNS`). A run finishes as a saved backtest (read it with `get-backtest`); a sweep finishes with its ranked results on the job.
- **`get-backtest`** returns the run's metrics and settings. The trade list, equity curve and strategy snapshot are large, so ask for them with `include`.
- **`save-workspaces`** sends the whole document with the `revision` read from `get-workspaces`. If the Workspaces changed somewhere else in the meantime, nothing is saved and the current state and revision come back to merge into.
- **`get-user`** is now available to every signed-in user for their own account. Only admins may pass `user_id`.

## Safety

- No tool places, changes or cancels a broker order. A strategy that is switched on with orders on does, so `set-strategy-status`, `set-strategy-flag` and `update-strategy-settings` are marked destructive and MCP clients should ask before calling them.
- A strategy can only be read or changed by the user who owns it; this is enforced by the API, not by the MCP server.
- Tools that delete or clear data are marked destructive.

## AI bridge tools

MCP is separate from in-app Laravel AI agents, but two MCP tools invoke agents in-process:

| Tool | Agent | Auth |
|------|-------|------|
| `run-support-agent` | SupportKnowledgeAgent (KB only) | No MCP auth required |
| `run-trading-agent` | TradingAssistantAgent | Authenticated MCP session |

Returns **plain text** from the configured LLM (`config/ai.php`).

## Tool catalog

Full list: **[Tool catalog](tools/README.md)** (generated from server descriptors).

Machine-readable index: [tools/index.json](tools/index.json)

## Canonical source

When using a private checkout, the live tool list is defined in:

- `OHLCX\TradingApp\Mcp\Servers\OHLCXServer`
- `src/Mcp/descriptors/*.json`

Reconnect Cursor or restart the IDE after changing tool registrations.

## Related

- [Cursor setup](cursor-setup.md)
- [AI overview](../ai/overview.md)
- [Agents](../ai/agents.md)
