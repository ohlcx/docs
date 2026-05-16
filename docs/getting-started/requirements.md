# Requirements

## Runtime

| Component | Version / notes |
|-----------|-----------------|
| PHP | ^8.2 |
| Composer | 2.x |
| Node.js & npm | For Vite frontend builds |
| MySQL or MariaDB | Application database |
| Redis | Horizon queues and caching |
| Laravel Reverb | WebSocket broadcasting |

## Optional (recommended for development)

| Tool | Purpose |
|------|---------|
| Laravel Horizon | Queue monitoring (`php artisan horizon`) |
| Laravel Dusk | Browser E2E tests (Light README) |
| Laravel Boost | Framework MCP for Cursor |
| GitHub personal access token | Composer VCS access to private `ohlcx/*` repos |

## Broker and data providers

Local development typically requires **your own** Schwab developer credentials (or sandbox) and any Alpaca keys if you enable pricefeed/news packages in Pro.

OHLCX does **not** distribute production API tokens for the hosted OHLCX API through this documentation site.

## IDE

- **Cursor** (recommended) with OHLCX MCP + Laravel Boost — see [Cursor and Boost](../ai/cursor-and-boost.md)
- Any editor with PHP and JavaScript tooling

## Host OS

macOS and Linux are commonly used. Windows may require WSL for some scripts and Dusk.
