# pricefeed

**Composer:** `ohlcx/pricefeed` · **Repository:** [github.com/ohlcx/pricefeed](https://github.com/ohlcx/pricefeed) (private) · **Edition:** Pro

## Role

Market and ticker price data: OHLCV bars ingested through the Alpaca API, technical analysis (moving averages, pivot points, indicators, candlestick patterns), live price publishing over Redis, and read API endpoints for markets, tickers, price bars, the market calendar and market balance.

## Dependents

**strategies** requires it: conditions are evaluated on its price bars. **news**, **analysis** and **sectors** work with its tickers when it is installed.

## Host setup

```bash
php artisan pricefeed:seed
```

Technical analysis needs PHP's `trader` extension.

## Light edition

OHLCX Light does not install this package. Market data requests are relayed to the hosted OHLCX API.

## Related

MCP tools: `list-markets`, `get-ticker`, `get-ticker-bars`, `get-market-calendar`, `get-market-balance`. See [Markets and price data](../mcp/tools/reference.md#markets-and-price-data).
