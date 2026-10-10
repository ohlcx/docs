# Domain Packages (vendor/ohlcx)

Private Laravel packages under `vendor/ohlcx/` and how the two applications use them. OHLCX Pro installs 21 of them and OHLCX Light 13: every package Light installs, Pro installs too. This page says briefly what each one is for; the Packages section of the public documentation (Packages, Ecosystem) has a page of detail for the main ones.

---

## 1. Overview

| Package | Pro | Light | Purpose |
|---------|-----|-------|---------|
| **trading-app** | yes | yes | Auth, activities, support, onboarding, preferences, settings, email verification, **knowledge base** (KB API), Trimmer credit holds, the MCP server and the in-app assistant. |
| **trading-rooms** | yes | yes | Chat: groups, invites, messages, users, sidebar conversations, join-requests, AI calls. |
| **user-profile** | yes | yes | Profile, sessions, password, profile-information, profile-photo, delete user. |
| **stripe-credits-billing** | yes | yes | Ledger credits, transactions, packages, Stripe checkout, and admin billing. |
| **schwab-integration** | yes | yes | Broker integration: accounts, balances, growth, PnL, TD auth, token webhook. |
| **tdameritrade-laravel** | yes | yes | TD/Schwab API client (used by schwab-integration). |
| **booking** | yes | yes | Public scheduling: event types, availability rules, blocked dates, admin booking management, ICS + reminder emails. |
| **goals** | yes | yes | Trading goal targets and progress tracking (day P&L stamps, admin targets). |
| **referrals** | yes | yes | Referral program: invitations, referral claims/clicks, qualification and reward services. |
| **node-license-client** | yes | yes | License **client** (every non-authority node): registers with the authority, heartbeats, blocks the app if unlicensed. |
| **pulse** | yes | yes | Internal telemetry/reporting: listens for app events (billing, trading-rooms, users, queue, nodes) and sends digests/reports (daily, weekly, AI usage, revenue, community) via Slack/mail. |
| **mail-kit** | yes | yes | Shared mail infrastructure: promo campaigns, unsubscribe handling, suppression list, transactional layout/components. |
| **chat-bots** | yes | yes | Simulated/bot users for trading-rooms (demo/load-testing presence, live rooms, random clients). |
| **strategies** | yes | no | The strategies centre: strategies, conditions, signals, trades, backtests, screeners and order routing. Light reads and writes these through the main OHLCX API. |
| **pricefeed** | yes | no | Markets, tickers and price bars. |
| **sectors** | yes | no | Sector definitions, ticker pivots, balance snapshots and the sector balance charts. |
| **news** | yes | no | Featured news and articles. |
| **analysis** | yes | no | Technical analysis items and articles. |
| **alpaca-trade-api-php** | yes | no | Client for the Alpaca trade API. |
| **development-features** | yes | no | Broadcasting lifecycle, channels and the data streaming API. |
| **node-management** | yes | no | License **authority** (central install only): node registration, heartbeat, admin approval. |
| **ai-dev** (internal) | no | no | Internal AI development sandbox for maintainers only, not part of the public product surface. |

The applications do **not** implement these domains in `app/`; they register package routes and use their traits/controllers. The eight packages only Pro installs hold the market and strategy data: Light reaches the same data through the main OHLCX API (see [API_DATA_SOURCES.md](API_DATA_SOURCES.md)), which is why its strategy, signal, market and news screens work without them. The sections below describe the packages both applications install.

---

## 2. trading-app

**Purpose:** Auth, user lifecycle, activities, support, onboarding, preferences, settings, **knowledge base** (product/feature KB API), and Trimmer credit holds.

**Main classes / entry points:**

