# analysis

**Composer:** `ohlcx/analysis` · **Repository:** [github.com/ohlcx/analysis](https://github.com/ohlcx/analysis) (private) · **Edition:** Pro

## Role

Scheduled ticker analysis snapshots with chart images (Highcharts), and a read API for them: `/api/analysis` and `/api/tickers/{symbol}/analysis`.

Snapshots are created on weekdays at preset times (by default 09:31, 13:01 and 16:01).

## Commands

| Command | Purpose |
|---------|---------|
| `ticker:createAnalysisSnapshot` | Creates a snapshot of ticker analysis for active tickers |
| `analysis:seed` | Seeds demo data |

## Dependencies

It requires no other OHLCX package. It works with **pricefeed** tickers and **strategies** when the application installs them.

## Related

MCP tool: `get-ticker-analysis` lists the published analysis for one symbol. See [Markets and price data](../mcp/tools/reference.md#markets-and-price-data).
