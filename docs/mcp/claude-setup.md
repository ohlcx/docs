# MCP Claude setup

This page connects Claude to the OHLCX MCP server: Claude Code, Claude Desktop, and Claude on the web. For what the server offers once connected, see the [MCP overview](overview.md). Building your own agent instead? See [Agents setup](agents-setup.md).

!!! note "How this page was checked"
    The Claude steps follow Anthropic's documentation as published on 2026-10-09, and the Claude Code commands were checked against `claude mcp --help` of Claude Code 2.1.286. Menus and flags change: where a step says "check your version", confirm it in your own client. The OHLCX side was read from the server's code.

## What the OHLCX server needs

The server has two transports. They differ in who is signed in, and that decides which tools Claude sees.

| Transport | How Claude reaches it | Signed-in user | Tools |
|-----------|----------------------|----------------|-------|
| Stdio | Claude starts `php artisan mcp:start ohlcx` in a checkout | None | 4: `ping`, `run-support-agent`, `search-knowledge-base`, `get-knowledge-base-article` |
| HTTP | `POST` to `/mcp/ohlcx` on a running OHLCX app | The owner of the bearer token | Everything that user is offered |

So for your strategies, accounts and orders you need the HTTP transport and a token. Stdio is enough for the knowledge base and for checking that a checkout works.

### The HTTP endpoint

- The path is `/mcp/ohlcx` on your OHLCX host, for example `https://ohlcx.example.com/mcp/ohlcx`. Replace the host with your own everywhere on this page.
- It is the MCP Streamable HTTP transport. Only `POST` is served; `GET` answers 405.
- It requires a signed-in user (Laravel Sanctum). An MCP client signs in by sending an API token as a bearer header:

```text
Authorization: Bearer <your token>
```

- The server has no OAuth sign-in. A request without a valid token answers 401 with `WWW-Authenticate: Bearer realm="mcp", error="invalid_token"`. In any Claude surface, choose the option that sends a fixed header, not the one that signs in.

### Getting a token

A token belongs to one OHLCX user. There are two ways to get one.

**Sign in through the API** (OHLCX Light and Pro). Send your email and password to `/api/login`:

```bash
curl -s https://ohlcx.example.com/api/login \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "<your password>"}'
```

The answer carries the token:

```json
{ "two_factor": false, "user": { "id": 12, "name": "Sam" }, "token": "<your token>" }
```

`user` is your user record, shortened here.

If your account uses two-factor authentication the answer is `{ "two_factor": true, "user_id": 12 }` instead. Send that id with a current code to `/api/two-factor-challenge` (`{"user_id": 12, "code": "<code>"}`) to receive the token.

**The API Tokens page** (OHLCX Pro). OHLCX Pro has the account's API Tokens page at `/user/api-tokens`, where you can create and delete tokens. OHLCX Light does not have this page. Check your version: if your installation does not show the page, use the sign-in call above.

