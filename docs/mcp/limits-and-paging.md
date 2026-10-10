# Limits and paging

Every tool that returns a list is bounded: it returns a set number of rows per call and says how to read on. On top of that, every answer is at most 256 KB. This page explains the three ways of reading on, gives each tool's bounds in one table, and shows how a client pages safely.

All numbers on this page are the server's own, read from the tools' schemas, which declare `minimum`, `maximum` and `default` for every bound.

## The three patterns

### Pages: `page`, with `meta`

The tool returns one page and takes `page` (1 to 100000, default 1) for the next. The answer carries `meta`:

```json
{
  "strategies": [ { "id": 7, "name": "SPY breakout", "symbol": "SPY" } ],
  "meta": { "current_page": 1, "last_page": 3, "per_page": 25, "total": 61, "has_more": true }
}
```

| Field of `meta` | Meaning |
|-----------------|---------|
| `current_page`, `per_page` | The page that came and its length |
| `has_more` | Whether another page follows. Always present |
| `last_page`, `total` | Present only when the API gives them |

Read on while `has_more` is true. Where the API gives no total, `has_more` is true whenever the page came back full, so the last full page is followed by one empty page: an empty page is the end, not an error.

Some of these tools take `per_page`, so you can ask for shorter pages. The others have a fixed page length.

### Limit: `limit`, with `more`

A tool whose API does not page takes `limit`. When rows were left out, `more` says how many:

```json
{ "watchlists": [ { "id": 3, "name": "Tech" } ], "more": 12, "next_offset": 50 }
```

Most of these tools also take `offset`: ask again with `offset` set to `next_offset` to read the rows that were left out. `next_offset` is present only while rows remain.

A few tools take `limit` without `offset`. Their API stops at a fixed number of rows, so `limit` can only ask for fewer, and older rows cannot be read through that tool. The table says which.

### Offset within a page: `offset`, with `next_offset`

A tool with a fixed page length cannot be asked for a shorter page. When the size budget cuts such a page, the rows left out would be lost. So these tools take `offset`: the answer carries `truncated`, `more` and `next_offset`, and asking for the same `page` with `offset` set to `next_offset` returns the rest of that page.

## The size budget

Every answer is at most 256 KB of JSON.

| Field | Meaning |
|-------|---------|
| `truncated` | `true` when rows were dropped to fit the budget |
| `more` | How many rows were left out, by `limit` or by the budget |
| `next_offset` | Where to read on, on the tools that take `offset` |
| `row_too_large` | `true` when a single row is too large for any answer. It is stepped over, and `next_offset` points past it, so a client following `next_offset` never asks for the same rows twice. Read that one item with its own tool, for example `get-strategy` |

Rows are dropped from the end of a list. A series that comes oldest first (balance history, growth, profit and loss by day) loses its oldest rows instead, so the most recent days are kept.

