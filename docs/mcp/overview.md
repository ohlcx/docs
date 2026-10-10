# MCP overview

The OHLCX MCP server (name `OHLCX`, version 1.1.0) lets an AI client such as Claude or Cursor work with a user's OHLCX data: strategies, backtests, signals, trades, Workspaces, watchlists, linked brokerage accounts and their orders, market data, news, support tickets and the knowledge base.

It offers 147 tools, 3 prompts and 1 resource. This page says what the server can and cannot do. The other pages of this section are the reference:

| Page | What it covers |
|------|----------------|
| [Cursor setup](cursor-setup.md) | Configuring Cursor, checking the connection, troubleshooting |
| [Claude setup](claude-setup.md) | Connecting Claude Code, Claude Desktop and Claude on the web; getting a token |
| [Agents setup](agents-setup.md) | Using the server from an agent you build: authentication, read-only allow-lists, confirmed writes |
| [Accounts and identifiers](accounts.md) | Account ids, masked labels, what is never shown, the shape of every account and order answer |
| [Strategies and order routing](strategy-routing.md) | Order accounts, switching orders on, deploy and retain, with the tool calls in order and every refusal |
| [Errors and refusals](errors.md) | The fixed sentences a client receives when a call fails and what to do with each kind |
| [Limits and paging](limits-and-paging.md) | Pages, limits and offsets, each list tool's bounds, and the 256 KB size budget |
| [Tool reference](tools/reference.md) | Every tool by area, with one line, its kind, who is offered it, and its arguments |
| [Changes](changes.md) | Every tool whose input or output changed in the latest releases, for clients that need to migrate |

## What the server can do

- **Read** the signed-in user's strategies, conditions, signals, trades, saved backtests, Workspaces, watchlists, credits, activities, messages and settings.
- **Read** the user's linked brokerage accounts: balances, growth, profit and loss, cash transfers, and broker orders.
- **Read** market data: markets, tickers, price bars, sectors, screeners, the market calendar, news and published analysis.
- **Change** what belongs to the user in OHLCX: create and edit strategies and conditions, set a strategy's settings, schedule and order accounts, switch a strategy and its signals, trades and orders on or off, deploy and retain it, start backtests, save Workspaces and watchlists, open support tickets, send messages.
- **Administer** users, billing and knowledge base articles, for a signed-in admin only.

## What the server cannot do

