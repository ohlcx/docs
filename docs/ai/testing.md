# How To Run AI Agent and MCP Tests

## Introduction

AI/MCP live in the **`ohlcx/trading-app`** package (`OHLCX\TradingApp\Ai\Tools`, `OHLCX\TradingApp\Mcp\Tools`, exposed via `/mcp/ohlcx`). Agent HTTP routes are loaded from the package’s `routes/api.php` (via `TradingAppServiceProvider`). Automated tests live under `vendor/ohlcx/trading-app/tests` (Orchestra Testbench; hosts autoload `OHLCX\TradingApp\Tests\` in dev).

## Prerequisites

- PHP and Composer dependencies installed (`composer install`).
- From a host app root (`ohlcx` or `ohlcx-light`).

## Steps

### 1. Run package tests from a host (`ohlcx` recommended)

**First run:** copy shared assets the agents expect (prompts, docs, etc.):

```bash
cd ohlcx   # or ohlcx-light
php artisan trading-app:install --force
```

**Then** (paths assume default Composer vendor layout):

```bash
cd ohlcx
./vendor/bin/phpunit --bootstrap vendor/autoload.php vendor/ohlcx/trading-app/tests/Feature/Ai
./vendor/bin/phpunit --bootstrap vendor/autoload.php vendor/ohlcx/trading-app/tests/Feature/Mcp
./vendor/bin/phpunit --bootstrap vendor/autoload.php vendor/ohlcx/trading-app/tests/Unit
```

**Unit-only** (`LocalInternalApiAdapter`) does not need install or prompts:

```bash
./vendor/bin/phpunit --bootstrap vendor/autoload.php vendor/ohlcx/trading-app/tests/Unit/Services/LocalInternalApiAdapterTest.php
```

More context: [AI_AND_MCP.md](overview.md).

### 2. Host smoke (routes registered)

```bash
php artisan test tests/Feature/AiMcpPackageRoutesSmokeTest.php
```

### 3. Single test class (example)

```bash
cd ohlcx
./vendor/bin/phpunit --bootstrap vendor/autoload.php \
  vendor/ohlcx/trading-app/tests/Feature/Ai/Agents/AiAgentToolsInventoryTest.php
```

## Expected results

- All selected tests pass with exit code 0.
- No real outbound HTTP to OHLCX or internal APIs during AI tool smokes (mocks only).

## Troubleshooting

- **Inventory test fails after adding a tool:** Update the expected sorted `name()` list in `AiAgentToolsInventoryTest` to match `SupportKnowledgeAgent`, `TradingAssistantAgent`, or `UnifiedAssistantAgent::tools()`.
- **"is not classified" after adding an assistant tool:** every tool of the unified assistant must be listed as reading outside text or not. Add its name to one of the two lists in the accounts-proposal tool test (and, when it reads text someone other than the user wrote, register it as a reader).
- **Catalog test fails after adding an MCP tool:** every registered tool needs a descriptor file with the same arguments and an entry in `descriptors/index.json`, in the server's order (the catalog test).
- **A test passes alone and fails in the suite because of the data source:** the suite runs with `TRADING_APP_AI_DOMAIN_DATA_SOURCE=remote`; a test that needs the local source sets it itself.
- **MCP descriptor mismatch in Cursor:** Canonical sources are `OHLCXServer.php` and `vendor/ohlcx/trading-app/src/Mcp/descriptors/`.
- **Prompt tests fail:** Run `trading-app:install` so `resources/prompts` exists in the host.

## Additional information

- Agents and MCP bridge: [../../ai/agents.md](agents.md)
- Package overview: [../../AI_AND_MCP.md](overview.md)
