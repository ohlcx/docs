# AI and MCP

The `ohlcx/trading-app` package is the single source of truth for AI and MCP in both OHLCX Light and OHLCX Pro. It holds two separate things:

- The **in-app assistant**: three AI agents behind `POST /api/ai/agents/*`, used by the assistant drawer and by the Ask OHLCX panels. 57 tools.
- The **MCP server** `OHLCX`: 147 tools, 1 resource and 3 prompts for outside clients (an IDE, a desktop client), at `/mcp/ohlcx` and over stdio.

The two do not share tools. An assistant tool is named in `snake_case` (`list_trading_strategies`); an MCP tool in `kebab-case` (`list-strategies`). The same subject can appear on both sides with a different shape.

## Pages

| Page | What it answers |
| ---- | --------------- |
| [Agents and their tools](agents.md) | Which agent has which tools, under which conditions. Every assistant tool name. |
| [In-app assistant](in-app-assistant.md) | The endpoints, the page context, Ask OHLCX, and how a proposal becomes a card and a click. |
| [What changed in 1.0.350 and 1.0.351](changes-1.0.351.md) | Every MCP tool whose input or output changed, the new tools, and the relay changes. For whoever maintains a client. |
| [Running the tests](testing.md) | How to run the AI and MCP tests. |
| [MCP tool catalogue](../mcp/tools/README.md) | Every MCP tool with its arguments. The machine-readable catalogue is `index.json` beside it. |

Maintainers: the notes on how this is built (the MCP server's internals, order routing and accounts, failures and refusals, the security model, adding a tool) are in the package repository under `docs/ai/`, starting at `docs/ai/README.md`. They are not part of the public documentation.

## What the assistant and an MCP client can and cannot do

- No tool, on either side, places, changes or cancels a broker order. Orders are placed only by a deployed strategy that has orders switched on.
- No tool shows a full brokerage account number or a broker's internal key for an account. An account is an id and a masked label such as `*****678`.
- The in-app assistant cannot create, change, deploy or delete a strategy, and cannot choose a strategy's order accounts. It can offer a card; the user presses its button.
- An MCP client can write: create and change strategies and conditions, retain and deploy, set order accounts, manage watchlists, send messages. The server tells the client's model to confirm with the user first. An MCP session acts as its signed-in user, and an access token gives everything that user can do through the server; there are no narrower token scopes.
- The in-app assistant only reads the Screener, the user's watchlists and the realized results of the user's own linked accounts. There are no saved screeners to read, a watchlist holds symbols and no prices, and it has no tool for single closed trades, cash transfers or a profit and loss sync. It cannot create or change a watchlist or save a screener.
- While the user has "Hide Account Balance" switched on, the assistant's account tools leave out every amount of money and give percentages and counts. If the preference cannot be read, it counts as on. The MCP server's own account tools do not follow this preference.
- Admin tools are listed only for an admin.

## Host app wiring

Host apps must keep a local `routes/ai.php` because Laravel MCP only loads the host's own `routes/ai.php`. Use a thin stub:

```php
<?php

require __DIR__.'/../vendor/ohlcx/trading-app/routes/ai.php';
```

The agent HTTP routes are loaded with the package's API routes. Hosts do **not** need to include them in their own `routes/api.php`. Remove any legacy block there that included the package's agent routes; `trading-app:install` strips common patterns.

## Configuration switches

All in the host's `config/trading-app.php`.

| Key | Env | Default | What it decides |
| --- | --- | ------- | --------------- |
| `app_version` | `APP_VERSION` | `light` | `pro` adds the market tools to the assistants and is needed for strategy order routing. |
| `ai.domain_data_source` | `TRADING_APP_AI_DOMAIN_DATA_SOURCE` | `auto` | Where strategy and market data is read from: `local`, `remote`, or `auto`. See below. |
| `run_assistant` | `TRADING_APP_RUN_ASSISTANT` | `false` | Ask OHLCX. Off: the page context is ignored and the saved-run and proposing tools do not exist. It has an effect only on Pro, for a signed-in user. |
| `backtest_server_runs` | `TRADING_APP_BACKTEST_SERVER_RUNS` | `false` | Server-side backtests. Off: the five MCP backtest job tools are not listed. |
| `ohlcx_api_token` | `OHLCX_API_TOKEN` | none | The token of the remote data source. |

The four MCP support ticket tools are listed only when the support desk connection is configured.

## Data source mode

- `ai.domain_data_source = auto|remote|local`
- `auto` resolves by `APP_VERSION` (`pro` → local, otherwise remote).

`remote` uses an authorized `OHLCX_API_TOKEN` against the hosted OHLCX API.

`local` uses this app's own `/api/*` with the current user's sign-in.

The difference is more than the address:

| | `local` (Pro) | `remote` (Light) |
| - | ------------- | ---------------- |
| A request for strategy or market data runs as | the signed-in user | one API account, whoever is signed in |
| Strategy order routing (which accounts receive a strategy's orders) | available | not available: it is managed in OHLCX Pro |

## Light vs Pro behavior

- `APP_VERSION=light`: the remote proxy routes are active.
- `APP_VERSION=pro`: the remote proxy routes are off; the app uses its own domain routes.
- If the local domain packages are not installed in Light, force `ai.domain_data_source=remote`.

## Install/update

```bash
php artisan trading-app:install --force
```

This copies prompts, docs and assets as configured, ensures the `routes/ai.php` stub, removes legacy agent-route includes from the host's `routes/api.php`, installs `config/trading-app.php` when missing, and patches `bootstrap/app.php` to add the CSRF exemption `api/ai/agents/*` (required for server-sent events from the SPA). Re-run after pulling if you reset `bootstrap/app.php` to stock Laravel.

Optional pro overlays:

```bash
php artisan trading-app:install --force --pro
```
