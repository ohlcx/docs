# booking

**Composer:** `ohlcx/booking` · **Repository:** [github.com/ohlcx/booking](https://github.com/ohlcx/booking) (private) · **Edition:** Pro, Light · **Version:** 1.0.18

## Role

Self-hosted scheduling. A visitor picks a session type, sees the free slots, and books one without an account. Admins manage bookings, weekly availability, blocked dates and session types.

There is no external calendar integration and no generated meeting link: an admin adds the meeting link to a booking.

## What it provides

- **Session types** with a duration, buffers before and after, and optional notice and advance limits.
- **Availability**: recurring weekly hours, minus blocked dates, minus existing bookings and buffers, within a minimum notice and a maximum advance.
- **Public API** under `/api/booking`: session types, availability for one type, create a booking, and cancel through the link in the confirmation email. No sign-in; creating and cancelling are rate limited. Two visitors cannot book the same slot.
- **Admin API** under `/api/booking/admin` for an admin: bookings (list, read, update notes and meeting link, cancel), session types, availability rules, blocked dates.
- **Emails**: a confirmation with a calendar file to the visitor, a notification to the team, a notice when a meeting link is added, a cancellation notice, and reminders 24 hours and 1 hour before.
- The admin bookings page of trading-app uses the admin API.

## Commands

| Command | Purpose |
|---------|---------|
| `booking:seed` | Seeds default session types, weekday availability and public holidays as blocked dates |
| `booking:send-reminders` | Sends the 24 hour and 1 hour reminders. Scheduled every five minutes. `--dry-run` only logs |

## Configuration

Set by name in the host `.env`: `BOOKING_BUSINESS_TIMEZONE`, `BOOKING_SLOT_INTERVAL_MINUTES`, `BOOKING_MIN_NOTICE_MINUTES`, `BOOKING_MAX_ADVANCE_DAYS`, `BOOKING_TEAM_EMAIL`, `BOOKING_REMINDER_24H_ENABLED`, `BOOKING_REMINDER_1H_ENABLED`, `BOOKING_RECAPTCHA_SECRET_KEY`, `BOOKING_PUBLIC_CORS_ORIGINS`.

## Dependencies

Requires **mail-kit**. trading-app names it as optional.
