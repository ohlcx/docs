# API & Data Sources: Our API vs Broker API

This document clarifies where data comes from in the OHLCX app: **our Laravel API** (`/api/*`) vs the **broker API** (Schwab) called directly from the frontend.

## Our API (Laravel `/api/*`)

- **Base URL:** Same origin as the app (e.g. `https://your-app.com/api`).
- **Auth:** Cookie-based Laravel Sanctum. The React app uses `window.axios` with `withCredentials: true` so cookies are sent.
- **Used for:**
  - Auth: login, register, password reset, 2FA, `/api/user`.
  - User profile: profile info, sessions, delete account (`DELETE /api/user-profile`).
  - Onboarding, preferences, settings: `/api/user/onboarding`, `/api/user/preferences`, `/api/user/settings`.
  - Markets & content: markets, tickers, market calendar, market balance, news, analysis (many of these are **proxied** to the external OHLCX API via `OHLCXApiService`).
  - Strategies & conditions: full CRUD and strategy actions (again proxied to the external OHLCX API).
  - Signals, activities: `/api/signals`, `/api/activities`.
  - Account summaries and billing: `/api/accounts/*`, `/api/credits`, `/api/transaction-history` (implemented by private packages; account *details* may still come from the broker).
  - Chat / trading rooms: groups, invites, messages (`/api/group/*`, `/api/message/*`, etc.).
  - Support: `/api/contact-form`, `/api/support-request`, `/api/report-issue`.
- **Where it’s called:** React code uses `window.axios.get/post/put/delete('/api/...')` from stores (e.g. `useStrategyStore`, `useSignalStore`), pages, and components. See `docs/api/openapi.yaml` for the contract.

## Broker API (Schwab)

- **Base URL:** `https://api.schwabapi.com` (production) or sandbox equivalent.
- **Auth:** OAuth tokens. The app stores a Schwab access/refresh token (e.g. from linking a brokerage account) and sends it in `Authorization: Bearer <token>`.
- **Used for:**
  - Brokerage accounts: list accounts, balances, positions, orders, transactions.
  - Market data: instruments, option chains, price history, movers.
  - Order placement: preview and submit orders to the broker.
- **Where it’s called:** The React app uses **`useApiService`** (`resources/js/hooks/useApiService.jsx`), which calls the Schwab API directly (e.g. `fetch('https://api.schwabapi.com/...')`) with the user’s broker token. There is a circuit-breaker for repeated 401s. **This is not our Laravel API** — it’s a separate integration from the frontend to Schwab.

## Summary

| Data / action              | Source              | How it’s called in the app      |
|---------------------------|---------------------|----------------------------------|
| Login, register, profile  | Our API             | `window.axios` → `/api/*`        |
| Strategies, conditions    | Our API (proxied)   | `window.axios` → `/api/*`        |
| Markets, news, analysis   | Our API (proxied)   | `window.axios` → `/api/*`        |
| Chat, invites, billing    | Our API             | `window.axios` → `/api/*`        |
| Broker accounts/positions | Broker (Schwab)     | `useApiService` → Schwab API    |
| Broker orders/transactions| Broker (Schwab)     | `useApiService` → Schwab API    |
| Option chains, movers     | Broker (Schwab)     | `useApiService` → Schwab API     |

When adding features or debugging, check whether the data comes from our Laravel routes (and possibly the external OHLCX API behind them) or from the broker API via `useApiService`.
