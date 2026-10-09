# trading-app

**Composer:** `ohlcx/trading-app` · **Repository:** [github.com/ohlcx/trading-app](https://github.com/ohlcx/trading-app) (private) · **Edition:** Pro, Light

## Role

The application layer of OHLCX, shared by both editions: the React trading UI, the Laravel routes behind it, sign-in and support flows, the knowledge base, the **in-app assistant**, and the **OHLCX MCP server**.

## Capabilities

- Trading UI at `/trading` (orders, positions, dashboard, strategies, Workspaces, watchlists)
- API for sign-in, activities, onboarding, preferences, settings, watchlists, Workspaces, credit holds, the knowledge base and support tickets
- Social login routes (optional)
- In-app assistant: `POST /api/ai/agents/*` (Support, Trading, Assistant). See [AI overview](../ai/overview.md)
- MCP server: `/mcp/ohlcx` and `php artisan mcp:start ohlcx`, with 147 tools, 3 prompts and 1 resource. See [MCP overview](../mcp/overview.md)

## Light and Pro

On **Pro**, strategies, markets, sectors, news and analysis are served by the Pro-only packages installed beside trading-app. On **Light**, trading-app relays those requests to the hosted OHLCX API. The two MCP tools for a strategy's order accounts exist only on Pro. See [Light vs Pro](../architecture/light-vs-pro.md).

## Requires

`node-license-client`, `tdameritrade-laravel`, `schwab-integration`, `stripe-credits-billing`, `user-profile`, `trading-rooms`, `goals`, `mail-kit`. Optional: `booking`, `referrals`, `pulse`.

## Host setup

```bash
php artisan trading-app:install
php artisan trading-app:seed
```

`trading-app:install` copies the package's frontend, public assets and documents into the host application. `trading-app:seed` seeds the knowledge base. See [trading-app install](../setup/trading-app-install.md).

## Documentation source

The AI, API and architecture pages of this site are synced from this package's `docs/` directory, and the MCP tool list from its tool index. Maintainers run `scripts/sync-public-docs.sh`.

## Related

- [AI overview](../ai/overview.md)
- [MCP overview](../mcp/overview.md)
- [API reference](../api/reference.md)
