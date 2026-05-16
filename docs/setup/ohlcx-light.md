# OHLCX Light setup

For developers with **private access** to [ohlcx/ohlcx-light](https://github.com/ohlcx/ohlcx-light).

## Quick start

### 1. Clone (after access is granted)

```bash
git clone https://github.com/ohlcx/ohlcx-light.git
cd ohlcx-light
```

### 2. Dependencies

```bash
composer install
npm install
```

### 3. Environment

```bash
cp .env.example .env
php artisan key:generate
```

Set `VITE_APP_VERSION=light`. For remote sectors/domain data, your maintainer will provide **`OHLCX_API_TOKEN`** (hosted API—not issued via public docs).

### 4. Database

```bash
php artisan migrate:fresh
php artisan db:seed
php artisan stripe-credits-billing:seed
php artisan trading-app:install
php artisan trading-app:seed
php artisan trading-rooms:seed
```

### 5. Build and run

```bash
npm run dev
php artisan serve
```

## Sectors (remote API)

Light does **not** require the `ohlcx/sectors` Composer package by default. Sector routes proxy to the hosted OHLCX API via `OHLCXApiService`.

## Frontend `.env` (excerpt)

```env
VITE_APP_URL=http://127.0.0.1:8000
VITE_APP_ENV=local
VITE_APP_VERSION=light
```

## Laravel Boost (recommended)

```bash
composer require laravel/boost --dev
php artisan boost:install
```

Enable `laravel-boost` in Cursor MCP settings. See [Cursor and Boost](../ai/cursor-and-boost.md).

## Browser tests (Dusk)

```bash
composer require laravel/dusk --dev
php artisan dusk:install
php artisan dusk:chrome-driver --detect
php artisan dusk --group=smoke
```

## Workspace for Cursor

Open the **`ohlcx-light`** folder as the Cursor workspace so `.cursor/mcp.json` resolves `${workspaceFolder}/artisan` correctly. For monorepo roots, see [Cursor setup](../mcp/cursor-setup.md).

## Further reading

- [Light vs Pro](../architecture/light-vs-pro.md)
- [AI overview](../ai/overview.md)
