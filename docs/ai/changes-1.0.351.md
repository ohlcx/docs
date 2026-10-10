# What changed in 1.0.350 and 1.0.351

For whoever maintains a client of the OHLCX MCP server, of the in-app assistant, or of the Light relay. The first section lists what changes after 1.0.353; everything below it is in package version 1.0.351.

The MCP server went from 144 tools (1.0.349) to 145 (1.0.350) to 147 (1.0.351). The server version string is unchanged: `1.1.0`.

## After 1.0.353

Not released yet. Every MCP tool whose input or output changes for a client is listed here, one line each. No tool was added or removed: the server still has 147 tools.

### What every list tool now has

- **`page`** (1 to 100000) on every tool whose API pages, and **`per_page`** where the API reads one. The answer carries `meta`: `current_page`, `per_page` and `has_more`, with `last_page` and `total` when the API gives them. Where the API sends a bare page of rows, `has_more` is true when the page came back full.
- **`limit`** on every tool whose API does not page. `more` says how many rows were left out.
- **A size budget of 256 KB** for every answer. Rows are dropped from the end (the oldest rows of a series), `truncated` is set and `more` counts them. An answer with no rows to drop is refused with "The result is too large to return. Ask for fewer rows or a narrower range."
- **`offset`** where a caller cannot lower a page length. While rows were left out the answer carries `next_offset`: ask again with it to read on. A single row too large for any answer is stepped over and `row_too_large` says so.
- **Bounds in the schema.** `limit`, `page`, `per_page`, `offset`, `days`, `max_results` and `round_trips_limit` declare `minimum`, `maximum` and `default`. A value that is not a whole number in plain digits within them (also `true`, `"+2"`, `1.5`) is refused with "`<name>` must be a whole number from `<least>` to `<most>`." and nothing is asked.
- Nothing was renamed or moved. `meta`, `more`, `truncated` and `next_offset` are added beside what a tool already answered.

### A different shape

| Tool | Change |
| ---- | ------ |
| `get-account-growth` | Was a bare list. Now `{account_id, account, growth}`. |
| `get-account-pnl` | Was a bare list. Now `{account_id, account, pnl}`. |
| `get-sessions` | Was a bare list. Now `{sessions}`. An empty list used to be answered as a failure and is now `{sessions: []}`. |
| `get-sidebar-conversations` | Was a bare list. Now `{conversations}`. |
| `get-strategy-timeline` | Answers the most recent whole days that fit one answer (about three), with `returned` (`days`, `from`, `to`) and `more`. `days` is 1 to 365 and now defaults to 3 (was 7, which no longer fitted). New `logged_only` leaves out the minutes with no log, so that a year of days usually fits. A day too busy to fit comes with its latest logged minutes and `more_minutes`. |
| `get-account-pnl-symbols` | `symbols` come largest move first, winners and losers alike (was best first). `round_trips` are bounded: new `round_trips_limit` (1 to 200, default 50) and `more_round_trips`. |
| `get-strategy`, `list-strategies` | The `routing` block is given as the routing tools give it: `reason` is a sentence (was a code), `set_aside_reason` and unknown keys are gone, a label is always masked, at most 50 accounts with `more`. |
| `get-support-ticket` | A conversation over 256 KB keeps its newest messages; `more` counts the older ones left out. |

### Fewer rows by default (`limit` 1 to 200, default 50; `offset` to read on)

