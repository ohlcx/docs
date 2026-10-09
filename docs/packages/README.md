# Package ecosystem

OHLCX is built from **private Composer packages** under the [github.com/ohlcx](https://github.com/ohlcx) organization. This page lists every `ohlcx/*` package the two applications install, what each one is for, and how they depend on each other. Source requires authorized access.

The lists and versions on this page are read from the applications' `composer.json` and `composer.lock`. The dependency diagram is read from each package's own `composer.json`.

## Applications

| Repository | Edition | `ohlcx/*` packages installed |
|------------|---------|------------------------------|
| [ohlcx/ohlcx](https://github.com/ohlcx/ohlcx) | **Pro** | 21: alpaca-trade-api-php, analysis, booking, chat-bots, development-features, goals, mail-kit, news, node-license-client, node-management, pricefeed, pulse, referrals, schwab-integration, sectors, strategies, stripe-credits-billing, tdameritrade-laravel, trading-app, trading-rooms, user-profile |
| [ohlcx/ohlcx-light](https://github.com/ohlcx/ohlcx-light) | **Light** | 13: booking, chat-bots, goals, mail-kit, node-license-client, pulse, referrals, schwab-integration, stripe-credits-billing, tdameritrade-laravel, trading-app, trading-rooms, user-profile |

Pro installs everything Light installs, plus eight packages of its own.

## Packages in both editions

| Package | Responsibility | Version (Pro / Light) | Page |
|---------|----------------|-----------------------|------|
| trading-app | The application layer: trading UI, API routes, relay to the hosted API on Light, knowledge base, in-app assistant, MCP server | 1.0.352 / 1.0.351 | [trading-app](trading-app.md) |
| schwab-integration | Schwab account and token management: linked accounts, balances, profit and loss, cash transfers, order reads | 1.0.49 | [schwab-integration](schwab-integration.md) |
| tdameritrade-laravel | Low-level client for the TD Ameritrade / Schwab API | 1.0.20 | [tdameritrade-laravel](tdameritrade-laravel.md) |
| stripe-credits-billing | Credits bought through Stripe Checkout, and their use | 1.0.34 | [stripe-credits-billing](stripe-credits-billing.md) |
| trading-rooms | Realtime messaging: direct messages, rooms, invites, live sessions | 1.0.49 | [trading-rooms](trading-rooms.md) |
| user-profile | Profile management components and API | 1.012 | [user-profile](user-profile.md) |
| goals | Realized P&L goals per linked account: daily, weekly and monthly targets and a progress calendar, read from schwab-integration's P&L | 1.0.11 | [goals](goals.md) |
| mail-kit | Shared branded email layout and notification theme, with unsubscribe and suppression for every outgoing email | 1.0.15 | [mail-kit](mail-kit.md) |
| booking | Self-hosted scheduling: session types, availability, public booking without an account, admin management, reminder emails | 1.0.18 | [booking](booking.md) |
| referrals | Invitations between users and a referral program: referral codes, qualification, and a credit reward for the referrer | 1.0.24 | [referrals](referrals.md) |
| pulse | Operator visibility: Slack alerts, digests and scheduled reports from the events of the installed packages | 1.0.23 | [pulse](pulse.md) |
| node-license-client | Licensing of a self-hosted deployment (a node): registers with the license server, reports to it, and blocks the application while unlicensed | 1.0.14 | [node-license-client](node-license-client.md) |
| chat-bots | Simulated chat users for load-testing and demonstrating trading-rooms' realtime messaging. A testing tool | 1.0.7 | [chat-bots](chat-bots.md) |

## Pro-only packages

| Package | Responsibility | Version | Page |
|---------|----------------|---------|------|
| strategies | Strategies center: conditions, signals, trades, backtests, the screener, and routing a strategy's orders to the owner's linked brokerage accounts | 1.5.0 | [strategies](strategies.md) |
| pricefeed | Market and ticker price data, technical analysis, live price publishing | 1.0.44 | [pricefeed](pricefeed.md) |
| sectors | Sector definitions, sector tickers, sector balance snapshots and charts | 1.0.12 | [sectors](sectors.md) |
| news | Featured news and articles | 1.0.15 | [news](news.md) |
| analysis | Scheduled ticker analysis snapshots | 1.0.14 | [analysis](analysis.md) |
| alpaca-trade-api-php | PHP SDK for the Alpaca API. In OHLCX it is used for market data and news | 1.0.15 | [alpaca-trade-api-php](alpaca-trade-api-php.md) |
| development-features | Development features: market data stream listeners, broadcast channels and components built on them | 1.0.2 | [development-features](development-features.md) |
| node-management | The license server for self-hosted deployments: node registration, heartbeat, admin approval. Dormant except on the one license authority | 1.0.13 | [node-management](node-management.md) |

OHLCX Light does not install these. It reaches strategies, markets, sectors, news and analysis through the **hosted OHLCX API**, relayed by trading-app. See [Light vs Pro](../architecture/light-vs-pro.md).

## Not installed by either application

Two packages of the organization are not required by Pro or Light and are not part of this section: **proxymanager** (an HTTP proxy manager, listed here in earlier editions) and **support** (a client support and ticketing platform).

## Dependencies

The packages require each other in 23 places. Each one is a `require` in a package's own `composer.json`. The two diagrams and the note between them show all 23: 9 in the first diagram, 5 in the note, 9 in the second diagram. An arrow points from a package to the package it requires. Each diagram reads left to right and grows downward, so it stays readable on a narrow screen.

### Shared packages: who requires whom

The 13 packages both editions install. 9 requirements are drawn.

```mermaid
flowchart LR
  classDef shared fill:#0e7490,stroke:#67e8f9,color:#ffffff,stroke-width:1px;
  ta[trading-app]:::shared
  schwab[schwab-integration]:::shared
  rooms[trading-rooms]:::shared
  bots[chat-bots]:::shared
  td[tdameritrade-laravel]:::shared
  billing[stripe-credits-billing]:::shared
  profile[user-profile]:::shared
  goals[goals]:::shared
  license[node-license-client]:::shared
  ta --> schwab
  ta --> rooms
  ta --> td
  ta --> billing
  ta --> profile
  ta --> goals
  ta --> license
  schwab --> td
  bots --> rooms
```

Not drawn, to keep the picture readable: **mail-kit** is required by trading-app, schwab-integration, trading-rooms, booking and referrals (5 requirements). booking and referrals require nothing else. **pulse** requires no other package and none requires it.

### Pro-only packages and what they build on

The 8 packages only OHLCX Pro installs, in blue, with the shared packages they require, in teal. 9 requirements are drawn. sectors, news and analysis require no other package.

```mermaid
flowchart LR
  classDef shared fill:#0e7490,stroke:#67e8f9,color:#ffffff,stroke-width:1px;
  classDef pro fill:#1d4ed8,stroke:#93c5fd,color:#ffffff,stroke-width:1px;
  strategies[strategies]:::pro
  dev[development-features]:::pro
  nodes[node-management]:::pro
  pricefeed[pricefeed]:::pro
  alpaca[alpaca-trade-api-php]:::pro
  schwab[schwab-integration]:::shared
  td[tdameritrade-laravel]:::shared
  mail[mail-kit]:::shared
  strategies --> pricefeed
  strategies --> alpaca
  strategies --> schwab
  strategies --> td
  strategies --> mail
  dev --> alpaca
  dev --> schwab
  dev --> td
  nodes --> mail
```

### The same as a table

| Package | Edition | Requires | Required by |
|---------|---------|----------|-------------|
| trading-app | Pro, Light | node-license-client, tdameritrade-laravel, schwab-integration, stripe-credits-billing, user-profile, trading-rooms, goals, mail-kit | none |
| schwab-integration | Pro, Light | tdameritrade-laravel, mail-kit | trading-app, strategies, development-features |
| tdameritrade-laravel | Pro, Light | none | trading-app, schwab-integration, strategies, development-features |
| stripe-credits-billing | Pro, Light | none | trading-app |
| trading-rooms | Pro, Light | mail-kit | trading-app, chat-bots |
| user-profile | Pro, Light | none | trading-app |
| goals | Pro, Light | none | trading-app |
| mail-kit | Pro, Light | none | trading-app, schwab-integration, trading-rooms, booking, referrals, strategies, node-management |
| booking | Pro, Light | mail-kit | none |
| referrals | Pro, Light | mail-kit | none |
| pulse | Pro, Light | none | none |
| node-license-client | Pro, Light | none | trading-app |
| chat-bots | Pro, Light | trading-rooms | none |
| strategies | Pro | alpaca-trade-api-php, tdameritrade-laravel, schwab-integration, pricefeed, mail-kit | none |
| pricefeed | Pro | none | strategies |
| sectors | Pro | none | none |
| news | Pro | none | none |
| analysis | Pro | none | none |
| alpaca-trade-api-php | Pro | none | strategies, development-features |
| development-features | Pro | alpaca-trade-api-php, tdameritrade-laravel, schwab-integration | none |
| node-management | Pro | mail-kit | none |

### Optional packages

Some packages name others as optional (`suggest`) and work with them when the application installs them:

| Package | Suggests |
|---------|----------|
| trading-app | booking, referrals, pulse |
| pricefeed | alpaca-trade-api-php, strategies |
| news | alpaca-trade-api-php, pricefeed |
| analysis | pricefeed, strategies |
| sectors | pricefeed |

## Request access

See [Contributor access](../getting-started/contributor-access.md).
