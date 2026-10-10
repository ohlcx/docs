# Changes

Every tool whose input or output changed, release by release, so that an existing client can migrate. The server version is 1.1.0 throughout and the tool count is 147 since the first of these releases. Versions are those of the `ohlcx/trading-app` package, which carries the server.

| Release | What changed |
|---------|--------------|
| [1.0.355](#10355-bounded-lists-and-fixed-failure-sentences) | Every list tool is bounded and can be read on; every answer is at most 256 KB; every failure is a fixed sentence |
| [1.0.351](#10351-account-ids-and-order-routing) | Order routing accounts; accounts by id and masked label; the deployed lock |

## 1.0.355: bounded lists and fixed failure sentences

No tool was added or removed. Nothing was renamed or moved: `meta`, `more`, `truncated` and `next_offset` are added beside what a tool already answered. The patterns are explained on [Limits and paging](limits-and-paging.md) and the failures on [Errors and refusals](errors.md).

### Do this first

| If your client | Change it to |
|----------------|--------------|
| Reads the answer of `get-account-growth`, `get-account-pnl`, `get-sessions` or `get-sidebar-conversations` as a bare list | Read the list from the object it is now in. See [A different shape](#a-different-shape) |
| Assumes a list tool returns everything | Read `more`, `meta.has_more` and `next_offset`, and page. Several tools now return 50 rows by default |
| Calls `get-strategy-timeline` for a week | It now answers about the three most recent days by default. Use `logged_only` for longer ranges |
| Relies on the order of `symbols` from `get-account-pnl-symbols` | They now come largest move first, winners and losers alike |
| Reads `routing.accounts[].reason` of `get-strategy` or `list-strategies` as a code | It is now a sentence, as in the routing tools |
| Passes `id` to `get-sector` | Pass `sector_id`. The second name is no longer read |
| Parses the text after a colon in a failure | There is none any more. A failure is the tool's sentence, sometimes followed by the API's validation lines |
| Auto-approves `run-trading-agent` as read-only | It is no longer marked read-only |

### What every list tool now has

- **`page`** (1 to 100000) on every tool whose API pages, and **`per_page`** where the API reads one. The answer carries `meta`: `current_page`, `per_page` and `has_more`, with `last_page` and `total` when the API gives them.
- **`limit`** on every tool whose API does not page. `more` says how many rows were left out.
- **A size budget of 256 KB** for every answer. Rows are dropped, `truncated` is set and `more` counts them. An answer with no rows to drop is refused with "The result is too large to return. Ask for fewer rows or a narrower range."
- **`offset`** where a caller cannot lower a page length. While rows were left out the answer carries `next_offset`. A single row too large for any answer is stepped over and `row_too_large` says so.
- **Bounds in the schema.** `limit`, `page`, `per_page`, `offset`, `days`, `max_results` and `round_trips_limit` declare `minimum`, `maximum` and `default`. A value outside them, or not a whole number in plain digits, is refused with a sentence such as `limit must be a whole number from 1 to 200.`

### A different shape

| Tool | Change |
|------|--------|
| `get-account-growth` | Was a bare list. Now `{account_id, account, growth}` |
| `get-account-pnl` | Was a bare list. Now `{account_id, account, pnl}` |
| `get-sessions` | Was a bare list. Now `{sessions}`. An empty list used to be answered as a failure and is now `{sessions: []}` |
| `get-sidebar-conversations` | Was a bare list. Now `{conversations}` |
| `get-strategy-timeline` | Answers the most recent whole days that fit one answer (about three), with `returned` (`days`, `from`, `to`) and `more`. `days` is 1 to 365 and now defaults to 3 (was 7). New `logged_only` leaves out the minutes with no log. A day too busy to fit comes with its latest logged minutes and `more_minutes` |
| `get-account-pnl-symbols` | `symbols` come largest move first, winners and losers alike (was best first). `round_trips` are bounded: new `round_trips_limit` (1 to 200, default 50) and `more_round_trips` |
| `get-strategy`, `list-strategies` | The `routing` block is given as the routing tools give it: `reason` is a sentence (was a code), `set_aside_reason` and unknown keys are gone, a label is always masked, at most 50 accounts with `more` |
| `get-support-ticket` | A conversation over 256 KB keeps its newest messages; `more` counts the older ones left out |

### Fewer rows by default

These tools now return 50 rows unless `limit` (1 to 200) says otherwise, with `offset` to read on:

`search-knowledge-base`, `get-accounts-balances` (accounts), `get-account-pnl-symbols` (symbols), `list-watchlists` (the user's own lists), `screen-market-gaps`, `screen-asset-gaps`, `get-sessions`, `list-pending-join-requests`, `get-sidebar-conversations`.

`get-account-pnl-history` returns the 366 most recent days by default (`limit` 1 to 1000). Narrow `from` and `to` for older days.

These got `limit` only to ask for fewer. Their API stops where it always did, and the description now says so: `list-accounts` (100 accounts), `get-account-balance` (360 rows), `get-account-growth` and `get-account-pnl` (120 rows), `get-strategy-activities` (10), `get-transaction-history` (100 of each list), `get-unread-messages` (50).

### New `page`, and `offset` within a page

| Tool | Page length | New arguments |
|------|-------------|---------------|
| `list-signals`, `list-conditions`, `get-strategy-conditions` | 100 | `page`, `offset` |
| `list-strategy-signals`, `list-strategy-trades`, `get-strategy-flags`, `list-trades` | 100 | `offset` (`page` existed) |
| `search-strategies` | 30 | `page`, `offset` |
| `list-backtests`, `list-backtest-jobs` | 25 | `offset` (`page` existed) |
| `list-markets` | 10 | `page`, `offset` |
| `get-ticker-analysis` | 10 | `offset` (`page` existed) |
| `get-ticker` without a symbol | 1000 | `page`, `offset`. A page of 1000 is usually over the size budget: follow `next_offset` |
| `browse-users`, `discover-groups` | 20, 10 | `page`, `offset` |
| `list-support-tickets` | 20 | `page`, `offset` |

### New or changed `page` and `per_page`

| Tool | Change |
|------|--------|
| `list-news`, `list-crypto-news`, `list-popular-news` | `per_page` now takes effect (it was ignored and every page had 10 items) and is 1 to 50 |
| `get-analysis` | New `page` and `per_page` (1 to 50, default 10). It returns the Analysis feed |
| `list-sectors` | New `page`. `per_page` is 1 to 100, default 10 |
| `list-activities` | New `page` and `per_page` (1 to 50, default 30) |
| `list-invites` | New `page` and `per_page` (1 to 50, default 10) |
| `list-users` | `per_page` is 1 to 100; `meta` beside `total`, `per_page`, `current_page` |
| `list-strategies` | `meta` gains `has_more` |
| `list-account-cash-transfers`, `list-credit-holds`, `screen-technicals`, `get-older-messages` | `meta` added or gains `has_more` |

### Other arguments

| Tool | Change |
|------|--------|
| `get-accounts-balances` | `days` is refused outside 1 to 365 with the same sentence as the other bounds |
| `list-orders` | `max_results` (1 to 500) is refused the same way |
| `get-ticker-bars` | `limit` (1 to 1000) is refused the same way. When the size budget cuts bars, `meta.next_cursor` is null: ask again with a smaller `limit` |
| `get-sector` | `sector_id` must be plain digits. An undocumented second name for it, `id`, is no longer read |
| `list-markets`, `get-ticker` | `market_id` must be plain digits |
| `get-news` | `id` must be plain digits |
| `deploy-strategy`, `duplicate-strategy` | `strategy_id` must be a whole number of 1 or more |
| `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers` | An `account_id` that is not one of the caller's accounts answers "No linked account of yours has that id.", like the other account tools |
| `get-order`, `list-orders` | The caller's own account that is not linked for orders answers "That account of yours is not linked with the broker for orders. Link it again in OHLCX." |
| `run-trading-agent` | No longer marked read-only: its assistant can change the user's settings and preferences and, for an admin, a user's credits and billing package |
| `run-support-agent` | Description corrected: it reads the knowledge base and pages of ohlcx.com, as a guest |

81 tools are now marked read-only and 66 are not.

### Failures

- **63 tools no longer add the cause of a failure to their sentence.** "Unable to fetch sector: ..." is now "Unable to fetch sector."
- **Of those, 22 write tools say why the API refused the request** as invalid, in the API's own validation lines after the tool's sentence (at most ten lines of 200 characters, no markup): `update-password`, `update-profile`, `create-group`, `update-group`, `invite-to-group`, `join-group`, `send-invite`, `accept-invite`, `respond-join-request`, `send-message`, `save-settings`, `update-preferences`, `log-activity`, `create-knowledge-base-article`, `update-knowledge-base-article`, `submit-contact-form`, `report-issue`, `submit-support-request`, `adjust-user-billing`, `set-user-billing-package`, `change-user-role`, `block-unblock-user`. The other 41 answer their sentence alone whatever happened.
- **OHLCX Light.** The tools that already passed the API's words on for a refusal on Pro now read a failure the same way on Light: the validation lines of an invalid request after the tool's sentence, and "That was not found." when the thing does not exist. A refusal for not being signed in or not being allowed stays the tool's sentence alone on Light, because there it is the server's own access that was refused, not the user's.

## 1.0.351: account ids and order routing

This section lists every tool whose input or output changed in 1.0.351 and the release before it, compared with the first edition of these pages. The tool count went from 144 to 147.

The release did three things:

1. **Strategy order routing.** A strategy now sends its orders to order accounts you choose. Two new tools read and set them.
2. **Accounts by id and masked label everywhere.** No tool returns a broker account key or a full account number any more.
3. **The deployed lock.** A deployed strategy refuses changes until it is retained. A new tool retains it.

### Do this first

| If your client | Change it to |
|----------------|--------------|
| Reads an account key from `list-accounts` or any other answer | Use the account's `id`. The key is no longer returned |
| Reads the answer of `get-accounts-balances` or `get-account-balance` as an object keyed by account key | Read the new shapes below |
| Shows a full account number | Show the masked label. Full numbers are no longer returned |
| Passes an account key as `account_id` | Pass the account id from `list-accounts`. Your own key is still accepted for now |
| Treats the broker's `accountNumber` in an order as a number | It is now a string, the masked label |
| Changes a strategy that is deployed | Call `retain-strategy` first, then `deploy-strategy` again |
| Matches on failure texts of the account tools | They are now fixed sentences. See below |

### New tools

| Tool | What it does | Offered to |
|------|--------------|------------|
| [`list-strategy-accounts`](tools/reference.md#list-strategy-accounts) | Lists the linked accounts as a strategy's orders can be routed to them. Returns `connected` and `accounts` (each with `id`, `label`, `broker`, `routable`, `reason`, and `is_default` on routable accounts), and `more` when over 50 | Signed in, OHLCX Pro |
| [`set-strategy-accounts`](tools/reference.md#set-strategy-accounts) | Chooses a strategy's order accounts. Arguments `strategy_id`, `mode` (`selected` or `all`), `account_ids`. Returns `strategy_id` and `routing`. Never switches orders on | Signed in, OHLCX Pro |
| [`retain-strategy`](tools/reference.md#retain-strategy) | Takes a strategy out of evaluation so that it can be changed. Arguments `strategy_id`, `stop` (optional) | Signed in |

All three are walked through on [Strategies and order routing](strategy-routing.md).

### Changed: account and order tools

The new shapes are shown in full on [Accounts and identifiers](accounts.md).

| Tool | Input | Output |
|------|-------|--------|
| `list-accounts` | No change | The account key is removed at every depth. `account_number` is the masked label, the same label `list-strategy-accounts` shows. Every other field is unchanged |
| `get-accounts-balances` | No change | **New shape.** Was an object keyed by account key. Now `accounts`, a list with one entry per account: `account_id`, `account` (the masked label) and `history`. In each history row `account_display` is the masked label. A history that names no account is left out |
| `get-account-balance` | `account_id` must be one of the caller's accounts | **New shape.** Was an object keyed by account key. Now `account_id`, `account` (the masked label) and `history` |
| `get-account-growth`, `get-account-pnl` | `account_id` must be one of the caller's accounts | Same shape. An account key in it is removed and a full number masked |
| `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers` | `account_id` may be a number. A key is accepted only when it is the caller's own. Digits are always read as an account id, never as an account number | The account key is removed. `account_display` is the masked label |
| `get-order` | `account_id` is the account id from `list-accounts` | `accountNumber` is the masked label (a string; it was the full number) at every depth. No key appears |
| `list-orders` | The optional `account_id` is the account id from `list-accounts`. Left out, `null` or empty still lists every account | The same as `get-order` |
| `list-credit-holds` | No change | The account key is removed from every hold |
| `get-user-billing` (admin) | No change | Any account key is removed and any account number masked |
| `list-activities` | No change | Any account key is removed and any account number masked inside each activity |

#### `get-accounts-balances`, before and after

Before:

```json
{
  "<account key>": [
    { "account_id": 4, "account_display": "<full number>", "date": "2026-10-01", "current_balance": 25000.5 }
  ]
}
```

After:

```json
{
  "accounts": [
    {
      "account_id": 4,
      "account": "*****678",
      "history": [
        { "account_id": 4, "account_display": "*****678", "date": "2026-10-01", "current_balance": 25000.5 }
      ]
    }
  ]
}
```

#### `account_id` on every tool that takes one

`get-account-balance`, `get-account-growth`, `get-account-pnl`, `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers`, `get-order` and `list-orders` now declare `account_id` as a string or an integer, so a client that checks its arguments can send the number `list-accounts` gives.

An `account_id` that is not one of the caller's linked accounts answers:

```text
No linked account of yours has that id.
```

A value with a slash, a dot, a space or a query in it is refused as a wrong argument.

### Changed: failure texts

These tools used to end their failure with the cause as OHLCX reported it. They now answer a fixed sentence.

| Tool | Failure sentence now |
|------|----------------------|
| `list-accounts` | `Unable to fetch accounts.` |
| `get-account-balance` | `Unable to fetch the account balance.` |
| `get-account-growth` | `Unable to fetch the account growth.` |
| `get-account-pnl` | `Unable to fetch the account profit and loss.` |
| `list-activities` | `Unable to fetch activities.` |
| `get-user-billing` (admin) | `Unable to fetch user billing.` |

See [Errors and refusals](errors.md) for what to do with each kind of failure.

### Changed: strategy tools

| Tool | Change |
|------|--------|
| `list-strategies` | New optional `page` and `per_page` (1 to 50). With either, the answer is the paged list with `meta`. Without arguments nothing changed. See [Limits and paging](limits-and-paging.md#list-strategies) |
| `get-strategy` | The strategy now carries its order accounts under `routing` |
| `update-strategy`, `delete-strategy`, `update-strategy-settings`, `set-strategy-schedule`, `clear-strategy-conditions-readings`, `create-condition`, `update-condition`, `delete-condition` | Refused while the strategy is deployed: `Retain the strategy before changing it.` |
| `set-strategy-status` | Switching on is refused while the strategy is deployed. Switching off always works |
| `set-strategy-flag` | Switching signals, trades or orders on, or toggling them, is refused while the strategy is deployed. Switching them off always works, and so do the notification switches. Switching orders on is also refused when no order could reach an account: `Choose a linked account before switching orders on.` |
| `clear-strategy-data` | Clearing flags is refused while the strategy is deployed. Clearing signals is refused only while it is deployed, real and has orders on. Clearing trades is never refused |
| `delete-signal` | Refused only while its strategy is deployed, real and has orders on |
| `deploy-strategy` | Refused for a real strategy with orders on and no account an order could reach: `Choose a linked account, or switch orders off, before deploying.` |
| `retain-strategy` | New. After it, `list-strategies` shows the strategy as retained at once |

### Changed: what the client is told

- The server's instructions gained one sentence: choosing a strategy's order routing accounts decides which brokerage accounts receive its orders and never switches orders on, and the client should confirm it with the user. The full text is on the [overview](overview.md#the-servers-instructions).
- The `ohlcx://strategy-settings` resource now explains the deployed lock and order routing accounts.

### Not changed

This note covers the tools the release changed. A tool that is not named here was not changed by it.
