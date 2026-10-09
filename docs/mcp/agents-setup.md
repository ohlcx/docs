# MCP Agents setup

This page is for an agent you build or run yourself: a program that calls the OHLCX MCP server without a person in an editor approving each step. For an editor or a chat client, see [Cursor setup](cursor-setup.md) and [Claude setup](claude-setup.md).

!!! note "How this page was checked"
    The Claude Agent SDK and Messages API sections follow Anthropic's documentation as published on 2026-10-09. The OHLCX side was read from the server's code. The examples were not run against an OHLCX host for this page: where a step says "check your version", confirm it in your own setup before you rely on it.

!!! note "Not the assistant inside OHLCX"
    OHLCX has its own in-app assistant, described under [Agents](../ai/agents.md) and [In-app assistant](../ai/in-app-assistant.md). It runs inside the app with its own tools and does not use MCP. This page is about the opposite direction: an external agent that reaches OHLCX through the MCP server, with the tools in the [tool reference](tools/reference.md).

## Choose a transport

| | Stdio | HTTP |
|---|-------|------|
| How | The agent starts `php artisan mcp:start ohlcx` in a checkout | The agent sends `POST` requests to `/mcp/ohlcx` on a running OHLCX app |
| Signed-in user | None | The owner of the bearer token |
| Tools | 4: `ping`, `run-support-agent`, `search-knowledge-base`, `get-knowledge-base-article` | Everything that user is offered |
| Use it for | A knowledge base agent, or a smoke test of a checkout | Anything that reads or changes a user's strategies, accounts or orders |

An agent that works with a user's data needs HTTP.

## Authenticate a headless agent

The HTTP endpoint requires a signed-in user. An agent signs in by sending an OHLCX API token on every request:

```text
Authorization: Bearer <token>
```

