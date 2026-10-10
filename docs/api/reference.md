# API Reference

Per-endpoint reference for the Laravel API. Each section lists its endpoints in a table (method, URL, who may call it, what it does) and, under the table, what each one takes and answers. For OpenAPI spec see `docs/api/openapi.yaml`.

**Base URL:** `/api`  
**Authentication:** Cookie-based Sanctum. Send credentials with requests; most endpoints require `auth:sanctum` and often `verified`.  
**CSRF:** Required except for `POST /api/contact-form`.

---

## Auth

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/user | Sanctum | The signed-in user. Served by the host application, not by a package. |
| POST | /api/login | — | Sign in. |
| POST | /api/register | — | Create an account. |
| POST | /api/password/email | — | Send a password reset link. |
| POST | /api/password/reset | — | Set a new password with a reset token. |
| POST | /api/two-factor-challenge | — | Answer the two-factor challenge. |
| GET | /api/email/verify | — | Verify an email address. |

Request and response:

- `GET /api/user`. Response: Current user object (with `UseTradingAppTrait`: appended `held_credits`, `credits_available_for_automation` for Trimmer credit holds; ledger remains `available_credits`).
- `POST /api/login`. Request: email, password. Response: Session.
- `POST /api/register`. Request: name, email, password. Response: 201 + user/session.
- `POST /api/password/email`. Request: email. Response: 200.
- `POST /api/password/reset`. Request: token, email, password. Response: 200.
- `POST /api/two-factor-challenge`. Request: code. Response: 200.
- `GET /api/email/verify`. Request: Query params per Laravel. Response: 200.

---

## Profile (user-profile package)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| DELETE | /api/user-profile | Sanctum | Delete the user. |
| PUT | /api/user-profile/profile | Sanctum | Update the profile. |
| PUT | /api/user-profile/profile-information | Sanctum | Update the profile information. |
| PUT | /api/user-profile/password | Sanctum | Change the password. |
| DELETE | /api/user-profile/profile-photo | Sanctum | Remove the profile photo. |
| GET | /api/user-profile/sessions | Sanctum | List the signed-in sessions. |
| POST | /api/user-profile/logout-other-sessions | Sanctum | Sign out of the other sessions. |
| POST | /api/user-profile/email/verification-notification | Sanctum | Send the verification email again. |

Request and response:

- `DELETE /api/user-profile`. Request: Optional body (e.g. password). Response: 200.
- `PUT /api/user-profile/profile`. Request: Profile fields. Response: 200.
- `PUT /api/user-profile/profile-information`. Request: Profile info. Response: 200.
- `PUT /api/user-profile/password`. Request: password, etc. Response: 200.
- `DELETE /api/user-profile/profile-photo`. Response: 200.
- `GET /api/user-profile/sessions`. Response: List of sessions.
- `POST /api/user-profile/logout-other-sessions`. Request: Optional password. Response: 200.
- `POST /api/user-profile/email/verification-notification`. Response: 200.

---

## User data (trading-app)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/user/onboarding | Sanctum | Read the onboarding state. |
| POST | /api/user/onboarding | Sanctum | Save the onboarding state. |
| GET | /api/user/preferences | Sanctum | Read the preferences. |
| POST | /api/user/preferences | Sanctum | Save the preferences. |
| GET | /api/user/settings | Sanctum | Read the settings. |
| POST | /api/user/settings | Sanctum | Save the settings. |
| GET | /api/user/chart-dashboards | Sanctum | Read the saved Workspaces document. |
| PUT | /api/user/chart-dashboards | Sanctum | Save the Workspaces document. |

Request and response:

- `GET /api/user/onboarding`. Response: Onboarding state.
- `POST /api/user/onboarding`. Request: Onboarding payload. Response: 200.
- `GET /api/user/preferences`. Response: Preferences.
- `POST /api/user/preferences`. Request: Preferences. Response: 200.
- `GET /api/user/settings`. Response: Settings.
- `POST /api/user/settings`. Request: Settings. Response: 200.
- `GET /api/user/chart-dashboards`. Response: `{ state, revision }` (`state` null and `revision` 0 when nothing is saved).
- `PUT /api/user/chart-dashboards`. Request: `{ state, revision }`. Response: 200 `{ revision }`; 409 `{ message, state, revision }`; 422.

