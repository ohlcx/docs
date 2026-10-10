# Errors and refusals

When a tool call fails, the server returns an MCP tool result marked as an error, with one short text. There are no error codes: the text is the whole answer. This page lists the kinds of failure, how to recognise each, and what a client should do.

A failed call changed nothing, unless this page says otherwise.

**Every tool answers a fixed sentence when it fails.** The cause is recorded on the server and is never sent. No tool appends an exception's text any more. The only words that are not the tool's own are the API's validation lines for a request it refused as invalid, and those are bounded as described under [What a failure text may contain](#what-a-failure-text-may-contain).

## The kinds

| Kind | How to recognise it | What to do |
|------|--------------------|------------|
| [Wrong arguments](#wrong-arguments) | A message that names an argument, such as `page must be a whole number from 1 to 100000.` or `strategy_id is required.` | Fix the call and send it again |
| [Not signed in](#not-signed-in) | `User not authenticated.`, or a tool's sentence followed by words about signing in | Ask the user to sign in. Do not retry before they have |
| [Not allowed](#not-allowed) | A sentence that starts `Only admins can`, or `You are not allowed to change this strategy.` | Stop. Tell the user. Do not retry |
| [Not found](#not-found) | A sentence ending in `That was not found.`, or `Strategy not found.`, or `No linked account of yours has that id.` | Read the list again and use an id from it |
| [Refused with a reason](#refused-with-a-reason) | One of the fixed sentences in the table below | Do what the sentence says, then call again |
| [Too large](#too-large) | `The result is too large to return. Ask for fewer rows or a narrower range.` | Ask for less: a shorter period, a smaller `limit` |
| [Try again](#try-again) | The tool's own sentence and nothing else, for example `Unable to fetch the balances.` | Wait and call again with the same arguments. If it keeps failing, tell the user |

## Wrong arguments

The server checks arguments before it asks anything of OHLCX or the broker.

A whole-number argument (`page`, `per_page`, `limit`, `offset`, `days`, `max_results`, `round_trips_limit`) that is not a whole number in plain digits within its bounds is refused with one fixed sentence that names the argument and its bounds:

```text
page must be a whole number from 1 to 100000.
limit must be a whole number from 1 to 200.
offset must be a whole number from 0 to 99.
days must be a whole number from 1 to 365.
```

`true`, `"+2"` and `1.5` are refused the same way. The bounds of each tool are on [Limits and paging](limits-and-paging.md), and each tool's schema declares them as `minimum`, `maximum` and `default`.

Other arguments of the wrong type, outside their allowed values or missing are answered with a message that names the argument. Some tools answer with their own sentence:

```text
strategy_id is required.
Strategy payload is required.
Send strategy_id as the strategy's id (a whole number).
With mode "selected", send account_ids as a list of at most 50 different account ids (whole numbers) from list-strategy-accounts.
```

When OHLCX itself refuses the values of a call (for example a settings section with a value out of range), the tools that write say why: the tool's sentence followed by the API's validation lines.

```text
Unable to update the strategy's settings. <what OHLCX said about the values>
```

Fix the values and call again. For strategy settings, read the `ohlcx://strategy-settings` resource.

## Not signed in

Over the web transport every request is signed in. Over stdio a client may run without a signed-in user: it is then offered only four tools, and the rest are not in its tool list.

A session that ends during use shows up as:

```text
User not authenticated.
Unable to set this strategy's accounts. You are signed out. Sign in and try again.
```

Ask the user to sign in again.

## Not allowed

| Sentence | Meaning |
|----------|---------|
| `Only admins can ...` (for example `Only admins can list users.`) | An admin tool was called by a user who is not an admin |
| `Unable to set this strategy's accounts. You are not allowed to change this strategy.` | The strategy is not the caller's |
| On OHLCX Pro: a tool's sentence followed by OHLCX's own words | OHLCX refused the call for this user |

A strategy can be read and changed only by the user who owns it. Do not retry a call that was not allowed.

## Not found

| Sentence | Meaning |
|----------|---------|
| The tool's sentence followed by `That was not found.` (for example `Unable to fetch the trade. That was not found.`) | No such strategy, trade, signal, backtest, job, watchlist or ticket for this user |
| `Strategy not found.`, `Condition not found.`, `Article not found.`, `News not found.`, `User not found.` | The same, from the tools that say it in their own words |
| `No linked account of yours has that id.` | The `account_id` is not one of the caller's linked accounts. Every account and order tool answers this itself, before anything is asked. See [Accounts and identifiers](accounts.md#passing-an-account-account_id) |

The server does not say whether the thing exists for someone else. Read the list again (`list-strategies`, `list-accounts`, and so on) and use an id from it.

## Refused with a reason

These are fixed sentences. Each names what stands in the way. Nothing was changed.

| Sentence | Tools | What to do |
|----------|-------|------------|
| `Retain the strategy before changing it.` | Every write a deployed strategy refuses. See [the deployed lock](strategy-routing.md#the-deployed-lock) | Call `retain-strategy`, make the change, then `deploy-strategy` |
| `Choose a linked account before switching orders on.` | `set-strategy-flag` with orders on, and other strategy writes that switch orders on | Set the strategy's order accounts with `set-strategy-accounts`, then try again |
| `Choose a linked account, or switch orders off, before deploying.` | `deploy-strategy`, and other strategy writes that deploy | Set the order accounts, or switch orders off, then deploy |
| `Switch orders off before removing every account that orders can go to.` | `set-strategy-accounts` | Switch orders off first, or keep a routable account in the choice |
| `Choose accounts from your linked accounts.` | `set-strategy-accounts` | Use ids from `list-strategy-accounts` |
| `Alpaca accounts cannot receive strategy orders yet.` | `set-strategy-accounts` | Choose accounts with `routable` true |
| `Choose at most 50 accounts.` | `set-strategy-accounts` | Send fewer, or use mode `all` |
| `Order routing accounts are managed in OHLCX Pro.` | `list-strategy-accounts`, `set-strategy-accounts` | The tools are not offered on this installation |
| `That account of yours is not linked with the broker for orders. Link it again in OHLCX.` | `get-order`, `list-orders` | The account is the caller's, but it cannot be read at the broker. The user links it again in the app |
| `You cannot delete your own user.` | `delete-user` | Nothing to do |
| `A user with this email already exists.` | `add-user` | Use another email, or update the existing user |

The full list for order routing, with the cause of each, is on [Strategies and order routing](strategy-routing.md#refusals).

`save-workspaces` handles a conflict without an error. When the Workspaces were changed somewhere else, the result is not marked as an error and reads:

```json
{
  "saved": false,
  "message": "These workspaces were changed somewhere else. Merge your change into the returned state and save again with the returned revision.",
  "state": { "version": 1, "dashboards": [] },
  "revision": 12
}
```

Merge your change into `state` and save again with `revision`.

## Too large

Every answer is at most 256 KB. A list that is larger loses rows and says so (see [Limits and paging](limits-and-paging.md#the-size-budget)); that is not an error. Only an answer that has no rows to drop is refused:

```text
The result is too large to return. Ask for fewer rows or a narrower range.
```

Ask for a shorter period or a smaller `limit`.

## Try again

When something fails for a reason the user and the client cannot fix (OHLCX or the broker could not be reached, or an unexpected fault), the answer is the tool's own sentence and nothing else.

```text
Unable to fetch accounts.
Unable to fetch the account balance.
Unable to fetch sector.
Unable to deploy the strategy.
Unable to set this strategy's accounts.
```

Call again later with the same arguments. Do not change the arguments, and do not treat the failure as "not found".

`set-strategy-accounts` also says when the server is rate limiting:

```text
Unable to set this strategy's accounts. Too many requests. Wait a moment and try again.
```

## What a failure text may contain

There are two kinds of tool.

### Tools that say why a request was refused

90 tools add the API's own words to their sentence in these cases, and only these:

| The API answered | OHLCX Pro | OHLCX Light |
|------------------|-----------|-------------|
| Invalid request (422) | The tool's sentence, then the API's validation lines | The same |
| Not signed in or not allowed (401, 403) | The tool's sentence, then the API's words | The tool's sentence alone, for the tools that read the hosted OHLCX API. There the refusal is about the server's own access, not about the user, so it is recorded for the operator and not told to the user |
| Not found (404) | The tool's sentence, then `That was not found.` | The same |
| Anything else | The tool's sentence alone | The same |

The API's lines are bounded: at most 10 lines, each at most 200 characters, with control characters removed, no repeats, and no line that holds markup.

The strategy and condition writes among them answer one of the three fixed strategy refusals instead when it applies (see [Refused with a reason](#refused-with-a-reason)).

These are the tools, by area:

| Area | Tools |
|------|-------|
| Knowledge base | `create-knowledge-base-article`, `update-knowledge-base-article` |
| Accounts | `get-accounts-balances`, `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers` |
| Orders (read-only) | `list-orders`, `get-order` |
| Strategies: reading | `get-strategy-statistics`, `get-strategies-statistics`, `get-strategy-performance`, `get-strategies-performance`, `get-strategy-timeline`, `list-strategy-signals`, `list-strategy-trades`, `get-strategy-flags` |
| Strategies: changing | `create-strategy`, `update-strategy`, `delete-strategy`, `duplicate-strategy`, `update-strategy-settings`, `set-strategy-schedule`, `clear-strategy-conditions-readings`, `clear-strategy-data` |
| Strategies: order routing and running | `set-strategy-flag`, `set-strategy-status`, `deploy-strategy`, `retain-strategy` |
| Conditions | `create-condition`, `update-condition`, `delete-condition` |
| Signals | `get-signal`, `delete-signal`, `set-signal-action`, `get-signal-actions` |
| Trades | `list-trades`, `get-trade`, `delete-trade` |
| Backtests | `list-backtests`, `get-backtest`, `rename-backtest`, `delete-backtest`, `run-backtest`, `run-backtest-sweep`, `list-backtest-jobs`, `get-backtest-job`, `cancel-backtest-job` |
| Workspaces | `get-workspaces`, `save-workspaces` |
| Watchlists | `list-watchlists`, `create-watchlist`, `rename-watchlist`, `delete-watchlist`, `add-watchlist-symbols`, `remove-watchlist-symbol` |
| Markets and price data | `get-ticker-bars`, `get-ticker-analysis` |
| Screeners | `screen-market-gaps`, `screen-asset-gaps`, `screen-technicals` |
| Analysis and AI usage | `get-ai-usage` |
| Activities | `log-activity` |
| Credits and billing | `list-credit-holds` |
| Support | `submit-contact-form`, `report-issue`, `submit-support-request`, `list-support-tickets`, `get-support-ticket`, `create-support-ticket`, `reply-support-ticket` |
| Profile and settings | `update-profile`, `update-password`, `update-preferences`, `save-settings` |
| Trading rooms and messages | `create-group`, `update-group`, `invite-to-group`, `join-group`, `discover-groups`, `browse-users`, `send-invite`, `accept-invite`, `respond-join-request`, `list-pending-join-requests`, `send-message`, `get-unread-messages` |
| Administration | `adjust-user-billing`, `set-user-billing-package`, `block-unblock-user`, `change-user-role` |

### Tools that answer their sentence alone

The other tools answer the same fixed sentence whatever happened: 56 tools, besides `ping`, which cannot fail. They are the read tools that are not listed above, the two assistant tools, most deletes, the admin user tools, `list-accounts`, `get-account-balance`, `get-account-growth`, `get-account-pnl`, `list-activities`, `list-strategies`, `get-user-billing` and the two order routing tools (whose refusals are the fixed sentences above).

| Area | Tools |
|------|-------|
| Health and assistants | `run-support-agent`, `run-trading-agent` |
| Knowledge base | `search-knowledge-base`, `get-knowledge-base-article`, `delete-knowledge-base-article` |
| Accounts | `list-accounts`, `get-account-balance`, `get-account-growth`, `get-account-pnl` |
| Strategies: reading | `list-strategies`, `get-strategy`, `search-strategies`, `get-strategy-activities`, `get-strategy-conditions` |
| Strategies: order routing and running | `list-strategy-accounts`, `set-strategy-accounts` |
| Conditions | `list-conditions`, `get-condition` |
| Signals | `list-signals` |
| Markets and price data | `list-markets`, `get-ticker`, `get-market-calendar`, `get-market-balance`, `list-sectors`, `get-sector`, `get-sector-balance` |
| News | `list-news`, `get-news`, `list-crypto-news`, `list-popular-news` |
| Analysis and AI usage | `get-analysis` |
| Activities | `list-activities`, `delete-activity` |
| Credits and billing | `get-credits`, `get-transaction-history` |
| Profile and settings | `get-user`, `get-sessions`, `delete-profile-photo`, `get-onboarding`, `complete-onboarding`, `get-preferences`, `get-settings` |
| Trading rooms and messages | `get-group`, `delete-group`, `leave-group`, `get-group-status`, `list-invites`, `get-older-messages`, `delete-message`, `get-sidebar-conversations` |
| Administration | `list-users`, `set-user-admin`, `update-user`, `add-user`, `delete-user`, `get-user-billing` |

## A rule of thumb for clients

1. If the text is one of the fixed refusals, act on it.
2. If it names an argument, fix the call.
3. If it ends in `That was not found.` or is the linked account sentence, refresh your ids.
4. If it says the user is signed out or not allowed, stop and tell the user.
5. If it says the result is too large, ask for less.
6. Otherwise wait and try again, and after a few attempts tell the user that OHLCX could not complete the request.

Match on the tool's own sentence. Show any words after it to the user as they are; do not parse them.

Never work around a refusal by calling a different tool to reach the same result. A refusal is the server telling you the user has to decide or change something first.
