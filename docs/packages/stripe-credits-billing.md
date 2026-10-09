# stripe-credits-billing

**Composer:** `ohlcx/stripe-credits-billing` · **Repository:** [github.com/ohlcx/stripe-credits-billing](https://github.com/ohlcx/stripe-credits-billing) (private) · **Edition:** Pro, Light

## Role

Credits bought through Stripe Checkout: credit packages, purchases, the features that consume credits and the record of their use, a Stripe webhook that completes a purchase, and admin billing (overview, a user's billing, package and adjustments).

## Host setup

```bash
php artisan stripe-credits-billing:seed
```

Configure Stripe keys in host `.env` (not documented here).

## Related

MCP tools: `get-credits`, `get-transaction-history`, and for admins `get-user-billing`, `adjust-user-billing` and `set-user-billing-package`. See the [tool reference](../mcp/tools/reference.md#credits-and-billing).