**Chart dashboards.** One document per user: `{ version: 1, dashboards: [{ id, name, tiles: [{ id, symbol, range, frequency, chartType?, kind?, view?, settings? }], layout: [{ i, x, y, w, h }], stackOrder }] }`. `PUT` sends the document with the `revision` it was based on (0 when the client has never seen one). When that is the stored revision the document is saved and the revision goes up by one; otherwise nothing is written and the response is 409 with the stored document and revision. Limits: 1 to 10 dashboards; up to 12 tiles and 12 layout entries each; ids 1 to 64 characters; names 1 to 40; `symbol` 0 to 64 (empty is a spot with no symbol chosen yet); `range` and `frequency` 1 to 16; optional `chartType`, `kind` and `view` up to 32 each, stored only when given (`kind` is what the block shows when it is not a chart; `view` is which half of a Level II block is shown, `charts` or absent for the table); optional `settings` is a block's own flat map of up to 16 entries (text up to 32 characters, numbers, true/false; names are plain words and are stored in alphabetical order), used for the options chain's filters; layout numbers are integers 0 to 10000; `stackOrder` is null or up to 12 ids. `activeId` and unknown keys are dropped. After a successful save `UserChartDashboardsUpdated` is broadcast on `private-App.Models.User.{id}` with `{ revision }`; a failed broadcast does not fail the save. This file is the copy of record: the release sync copies `docs/` from ohlcx-light over trading-app's.

---

## Knowledge Base

Structured product/feature articles (from docs and screenshot analysis). Read-only; requires Sanctum.

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/knowledge-base | Sanctum | List or search articles. |
| GET | /api/knowledge-base/{slug} | Sanctum | One article. |

Request and response:

- `GET /api/knowledge-base`. Request: Query: `area` (filter by area), `q` (search title/content). Response: `{ "data": [ { "id", "slug", "title", "area", "content", "excerpt", "route_path", "component_reference", "screenshot_filenames", "meta", "created_at", "updated_at" }, ... ] }`.
- `GET /api/knowledge-base/{slug}`. Response: `{ "data": { "id", "slug", "title", "area", "content", "excerpt", "route_path", "component_reference", "screenshot_filenames", "meta", "created_at", "updated_at" } }` or 404 `{ "message": "Article not found." }`.

---

## Markets & content (relayed to the main OHLCX API on Light)

All GETs use 1-minute cache unless noted. Errors return `{"error": "message"}` with 500.

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/markets | Sanctum | List markets, or one. |
| GET | /api/markets/{marketId} | Sanctum | One market. |
| GET | /api/tickers | Sanctum | List tickers. |
| GET | /api/tickers/{symbol} | Sanctum | One ticker. |
| GET | /api/market-calendar | Sanctum | The market calendar. |
| POST | /api/market-balance | Sanctum, verified | Market balance for a set of filters. |
| GET | /api/news | Sanctum | A page of news. |
| GET | /api/news/{id} | Sanctum | One news item. |
| GET | /api/popular-news | Sanctum | A page of popular news. |
| GET | /api/crypto-news | Sanctum | A page of crypto news. |
| GET | /api/legacy_analysis | Sanctum | The older analysis feed. |
| GET | /api/analysis | Sanctum | The analysis feed. |

Request and response:

