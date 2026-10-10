# AI agents and their tools

OHLCX has three AI agents behind the in-app assistant. Each has a fixed list of tools, decided on the server by who is asking and which edition is running. This page lists them.

The agents are separate from the MCP server. The MCP server has 147 tools for outside clients; the agents have 45 tools of their own, with different names (`snake_case`) and different output.

## Agents

| Agent | Used by | Sign-in |
| ----- | ------- | ------- |
| Support | The drawer's "AI Support Assistant" mode; the MCP tool `run-support-agent` | optional |
| Trading | The drawer's "AI Trading Assistant" mode; the MCP tool `run-trading-agent` | required |
| Unified | The drawer's "AI Assistant" mode and the Ask OHLCX panels | optional |

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
| Strategy insight | `get_trading_strategy`, `get_trading_strategy_statistics`, `get_trading_strategy_performance` |
| Routing reader | `get_strategy_routing` |
| Markets | `list_markets`, `get_market`, `list_tickers`, `get_ticker`, `list_sectors`, `list_sector_snapshots`, `get_sector`, `get_market_calendar`, `get_market_balance`, `get_sector_balance` |
| Saved runs | `list_backtest_runs`, `get_backtest_run` |
| Proposing | `propose_backtest_change`, `propose_backtest_sweep`, `propose_strategy_draft`, `propose_strategy_accounts` |
| Admin billing | `get_user_billing`, `adjust_user_billing`, `set_user_billing_package` |

45 tool names in all.

## Which agent has which group

| Group | Support | Trading | Unified | Condition |
| ----- | ------- | ------- | ------- | --------- |
| Knowledge | yes | yes | yes | none |
| Billing | yes | yes | yes | signed in |
| Profile | yes | yes | yes | signed in |
| Feed | yes | yes | yes | signed in |
| Community | yes | yes | yes | signed in |
| Accounts | no | yes | yes | signed in |
| Strategy insight | no | no | yes | signed in |
| Routing reader | no | yes | yes | signed in, on OHLCX Pro |
| Markets | no | yes | yes | signed in, on OHLCX Pro |
| Saved runs | no | no | yes | signed in, on OHLCX Pro, with Ask OHLCX switched on |
| Proposing | no | no | yes | as Saved runs, and only on the page each one belongs to |
| Admin billing | yes | yes | yes | signed in as an admin |

### Tool counts

| Agent | Guest | Signed in, Light | Signed in, Pro |
| ----- | ----- | ---------------- | -------------- |
| Support | 3 | 21 | 21 |
| Trading | not available | 22 | 33 |
| Unified | 3 | 25 | 36, or 38 with Ask OHLCX on |

Pro counts are for an app that reaches the strategies data as the signed-in user, which is how Pro runs; they include `get_strategy_routing`. An admin has three more tools in every column. On a page that offers one, the unified agent has one or two proposing tools more.

Why the lines are drawn there:

- A guest gets the knowledge group only, because everything else answers with one user's data.
- Support answers product questions, so it has no accounts, strategy detail or markets.
- Markets need the market data that only Pro has.
- The routing reader and the accounts card need the user's own strategies and accounts, which only Pro reads as that user.
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
| `list_brokerage_accounts` | Linked accounts, up to 25: a masked label, type, status and four balance figures. Never a full account number. |
| `get_trading_strategy` | One strategy with its counts; conditions, signals and trades only when asked for, up to 20 each. |
| `get_trading_strategy_statistics` | Trade statistics for a period, for one strategy or all. |
| `get_trading_strategy_performance` | Profit and loss day by day, the latest 31 days of the period. |
| `get_strategy_routing` | Which linked accounts a strategy's orders go to, as masked labels. Read-only. |

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

No agent has a tool to create, change, deploy or delete a strategy, to switch a strategy or its orders on, to run a backtest, to place an order, or to choose a strategy's order accounts. The proposing tools only offer a card; the user presses its button.

## MCP bridge tools

Two MCP tools run an agent and return its answer as plain text. Both call the configured language model.

| MCP tool | Listed for | Runs |
| -------- | ---------- | ---- |
| `run-support-agent` | everyone | The Support agent as a guest: the knowledge group only. It only reads, and is marked read-only. |
| `run-trading-agent` | a signed-in MCP session | The Trading agent for that user, with every tool of the Trading column above. It can change the user's settings and preferences (and, for an admin, a user's credits and billing package), so it is not marked read-only. |

Both take one argument, `message`, of at most 16,000 characters.

```json
{ "message": "Summarize my linked accounts and strategies." }
```

Prefer the MCP data tools when you want a deterministic result; use a bridge tool when you want the agent's reasoning over several tools.

## Configuration and cost

- Model providers and keys are configured in the host application (for example `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- Every agent request is recorded as AI usage. A user can read their own with the MCP tool `get-ai-usage`.
