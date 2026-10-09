# Limits and paging

The list tools whose answers can grow large return a bounded number of rows per call and say how to ask for more. There are three ways of paging, plus a few fixed caps. This page lists which tool uses which. A list tool that is not on this page takes no paging arguments and returns what OHLCX holds.

All numbers on this page are the server's own. Argument names, types and defaults are in the [tool reference](tools/reference.md).

## Page number

The tool returns one page and takes `page` (default 1) for the next. The page size is fixed.

| Tool | Rows per page |
|------|---------------|
| `list-strategy-signals` | 100 |
| `list-strategy-trades` | 100 |
| `get-strategy-flags` | 100 |
| `list-trades` | 100 |
| `get-ticker-analysis` | 10 |
| `list-backtests` | Set by the server |
| `list-backtest-jobs` | Set by the server |

Ask for `page` 2, 3 and so on until a page comes back empty or short.

## Page number and page size

The tool takes `page` and `per_page`.

| Tool | `per_page` | Default |
|------|-----------|---------|
| `list-strategies` | 1 to 50 | See below |
| `list-account-cash-transfers` | up to 50 | 25 |
| `list-credit-holds` | up to 50 | 25 |
| `screen-technicals` | up to 50 | 20 |
| `list-users` (admin) | up to 100 | 20 |
| `list-news`, `list-crypto-news`, `list-popular-news` | Set by the server | Set by the server |
| `list-sectors` | `per_page` only, no `page` | Set by the server |

### `list-strategies`

`list-strategies` has two forms.

Without arguments it returns the plain list, up to 50 strategies:

```json
{ "strategies": [ { "id": 7, "name": "SPY breakout", "symbol": "SPY" } ] }
```

With `page`, `per_page` or both it returns that page of the paged list, with the paging figures under `meta`:

```json
{
  "strategies": [ { "id": 7, "name": "SPY breakout", "symbol": "SPY" } ],
  "meta": { "current_page": 1, "last_page": 3, "per_page": 25, "total": 61 }
}
```

Read on until `current_page` equals `last_page`. A user with more than 50 strategies must use the paged form to see them all.

`meta` is absent on an installation whose API does not page yet. There, `page` counts in pages of 50 and `per_page` is ignored.

## Cursor

`get-ticker-bars` is the one cursor-paged tool.

| Argument | Rule |
|----------|------|
| `limit` | Bars to return, up to 1000 (default 200) |
| `order` | `desc` for newest first (default), `asc` for oldest first |
| `from`, `to` | Narrow the range. A date, or a date and time, in UTC |
| `cursor` | `meta.next_cursor` from the previous call |

With no `limit`, `from`, `to` or `order`, the tool returns the most recent 200 bars. To continue, send the same arguments again with `cursor` set to the `meta.next_cursor` of the answer you have. Stop when the answer carries no `meta.next_cursor`.

## A cap instead of pages

These tools return at most a set number of rows and have no next page. Narrow the request to see other rows.

| Tool | Cap | How to narrow |
|------|-----|---------------|
| `list-orders` | `max_results` up to 500 (default 100) | A shorter range between `start_date` and `end_date`, an `account_id`, a `status` |
| `get-accounts-balances` | `days` up to 365 per account (default 30) | Fewer `days` |
| `get-strategy-timeline` | `days` back (default 7) | Fewer `days` |
| `list-strategy-accounts` | 50 accounts. `more` says how many were left out | No narrowing |
| `set-strategy-accounts` | At most 50 ids in `account_ids`. The `routing` in the answer shows at most 50 accounts, and `more` says how many were left out | Use mode `all` for a user with more accounts |
| `get-backtest` | The trade list, equity curve and strategy snapshot are left out unless named in `include`. `omitted` lists what was left out | Name only the parts you need |

## Period filters

The statistics, performance and trade tools return figures for one period. They do not page: choose the period.

| Tools | `period` | Default | Other filters |
|-------|----------|---------|---------------|
| `get-strategy-statistics`, `get-strategies-statistics`, `get-strategy-performance`, `get-strategies-performance` | `TODAY`, `YESTERDAY`, `THISWEEK`, `LASTWEEK`, `THISMONTH`, `LASTMONTH`, `THISYEAR`, `LASTYEAR` | `THISMONTH` | `status`: `ALL`, `OPEN`, `CLOSED` (default `ALL`). `direction`: `BOTH`, `LONG`, `SHORT` (default `BOTH`) |
| `list-trades` | The same eight values | `THISMONTH` | `symbol`. `status`: `ALL`, `OPEN`, `CLOSED`. `direction`: `ALL`, `BUY`, `SELL`. Also paged, 100 per page |
| `get-account-pnl-history` | `week`, `month`, `quarter`, `year`, `this_week`, `this_month`, `this_quarter`, `ytd`, `last_year` | `month` | `from` and `to` (`YYYY-MM-DD`) replace `period` |
| `get-account-pnl-symbols`, `list-account-cash-transfers` | The same nine values | `ytd` | `from` and `to` replace `period`. `symbol`, `underlying` (P&L by symbol). `direction`, `q` (cash transfers) |
| `get-ai-usage` | `range`: a number of days such as `7d`, `30d` or `90d`, or `all` | `all` | `from` and `to` |

## Other limits

| Tool | Limit |
|------|-------|
| `run-backtest`, `run-backtest-sweep` | At most three backtests may wait or run at once. A period may cover at most five years. A sweep varies one or two settings |
| `save-workspaces` | Up to 10 workspaces of up to 12 blocks each |
| `create-watchlist`, `rename-watchlist` | A name of up to 30 characters |
| `rename-backtest` | A name of up to 120 characters |
| `create-support-ticket` | A subject of up to 255 characters, a category of up to 100 |
| `run-support-agent`, `run-trading-agent` | A message of up to 16,000 characters |
| `set-strategy-schedule` | Days as numbers 1 to 7, times as `HH:MM` in New York time |

## How fresh a list is

Three list tools may return an answer that is up to one minute old: `list-strategies`, `list-signals` and `list-conditions`. Each user has their own copy.

A change made through this server shows at once: every tool that changes a strategy, including `deploy-strategy`, `retain-strategy` and `set-strategy-accounts`, refreshes the strategy list, and the tools that write a condition or delete a signal refresh theirs. A change made in the OHLCX app can take up to a minute to appear in these three lists.

The account lists are never kept: `list-accounts` and `list-strategy-accounts` are read fresh on every call.
