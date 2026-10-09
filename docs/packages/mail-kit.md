# mail-kit

**Composer:** `ohlcx/mail-kit` · **Repository:** [github.com/ohlcx/mail-kit](https://github.com/ohlcx/mail-kit) (private) · **Edition:** Pro, Light · **Version:** 1.0.15

## Role

The shared email layer of the OHLCX packages: one branded layout for custom emails, a matching theme for Laravel's standard notification emails, and unsubscribe handling that applies to every email the application sends.

## What it provides

- **Layout and button component** that the other packages' emails extend, so every email has the same header, panel and footer.
- **A replacement for Laravel's notification email view**, so a plain notification is rendered in the same layout.
- **Unsubscribe and suppression.** A signed unsubscribe link (`/unsubscribe`), a list of suppressed addresses, and a listener that blocks delivery to a suppressed address for every outgoing email.
- **A promotional campaign email** and a command to send it to a list of recipients.

## Commands

| Command | Purpose |
|---------|---------|
| `mail:test-all` | Renders, sends or screenshots every email the packages have registered, for a visual check |
| `mail:send-promo-campaign` | Sends the promotional email to a list of recipients, skipping unsubscribed addresses |
| `mail:purge-suppressed-queue` | Removes queued emails addressed to a suppressed recipient. Scheduled daily |

## Host setup

```bash
php artisan migrate
```

There is no config to publish. The migration is required: the delivery check reads the suppression table on every outgoing email.

## Dependents

Required by **trading-app**, **schwab-integration**, **trading-rooms**, **booking**, **referrals**, **strategies** and **node-management**. It requires no other OHLCX package.
