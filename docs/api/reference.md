# API Reference

Per-endpoint reference for the Laravel API. For OpenAPI spec see `docs/api/openapi.yaml`.

**Base URL:** `/api`  
**Authentication:** Cookie-based Sanctum. Send credentials with requests; most endpoints require `auth:sanctum` and often `verified`.  
**CSRF:** Required except for `POST /api/contact-form`.

---

## Auth

| Method | URL | Controller / source | Auth | Request | Response |
|--------|-----|----------------------|------|---------|----------|
| GET | /api/user | Host `routes/api.php` (not trading-app) | Sanctum | — | Current user object (with `UseTradingAppTrait`: appended `held_credits`, `credits_available_for_automation` for Trimmer credit holds; ledger remains `available_credits`) |
| POST | /api/login | OHLCX\TradingApp\AuthController@login | — | email, password | Session |
| POST | /api/register | OHLCX\TradingApp\AuthController@register | — | name, email, password | 201 + user/session |
| POST | /api/password/email | OHLCX\TradingApp\PasswordResetController | — | email | 200 |
| POST | /api/password/reset | OHLCX\TradingApp\PasswordResetController | — | token, email, password | 200 |
| POST | /api/two-factor-challenge | OHLCX\TradingApp\AuthController@twoFactorChallenge | — | code | 200 |
| GET | /api/email/verify | OHLCX\TradingApp\EmailVerificationController | — | Query params per Laravel | 200 |

---

## Profile (user-profile package)

| Method | URL | Controller / source | Auth | Request | Response |
|--------|-----|----------------------|------|---------|----------|
| DELETE | /api/user-profile | OHLCX\UserProfile (delete user) | Sanctum | Optional body (e.g. password) | 200 |
| PUT | /api/user-profile/profile | UserProfile (update profile) | Sanctum | Profile fields | 200 |
| PUT | /api/user-profile/profile-information | UserProfile | Sanctum | Profile info | 200 |
| PUT | /api/user-profile/password | UserProfile | Sanctum | password, etc. | 200 |
| DELETE | /api/user-profile/profile-photo | UserProfile | Sanctum | — | 200 |
| GET | /api/user-profile/sessions | UserProfile | Sanctum | — | List of sessions |
| POST | /api/user-profile/logout-other-sessions | UserProfile | Sanctum | Optional password | 200 |
| POST | /api/user-profile/email/verification-notification | UserProfile | Sanctum | — | 200 |

---

## User data (trading-app)

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| GET | /api/user/onboarding | UserOnboardingController@get | Sanctum | — | Onboarding state |
| POST | /api/user/onboarding | UserOnboardingController@post | Sanctum | Onboarding payload | 200 |
| GET | /api/user/preferences | UserPreferencesController@get | Sanctum | — | Preferences |
| POST | /api/user/preferences | UserPreferencesController@post | Sanctum | Preferences | 200 |
| GET | /api/user/settings | UserSettingsController@getSettings | Sanctum | — | Settings |
| POST | /api/user/settings | UserSettingsController@saveSettings | Sanctum | Settings | 200 |

---

## Knowledge Base

Structured product/feature articles (from docs and screenshot analysis). Read-only; requires Sanctum.

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| GET | /api/knowledge-base | KnowledgeBaseController@index | Sanctum | Query: `area` (filter by area), `q` (search title/content) | `{ "data": [ { "id", "slug", "title", "area", "content", "excerpt", "route_path", "component_reference", "screenshot_filenames", "meta", "created_at", "updated_at" }, ... ] }` |
| GET | /api/knowledge-base/{slug} | KnowledgeBaseController@show | Sanctum | — | `{ "data": { "id", "slug", "title", "area", "content", "excerpt", "route_path", "component_reference", "screenshot_filenames", "meta", "created_at", "updated_at" } }` or 404 `{ "message": "Article not found." }` |

---

## Markets & content (remote.php → OHLCXApiService)

All GETs use 1-minute cache unless noted. Errors return `{"error": "message"}` with 500.

