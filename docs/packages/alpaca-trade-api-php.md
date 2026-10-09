# alpaca-trade-api-php

**Composer:** `ohlcx/alpaca-trade-api-php` · **Repository:** [github.com/ohlcx/alpaca-trade-api-php](https://github.com/ohlcx/alpaca-trade-api-php) (private) · **Edition:** Pro · **Version:** 1.0.15

## Role

A PHP SDK for the [Alpaca](https://alpaca.markets) API. It is a plain library: no routes, no database, no configuration of its own. It is not an official Alpaca SDK.

## What the SDK covers

- Account, account configuration, account activities and portfolio history
- Orders (list, read, create, replace, cancel) and positions
- Assets, watchlists, the market calendar and clock
- Market data: bars, trades, quotes and snapshots, for one symbol or several
- News
- OAuth for acting on behalf of an Alpaca user

## Where OHLCX uses it

| Package | Use |
|---------|-----|
| **pricefeed** | Market data only: bars, snapshots, assets, the market calendar and clock |
| **news** | News for tickers |
| **strategies** | Requires the SDK, but Alpaca accounts cannot receive strategy orders yet: no Alpaca order is sent |
| **development-features** | Requires the SDK |

In OHLCX today, Alpaca is a source of market data and news. Orders go to Schwab accounts. See [Strategies and order routing](../mcp/strategy-routing.md).

## Dependencies

It requires no other OHLCX package.
