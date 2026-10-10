# In-app AI assistant

The trading UI talks to the assistant in two places: the assistant **drawer**, with three modes, and the **Ask OHLCX** panels on a backtest run, on the Strategies page and in a strategy's settings. Answers stream over server-sent events.

Which tools each mode has is in [`agents.md`](agents.md). The MCP server for outside clients is separate from everything on this page.

---

## Modes and endpoints

| Label in UI | HTTP | Sign-in | Rate limit |
| ----------- | ---- | ------- | ---------- |
| AI Support Assistant | `POST /api/ai/agents/support` | optional | 60 a minute |
| AI Trading Assistant | `POST /api/ai/agents/trading` | required | 60 a minute |
| AI Assistant | `POST /api/ai/agents/assistant` | optional | 60 a minute |

A guest gets the three knowledge tools only. Voice output, image attachments and saved conversations need a signed-in user.

Other endpoints: `POST /api/ai/agents/voice`, `POST /api/ai/agents/voice/realtime-token`, `POST /api/ai/agents/speak`, `GET /api/ai/agents/attachments`, and the conversation endpoints under `/api/ai/agents/conversations`.

### Request body

| Field | Rule | Meaning |
| ----- | ---- | ------- |
| `message` | required, at most 16,000 characters (optional when images are attached) | The user's message. |
| `conversation` | optional list | Earlier turns. |
| `stream` | boolean, default true | Server-sent events when true, one JSON answer when false. |
| `persist` | boolean, default true | False keeps the exchange out of the user's saved conversations. Usage is still recorded. |
| `conversation_id` | optional | The saved conversation to add to. |
| `voice_output`, `voice` | optional | Spoken output, for signed-in users. |
| `page_context` | optional object, `assistant` endpoint only | What the page shows. See below. |

A streamed answer is a sequence of `data:` lines, each a JSON event (text as it is written, and the result of each tool the assistant called), ended by `data: [DONE]`. A turn that fails is described under "A failed turn" below.

### A failed turn

A failed turn ends with one `error` event, then `data: [DONE]`:

```
data: {"type":"error","code":"timeout","error":"The request took too long. Try again, or ask for less at once.","retryable":true}
```

The keys are `type`, `code`, `error` and `retryable`, in that order. `error` is a fixed sentence for the code, so a client that knows no codes can show it. Nothing else about the cause is sent. It goes to the server log.

| `code` | `error` | `retryable` | When | Status with `stream: false` |
| ------ | ------- | ----------- | ---- | --------------------------- |
| `timeout` | The request took too long. Try again, or ask for less at once. | true | A request to the model timed out. Also when the model sent nothing for about the whole timeout and the stream then ended. | 504 |
| `busy` | The assistant is busy right now. Try again in a moment. | true | The model is rate limited or overloaded, on every provider tried or after part of the answer was sent. Also when one provider is busy and the other is out of credits. | 503 |
| `too_long` | This conversation is too long to continue. Start a new one. | false | The request is larger than the model accepts. | 413 |
| `step_limit` | The assistant could not finish in the allowed steps. Try a narrower question. | true | The assistant used all of its steps and the last thing that happened was a tool result. | 502 |
| `unavailable` | The assistant is not available right now. | false | Every provider is out of credits. | 402 |
| `failed` | The assistant could not answer. Try again. | true | Anything else. Also a stream that ended without the provider's end event, and one that ended with no text and no tool call. | 502 |

- Events that were already sent stay sent. Text and tool results (cards included) come before the error event. When the stream itself ended normally (`step_limit`, and the `timeout` and `failed` cases that follow an end) and the exchange is saved, `conversation_id` comes before the error event as well.
- An assistant has 12 steps, and each request to the model may take 120 seconds. A step is one round of tool calls. The error is sent only when the 12th round was reached. Tool calls and no text below that are an ordinary end: no error, and a card or a changed setting is a whole answer.
- When a provider is out of credits, rate limited or overloaded, the next provider is tried, but only while nothing of the answer has been sent. A tool call counts as sent, so a tool never runs twice.
- A request with `stream: false` answers the same object as JSON, with the status in the last column.
- A request refused before the stream starts (for example 401, 419, 422 or 429) is not a failed turn and carries no `code`.
- The browser keeps a failed turn in the conversation and sends it back to the server as one fixed assistant line, such as "[This request was not answered: it took too long.]". When text had already arrived, the line follows that text as "[This answer was cut off: ...]". The assistant is told to say only what the line says and never to guess why.

