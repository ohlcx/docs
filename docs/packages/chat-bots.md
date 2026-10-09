# chat-bots

**Composer:** `ohlcx/chat-bots` · **Repository:** [github.com/ohlcx/chat-bots](https://github.com/ohlcx/chat-bots) (private) · **Edition:** Pro, Light · **Version:** 1.0.7

## Role

Simulated chat users for load-testing and demonstrating the realtime messaging of **trading-rooms**. It creates bot users, connects them over the same realtime channels a browser uses, and has them appear online and send messages.

It is a testing and demonstration tool. It has no user-facing feature.

## Commands

| Command | Purpose |
|---------|---------|
| `chat-bots:generate` | Creates bot users, each flagged as a bot, with an access token |
| `chat-bots:simulate` | Connects the bots and sends scripted direct messages |
| `chat-bots:simulate-random` | Sends randomized direct and room messages, with staggered disconnects |
| `chat-bots:simulate-presence` | Connects the bots to the presence channels only, without messages |
| `chat-bots:simulate-live-room` | Joins a room's active live session with bot viewers |
| `chat-bots:clean` | Removes every bot user with their messages and tokens. Run it before removing the package |

The simulations end by themselves when their script is done, unless `--keep-alive` is given.

## Host setup

```bash
php artisan migrate
php artisan chat-bots:generate
```

The simulations run with Node.js and use the realtime client libraries the host application already has for the chat UI. Connection settings come from the application's own realtime configuration; bot tuning uses `CHAT_BOTS_*` settings.

## Dependencies

Requires **trading-rooms**.

## Related

- [trading-rooms](trading-rooms.md)
