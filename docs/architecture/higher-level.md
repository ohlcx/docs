
Run php artisan route:list and explain the API design

What php artisan route:list shows
Key API routes (all prefixed with /api) include:

Accounts (brokerage integration, Schwab)

GET /api/accounts, /api/accounts/balances, /api/accounts/{accountId}/balance|growth|pnl → OHLCX\Schwab\AccountGrowthController@*
These expose portfolio, balance, PnL, and growth data from the brokerage integration.
Activities & logging

POST /api/activities, GET /api/activities, DELETE /api/activities/{id} → OHLCX\TradingApp\ActivityController
Generic user activity logging and retrieval for the app.
Admin billing & credits

GET /api/admin/users/{user}/billing, plus /billing/adjust, /billing/package → OHLCX\CreditsBilling\AdminBillingController@*
GET /api/credits, GET /api/transaction-history → credit balance and billing history
Web routes like GET /buy-credits/{package}, Stripe webhook at POST /stripe/buy-credits/webhook.
Markets & instruments (proxied via OHLCXApiService) – defined in routes/remote.php

GET /api/markets/{marketId?} – market list or specific market.
GET /api/tickers/{symbol?} with market_id optional query param.
GET /api/market-calendar – market schedule.
POST /api/market-balance – validated market balance query.
All of these use OHLCXApiService + Cache::remember(...) to proxy to a backend OHLCX API and cache responses for ~1 minute.
News & analysis (also via OHLCXApiService)

GET /api/popular-news, /api/crypto-news, /api/news – cached for 1 minute.
GET /api/legacy_analysis – older analysis endpoint (cached).
GET /api/analysis – newer AI-driven analysis assembled from OHLCX\TradingRooms\Models\Message plus S3-hosted attachments and ai_calls; returns normalized JSON for the frontend.
Strategies & conditions (core trading logic facade) – heavily structured and REST-ish

