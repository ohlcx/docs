# In-app AI assistant

!!! note "Private implementation paths"
    Code paths like `resources/js/components/` and `src/Ai/` refer to the private **`ohlcx/trading-app`** package. Authorized contributors clone the package or run `composer install` in a host app.

The trading UI includes a drawer-based **AI assistant** with three modes. It streams responses over **SSE** from Laravel AI agents.

**Related docs**

- [`agents.md`](agents.md) — full agent/tool matrix, MCP bridge, tests
- [MCP overview](../mcp/overview.md) — OHLCX MCP server (Cursor / `php artisan mcp:start ohlcx`)

---

## Where it lives in the app

- **UI:** `resources/js/components/AgentAssistantDrawer.jsx` — maps mode to API route, renders chat, handles streaming.
- **Mode toggle:** `resources/js/components/RightSidebar.jsx` — opens the drawer and switches Support / Trading / AI Assistant (unified).
- **Backend:** `src/Http/Controllers/Api/Agents/AgentController.php` in the trading-app package
- **Routes:** `routes/ai-agents.php` is `require`d from package `routes/api.php` (hosts should not duplicate this include)

---

## Modes and endpoints

| Label in UI | Internal `agentType` | HTTP | Middleware |
| ----------- | -------------------- | ---- | ---------- |
| AI Support Assistant | `support` | `POST /api/ai/agents/support` | `throttle:60,1` |
| AI Trading Assistant | `trading` | `POST /api/ai/agents/trading` | `auth:sanctum`, `throttle:60,1` |
| AI Assistant | `auto` | `POST /api/ai/agents/assistant` | `throttle:60,1` |

**Support** uses `SupportKnowledgeAgent` (knowledge base tools only; no account data).

**Trading** requires a logged-in session (Sanctum). Uses `TradingAssistantAgent` with the user’s strategies, accounts, and KB; **Pro** builds add live market/sector/calendar tools when `APP_VERSION=pro` (and matching frontend env — see [`agents.md`](agents.md)).

**AI Assistant (auto)** uses `UnifiedAssistantAgent`: KB always; if the browser session is authenticated, it can also use strategies, accounts, signals, activities, analysis, news; **Pro** adds the same market-family tools as trading.

---

## Prerequisites for local use or recording

1. **Dependencies and env** — Follow [OHLCX Pro setup](../setup/ohlcx-pro.md) or [OHLCX Light setup](../setup/ohlcx-light.md) (private repos).
2. **Knowledge base content** — e.g. `php artisan trading-app:seed` so KB-backed answers are substantive.
3. **AI providers** — Keys configured per `config/ai.php` / `.env` (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
4. **Assets** — `npm run dev` or `npm run build` so the trading UI loads.
5. **App URL** — Serve the app (e.g. `php artisan serve` or your usual host); ensure `VITE_APP_URL` matches.

**Optional realtime stack** (Horizon, Reverb) from the main README is not required for the assistant HTTP endpoints themselves, but matches a full trading demo environment.

---

## Laravel AI tools (in-app agents)

Agents call a **read-focused** set of Laravel AI tools in `src/Ai/Tools/`. There are **17** registered `name()` strings; which appear depends on agent, auth, and Light vs Pro.

Authoritative table: **[`agents.md` — AI tool names](agents.md)** (section *AI tool names*).

Summary groups:

- **Knowledge base:** `search_knowledge_base_articles`, `get_knowledge_base_article_by_slug`
- **Trading / account (authenticated):** strategies, brokerage accounts, signals, strategy activities, analysis, news
- **Pro-only markets:** markets, tickers, sectors, calendar, market balance, sector balance

---

## MCP (IDE / Cursor): prompts and tools

The in-app drawer is **separate** from the OHLCX MCP server. If you are automating or testing from Cursor:

- **Machine-readable catalog:** [MCP tools index.json](../mcp/tools/index.json) — lists every MCP tool name, admin flags, and **MCP prompts**.
- **MCP prompts:** `user-info` (authenticated sessions), `trading-terminology`, `support-knowledge-base`.
- **LLM bridge tools:** `run-support-agent` (no MCP auth required for listing), `run-trading-agent` (authenticated MCP session only).
- **Data tools:** 80+ additional MCP tools (CRUD, admin, messaging, etc.) — see [MCP tool catalog](../mcp/tools/README.md).

For deterministic data without an LLM, prefer direct MCP **data** tools; use bridge agents when you want the same agents as the app with multi-step tool use.

---

## Video demo script (copy-paste messages)

Use this sequence for a balanced demo: product overview, KB, orders/terminology, authenticated trading data, optional Pro markets, unified mode, and a follow-up turn.

**Before recording:** Log in for Trading and unified-account sections. For the optional Pro step, set `APP_VERSION=pro` and matching Vite app version per [`agents.md`](agents.md); otherwise skip step 6 or narrate “Pro feature.”

1. **Support mode** — Open the assistant; confirm title **AI Support Assistant**.  
   **Message:** `In one short paragraph, what is OHLCX and who is it for?`

2. **Knowledge base**  
   **Message:** `How do I search the knowledge base from the app, and what's the difference between support requests and reporting an issue?`

3. **Product depth / orders**  
   **Message:** `Walk me through placing an OCO equity order at a high level, and link any caveats from the docs.`

4. **Trading mode** — Switch to **AI Trading Assistant** (requires login).  
   **Message:** `Summarize my linked brokerage accounts and my trading strategies. If you can't access something, say what's missing.`

5. **Signals**  
   **Message:** `What signals do I have lately, and how would you suggest I use them alongside my strategies?`

6. **Optional (Pro)**  
   **Message:** `List available markets and give me a one-line description of the first five.`

7. **AI Assistant (unified)** — Switch to **AI Assistant**.  
   **Message:** `I want a single checklist: onboarding tasks I should complete, then anything specific you can infer about my account from tools.`

8. **Follow-up (conversation memory)**  
   **Message:** `Expand only the highest-priority item from that checklist and point me to the right KB article slug or title if you found one.`

---

## Developers

- **Tests:** [Testing AI and MCP](testing.md)
