# strategies

**Composer:** `ohlcx/strategies` · **Repository:** [github.com/ohlcx/strategies](https://github.com/ohlcx/strategies) (private) · **Edition:** Pro

## Role

The strategies center and automated trading system: strategies and their conditions, condition evaluation on price bars, signals, simulated and live trades, backtests, the screener, and the routing of a strategy's orders to the owner's linked brokerage accounts.

## What it provides

- Strategy create, read, update and delete, with settings for risk, allocation, sizing, exit flow, schedule and notifications
- Deploy and retain. The engine evaluates only deployed strategies
- Signals, with a user's marks on them (like, watch, ignore), and trades
- Backtests: saved runs, and server-side runs and parameter sweeps
- Screener API: gaps across a market, gaps in one symbol's history, technical readings per market
- Broadcast events when a strategy or a condition is evaluated and when a flag, a signal or a trade is created

## Order routing

A strategy sends its orders to brokerage accounts its owner has linked. There are no portfolios: the earlier portfolio tables were removed in 1.5.0 and their routes carried over to the strategy's own accounts.

- A strategy's order accounts are either a selected list or all linked accounts that can receive orders.
- Setting accounts never switches orders on.
- Switching orders on makes a strategy real and needs an account an order could reach. Making a strategy demo switches its orders off.
- A deployed strategy is locked: it refuses changes until it is retained. Switching things off always works.
- An account that had an order refused is set aside until the strategy's accounts are saved again.
- Alpaca accounts cannot receive strategy orders yet.

The rules, the sequence of calls and every refusal are described on [Strategies and order routing](../mcp/strategy-routing.md).

## Commands

| Command | Purpose |
|---------|---------|
| `strategies:routing-backfill` | Dry run: reports where each strategy routes today and what the move to linked accounts would do. Changes nothing. `--json` prints the report as JSON |
| `strategies:seed` | Seeds the package's data |

## Requires

`pricefeed` (price bars), `schwab-integration` (linked accounts and buying power), `tdameritrade-laravel`, `alpaca-trade-api-php`, `mail-kit`. It needs a queue worker for evaluation, chart and order jobs.

## Light edition

OHLCX Light does not install this package. Its strategy screens and MCP tools are relayed to the hosted OHLCX API by trading-app.

## Related

- [Strategies and order routing](../mcp/strategy-routing.md)
- [MCP tool reference](../mcp/tools/reference.md#strategies-reading)
- [API reference](../api/reference.md)
