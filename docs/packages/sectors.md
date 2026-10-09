# sectors

**Composer:** `ohlcx/sectors` · **Repository:** [github.com/ohlcx/sectors](https://github.com/ohlcx/sectors) (private) · **Edition:** Pro

## Role

Sector definitions, the tickers of each sector, sector balance snapshots, Livewire charts, and a REST API for sector data (`/api/sectors`, `/api/sector-balance`).

## Commands

| Command | Purpose |
|---------|---------|
| `sectors:seed` | Seeds sectors and their tickers |
| `sector:storeBalance` | Calculates and stores a sector's balance snapshot. `--all` does every active sector |

It works with **pricefeed** tickers when the application installs that package.

## Light edition

**ohlcx-light** does not install this package. Sector routes are relayed to the **hosted OHLCX API**. See [Light vs Pro](../architecture/light-vs-pro.md).

## Related

MCP tools: `list-sectors`, `get-sector`, `get-sector-balance`. See [Markets and price data](../mcp/tools/reference.md#markets-and-price-data).
