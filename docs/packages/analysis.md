# analysis

**Composer:** `ohlcx/analysis` · **Repository:** [github.com/ohlcx/analysis](https://github.com/ohlcx/analysis) (private) · **Edition:** Pro

## Role

Scheduled ticker analysis snapshots with chart images (rendered by the `chart-render` service through `ohlcx/chart-images`, or by the Highcharts export server until it is retired), and a read API for them: `/api/analysis` and `/api/tickers/{symbol}/analysis`.

Snapshots are created on weekdays at preset times (by default 09:31, 13:01 and 16:01).

## Commands

| Command | Purpose |
|---------|---------|
| `ticker:createAnalysisSnapshot` | Creates a snapshot of ticker analysis for active tickers |
| `analysis:prune-charts` | Deletes chart images older than the keep window (nightly) |
| `analysis:seed` | Seeds demo data |

## Dependencies

It requires **chart-images** (the chart-render client). It works with **pricefeed** tickers and **strategies** when the application installs them.

## Related

MCP tool: `get-ticker-analysis` lists the published analysis for one symbol. See [Markets and price data](../mcp/tools/reference.md#markets-and-price-data).