!!! warning "A token can do everything its user can"
    The MCP server does not check token permissions. Any valid token of a user reaches every tool that user is offered, including the tools that switch a strategy's orders on. The permissions you can tick on the API Tokens page do not narrow this. By default tokens do not expire.

    - Keep the token out of your repository and out of shared configuration.
    - Use one token per client, so that you can revoke one without the others.
    - To revoke the token a client is using, send `POST /api/auth/logout-device` with that token as the bearer header, or delete it on the API Tokens page.
    - To limit what Claude may do, limit it in the client. See [What Claude must confirm](#what-claude-must-confirm).

## Claude Code

Put the token in an environment variable first, so that it stays out of your shell history and your files:

```bash
export OHLCX_MCP_TOKEN="<your token>"
```

### Add the server over HTTP

```bash
claude mcp add --transport http ohlcx https://ohlcx.example.com/mcp/ohlcx \
  --header "Authorization: Bearer $OHLCX_MCP_TOKEN"
```

Your shell expands `$OHLCX_MCP_TOKEN` before Claude Code sees it, so the token itself is stored in Claude Code's configuration (`~/.claude.json`). To keep it out of that file, use a project file with `${OHLCX_MCP_TOKEN}` instead, as shown under [A project file](#a-project-file-mcpjson).

### Add the server over stdio

In a checkout, for the four tools that need no sign-in:

```bash
claude mcp add --transport stdio ohlcx-local -- php /absolute/path/to/ohlcx-light/artisan mcp:start ohlcx
```

Everything after `--` is the command that starts the server.

### Scopes: for this project, for you, or for the team

`--scope` (or `-s`) decides where the server is stored and where it loads.

| Scope | Loads in | Stored in |
|-------|----------|-----------|
| `local` (default) | The current project only, private to you | `~/.claude.json` |
| `project` | The current project, shared through version control | `.mcp.json` in the project root |
| `user` | All your projects, private to you | `~/.claude.json` |

For example, to have the server in every project of yours:

```bash
claude mcp add --scope user --transport http ohlcx https://ohlcx.example.com/mcp/ohlcx \
  --header "Authorization: Bearer $OHLCX_MCP_TOKEN"
```

### A project file: `.mcp.json`

A `.mcp.json` in the project root is shared with everyone who clones the repository, so it must not hold a token. Claude Code expands `${VAR}` in `url`, `headers`, `command`, `args` and `env`, so each person supplies their own token from their environment:

```json
{
  "mcpServers": {
    "ohlcx": {
      "type": "http",
      "url": "https://ohlcx.example.com/mcp/ohlcx",
      "headers": {
        "Authorization": "Bearer ${OHLCX_MCP_TOKEN}"
      }
    }
  }
}
```

The stdio form uses `command`, `args` and `env`:

```json
{
  "mcpServers": {
    "ohlcx-local": {
      "command": "php",
      "args": ["${OHLCX_APP_DIR}/artisan", "mcp:start", "ohlcx"]
    }
  }
}
```

Set `OHLCX_APP_DIR` to the absolute path of your checkout.

Claude Code asks for your approval before it uses a server from a project's `.mcp.json`. Until you approve, `claude mcp list` shows the server as pending approval. If `OHLCX_MCP_TOKEN` is not set, Claude Code warns about the missing variable and the server answers 401.

### Check the connection

```bash
claude mcp list
claude mcp get ohlcx
```

`claude mcp list` lists the configured servers with a health check. Inside a Claude Code session, `/mcp` shows each server's status.

To see the tools, ask Claude in a session: "Which tools does the ohlcx server give you?" Tool names appear as `mcp__ohlcx__<tool>`, for example `mcp__ohlcx__list-strategies`.

To remove the server:

```bash
claude mcp remove ohlcx
```

## Claude Desktop

Claude Desktop reaches MCP servers in two ways, and they are separate mechanisms.

### A local server through the config file (stdio)

This starts the server on your computer. It gives the four tools that need no sign-in.

1. Open the Claude menu in your system's menu bar and choose **Settings...**.
2. Open the **Developer** tab and click **Edit Config**. This opens `claude_desktop_config.json`:
    - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
3. Add the server. Use absolute paths:

    ```json
    {
      "mcpServers": {
        "ohlcx-local": {
          "command": "php",
          "args": ["/absolute/path/to/ohlcx-light/artisan", "mcp:start", "ohlcx"]
        }
      }
    }
    ```

4. Quit Claude Desktop completely and start it again.

If the server does not appear, read the logs: `~/Library/Logs/Claude` on macOS, `%APPDATA%\Claude\logs` on Windows. `mcp.log` holds connection failures, and `mcp-server-ohlcx-local.log` holds what the server wrote. If `php` is not found, give its absolute path as `command`.

### The full server through a custom connector (HTTP)

A custom connector reaches the HTTP endpoint with your token, so it gives every tool your user is offered. Two conditions apply:

- **Your OHLCX host must be reachable from the public internet.** Claude connects from Anthropic's cloud, not from your computer, also in Claude Desktop. A host on `localhost`, on a private network or behind a VPN will not connect.
- **The connector must send your token as a request header.** The server has no OAuth sign-in.

The steps are the same as for Claude on the web, below.

## Claude on the web

Custom connectors are set up in Claude's settings and then work in claude.ai, Claude Desktop and the mobile apps. Anthropic's steps for a Pro or Max plan are:

1. Go to **Customize > Connectors**.
2. Click **+ Add**, then **Add custom connector**.
3. Enter a name, for example `OHLCX`.
4. Enter the server URL: `https://ohlcx.example.com/mcp/ohlcx`. Click **Continue**.
5. Review the authentication settings Claude detected. Under **Authentication**, choose **No sign in**: the OHLCX server has no OAuth sign-in.
6. Under **Request headers**, add the header `Authorization` with the value `Bearer <your token>`.
7. Click **Add**.

On Team and Enterprise plans an Owner adds the connector under **Organization settings > Connectors** (**Add**, then **Custom**, then **Web**).

!!! warning "Do not share one token across an organization"
    On Team and Enterprise plans, a connector with a fixed request header gives everyone who uses it that credential's access. An OHLCX token is one user, so every member would act as that user, on that user's brokerage accounts. Use a custom connector with a fixed header for a single person only.

Check your version: these steps are Anthropic's as published and were not run against an OHLCX host for this page. If your plan or client does not show **Request headers**, the connector cannot authenticate to OHLCX; use Claude Code instead.

## First prompt

Start with a read that changes nothing:

```text
List my strategies.
```

Claude should call `list-strategies` and show your strategies. Then try:

```text
List my linked accounts and their balances.
```

Claude should call `list-accounts` and name each account by its masked label, such as `*****678`. If Claude answers without calling a tool, or says it has no such tool, see [Troubleshooting](#troubleshooting).

## What Claude must confirm

When Claude connects, the server sends it instructions. They tell Claude to confirm with you before it:

- switches a strategy on, or switches its orders on;
- changes a strategy's settings;
- deletes anything;
- chooses a strategy's order accounts with `set-strategy-accounts`. This decides which brokerage accounts receive the strategy's orders. It never switches orders on.

The instructions also state that no tool places, changes or cancels a broker order directly, and that a strategy that is switched on with orders on does. The full text is on the [overview](overview.md#the-servers-instructions).

Instructions are a request to the model, not a lock. Keep your client asking before each call of a tool that writes, and do not choose "always allow" for these tools: `set-strategy-accounts`, `set-strategy-flag`, `set-strategy-status`, `deploy-strategy`, `retain-strategy`, `update-strategy-settings`, and any tool that deletes. The [tool reference](tools/reference.md) marks every tool as a read or a write.

## Prompts and the resource

The server offers three prompts and one resource. See [Prompts](overview.md#prompts).

| Kind | Name | Use |
|------|------|-----|
| Prompt | `user-info` | A summary of the signed-in user. Listed only with a signed-in user |
| Prompt | `trading-terminology` | OHLCX product terms: TSP, OCO, TRIM, order types |
| Prompt | `support-knowledge-base` | Knowledge base content for a support question |
| Resource | `ohlcx://strategy-settings` | Every strategy setting with its allowed values. Read before creating a strategy or changing its settings |

In Claude Code, type `/` to find a prompt. Typing `/mcp__ohlcx__trading-terminology` runs it. Type `@` to find the resource; its reference has the form `@ohlcx:ohlcx://strategy-settings`. In Claude Desktop and on the web, the prompts and resources of a connector are behind the "Add files, connectors, and more" button of the message box, under **Connectors**. Check your version.

## Which tools you will see

| Signed in as | Tools |
|--------------|-------|
| Nobody (stdio) | 4 |
| A user on OHLCX Light | The tools for a signed-in user. `list-strategy-accounts` and `set-strategy-accounts` are not listed |
| A user on OHLCX Pro | The same, plus `list-strategy-accounts` and `set-strategy-accounts` |
| An admin | The same as a user of that edition, plus 13 admin tools |

The five server backtest tools and the four support ticket tools are listed only where the app has those features switched on. The [tool reference](tools/reference.md) says who is offered each tool.

## Troubleshooting

| Issue | Check |
|-------|-------|
| 401, or the server shows as failed or needing authentication | The token. Is `OHLCX_MCP_TOKEN` set in the shell that started Claude? Was the token revoked? Is the header exactly `Authorization: Bearer <token>`? Do not try to sign in through the client: the server has no OAuth sign-in |
| Only four tools | You are on stdio, where nobody is signed in. Use the HTTP endpoint with a token |
| The tool list is empty | Run `claude mcp get ohlcx`. A server from `.mcp.json` must be approved first. For stdio, run the command yourself in a terminal to see why it does not start |
| `list-strategy-accounts` and `set-strategy-accounts` are missing | They exist only on OHLCX Pro. On another installation, order accounts are set in the OHLCX app |
| Admin tools are missing | The token's user is not an admin |
| A custom connector does not connect | The host must be reachable from the public internet, and the connector must use **No sign in** with a request header |
| `No linked account of yours has that id.` | See [Accounts and identifiers](accounts.md#passing-an-account-account_id) |
| Any other refusal | See [Errors and refusals](errors.md) |
