# node-management

**Composer:** `ohlcx/node-management` · **Repository:** [github.com/ohlcx/node-management](https://github.com/ohlcx/node-management) (private) · **Edition:** Pro · **Version:** 1.0.13

## Role

The license server for self-hosted deployments. A **node** is one self-hosted deployment of OHLCX Pro or OHLCX Light. This package turns one OHLCX Pro deployment into the license authority that every node registers with and reports to through [node-license-client](node-license-client.md).

It is installed in every Pro deployment and is **dormant by default**. Only the one authority operated by OHLCX switches it on; everywhere else its routes do not exist.

## What it provides

- **Registration**: `POST /api/nodes/register`. Public and rate limited. A node sends its name, a contact email and a fingerprint of its installation, and receives an id and a secret that is shown once.
- **Heartbeat**: `POST /api/nodes/{uuid}/heartbeat`, authenticated with the node's id and secret. The server records when and from where the node was last seen, and answers with the node's status.
- **Admin API** under `/api/node-management/admin` for an admin: list and read nodes, approve, reject, revoke, edit notes, delete. The Nodes page of trading-app's admin area uses it.
- **Notifications**: admins are emailed when a node registers and waits for approval; the node's contact is emailed when it is approved, rejected or revoked.
- **Stale nodes**: an approved node that has not reported within the grace period is logged for the admins. Nothing is revoked automatically.

A node moves from pending to approved, rejected or revoked. Only an approved node runs the application.

## Commands

| Command | Purpose |
|---------|---------|
| `node-management:flag-stale` | Logs approved nodes that have not reported within the grace period. Scheduled daily when the package is switched on |

## Configuration

Set by name in the host `.env`: `NODE_MANAGEMENT_ENABLED` (the master switch, off by default), `NODE_MANAGEMENT_GRACE_PERIOD_DAYS`, `NODE_MANAGEMENT_NOTIFY_ADMINS`, `NODE_MANAGEMENT_NOTIFY_CUSTOMER`, `NODE_MANAGEMENT_SUPPORT_EMAIL`.

## Dependencies

Requires **mail-kit**.

## Related

- [node-license-client](node-license-client.md)
