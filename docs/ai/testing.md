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

More context: [AI overview](overview.md).

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
- **MCP descriptor mismatch in Cursor:** Canonical sources are `OHLCXServer.php` and `vendor/ohlcx/trading-app/src/Mcp/descriptors/`.
- **Prompt tests fail:** Run `trading-app:install` so `resources/prompts` exists in the host.

## Additional information

- Agents and MCP bridge: [agents.md](agents.md)
- Package overview: [overview.md](overview.md)