How to get a token is on [Claude setup](claude-setup.md#getting-a-token). The server has no OAuth sign-in: a request without a valid token answers 401 with `WWW-Authenticate: Bearer realm="mcp", error="invalid_token"`.

### What a token is

- **One token is one user.** The agent acts as that user and sees that user's strategies and linked brokerage accounts.
- **Tokens carry no scopes that the MCP server reads.** Any valid token reaches every tool its user is offered, reads and writes alike. There is no read-only token.
- **By default tokens do not expire.** A token works until it is revoked.

What follows from that:

1. **Read-only has to be enforced in your agent**, by the tools you allow. See [Restrict an agent to read-only tools](#restrict-an-agent-to-read-only-tools). The server will not do it for you.
2. **Treat the token like the user's password.** Read it from an environment variable or a secret store at run time. Never write it into the repository, a prompt, a log or a shared configuration file.
3. **Give each agent its own token**, so that you can revoke one agent without stopping the others. Revoke with `POST /api/auth/logout-device`, sent with that token as the bearer header.
4. **Do not run an agent with an admin's token** unless it needs the admin tools. An admin's token also reaches user administration and billing.
5. **One agent, one user.** Do not put one user's token behind a service that several people use: each of them would act on that user's brokerage accounts.

```bash
export OHLCX_MCP_TOKEN="<token>"
```

## The server's rules for agents

These are the server's own rules. An unattended agent has to keep them without a person watching.

- **No tool places, changes or cancels a broker order directly.** A strategy does: one that is deployed, switched on, real (not demo), with orders on and at least one order account that can receive orders. See [What leads to broker orders](overview.md#what-leads-to-broker-orders).
- **Confirm with the user before** switching a strategy or its orders on, changing its settings, or deleting anything.
- **Confirm before setting order accounts.** `set-strategy-accounts` decides which brokerage accounts receive a strategy's orders. It never switches orders on.
- **Retain before changing a deployed strategy.** A deployed strategy refuses changes with "Retain the strategy before changing it." Call `retain-strategy`, make the change, then `deploy-strategy`. Switching things off always works. See [the deployed lock](strategy-routing.md#the-deployed-lock).
- **Read `ohlcx://strategy-settings` before creating a strategy or changing its settings.**
- **A refusal is an answer, not an obstacle.** Do not reach the same result through another tool. See [Errors and refusals](errors.md).

### Reads and writes

The server sends a hint with each tool, in the tool's `annotations`: `readOnlyHint` for a tool that changes nothing, `destructiveHint` for a write, `idempotentHint` where repeating a call changes nothing more. Some writes carry no hint: treat a tool without `readOnlyHint: true` as a write. The [tool reference](tools/reference.md#how-to-read-this-page) lists every tool's kind.

| Agent | Allow |
|-------|-------|
| Unattended | Tools of kind Read only |
| With a person who confirms | Reads freely. Each write only after that person has seen the tool and its arguments and said yes |

The hints are the server's description of its tools. They are a sound basis for an allow-list. They are not an enforcement: enforce in your agent.

## Claude Agent SDK

The Agent SDK runs Claude's agent loop in your own process and connects to MCP servers you configure.

Install it (Node.js 18 or later, or Python 3.10 or later) and set your Anthropic API key:

```bash
npm install @anthropic-ai/claude-agent-sdk
```

```bash
pip install claude-agent-sdk
```

```bash
export ANTHROPIC_API_KEY="<your Anthropic API key>"
```

### Connect over HTTP

Pass the server in `mcpServers` (TypeScript) or `mcp_servers` (Python), with `"type": "http"` and the token in `headers`. MCP tools are named `mcp__<server>__<tool>`, so with the server named `ohlcx` the tool `list-strategies` is `mcp__ohlcx__list-strategies`.

### Restrict an agent to read-only tools

The SDK allows and denies tools by name. It has no switch for "tools with a read-only hint", so build the allow-list from the [tool reference](tools/reference.md): every tool whose kind is Read.

Two options do the work together:

- `allowedTools` lists the tools that run without asking.
- `permissionMode: "dontAsk"` denies every call that would otherwise ask. Without it, a tool that is not on the list is still available and falls through to the permission mode.

Never use `bypassPermissions` for this: `allowedTools` does not constrain that mode, and every tool would be approved.

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

const readOnly = [
  "mcp__ohlcx__list-strategies",
  "mcp__ohlcx__get-strategy",
  "mcp__ohlcx__get-strategy-statistics",
  "mcp__ohlcx__list-trades",
  "mcp__ohlcx__list-accounts",
  "mcp__ohlcx__get-accounts-balances",
  "mcp__ohlcx__list-orders",
  "mcp__ohlcx__get-ticker-bars"
];

for await (const message of query({
  prompt: "Summarise how my strategies did this month.",
  options: {
    mcpServers: {
      ohlcx: {
        type: "http",
        url: "https://ohlcx.example.com/mcp/ohlcx",
        headers: {
          Authorization: `Bearer ${process.env.OHLCX_MCP_TOKEN}`
        }
      }
    },
    allowedTools: readOnly,
    permissionMode: "dontAsk"
  }
})) {
  if (message.type === "system" && message.subtype === "init") {
    const unavailable = message.mcp_servers.filter(
      (s) => s.status === "failed" || s.status === "needs-auth"
    );
    if (unavailable.length > 0) {
      throw new Error("OHLCX MCP server is not available");
    }
  }
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

The same in Python:

```python
import asyncio
import os

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, SystemMessage, query

READ_ONLY = [
    "mcp__ohlcx__list-strategies",
    "mcp__ohlcx__get-strategy",
    "mcp__ohlcx__get-strategy-statistics",
    "mcp__ohlcx__list-trades",
    "mcp__ohlcx__list-accounts",
    "mcp__ohlcx__get-accounts-balances",
    "mcp__ohlcx__list-orders",
    "mcp__ohlcx__get-ticker-bars",
]


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "ohlcx": {
                "type": "http",
                "url": "https://ohlcx.example.com/mcp/ohlcx",
                "headers": {"Authorization": f"Bearer {os.environ['OHLCX_MCP_TOKEN']}"},
            }
        },
        allowed_tools=READ_ONLY,
        permission_mode="dontAsk",
    )

    async for message in query(
        prompt="Summarise how my strategies did this month.", options=options
    ):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            unavailable = [
                s
                for s in message.data.get("mcp_servers", [])
                if s.get("status") in ("failed", "needs-auth")
            ]
            if unavailable:
                raise RuntimeError("OHLCX MCP server is not available")
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

What this agent does, step by step:

1. It connects with the user's token. The first message, the `init` message, reports each server's status. `failed` or `needs-auth` means the token or the host is wrong: stop, do not continue on built-in tools. A status of `pending` is not a failure.
2. Claude reads the server's instructions and calls read tools: `list-strategies`, then `get-strategy-statistics` for each one.
3. If Claude tries a tool that is not on the list, for example `set-strategy-flag`, the call is denied and Claude is told so. Nothing reaches OHLCX.
4. The agent prints the result. Nothing was changed, and nothing could have been.

The SDK also has its own built-in tools (files, shell). `dontAsk` denies those that would ask, but some reads run without asking. To take tools away entirely, name them in `disallowedTools`. See Anthropic's [permissions page](https://code.claude.com/docs/en/agent-sdk/permissions).

A longer list can be kept short with a pattern after the server prefix, for example `mcp__ohlcx__list-*`. Check each pattern against the tool reference first: a name pattern is not a kind. `get-` and `list-` tools are reads in this server; `set-`, `update-`, `create-`, `delete-`, `clear-`, `deploy-`, `retain-` and `run-backtest` tools are not.

### A write that a person confirms

For a write, a person has to see the call and agree. In the SDK that is the `canUseTool` callback. It runs only for calls that nothing earlier approved, so:

- keep the write tools **out of** `allowedTools`. A tool on that list never reaches the callback;
- set `permissionMode: "default"` explicitly;
- show the person the tool and its arguments, with accounts by their masked labels, and wait.

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Replace with your application's own confirmation: a dialog, a chat message, a ticket.
async function askUser(question: string): Promise<boolean> {
  throw new Error("Connect this to your own confirmation step");
}

for await (const message of query({
  prompt: "Send strategy 7's orders to my account ending 678.",
  options: {
    mcpServers: {
      ohlcx: {
        type: "http",
        url: "https://ohlcx.example.com/mcp/ohlcx",
        headers: {
          Authorization: `Bearer ${process.env.OHLCX_MCP_TOKEN}`
        }
      }
    },
    allowedTools: [
      "mcp__ohlcx__get-strategy",
      "mcp__ohlcx__list-strategy-accounts"
    ],
    permissionMode: "default",
    canUseTool: async (toolName, input) => {
      const approved = await askUser(
        `Allow ${toolName} with ${JSON.stringify(input)}?`
      );
      if (approved) {
        return { behavior: "allow", updatedInput: input };
      }
      return { behavior: "deny", message: "User declined" };
    }
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

What happens:

1. Claude calls `get-strategy` and `list-strategy-accounts`. Both are reads on the allow-list and run at once.
2. Claude decides to call `set-strategy-accounts` with `{"strategy_id": 7, "mode": "selected", "account_ids": [4]}`. The tool is not on the allow-list, so the SDK calls `canUseTool`.
3. Your application shows the person the call, naming account 4 by its masked label `*****678`, and waits.
4. On yes, the call runs. On no, Claude is told "User declined" and nothing is sent.
5. If the strategy is deployed, the server refuses with "Retain the strategy before changing it." Claude then needs `retain-strategy`, which is another write and another confirmation.

Setting the accounts does not switch orders on. Switching orders on (`set-strategy-flag`) and deploying (`deploy-strategy`) are separate writes, each with its own confirmation. The whole sequence is on [Strategies and order routing](strategy-routing.md#the-sequence).

In Python the callback is `can_use_tool`, and it returns `PermissionResultAllow(updated_input=...)` or `PermissionResultDeny(message=...)`. Anthropic's example for it uses a streaming prompt and a hook that keeps the stream open: follow [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input) for the current form.

## Messages API: the MCP connector

The Messages API can connect to a remote MCP server itself, with the beta header `anthropic-beta: mcp-client-2025-11-20`. Whether the OHLCX server qualifies:

| Requirement of the connector | OHLCX server |
|------------------------------|--------------|
| Publicly exposed over HTTP; the URL must start with `https://` | Yes, if your OHLCX host is on the public internet with HTTPS. A local or private host does not qualify |
| Streamable HTTP or SSE transport | Yes: Streamable HTTP at `/mcp/ohlcx` |
| Only tool calls are supported | The tools work. The three prompts and the `ohlcx://strategy-settings` resource are not available through the connector |
| `authorization_token`, documented as an OAuth token | The OHLCX server expects its own API token as a bearer header. Check your version: this page did not verify that the connector accepts an OHLCX token in `authorization_token` |

The connector takes the server in `mcp_servers` and a toolset in `tools`. To allow only chosen tools, set `enabled` to `false` by default and enable tools by name:

```json
{
  "model": "claude-opus-5-5",
  "max_tokens": 1000,
  "messages": [{ "role": "user", "content": "List my strategies." }],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://ohlcx.example.com/mcp/ohlcx",
      "name": "ohlcx",
      "authorization_token": "<token>"
    }
  ],
  "tools": [
    {
      "type": "mcp_toolset",
      "mcp_server_name": "ohlcx",
      "default_config": { "enabled": false },
      "configs": {
        "list-strategies": { "enabled": true },
        "get-strategy": { "enabled": true },
        "list-accounts": { "enabled": true }
      }
    }
  ]
}
```

With the connector, Anthropic's servers call the tool during the request. Your code does not see a call before it runs, so there is no place for a person to confirm one. Use the connector for read-only agents, with an allow-list as above. For a write, enable that one tool only in a request your application sends after the user has confirmed, or use the Agent SDK.

Because the resource is not available through the connector, an agent that creates strategies or changes settings this way has no settings reference. Prefer the Agent SDK for that work.

## Any other MCP client

The server speaks the Model Context Protocol, so any conforming client can use it. In terms of the specification:

| Item | Value |
|------|-------|
| Transport | Streamable HTTP: JSON-RPC messages sent with `POST` to `/mcp/ohlcx`. `GET` answers 405 |
| Local transport | stdio: `php artisan mcp:start ohlcx` |
| Protocol revisions | `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05` |
| Authorization | `Authorization: Bearer <token>` on every request. No OAuth discovery |
| Capabilities | Tools, resources and prompts. The lists do not change during a session |
| Session | When the server returns an `MCP-Session-Id` header, send it back on later requests |

Three things a client must get right:

1. **Follow `nextCursor` on `tools/list`.** The server returns the tool list in pages of 15 by default (at most 50 per page). A client that reads only the first page sees 15 tools. Request the next page with the `cursor` it was given until there is none.
2. **Read each tool's `annotations`** from `tools/list` and build your allow-list from `readOnlyHint`. This is where a client can restrict by annotation rather than by name.
3. **Treat a tool result with `isError: true` as a sentence to act on**, not as a transport failure. See [Errors and refusals](errors.md).

## Refusals and limits

- An agent must tell a refusal from a fault. A refusal names what stands in the way; a fault says only that something could not be done. What to do with each kind is on [Errors and refusals](errors.md#a-rule-of-thumb-for-clients).
- Retry only the "try again" kind, with a pause and a small fixed number of attempts. Never retry a refusal unchanged.
- List tools page or cap their answers. An agent that needs everything has to follow pages and cursors: see [Limits and paging](limits-and-paging.md).
- `list-strategies`, `list-signals` and `list-conditions` can be up to a minute behind changes made in the OHLCX app.
- Account ids come from `list-accounts`. Show people masked labels. See [Accounts and identifiers](accounts.md).

## Checklist before you leave an agent unattended

1. It uses its own token, read from the environment, for a user who is not an admin.
2. Its allow-list holds only tools of kind Read, and calls outside the list are denied, not asked.
3. It stops when the server is unavailable or the token is refused.
4. It does not retry refusals.
5. Nothing it can call switches a strategy or its orders on, sets order accounts, changes settings, deploys, retains or deletes.
