# AI and MCP (shared package)

This package is the single source of truth for AI/MCP in both `ohlcx-light` and `ohlcx`.

- Code (private package): `vendor/ohlcx/trading-app/src/Ai`, `src/Mcp`, `src/Services`, `src/Contracts`
- Routes: package `routes/ai.php` (MCP), `routes/ai-agents.php` (HTTP agents API)
- Agent HTTP routes are loaded by `packages/ohlcx/trading-app/routes/api.php` via `require __DIR__.'/ai-agents.php'`. Hosts do **not** need to include `ai-agents.php` in their own `routes/api.php` once the package API routes are registered (as with `RouteServiceProvider` / `TradingAppServiceProvider`).

## Host app wiring

Host apps must keep a local `routes/ai.php` because Laravel MCP only loads `base_path('routes/ai.php')`. Use a thin stub:

```php
<?php

require __DIR__.'/../vendor/ohlcx/trading-app/routes/ai.php';
```

Remove any legacy block in host `routes/api.php` that included `vendor/.../ai-agents.php` or workspace fallback — `trading-app:install` strips common patterns.

## Data source mode

`config/trading-app.php`:

- `ai.domain_data_source = auto|remote|local`
- `auto` resolves by `APP_VERSION` (`pro` → local, otherwise remote).

`remote` uses an authorized `OHLCX_API_TOKEN` against the **hosted OHLCX API** (provided by maintainers for Light deployments—not via this public docs site).

`local` uses `InternalApiService` against this app `/api/*` with current auth.

## Light vs Pro behavior

- `APP_VERSION=light`: keep remote proxy routes (`routes/remote.php`) active where applicable.
- `APP_VERSION=pro`: disable remote proxy routes, use local package/domain routes.
- If local domain packages are not installed in light, force `ai.domain_data_source=remote`.

## Install/update

```bash
php artisan trading-app:install --force
```

This copies prompts/docs/assets as configured, ensures `routes/ai.php` stub, removes legacy agent-route includes from host `routes/api.php`, installs `config/trading-app.php` when missing, and patches `bootstrap/app.php` to add the CSRF exemption `api/ai/agents/*` (required for SSE from the SPA). Re-run after pulling if you reset `bootstrap/app.php` to stock Laravel.

Optional pro overlays:

```bash
php artisan trading-app:install --force --pro
```
