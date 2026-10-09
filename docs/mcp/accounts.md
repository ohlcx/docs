# Accounts and identifiers

A user links brokerage accounts to OHLCX. The MCP server identifies each of them the same way in every tool: by an **account id** and a **masked label**.

| Term | What it is | Example |
|------|------------|---------|
| Account id | OHLCX's own number for a linked account. A positive whole number. This is what you pass as `account_id` and in `account_ids` | `4` |
| Masked label | The account's number with all but the end hidden. This is what you show the user | `*****678` |

## What is never shown

- **A full account number.** Wherever the broker or OHLCX stores one, the server returns the masked label in its place.
- **The broker's own key for an account** (its account hash). The server removes it from every answer. When a tool has to name an account to the broker, the server looks the key up itself from the account id you gave, among the caller's own accounts only, and never returns it.

This holds for every tool whose answer can hold an account: the account tools, the order tools, `list-credit-holds`, `list-activities`, `list-strategy-accounts`, `set-strategy-accounts` and, for admins, `get-user-billing`.

!!! note "Free text is relayed as written"
    The server hides account numbers and keys by field, at any depth of an answer. Text written by the broker or by a person, such as an order's status description or an activity's description, is passed on as it is.

## The masked label

A masked label is five asterisks followed by the end of the stored number:

| Stored | Shown |
|--------|-------|
| A number of four or more characters | `*****` and its last three characters, for example `*****678` |
| A number that was stored already masked | `*****` and the digits it kept (one to four), for example `*****289` |
| Anything shorter | `*****` |
| Nothing | `null` in the account tools. `Account 4` (the word and the account id) in the order routing tools |

The same account has the same masked label in every tool, so a client can match the `account_number` of `list-accounts` with the `label` of `list-strategy-accounts`.

## Passing an account: `account_id`

Start with [`list-accounts`](tools/reference.md#list-accounts) and use the `id` of an account wherever a tool asks for `account_id`.

`account_id` accepts:

- the account id as a number: `4`
- the account id in digits: `"4"`
- the caller's own broker key for the account, for clients that stored one before this release. New clients should not rely on this. See [Changes](changes.md).

Anything else is refused. An account that is not one of the caller's linked accounts answers:

```text
No linked account of yours has that id.
```

The same sentence is given for another user's account and for an account nobody has, so the answer does not tell them apart. Nothing is asked of the broker in that case. Do not retry: call `list-accounts` and use an id from it.

| Tool | `account_id` | An id or key that is not yours |
|------|--------------|--------------------------------|
| `get-account-balance`, `get-account-growth`, `get-account-pnl` | Required | `No linked account of yours has that id.` |
| `get-order` | Required | `No linked account of yours has that id.` |
| `list-orders` | Optional. Left out, `null` or empty lists every linked account | `No linked account of yours has that id.` |
| `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers` | Required | A key that is not yours: `No linked account of yours has that id.` An account id is passed on to the accounts API, which answers only for the caller's own accounts: an id that is not yours fails with the tool's own sentence. See [Errors and refusals](errors.md) |

`set-strategy-accounts` is stricter: its `account_ids` are whole numbers only. A string is not read as an id there, and a key is never accepted. See [Strategies and order routing](strategy-routing.md).

## The shape of each answer

The examples use made-up values. Fields the examples do not show are relayed as the accounts API or the broker gives them.

### `list-accounts`

No arguments. Returns the user's linked accounts. `account_number` is the masked label.

```json
{
  "accounts": {
    "accounts": [
      {
        "id": 4,
        "account_number": "*****678",
        "type": "MARGIN",
        "current_balances": { "liquidationValue": 25000.5 }
      },
      {
        "id": 5,
        "account_number": "*****289",
        "type": "CASH"
      }
    ]
  }
}
```

Each account also carries its flags, its balances and, where the API sends them, its balance histories.

### `get-accounts-balances`

Optional `days`: how many of the most recent days to return per account, up to 365 (default 30). Returns one entry per account. `account` is the masked label; `history` is oldest first.

```json
{
  "accounts": [
    {
      "account_id": 4,
      "account": "*****678",
      "history": [
        {
          "account_id": 4,
          "account_display": "*****678",
          "date": "2026-10-01",
          "initial_balance": 24800.0,
          "current_balance": 25000.5,
          "change": 200.5
        }
      ]
    }
  ]
}
```

With no linked account the answer is `{ "accounts": [] }`.

### `get-account-balance`

Required `account_id`. Returns the daily balance history of one account, oldest first.

```json
{
  "account_id": 4,
  "account": "*****678",
  "history": [
    { "date": "2026-10-01 09:30AM", "balance": 25000.5, "change": "200.50" }
  ]
}
```

### `get-account-growth` and `get-account-pnl`

Required `account_id`. The answer is the accounts API's growth or profit and loss data for that account. A full account number in it is replaced by the masked label.

### `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers`

Required `account_id`. Optional `period`, or `from` and `to` dates (`YYYY-MM-DD`) that replace it. The default period is `month` for `get-account-pnl-history` and `ytd` for the other two. The answer is the accounts API's own. In it, `account_display` is the masked label.

The two profit and loss tools need the user's consent to P&L sync, given in the app.

### Orders

`list-orders` and `get-order` relay the broker's order objects. In them:

- `accountNumber` is the masked label, a string such as `"*****678"`, at every depth;
- no account key appears.

`list-orders` needs `start_date` and `end_date` (`YYYY-MM-DD`; the end date covers the whole of that day). `status` filters by the broker's status, for example `FILLED`, `WORKING` or `CANCELED`. `max_results` is up to 500 (default 100).

`get-order` needs `account_id` and `order_id`, the broker's order id in digits.

Both tools are read-only. No tool places, changes or cancels an order.

### `list-credit-holds`, `list-activities`, `get-user-billing`

These answers can mention an account. No account key appears in them, and any account number is the masked label. `list-activities` returns `count`, `activities` and `meta`.

### Order routing accounts

`list-strategy-accounts` and `set-strategy-accounts` return accounts as `id` and `label` (the masked label), with whether each can receive orders. Their shapes are on [Strategies and order routing](strategy-routing.md).

## Checklist for a client

1. Call `list-accounts` once and keep the account ids.
2. Show the user masked labels, never ids alone.
3. Pass account ids as numbers.
4. Do not store or expect a broker key or a full account number: the server does not return either.
5. On `No linked account of yours has that id.`, refresh your list with `list-accounts`.