An answer with no rows to drop is refused: "The result is too large to return. Ask for fewer rows or a narrower range." See [Errors and refusals](errors.md#too-large).

Nothing was renamed to make room for this: `meta`, `more`, `truncated` and `next_offset` sit beside what a tool already answered.

## Each tool's bounds

| Tool | Pattern | Rows | Arguments |
|------|---------|------|-----------|
| `list-users` | Pages | 1 to 100 per page (default 20) | `page`; `per_page` |
| `search-knowledge-base` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000 |
| `list-accounts` | Limit, no pages | 1 to 100 (default 100) | `limit` |
| `get-account-balance` | Limit, no pages | 1 to 360 (default 360) | `limit` |
| `get-account-growth` | Limit, no pages | 1 to 120 (default 120) | `limit` |
| `get-account-pnl` | Limit, no pages | 1 to 120 (default 120) | `limit` |
| `get-accounts-balances` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000; `days` 1 to 365 (default 30) |
| `get-account-pnl-history` | Limit, no pages | 1 to 1000 (default 366) | `limit` |
| `get-account-pnl-symbols` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000; `round_trips_limit` 1 to 200 (default 50) |
| `list-account-cash-transfers` | Pages | 1 to 50 per page (default 25) | `page`; `per_page` |
| `list-orders` | Cap, no pages | 1 to 500 (default 100) | `max_results` |
| `list-activities` | Pages | 1 to 50 per page (default 30) | `page`; `per_page` |
| `get-analysis` | Pages | 1 to 50 per page (default 10) | `page`; `per_page` |
| `list-strategies` | Pages | 1 to 50 per page (default 50) | `page`; `per_page` |
| `search-strategies` | Pages of fixed length | 30 per page | `page`; `offset` 0 to 29 |
| `get-strategy-activities` | Limit, no pages | 1 to 10 (default 10) | `limit` |
| `get-strategy-conditions` | Pages of fixed length | 100 per page | `page`; `offset` 0 to 99 |
| `get-strategy-timeline` | Days | 1 to 365 (default 3) | `days` |
| `list-strategy-signals` | Pages of fixed length | 100 per page | `page`; `offset` 0 to 99 |
| `list-strategy-trades` | Pages of fixed length | 100 per page | `page`; `offset` 0 to 99 |
| `get-strategy-flags` | Pages of fixed length | 100 per page | `page`; `offset` 0 to 99 |
| `list-signals` | Pages of fixed length | 100 per page | `page`; `offset` 0 to 99 |
| `list-backtests` | Pages of fixed length | 25 per page | `page`; `offset` 0 to 24 |
| `list-backtest-jobs` | Pages of fixed length | 25 per page | `page`; `offset` 0 to 24 |
| `list-trades` | Pages of fixed length | 100 per page | `page`; `offset` 0 to 99 |
| `list-watchlists` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000 |
| `list-markets` | Pages of fixed length | 10 per page | `page`; `offset` 0 to 9 |
| `list-sectors` | Pages | 1 to 100 per page (default 10) | `page`; `per_page` |
| `get-ticker` | Pages of fixed length | 1000 per page | `page`; `offset` 0 to 999 |
| `screen-market-gaps` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000 |
| `screen-asset-gaps` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000 |
| `screen-technicals` | Pages | 1 to 50 per page (default 20) | `page`; `per_page` |
| `get-ticker-bars` | Cursor | 1 to 1000 (default 200) | `limit` |
| `get-ticker-analysis` | Pages of fixed length | 10 per page | `page`; `offset` 0 to 9 |
| `list-news` | Pages | 1 to 50 per page (default 10) | `page`; `per_page` |
| `list-crypto-news` | Pages | 1 to 50 per page (default 10) | `page`; `per_page` |
| `list-popular-news` | Pages | 1 to 50 per page (default 10) | `page`; `per_page` |
| `list-conditions` | Pages of fixed length | 100 per page | `page`; `offset` 0 to 99 |
| `list-support-tickets` | Pages of fixed length | 20 per page | `page`; `offset` 0 to 19 |
| `get-transaction-history` | Limit, no pages | 1 to 100 (default 100) | `limit` |
| `list-credit-holds` | Pages | 1 to 50 per page (default 25) | `page`; `per_page` |
| `get-sessions` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000 |
| `discover-groups` | Pages of fixed length | 10 per page | `page`; `offset` 0 to 9 |
| `browse-users` | Pages of fixed length | 20 per page | `page`; `offset` 0 to 19 |
| `list-invites` | Pages | 1 to 50 per page (default 10) | `page`; `per_page` |
| `list-pending-join-requests` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000 |
| `get-sidebar-conversations` | Limit and offset | 1 to 200 (default 50) | `limit`; `offset` 0 to 100000 |
| `get-unread-messages` | Limit, no pages | 1 to 50 (default 50) | `limit` |

A bound that is not met is refused before anything is asked, for example `limit must be a whole number from 1 to 200.`

`get-older-messages` has no page number: it returns the 10 messages before a given message, with `meta.has_more`. Ask again with the oldest message's id.

## What cannot be read further

Some APIs stop at a fixed number of rows. The tool's description says so, and `limit` only asks for fewer.

| Tool | The API gives | To read more |
|------|---------------|--------------|
| `list-accounts` | 100 accounts, the most recently linked first | Not through this tool |
| `get-account-balance` | 360 rows | Not through this tool |
| `get-account-growth`, `get-account-pnl` | The 120 most recent balance rows | Not through this tool |
| `get-strategy-activities` | The latest 10, with `total_activities` | Not through this tool |
| `get-transaction-history` | The latest 100 transactions and the latest 100 used features | Not through this tool |
| `get-unread-messages` | The latest 50 unread messages | Not through this tool |
| `get-strategy` | The latest 100 of each of its conditions, flags, signals and trades | `get-strategy-conditions`, `get-strategy-flags`, `list-strategy-signals`, `list-strategy-trades` |
| `list-strategies` without arguments | The first 50, with nothing to say whether there are more | Ask with `page` |
| `list-orders` | Up to 500 orders, no pages | Narrow `start_date` and `end_date` |
| `get-account-pnl-history` | Up to 1000 days at a time, the most recent first to be kept | Narrow `from` and `to` |
| `get-backtest` | Rows the size budget cut from the trade list or the equity curve | Not through this tool. The whole run is in the app |
| `get-support-ticket` | The newest messages of a conversation over the size budget; `more` counts the older ones | In the app |

## Tools with their own rules

### `get-strategy-timeline`

The timeline is a grid: for each day, newest first, a cell for every minute. It is large, so one answer holds the most recent whole days that fit, about three.

- `days` is 1 to 365 and defaults to 3.
- `returned` says which days came (`days`, `from`, `to`). `more` says how many older days that were asked for were left out.
- The timeline always ends today: there is no way to start further back.
- To read older days, set `logged_only` to `true`. It leaves out the minutes in which nothing was logged, so that a year of days usually fits.
- A single day too busy to fit comes with its latest logged minutes only; `more_minutes` counts the rest.

### `get-account-pnl-symbols`

- `symbols` come largest move first, winners and losers alike. At most 50 unless `limit` says otherwise; `more` and `next_offset` read on.
- `round_trips` come most recent first. At most 50 unless `round_trips_limit` (1 to 200) says otherwise; `more_round_trips` counts the older ones left out. To read those, narrow the dates or name a symbol.

### `get-ticker-bars`

The one cursor-paged tool. It returns the most recent 200 bars unless `limit` (1 to 1000), `from`, `to` or `order` say otherwise. To continue, send the same arguments with `cursor` set to the `meta.next_cursor` of the answer you have, until there is none.

When the size budget cuts the bars, `truncated` is set and `meta.next_cursor` is null: ask again with a smaller `limit`.

### `get-ticker` without a symbol

It lists tickers 1000 per page. A page of 1000 is usually over the size budget, so expect `truncated` and follow `next_offset` within the page before you go to the next `page`.

### `list-strategies`

Without arguments it returns the first 50 as a plain list, with no `meta`. With `page` or `per_page` (1 to 50) it returns the paged list with `meta`. On an installation whose API does not page yet, `meta` is absent, `page` counts in pages of 50 and `per_page` is ignored.

## Period filters

The statistics, performance and trade tools return figures for one period.

| Tools | `period` | Default | Other filters |
|-------|----------|---------|---------------|
| `get-strategy-statistics`, `get-strategies-statistics`, `get-strategy-performance`, `get-strategies-performance` | `TODAY`, `YESTERDAY`, `THISWEEK`, `LASTWEEK`, `THISMONTH`, `LASTMONTH`, `THISYEAR`, `LASTYEAR` | `THISMONTH` | `status`: `ALL`, `OPEN`, `CLOSED`. `direction`: `BOTH`, `LONG`, `SHORT` |
| `list-trades` | The same eight values | `THISMONTH` | `symbol`. `status`: `ALL`, `OPEN`, `CLOSED`. `direction`: `ALL`, `BUY`, `SELL` |
| `get-account-pnl-history` | `week`, `month`, `quarter`, `year`, `this_week`, `this_month`, `this_quarter`, `ytd`, `last_year` | `month` | `from` and `to` (`YYYY-MM-DD`) replace `period` |
| `get-account-pnl-symbols`, `list-account-cash-transfers` | The same nine values | `ytd` | `from` and `to` replace `period`. `symbol`, `underlying` (P&L by symbol). `direction`, `q` (cash transfers) |
| `get-ai-usage` | `range`: a number of days such as `7d`, `30d` or `90d`, or `all` | `all` | `from` and `to` |

## Paging safely

A loop that reads every row of a list, whichever pattern the tool uses:

1. Call the tool with its defaults, or with `page` 1.
2. Keep the rows that came.
3. If the answer has `next_offset`, call again with the same arguments and `offset` set to it. Repeat until an answer has no `next_offset`. If an answer says `row_too_large`, note that one row was skipped.
4. If the answer has `meta.has_more` true, add 1 to `page`, set `offset` back to 0, and go to step 2.
5. Stop when there is no `next_offset` and `has_more` is false or absent. An empty page also ends the loop.

Rules that keep the loop safe:

- Never guess a next page from the number of rows: use `has_more` and `next_offset`.
- Set a ceiling on the number of calls. `page` goes up to 100000.
- If `more` is set and there is no `next_offset`, the rest cannot be read through this call: narrow the request (a shorter period, a named symbol or account) or read the item itself.
- A list can change between calls. Do not treat a row seen twice, or missed, as an error.

## Other limits

| Tool | Limit |
|------|-------|
| `set-strategy-accounts` | At most 50 ids in `account_ids`. A `routing` block shows at most 50 accounts, with `more` |
| `run-backtest`, `run-backtest-sweep` | At most three backtests may wait or run at once. A period may cover at most five years. A sweep varies one or two settings |
| `save-workspaces` | Up to 10 workspaces of up to 12 blocks each |
| `create-watchlist`, `rename-watchlist` | A name of up to 30 characters |
| `rename-backtest` | A name of up to 120 characters |
| `create-support-ticket` | A subject of up to 255 characters, a category of up to 100 |
| `run-support-agent`, `run-trading-agent` | A message of up to 16,000 characters |
| `set-strategy-schedule` | Days as numbers 1 to 7, times as `HH:MM` in New York time |

## The tool list itself is paged

An MCP client that lists the server's tools receives them in pages of 15 (at most 50) and must follow `nextCursor` to see all 147. Claude and Cursor do this themselves. See [Agents setup](agents-setup.md#any-other-mcp-client).

## How fresh a list is

Three list tools may return an answer that is up to one minute old: `list-strategies`, `list-signals` and `list-conditions`. Each user has their own copy, and each page is kept apart.

A change made through this server shows at once: every tool that changes a strategy, a condition or deletes a signal refreshes the lists. A change made in the OHLCX app can take up to a minute to appear in these three lists.

The account lists are never kept: `list-accounts` and `list-strategy-accounts` are read fresh on every call.
