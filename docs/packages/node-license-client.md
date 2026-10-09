# node-license-client

**Composer:** `ohlcx/node-license-client` · **Repository:** [github.com/ohlcx/node-license-client](https://github.com/ohlcx/node-license-client) (private) · **Edition:** Pro, Light · **Version:** 1.0.14

## Role

Licensing for self-hosted deployments. A **node** is one self-hosted deployment of OHLCX Pro or OHLCX Light. This package is installed in every deployment: it registers the node with the license server, reports to it on a schedule, and shows a blocked page instead of the application while the node is not licensed.

Its counterpart, the license server, is [node-management](node-management.md).

## How it works

1. **Registration.** A fresh node is unregistered and blocked. An operator activates it through the setup form at `/node-license/setup` or with `node-license:register`. The node receives an id and a secret and waits as pending.
2. **Approval.** An OHLCX admin approves the node on the license server. Until then the application stays blocked.
3. **Heartbeat.** The node reports to the license server every six hours and keeps the status it was given.
4. **Enforcement.** Every web request is checked. A rejected or revoked node is blocked at once. An approved node that cannot reach the license server keeps working for a grace period.
5. **Recheck.** A registered node also asks the license server again on incoming requests, at most once per cooldown, so an approval takes effect when the blocked page is reloaded. The blocked page has a button that asks at once.

Console commands, health checks, the setup and recheck routes and the sign-in cookie endpoint are never blocked, so an unlicensed node can still be operated and activated.

## What it provides

- Setup form and blocked page
- `GET /api/node-license/status` for an admin: the node's own license status, shown on the Licensing page of trading-app's admin area

## Commands

| Command | Purpose |
|---------|---------|
| `node-license:register` | Registers this node with the license server |
| `node-license:heartbeat` | Sends a heartbeat and refreshes the status. Scheduled every six hours |
| `node-license:status` | Shows this node's license status |

## Configuration

Set by name in the host `.env`: `NODE_LICENSE_SERVER_URL`, `NODE_LICENSE_ENFORCE` (the master switch; off for local development), `NODE_LICENSE_GRACE_PERIOD_DAYS`, `NODE_LICENSE_RECHECK_COOLDOWN_SECONDS`, `NODE_LICENSE_SETUP_TOKEN` (protects the setup form), `NODE_LICENSE_RESET_AFTER_AUTH_FAILURES`, `NODE_LICENSE_SUPPORT_EMAIL`.

A node must be served over HTTPS: registration returns the node's secret once.

## Dependencies

It requires no other OHLCX package. **trading-app** requires it.
