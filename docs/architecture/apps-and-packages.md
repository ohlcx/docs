# Domain Packages (vendor/ohlcx)

Private Laravel packages under `vendor/ohlcx/` and how the app uses them.

---

## 1. Overview

| Package | Purpose |
|---------|---------|
| **trading-app** | Auth, activities, support, onboarding, preferences, settings, email verification, **knowledge base** (KB API). |
| **trading-rooms** | Chat: groups, invites, messages, users, sidebar conversations, join-requests, AI calls. |
| **user-profile** | Profile, sessions, password, profile-information, profile-photo, delete user. |
| **stripe-credits-billing** | Credits, transactions, packages, Stripe, admin billing. |
| **schwab-integration** | Broker integration: accounts, balances, growth, PnL, TD auth, token webhook. |
| **tdameritrade-laravel** | TD/Schwab API client (used by schwab-integration). |
| **ai-dev** (internal) | Internal AI development sandbox for maintainers only—not part of the public product surface. |

The app does **not** implement these domains in `app/`; it registers package routes and uses their traits/controllers.

---

## 2. trading-app

**Purpose:** Auth, user lifecycle, activities, support, onboarding, preferences, settings, **knowledge base** (product/feature KB API).

**Main classes / entry points:**

- **Controllers:** AuthController (login, register, twoFactorChallenge), PasswordResetController (password/email, password/reset), ActivityController (log, list, delete), SupportController (contact_form, support_request, report_issue), UserOnboardingController, UserPreferencesController, UserSettingsController, EmailVerificationController, **KnowledgeBaseController** (index, show).
- **Models:** Activity, **KnowledgeBaseArticle** (KB lives in this package at `vendor/ohlcx/trading-app`).
- **Events:** ActivityLogged.
- **Mail:** ContactFormSubmitted, SupportRequested, IssueReported.
- **Config:** social-login, horizon (if any).
- **Traits:** UseTradingAppTrait (for registering routes/views).

**How the app uses it:**

