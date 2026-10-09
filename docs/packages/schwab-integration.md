# schwab-integration

**Composer:** `ohlcx/schwab-integration` · **Repository:** [github.com/ohlcx/schwab-integration](https://github.com/ohlcx/schwab-integration) (private) · **Edition:** Pro, Light

## Role

Broker integration for Schwab (TD Ameritrade API): a user's tokens, their linked accounts, and the account data built from them.

## What it provides

- **Tokens.** Access and refresh tokens are stored encrypted. A scheduled command (`refresh:tdtokens`, every minute) refreshes tokens that are about to expire, so a linked account stays linked without the user doing anything. When a token can no longer be refreshed it is removed, and the user links Schwab again.
- **Accounts.** One row per user and Schwab account, synced after each token update, with a history snapshot on each sync. The account number is stored masked, such as `*****678`.
- **The default account.** The account the broker reports as the user's default is flagged on that account.
- **Account data API.** Balances and growth, realized profit and loss (history and by symbol), deposits and withdrawals, and order reads.
- **Profit and loss sync** is opt-in: it runs only for users who have given consent in the app.

## Events

- `TokenUpdatedEvent` when a user's tokens are updated. The account sync follows it.

## Requires

`tdameritrade-laravel`, `mail-kit`.

## Related

- [tdameritrade-laravel](tdameritrade-laravel.md): low-level API client
- [Accounts and identifiers](../mcp/accounts.md): how accounts appear to MCP clients (account id and masked label)
- [Data sources](../architecture/data-sources.md): Schwab called from the frontend and from Laravel
