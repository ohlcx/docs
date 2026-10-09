# pulse

**Composer:** `ohlcx/pulse` · **Repository:** [github.com/ohlcx/pulse](https://github.com/ohlcx/pulse) (private) · **Edition:** Pro, Light · **Version:** 1.0.23

## Role

Event visibility and Slack alerting for operators. Pulse listens to events fired by the OHLCX packages and by Laravel's sign-in, mail and queue features, sends each to a Slack channel, and writes every occurrence to an event log that the scheduled reports are built from.

It has no API and no user interface. It is not Laravel's own Pulse package.

## What it provides

- **Immediate alerts** for events such as a registration, an admin sign-in, a failed queue job, a new signal or trade, a new booking, and billing events.
- **Digests** for events too frequent to alert one by one, such as strategy evaluations, flags, activity, sign-ins of non-admins, and market and sector balance updates.
- **Scheduled reports**: daily, end of day, weekly and monthly event reports, and weekly reports on revenue, trading rooms activity, brokerage linking and AI usage.
- **An event log** with a retention period, pruned on a schedule.
- Other packages can make an event of their own alert by marking it; Pulse picks it up without a change to Pulse.

## Commands

| Command | Purpose |
|---------|---------|
| `pulse:status` | Diagnoses the event log and recent event counts |
| `pulse:digest`, `pulse:digest-logins`, `pulse:digest-balances`, `pulse:digest-hourly` | Rolling digests |
| `pulse:report-daily`, `pulse:report-eod`, `pulse:report-weekly`, `pulse:report-monthly` | Event reports |
| `pulse:report-revenue`, `pulse:report-community`, `pulse:report-linking`, `pulse:report-ai-usage`, `pulse:report-balances-weekly`, `pulse:report-balances-monthly` | Topic reports |
| `pulse:prune` | Deletes events older than the retention period |

## Configuration

Two Slack webhooks are required, set by name in the host `.env`: `SLACK_ALERT_WEBHOOK_GENERAL` and `SLACK_ALERT_WEBHOOK_GENERAL_BOT`. `PULSE_ENABLED` switches the package off. Each digest and report has its own `PULSE_*` switch, and `PULSE_RETENTION_DAYS` sets how long events are kept.

## Dependencies

It requires no other OHLCX package and listens only to the events of the packages that are installed. trading-app names it as optional.
