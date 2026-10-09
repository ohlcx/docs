# goals

**Composer:** `ohlcx/goals` · **Repository:** [github.com/ohlcx/goals](https://github.com/ohlcx/goals) (private) · **Edition:** Pro, Light · **Version:** 1.0.11

## Role

Realized profit and loss goals per linked brokerage account. A user sets a target amount, a target percent, or both, for each cadence (daily, weekly, monthly). A calendar then shows every period as hit, missed, in progress, upcoming, or without a target.

The package does not compute or store profit and loss. It reads the daily realized P&L that **schwab-integration** keeps, and works progress out when it is asked.

## What it provides

- **Targets with history.** Editing a target adds a new version instead of changing the old one, so past periods stay judged against the target that applied at the time.
- **Progress by period**, computed on read for every period in the requested range, including periods without trades.
- **API** under `/api/goals` for a signed-in user: an account's targets and its progress. Under `/api/goals/admin` an admin lists every user's current targets.
- **Recorded moments** for a period, such as when a goal was first reached. They are rebuilt after a profit and loss sync finishes.
- The trading UI's Goals page and the admin goals page, which are part of trading-app, use this API.

## Commands

| Command | Purpose |
|---------|---------|
| `goals:seed-demo` | Seeds a demo account, trading history and targets for local testing |
| `goals:set-day-pnl` | Sets one day's realized P&L, to test a goal under or over its target |

## Configuration

`GOALS_WEEK_START_DAY`: the day a week starts on.

## Dependencies

It requires no other OHLCX package in `composer.json`. At run time it needs **schwab-integration** for accounts and profit and loss: without it the endpoints answer that the dependency is missing. **trading-app** requires this package.

## Related

- [schwab-integration](schwab-integration.md)
- No MCP tool reads goals. An MCP client can read the underlying profit and loss with `get-account-pnl-history`. See [Accounts](../mcp/tools/reference.md#accounts).