| Method | URL | Auth | Request | Response |
|--------|-----|------|---------|----------|
| GET | /api/markets | Sanctum | Optional query: market_id | Market list or single |
| GET | /api/markets/{marketId} | Sanctum | — | Single market |
| GET | /api/tickers | Sanctum | Optional query: market_id | Ticker list |
| GET | /api/tickers/{symbol} | Sanctum | — | Single ticker |
| GET | /api/market-calendar | Sanctum | — | Calendar data |
| POST | /api/market-balance | Sanctum, verified | filters (marketId, filteredPeriod, filteredInterval, filteredSession) | Balance data |
| GET | /api/news | Sanctum | Query: `page`, `per_page` | Paginated news: `{ data, links, meta }` (Laravel-style) |
| GET | /api/news/{id} | Sanctum | — | Single news item by id |
| GET | /api/popular-news | Sanctum | Query: `page`, `per_page` | Paginated news items |
| GET | /api/crypto-news | Sanctum | Query: `page`, `per_page` | Paginated news items |
| GET | /api/legacy_analysis | Sanctum | — | Legacy analysis |
| GET | /api/analysis | Sanctum | — | AI analysis (TradingRooms Message + attachments) |

---

## Strategies (remote.php → OHLCXApiService)

| Method | URL | Auth | Request | Response |
|--------|-----|------|---------|----------|
| GET | /api/strategies | Sanctum | — | Strategy list (cached) |
| GET | /api/strategies/{id} | Sanctum | — | Single strategy |
| POST | /api/strategies | Sanctum | Strategy payload | 201 + data |
| PUT | /api/strategies/{id} | Sanctum | Strategy payload | 200 + data |
| DELETE | /api/strategies/{id} | Sanctum | — | 204 |
| GET | /api/strategies/search/{symbol} | Sanctum | — | Search results (cached) |
| GET | /api/strategy/{strategy}/conditions | Sanctum | — | Strategy conditions |
| POST | /api/strategy/{strategy}/clear-conditions-readings | Sanctum | — | 200 |
| GET | /api/strategy/{strategy}/activities | Sanctum | — | Activities |

Strategy action endpoints (all POST, Sanctum):  
`/api/strategy/{strategy}/settings/update-name`, `update-symbol`, `update-direction`, `update-timeframe`, `update-allocation`, `update-sizing-ordering`, `update-trailing-stop`, `update-order-cancelation`, `update-slack-webhook-url`, `update-risk-management`;  
`/api/strategy/{strategy}/retain`, `retain-stop`, `deploy`, `duplicate`;  
`/api/strategy/{strategy}/status/on`, `status/off`;  
`/api/strategy/{strategy}/signals/on|off|toggle`, `trades/on|off|toggle`, `orders/on|off|toggle`;  
`/api/strategy/{strategy}/notifications/signals/on|off|toggle`, same for trades and orders;  
`/api/strategy/{strategy}/notifications/send-slack-test-notification`.  

Request body for these is typically JSON; response is `data['data']` from upstream or error 500.

---

## Conditions (remote.php → OHLCXApiService)

| Method | URL | Auth | Request | Response |
|--------|-----|------|---------|----------|
| GET | /api/conditions | Sanctum | — | Condition list (cached) |
| GET | /api/conditions/{id} | Sanctum | — | Single condition |
| POST | /api/conditions | Sanctum | Condition payload | 201 + data |
| PUT | /api/conditions/{id} | Sanctum | Condition payload | 200 |
| DELETE | /api/conditions/{id} | Sanctum | — | 204 |

---

## Signals (remote.php → OHLCXApiService)

| Method | URL | Auth | Request | Response |
|--------|-----|------|---------|----------|
| GET | /api/signals | Sanctum | — | Signal list (cached) |

---

## Activities (trading-app)

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| GET | /api/activities | ActivityController@userActivities | Sanctum | — | Activity list |
| POST | /api/activities | ActivityController@logActivity | Sanctum | Activity payload (optional `advanced_order_type`, max 32 chars) | 200 — logs only; does **not** debit credits |
| DELETE | /api/activities/{id} | ActivityController@deleteActivity | Sanctum | — | 200 |

Trimmer billing uses **credit holds** (below), not activity deductions.

---

## Credit holds (trading-app)

Trimmer parent orders: reserve spendable credits (`credits_available_for_automation`), capture on fill, release on cancel/expiry. Idempotent per `(user_id, schwab_parent_order_id)`.

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| GET | /api/credit-holds | CreditHoldController@index | Sanctum | Query: `per_page` (1–50, default 25) | Laravel paginator JSON |
| POST | /api/credit-holds/transfer | CreditHoldController@transfer | Sanctum | `from_schwab_parent_order_id`, `to_schwab_parent_order_id` | `{ transferred: bool }` — **409** if another hold already uses `to` |
| POST | /api/credit-holds | CreditHoldController@store | Sanctum | `schwab_parent_order_id` (required), `broker_account_hash` (optional), `credits_amount` (optional) | `{ id, status, schwab_parent_order_id, credits_amount }` — **201** if created, **200** if existing held row; **422** if insufficient spendable credits |
| POST | /api/credit-holds/capture | CreditHoldController@capture | Sanctum | `schwab_parent_order_id` | `{ captured: bool }` |
| POST | /api/credit-holds/release | CreditHoldController@release | Sanctum | `schwab_parent_order_id` | `{ released: bool }` |

