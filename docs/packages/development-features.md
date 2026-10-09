# development-features

**Composer:** `ohlcx/development-features` · **Repository:** [github.com/ohlcx/development-features](https://github.com/ohlcx/development-features) (private) · **Edition:** Pro · **Version:** 1.0.2

## Role

Development features for broadcasting and data streaming: console commands that listen to a market data stream and broadcast what arrives, the broadcast channels for it, and a set of Livewire and Blade components built on them.

Its last release is from 2025.

## What it provides

- **Stream listeners.** Commands that connect to Alpaca's market data stream for equities and for crypto and broadcast bar, quote and trade updates.
- **Broadcast channels**: `orders.{orderId}` (the order's owner only), `active-record`, `quotes-updates`, `trades-updates`.
- **An orders table** of its own, with a command that updates an order's status.
- **Components**: Livewire components (an order form, a chat with an OpenAI client, a status history, a trading view) and Blade components (quotes, trades, online users, order status, a profile card).
- **A few web pages** for a signed-in, verified user, such as `/chat`.

## Commands

| Command | Purpose |
|---------|---------|
| `app:listen-to-web-socket` | Listens to the equities stream and broadcasts updates |
| `app:listen-to-web-socket-crypto` | Listens to the crypto stream and broadcasts updates |
| `redis:subscribe-exchange` | Subscribes to the exchanges channel |
| `app:update-order-status` | Updates an order's status |

## Configuration

`OPENAI_API_KEY`, by name, for the chat component.

## Dependencies

Requires **alpaca-trade-api-php**, **tdameritrade-laravel** and **schwab-integration**.
