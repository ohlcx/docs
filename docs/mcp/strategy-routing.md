# Strategies and order routing

A strategy sends its orders to the owner's linked brokerage accounts. This page explains the switches that decide whether it does, walks through the tool calls in order, and lists every refusal with what to do about it.

No tool on this page places an order. Together they decide whether a strategy will. Confirm each step with the user.

## The words

| Term | Meaning |
|------|---------|
| Deployed | The strategy is in evaluation. The engine evaluates only deployed strategies |
| Retained | The opposite of deployed: the strategy is out of evaluation and can be changed |
| Status | The strategy's main switch: on or off |
| Signals, trades, orders | Three switches: whether the strategy raises signals, takes trades, and places broker orders |
| Demo and real | A demo strategy never places broker orders. A real strategy can |
| Order accounts | The linked brokerage accounts that receive the strategy's orders |
| Routable | An account can receive strategy orders now |
| Set aside | An order to that account was refused. The account receives no orders until the strategy's order accounts are saved again |

A strategy sends broker orders only when it is deployed, its status is on, it is real, its orders switch is on, and at least one of its order accounts is routable.

## The rules

### Order accounts

- [`list-strategy-accounts`](tools/reference.md#list-strategy-accounts) lists the accounts that can be chosen. [`set-strategy-accounts`](tools/reference.md#set-strategy-accounts) sets the choice for one strategy.
- Both tools exist only on OHLCX Pro and only for a signed-in user. Elsewhere they are not listed.
- The choice has a mode:
    - `selected`: only the accounts in `account_ids`.
    - `all`: every linked account that can receive orders when an order is sent, including accounts linked later.
- The choice replaces the previous one.
- **Setting accounts never switches orders on or off.** It only decides where orders go once they are on.
- Only the user's own linked accounts that can receive orders are accepted.

### Demo and orders are tied

- Switching orders on makes the strategy real. It is allowed only when an order could reach one of the strategy's order accounts. Otherwise it is refused: "Choose a linked account before switching orders on."
- Making a strategy demo switches its orders off.
- A real strategy with orders on cannot be left without an account: "Switch orders off before removing every account that orders can go to."
- A real strategy with orders on and no account an order could reach cannot be deployed: "Choose a linked account, or switch orders off, before deploying."

### The deployed lock

While a strategy is deployed, the server refuses every change to what it is or does. The answer is always the same sentence:

```text
Retain the strategy before changing it.
```

| While deployed | Tools |
|----------------|-------|
| Refused | `update-strategy`, `delete-strategy`, `update-strategy-settings` (every section), `set-strategy-schedule`, `set-strategy-accounts`, `create-condition`, `update-condition`, `delete-condition`, `clear-strategy-conditions-readings`, `clear-strategy-data` with target `flags` |
| Refused when switching on or toggling | `set-strategy-status` with status `on`; `set-strategy-flag` with state `on` or `toggle` for signals, trades or orders |
| Refused only while the strategy is also real and has orders on | `delete-signal`, `clear-strategy-data` with target `signals`. There the signal is what stops the same order being sent twice. Always allowed for a demo strategy |
| Always allowed | Every off switch: `set-strategy-status` with status `off`, `set-strategy-flag` with state `off`. The notification switches. `retain-strategy`, `deploy-strategy`, `duplicate-strategy`, backtests, `delete-trade`, `clear-strategy-data` with target `trades` |

To change a deployed strategy: retain it, make the change, deploy it again.

!!! note "To stop a strategy, use off"
    Use state `off`, never `toggle`. `toggle` is refused while the strategy is deployed. `off` always works.

### Retain

[`retain-strategy`](tools/reference.md#retain-strategy) takes a strategy out of evaluation.

- A plain retain leaves the switches (status, signals, trades, orders) as they were, so deploying the strategy again resumes them.
- With `stop` set to `true` it also switches orders, trades and signals off. The status stays as it was.

After a retain, `list-strategies` shows the strategy as retained at once.

## The sequence

This is the order that works for a strategy that should send real orders. The examples use strategy `7` and accounts `4` and `5`.

### 1. Read the strategy

```json
{ "tool": "get-strategy", "arguments": { "id": "7" } }
```

The strategy comes back with its switches and, under `routing`, its current order accounts: the mode, whether an order would reach an account now (`can_route`), and each account by its account id and masked label, with whether orders can go there and, if not, the reason as a sentence. It is the same `routing` block that `set-strategy-accounts` answers, shown in step 3.

If the strategy is deployed, retain it before you go on:

```json
{ "tool": "retain-strategy", "arguments": { "strategy_id": 7 } }
```

### 2. List the accounts that can be chosen

```json
{ "tool": "list-strategy-accounts", "arguments": {} }
```

```json
{
  "connected": true,
  "accounts": [
    { "id": 4, "label": "*****678", "broker": "schwab", "routable": true, "reason": null, "is_default": true },
    { "id": 5, "label": "*****289", "broker": "schwab", "routable": true, "reason": null, "is_default": false },
    { "id": 6, "label": "*****412", "broker": "alpaca", "routable": false, "reason": "Accounts at this broker cannot receive strategy orders yet." }
  ]
}
```

| Field | Meaning |
|-------|---------|
| `connected` | Whether the user's broker connection is in place |
| `id` | The account id to pass to `set-strategy-accounts` |
| `label` | The masked label. An account with nothing stored to label it reads `Account` and its id |
| `broker` | `schwab`, `alpaca`, or `null` |
| `routable` | `true` when the account can receive strategy orders now |
| `reason` | `null` for a routable account. Otherwise one of the sentences below |
| `is_default` | Present on routable accounts when the API says which one is the user's default |
| `more` | Present only when the user has more than 50 accounts: how many were left out |

The reasons an account is not routable:

| `reason` | What to do |
|----------|------------|
| `This account is not linked with the broker for trading.` | The user links the account for trading in OHLCX |
| `Accounts at this broker cannot receive strategy orders yet.` | Choose an account at another broker |
| `This account is no longer among the user's linked accounts.` | Remove it from the choice |
| `The broker is not connected: connect it again in OHLCX.` | The user reconnects the broker in the app |
| `This account cannot receive strategy orders right now.` | Any other cause. Try later or choose another account |

### 3. Set the order accounts

Tell the user which accounts you are about to set, by their masked labels, and wait for a yes. Then:

```json
{
  "tool": "set-strategy-accounts",
  "arguments": { "strategy_id": 7, "mode": "selected", "account_ids": [4, 5] }
}
```

```json
{
  "strategy_id": 7,
  "routing": {
    "mode": "selected",
    "connected": true,
    "can_route": true,
    "accounts": [
      { "id": 4, "label": "*****678", "broker": "schwab", "routable": true, "reason": null, "set_aside": false },
      { "id": 5, "label": "*****289", "broker": "schwab", "routable": true, "reason": null, "set_aside": false }
    ]
  }
}
```

| Argument | Rule |
|----------|------|
| `strategy_id` | The strategy's id, a whole number |
| `mode` | `selected` or `all` |
| `account_ids` | Required with `selected`: a list of at most 50 different account ids, as whole numbers. An empty list removes every account. Not used with `all` |

| Field of `routing` | Meaning |
|--------------------|---------|
| `mode` | `selected` or `all` |
| `connected` | Whether the broker connection is in place. Present when the API gives it |
| `can_route` | Whether an order would reach at least one account now. Present when the API gives it |
| `accounts` | The strategy's order accounts. With mode `all`, the accounts that are routable now |
| `set_aside` | `true` when an order to this account was refused. See below |
| `more` | Present only when there are more than 50 accounts: how many were left out |

To send orders to every account that can take them, now and later:

```json
{ "tool": "set-strategy-accounts", "arguments": { "strategy_id": 7, "mode": "all" } }
```

Orders are still as they were. Nothing is sent yet.

### 4. Switch orders on

Confirm with the user. Then:

```json
{
  "tool": "set-strategy-flag",
  "arguments": { "strategy_id": 7, "flag": "orders", "state": "on" }
}
```

This makes the strategy real. It is refused when no order could reach one of the strategy's order accounts.

If the strategy's status is off, switch it on as well:

```json
{ "tool": "set-strategy-status", "arguments": { "strategy_id": 7, "status": "on" } }
```

Both calls are refused while the strategy is deployed, which is why they come before the deploy.

### 5. Deploy

Confirm with the user. Then:

```json
{ "tool": "deploy-strategy", "arguments": { "strategy_id": "7" } }
```

From here the engine evaluates the strategy, and a signal can lead to a broker order in each routable order account.

### Changing a deployed strategy later

```json
{ "tool": "retain-strategy", "arguments": { "strategy_id": 7 } }
```

Make the change (settings, schedule, conditions, order accounts), then deploy again:

```json
{ "tool": "deploy-strategy", "arguments": { "strategy_id": "7" } }
```

A plain retain leaves orders on, so the second deploy resumes sending orders. To stop orders as well, retain with `"stop": true`, or call `set-strategy-flag` with state `off` at any time.

## Set aside

When an order to one of a strategy's accounts is refused, the strategy sets that account aside. In the strategy's `routing` the account then shows `"set_aside": true`.

- A set-aside account receives no orders, whatever `routable` says.
- It stays set aside until the strategy's order accounts are saved again. Calling `set-strategy-accounts` with the same choice brings it back.
- A deployed strategy must be retained before its accounts can be saved.

What to do: tell the user which account was set aside, by its masked label. If they want it back, retain the strategy, call `set-strategy-accounts` again, and deploy.

## Refusals

Every refusal below is the exact sentence the client receives. None of them changed anything.

### From `set-strategy-accounts`

| Sentence | Why | What to do |
|----------|-----|------------|
| `Order routing accounts are managed in OHLCX Pro.` | The tool was called where it is not offered | Set the accounts in OHLCX Pro |
| `Send strategy_id as the strategy's id (a whole number).` | `strategy_id` is not a positive whole number | Fix the argument |
| `With mode "selected", send account_ids as a list of at most 50 different account ids (whole numbers) from list-strategy-accounts.` | `account_ids` is missing, not a list, holds a string, a repeat or more than 50 ids | Fix the argument. Send numbers, not strings |
| `Choose "selected" or "all".` | The mode is not one of the two | Fix the argument |
| `Send the accounts as a list of account ids.` | The accounts were not a list of ids | Fix the argument |
| `Choose at most 50 accounts.` | More than 50 accounts | Send fewer, or use mode `all` |
| `Choose accounts from your linked accounts.` | An id is not one of the user's linked accounts. The same sentence is given for an account that does not exist | Call `list-strategy-accounts` and use its ids |
| `Alpaca accounts cannot receive strategy orders yet.` | An Alpaca account was chosen | Choose accounts with `routable` true |
| `Switch orders off before removing every account that orders can go to.` | The strategy is real with orders on, and the new choice would leave it no account | Call `set-strategy-flag` with flag `orders` and state `off` first, or keep a routable account |
| `Retain the strategy before changing it.` | The strategy is deployed | Call `retain-strategy`, then try again |
| `Unable to set this strategy's accounts. You are not allowed to change this strategy.` | The strategy is not the caller's to change | Do not retry |
| `Unable to set this strategy's accounts. That was not found.` | No such strategy | Check the id with `list-strategies` |
| `Unable to set this strategy's accounts. You are signed out. Sign in and try again.` | The session ended | The user signs in again |
| `Unable to set this strategy's accounts. The server did not accept these settings.` | The choice was refused for a reason the server does not pass on | Read the accounts again with `list-strategy-accounts` and check the choice |
| `Unable to set this strategy's accounts. Too many requests. Wait a moment and try again.` | Rate limited | Wait, then try again |
| `Unable to set this strategy's accounts.` | Anything else | Try again later |

When several of the accounts sentences apply, they come in one answer, separated by a space.

The tool checks `strategy_id`, `mode` and `account_ids` itself before it asks anything. A wrong `mode` is reported as a validation error that names `mode`, and a malformed `account_ids` as the tool's own sentence above, so the three sentences about the mode, the list and the limit of 50 are rarely seen.

### From `list-strategy-accounts`

| Sentence | What to do |
|----------|------------|
| `Order routing accounts are managed in OHLCX Pro.` | The tool was called where it is not offered |
| `Unable to list the accounts right now.` | Try again later |

### From the switches, deploy and the other strategy writes

| Sentence | Comes from | What to do |
|----------|-----------|------------|
| `Retain the strategy before changing it.` | Any tool the [deployed lock](#the-deployed-lock) refuses | Call `retain-strategy`, make the change, deploy again |
| `Choose a linked account before switching orders on.` | `set-strategy-flag` with orders on; also `create-strategy` and `update-strategy` when the payload switches orders on | Set the order accounts first (steps 2 and 3) |
| `Choose a linked account, or switch orders off, before deploying.` | `deploy-strategy`; also `create-strategy` and `update-strategy` when the payload deploys | Set the order accounts first, or switch orders off, then deploy |

Any tool that writes a strategy can answer with one of these three sentences. Any other failure of these tools is the tool's own sentence, for example `Unable to deploy the strategy.` See [Errors and refusals](errors.md).

## Reading a strategy's order accounts

`get-strategy` and `list-strategies` return each strategy's current choice under `routing`, so you can check it at any time without changing anything. The block is the one the routing tools give: a masked label for every account, `reason` as a sentence, `set_aside`, and at most 50 accounts with `more`.

The `ohlcx://strategy-settings` resource carries the same rules in short form for the client to read.