---

## Accounts (schwab-integration)

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| GET | /api/accounts | AccountGrowthController@index | Sanctum | — | Account list |
| GET | /api/accounts/balances | AccountGrowthController | Sanctum | — | Balances |
| GET | /api/accounts/{accountId}/balance | AccountGrowthController | Sanctum | — | Balance |
| GET | /api/accounts/{accountId}/growth | AccountGrowthController | Sanctum | — | Growth |
| GET | /api/accounts/{accountId}/pnl | AccountGrowthController | Sanctum | — | PnL |

---

## Billing (stripe-credits-billing)

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| GET | /api/credits | CreditController@index | Sanctum | — | Credits |
| GET | /api/transaction-history | BillingController | Sanctum | — | History |
| GET | /api/admin/users/{user}/billing | AdminBillingController | Sanctum (admin) | — | Billing |
| POST | /api/admin/users/{user}/billing/adjust | AdminBillingController | Sanctum (admin) | Body | 200 |
| POST | /api/admin/users/{user}/billing/package | AdminBillingController | Sanctum (admin) | Body | 200 |

---

## Chat (trading-rooms)

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| POST | /api/group | ApiController@storeGroup | Sanctum | Group payload | 201 |
| GET | /api/group/{group} | ApiController | Sanctum | — | Group |
| PUT | /api/group/{group} | ApiController | Sanctum | Group payload | 200 |
| DELETE | /api/group/{group} | ApiController | Sanctum | — | 200 |
| PUT | /api/group/{group}/invite | ApiController | Sanctum | Invite payload | 200 |
| POST | /api/group/{group}/join | ApiController | Sanctum | — | 200 |
| DELETE | /api/group/{group}/leave | ApiController | Sanctum | — | 200 |
| GET | /api/group/{group}/status | ApiController | Sanctum | — | Status |
| GET | /api/invites | ApiController@userInvitations | Sanctum | — | Invites |
| POST | /api/invites | ApiController@sendInvite | Sanctum | Invite payload | 200 |
| POST | /api/invites/accept | ApiController@acceptInvite | Sanctum | Body | 200 |
| GET | /api/invites/validate/{token} | ApiController | Sanctum | — | Validation |
| DELETE | /api/invites/{id} | ApiController | Sanctum | — | 200 |
| POST | /api/invites/{id}/resend | ApiController | Sanctum | — | 200 |
| POST | /api/join-requests/{joinRequest}/respond | ApiController | Sanctum | Body | 200 |
| POST | /api/message | ApiController@storeMessage | Sanctum | Message payload | 201 |
| GET | /api/message/older/{message} | ApiController | Sanctum | — | Older messages |
| DELETE | /api/message/{message} | ApiController | Sanctum | — | 200 |
| GET | /api/sidebar-conversations | ApiController@getConversations | Sanctum | — | Conversations |
| GET | /api/user/{user} | ApiController | Sanctum | — | User |
| GET | /api/user/{user}/status | ApiController | Sanctum | — | Status |
| GET | /api/users | ApiController@users | Sanctum | — | Users |
| POST | /api/users | ApiController@storeUser | Sanctum | User payload | 201 |
| GET | /api/users/{id} | ApiController | Sanctum | — | User |
| PUT | /api/users/{id} | ApiController | Sanctum | User payload | 200 |
| DELETE | /api/users/{id} | ApiController | Sanctum | — | 200 |
| POST | /api/user/block-unblock/{user} | ApiController | Sanctum | — | 200 |
| POST | /api/user/change-role/{user} | ApiController | Sanctum | Body | 200 |

---

## Support (trading-app)

| Method | URL | Controller | Auth | Request | Response |
|--------|-----|------------|------|---------|----------|
| POST | /api/contact-form | SupportController@contact_form | None (CSRF exempt) | Form fields | 200 |
| POST | /api/support-request | SupportController@support_request | Sanctum | Body | 200 |
| POST | /api/report-issue | SupportController@report_issue | Sanctum | Body | 200 |

---

## Response structure

- **Success:** JSON body; proxy routes often return the upstream `data` key (e.g. array or object).
- **Error:** `{"error": "message"}` with appropriate status (e.g. 500).
- **Validation:** 422 with Laravel validation error structure.

Run `php artisan route:list --path=api` for the exact list. See `docs/api/openapi.yaml` for an OpenAPI 3 spec.