- `GET /api/markets`. Request: Optional query: market_id. Response: Market list or single.
- `GET /api/markets/{marketId}`. Response: Single market.
- `GET /api/tickers`. Request: Optional query: market_id. Response: Ticker list.
- `GET /api/tickers/{symbol}`. Response: Single ticker.
- `GET /api/market-calendar`. Response: Calendar data.
- `POST /api/market-balance`. Request: filters (marketId, filteredPeriod, filteredInterval, filteredSession). Response: Balance data.
- `GET /api/news`. Request: Query: `page`, `per_page`. Response: Paginated news: `{ data, links, meta }` (Laravel-style).
- `GET /api/news/{id}`. Response: Single news item by id.
- `GET /api/popular-news`. Request: Query: `page`, `per_page`. Response: Paginated news items.
- `GET /api/crypto-news`. Request: Query: `page`, `per_page`. Response: Paginated news items.
- `GET /api/legacy_analysis`. Response: Legacy analysis.
- `GET /api/analysis`. Response: AI analysis (TradingRooms Message + attachments).

---

## Strategies (relayed to the main OHLCX API on Light)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/strategies | Sanctum | List strategies. |
| GET | /api/strategies/{id} | Sanctum | One strategy. |
| POST | /api/strategies | Sanctum | Create a strategy. |
| PUT | /api/strategies/{id} | Sanctum | Update a strategy. |
| DELETE | /api/strategies/{id} | Sanctum | Delete a strategy. |
| GET | /api/strategies/search/{symbol} | Sanctum | Strategies on a symbol. |
| GET | /api/strategy/{strategy}/conditions | Sanctum | A strategy's conditions. |
| POST | /api/strategy/{strategy}/clear-conditions-readings | Sanctum | Clear a strategy's condition readings. |
| GET | /api/strategy/{strategy}/activities | Sanctum | A strategy's activities. |

Request and response:

- `GET /api/strategies`. Response: Strategy list (cached).
- `GET /api/strategies/{id}`. Response: Single strategy.
- `POST /api/strategies`. Request: Strategy payload. Response: 201 + data.
- `PUT /api/strategies/{id}`. Request: Strategy payload. Response: 200 + data.
- `DELETE /api/strategies/{id}`. Response: 204.
- `GET /api/strategies/search/{symbol}`. Response: Search results (cached).
- `GET /api/strategy/{strategy}/conditions`. Response: Strategy conditions.
- `POST /api/strategy/{strategy}/clear-conditions-readings`. Response: 200.
- `GET /api/strategy/{strategy}/activities`. Response: Activities.

Strategy action endpoints (all POST, Sanctum):  
`/api/strategy/{strategy}/settings/update-name`, `update-symbol`, `update-direction`, `update-timeframe`, `update-allocation`, `update-sizing-ordering`, `update-trailing-stop`, `update-order-cancelation`, `update-slack-webhook-url`, `update-risk-management`;  
`/api/strategy/{strategy}/retain`, `retain-stop`, `deploy`, `duplicate`;  
`/api/strategy/{strategy}/status/on`, `status/off`;  
`/api/strategy/{strategy}/signals/on|off|toggle`, `trades/on|off|toggle`, `orders/on|off|toggle`;  
`/api/strategy/{strategy}/notifications/signals/on|off|toggle`, same for trades and orders;  
`/api/strategy/{strategy}/notifications/send-slack-test-notification`.  

Also under `/api/strategy/{strategy}`: `schedule` (POST); `clear-signals`, `clear-trades`, `clear-flags` (POST); `signals`, `trades`, `flags`, `statistics`, `performance`, `timeline` (GET). `GET /api/strategies?paged=1` returns the paged list, with optional `page` and `per_page` (1 to 50).

Request body for these is typically JSON; a success is `data['data']` from upstream.

### Failures of strategy and condition writes

Creating, updating and deleting a strategy or a condition, every strategy action endpoint above, the four clear actions and `DELETE /api/signals/{id}` answer a failure with one fixed sentence under both `message` and `error`. The cause is never sent.