---

## Page context

A page may send `page_context` with a message, so the assistant can answer about what is on screen.

It is read only for a signed-in user, on OHLCX Pro, with Ask OHLCX switched on. Anywhere else it is ignored and the assistant behaves as if the page had sent nothing.

The page context comes from the browser, so the server treats it as data and nothing more:

- It must be one of three kinds: `backtest_run`, `strategy_builder`, `strategy_routing`.
- It is limited to 12,000 bytes. A block that is too large or of another kind is refused with status 422.
- The assistant is shown a block the server rebuilt from keys, numbers and codes it already knows, never the block as sent. Text typed by anyone is cleaned and shortened or left out.
- The assistant is told the block is data, not instructions.

| Kind | Page | What it lets the assistant do |
| ---- | ---- | ----------------------------- |
| `backtest_run` | A backtest run | Explain the run from its figures; propose one change to test or one sweep. |
| `strategy_builder` | The Strategies page | Propose one draft strategy from the listed condition shapes. |
| `strategy_routing` | A strategy's settings | Propose which linked accounts receive the strategy's orders. |

---

## Ask OHLCX

Ask OHLCX is the assistant with a page context.

| Step | What the user gets |
| ---- | ------------------ |
| 1. Explain a run | Answers about the open run from its own figures: which hours, weekdays, exit kinds and sides made or lost money, always with trade counts. The assistant can also find and read a saved run. |
| 2. Suggestion cards | One change to test, as a card with a "Run as what-if" button. At most 4 settings, and only settings the page says a what-if can change. |
| 3. What-if | After the what-if ran, the assistant reads the comparison back in the card's own words: the gain held, faded, did not hold, or there were too few trades to tell. |
| 4. Sweeps and drafts | One sweep of one or two settings, as a card with a "Run this sweep" button (2 to 200 combinations), read back afterwards with the reasons to doubt it first. On the Strategies page, one draft strategy as a card with a "Create this strategy" button (1 to 8 conditions). |

A strategy's settings add a fifth card: "Set these accounts", for the accounts the strategy's orders go to.

Rules that hold throughout:

- The assistant describes a change as something to test, never as a trade to place.
- It never calculates a figure that is not in front of it, and never guesses one.
- A proposing tool runs nothing, creates nothing and saves nothing.

### Switches

Ask OHLCX needs the server setting and a build switch of the front end. All are off by default, and all are for OHLCX Pro.

| Panel or feature | Server setting | Front-end build switch |
| ---------------- | -------------- | ---------------------- |
| "Ask about this run" on a backtest run | `TRADING_APP_RUN_ASSISTANT=true` | `VITE_RUN_ASSISTANT=true` |
| Suggestion cards | the same | also `VITE_RUN_ASSISTANT_SUGGESTIONS=true` |
| Comparing a what-if and checking it on the earlier period | the same | also `VITE_RUN_ASSISTANT_EVALUATE=true` (with suggestion cards on) |
| Proposed sweeps | the same | also `VITE_RUN_ASSISTANT_SWEEPS=true` (with suggestion cards on) |
| Running a proposed sweep on the server | the same | also `VITE_BACKTEST_SERVER_RUNS=true` |
| Drafting a strategy on the Strategies page | the same | `VITE_STRATEGY_ASSISTANT=true` (independent of the backtest switches) |
| "Ask about order accounts" in a strategy's settings | the same | `VITE_STRATEGY_ROUTING_ASSISTANT=true` (independent of the others) |

The server has one switch for all of it. The front-end switches only show or hide a panel or a card.

What the panels do, beyond the steps above:

- A panel's conversation is not saved to the user's assistant history and does not appear in the drawer. It lasts while the page is open.
- The backtest panel sends the run as figures only, at most 10,000 bytes. Trades and the equity curve are never sent.
- "Run as what-if" runs the run on screen again with the card's change and nothing else, over the same period. It is refused, with a plain message, when the strategy on the page is no longer the one the run was made from.
- "Show those trades" on a suggestion card narrows the trades tab to the hour, weekday, exit or side the suggestion names.
- The what-if comparison is judged by the page, on net profit, as one of nine fixed outcomes with one fixed sentence each. The assistant is handed that sentence and never works out a difference itself.
- A proposed sweep always holds back 30% of the period to check the best result.
- Creating a strategy from a draft has three outcomes: created, refused (nothing was stored, and the card offers the button again), or not known (the card says to check the strategies list and offers no second try).
- One draft creates at most one strategy: a second click on the same card does nothing.