Base strategies CRUD:
GET /api/strategies – index (cached).
GET /api/strategies/{id} – show.
POST /api/strategies – create.
PUT /api/strategies/{id} – update.
DELETE /api/strategies/{id} – delete.
GET /api/strategies/search/{symbol} – symbol-based search (cached).
These all call OHLCXApiService (get/post/put/delete) and maintain a small cache (strategies, strategies_search_{symbol}).
Strategy actions under a prefix group: Route::prefix('strategy/')->name('strategy.')->group(...):
Settings endpoints (all POST /api/strategy/{strategy}/settings/*): update-name, update-symbol, update-direction, update-timeframe, update-allocation, update-sizing-ordering, update-trailing-stop, update-order-cancelation, update-slack-webhook-url.
Lifecycle/behavior: retain, retain-stop, deploy.
Status toggles: status/on|off, signals/on|off|toggle, trades/on|off|toggle, orders/on|off|toggle.
Notification toggles: /notifications/signals/*, /notifications/trades/*, /notifications/orders/*, including Slack test notification.
Strategy-related data: GET /api/strategy/{strategy}/conditions and POST /api/strategy/{strategy}/clear-conditions-readings, GET /api/strategy/{strategy}/activities.
All these are thin facades: they forward to equivalent upstream paths (same URI after strategy/...) via OHLCXApiService, then return data['data'] JSON and clear appropriate caches (strategies, conditions).
Conditions (global) – separate from the per-strategy endpoints

GET /api/conditions, GET /api/conditions/{id}, POST /api/conditions, PUT /api/conditions/{id}, DELETE /api/conditions/{id}.
Again, pure proxy to upstream conditions endpoints with 1-minute caching and cache invalidation on write.
Signals

GET /api/signals – lists signals from upstream via OHLCXApiService, cached.
Chat / trading rooms (TradingRooms package)

Group endpoints: POST /api/group, GET|PUT|DELETE /api/group/{group}, plus /invite, /join, /leave, /status.
Invites: GET|POST /api/invites, POST /api/invites/accept, GET /api/invites/validate/{token}, DELETE /api/invites/{id} + /delete + /resend.
Join-requests: POST /api/join-requests/{joinRequest}/respond.
Messages: POST /api/message, GET /api/message/older/{message}, DELETE /api/message/{message}.
Conversation lists: GET /api/sidebar-conversations.
User-level chat helpers: GET /api/user/{user}, GET /api/user/{user}/status, GET /api/users, POST /api/users, GET|PUT|DELETE /api/users/{id}, POST /api/user/block-unblock/{user}, POST /api/user/change-role/{user}.
All these map to OHLCX\TradingRooms\ApiController and related package controllers.
Auth & user lifecycle (API-facing)

POST /api/login, POST /api/register → OHLCX\TradingApp\AuthController.
Password reset: POST /api/password/email, POST /api/password/reset.
Email verification: GET /api/email/verify (named api.verification.verify).
Multi-factor: POST /api/two-factor-challenge.
User info: GET /api/user (also the default route from routes/api.php).
There is also the standard Fortify/Jetstream web auth surface (login, logout, user/profile, two-factor routes, etc.) for non-API usage.
User profile, settings, onboarding

DELETE /api/user-profile + other profile routes (/email/verification-notification, /logout-other-sessions, /password, /profile, /profile-information, /profile-photo, /sessions) → OHLCX\UserProfile\UserProfileController style routes.
GET|POST /api/user/onboarding → UserOnboardingController.
GET|POST /api/user/preferences → UserPreferencesController.
GET|POST /api/user/settings → UserSettingsController.
Support & contact

POST /api/contact-form and POST /api/report-issue → SupportController.
These are open to the SPA, with CSRF disabled just for api/contact-form (per bootstrap/app.php).
Other system/infra routes

Horizon (/horizon/*), Telescope (/telescope/*), Livewire JS endpoints, Sanctum’s sanctum/csrf-cookie, broadcast auth, etc. – all standard Laravel ecosystem tooling, not part of your public JSON API surface for the SPA.
Design patterns & key characteristics
SPA-centric, Sanctum-protected API:

Most /api/* endpoints sit behind auth:sanctum (and often verified) middleware in routes/remote.php.
The React app under /trading uses these routes as its backend, with cookie-based Sanctum auth and CSRF provided via sanctum/csrf-cookie and global CSRF middleware.
Thin facade over an upstream OHLCX backend:

routes/remote.php shows a very consistent pattern: each Laravel route is a thin proxy to a same-named path on a remote OHLCX API, via OHLCXApiService.
Caching is centralized via Laravel’s Cache::remember() for read-heavy endpoints (markets, tickers, strategies, conditions, signals, news).
Write operations (POST/PUT/DELETE) immediately invalidate pertinent caches to keep the SPA view in sync.
Resource-oriented, domain-based grouping:

Domains: markets, tickers, strategies, conditions, signals, activities, accounts, user-profile, billing/credits, chat/trading rooms, support.
Strategies and conditions follow familiar REST verbs, with an additional layer of action endpoints (deploy, retain, status/*, notifications/*) grouped under strategy/{strategy}.
Named routes (e.g. search-strategy, many strategy.* names, chat route names) give the PHP side semantic handles, though the SPA mostly talks by URL.
Clear separation of concerns:

Package controllers (OHLCX\TradingApp, OHLCX\TradingRooms, OHLCX\CreditsBilling, OHLCX\Schwab, OHLCX\UserProfile) encapsulate domain-specific logic.
routes/remote.php is focused on proxying to the OHLCX API, while those controllers manage internal state (users, sessions, billing, chat) and integrations (Schwab, Stripe).
In short, the API is designed as a Laravel façade in front of multiple OHLCX domain services plus a remote OHLCX HTTP API, exposing a REST/JSON surface under /api/* for the /trading React SPA, with Sanctum-based auth, short-lived caching for read endpoints, and a very granular set of POST-only endpoints for toggling trading strategy behavior and notifications.