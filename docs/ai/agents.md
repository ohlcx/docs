# Laravel AI agents (OHLCX)

**Related:** [In-app assistant](in-app-assistant.md) (drawer modes, recording script), [MCP tool catalog](../mcp/tools/README.md) (generated from server descriptors).

Agents live under `src/Ai/Agents/` (namespace `OHLCX\TradingApp\Ai\Agents`). They use **Laravel AI** tools in `src/Ai/Tools/` (interface `Laravel\Ai\Contracts\Tool`), which is separate from MCP tools in `src/Mcp/Tools/`.

## Agents

| Agent | Class | Tools | Typical use |
| ----- | ----- | ----- | ----------- |
| Support (KB only) | `OHLCX\TradingApp\Ai\Agents\SupportKnowledgeAgent` | KB search + get-by-slug | Public support answers; no account data. |
| Trading assistant | `OHLCX\TradingApp\Ai\Agents\TradingAssistantAgent` | KB + strategies + accounts; **Pro:** markets, tickers, sectors (list + one sector + sector balance), calendar, market balance | Authenticated session; `APP_VERSION=pro` adds live market tools. |
| Unified assistant | `OHLCX\TradingApp\Ai\Agents\UnifiedAssistantAgent` | KB; **if authenticated:** strategies, accounts, signals, activities, analysis, news; **if also Pro:** same market tools as trading | `POST /api/ai/agents/assistant` — combined help + live data when available. |

`list_sectors` uses the upstream **`sectors`** API when available, otherwise distinct sector names from **`markets`**. OHLCX Light does **not** install the `ohlcx/sectors` package; sector HTTP is proxied only (see [Light vs Pro](../architecture/light-vs-pro.md)).

Instructions are loaded from:

- `resources/prompts/support-knowledge-agent.md`
- `resources/prompts/trading-assistant-agent.md`
- `resources/prompts/unified-assistant-agent.md`

## AI tool names (all `OHLCX\TradingApp\Ai\Tools`)

These are the `name()` strings registered with the model (17 tools). Which agent exposes which tool depends on auth and `APP_VERSION` — see `AiAgentToolsInventoryTest`.

| `name()` | Purpose (short) |
| -------- | ----------------- |
| `search_knowledge_base_articles` | Search/list KB articles |
| `get_knowledge_base_article_by_slug` | Full article by slug |
| `list_trading_strategies` | User strategies (OHLCX API) |
| `list_brokerage_accounts` | Linked accounts |
| `list_signals` | Trading signals |
| `get_strategy_activities` | Activities for a strategy id |
| `get_analysis` | Analysis feed |
| `list_news` | News list |
| `list_markets` | Markets (Pro) |
| `get_market` | One market (Pro) |
| `list_tickers` | Tickers (Pro) |
| `get_ticker` | One ticker (Pro) |
| `list_sectors` | Sector names: upstream `sectors` API, else from markets (Pro) |
| `get_sector` | One sector by id from upstream API (Pro) |
| `get_market_calendar` | Calendar (Pro) |
| `get_market_balance` | Market balance chart data (Pro) |
| `get_sector_balance` | Sector balance chart data (Pro) |

## MCP vs Laravel AI tools

- **MCP** (`OHLCXServer`, `src/Mcp/Tools/*`): dozens of tools for Cursor/IDE and HTTP transport — strategies CRUD, messaging, admin, etc. **Descriptors** live in `src/Mcp/descriptors/` and `index.json` (source of truth for the full list). The Cursor UI may show only a **subset** of tools depending on client config; trust the server registration in `OHLCXServer.php` for the canonical catalog.
- **Laravel AI** (`src/Ai/Tools/*`): slim read-only tools for chat agents and the in-app drawer. Same *domain* as some MCP tools (e.g. markets, KB) but **different PHP classes** and wire-up.

## MCP bridge tools

Registered on `OHLCX\TradingApp\Mcp\Servers\OHLCXServer`:

| MCP tool | Auth | Effect |
| -------- | ---- | ------ |
| `run-support-agent` | None (same family as `ping` + KB reads) | Runs `SupportKnowledgeAgent::make()->prompt($message)`; **invokes configured LLM**. |
| `run-trading-agent` | Authenticated MCP session only (`RegistersWhenAuthenticated`) | Runs `TradingAssistantAgent::make(user: $user)->prompt($message)`; **invokes configured LLM**. |

Descriptors: `src/Mcp/descriptors/run-support-agent.json`, `run-trading-agent.json`.

## Cursor stdio call examples
In Cursor’s MCP tool UI, select the tool and pass the JSON arguments below.

`run-support-agent` (no MCP auth required)
```json
{ "message": "tell me about ohlcx" }
```

`run-trading-agent` (only listed when the MCP request is authenticated)
```json
{ "message": "Summarize my linked accounts and strategies." }
```

Both tools return **plain text** responses.

## Configuration & cost

- Providers and keys: `config/ai.php` (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- Bridge tools perform real model calls unless you fake agents in tests (`SupportKnowledgeAgent::fake([...])`).
- Prefer the normal MCP data tools for deterministic results; use bridge agents when you need multi-step reasoning with tool use.

## In-app usage

```php
use OHLCX\TradingApp\Ai\Agents\SupportKnowledgeAgent;
use OHLCX\TradingApp\Ai\Agents\TradingAssistantAgent;

$support = SupportKnowledgeAgent::make()->prompt('How do I use OCO on options?');

$trading = TradingAssistantAgent::make(user: auth()->user())
    ->prompt('Summarize my linked accounts and strategies.');
```

## Tests

| Suite | File | What it checks |
| ----- | ---- | -------------- |
| MCP bridge | `tests/Feature/Mcp/Agents/AgentBridgeToolsTest.php` | `run-support-agent` / `run-trading-agent` with faked agents |
| KB AI tools | `tests/Feature/Ai/KnowledgeBaseAiToolsTest.php` | KB search + get-by-slug with mocked repository |
| Tool inventory | `tests/Feature/Ai/Agents/AiAgentToolsInventoryTest.php` | Exact tool `name()` sets per agent × auth × `APP_VERSION` |
| Handle smokes | `tests/Feature/Ai/AiToolsHandleSmokeTest.php` | Each non-KB tool `handle()` with mocked `OhlcxMainApi` / `InternalApiService` |
| Prompts | `tests/Feature/Ai/AgentPromptsLoadTest.php` | Prompt files exist; instructions load and contain expected content |
| HTTP endpoints | `tests/Feature/Ai/Agents/AgentEndpointsTest.php`, `UnifiedAgentEndpointsTest.php` | JSON + SSE; tool class gating |

Run all AI feature tests:

```bash
php artisan test tests/Feature/Ai
```
