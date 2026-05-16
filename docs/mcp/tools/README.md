# OHLCX MCP tool catalog

> Auto-generated from `src/Mcp/descriptors/index.json`. Do not edit by hand; run `php scripts/generate-mcp-tools-readme.php` or `scripts/sync-public-docs.sh`.

## Server

| Field | Value |
|-------|-------|
| Name | OHLCX |
| Version | 1.0.0 |
| Web transport | `/mcp/ohlcx` |
| Stdio | `php artisan mcp:start ohlcx` |
| Auth | Sanctum (web); stdio may run unauthenticated. |

OHLCX MCP server: trading platform tools for strategies, signals, markets, sectors, news, conditions, knowledge base, and user management.

## Prompts (3)

| Name | Description |
|------|-------------|
| `user-info` | Current user summary (authenticated MCP session only) |
| `trading-terminology` | TSP, OCO, TRIM, order types |
| `support-knowledge-base` | Answer support questions using KB |

## Tools (86)

### User and guest tools (72)

| Tool | Notes |
|------|-------|
| `ping` | Health check; no args. |
| `run-support-agent` | Laravel AI support agent (KB tools only); triggers LLM. |
| `run-trading-agent` | Laravel AI trading assistant; authenticated MCP only; triggers LLM. |
| `search-knowledge-base` | Filter by area, q; uses DB. Available to all. |
| `get-knowledge-base-article` | Article by slug; uses DB. Available to all. |
| `list-accounts` | User's brokerage accounts. |
| `get-account-balance` | Account balance by account_id. |
| `get-account-growth` | Account growth by account_id. |
| `get-account-pnl` | Account PnL by account_id. |
| `list-activities` | User's activity feed. |
| `log-activity` | Log activity. |
| `delete-activity` | Delete activity by id. |
| `get-analysis` | User's AI analysis data. |
| `list-strategies` | User's strategies. |
| `get-strategy` | Strategy by id. |
| `create-strategy` | Create strategy. |
| `update-strategy` | Update strategy by id. |
| `delete-strategy` | Delete strategy by id. |
| `search-strategies` | Search strategies by symbol. |
| `get-strategy-activities` | Strategy activities by strategy_id. |
| `get-strategy-conditions` | Strategy conditions by strategy_id. |
| `deploy-strategy` | Deploy strategy. |
| `duplicate-strategy` | Duplicate strategy. |
| `clear-strategy-conditions-readings` | Clear condition readings for strategy. |
| `list-signals` | User's signals. |
| `list-markets` | Markets; optional market_id. |
| `list-sectors` | Sectors from proxied API; optional per_page. |
| `get-sector` | Sector by sector_id. |
| `get-ticker` | Ticker by symbol or market_id. |
| `get-market-calendar` | Market calendar. |
| `get-market-balance` | Market balance; optional filters. |
| `get-sector-balance` | Sector balance; optional filters. |
| `list-news` | Paginated news. |
| `get-news` | News item by id. |
| `list-crypto-news` | Paginated crypto news. |
| `list-popular-news` | Paginated popular news. |
| `list-conditions` | All conditions. |
| `get-condition` | Condition by id. |
| `create-condition` | Create condition. |
| `update-condition` | Update condition by id. |
| `delete-condition` | Delete condition by id. |
| `submit-contact-form` | Submit contact form. |
| `report-issue` | Report issue. |
| `submit-support-request` | Submit support request. |
| `get-credits` | User's credit balance. |
| `get-transaction-history` | User's billing history. |
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
| `list-invites` | User's invites. |
| `send-invite` | Send invite. |
| `accept-invite` | Accept invite. |
| `respond-join-request` | Respond to join request. |
| `send-message` | Send message in room. |
| `get-older-messages` | Older messages before message_id. |
| `delete-message` | Delete message. |
| `get-sidebar-conversations` | Sidebar conversation list. |

### Admin-only tools (14)

| Tool | Notes |
|------|-------|
| `get-user` | Current user or optional user_id for another user. |
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

