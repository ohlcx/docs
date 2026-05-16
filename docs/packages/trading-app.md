# trading-app

**Composer:** `ohlcx/trading-app` · **Repository:** [github.com/ohlcx/trading-app](https://github.com/ohlcx/trading-app) (private)

## Role

Central trading platform package: React SPA assets, Laravel routes, auth and support flows, knowledge base API, **in-app AI agents**, and the **OHLCX MCP server**.

## Capabilities

- Trading UI at `/trading` (orders, positions, dashboard, strategies UI shell)
- Social login routes (optional)
- Activity log, onboarding, preferences, settings
- `trading-app:install` — copies docs, frontend, prompts into host apps
- AI: `POST /api/ai/agents/*` (Support, Trading, Assistant)
- MCP: `/mcp/ohlcx` and `php artisan mcp:start ohlcx`

## Documentation source

Public docs are synced from this package’s `docs/` directory. Maintainers run `scripts/sync-public-docs.sh`.

## Related

- [AI overview](../ai/overview.md)
- [MCP overview](../mcp/overview.md)
- [trading-app install](../setup/trading-app-install.md)
