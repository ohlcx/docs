# news

**Composer:** `ohlcx/news` · **Repository:** [github.com/ohlcx/news](https://github.com/ohlcx/news) (private) · **Edition:** Pro

## Role

Featured news and articles. News for a market's tickers is fetched on a schedule (`market:tickerNews`, every 15 minutes) through the Alpaca API, for the tickers **pricefeed** holds.

## Commands

| Command | Purpose |
|---------|---------|
| `market:tickerNews` | Fetches news for a market's tickers |
| `ticker:news` | Fetches news for one symbol |
| `news:seed` | Seeds demo data |

## API

News list and detail, news for one ticker, popular news and crypto news. MCP tools: `list-news`, `get-news`, `list-crypto-news`, `list-popular-news`. See [News](../mcp/tools/reference.md#news).
