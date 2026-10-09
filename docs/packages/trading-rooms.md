# trading-rooms

**Composer:** `ohlcx/trading-rooms` · **Repository:** [github.com/ohlcx/trading-rooms](https://github.com/ohlcx/trading-rooms) (private) · **Edition:** Pro, Light

## Role

Realtime messaging: direct messages, rooms (groups), attachments, invites, join requests, unread tracking, room discovery, and live sessions in a room. Messages are broadcast over Laravel Reverb. Optional Gemini image analysis in an AI-enabled room.

The package provides the API, the broadcasts and the database. It does not ship a full frontend: the host application provides the client.

## Host setup

```bash
php artisan trading-rooms:seed
php artisan reverb:start
```

## Requires

`mail-kit`.

## Related

MCP tools: `create-group`, `send-message`, `get-sidebar-conversations`, `discover-groups`, `get-unread-messages` and the other entries under [Trading rooms and messages](../mcp/tools/reference.md#trading-rooms-and-messages).
