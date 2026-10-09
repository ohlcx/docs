# Contributing to ohlcx/docs

This repository is **public documentation only**.

## Maintainers (private monorepo)

1. Edit source docs in `ohlcx/trading-app` (see `docs/publish-manifest.json`).
2. Run from package root:

```bash
./scripts/sync-public-docs.sh /path/to/ohlcx/docs
```

3. Rebuild the MCP tool reference (add a summary to `scripts/mcp_tool_areas.json` for any new tool first):

```bash
python3 scripts/build_mcp_reference.py /path/to/trading-app/src/Mcp
```

4. Review diff, fix any hand-edited pages if needed (`architecture/contributing.md` is not auto-overwritten; the pages under `docs/mcp/` other than `tools/README.md`, `tools/index.json` and `tools/reference.md` are written by hand).
5. Open PR on `ohlcx/docs`.

## External contributors

- Fix typos and clarify public docs via PR.
- Do not include secrets, tokens, or private URLs with credentials.
- For source code changes, request access to private `ohlcx/*` repositories separately.

## Local preview

```bash
cd docs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open http://127.0.0.1:8000

## Org profile (optional)

Only if you have a GitHub **Organization** `ohlcx`: push `github-org-profile/profile/README.md` to [ohlcx/.github](https://github.com/ohlcx/.github). Personal accounts can skip this.
