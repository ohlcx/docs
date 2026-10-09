# referrals

**Composer:** `ohlcx/referrals` · **Repository:** [github.com/ohlcx/referrals](https://github.com/ohlcx/referrals) (private) · **Edition:** Pro, Light · **Version:** 1.0.24

## Role

Invitations between users and a referral program. A signed-in user can invite a friend by email, or share a permanent referral code and link with which a visitor asks for access. When the referred user reaches a milestone, the referrer receives a credit reward once.

This is separate from the admin invitations of **trading-rooms**, which are an onboarding tool for admins.

## What it provides

- **Invitations by email** and **claims of a referral code**. Both end at the same acceptance step, which creates the user and records who referred them.
- **Qualification.** A referral qualifies when the referred user links a broker account or makes a first paid credits purchase, whichever comes first.
- **Reward.** On qualification the referrer is granted credits through **stripe-credits-billing**. If that package is not installed, the referral stays qualified and no reward is granted.
- **Public API** under `/api/referrals`: read an invitation, accept it, claim a code, record a link click. Rate limited.
- **User API** under `/api/referrals` for a signed-in user: their code, link and counts, the invitations they sent (send one, send several, revoke), and the people they referred.
- **Admin API** under `/api/referrals/admin`: all invitations and referrals, a manual reward, and the program's settings.
- The Referrals page and the admin referrals page of trading-app use this API.

## Configuration

Set by name in the host `.env`: `REFERRALS_INVITATION_EXPIRES_DAYS`, `REFERRALS_CODE_LENGTH`, `REFERRALS_MAX_PENDING_INVITATIONS`, `REFERRALS_MAX_BULK_INVITATIONS`, `REFERRALS_FALLBACK_VALUE_PER_CREDIT`.

## Dependencies

Requires **mail-kit**. It works with **stripe-credits-billing** (the reward) and **schwab-integration** (the broker account milestone) when they are installed, without requiring them. trading-app names it as optional.

## Related

- [stripe-credits-billing](stripe-credits-billing.md)