- **Controllers:** AuthController (login, register, twoFactorChallenge), PasswordResetController (password/email, password/reset), ActivityController (log, list, delete), SupportController (contact_form, support_request, report_issue), UserOnboardingController, UserPreferencesController, UserSettingsController, EmailVerificationController, **KnowledgeBaseController** (index, show), **CreditHoldController** (Trimmer reserve/capture/release/transfer).
- **Models:** Activity, **CreditHold**, **KnowledgeBaseArticle** (KB lives in this package at `vendor/ohlcx/trading-app`).
- **Services:** **CreditHoldService** (Trimmer hold / capture / release / transfer).
- **Jobs:** **ReconcileTrimmerCreditHoldsJob** (every 4 min); **ReconcileTrimmerCreditHoldsAtEndOfDayJob** (20:00 NY).
- **Support:** **TrimmerCreditHoldOrderActionMapper** (Schwab status → capture / release for reconcile).
- **Events:** ActivityLogged, **UserCreditsUpdated** (credit balance broadcast).
- **Listeners:** **AttachCreditHoldToActivityListener** (link Trimmer `OrderCreated` activities to holds when TradeTag is allowlisted).
- **Mail:** ContactFormSubmitted, SupportRequested, IssueReported.
- **Config:** social-login, horizon (if any).
- **Traits:** UseTradingAppTrait (for registering routes/views).

**How the app uses it:**

