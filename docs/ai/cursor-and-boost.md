# Cursor and Laravel Boost

OHLCX Light includes patterns for **AI-assisted development** with Cursor and **Laravel Boost**. Pro hosts can use the same MCP configuration; rule/skill trees are most complete in the Light repository.

## Laravel Boost

Install in a host app with private access:

```bash
composer require laravel/boost --dev
php artisan boost:install
```

Documentation: [Laravel Boost](https://laravel.com/docs/12.x/boost)

Enable the `laravel-boost` MCP server in Cursor (see [MCP Cursor setup](../mcp/cursor-setup.md)).

## OHLCX MCP

The **ohlcx** MCP server exposes domain tools (strategies, markets, KB, etc.). It complements Boost’s framework-focused tools.

```bash
php artisan mcp:start ohlcx
```

## Workspace layout

| Path (Light repo) | Purpose |
|-------------------|---------|
| `.cursor/mcp.json` | MCP server definitions |
| `.cursor/rules/` | Architecture, React, API, package conventions |
| `.cursor/skills/` | Task-specific skills (e.g. MCP engineer, React) |
| `AGENTS.md` | Agent context: versions, MCP list, doc pointers |
| `boost.json` | Boost skill configuration |

!!! note
    Raw `.cursor/` rules and `AGENTS.md` are **not** copied to this public repo. Patterns are summarized here; authorized contributors use the private repository.

## Recommended agent workflow

1. Read [Architecture overview](../architecture/overview.md) and [Data sources](../architecture/data-sources.md).
2. Use Boost for Laravel/Facade/documentation questions.
3. Use OHLCX MCP for product data (strategies, KB, markets) against a running local app.
4. Run tests: [Testing AI and MCP](testing.md).

## Product documentation for agents

After `php artisan trading-app:install`, package docs are available under `vendor/ohlcx/trading-app/docs/` in the host app. Public copies are synced to this Developer Hub.

## OHLCX DEV AGENTS (private repo layout)

```
packages/ohlcx/          # Backend packages (local path or vendor)
.cursor/                 # Rules, skills, MCP
.agents/                 # Legacy Boost skills
AGENTS.md
boost.json
```

## Further reading

- [MCP overview](../mcp/overview.md)
- [In-app assistant](in-app-assistant.md) (end-user UI, not MCP)
