# Contributing to ohlcx/docs

This repository is **public documentation only**.

## Maintainers (private monorepo)

1. Edit source docs in `ohlcx/trading-app` (see `docs/publish-manifest.json`).
2. Run from package root:

```bash
./scripts/sync-public-docs.sh /path/to/ohlcx/docs
```

3. Review diff, fix any hand-edited pages if needed (`architecture/contributing.md` is not auto-overwritten).
4. Open PR on `ohlcx/docs`.

## External contributors

- Fix typos and clarify public docs via PR.
- Do not include secrets, tokens, or private URLs with credentials.
- For source code changes, request access to private `ohlcx/*` repositories separately.

## Local preview

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Org profile

Push `github-org-profile/profile/README.md` from the workspace monorepo to [ohlcx/.github](https://github.com/ohlcx/.github) for the GitHub organization landing page.
