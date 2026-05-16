# trading-rooms

**Composer:** `ohlcx/trading-rooms` · **Repository:** [github.com/ohlcx/trading-rooms](https://github.com/ohlcx/trading-rooms) (private)

## Role

Realtime messaging: DMs, groups, invites, join requests, Reverb broadcasts. Optional Gemini analysis route in AI-enabled groups.

## Host setup

```bash
php artisan trading-rooms:seed
php artisan reverb:start
```

MCP tools: `create-group`, `send-message`, `get-sidebar-conversations`, and related entries in the [tool catalog](../mcp/tools/README.md).
