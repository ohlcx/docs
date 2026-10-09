# OHLCX MCP tool catalog

> Auto-generated from `src/Mcp/descriptors/index.json`. Do not edit by hand; run `php scripts/generate-mcp-tools-readme.php` or `scripts/sync-public-docs.sh`.

## Server

| Field | Value |
|-------|-------|
| Name | OHLCX |
| Version | 1.1.0 |
| Web transport | `/mcp/ohlcx` |
| Stdio | `php artisan mcp:start ohlcx` |
| Auth | Sanctum (web); stdio may run unauthenticated. |

OHLCX MCP server: trading platform tools for strategies, backtests, signals, trades, workspaces, watchlists, screeners, accounts and orders (read-only), support tickets, markets, sectors, news, conditions, knowledge base, and user management.

## Prompts (3)

| Name | Description |
|------|-------------|
| `user-info` | Current user summary (authenticated MCP session only) |
| `trading-terminology` | TSP, OCO, TRIM, order types |
| `support-knowledge-base` | Answer support questions using KB |

## Resources (1)

| Name | URI | Description |
|------|-----|-------------|
| `strategy-settings` | `ohlcx://strategy-settings` | Every strategy setting by section, with its allowed values |

## Tools (147)

### User and guest tools (134)

| Tool | Notes |
|------|-------|
| `ping` | Health check; no args. |
| `run-support-agent` | Laravel AI support agent (KB tools only); triggers LLM. |
| `run-trading-agent` | Laravel AI trading assistant; authenticated MCP only; triggers LLM. |
| `get-user` | Current user; admins may pass user_id for another user. |
| `search-knowledge-base` | Filter by area, q; uses DB. Available to all. |
| `get-knowledge-base-article` | Article by slug; uses DB. Available to all. |
| `list-accounts` | User's brokerage accounts: id, masked number, type, balances; never the broker's key or a full number. |
| `list-strategy-accounts` | Linked accounts as strategies can route orders to them: id, masked label, routable or the reason not. Pro only. Read-only. |
| `set-strategy-accounts` | Choose which linked accounts receive a strategy's orders (selected ids, or all). Pro only. Decides where orders go: confirm first. |
| `get-account-balance` | Daily balance history of one account: its id, masked number and history; never the broker's key. |
| `get-account-growth` | Account growth by account_id. |
| `get-account-pnl` | Account PnL by account_id. |
| `get-accounts-balances` | Daily balance history of every linked account, one entry per account with its id and masked number; optional days (default 30). |
| `get-account-pnl-history` | Realized P&L over time for an account; optional period or from/to. |
| `get-account-pnl-symbols` | Realized P&L by symbol for an account; optional period or from/to, symbol, underlying. |
| `list-account-cash-transfers` | Deposits and withdrawals of an account; optional period or from/to, direction, q, page, per_page. |
| `list-orders` | Broker orders between two dates; optional account_id, status, max_results. Read-only. |
| `get-order` | One broker order by account_id and order_id. Read-only. |
| `list-activities` | User's activity feed. |
| `log-activity` | Log activity. |
| `delete-activity` | Delete activity by id. |
| `get-analysis` | User's AI analysis data. |
| `get-ai-usage` | The user's AI usage by agent and source; optional range or from/to. |
| `list-strategies` | User's strategies; optional page and per_page ask for the paged list. |
| `get-strategy` | Strategy by id. |
| `create-strategy` | Create strategy. |
| `update-strategy` | Update strategy by id. Refused while deployed: retain-strategy first. |
| `delete-strategy` | Delete strategy by id. Refused while deployed: retain-strategy first. |
| `search-strategies` | Search strategies by symbol. |
| `get-strategy-activities` | Strategy activities by strategy_id. |
| `get-strategy-conditions` | Strategy conditions by strategy_id. |
| `deploy-strategy` | Deploy strategy. |
| `retain-strategy` | Retain a strategy (take it out of evaluation); stop true also switches orders, trades and signals off (owner only). |
| `duplicate-strategy` | Duplicate strategy. |
| `clear-strategy-conditions-readings` | Clear condition readings for strategy. Refused while deployed: retain-strategy first. |
| `get-strategy-statistics` | One strategy's statistics; optional period, status, direction. |
| `get-strategies-statistics` | Statistics across all the user's strategies; optional period, status, direction. |
| `get-strategy-performance` | One strategy's performance; optional period, status, direction. |
| `get-strategies-performance` | Performance across all the user's strategies; optional period, status, direction. |
| `get-strategy-timeline` | Get a strategy's activity timeline: what it did, day by day, over the last days. |
| `list-strategy-signals` | List the signals a strategy has raised, 100 per page. |
| `list-strategy-trades` | List the trades a strategy has taken, 100 per page. |
| `get-strategy-flags` | List the flags a strategy's conditions have raised, 100 per page. |
| `set-strategy-status` | Switch a strategy on or off (owner only). On is refused while deployed (retain-strategy first); off always works. |
| `set-strategy-flag` | signals, trades or orders (or their notifications): on, off, toggle (owner only). On and toggle are refused while deployed (retain-strategy first); off always works. |
| `set-strategy-schedule` | Set the days and hours a strategy is allowed to run. Times are New York time. Refused while deployed: retain-strategy first. |
| `update-strategy-settings` | One validated section at a time; see the ohlcx://strategy-settings resource (owner only). Refused while deployed: retain-strategy first. |
| `clear-strategy-data` | Delete a strategy's signals, trades or flags (owner only). Clearing flags is refused while deployed, and signals while deployed, real and with orders on (retain-strategy first); trades never. |
| `list-signals` | User's signals. |
| `list-backtests` | Saved runs, newest first; optional strategy_id, page. |
| `get-backtest` | One saved run; trades, equity and strategy_snapshot only when named in include. |
| `rename-backtest` | Rename a saved backtest run. |
| `delete-backtest` | Delete a saved backtest run. This cannot be undone. |
| `run-backtest` | Server-side run; listed only when server backtests are switched on. |
| `run-backtest-sweep` | Server-side sweep over one or two settings; listed only when server backtests are switched on. |
| `list-backtest-jobs` | Server-side jobs with status and progress; listed only when server backtests are switched on. |
| `get-backtest-job` | Poll a server-side job; listed only when server backtests are switched on. |
| `cancel-backtest-job` | Cancel a waiting or running job; listed only when server backtests are switched on. |
| `list-trades` | Strategy trades; optional symbol, period, status, direction, page. |
| `get-trade` | Get one strategy trade by ID. |
| `delete-trade` | Delete a trade record; does not touch the broker. |
| `get-signal` | Get one signal by ID, with its strategy and trades. |
| `delete-signal` | Delete a signal. This cannot be undone. Refused only while its strategy is deployed, real and has orders on (retain-strategy first). |
| `set-signal-action` | like, unlike, ignore, unignore, watch or unwatch a signal. |
| `get-signal-actions` | Get how the authenticated user has marked a signal: liked, ignored, watched. |
| `get-workspaces` | The user's Workspaces document and its revision. |
| `save-workspaces` | Replace the Workspaces document against a revision; a stale revision returns the current state. |
| `list-watchlists` | The user's watchlists, the built-in ones, and the hidden built-ins. |
| `create-watchlist` | Create an empty watchlist for the authenticated user. Add symbols with add-watchlist-symbols. |
| `rename-watchlist` | Rename one of the authenticated user's watchlists. |
| `delete-watchlist` | Delete one of the authenticated user's watchlists and the symbols in it. This cannot be undone. |
| `add-watchlist-symbols` | Add one or more symbols to one of the authenticated user's watchlists. Symbols already in it are kept once. |
| `remove-watchlist-symbol` | Remove one symbol from one of the authenticated user's watchlists. |
| `list-markets` | Markets; optional market_id. |
| `list-sectors` | Sectors from proxied API; optional per_page. |
| `get-sector` | Sector by sector_id. |
| `get-ticker` | Ticker by symbol or market_id. |
| `get-market-calendar` | Market calendar. |
| `get-market-balance` | Market balance; optional filters. |
| `get-sector-balance` | Sector balance; optional filters. |
| `screen-market-gaps` | Gap screen of a market; optional market_id, gap_min_percent, direction. |
| `screen-asset-gaps` | Gap screen of one symbol; optional timeframe, gap_min_percent, direction. |
| `screen-technicals` | Technical readings per symbol for a market; optional market_id, timeframe, search, page, per_page. |
| `get-ticker-bars` | Price bars for a symbol; newest 200 by default, cursor paginated. |
| `get-ticker-analysis` | Published analysis for one symbol; optional page. |
| `list-news` | Paginated news. |
| `get-news` | News item by id. |
| `list-crypto-news` | Paginated crypto news. |
| `list-popular-news` | Paginated popular news. |
| `list-conditions` | All conditions. |
| `get-condition` | Condition by id. |
| `create-condition` | Create condition. Refused while the strategy is deployed: retain-strategy first. |
| `update-condition` | Update condition by id. Refused while the strategy is deployed: retain-strategy first. |
| `delete-condition` | Delete condition by id. Refused while the strategy is deployed: retain-strategy first. |
| `submit-contact-form` | Submit contact form. |
| `report-issue` | Report issue. |
| `submit-support-request` | Submit support request. |
| `list-support-tickets` | The user's support tickets; optional status. |
| `get-support-ticket` | Get one of the authenticated user's support tickets with its messages. |
| `create-support-ticket` | Open a support ticket: subject, body, optional category and priority. |
| `reply-support-ticket` | Add a message from the authenticated user to one of their support tickets. The support team is notified. Confirm the wording with the user first. |
| `get-credits` | User's credit balance. |
| `get-transaction-history` | User's billing history. |
| `list-credit-holds` | Credit holds and their status; optional page, per_page. Read-only. |
| `get-sessions` | User's sessions. |
| `update-profile` | Update profile. |
| `update-password` | Update password. |
| `delete-profile-photo` | Delete profile photo. |
| `get-onboarding` | User onboarding state. |
| `complete-onboarding` | Submit onboarding. |
| `get-preferences` | User preferences. |
| `update-preferences` | Update preferences. |
| `get-settings` | User settings. |
| `save-settings` | Save settings. |
| `get-group` | Trading room group by id. |
| `create-group` | Create group. |
| `update-group` | Update group. |
| `delete-group` | Delete group. |
| `invite-to-group` | Invite to group. |
| `join-group` | Join group. |
| `leave-group` | Leave group. |
| `get-group-status` | Group status. |
| `discover-groups` | Trading rooms open to join; optional search. |
| `browse-users` | Other users to message or invite; optional search. |
| `list-invites` | User's invites. |
| `send-invite` | Send invite. |
| `accept-invite` | Accept invite. |
| `respond-join-request` | Respond to join request. |
| `list-pending-join-requests` | Join requests waiting on rooms the user owns. |
| `send-message` | Send message in room. |
| `get-older-messages` | Older messages before message_id. |
| `delete-message` | Delete message. |
| `get-sidebar-conversations` | Sidebar conversation list. |
| `get-unread-messages` | Unread messages by conversation. |

### Admin-only tools (13)

| Tool | Notes |
|------|-------|
| `list-users` | Search, pagination. |
| `set-user-admin` | Set/clear is_admin. |
| `update-user` | Update name, email, is_admin, email_verified. |
| `add-user` | Create user. |
| `delete-user` | Delete by ID; cannot delete self. |
| `create-knowledge-base-article` | Create KB article. |
| `update-knowledge-base-article` | Update KB article by id. |
| `delete-knowledge-base-article` | Delete KB article by id. |
| `get-user-billing` | User billing (admin). |
| `adjust-user-billing` | Adjust user billing (admin). |
| `set-user-billing-package` | Set user billing package (admin). |
| `block-unblock-user` | Block/unblock user (admin). |
| `change-user-role` | Change user role (admin). |