`search-knowledge-base`, `get-accounts-balances` (accounts), `get-account-pnl-symbols` (symbols), `list-watchlists` (the user's own lists), `screen-market-gaps`, `screen-asset-gaps`, `get-sessions`, `list-pending-join-requests`, `get-sidebar-conversations`.

`get-account-pnl-history`: the 366 most recent days by default (`limit` 1 to 1000); narrow `from` and `to` for older days.

### `limit` up to what the API itself gives

These got `limit` only to ask for fewer. The API stops where it always did, and the description now says so: `list-accounts` (100 accounts), `get-account-balance` (360 rows), `get-account-growth` and `get-account-pnl` (120 rows), `get-strategy-activities` (10), `get-transaction-history` (100 of each list), `get-unread-messages` (50).

### New `page`, and `offset` within a page

| Tool | Page length | New arguments |
| ---- | ----------- | ------------- |
| `list-signals`, `list-conditions`, `get-strategy-conditions` | 100 | `page`, `offset` |
| `list-strategy-signals`, `list-strategy-trades`, `get-strategy-flags`, `list-trades` | 100 | `offset` (`page` existed) |
| `search-strategies` | 30 | `page`, `offset` |
| `list-backtests`, `list-backtest-jobs` | 25 | `offset` (`page` existed) |
| `list-markets` | 10 | `page`, `offset` |
| `get-ticker-analysis` | 10 | `offset` (`page` existed) |
| `get-ticker` without a symbol | 1000 | `page`, `offset`. A page of 1000 is usually over the size budget: follow `next_offset`. |
| `browse-users`, `discover-groups` | 20, 10 | `page`, `offset` |
| `list-support-tickets` | 20 | `page`, `offset` |

### New or changed `page` and `per_page`

| Tool | Change |
| ---- | ------ |
| `list-news`, `list-crypto-news`, `list-popular-news` | `per_page` now takes effect (it was ignored and every page had 10 items) and is 1 to 50. |
| `get-analysis` | New `page` and `per_page` (1 to 50, default 10). The description now says what the tool returns: the Analysis feed. |
| `list-sectors` | New `page`. `per_page` is 1 to 100, default 10. |
| `list-activities` | New `page` and `per_page` (1 to 50, default 30). |
| `list-invites` | New `page` and `per_page` (1 to 50, default 10). |
| `list-users` | `per_page` is 1 to 100; `meta` beside `total`, `per_page`, `current_page`. |
| `list-strategies` | `meta` gains `has_more`. |
| `list-account-cash-transfers`, `list-credit-holds`, `screen-technicals`, `get-older-messages` | `meta` added or gains `has_more`. |

### Other arguments

| Tool | Change |
| ---- | ------ |
| `get-accounts-balances` | `days` is refused outside 1 to 365 with the same sentence as the other bounds. |
| `list-orders` | `max_results` (1 to 500) is refused the same way. |
| `get-ticker-bars` | `limit` (1 to 1000) is refused the same way. When the size budget cuts bars, `meta.next_cursor` is null: ask again with a smaller `limit`. |
| `get-sector` | `sector_id` must be plain digits. An undocumented second name for it, `id`, is no longer read. |
| `list-markets`, `get-ticker` | `market_id` must be plain digits. |
| `get-news` | `id` must be plain digits. |
| `deploy-strategy`, `duplicate-strategy` | `strategy_id` must be a whole number of 1 or more. |
| `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers` | An `account_id` that is not one of the caller's accounts answers "No linked account of yours has that id.", like the other account tools. |
| `get-order`, `list-orders` | The caller's own account that is not linked for orders answers "That account of yours is not linked with the broker for orders. Link it again in OHLCX." |
| `run-trading-agent` | No longer marked read-only: its agent can change the user's settings and preferences and, for an admin, a user's credits and billing package. The description says so. It also lists what the agent now reads: linked accounts with their realized profit and loss and balance over time, watchlists and the Screener's screens. |
| `run-support-agent` | Description corrected: it reads the knowledge base and pages of ohlcx.com, as a guest. |

### Failures

- **63 tools no longer add the cause of a failure to their sentence.** "Unable to fetch sector: ..." is now "Unable to fetch sector."
- **Of those, 22 write tools say why the API refused the request** (a 422), in the API's own validation lines after the tool's sentence, at most ten lines of 200 characters, no markup: `update-password`, `update-profile`, `create-group`, `update-group`, `invite-to-group`, `join-group`, `send-invite`, `accept-invite`, `respond-join-request`, `send-message`, `save-settings`, `update-preferences`, `log-activity`, `create-knowledge-base-article`, `update-knowledge-base-article`, `submit-contact-form`, `report-issue`, `submit-support-request`, `adjust-user-billing`, `set-user-billing-package`, `change-user-role`, `block-unblock-user`. The other 41 (the read tools, the two agent tools, the deletes) answer their sentence alone whatever happened.
- **OHLCX Light.** The tools that already passed the API's words on for a refusal on Pro now read a failure the same way on Light: the validation lines of a 422 after the tool's sentence, and "That was not found." for a 404 (both were the sentence alone). A 401 or a 403 on Light stays the tool's sentence alone, because there it is the server's own access that was refused, not the user's.

### The in-app assistant

- `list_brokerage_accounts`: an account's label is five asterisks and then up to four digits of a number the broker stores masked, or the last three characters of any other number (was four asterisks and up to four characters). It is the label every other tool shows for the same account.
- **A failed turn has a code.** The stream's `error` event is now `{"type":"error","code":...,"error":...,"retryable":...}`. The codes are `timeout`, `busy`, `too_long`, `step_limit`, `unavailable` and `failed`, each with one fixed sentence under `error`, which is kept for clients that know no codes. The table is in [`in-app-assistant.md`](in-app-assistant.md#a-failed-turn). A stream that ends after tool calls and no text is an error only when the step limit was reached.
- **A request with `stream: false` that fails** answers that same object as JSON, with status 504, 503, 413, 502, 402 or 502 by code. The old body, `{"text": "AI provider unavailable (insufficient credits or quota)."}`, is gone.
- **New limits.** The three agents take at most 12 steps in a turn (before: 1.5 times the agent's tool count, which is more than 12 for a signed-in user) and each request to the model may take 120 seconds (before: 60).
- **Failover.** The next provider is now tried when the first is rate limited or overloaded as well as out of credits, and only while nothing of the answer has been sent. A tool that started is never run on a second provider.
- **Two new assistant tools** (OHLCX Pro, with Ask OHLCX on), 47 tool names in all. `get_backtest_run_trades` reads single trades of one saved run: filtered, sorted, at most 50 rows, with the totals of every match; it is listed only where the app reaches the strategies data as the signed-in user. `show_backtest_trades` shows trades of the open run as a card the page draws from the trades it holds; it reads nothing and returns no trade.
- **New page-context key `trades_card`** (kind `backtest_run`, the boolean `true` only): the page saying it can draw the trades card. The server offers `show_backtest_trades` only then, and removes the key from what the model reads. The front end sends it only with the build switch `VITE_RUN_ASSISTANT_TRADES=true`. Switch that on only on a host whose package has the tool: an older package passes the key into the run's data with no tool behind it.
- **One shared trade filter.** Both tools take `filters`, a list of `{"field", "value"}` entries, beside `sort`, `order` and `limit`. A field is one of `direction`, `option_type`, `result`, `exit_reason`, `entry_hour`, `weekday`, `from`, `to`, `min_pnl`, `max_pnl`, `contract`; a value is always text; a field is given at most once; an entry with an empty value asks for nothing and is left out. A filter given as an argument of its own is refused, with a sentence that points to `filters`. A profit bound at the outer limit (`min_pnl` of -1000000000, `max_pnl` of 1000000000) lets every trade through and is left out of the view. What the card tool returns is unchanged: a view whose `filter` is a plain object. The browser applies the same rules to the card. They are pinned by `tradeFilterCases.json`, held byte for byte in the package and in the host app with the same hash.
- **Two more assistant tools that show a card** (OHLCX Pro, with Ask OHLCX on), 49 tool names in all. `show_backtest_breakdown` shows how the trades of the open run split by entry hour, weekday, exit kind, side, calls or puts, or month; `show_backtest_stats` shows one to six headline figures as tiles, out of 23 names. Both read nothing and return a checked view with no figure; the page draws the card from the run it holds. An answer may show trades, a breakdown and figures and carry one proposal, one of each.
- **New page-context key `cards`** (kind `backtest_run`): the page's list of the cards it can draw, `"trades"`, `"breakdown"`, `"stats"`. The server offers each card's tool only for a name in the list and removes the key from what the model reads. A name it does not know is ignored on its own; a value that is not a list of text is ignored as a whole. `trades_card: true` still works alone and means `"trades"`. The front end sends the list only with `VITE_RUN_ASSISTANT_BREAKDOWN=true` or `VITE_RUN_ASSISTANT_STATS=true` (both off by default, Pro), and lists `"breakdown"` only for a run whose every trade the page holds. Install the package release with the two tools first, then set the switches and build: an older package passes the unknown key on to the model, and no card comes.
- **Two more shared fixtures.** The grouping of a breakdown and the names of the stats card are written on both sides and pinned by `tradeBreakdownCases.json` (SHA-256 `75ed9bfb2ed94f3a0e788e4e267bf3589bb440c898f8dc84539c5a5d8c205730`) and `statsCardCases.json` (SHA-256 `177766e4c70040f2386f62a03da0c784be9d9049981fc08ee639dd2061264d26`), each held byte for byte in both repositories.
- **One rounding on the backtest run page.** The results header ("Net profit", "Win rate"), the Metrics tab's own rows ("Net profit", "Gross profit", "Gross loss", "Win rate", and the bar above them) and its breakdowns (by signal, exit, weekday and hour) now write money as `floor(sum * 100 + 0.5) / 100` and a win rate as `floor(wins * 1000 / trades + 0.5) / 10`, in floating point as the server does, and the breakdowns mark the best and the worst group by the rounded result. The breakdown and stats cards use the same rule, so no two places show two numbers for the same trades. With profits in whole cents and trade counts that are not multiples of 80 nothing reads differently. Otherwise a figure can change by its last digit, in either direction: 23 winners of 80 trades reads 28.8% (was 28.7%); a sum of 8.575 reads $8.57 (was $8.58); a sum of 1400.5149999999999 reads $1,400.52 (was $1,400.51); a sum of -0.125 reads -$0.12 (was -$0.13); a loss under half a cent reads "+$0.00" (was "-$0.00" in red); groups less than a cent apart are no longer marked best and worst. A run saved without its longest losing streak shows a dash there (was 0). This is in the front end and does not depend on either switch.
- **The prompts and the cards.** The first line of "Response formatting" in the main prompt now says that what a `show_` tool is offered for is shown by calling it, with no table and no block, and that trades of a backtest run are never written as a table. The backtests prompt has a new block, "Cards of a backtest run (Pro)". The rules for each card are also in the run's own section, which does not depend on the prompt files.
- **The prompts** of the three agents have a rule for turns that failed and say the assistant cannot create or change a strategy or run a backtest. A host reads its own published copies of the prompts, so it gets the rule when it republishes them.
- **Eight new assistant tools that only read**, 57 tool names in all: `screen_market_gaps`, `screen_symbol_gaps` and `screen_technicals` (the Screener page's three screens), `list_watchlists` and `get_watchlist` (symbols only, no prices), and `get_account_pnl`, `get_account_pnl_by_symbol` and `get_account_growth` (realized profit and loss, by symbol, and the balance over time of one linked account). The Trading and the Unified agents have them for a signed-in user, on OHLCX Light and on OHLCX Pro, with nothing switched on. Tool counts for a signed-in user: Trading 30 on Light and 41 on Pro (were 22 and 33); Unified 33 on Light, 44 on Pro and 47 on Pro with Ask OHLCX on (were 25, 36 and 39); Support is unchanged at 21. No tool saves a screener, changes a watchlist, starts a profit and loss sync, or reads single closed trades or cash transfers; the assistant has no saved screeners to read, because there are none. No MCP tool changed.
- **"Hide Account Balance" is honoured by the account tools.** While the user has it on, the results of `get_account_pnl`, `get_account_pnl_by_symbol`, `get_account_growth` and `list_brokerage_accounts` hold no amount of money (profit and loss, fees, balances, buying power), only percentages, counts and dates, and the model is told so in a fixed note. If the preference cannot be read it counts as on. The MCP server's own account tools do not follow this preference.
- **`list_brokerage_accounts` result changed.** Every result now has `balances_hidden` (true or false), and `note` when true. When true, the five balance keys (`liquidation_value`, `cash_balance`, `buying_power`, `day_trading_buying_power`, `balances_as_of`) are absent from every row, not null. A client that draws the accounts list from this result must handle rows without figures.
- **The prompts** of the Trading and the Unified agent have a subsection for these tools and for `balances_hidden`, and the Unified prompt's "Response formatting" says they are not written as tables. A host that published its own copies gets them when it republishes.

### The relay (OHLCX Light)

- `GET /api/support/tickets` passes `page` on to the support desk when it is a whole number of 1 or more.
- Whether the relay routes exist is read from the configuration only, and the data source setting is read without regard to case.

## At a glance

| Area | 1.0.350 | 1.0.351 |
| ---- | ------- | ------- |
| New MCP tools | `retain-strategy` | `list-strategy-accounts`, `set-strategy-accounts` |
| MCP tools whose input or output changed | `list-strategies`; the strategy and condition write tools (refusals) | the account and order tools; `list-credit-holds`, `list-activities`, `get-user-billing`; `retain-strategy` |
| Assistant | Ask OHLCX; bounded results on every tool; three strategy tools | `get_strategy_routing`, `propose_strategy_accounts` |
| Relay (Light) | Strategy and condition writes keep a refusal's status and never send its cause | no change |

## New MCP tools

### `retain-strategy` (1.0.350)

Takes a strategy out of evaluation. Arguments: `strategy_id` (integer, required), `stop` (boolean, optional).

- A plain retain leaves the strategy's switches as they were, so deploying it again resumes them.
- `stop` true also switches orders, trades and signals off.
- Since 1.0.351 it also refreshes `list-strategies` at once.

A deployed strategy refuses changes. The workflow is: `retain-strategy`, make the change, `deploy-strategy`.

### `list-strategy-accounts` (1.0.351, OHLCX Pro only)

No arguments. Lists the user's linked accounts as a strategy's orders can be routed to them.

```json
{
  "connected": true,
  "accounts": [
    { "id": 4, "label": "*****678", "broker": "schwab", "routable": true, "reason": null, "is_default": true },
    { "id": 5, "label": "*****321", "broker": "alpaca", "routable": false, "reason": "Accounts at this broker cannot receive strategy orders yet." }
  ]
}
```

At most 50 accounts; `more` says how many were left out. `reason` is a sentence, not a code.

### `set-strategy-accounts` (1.0.351, OHLCX Pro only)

Chooses which linked accounts receive a strategy's orders.

| Argument | Type | Notes |
| -------- | ---- | ----- |
| `strategy_id` | integer, required | |
| `mode` | `selected` or `all`, required | `all`: every linked account that can receive orders when an order is sent, including accounts linked later. |
| `account_ids` | array of integers | Required with `selected`: ids from `list-strategy-accounts`, at most 50, each once. JSON integers only. An empty list removes every account. Not used with `all`. |

Answers `{ "strategy_id": 7, "routing": { "mode", "connected", "can_route", "accounts": [ { "id", "label", "broker", "routable", "reason", "set_aside" } ] } }`.

- The choice replaces the previous one.
- It never switches orders on or off.
- Confirm with the user first, naming accounts by their masked labels.
- `set_aside: true` on an account means an order to it was refused: it receives no orders until the accounts are set again. Setting the same choice again brings it back.

Refusals, each a fixed sentence:

| Sentence | When |
| -------- | ---- |
| Retain the strategy before changing it. | The strategy is deployed. |
| Choose accounts from your linked accounts. | An id is not one of the user's linked accounts. |
| Alpaca accounts cannot receive strategy orders yet. | An account at a broker that cannot be routed to yet. |
| Switch orders off before removing every account that orders can go to. | It would leave a real strategy with orders on without an account. |
| Choose at most 50 accounts. | Too many ids. |
| Unable to set this strategy's accounts. You are not allowed to change this strategy. | The strategy is not the caller's. |
| Order routing accounts are managed in OHLCX Pro. | Called where routing is not available. |

Both tools are listed only on OHLCX Pro for a signed-in user.

## MCP tools whose input or output changed

### Accounts: no broker key, no full number (1.0.351)

No tool returns a broker's key for an account (`account_hash`, `accountHash`, `hashValue`, `broker_account_hash`) or a full account number any more. An account is its id and a masked label such as `*****678`, the same label `list-strategy-accounts` shows.

| Tool | Input | Output |
| ---- | ----- | ------ |
| `list-accounts` | unchanged | The key is removed at every depth. `account_number` is the masked label. Every other field is unchanged. |
| `get-account-balance` | `account_id`: see below | **New shape.** Was an object keyed by the broker's key. Now `{ "account_id": 4, "account": "*****678", "history": [ ... ] }`. |
| `get-accounts-balances` | unchanged (`days`) | **New shape.** Was an object keyed by the broker's key. Now `{ "accounts": [ { "account_id": 4, "account": "*****678", "history": [ ... ] } ] }`. A history that names no account is left out. |
| `get-account-growth`, `get-account-pnl` | `account_id`: see below | Same shape. A key is removed and a number masked if present. |
| `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers` | `account_id`: see below | `account_hash` is removed; `account_display` is the masked label. |
| `get-order`, `list-orders` | `account_id`: see below | No key. `accountNumber` in an order is a masked string at every depth (it was the full number). |
| `list-credit-holds` | unchanged | `broker_account_hash` is removed from every hold. |
| `list-activities` | unchanged | Inside each activity, a key is removed and an account number masked. |
| `get-user-billing` (admin) | unchanged | A key is removed and an account number masked. |

### `account_id` on the eight account and order tools (1.0.351)

`get-account-balance`, `get-account-growth`, `get-account-pnl`, `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers`, `get-order`, `list-orders`.

- The schema declares `"type": ["string", "integer"]`.
- Send the account's **id** from `list-accounts`, as a number (`4`) or in digits (`"4"`).
- A client that still holds a broker key may send it, but only its own user's key is accepted.
- The value may hold only letters, digits, `_` and `-`, at most 128 characters.
- `get-order` used to need the broker's key. It now takes the id. This is the change most likely to break an existing client, because the key is no longer available from `list-accounts`.
- `get-account-balance`, `get-account-growth`, `get-account-pnl`, `get-order` and `list-orders` answer "No linked account of yours has that id." for an id or a key that is not one of the caller's accounts. The other three answer that sentence for a key that is not the caller's.
- `list-orders` without `account_id` still lists every account.

### Failure sentences (1.0.351)

These tools no longer append the cause of a failure:

| Tool | Sentence |
| ---- | -------- |
| `list-accounts` | Unable to fetch accounts. |
| `get-account-balance` | Unable to fetch the account balance. |
| `get-account-growth` | Unable to fetch the account growth. |
| `get-account-pnl` | Unable to fetch the account profit and loss. |
| `list-activities` | Unable to fetch activities. |
| `get-user-billing` | Unable to fetch user billing. |

Most other tools still answer their own sentence followed by the cause.

### `list-strategies` (1.0.350)

New optional arguments `page` and `per_page` (1 to 50).

- Without them: the plain list, up to 50 strategies, as before.
- With either: `{ "strategies": [ ... ], "meta": { "total", "per_page", "current_page", "last_page" } }`.

This is the only MCP list tool that gained paging in these releases.

### Strategy and condition writes: refusals (1.0.350)

Twelve tools say in their description that they are refused while the strategy is deployed, and answer one sentence when it is: "Retain the strategy before changing it."

`update-strategy`, `update-strategy-settings`, `set-strategy-schedule`, `set-strategy-status` (switching on), `set-strategy-flag` (switching signals, trades or orders on, or toggling), `delete-strategy`, `clear-strategy-conditions-readings`, `clear-strategy-data` (flags), `create-condition`, `update-condition`, `delete-condition`, `delete-signal`.

Never refused for that reason: switching anything off, the notification switches, deploying, duplicating, backtests, deleting or clearing trades. Deleting a signal, or clearing all signals, is refused only while the strategy is deployed, real and has orders on.

`deploy-strategy`, `duplicate-strategy` and `create-strategy` joined them in answering two more refusals as one sentence each:

| Sentence | When |
| -------- | ---- |
| Choose a linked account before switching orders on. | Switching orders on for a real strategy with no account that can receive them. |
| Choose a linked account, or switch orders off, before deploying. | Deploying a real strategy with orders on and no account. |

For any other refusal these tools answer their own sentence. When the API refused the request as invalid, not signed in or not allowed, what the API said is added, shortened and cleaned. A strategy or condition that does not exist reads "That was not found."

### Per-user caches (1.0.350)

`list-strategies`, `list-signals` and `list-conditions` keep an answer for one minute per user. A write through any strategy, signal or condition tool clears it, so a list read after a write is fresh.

### Server instructions and the settings resource (1.0.351)

The server's instructions now also say that choosing a strategy's order routing accounts decides which brokerage accounts receive its orders, never switches orders on, and must be confirmed with the user. The `ohlcx://strategy-settings` resource gained a section on order routing accounts and on the deployed lock.

## The in-app assistant

### 1.0.350

- **Ask OHLCX** (OHLCX Pro, behind a switch): the assistant reads the open backtest run from the page; `list_backtest_runs` and `get_backtest_run`; the proposing tools `propose_backtest_change`, `propose_backtest_sweep` and `propose_strategy_draft`, each of which returns a card the user must press.
- **Three strategy tools** on the unified assistant: `get_trading_strategy`, `get_trading_strategy_statistics`, `get_trading_strategy_performance`.
- **Every tool's result is bounded.** Lists are short rows with a row limit and say `returned`, `count`, `total`, `truncated` and, where the total is not known, `more_may_exist`. `list_trading_strategies` gained a `page` argument (25 to a page).
- **Less personal data.** `list_brokerage_accounts` returns a masked label and a few fields, never a number or a key. The community tools return names, never emails. Failures are one fixed sentence.

### 1.0.351

- `get_strategy_routing` (OHLCX Pro): which linked accounts a strategy's orders go to, as masked labels. Read-only. No account id.
- `propose_strategy_accounts` (OHLCX Pro, in a strategy's settings): offers a change of the strategy's order accounts as a card with a "Set these accounts" button. It calls nothing and sets nothing. One proposal per answer. It refuses in an answer that read a web page, news, an article or messages.

## The relay (OHLCX Light)

Changed in 1.0.350. A Light app relays strategy requests to the hosted OHLCX API.

### Strategy and condition writes

Creating, updating and deleting a strategy or a condition, every settings section, the schedule, retain, retain-stop, deploy, duplicate, every switch (status, signals, trades, orders and their notifications), the Slack test notification, the four clear actions, and deleting a signal now answer like this:

| The API answered | The relay answers | `message` and `error` |
| ---------------- | ----------------- | --------------------- |
| 422 | 422, with the validation `errors` | The server did not accept these settings. |
| 422 with one of three named refusals | 422, with `errors` and a `code` | that refusal's sentence |
| 401 | 401 | You are signed out. Sign in and try again. |
| 403 | 403 | This account is not allowed to do that. |
| 404 | 404 | That was not found. |
| 429 | 429 | Too many requests. Wait a moment and try again. |
| a server error, or no answer | 502 | Unable to save right now. |
| anything else | 500 | Unable to save right now. |

The three codes: `strategy_deployed` ("Retain the strategy before changing it."), `no_routable_account` ("Choose a linked account before switching orders on."), `deploy_needs_account` ("Choose a linked account, or switch orders off, before deploying.").

```json
{
  "message": "Choose a linked account before switching orders on.",
  "error": "Choose a linked account before switching orders on.",
  "code": "no_routable_account",
  "errors": { "orders_on": ["Choose a linked account before switching orders on."] }
}
```

What a client should change:

- Read the status. A 4xx from this table means nothing was stored. Before, most of these answered 500 with the cause as `error`.
- A 404 is now a 404, not a 500.
- `message` and `error` carry the same sentence. Show either.
- To offer "choose an account", branch on `code`.

### The two account routes

`GET /api/strategy-accounts` and `POST /api/strategy/{strategy}/settings/update-accounts` are not relayed. On Light both answer 403 with "Order routing accounts are managed in OHLCX Pro." under `message` and `error`.

### The paged strategies list

`GET /api/strategies?paged=1` returns the paged list, with optional `page` and `per_page` (1 to 50). Without `paged` the two are ignored and the answer is the plain list, as before.

### Unchanged

Reads, backtests, the screener and the market, ticker and signal-action routes answer as before.
