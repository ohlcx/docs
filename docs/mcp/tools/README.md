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
| `run-support-agent` | Laravel AI support agent, run as a guest; it only reads (knowledge base tools and the ohlcx.com page reader); triggers LLM. |
| `run-trading-agent` | Laravel AI trading assistant with the signed-in user's own tools; not read-only (can change the user's settings and preferences; for an admin, a user's credits and billing package); authenticated MCP only; triggers LLM. |
| `get-user` | Current user; admins may pass user_id for another user. |
| `search-knowledge-base` | Filter by area, q; uses DB. Available to all. Bounds: `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
| `get-knowledge-base-article` | Article by slug; uses DB. Available to all. |
| `list-accounts` | User's brokerage accounts: id, masked number, type, balances; never the broker's key or a full number. Bounds: the API lists at most 100; `limit` 1-100. |
| `list-strategy-accounts` | Linked accounts as strategies can route orders to them: id, masked label, routable or the reason not. Pro only. Read-only. |
| `set-strategy-accounts` | Choose which linked accounts receive a strategy's orders (selected ids, or all). Pro only. Decides where orders go: confirm first. |
| `get-account-balance` | Daily balance history of one account: its id, masked number and history; never the broker's key. Bounds: the API keeps the 360 most recent rows; `limit` 1-360. |
| `get-account-growth` | Account growth by account_id (the id list-accounts gives, as a number or digits); never the broker's key or a full number. Bounds: answers {account_id, account, growth}; the API reads the 120 most recent rows; `limit` 1-120. |
| `get-account-pnl` | Account PnL by account_id (the id list-accounts gives, as a number or digits); never the broker's key or a full number. Bounds: answers {account_id, account, pnl}; the API reads the 120 most recent rows; `limit` 1-120. |
| `get-accounts-balances` | Daily balance history of every linked account, one entry per account with its id and masked number; optional days (default 30). Bounds: `days` 1-365 (default 30), `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
| `get-account-pnl-history` | Realized P&L over time for an account (account_id: the id list-accounts gives); optional period or from/to. No broker key; the account number is a masked label. Bounds: `limit` 1-1000 (default 366); `more`. |
| `get-account-pnl-symbols` | Realized P&L by symbol for an account (account_id: the id list-accounts gives); optional period or from/to, symbol, underlying. No broker key; the account number is a masked label. Bounds: `symbols` largest move first, `limit` 1-200 (default 50), `offset`, `more`, `next_offset`; `round_trips` most recent first, `round_trips_limit` 1-200 (default 50), `more_round_trips`. |
| `list-account-cash-transfers` | Deposits and withdrawals of an account (account_id: the id list-accounts gives); optional period or from/to, direction, q, page, per_page. No broker key; the account number is a masked label. Bounds: `page`, `per_page` 1-50 (default 25); `meta` with `has_more`. |
| `list-orders` | Broker orders between two dates; optional account_id (the id list-accounts gives), status, max_results; account numbers are masked labels. Read-only. Bounds: `max_results` 1-500 (default 100); no pages, narrow the dates. |
| `get-order` | One broker order by account_id (the id list-accounts gives) and order_id; the account number in it is a masked label. Read-only. |
| `list-activities` | User's Activities Feed; no broker key, account numbers as masked labels. Bounds: `page`, `per_page` 1-50 (default 30); `meta` with `has_more`. |
| `log-activity` | Log activity. |
| `delete-activity` | Delete activity by id. |
| `get-analysis` | User's AI analysis data. Bounds: `page`, `per_page` 1-50 (default 10); `meta` with `has_more`. |
| `get-ai-usage` | The user's AI usage by agent and source; optional range or from/to. |
| `list-strategies` | User's strategies; optional page and per_page ask for the paged list. Bounds: the first 50 without arguments; `page` 1-100000, `per_page` 1-50 for the paged list; `meta`: current_page, last_page, per_page, total, has_more. |
| `get-strategy` | Strategy by id; its routing block as the routing tools give it (ids, masked labels, plain-words reasons). Bounds: its conditions, flags, signals and trades come at most 100 each (the API's bound). |
| `create-strategy` | Create strategy. |
| `update-strategy` | Update strategy by id. Refused while deployed: retain-strategy first. |
| `delete-strategy` | Delete strategy by id. Refused while deployed: retain-strategy first. |
| `search-strategies` | Search strategies by symbol. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-strategy-activities` | Strategy activities by strategy_id. Bounds: the API gives the latest 10; `limit` 1-10. |
| `get-strategy-conditions` | Strategy conditions by strategy_id. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `deploy-strategy` | Deploy strategy. |
| `retain-strategy` | Retain a strategy (take it out of evaluation); stop true also switches orders, trades and signals off (owner only). |
| `duplicate-strategy` | Duplicate strategy. |
| `clear-strategy-conditions-readings` | Clear condition readings for strategy. Refused while deployed: retain-strategy first. |
| `get-strategy-statistics` | One strategy's statistics; optional period, status, direction. |
| `get-strategies-statistics` | Statistics across all the user's strategies; optional period, status, direction. |
| `get-strategy-performance` | One strategy's performance; optional period, status, direction. Bounds: one row per day of the period, at most a year. |
| `get-strategies-performance` | Performance across all the user's strategies; optional period, status, direction. Bounds: one row per day of the period, at most a year. |
| `get-strategy-timeline` | Get a strategy's activity timeline: what it did, day by day, over the last days. Bounds: the most recent whole days that fit one answer (about three); `days` 1-365 (default 3), `logged_only` for more days; `returned`, `more`. |
| `list-strategy-signals` | List the signals a strategy has raised, 100 per page. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `list-strategy-trades` | List the trades a strategy has taken, 100 per page. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-strategy-flags` | List the flags a strategy's conditions have raised, 100 per page. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `set-strategy-status` | Switch a strategy on or off (owner only). On is refused while deployed (retain-strategy first); off always works. |
| `set-strategy-flag` | signals, trades or orders (or their notifications): on, off, toggle (owner only). On and toggle are refused while deployed (retain-strategy first); off always works. |
| `set-strategy-schedule` | Set the days and hours a strategy is allowed to run. Times are New York time. Refused while deployed: retain-strategy first. |
| `update-strategy-settings` | One validated section at a time; see the ohlcx://strategy-settings resource (owner only). Refused while deployed: retain-strategy first. |
| `clear-strategy-data` | Delete a strategy's signals, trades or flags (owner only). Clearing flags is refused while deployed, and signals while deployed, real and with orders on (retain-strategy first); trades never. |
| `list-signals` | User's signals. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `list-backtests` | Saved runs, newest first; optional strategy_id, page. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-backtest` | One saved run; trades, equity and strategy_snapshot only when named in include. Bounds: the parts named in `include` lose rows when the answer is over 256 KB (`truncated`, `more`); the whole run is in the app. |
| `rename-backtest` | Rename a saved backtest run. |
| `delete-backtest` | Delete a saved backtest run. This cannot be undone. |
| `run-backtest` | Server-side run; listed only when server backtests are switched on. |
| `run-backtest-sweep` | Server-side sweep over one or two settings; listed only when server backtests are switched on. |
| `list-backtest-jobs` | Server-side jobs with status and progress; listed only when server backtests are switched on. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-backtest-job` | Poll a server-side job; listed only when server backtests are switched on. |
| `cancel-backtest-job` | Cancel a waiting or running job; listed only when server backtests are switched on. |
| `list-trades` | Strategy trades; optional symbol, period, status, direction, page. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-trade` | Get one strategy trade by ID. |
| `delete-trade` | Delete a trade record; does not touch the broker. |
| `get-signal` | Get one signal by ID, with its strategy and trades. |
| `delete-signal` | Delete a signal. This cannot be undone. Refused only while its strategy is deployed, real and has orders on (retain-strategy first). |
| `set-signal-action` | like, unlike, ignore, unignore, watch or unwatch a signal. |
| `get-signal-actions` | Get how the authenticated user has marked a signal: liked, ignored, watched. |
| `get-workspaces` | The user's Workspaces document and its revision. |
| `save-workspaces` | Replace the Workspaces document against a revision; a stale revision returns the current state. |
| `list-watchlists` | The user's watchlists, the built-in ones, and the hidden built-ins. Bounds: `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
| `create-watchlist` | Create an empty watchlist for the authenticated user. Add symbols with add-watchlist-symbols. |
| `rename-watchlist` | Rename one of the authenticated user's watchlists. |
| `delete-watchlist` | Delete one of the authenticated user's watchlists and the symbols in it. This cannot be undone. |
| `add-watchlist-symbols` | Add one or more symbols to one of the authenticated user's watchlists. Symbols already in it are kept once. |
| `remove-watchlist-symbol` | Remove one symbol from one of the authenticated user's watchlists. |
| `list-markets` | Markets; optional market_id. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `list-sectors` | Sectors from proxied API; optional per_page. Bounds: `page`, `per_page` 1-100 (default 10); `meta` with `has_more`. |
| `get-sector` | Sector by sector_id (digits only). |
| `get-ticker` | Ticker by symbol or market_id. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-market-calendar` | Market calendar. |
| `get-market-balance` | Market balance; optional filters. |
| `get-sector-balance` | Sector balance; optional filters. |
| `screen-market-gaps` | Gap screen of a market; optional market_id, gap_min_percent, direction. Bounds: `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
| `screen-asset-gaps` | Gap screen of one symbol; optional timeframe, gap_min_percent, direction. Bounds: `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
| `screen-technicals` | Technical readings per symbol for a market; optional market_id, timeframe, search, page, per_page. Bounds: `page`, `per_page` 1-50 (default 20); `meta` with `has_more`. |
| `get-ticker-bars` | Price bars for a symbol; newest 200 by default, cursor paginated. Bounds: `limit` 1-1000 (default 200), `cursor` to continue. |
| `get-ticker-analysis` | Published analysis for one symbol; optional page. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `list-news` | Paginated news. Bounds: `page`, `per_page` 1-50 (default 10); `meta` with `has_more`. |
| `get-news` | News item by id. |
| `list-crypto-news` | Paginated crypto news. Bounds: `page`, `per_page` 1-50 (default 10); `meta` with `has_more`. |
| `list-popular-news` | Paginated popular news. Bounds: `page`, `per_page` 1-50 (default 10); `meta` with `has_more`. |
| `list-conditions` | All conditions. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-condition` | Condition by id. |
| `create-condition` | Create condition. Refused while the strategy is deployed: retain-strategy first. |
| `update-condition` | Update condition by id. Refused while the strategy is deployed: retain-strategy first. |
| `delete-condition` | Delete condition by id. Refused while the strategy is deployed: retain-strategy first. |
| `submit-contact-form` | Submit contact form. |
| `report-issue` | Report issue. |
| `submit-support-request` | Submit support request. |
| `list-support-tickets` | The user's support tickets; optional status. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `get-support-ticket` | Get one of the authenticated user's support tickets with its messages. Bounds: a conversation over 256 KB keeps its newest messages (`truncated`, `more`). |
| `create-support-ticket` | Open a support ticket: subject, body, optional category and priority. |
| `reply-support-ticket` | Add a message from the authenticated user to one of their support tickets. The support team is notified. Confirm the wording with the user first. |
| `get-credits` | User's credit balance. |
| `get-transaction-history` | User's billing history. Bounds: the latest 100 of each list is all the reader gives; `limit` 1-100. |
| `list-credit-holds` | Credit holds and their status, without the broker's key for an account; optional page, per_page. Read-only. Bounds: `page`, `per_page` 1-50 (default 25); `meta` with `has_more`. |
| `get-sessions` | User's sessions. Bounds: `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
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
| `discover-groups` | Trading rooms open to join; optional search. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `browse-users` | Other users to message or invite; optional search. Bounds: `page`, `offset`; `meta` with `has_more`, `next_offset`. |
| `list-invites` | User's invites. Bounds: `page`, `per_page` 1-50 (default 10); `meta` with `has_more`. |
| `send-invite` | Send invite. |
| `accept-invite` | Accept invite. |
| `respond-join-request` | Respond to join request. |
| `list-pending-join-requests` | Join requests waiting on rooms the user owns. Bounds: `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
| `send-message` | Send message in room. |
| `get-older-messages` | Older messages before message_id. Bounds: 10 at a time; `meta.has_more`. |
| `delete-message` | Delete message. |
| `get-sidebar-conversations` | Sidebar conversation list. Bounds: `limit` 1-200 (default 50), `offset`; `more`, `next_offset`. |
| `get-unread-messages` | Unread messages by conversation. Bounds: the API gives the latest 50; `limit` 1-50. |

### Admin-only tools (13)

| Tool | Notes |
|------|-------|
| `list-users` | Search, pagination. Bounds: `per_page` 1-100 (default 20), `page`; `meta` with `has_more`. |
| `set-user-admin` | Set/clear is_admin. |
| `update-user` | Update name, email, is_admin, email_verified. |
| `add-user` | Create user. |
| `delete-user` | Delete by ID; cannot delete self. |
| `create-knowledge-base-article` | Create KB article. |
| `update-knowledge-base-article` | Update KB article by id. |
| `delete-knowledge-base-article` | Delete KB article by id. |
| `get-user-billing` | User billing (admin); no broker key, account numbers as masked labels. Bounds: held to the 256 KB budget. |
| `adjust-user-billing` | Adjust user billing (admin). |
| `set-user-billing-package` | Set user billing package (admin). |
| `block-unblock-user` | Block/unblock user (admin). |
| `change-user-role` | Change user role (admin). |

