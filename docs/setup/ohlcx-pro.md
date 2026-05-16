# OHLCX Pro setup

For developers with **private access** to [ohlcx/ohlcx](https://github.com/ohlcx/ohlcx).

## Quick start

### 1. Clone (after access is granted)

```bash
git clone https://github.com/ohlcx/ohlcx.git
cd ohlcx
```

### 2. PHP and Node dependencies

```bash
composer install
npm install
```

### 3. Environment

```bash
cp .env.example .env
php artisan key:generate
```

Configure database, Redis, Reverb, Schwab, and AI provider keys in `.env`.

### 4. Database and packages

```bash
php artisan migrate --seed
php artisan stripe-credits-billing:seed
php artisan trading-app:install --pro
php artisan trading-app:seed
```

Use `--force` on `trading-app:install` when updating package assets/docs into the host app.

### 5. Frontend

```bash
npm run dev
```

### 6. Serve

```bash
php artisan serve
```

## Local services

```bash
php artisan horizon
php artisan reverb:start
php artisan schedule:work   # optional
```

Horizon dashboard: `http://localhost:8000/horizon`

## Reverb (`.env` excerpt)

```env
BROADCAST_DRIVER=reverb
REVERB_APP_ID=123456
REVERB_APP_KEY=abcdef
REVERB_APP_SECRET=qwerty
REVERB_HOST=localhost
REVERB_PORT=8082
REVERB_SCHEME=http
```

## Pro-specific seeds

```bash
php artisan pricefeed:seed
php artisan strategies:seed
```

## MCP and AI

See [AI overview](../ai/overview.md) and [MCP overview](../mcp/overview.md). Pro uses **local** domain data for AI/MCP when `APP_VERSION=pro` and packages are installed.

## Further reading

- [trading-app install](trading-app-install.md)
- [Architecture: Light vs Pro](../architecture/light-vs-pro.md)
