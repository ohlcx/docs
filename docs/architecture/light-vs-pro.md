# Light vs Pro

| Aspect | Light (`ohlcx-light`) | Pro (`ohlcx`) |
|--------|----------------------|---------------|
| **APP_VERSION** | `light` | `pro` |
| **Domain packages** | Subset (trading-app, schwab, billing, rooms, profile) | Full set (+ strategies, sectors, pricefeed, news, analysis, …) |
| **Sectors** | Proxied to hosted OHLCX API | Local `ohlcx/sectors` package |
| **Strategies / signals** | Proxied or remote AI source | Local package routes |
| **AI `domain_data_source`** | Usually `remote` or `auto` → remote | `local` when packages installed |
| **remote.php proxy** | Active for missing domains | Disabled when local packages serve routes |
| **Cursor / Boost** | Rich `.cursor/` rules and skills in repo | MCP config; docs reference Light patterns |

## AI and MCP

Both editions share **`ohlcx/trading-app`** for:

- MCP server (`/mcp/ohlcx`, `mcp:start ohlcx`)
- In-app agents (`POST /api/ai/agents/*`)

**Pro** agents may expose extra market/sector tools when `APP_VERSION=pro` and frontend env align.

## Choosing an edition

- **Light:** faster setup, smaller footprint, depends on hosted API for some domain data.
- **Pro:** full control, local simulation/strategies/sectors, no upstream API dependency for core features.

## Configuration

`config/trading-app.php`:

```php
'ai' => [
    'domain_data_source' => env('AI_DOMAIN_DATA_SOURCE', 'auto'),
],
```

If Light runs without local domain packages, force `remote` for AI tools that need strategies/markets data.