| Upstream answered | Status | Sentence |
|-------------------|--------|----------|
| 422 | 422, with the validation `errors` | The server did not accept these settings. |
| 422 with a named refusal | 422, with `errors` and `code` | the refusal's sentence (below) |
| 401 | 401 | You are signed out. Sign in and try again. |
| 403 | 403 | This account is not allowed to do that. |
| 404 | 404 | That was not found. |
| 429 | 429 | Too many requests. Wait a moment and try again. |
| a server error, or no answer | 502 | Unable to save right now. |
| anything else | 500 | Unable to save right now. |

| `code` | Sentence |
|--------|----------|
| `strategy_deployed` | Retain the strategy before changing it. |
| `no_routable_account` | Choose a linked account before switching orders on. |
| `deploy_needs_account` | Choose a linked account, or switch orders off, before deploying. |

A 4xx from the first table means nothing was stored.

### Order routing accounts

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/strategy-accounts | Sanctum | Order routing accounts (OHLCX Pro only). |
| POST | /api/strategy/{strategy}/settings/update-accounts | Sanctum | Choose a strategy's order routing accounts (OHLCX Pro only). |

Request and response:

- `GET /api/strategy-accounts`. Response: Not relayed. 403 `{ "message": "Order routing accounts are managed in OHLCX Pro.", "error": "Order routing accounts are managed in OHLCX Pro." }`.
- `POST /api/strategy/{strategy}/settings/update-accounts`. Response: Not relayed. The same 403.

Reads in this section, and the relays in the other relayed sections, still answer a failure with `{"error": "message"}` and 500.

---

## Conditions (relayed to the main OHLCX API on Light)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/conditions | Sanctum | List conditions. |
| GET | /api/conditions/{id} | Sanctum | One condition. |
| POST | /api/conditions | Sanctum | Create a condition. |
| PUT | /api/conditions/{id} | Sanctum | Update a condition. |
| DELETE | /api/conditions/{id} | Sanctum | Delete a condition. |

Request and response:

- `GET /api/conditions`. Response: Condition list (cached).
- `GET /api/conditions/{id}`. Response: Single condition.
- `POST /api/conditions`. Request: Condition payload. Response: 201 + data.
- `PUT /api/conditions/{id}`. Request: Condition payload. Response: 200.
- `DELETE /api/conditions/{id}`. Response: 204.

---

## Signals (relayed to the main OHLCX API on Light)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/signals | Sanctum | List signals. |
| DELETE | /api/signals/{id} | Sanctum | Delete a signal. |
| POST | /api/signals/{id}/like, unlike, ignore, unignore, watch, unwatch | Sanctum | Mark a signal for the user. |

Request and response:

- `GET /api/signals`. Response: Signal list (cached).
- `DELETE /api/signals/{id}`. Response: Deletes a signal; failures as under "Failures of strategy and condition writes".
- `POST /api/signals/{id}/like, unlike, ignore, unignore, watch, unwatch`. Response: Marks a signal for the user.

---

## Activities (trading-app)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/activities | Sanctum | List the activities. |
| POST | /api/activities | Sanctum | Log an activity. |
| DELETE | /api/activities/{id} | Sanctum | Delete an activity. |

Request and response:

- `GET /api/activities`. Response: Activity list.
- `POST /api/activities`. Request: Activity payload (optional `advanced_order_type`, max 32 chars). Response: 200 — logs only; does **not** debit credits.
- `DELETE /api/activities/{id}`. Response: 200.

Trimmer billing uses **credit holds** (below), not activity deductions.

---

## Credit holds (trading-app)

Trimmer parent orders: reserve spendable credits (`credits_available_for_automation`), capture on fill, release on cancel/expiry. Idempotent per `(user_id, schwab_parent_order_id)`.

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/credit-holds | Sanctum | List the credit holds. |
| POST | /api/credit-holds/transfer | Sanctum | Move a hold to another parent order. |
| POST | /api/credit-holds | Sanctum | Hold credits for a parent order. |
| POST | /api/credit-holds/capture | Sanctum | Capture a hold. |
| POST | /api/credit-holds/release | Sanctum | Release a hold. |

Request and response:

