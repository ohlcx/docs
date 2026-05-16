# trading-app install

The **`ohlcx/trading-app`** package is the core trading UI, API routes, AI/MCP, and shared documentation source. Host apps run:

```bash
php artisan trading-app:install [--force] [--pro]
```

## What install does

- Copies package **views**, **React assets**, **prompts**, and **docs** into the host app (when `--force` or paths missing)
- Ensures host **`routes/ai.php`** stub loads package MCP routes
- Installs **`config/trading-app.php`** when missing
- Patches **`bootstrap/app.php`** for CSRF exemption on `api/ai/agents/*` (SSE)
- **Pro (`--pro`):** additional config such as Horizon

## Host `routes/ai.php` stub

Laravel MCP loads only `base_path('routes/ai.php')`. Keep a thin stub:

```php
<?php

require __DIR__.'/../vendor/ohlcx/trading-app/routes/ai.php';
```

## Seed knowledge base

```bash
php artisan trading-app:seed
```

## Configuration: AI data source

In `config/trading-app.php`:

| Value | Behavior |
|-------|----------|
| `auto` | `pro` → local package routes; otherwise remote |
| `remote` | Hosted OHLCX API with `OHLCX_API_TOKEN` |
| `local` | Same-app `/api/*` via internal service |

## Related commands

| Command | Purpose |
|---------|---------|
| `trading-app:seed` | Knowledge base seed |
| `mcp:start ohlcx` | Stdio MCP server for Cursor |
| `stripe-credits-billing:seed` | Billing packages (host) |
| `trading-rooms:seed` | Chat seed data (Light) |

## After package updates

Re-run when pulling trading-app changes that affect routes, docs, or frontend:

```bash
php artisan trading-app:install --force
# Pro hosts:
php artisan trading-app:install --force --pro
```

See [AI overview](../ai/overview.md) for MCP and agent details.
