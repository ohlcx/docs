# MCP overview

The **OHLCX MCP server** exposes tools and prompts for the trading platform: strategies, signals, markets, sectors, news, conditions, knowledge base, messaging, billing, and user administration.

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