- `routes/api.php` is extended by the package’s API routes (login, register, password/*, two-factor-challenge, activities, contact-form, support-request, report-issue, user/onboarding, user/preferences, user/settings, email/verify, **knowledge-base**, **knowledge-base/{slug}**).
- SPA entry routes (`/trading`, `/trading/*`) may be registered by this package’s web routes.
- No app-level controllers; the app just loads the package and uses its routes.

**Recommendations:**

- Keep auth and support contract stable; document expected request/response for frontend.
- Consider extracting a small “support” or “auth” facade in app only if you need a single place to customize behavior.

---

## 3. trading-rooms

**Purpose:** Chat, groups, invites, messages, conversations, AI analysis.

**Main classes:**

- **Controllers:** ApiController (groups, invites, messages, users, sidebar-conversations, join-requests, block/role).
- **Models:** Group, Invite, Message, MessageAttachment, Conversation, JoinRequest, AiCall.
- **Jobs:** CallAiJob, DeleteGroupJob, SendInviteEmailJob.
- **Events:** JoinRequestResponded, AiCallCompleted, GroupDeleted, MessageDeleted, UserLeftGroup, AiCallFailed, SocketMessage.
- **Mail:** InviteUserMail, UserCreated, UserRoleChanged, UserBlockedUnblocked.
- **Traits:** UseTradingRoomsTrait.

**How the app uses it:**

- Package registers API routes: group, group/{id}, invites, message, message/older/{id}, message/{id}, join-requests/{id}/respond, sidebar-conversations, user/{user}, user/{user}/status, users, users/{id}, user/block-unblock, user/change-role.
- `routes/remote.php` uses `OHLCX\TradingRooms\Models\Message` (and attachments, ai_calls) for the custom `GET /api/analysis` response.
- Frontend uses these routes for chat UI and conversation lists.

**Recommendations:**

- Keep API contract for messages/invites documented (e.g. in api-reference.md or OpenAPI).
- If more realtime events are added, document channel names and payloads.

---

## 4. user-profile

**Purpose:** User profile, sessions, password, delete account.

**Main classes:**

- **Routes:** user-profile (DELETE for delete user), user-profile/profile, user-profile/sessions, user-profile/logout-other-sessions, user-profile/password, user-profile/profile-information, user-profile/profile-photo, user-profile/email/verification-notification.
- **Controllers:** UserProfileController (or equivalent) for these actions.
- **Rules:** NoHtmlOrJs (validation).
- **Traits:** UseUserProfileTrait.

**How the app uses it:**

- Frontend calls `DELETE /api/user-profile` (with optional body) for account deletion; other profile endpoints for profile/sessions/password.
- No app-level profile controller; all behavior is in the package.

**Recommendations:**

- Ensure DELETE /api/user-profile request/response (and any confirmation payload) is documented and aligned with React (AuthProvider).

---

## 5. stripe-credits-billing

**Purpose:** Credits, transactions, packages, Stripe checkout, admin billing.

**Main classes:**

- **Controllers:** CreditController (credits), BillingController (transaction-history), AdminBillingController (admin/users/{user}/billing, adjust, package).
- **Models:** Transaction, Package, Feature, UsedFeature.
- **Observers:** UserObserver (if any).
- **Config:** stripe.
- **Traits:** UseStripeCreditsBillingTrait.

**How the app uses it:**

- Package registers API routes: credits, transaction-history, admin/users/{user}/billing, admin/users/{user}/billing/adjust, admin/users/{user}/billing/package.
- Web routes for buy-credits, Stripe webhook, etc.
- Frontend (CreditsPage, billing widgets) calls these endpoints.

**Recommendations:**

- Document webhook payload and idempotency if not already.
- Keep package responsible for all Stripe and credit logic; app should not duplicate it.

---

## 6. schwab-integration

**Purpose:** Broker integration: list accounts, balances, growth, PnL; TD auth and token lifecycle.

**Main classes:**

- **Controllers:** AccountGrowthController (accounts, accounts/balances, accounts/{id}/balance, growth, pnl).
- **Models:** Token, Account, AccountHistory.
- **Jobs:** UpdateTDAccountsJob.
- **Events/Listeners:** TokenUpdatedEvent, TokenUpdatedListener.
- **Traits:** UseSchwabTrait.
- **Routes:** api (accounts/*), web (td/auth, td/callback, td/logout, td/refresh, webhook if any).

**How the app uses it:**

- Package exposes `/api/accounts*` for the React app to get account summaries, balances, growth, PnL.
- Actual brokerage data (positions, orders, transactions, option chains, movers) is fetched by the frontend via **useApiService** from the Schwab API directly; this package complements that with server-side account aggregation and token handling.

**Recommendations:**

- Clearly document which data comes from this package (e.g. aggregated account/growth) vs from the frontend’s direct Schwab calls (positions, orders, instruments).
- Ensure token refresh and webhook are robust and logged.

---

## 7. tdameritrade-laravel

**Purpose:** TD/Schwab API client used by schwab-integration (and possibly app code).

**Main classes:**

- **Tdameritrade** (main service), **Facades\TdameritradeFacades**.
- **Api:** UserPrincipal, Instruments, Transactions, Movers, Price, Accounts, Options, Api, Market, Orders.
- **Config:** tdameritrade.

**How the app uses it:**

- Typically via schwab-integration (token + API calls). The app may also use the facade or config for custom server-side Schwab calls.

**Recommendations:**

- Keep this package as the single server-side TD/Schwab client; avoid ad-hoc HTTP calls elsewhere.
- Document which API classes are used and for what (accounts, orders, instruments, etc.) if you add more server-side broker features.

---

## 8. Summary diagram

```
Laravel App (routes/api.php + remote.php)
        │
        ├──► trading-app      → auth, activities, support, onboarding, preferences, settings, knowledge base
        ├──► trading-rooms    → chat (groups, invites, messages), analysis data
        ├──► user-profile     → profile, sessions, password, delete user
        ├──► stripe-credits-billing → credits, transactions, Stripe, admin billing
        ├──► schwab-integration → accounts, balances, growth, PnL, TD auth
        └──► tdameritrade-laravel  → TD/Schwab API client (used by schwab-integration)
```

See also: `docs/architecture.md`, `docs/backend.md`, `docs/api-reference.md`.
