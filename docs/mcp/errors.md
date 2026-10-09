# Errors and refusals

When a tool call fails, the server returns an MCP tool result marked as an error, with one short text. There are no error codes: the text is the whole answer. This page lists the kinds of failure, how to recognise each, and what a client should do.

A failed call changed nothing, unless this page says otherwise.

## The kinds

| Kind | How to recognise it | What to do |
|------|--------------------|------------|
| [Wrong arguments](#wrong-arguments) | A message that names an argument, or a sentence such as `strategy_id is required.` | Fix the call and send it again |
| [Not signed in](#not-signed-in) | `User not authenticated.`, or a tool's sentence followed by words such as `You are signed out. Sign in and try again.` | Ask the user to sign in. Do not retry before they have |
| [Not allowed](#not-allowed) | A sentence that starts `Only admins can`, or `You are not allowed to change this strategy.` | Stop. Tell the user. Do not retry |
| [Not found](#not-found) | A sentence ending in `That was not found.`, or `Strategy not found.`, or `No linked account of yours has that id.` | Read the list again and use an id from it |
| [Refused with a reason](#refused-with-a-reason) | One of the fixed sentences in the table below | Do what the sentence says, then call again |
| [Try again](#try-again) | The tool's own sentence and nothing else, for example `Unable to fetch the balances.` | Wait and call again with the same arguments. If it keeps failing, tell the user |

## Wrong arguments

The server checks arguments before it asks anything of OHLCX or the broker. An argument of the wrong type, outside its allowed values or missing is answered with a message that names the argument. Some tools answer with their own sentence instead:

```text
strategy_id is required.
Strategy payload is required.
Send strategy_id as the strategy's id (a whole number).
With mode "selected", send account_ids as a list of at most 50 different account ids (whole numbers) from list-strategy-accounts.
```

The [tool reference](tools/reference.md) gives every argument with its type and allowed values.

When OHLCX itself refuses the values of a call (for example a settings section with a value out of range), the answer is the tool's sentence followed by what was wrong, one short line per problem:

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

Other tools answer with their own sentence followed by OHLCX's words for it. In every case, ask the user to sign in again.

## Not allowed

| Sentence | Meaning |
|----------|---------|
| `Only admins can ...` (for example `Only admins can list users.`) | An admin tool was called by a user who is not an admin |
| `Unable to set this strategy's accounts. You are not allowed to change this strategy.` | The strategy is not the caller's |
| The tool's sentence followed by OHLCX's own words | OHLCX refused the call for this user |

A strategy can be read and changed only by the user who owns it. Do not retry a call that was not allowed.

## Not found

| Sentence | Meaning |
|----------|---------|
| The tool's sentence followed by `That was not found.` (for example `Unable to fetch the trade. That was not found.`) | No such strategy, trade, signal, backtest, job, watchlist or ticket for this user |
| `Strategy not found.`, `Condition not found.`, `Article not found.`, `News not found.`, `User not found.` | The same, from the tools that say it in their own words |
| `No linked account of yours has that id.` | The `account_id` is not one of the caller's linked accounts. See [Accounts and identifiers](accounts.md#passing-an-account-account_id) |

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

## Try again

When something fails for a reason the user and the client cannot fix (OHLCX or the broker could not be reached, or an unexpected fault), the answer is the tool's own sentence and nothing else. The cause is recorded on the server and is not sent.

```text
Unable to fetch accounts.
Unable to fetch the account balance.
Unable to list the accounts right now.
Unable to deploy the strategy.
Unable to set this strategy's accounts.
```

Call again later with the same arguments. Do not change the arguments, and do not treat the failure as "not found".

`set-strategy-accounts` also says when the server is rate limiting:

```text
Unable to set this strategy's accounts. Too many requests. Wait a moment and try again.
```

## What a failure text may contain

How much a failure says depends on the tool.

| Tools | A failure is |
|-------|--------------|
| `list-accounts`, `get-account-balance`, `get-account-growth`, `get-account-pnl`, `list-activities`, `list-strategies`, `list-strategy-accounts`, `set-strategy-accounts`, `get-user-billing` | A fixed sentence, or one of the fixed refusals above. Nothing of the cause |
| The strategy and condition writes (`create-strategy`, `update-strategy`, `delete-strategy`, `duplicate-strategy`, `deploy-strategy`, `set-strategy-status`, `set-strategy-flag`, `set-strategy-schedule`, `update-strategy-settings`, `clear-strategy-conditions-readings`, `clear-strategy-data`, `delete-signal`, `create-condition`, `update-condition`, `delete-condition`) | One of the three fixed strategy refusals when it applies. Otherwise as the next row |
| `retain-strategy`, the other account and order tools, strategy statistics and history, trades, single signals and their marks, backtests, Workspaces, watchlists, screeners, price bars and ticker analysis, support tickets, credit holds, AI usage, room discovery, join requests and unread messages | The tool's sentence. For a call that was invalid, not signed in or not allowed, followed by OHLCX's own words about it: at most 10 short lines, without markup. For not found, followed by `That was not found.` For anything else, the sentence alone |
| Most of the remaining tools (profile and settings, trading rooms, invites and messages, news, markets and sectors, knowledge base, credits, activity writes, `get-strategy`, `search-strategies`, `get-strategy-activities`, `get-strategy-conditions`, `list-signals`, the condition reads, the assistant tools, the admin billing and role writes) | The tool's sentence, a colon, and the cause as OHLCX reported it, for example `Unable to fetch news: ...` |

!!! note "Do not parse the text after a colon"
    For the last group, the text after the colon is written for a person and can change. Match on the part before the colon, and show the rest to the user as it is.

## A rule of thumb for clients

1. If the text is one of the fixed refusals, act on it.
2. If it names an argument, fix the call.
3. If it ends in `That was not found.` or is the linked account sentence, refresh your ids.
4. If it says the user is signed out or not allowed, stop and tell the user.
5. Otherwise wait and try again, and after a few attempts tell the user that OHLCX could not complete the request.

Never work around a refusal by calling a different tool to reach the same result. A refusal is the server telling you the user has to decide or change something first.