- `routes/api.php` is extended by the package’s API routes (login, register, password/*, two-factor-challenge, activities, contact-form, support-request, report-issue, user/onboarding, user/preferences, user/settings, email/verify, **knowledge-base**, **knowledge-base/{slug}**, **credit-holds**).
- SPA entry routes (`/trading`, `/trading/*`) may be registered by this package’s web routes.
- No app-level controllers; the app just loads the package and uses its routes.
- Trimmer billing: see **[billing-trimmer-credit-holds.md](billing-trimmer-credit-holds.md)** (`/api/credit-holds*`, Echo `UserCreditsUpdated`).

**Trimmer credit-hold ownership:**

- **trading-app** owns the `/api/credit-holds*` API, `credit_holds` table, hold lifecycle service, user balance broadcasts, and `held_credits` / `credits_available_for_automation` aggregates.
- **stripe-credits-billing** owns ledger credits, packages, purchases, transaction history, and the usage rows created when a hold is captured; temporary hold rows do not belong to that package.
- The SPA touches holds through `resources/js/helpers/creditHoldApi.js`, `resources/js/managers/OrdersManager.jsx`, `resources/js/hooks/SchwabWebSocketProvider.jsx`, `resources/js/hooks/useCreditsGate.jsx`, and `resources/js/pages/CreditsPage.jsx`.
- See `docs/billing-trimmer-credit-holds.md`, `docs/api-reference.md#credit-holds-trading-app`, and `resources/js/managers/ORDERS_STREAM.md` for endpoint details, realtime behavior, and stream lifecycle constraints.

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

**Purpose:** Ledger credits, transactions, packages, Stripe checkout, and admin billing.

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
- Trimmer credit holds are intentionally outside this package; use `/api/credit-holds*` from **trading-app** for held/spendable automation balances and lifecycle changes.

**Recommendations:**

- Document webhook payload and idempotency if not already.
- Keep this package responsible for Stripe checkout, credit purchases, ledger balance, and transaction history; do not duplicate those concerns in the app layer.
- Keep Trimmer hold lifecycle changes in **trading-app** so ledger credits and temporary order holds remain separate domains.

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
- Trimmer credit-hold reconcile runs in **trading-app** (uses Schwab tokens from this package); see **[billing-trimmer-credit-holds.md](billing-trimmer-credit-holds.md)**.

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

## 8. booking

**Purpose:** Public scheduling — event types, availability rules, blocked dates, bookings, ICS invites and reminder emails.

**Main classes:**

- **Controllers (admin):** AdminEventTypeController, AdminAvailabilityRuleController, AdminBlockedDateController, AdminBookingController.
- **Controllers (public):** PublicEventTypeController, PublicAvailabilityController, PublicBookingController, PublicCancelController.
- **Models:** EventType, AvailabilityRule, BlockedDate, Booking.
- **Services:** AvailabilityService, BookingCreationService, IcsGenerator, RecaptchaVerifier.
- **Events/Listeners:** BookingCreated → SendBookingCreatedNotifications.
- **Mail:** BookingConfirmed, BookingCancelled, BookingMeetingLinkAdded, BookingReminder.
- **Commands:** BookingSeedCommand, SendBookingRemindersCommand.
- **Config:** `BOOKING_BUSINESS_TIMEZONE`, `BOOKING_SLOT_INTERVAL_MINUTES`, `BOOKING_MIN_NOTICE_MINUTES`, `BOOKING_MAX_ADVANCE_DAYS`, `BOOKING_TEAM_EMAIL`, `BOOKING_PUBLIC_CORS_ORIGINS` (falls back to `RECAPTCHA_SECRET_KEY` if `BOOKING_RECAPTCHA_SECRET_KEY` unset).

**How the app uses it:**

- Public booking API is intentionally exposed cross-origin (see `config/cors.php` + `BOOKING_PUBLIC_CORS_ORIGINS`) so the marketing site can book meetings without a logged-in session.
- Admin endpoints manage event types, availability, and blocked dates from inside the app.

---

## 9. goals

**Purpose:** Trading goal targets and progress tracking, driven off P&L sync.

**Main classes:**

- **Controllers:** MyGoalTargetController, MyGoalProgressController, MyGoalProgressStampObserveController, AdminGoalTargetController.
- **Models:** GoalTarget, GoalProgressStamp.
- **Services:** GoalTargetService, GoalProgressService, GoalProgressStampService, GoalRealizedCrossingService, GoalsAccountResolver.
- **Events/Listeners:** GoalProgressStampUpdated; `ReconstructGoalStampsOnPnlSyncFinished` rebuilds progress stamps whenever the (schwab-integration) P&L sync finishes.
- **Traits:** UseGoalsTrait (added to the `User` model).

**How the app uses it:**

- Reacts to P&L sync events from **schwab-integration** to keep goal progress current; no app-level controllers.

---

## 10. referrals

**Purpose:** Referral program — invitations, referral tracking/claims, qualification milestones, rewards.

**Main classes:**

- **Controllers:** MyInvitationController, MyReferralController, AdminInvitationController, AdminReferralController, AdminReferralSettingsController, PublicInvitationController, PublicReferralClaimController, PublicReferralClickController.
- **Models:** Invitation, Referral, ReferralSettings.
- **Services:** InvitationCreationService, InvitationAcceptanceService, ReferralClaimService, ReferralValueService, ReferralRewardService, QualificationService.
- **Mail:** InvitationMail.
- **Traits:** UseReferralsTrait (added to the `User` model, adds `referral_code` and click tracking).

**How the app uses it:**

- Public click/claim endpoints track referral links; qualification milestones and reward payout are computed server-side and surfaced through the admin referral settings.

---

## 11. node-management / node-license-client

**Purpose:** Self-hosted "node" licensing for on-prem/private deployments. Two complementary packages — only one is active per install.

- **node-management** (central authority — one install only): node registration, heartbeat verification, admin approval queue.
  - **Controllers:** NodeRegistrationController, NodeHeartbeatController, Admin\NodeAdminController.
  - **Models:** Node. **Events:** NodeRegistered. **Notifications:** NodeAwaitingApprovalNotification (emails admins on new registration).
  - **Middleware:** VerifyNodeSecret. **Commands:** FlagStaleNodesCommand.
  - **Config:** `NODE_MANAGEMENT_ENABLED` (false by default), `NODE_MANAGEMENT_GRACE_PERIOD_DAYS`, `NODE_MANAGEMENT_NOTIFY_ADMINS`.

- **node-license-client** (every other node, including this install): registers with the authority, heartbeats, blocks the app if the license is invalid/revoked.
  - **Controllers:** NodeLicenseController, NodeLicenseStatusController, NodeSetupController.
  - **Middleware:** EnsureNodeIsLicensed (live-rechecks with the license server, subject to a cooldown; blocks with a support-contact page on rejection).
  - **Services:** NodeLicenseManager. **Commands:** RegisterNodeCommand, HeartbeatNodeCommand, NodeStatusCommand.
  - **Config:** `NODE_LICENSE_SERVER_URL`, `NODE_LICENSE_CHECK_INTERVAL_MINUTES`, `NODE_LICENSE_GRACE_PERIOD_DAYS`, `NODE_LICENSE_ENFORCE` (the authority install sets this `false`), `NODE_LICENSE_RECHECK_COOLDOWN_SECONDS`, `NODE_LICENSE_SUPPORT_EMAIL`, `NODE_LICENSE_RESET_AFTER_AUTH_FAILURES` (consecutive 401s before the node assumes its record was deleted and re-registers).

**Recommendations:**

- Never enable both packages' enforcement on the same install — `node-management` is the authority, everything else runs `node-license-client` against it.

---

## 12. pulse

**Purpose:** Internal telemetry and operational reporting — listens for domain events across the app and packages, sends digests/reports (Slack and/or mail).

**Main classes:**

- **Listeners:** ActivityListener, BillingListener, StripeBillingListener, MailListener, NodeListener, QueueListener, TradingRoomsListener, UserEventListener, WildcardListener.
- **Reports:** ReportBuilder, BalanceReportBuilder, RevenueReportBuilder, AiUsageReportBuilder, CommunityReportBuilder, LinkingAccountsReportBuilder.
- **Commands:** SendDailyReport, SendHourlyDigest, SendWeeklyReport, SendMonthlyReport, SendEndOfDayReport, SendBalanceDigest/WeeklyReport/MonthlyReport, SendActivityDigest, SendLoginDigest, SendAiUsageReport, SendRevenueReport, SendCommunityReport, SendLinkingAccountsReport, PruneEvents, StatusCheck.
- **Slack:** DispatchSlackAlert, SlackMessage, AlertRouter, ThrottleGuard (rate-limits repeat alerts).
- **Models:** PulseEvent (event log the reports/digests are built from).

**How the app uses it:**

- Passive — subscribes to events emitted by other packages (billing, trading-rooms, nodes, mail, queue, user actions) and schedules recurring report/digest commands; no app-level controllers or routes.

---

## 13. mail-kit

**Purpose:** Shared mail infrastructure — promo campaigns, unsubscribe/suppression handling, transactional layout components.

**Main classes:**

- **Controllers:** UnsubscribeController.
- **Models:** EmailSuppression.
- **Mail:** PromoCampaignMail.
- **Listeners:** BlockSuppressedRecipients (guards outbound mail against the suppression list).
- **Commands:** SendPromoCampaign, TestAllMail, PurgeSuppressedQueueJobs.
- **Views:** shared layout/header/footer/button components used by transactional mail across packages (booking, referrals, etc.).

**How the app uses it:**

- Other packages' mailables build on `mail-kit`'s layout components; `BlockSuppressedRecipients` is a cross-cutting guard so any package sending mail respects unsubscribes.

---

## 14. chat-bots

**Purpose:** Simulated/bot users for **trading-rooms** — demo data and load/presence testing, not a customer-facing feature.

**Main classes:**

- **Commands:** GenerateBotUsersCommand, CleanBotUsersCommand, SimulateClientsCommand, SimulateRandomClientsCommand, SimulateLiveRoomCommand, SimulatePresenceCommand.
- Adds an `is_chat_bot` flag to the `users` table (migration) so bot accounts are distinguishable from real users.

**How the app uses it:**

- Dev/staging tooling only — generates and drives bot users inside trading-rooms for demoing chat activity or presence load-testing.

---

## 15. Summary diagram

```
Laravel App (routes/api.php + remote.php)
        │
        ├──► trading-app      → auth, activities, support, onboarding, preferences, settings, knowledge base, Trimmer credit holds
        ├──► trading-rooms    → chat (groups, invites, messages), analysis data
        ├──► user-profile     → profile, sessions, password, delete user
        ├──► stripe-credits-billing → ledger credits, transactions, Stripe, admin billing
        ├──► schwab-integration → accounts, balances, growth, PnL, TD auth
        ├──► tdameritrade-laravel  → TD/Schwab API client (used by schwab-integration)
        ├──► booking          → public scheduling, availability, ICS invites
        ├──► goals            → trading goal targets & progress (driven by P&L sync)
        ├──► referrals        → invitations, referral tracking, rewards
        ├──► node-management / node-license-client → self-hosted node licensing (authority vs. client)
        ├──► pulse            → cross-package event telemetry, Slack/mail digests & reports
        ├──► mail-kit         → shared mail layout, promo campaigns, unsubscribe/suppression
        └──► chat-bots        → simulated bot users for trading-rooms (dev/demo only)
```

See also: `docs/architecture.md`, `docs/backend.md`, `docs/api-reference.md`.
