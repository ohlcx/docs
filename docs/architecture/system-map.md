# System Map

Relationships between Laravel routes, controllers, models, services, React pages, and API calls.

---

## AI system map (request flow)

End-to-end flow for a typical request from the UI to data:

```
React Page
    ↓
API endpoint (/api/...)
    ↓
Controller (route closure in remote.php, or package controller in vendor/ohlcx)
    ↓
Service (OHLCXApiService for Light `remote.php` proxy; `OhlcxMainApi` for MCP/AI; or package service)
    ↓
Database (app DB via Eloquent) or External API (OHLCX API / Schwab)
```

In this app:

- **React Page** → calls `window.axios('/api/...')` or `useApiService` (Schwab). See [React pages → API calls](#3-react-pages--api-calls).
- **API endpoint** → defined in `routes/api.php` / `routes/remote.php` or by packages in `vendor/ohlcx/*`.
- **Controller** → either a closure in `routes/remote.php` or a controller class in a package (e.g. AuthController, UserProfileController, ApiController in trading-rooms).
- **Service** → `OHLCXApiService` for proxy routes; `OhlcxMainApi` (`RemoteOhlcxApiAdapter`) for MCP/AI domain tools; package-specific logic for auth, profile, chat, billing, accounts.
- **Database / external** → app uses MySQL for User and package tables (activities, groups, messages, transactions, etc.); many read paths go to the **external OHLCX API** or **Schwab API** instead of the app DB.

---

## 1. High-level flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           React SPA (resources/js)                               │
│  Pages (Index → Layout / AuthenticatedLayout → Main, Strategies, Signals, …)     │
│  Components (StrategyCard, Chat, UserProfile, OrderForms, …)                     │
│  Stores (useStrategyStore, useSignalStore, useAccountStore, …)                   │
│  Hooks (AuthProvider, AppContext, useApiService, useSettings, …)                │
└─────────────────────────────────────────────────────────────────────────────────┘
     │                                              │
     │ window.axios ('/api/...')                     │ useApiService (fetch)
     │ Cookie (Sanctum)                             │ Bearer (Schwab)
     ▼                                              ▼
┌─────────────────────────────┐          ┌─────────────────────────────┐
│  Laravel (routes/api.php,   │          │  Schwab API                 │
│  routes/remote.php)         │          │  (api.schwabapi.com)        │
│  + vendor/ohlcx/* routes    │          │  Accounts, orders,         │
│  OHLCXApiService           │          │  instruments, chains,       │
│  (proxy → ohlcx.online)     │          │  movers, history            │
└─────────────────────────────┘          └─────────────────────────────┘
     │
     │ Bearer (OHLCX_API_TOKEN)
     ▼
┌─────────────────────────────┐
│  External OHLCX API         │
│  (www.ohlcx.online/api/)    │
│  Strategies, conditions,   │
│  signals, markets, tickers  │
└─────────────────────────────┘
```

---

## 2. Laravel routes → implementation

| Route source | Implementation | Used by React |
|--------------|----------------|---------------|
| GET /api/user | routes/api.php closure | AuthProvider, layout |
| routes/remote.php (markets, tickers, strategies, conditions, signals, news, analysis, market-balance, market-calendar) | OHLCXApiService (proxy) + Cache | useStrategyStore, useSignalStore, useMarketStore, MarketsPage, MarketBalancePage, NewsFeed, Analysis, etc. |
| POST /api/login, register, password/*, two-factor-challenge | TradingApp (AuthController, PasswordResetController) | AuthProvider |
| GET|PUT|DELETE /api/user-profile/* | UserProfile package | AuthProvider, UserProfile components |
| GET|POST /api/user/onboarding, preferences, settings | TradingApp (UserOnboardingController, UserPreferencesController, UserSettingsController) | Onboarding, preferences, settings UI |
| GET|POST|DELETE /api/activities | TradingApp (ActivityController) | ActivityFeed |
| GET /api/accounts/* | Schwab (AccountGrowthController) | useAccountStore, dashboard, AccountInfo |
| GET /api/credits, transaction-history, admin/users/*/billing | CreditsBilling (CreditController, BillingController, AdminBillingController) | CreditsPage, billing widgets |
| group, invites, message, sidebar-conversations, user/{user}, users | TradingRooms (ApiController) | Chat, ConversationsSidebar, invites |
| POST /api/contact-form, support-request, report-issue | TradingApp (SupportController) | ContactPage, support forms |

---

## 3. React pages → API calls

| Page / feature | Laravel API calls | Schwab (useApiService) |
|----------------|--------------------|-------------------------|
| Main / Dashboard | user, accounts/balances, preferences | fetchAccounts, positions, orders, etc. |
| Strategies | strategies CRUD, strategy/* actions | — |
| Signals | signals | — |
| Markets | markets, tickers, market-calendar | — |
| Market balance | market-balance | — |
| Analysis | analysis, legacy_analysis | — |
| News | news, popular-news, crypto-news | — |
| Positions | — | positions, account data |
| Orders | — | orders, preview, submit |
| Options | — | option chains, instruments |
| Movers | — | movers |
| Credits | credits, transaction-history | — |
| Chat | group, message, invites, sidebar-conversations, users | — |
| User profile | user-profile/*, user | — |
| Auth | login, register, password/*, two-factor-challenge, user | — |

---

## 4. Models and services (backend)

| Layer | Item | Used by |
|-------|------|--------|
| App | User | Auth, packages |
| App | OHLCXApiService | remote.php closures |
| trading-app | Activity | ActivityController |
| trading-rooms | Group, Invite, Message, Conversation, JoinRequest, AiCall | ApiController, analysis |
| user-profile | (User + profile routes) | UserProfile controllers |
| stripe-credits-billing | Transaction, Package, Feature, UsedFeature | CreditController, BillingController, AdminBillingController |
| schwab-integration | Token, Account, AccountHistory | AccountGrowthController, jobs |

---

## 5. Diagram: Strategy flow

```
React (Strategies page, StrategyCard, useStrategyStore)
    │
    │ axios.get/post/put/delete('/api/strategies', '/api/strategy/...')
    ▼
Laravel routes/remote.php
    │
    │ OHLCXApiService->getData/postData/putData/deleteData
    ▼
External OHLCX API (strategies, strategy/{id}/...)
    │
    │ response data['data']
    ▼
Laravel (Cache::forget on write; Cache::remember on read)
    ▼
React (state update, UI)
```

---

## 6. Diagram: Order flow (broker)

```
React (Order form, useApiService)
    │
    │ fetch('https://api.schwabapi.com/...', { headers: { Authorization: Bearer token } })
    ▼
Schwab API (preview order, place order)
    │
    │ response
    ▼
React (useOrderStore, UI, useEchoOrderStatusUpdated for realtime)
```

(Laravel does not place orders; it may consume account summaries from schwab-integration and expose them via /api/accounts/*.)

---

See also: `docs/architecture.md`, `docs/api-reference.md`, `docs/API_DATA_SOURCES.md`, `docs/backend.md`, `docs/frontend.md`.
