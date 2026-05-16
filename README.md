# OHLCX Developer Hub

**Public documentation** for the OHLCX trading platform. Application and package **source code is private**; this repository is the open developer entry point.

**Live site:** [https://docs.ohlcx.com/](https://docs.ohlcx.com/)

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

## Building docs locally (preview)

From this repository root (`docs/`):

```bash
cd docs   # this folder — the public ohlcx/docs repo root

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
mkdocs serve
```

Open **http://127.0.0.1:8000** (MkDocs Material dev server; edits reload on save).

**Production-style build** (same output as GitHub Pages):

```bash
mkdocs build
# static site in ./site/
```

Use a venv (as above) on macOS if `pip install` fails with an “externally managed environment” error.

## Regenerating docs from private source

Maintainers with the private monorepo sync allowlisted files from **`ohlcx/trading-app`** (not from `ohlcx` or `ohlcx-light` app repos):

```bash
cd /path/to/_OHLCX/packages/ohlcx/trading-app

./scripts/sync-public-docs.sh /path/to/docs
```

That script copies manifest entries, refreshes `docs/mcp/tools/index.json`, runs `generate-mcp-tools-readme.php`, and applies public sanitization. Review the diff, then commit and push **this** `docs` repo.

See [Contributor access](docs/getting-started/contributor-access.md#publishing-to-this-repo).

## Which app repo: `ohlcx` or `ohlcx-light`?

| Task | Use |
|------|-----|
| **Publish this site** | This repo only — push to public `ohlcx/docs` (or your user’s `docs` repo; see below). |
| **Sync doc content** | `packages/ohlcx/trading-app` in the private monorepo. |
| **Run the product locally** | Either app after private access; **Light** is the usual dev setup (Boost, Dusk, `.cursor/`). **Pro** if you need all domain packages locally. |
| **Cursor / MCP while coding** | Open **`ohlcx-light`** as the workspace folder when possible. |

Neither `ohlcx` nor `ohlcx-light` is the docs repo; they are private application hosts.

## GitHub org profile (`ohlcx/.github`) — optional

The folder `github-org-profile/profile/README.md` in the monorepo is only for a **GitHub Organization** named `ohlcx`.

- **You have** [github.com/ohlcx](https://github.com/ohlcx) as an org → create public repo **`ohlcx/.github`**, push `profile/README.md` there. It becomes the org’s landing README.
- **You only have a personal account** (no org, no “corporate” GitHub) → **skip** `ohlcx/.github`. Optionally add a [profile README](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme) on **`YOUR_USERNAME/.github`** instead, and link to your public `docs` repo.
- **Free org:** You can create a GitHub Organization at no cost and still use `ohlcx/.github` if you want the `ohlcx` namespace for repos and the org profile.

You do **not** need GitHub Enterprise or a paid plan for org profile READMEs or GitHub Pages on a public `docs` repo.

## Custom domain

The live site is **[https://docs.ohlcx.com](https://docs.ohlcx.com)**. `mkdocs.yml` sets `site_url` accordingly. Each deploy writes `site/CNAME` (`docs.ohlcx.com`) for GitHub Pages.

**`site/sitemap.xml`** (and all of `site/`) is **generated** on `mkdocs build` / CI — do not edit or commit it. URLs come from `site_url` (e.g. `https://docs.ohlcx.com/...`, not `ohlcx.github.io`). Rebuild locally after changing `site_url`:

```bash
source .venv/bin/activate
mkdocs build
# inspect site/sitemap.xml
```

In the repo **Settings → Pages → Custom domain**, enter `docs.ohlcx.com` and enable HTTPS. DNS: `CNAME` record `docs` → `ohlcx.github.io` (or your Pages host shown in GitHub).