- **No tool places, changes or cancels a broker order directly.** `list-orders` and `get-order` only read. `delete-trade` removes OHLCX's record of a trade; it does not close a position or cancel an order at the broker.
- **No tool shows a full account number or the broker's own key for an account.** An account is always its account id and a masked label such as `*****678`. See [Accounts and identifiers](accounts.md).
- **No tool reads or changes another user's strategies or accounts.** A strategy belongs to the user who created it. An account id that is not one of the caller's linked accounts is refused.
- **No tool changes what a deployed strategy does.** A deployed strategy refuses changes to its settings, conditions, schedule and order accounts, and refuses to be switched on, until it is retained. Switching things off always works. See [the deployed lock](strategy-routing.md#the-deployed-lock).

## What leads to broker orders

Orders are sent by a strategy, never by a tool call. A strategy sends orders to the owner's linked brokerage accounts when all of this is true:

1. it is **deployed** (the engine evaluates only deployed strategies),
2. its **status** is on,
3. it is **real**, not demo, and its **orders** switch is on,
4. at least one of its **order accounts** can receive orders.

So the tools that can lead to orders are the ones that change those four things, and the settings that shape an order:

| Tool | What it changes |
|------|-----------------|
| [`deploy-strategy`](tools/reference.md#deploy-strategy) | Puts the strategy into evaluation |
| [`set-strategy-status`](tools/reference.md#set-strategy-status) | Switches the strategy on or off |
| [`set-strategy-flag`](tools/reference.md#set-strategy-flag) | Switches signals, trades or orders on or off |
| [`set-strategy-accounts`](tools/reference.md#set-strategy-accounts) | Chooses which accounts receive the strategy's orders. It never switches orders on |
| [`update-strategy-settings`](tools/reference.md#update-strategy-settings), [`set-strategy-schedule`](tools/reference.md#set-strategy-schedule) | Order size, order type, exits, risk, and when the strategy may run |
| [`create-strategy`](tools/reference.md#create-strategy), [`update-strategy`](tools/reference.md#update-strategy) | A strategy's definition, which includes its switches |
| [`create-condition`](tools/reference.md#create-condition), [`update-condition`](tools/reference.md#update-condition), [`delete-condition`](tools/reference.md#delete-condition) | What makes the strategy raise a signal |

[Strategies and order routing](strategy-routing.md) walks through the sequence.

## What needs the user's confirmation

The server tells every client, in its instructions, to ask the user first. An operator should configure the client so that these calls are never approved automatically:

- switching a strategy on, or switching its orders on (`set-strategy-status`, `set-strategy-flag`);
- choosing a strategy's order accounts (`set-strategy-accounts`): name the accounts to the user by their masked labels;
- changing a strategy's settings (`update-strategy-settings`, `update-strategy`, `set-strategy-schedule`);
- retaining a strategy (`retain-strategy`);
- deleting anything (a strategy, a condition, a signal, a trade, a backtest, a watchlist, a message, a user);
- opening or answering a support ticket (`create-support-ticket`, `reply-support-ticket`): confirm the wording.

The server also sends a hint with each tool (read-only, or destructive). 81 of the 147 tools are marked read-only; the other 66 are not. The [tool reference](tools/reference.md#how-to-read-this-page) lists the hint of every tool. The hints help a client decide when to ask; they do not replace the list above.

!!! warning "Orders are real"
    A deployed, real strategy with orders on sends orders to a brokerage account without asking again. Treat every tool in the table above as a decision the user makes, not the client.

## The server's instructions

This is the text every client receives when it connects:

> OHLCX is a trading platform: strategies, backtests, signals, trades, workspaces, accounts, and market data. Tools expose the user's strategies (settings, schedule, statistics, performance), saved backtests, signals, trades, Workspaces, watchlists, accounts with their balances, profit and loss, cash transfers and broker orders (read-only), support tickets, markets, tickers and their price bars, screeners, sectors, news, conditions, and the knowledge base. No tool places, changes or cancels a broker order directly; a strategy that is switched on with orders on does. Confirm with the user before switching a strategy or its orders on, changing its settings, or deleting anything. Choosing a strategy's order routing accounts (set-strategy-accounts) decides which brokerage accounts receive its orders and never switches orders on: confirm it with the user too. Read the ohlcx://strategy-settings resource before creating a strategy or changing its settings. Prompts provide user context, product terminology (TSP, OCO, TRIM, order types), and support content from the knowledge base. When the user is authenticated, prefer using tools to fetch fresh data before answering.

## Transports and sign-in

| Transport | How to use | Sign-in |
|-----------|------------|---------|
| Web | `/mcp/ohlcx` while the app is running | Required (Laravel Sanctum session or token) |
| Stdio | `php artisan mcp:start ohlcx` | May run without a signed-in user |

Which tools a client is offered depends on who is signed in. A tool you are not offered is not in the tool list at all.

| Who | Tools offered |
|-----|---------------|
| No signed-in user | 4: `ping`, `run-support-agent`, `search-knowledge-base`, `get-knowledge-base-article` |
| A signed-in user | 119 more |
| A signed-in user on OHLCX Pro | 2 more: `list-strategy-accounts`, `set-strategy-accounts` |
| A signed-in user, where server backtests are switched on | 5 more: `run-backtest`, `run-backtest-sweep`, `list-backtest-jobs`, `get-backtest-job`, `cancel-backtest-job` |
| A signed-in user, where the app is connected to the support desk | 4 more: `list-support-tickets`, `get-support-ticket`, `create-support-ticket`, `reply-support-ticket` |
| A signed-in admin | 13 more: user administration, billing and knowledge base writing |

### OHLCX Pro and OHLCX Light

The two order routing tools exist only on OHLCX Pro, where the server reaches a strategy's order accounts as the signed-in user. On any other installation they are not listed, and a call made anyway answers:

```text
Order routing accounts are managed in OHLCX Pro.
```

Everything else in this section applies to both editions. See [Light vs Pro](../architecture/light-vs-pro.md).

## Prompts

| Name | Arguments | What it gives the client |
|------|-----------|--------------------------|
| `user-info` | `tone` (optional), `user_id` (optional, admin only) | A summary of the signed-in user. Listed only for a signed-in user |
| `trading-terminology` | `area` (optional: `options` or `orders`) | OHLCX product terminology: TSP, OCO, TRIM, order types |
| `support-knowledge-base` | `slug`, `area`, `q` (all optional) | Knowledge base content for answering a support question |

## Resource

| URI | What it holds |
|-----|---------------|
| `ohlcx://strategy-settings` | Every strategy setting by section, with its allowed values: what `create-strategy` needs and what each section of `update-strategy-settings` accepts. It also explains the deployed lock and order routing accounts. Read it before you create a strategy or change its settings |

## Assistant tools

Two tools run the assistants of the OHLCX app and return their answer as plain text. They call a language model.

| Tool | Reads | Offered to |
|------|-------|------------|
| `run-support-agent` | The knowledge base and pages of ohlcx.com, as a guest. It changes nothing | Everyone |
| `run-trading-agent` | The knowledge base, pages of ohlcx.com, and the signed-in user's credits and billing, settings and preferences, feeds, community and linked accounts, and on OHLCX Pro markets and strategies | A signed-in user |

`run-trading-agent` is not read-only. Its assistant can change the user's settings and preferences when the message asks for that, and for an admin it can also adjust a user's credits and set a user's billing package. It places no order and changes no strategy. Treat a call to it as a write.

For data you intend to process, call the data tools directly. See [Agents](../ai/agents.md).

## Good to know

- **Backtests.** A server-side run finishes as a saved backtest: poll `get-backtest-job`, then read the run with `get-backtest` using the job's `backtest_id`. A sweep finishes with its ranked results on the job. `get-backtest` leaves the trade list, equity curve and strategy snapshot out unless you name them in `include`.
- **Workspaces.** `save-workspaces` sends the whole document with the `revision` read from `get-workspaces`. If the Workspaces changed somewhere else in the meantime, nothing is saved and the current state and revision come back to merge into.
- **Profit and loss.** `get-account-pnl-history` and `get-account-pnl-symbols` need the user's consent to P&L sync, given in the app.
- **Watchlists.** The watchlist tools change the user's own watchlists. Built-in watchlists are listed but not changed.
- **`get-user`.** Every signed-in user can read their own account. Only an admin may pass `user_id`.

## Related

- [Tool reference](tools/reference.md) and the [generated tool list](tools/README.md)
- [AI overview](../ai/overview.md)
- [In-app assistant](../ai/in-app-assistant.md)
