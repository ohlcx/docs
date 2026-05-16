# Contributor access

## Public vs private

| Asset | Visibility |
|-------|------------|
| This documentation (`ohlcx/docs`) | **Public** |
| Applications (`ohlcx`, `ohlcx-light`) | **Private** GitHub |
| Composer packages (`ohlcx/trading-app`, …) | **Private** GitHub |

## Requesting source access

1. Contact OHLCX maintainers (your usual channel: team email, support, or internal onboarding).
2. Receive GitHub organization or repository access for the repos you need.
3. Create a **GitHub personal access token** with `repo` scope (for private Composer VCS).

## Composer GitHub token

After access is granted:

```bash
export GITHUB_TOKEN=ghp_your_token_here
composer config --global github-oauth.github.com "$GITHUB_TOKEN"
```

Then clone the application repository you were assigned (Pro or Light) and run `composer install`.

!!! warning
    Never commit tokens, `.env` files, or broker secrets to any repository—including forks of this docs repo.

## Hosted OHLCX API (Light)

Light edition may call the **hosted OHLCX API** for sectors and domain data. Your maintainer will provide `OHLCX_API_TOKEN` for authorized environments only. This token is **not** available through the public docs site.

## Publishing to this repo

Maintainers sync documentation from the private `ohlcx/trading-app` package:

```bash
cd packages/ohlcx/trading-app
./scripts/sync-public-docs.sh /path/to/ohlcx/docs
```

The script uses `docs/publish-manifest.json` (allowlist) and regenerates the MCP tool index. Open a PR on `ohlcx/docs` after review.

**Policy:** When changing API routes, MCP tools, or AI behavior in private code, update private docs first, then run the sync script before merging public docs.

## Organization profile

The GitHub organization README template lives in the private workspace at `github-org-profile/profile/README.md`. Publish it to the [ohlcx/.github](https://github.com/ohlcx/.github) repository to update [github.com/ohlcx](https://github.com/ohlcx).