- `GET /api/credit-holds`. Request: Query: `per_page` (1–50, default 25). Response: Laravel paginator JSON.
- `POST /api/credit-holds/transfer`. Request: `from_schwab_parent_order_id`, `to_schwab_parent_order_id`. Response: `{ transferred: bool }` — **409** if another hold already uses `to`.
- `POST /api/credit-holds`. Request: `schwab_parent_order_id` (required), `broker_account_hash` (optional), `credits_amount` (optional). Response: `{ id, status, schwab_parent_order_id, credits_amount }` — **201** if created, **200** if existing held row; **422** if insufficient spendable credits.
- `POST /api/credit-holds/capture`. Request: `schwab_parent_order_id`. Response: `{ captured: bool }`.
- `POST /api/credit-holds/release`. Request: `schwab_parent_order_id`. Response: `{ released: bool }`.

**Broadcast:** successful hold (new row), capture, release, and transfer dispatch **`UserCreditsUpdated`** on `private-App.Models.User.{userId}` with `held_credits`, `credits_available_for_automation`, and `available_credits`. See [billing-trimmer-credit-holds.md](billing-trimmer-credit-holds.md).

**Offline reconcile (trading-app):** `ReconcileTrimmerCreditHoldsJob` (every 4 min: today's order list, then per-id `GET` for parents missing from that list) and `ReconcileTrimmerCreditHoldsAtEndOfDayJob` (20:00 America/New_York) poll Schwab and bulk capture/release HELD rows when stream/API missed an update. Full flow: [billing-trimmer-credit-holds.md](billing-trimmer-credit-holds.md).

---

## Accounts (schwab-integration)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/accounts | Sanctum | List the linked accounts. |
| GET | /api/accounts/balances | Sanctum | Balance history of every account. |
| GET | /api/accounts/{accountId}/balance | Sanctum | One account's balance history. |
| GET | /api/accounts/{accountId}/growth | Sanctum | One account's growth. |
| GET | /api/accounts/{accountId}/pnl | Sanctum | One account's profit and loss. |

Request and response:

- `GET /api/accounts`. Response: Account list.
- `GET /api/accounts/balances`. Response: Balances.
- `GET /api/accounts/{accountId}/balance`. Response: Balance.
- `GET /api/accounts/{accountId}/growth`. Response: Growth.
- `GET /api/accounts/{accountId}/pnl`. Response: PnL.

---

## Billing (stripe-credits-billing)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| GET | /api/credits | Sanctum | Credits and packages. |
| GET | /api/transaction-history | Sanctum | Billing history. |
| GET | /api/admin/users/{user}/billing | Sanctum (admin) | A user's billing (admin). |
| POST | /api/admin/users/{user}/billing/adjust | Sanctum (admin) | Adjust a user's credits (admin). |
| POST | /api/admin/users/{user}/billing/package | Sanctum (admin) | Set a user's package (admin). |

Request and response:

- `GET /api/credits`. Response: Credits.
- `GET /api/transaction-history`. Response: History.
- `GET /api/admin/users/{user}/billing`. Response: Billing.
- `POST /api/admin/users/{user}/billing/adjust`. Request: Body. Response: 200.
- `POST /api/admin/users/{user}/billing/package`. Request: Body. Response: 200.

---

## Chat (trading-rooms)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| POST | /api/group | Sanctum | Create a room. |
| GET | /api/group/{group} | Sanctum | One room. |
| PUT | /api/group/{group} | Sanctum | Update a room. |
| DELETE | /api/group/{group} | Sanctum | Delete a room. |
| PUT | /api/group/{group}/invite | Sanctum | Invite users to a room. |
| POST | /api/group/{group}/join | Sanctum | Ask to join a room. |
| DELETE | /api/group/{group}/leave | Sanctum | Leave a room. |
| GET | /api/group/{group}/status | Sanctum | A room's status. |
| GET | /api/invites | Sanctum | List invitations. |
| POST | /api/invites | Sanctum | Send an invitation. |
| POST | /api/invites/accept | Sanctum | Accept an invitation. |
| GET | /api/invites/validate/{token} | Sanctum | Check an invitation token. |
| DELETE | /api/invites/{id} | Sanctum | Delete an invitation. |
| POST | /api/invites/{id}/resend | Sanctum | Send an invitation again. |
| POST | /api/join-requests/{joinRequest}/respond | Sanctum | Answer a request to join. |
| POST | /api/message | Sanctum | Send a message. |
| GET | /api/message/older/{message} | Sanctum | Messages older than one message. |
| DELETE | /api/message/{message} | Sanctum | Delete a message. |
| GET | /api/sidebar-conversations | Sanctum | The conversation list. |
| GET | /api/user/{user} | Sanctum | One chat user. |
| GET | /api/user/{user}/status | Sanctum | A chat user's status. |
| GET | /api/users | Sanctum | List chat users. |
| POST | /api/users | Sanctum | Create a chat user. |
| GET | /api/users/{id} | Sanctum | One user. |
| PUT | /api/users/{id} | Sanctum | Update a user. |
| DELETE | /api/users/{id} | Sanctum | Delete a user. |
| POST | /api/user/block-unblock/{user} | Sanctum | Block or unblock a user. |
| POST | /api/user/change-role/{user} | Sanctum | Change a user's role. |

Request and response:

- `POST /api/group`. Request: Group payload. Response: 201.
- `GET /api/group/{group}`. Response: Group.
- `PUT /api/group/{group}`. Request: Group payload. Response: 200.
- `DELETE /api/group/{group}`. Response: 200.
- `PUT /api/group/{group}/invite`. Request: Invite payload. Response: 200.
- `POST /api/group/{group}/join`. Response: 200.
- `DELETE /api/group/{group}/leave`. Response: 200.
- `GET /api/group/{group}/status`. Response: Status.
- `GET /api/invites`. Response: Invites.
- `POST /api/invites`. Request: Invite payload. Response: 200.
- `POST /api/invites/accept`. Request: Body. Response: 200.
- `GET /api/invites/validate/{token}`. Response: Validation.
- `DELETE /api/invites/{id}`. Response: 200.
- `POST /api/invites/{id}/resend`. Response: 200.
- `POST /api/join-requests/{joinRequest}/respond`. Request: Body. Response: 200.
- `POST /api/message`. Request: Message payload. Response: 201.
- `GET /api/message/older/{message}`. Response: Older messages.
- `DELETE /api/message/{message}`. Response: 200.
- `GET /api/sidebar-conversations`. Response: Conversations.
- `GET /api/user/{user}`. Response: User.
- `GET /api/user/{user}/status`. Response: Status.
- `GET /api/users`. Response: Users.
- `POST /api/users`. Request: User payload. Response: 201.
- `GET /api/users/{id}`. Response: User.
- `PUT /api/users/{id}`. Request: User payload. Response: 200.
- `DELETE /api/users/{id}`. Response: 200.
- `POST /api/user/block-unblock/{user}`. Response: 200.
- `POST /api/user/change-role/{user}`. Request: Body. Response: 200.

---

## Support (trading-app)

| Method | URL | Auth | Summary |
|--------|-----|------|---------|
| POST | /api/contact-form | None (CSRF exempt) | Send the contact form. |
| POST | /api/support-request | Sanctum | Send a support request. |
| POST | /api/report-issue | Sanctum | Report an issue. |

Request and response:

- `POST /api/contact-form`. Request: Form fields. Response: 200.
- `POST /api/support-request`. Request: Body. Response: 200.
- `POST /api/report-issue`. Request: Body. Response: 200.

---

## Response structure

- **Success:** JSON body; proxy routes often return the upstream `data` key (e.g. array or object).
- **Error:** `{"error": "message"}` with appropriate status (e.g. 500).
- **Validation:** 422 with Laravel validation error structure.

Run `php artisan route:list --path=api` for the exact list. See `docs/api/openapi.yaml` for an OpenAPI 3 spec.
