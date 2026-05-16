# OHLCX Developer Hub

**Public documentation** for the OHLCX trading platform. Application and package **source code is private**; this repository is the open developer entry point.

**Live site:** [https://ohlcx.github.io/docs/](https://ohlcx.github.io/docs/) (after GitHub Pages is enabled)

## What is OHLCX?

OHLCX is a **Laravel + React** trading platform: Schwab brokerage integration, unified dashboard, strategies and signals, realtime messaging, credits billing, market data, news, and technical analysis. Optional **in-app AI assistants** and an **MCP server** (80+ tools) support developers and power users.

## Editions

| Edition | Repository | Description |
|---------|------------|-------------|
| **Pro** | [ohlcx/ohlcx](https://github.com/ohlcx/ohlcx) (private) | Full stack: local domain packages (strategies, sectors, pricefeed, news, analysis, …) |
| **Light** | [ohlcx/ohlcx-light](https://github.com/ohlcx/ohlcx-light) (private) | Slimmer app; sectors and some domain data via hosted OHLCX API |

## Developer paths

| Topic | Start here |
|-------|------------|
| **Getting started** | [Overview](docs/getting-started/overview.md) · [Requirements](docs/getting-started/requirements.md) · [Contributor access](docs/getting-started/contributor-access.md) |
| **Setup** | [OHLCX Pro](docs/setup/ohlcx-pro.md) · [OHLCX Light](docs/setup/ohlcx-light.md) · [trading-app install](docs/setup/trading-app-install.md) |
| **Architecture** | [Overview](docs/architecture/overview.md) · [Apps & packages](docs/architecture/apps-and-packages.md) · [Light vs Pro](docs/architecture/light-vs-pro.md) · [Data sources](docs/architecture/data-sources.md) |
| **API** | [Reference](docs/api/reference.md) · [OpenAPI](docs/api/openapi.yaml) |
| **AI** | [Overview](docs/ai/overview.md) · [In-app assistant](docs/ai/in-app-assistant.md) · [Agents](docs/ai/agents.md) · [Cursor & Boost](docs/ai/cursor-and-boost.md) · [Testing](docs/ai/testing.md) |
| **MCP** | [Overview](docs/mcp/overview.md) · [Cursor setup](docs/mcp/cursor-setup.md) · [Tool catalog](docs/mcp/tools/README.md) |
| **Packages** | [Ecosystem map](docs/packages/README.md) |

## AI & MCP highlight

- **In-app agents:** Support, Trading, and unified Assistant modes over SSE (`POST /api/ai/agents/*`).
- **OHLCX MCP server:** Web (`/mcp/ohlcx`) and stdio (`php artisan mcp:start ohlcx`) with strategies, markets, KB, messaging, billing, and admin tools.
- **IDE integration:** Cursor + Laravel Boost; see [Cursor & Boost](docs/ai/cursor-and-boost.md).

## Access model

- **Documentation:** public (this repo).
- **Source:** private GitHub repos under [github.com/ohlcx](https://github.com/ohlcx). Install via Composer VCS with an authorized **GitHub token**. See [Contributor access](docs/getting-started/contributor-access.md).

## Links

- **Product:** [ohlcx.online](https://www.ohlcx.online)
- **Docs repo:** [github.com/ohlcx/docs](https://github.com/ohlcx/docs)
- **Disclaimer:** [DISCLAIMER.md](DISCLAIMER.md)

## Building docs locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Open http://127.0.0.1:8000

## Syncing from private source

Maintainers: docs are synced from `ohlcx/trading-app` via `scripts/sync-public-docs.sh`. See [Contributor access](docs/getting-started/contributor-access.md#publishing-to-this-repo).
