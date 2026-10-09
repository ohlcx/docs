# Changes: account ids and order routing

This note lists every tool whose input or output changed in the latest release of the OHLCX MCP server, compared with the previous edition of these pages, so that an existing client can migrate. The server version is still 1.1.0. The tool count went from 144 to 147.

The release did three things:

1. **Strategy order routing.** A strategy now sends its orders to order accounts you choose. Two new tools read and set them.
2. **Accounts by id and masked label everywhere.** No tool returns a broker account key or a full account number any more.
3. **The deployed lock.** A deployed strategy refuses changes until it is retained. A new tool retains it.

## Do this first

| If your client | Change it to |
|----------------|--------------|
| Reads an account key from `list-accounts` or any other answer | Use the account's `id`. The key is no longer returned |
| Reads the answer of `get-accounts-balances` or `get-account-balance` as an object keyed by account key | Read the new shapes below |
| Shows a full account number | Show the masked label. Full numbers are no longer returned |
| Passes an account key as `account_id` | Pass the account id from `list-accounts`. Your own key is still accepted for now |
| Treats the broker's `accountNumber` in an order as a number | It is now a string, the masked label |
| Changes a strategy that is deployed | Call `retain-strategy` first, then `deploy-strategy` again |
| Matches on failure texts of the account tools | They are now fixed sentences. See below |

## New tools

| Tool | What it does | Offered to |
|------|--------------|------------|
| [`list-strategy-accounts`](tools/reference.md#list-strategy-accounts) | Lists the linked accounts as a strategy's orders can be routed to them. Returns `connected` and `accounts` (each with `id`, `label`, `broker`, `routable`, `reason`, and `is_default` on routable accounts), and `more` when over 50 | Signed in, OHLCX Pro |
| [`set-strategy-accounts`](tools/reference.md#set-strategy-accounts) | Chooses a strategy's order accounts. Arguments `strategy_id`, `mode` (`selected` or `all`), `account_ids`. Returns `strategy_id` and `routing`. Never switches orders on | Signed in, OHLCX Pro |
| [`retain-strategy`](tools/reference.md#retain-strategy) | Takes a strategy out of evaluation so that it can be changed. Arguments `strategy_id`, `stop` (optional) | Signed in |

All three are walked through on [Strategies and order routing](strategy-routing.md).

## Changed: account and order tools

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

### `get-accounts-balances`, before and after

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

### `account_id` on every tool that takes one

`get-account-balance`, `get-account-growth`, `get-account-pnl`, `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers`, `get-order` and `list-orders` now declare `account_id` as a string or an integer, so a client that checks its arguments can send the number `list-accounts` gives.

An `account_id` that is not one of the caller's linked accounts answers:

```text
No linked account of yours has that id.
```

A value with a slash, a dot, a space or a query in it is refused as a wrong argument.

## Changed: failure texts

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

## Changed: strategy tools

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

## Changed: what the client is told

- The server's instructions gained one sentence: choosing a strategy's order routing accounts decides which brokerage accounts receive its orders and never switches orders on, and the client should confirm it with the user. The full text is on the [overview](overview.md#the-servers-instructions).
- The `ohlcx://strategy-settings` resource now explains the deployed lock and order routing accounts.

## Not changed

This note covers the tools the release changed. A tool that is not named here was not changed by it.
