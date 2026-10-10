# AI agents and their tools

OHLCX has three AI agents behind the in-app assistant. Each has a fixed list of tools, decided on the server by who is asking and which edition is running. This page lists them.

The agents are separate from the MCP server. The MCP server has 147 tools for outside clients; the agents have 57 tools of their own, with different names (`snake_case`) and different output.

## Agents

| Agent | Used by | Sign-in |
| ----- | ------- | ------- |
| Support | The drawer's "AI Support Assistant" mode; the MCP tool `run-support-agent` | optional |
| Trading | The drawer's "AI Trading Assistant" mode; the MCP tool `run-trading-agent` | required |
| Unified | The drawer's "AI Assistant" mode and the Ask OHLCX panels | optional |

Each agent may take at most 12 steps in one turn, and a single request to the model may take 120 seconds. If a turn fails or hits a limit, the user reads one fixed sentence and the cause goes to the server log. The codes and sentences are in [`in-app-assistant.md`](in-app-assistant.md#a-failed-turn).

A guest has three tools and nothing else: `search_knowledge_base_articles`, `get_knowledge_base_article_by_slug` and `fetch_ohlcx_webpage`.

## Tool groups

| Group | Tools |
| ----- | ----- |
| Knowledge | `search_knowledge_base_articles`, `get_knowledge_base_article_by_slug`, `fetch_ohlcx_webpage` |
| Billing | `get_available_credits`, `get_billing_summary`, `get_credit_holds`, `get_transaction_history` |
| Profile | `get_user_settings`, `get_user_preferences`, `update_user_settings`, `update_user_preferences` |
| Feed | `list_activities_feed`, `list_trading_strategies`, `list_signals`, `get_analysis`, `list_news`, `get_strategy_activities` |
| Community | `list_community_channels`, `get_community_messages`, `search_community_users`, `discover_community_groups` |
| Accounts | `list_brokerage_accounts` |
| Screener | `screen_market_gaps`, `screen_symbol_gaps`, `screen_technicals` |
| Watchlists | `list_watchlists`, `get_watchlist` |
| Account results | `get_account_pnl`, `get_account_pnl_by_symbol`, `get_account_growth` |
| Strategy insight | `get_trading_strategy`, `get_trading_strategy_statistics`, `get_trading_strategy_performance` |
| Routing reader | `get_strategy_routing` |
| Markets | `list_markets`, `get_market`, `list_tickers`, `get_ticker`, `list_sectors`, `list_sector_snapshots`, `get_sector`, `get_market_calendar`, `get_market_balance`, `get_sector_balance` |
| Saved runs | `list_backtest_runs`, `get_backtest_run`, `get_backtest_run_trades` |
| Proposing | `propose_backtest_change`, `propose_backtest_sweep`, `propose_strategy_draft`, `propose_strategy_accounts` |
| Showing | `show_backtest_trades`, `show_backtest_breakdown`, `show_backtest_stats` |
| Admin billing | `get_user_billing`, `adjust_user_billing`, `set_user_billing_package` |

57 tool names in all.

## Which agent has which group

| Group | Support | Trading | Unified | Condition |
| ----- | ------- | ------- | ------- | --------- |
| Knowledge | yes | yes | yes | none |
| Billing | yes | yes | yes | signed in |
| Profile | yes | yes | yes | signed in |
| Feed | yes | yes | yes | signed in |
| Community | yes | yes | yes | signed in |
| Accounts | no | yes | yes | signed in |
| Screener | no | yes | yes | signed in |
| Watchlists | no | yes | yes | signed in |
| Account results | no | yes | yes | signed in |
| Strategy insight | no | no | yes | signed in |
| Routing reader | no | yes | yes | signed in, on OHLCX Pro |
| Markets | no | yes | yes | signed in, on OHLCX Pro |
| Saved runs | no | no | yes | signed in, on OHLCX Pro, with Ask OHLCX switched on. `get_backtest_run_trades` only where the app reaches the strategies data as the signed-in user |
| Proposing | no | no | yes | as Saved runs, and only on the page each one belongs to |
| Showing | no | no | yes | as Saved runs, and only while a backtest run is open on a page that says it can draw that tool's card |
| Admin billing | yes | yes | yes | signed in as an admin |

### Tool counts

| Agent | Guest | Signed in, Light | Signed in, Pro |
| ----- | ----- | ---------------- | -------------- |
| Support | 3 | 21 | 21 |
| Trading | not available | 30 | 41 |
| Unified | 3 | 33 | 44, or 47 with Ask OHLCX on |

Pro counts are for an app that reaches the strategies data as the signed-in user, which is how Pro runs; they include `get_strategy_routing` and, with Ask OHLCX on, `get_backtest_run_trades`. An admin has three more tools in every column. On a page that offers one, the unified agent has one or two proposing tools more. On a backtest run it has one more tool for each card the page says it can draw: `show_backtest_trades`, `show_backtest_breakdown`, `show_backtest_stats`.

Why the lines are drawn there:

- A guest gets the knowledge group only, because everything else answers with one user's data.
- Support answers product questions, so it has no accounts, strategy detail or markets.
- Markets need the market data that only Pro has.
- The routing reader and the accounts card need the user's own strategies and accounts, which only Pro reads as that user.
- The three Screener tools read market data, which is the same for everyone, so they are on Light too.
- Watchlists and account results are read from the app itself, as the signed-in user, on Light and on Pro. Nothing of one user's goes through the relay that Light uses for the strategies data.
- Saved runs and the proposing tools are Ask OHLCX, one feature behind one switch.

## What each tool returns

Every tool returns a bounded result. A list says how many rows it shows and whether more exist.

### Knowledge

| Tool | Returns |
| ---- | ------- |
| `search_knowledge_base_articles` | Up to 20 articles with a preview of each. |
| `get_knowledge_base_article_by_slug` | One article, cut at 48,000 bytes. |
| `fetch_ohlcx_webpage` | The readable text of a page of the OHLCX website. No other site is accepted. |

### The user's data

| Tool | Returns |
| ---- | ------- |
| `get_available_credits` | The credit balance. |
| `get_billing_summary` | Balance, packages and billable features, up to 25 of each. |
| `get_credit_holds` | Credit holds, up to 25 a page. |
| `get_transaction_history` | Purchases and feature usage, up to 25 of each. |
| `get_user_settings`, `get_user_preferences` | The user's Settings toggles and Preferences. |
| `update_user_settings`, `update_user_preferences` | **Changes** one of the user's own Settings toggles or Preferences. The assistant is told to confirm first. |
| `list_activities_feed` | The Activities Feed, up to 25 rows. |
| `list_trading_strategies` | Strategies as short rows, 25 to a page. |
| `list_signals` | Signals as short rows, up to 25. |
| `get_analysis` | The Analysis feed, up to 25 rows. |
| `list_news` | Headlines, up to 25 rows. |
| `get_strategy_activities` | One strategy's execution log, up to 25 rows. |
| `list_community_channels` | Groups and direct messages, up to 50 of each. |
| `get_community_messages` | One conversation's messages, up to 20, each clipped. Senders by name, never by email. |
| `search_community_users` | Users by name, 20 a page. An email is never searched or returned. |
| `discover_community_groups` | Groups the user could join, 10 a page. |
| `list_brokerage_accounts` | Linked accounts, up to 25: a masked label, type, status and four balance figures. Never a full account number. With "Hide Account Balance" on, no balance figure (see below). |
| `get_trading_strategy` | One strategy with its counts; conditions, signals and trades only when asked for, up to 20 each. |
| `get_trading_strategy_statistics` | Trade statistics for a period, for one strategy or all. |
| `get_trading_strategy_performance` | Profit and loss day by day, the latest 31 days of the period. |
| `get_strategy_routing` | Which linked accounts a strategy's orders go to, as masked labels. Read-only. |

### Screener, watchlists and account results

| Tool | Returns |
| ---- | ------- |
| `screen_market_gaps` | The Screener's market screen: symbols that gapped, largest first, up to 25, with the statistics of every gap found. Up, down or both, and a smallest gap in percent. |
| `screen_symbol_gaps` | The Screener's symbol screen: one symbol's gaps in its latest 250 bars on a timeframe, newest first, up to 25, and how each played out. The bars are not returned. |
| `screen_technicals` | The Screener's technical screen: 10 symbols a page of one market on a timeframe, each with a rating, the count of indicators that buy, sell or are neutral, its trend, RSI and any candlestick pattern. A text search reads one symbol. |
| `list_watchlists` | The user's own watchlists first, then the built-in ones they have not hidden, up to 50: name, number of symbols, and whether the list is built in. |
| `get_watchlist` | One watchlist's symbols in the list's order, up to 100 an answer, with a point to read on from. Symbols only, no prices. |
| `get_account_pnl` | The realized profit and loss of one linked account for a period: totals for the whole period and the latest 31 rows, by day, week or month. It says where the account's sync stands. |
| `get_account_pnl_by_symbol` | The same by underlying symbol: totals for every symbol and the 25 that moved most, winners and losers alike. |
| `get_account_growth` | The account's balance over time: one change from the first balance to the last, and the latest 60 points, one for each hour of a day. A balance also moves with deposits and withdrawals, so this is not profit. |

All eight only read. A result says how many rows it shows, how many there are and whether more exist.

- The Screener tools take a market by its id; left out, the market is US stocks for the two gap screens and ETFs for the technical screen. The result names the market it used. The ids of other markets come from `list_markets`, which only OHLCX Pro has.
- The two P&L tools take `period` (the last 30 days by default, or a week, quarter or year, to date, or last year) or `custom` with two dates at most 731 days apart. Dates beside any other period are not used, and the result says so. A result for a week or month may begin or end with part of one.
- An account is named by its id, as `list_brokerage_accounts` gives it, and only one of the user's own is accepted. Left out, it is the user's only account; with several, the tool refuses until one is named. Every result names the account by its masked label.
- If an account has never synced, or its sync failed, the P&L result says so, so that zeros are not read as "nothing was made". If the user has not allowed Portfolio Performance in the app, the tool says that and reads nothing.

#### Hide Account Balance

The Preferences page has a toggle named "Hide Account Balance", off by default. While it is on, `list_brokerage_accounts`, `get_account_pnl`, `get_account_pnl_by_symbol` and `get_account_growth` leave every amount of money out of what they return:

- Balances and buying power from the accounts list. Profit and loss, gross profit and loss, fees and the daily average from the P&L results, in the totals, in the best and worst day and in every row. The start and end balance from the growth result.
- Percentages, counts, win rates and dates stay.
- The result says `balances_hidden` is true and carries a fixed note telling the assistant to give percentages and counts only, and not to estimate or ask for the amounts. Every result of these four tools has `balances_hidden`, true or false.
- If the user's preferences cannot be read, the result is treated as hidden. If nothing is stored, the toggle is at its default, off.

So neither the assistant's text nor a card drawn from the result can show what the user chose to hide. No other assistant tool returns a linked account's balances or realized results. A strategy's own figures (its statistics and performance) are not an account's, and this toggle does not hide them. The MCP server's own account tools (`list-accounts`, `get-account-balance`, `get-accounts-balances`, `get-account-growth`, `get-account-pnl`, `get-account-pnl-history`, `get-account-pnl-symbols`, `list-account-cash-transfers`) do not read this preference and return the figures. The Trading agent reached through `run-trading-agent` does honour it.

### Markets (OHLCX Pro)

| Tool | Returns |
| ---- | ------- |
| `list_markets`, `get_market` | Markets (up to 25); one market with its first 50 symbols. |
| `list_tickers`, `get_ticker` | Tickers (up to 25); one ticker. |
| `list_sectors`, `list_sector_snapshots`, `get_sector` | Sectors (up to 50); the latest snapshot of each; one sector with its first 50 symbols. |
| `get_market_calendar` | The year's market-day counts. |
| `get_market_balance`, `get_sector_balance` | The latest 26 points of a balance series. |

### Ask OHLCX

| Tool | Returns |
| ---- | ------- |
| `list_backtest_runs` | The user's saved backtest runs, newest first, up to 25. |
| `get_backtest_run` | One saved run: metrics, settings, and trades grouped by hour, weekday, exit kind and side. |
| `get_backtest_run_trades` | Single trades of one saved run: filtered, sorted, at most 50 rows, with the totals of every match. |
| `show_backtest_trades` | Shows trades of the open run as a card, drawn by the page from the trades it holds. Reads nothing and returns no trade. |
| `show_backtest_breakdown` | Shows how the trades of the open run split by entry hour, weekday, exit kind, side, calls or puts, or month, as a card. Reads nothing and returns no figure. |
| `show_backtest_stats` | Shows up to six headline figures of the open run as tiles. Reads nothing and returns no figure. |
| `propose_backtest_change` | A card: one change to test, with a "Run as what-if" button. Runs nothing. |
| `propose_backtest_sweep` | A card: one sweep, with a "Run this sweep" button. Runs nothing. |
| `propose_strategy_draft` | A card: one draft strategy, with a "Create this strategy" button. Creates nothing. |
| `propose_strategy_accounts` | A card: one change of a strategy's order accounts, with a "Set these accounts" button. Changes nothing. |

How a card works is in [`in-app-assistant.md`](in-app-assistant.md).

### Admin only

| Tool | Returns |
| ---- | ------- |
| `get_user_billing` | Another user's billing: lists of up to 25. |
| `adjust_user_billing` | **Changes** a user's credits. |
| `set_user_billing_package` | **Changes** a user's billing package. |

## What the agents cannot do

No agent has a tool to create, change, deploy or delete a strategy, to switch a strategy or its orders on, to run a backtest, to place an order, or to choose a strategy's order accounts. The proposing tools only offer a card; the user presses its button. The prompt of each agent tells it the same: it says it cannot create or change a strategy or run a backtest itself, and points to the page or the card that can.

Nor can any agent create, rename or change a watchlist, save a screener, or start a profit and loss sync.

Some things it cannot read at all:

- **Saved screeners.** None exist. The Screener page is three fixed screens, each with a few filters, and the assistant has one tool for each. There is no list of screeners and no screener definition to read.
- **Prices in a watchlist.** A watchlist holds symbols and nothing else. A price is a separate call for each symbol, and `get_ticker` makes it only on OHLCX Pro.
- **Single closed trades of an account** (round trips), **cash transfers** (deposits and withdrawals), and the state of a **profit and loss sync** beyond the status word that `get_account_pnl` returns. The MCP server has tools for the first two.
- **Any amount of money**, while "Hide Account Balance" is on, as described above.

## MCP bridge tools

Two MCP tools run an agent and return its answer as plain text. Both call the configured language model.

| MCP tool | Listed for | Runs |
| -------- | ---------- | ---- |
| `run-support-agent` | everyone | The Support agent as a guest: the knowledge group only. It only reads, and is marked read-only. |
| `run-trading-agent` | a signed-in MCP session | The Trading agent for that user, with every tool of the Trading column above. That includes the Screener screens, watchlists and the realized results and balance over time of the user's linked accounts. It can change the user's settings and preferences (and, for an admin, a user's credits and billing package), so it is not marked read-only. |

Both take one argument, `message`, of at most 16,000 characters. They run the same agents, so the same 12 steps and 120 seconds apply.

```json
{ "message": "Summarize my linked accounts and strategies." }
```

Prefer the MCP data tools when you want a deterministic result; use a bridge tool when you want the agent's reasoning over several tools.

## Configuration and cost

- Model providers and keys are configured in the host application (for example `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- Every agent request is recorded as AI usage. A user can read their own with the MCP tool `get-ai-usage`.