---

## Cards: a proposal and a click

A proposing tool does one thing: it returns a proposal, which the page draws as a card with a button. Nothing changes until the user presses the button.

1. The page sends its context with the user's message.
2. The server reads the context and decides which proposing tool, if any, the assistant has for this answer. The tool is built with the list of what it may propose, taken from the page. The assistant cannot add to that list.
3. The assistant calls the tool. The tool checks the proposal against its list and returns either one sentence saying why not, or the proposal.
4. The page receives the proposal, checks it again against what it knows now, and draws the card. Names and labels on the card come from the page, not from the assistant.
5. The user presses the button. The page sends an ordinary request from the user's own session, the same request the form on that page would send. The server decides, as it does for the form.

An answer carries at most one card.

| Card | Button | What the click does |
| ---- | ------ | ------------------- |
| A change to test | Run as what-if | Runs the open backtest again with the change. The strategy is not changed. |
| A sweep | Run this sweep | Runs the sweep. The strategy is not changed. |
| A draft strategy | Create this strategy | Creates the strategy switched off: demo, paused, not deployed, with signals, trades, orders and notifications off. |
| Order accounts | Set these accounts | Saves which accounts receive the strategy's orders. It never switches orders on and never deploys the strategy. |

### The accounts card

- It exists only in a strategy's settings, on OHLCX Pro, for a strategy that is not deployed, when at least one linked account can receive orders.
- The assistant knows an account only as an id, a masked label such as `*****678`, and whether orders can go there. It never sees an account number.
- It can propose only accounts from the page's list that can receive orders, or "all".
- It proposes accounts only when the user asked for it in that message.
- A deployed strategy's settings are locked. The assistant says the strategy has to be retained first.

### The outside-content rule

In an answer in which the assistant has read text that someone other than the user wrote, it cannot propose accounts. The user reads:

> Accounts cannot be suggested in an answer that also read a web page, news, an article or messages. Ask again in a new message.

The reason: a web page, a news item or a chat message can contain instructions aimed at the assistant, and this card decides where real orders go. Thirteen tools count as reading outside text: `fetch_ohlcx_webpage`, `list_news`, `get_analysis`, `get_knowledge_base_article_by_slug`, `search_knowledge_base_articles`, `get_community_messages`, `list_community_channels`, `discover_community_groups`, `search_community_users`, `list_activities_feed`, `get_sector`, `get_billing_summary`, `get_user_billing`. A new message starts clean.

---

## Prerequisites for local use or recording

1. **Dependencies and env**: install the host application as its own README describes (Composer, `.env`, application key, database migrate and seed).
2. **Knowledge base content**: seed the knowledge base so its answers are substantive.
3. **AI providers**: keys configured in `.env` (for example `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
4. **Assets**: `npm run dev` or `npm run build` so the trading UI loads.
5. **For Ask OHLCX**: `APP_VERSION=pro` and `TRADING_APP_RUN_ASSISTANT=true`.

---

## Video demo script (copy-paste messages)

Use this sequence for a balanced demo: product overview, knowledge base, orders and terminology, authenticated trading data, optional Pro markets, unified mode, and a follow-up turn.

**Before recording:** Log in for the Trading and unified sections. For the optional Pro step, set `APP_VERSION=pro`; otherwise skip step 6 or narrate "Pro feature."

1. **Support mode**: open the assistant; confirm title **AI Support Assistant**.
   **Message:** `In one short paragraph, what is OHLCX and who is it for?`

2. **Knowledge base**
   **Message:** `How do I search the knowledge base from the app, and what's the difference between support requests and reporting an issue?`

3. **Product depth / orders**
   **Message:** `Walk me through placing an OCO equity order at a high level, and link any caveats from the docs.`

4. **Trading mode**: switch to **AI Trading Assistant** (requires login).
   **Message:** `Summarize my linked brokerage accounts and my trading strategies. If you can't access something, say what's missing.`

5. **Signals**
   **Message:** `What signals do I have lately, and how would you suggest I use them alongside my strategies?`

6. **Optional (Pro)**
   **Message:** `List available markets and give me a one-line description of the first five.`

7. **AI Assistant (unified)**: switch to **AI Assistant**.
   **Message:** `I want a single checklist: onboarding tasks I should complete, then anything specific you can infer about my account from tools.`

8. **Follow-up (conversation memory)**
   **Message:** `Expand only the highest-priority item from that checklist and point me to the right KB article slug or title if you found one.`
