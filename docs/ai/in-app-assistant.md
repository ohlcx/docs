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

## The Screener, watchlists and account results

A signed-in user can ask the Trading and the AI Assistant modes about three more subjects. They work on OHLCX Light and on OHLCX Pro, and need nothing switched on.

| Subject | What the assistant can answer |
| ------- | ----------------------------- |
| The Screener | What gapped in a market, one symbol's gap history and how each gap played out, and a market's symbols by their technical readings. These are the Screener page's three screens, read when asked. |
| Watchlists | Which watchlists the user has, built-in ones included, and the symbols of one of them. |
| Account results | The realized profit and loss of one of the user's linked accounts for a period, by day, week or month, the same by symbol, and the account's balance over time. |

Each answer is a sentence or two with the few figures or symbols that matter. The assistant does not write the rows out as a table or a list, and these tools draw no card. It names the period it used, so that "this month" and "the last 30 days" are not mixed up. With more than one linked account, the tool refuses until one is named by its id. If an account has never synced, or its sync failed, it says the figures may be incomplete.

What it cannot read:

- **Saved screeners.** There are none. The Screener page is three fixed screens, and the assistant has no list of screeners to read or a definition to open.
- **Prices in a watchlist.** A watchlist holds symbols only. On OHLCX Pro the assistant can look up a price for a few symbols, one at a time.
- **Single closed trades, deposits and withdrawals** of an account, and it cannot start a profit and loss sync.
- **Anything it would have to change.** It cannot create, rename or change a watchlist, or save a screener.

### Hide Account Balance

If the user has "Hide Account Balance" switched on in Preferences, an answer about the user's accounts holds no amount of money. This covers the list of linked accounts (no balances or buying power), profit and loss (no profit, loss, fees or daily average) and the balance over time (no balances). Percentages, counts and dates are still given. The assistant says that amounts are hidden by that preference and does not estimate them. A result that cannot tell whether the preference is on is treated as hidden. Each of these results says `balances_hidden`, true or false, so a card drawn from one can rely on it.

The MCP server's own account tools do not follow this preference. A client that reads an account through them gets the figures. The assistant reached through the MCP tool `run-trading-agent` does follow it.

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
| `backtest_run` | A backtest run | Explain the run from its figures; propose one change to test or one sweep; show trades, a breakdown of them or headline figures as cards, where the page says it can draw them. |
| `strategy_builder` | The Strategies page | Propose one draft strategy from the listed condition shapes. |
| `strategy_routing` | A strategy's settings | Propose which linked accounts receive the strategy's orders. |

A page of any of the three kinds may also send a list named `cards`. On a run it names the cards the page can draw. On every kind it may name `"handoff"`: the page can draw the button that opens the main AI Assistant. The assistant is never shown the list.

### What a panel can reach

In the drawer the assistant has its whole list of tools. On a page that sends a page context it has only the tools that fit that page:

| Panel | It can |
| ----- | ------ |
| "Ask about this run" (also under a sweep's results) | Show the run's cards and propose a change or a sweep; read saved runs; read the list of strategies and one strategy's settings, conditions, recent signals and trades, and results; search the knowledge base; read the OHLCX website; read a symbol's daily or weekly price history. |
| "Draft a strategy" | Propose a draft; read the list of strategies and one strategy's detail; search the knowledge base; read the OHLCX website; read a symbol's daily or weekly price history. |
| "Ask about order accounts" | Propose the accounts; read the strategy's order accounts and the linked accounts; read the list of strategies; search the knowledge base; read the OHLCX website. |

What a panel will not answer: anything else, such as account balances on a backtest run, news, the Screener, watchlists, billing or settings. Asked for one of those, it says in one short sentence that this page cannot do that part, shows a button that opens the main AI Assistant with the question (or says so in words, where the page cannot draw the button), and answers the rest of the question as usual. It is told never to offer to look such a thing up itself and never to answer it from memory. It cannot change Settings or Preferences from a panel.

This is on by default. A host turns it off with `TRADING_APP_ASSISTANT_SCOPED_TOOLS=false` on the server; every panel then has the whole list again.

### Price history

On OHLCX Pro the assistant can read a symbol's price history with `get_ticker_bars`: its latest 5, 20 or 60 daily or weekly bars, with the change, the high and the low of that stretch, or what it did on one day. It states only figures that are in the result. For a day the market was closed it says so and names the last trading day before it. There are no intraday bars. It has this in the drawer, on a backtest run and on the Strategies page.

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
| Trades shown as a card in "Ask about this run" | the same | also `VITE_RUN_ASSISTANT_TRADES=true` (needs only the panel's own switch) |
| A breakdown of the trades shown as a card | the same | also `VITE_RUN_ASSISTANT_BREAKDOWN=true` (needs only the panel's own switch) |
| Headline figures shown as tiles | the same | also `VITE_RUN_ASSISTANT_STATS=true` (needs only the panel's own switch) |
| The equity and drawdown chart shown as a card | the same | also `VITE_RUN_ASSISTANT_EQUITY=true` (needs only the panel's own switch) |
| "Undo last change" and "Start over" in "Ask about this run" | none: the server is told nothing new | also `VITE_RUN_ASSISTANT_UNDO=true` (with suggestion cards on) |
| Drafting a strategy on the Strategies page | the same | `VITE_STRATEGY_ASSISTANT=true` (independent of the backtest switches) |
| "Ask about order accounts" in a strategy's settings | the same | `VITE_STRATEGY_ROUTING_ASSISTANT=true` (independent of the others) |
| The hand-off card on the three panels ("Ask in the AI Assistant") | the same | also `VITE_ASSISTANT_HANDOFF=true` (needs the panel's own switch, and the main AI Assistant on the page) |

The server has one switch for all of it. The front-end switches only show or hide a panel or a card. A second server setting, `TRADING_APP_ASSISTANT_SCOPED_TOOLS` (on by default), decides whether a panel's assistant has only the tools of its page; see "What a panel can reach".

One of them has an order to keep. `VITE_RUN_ASSISTANT_TRADES` also tells the server that the page can draw the trades card, and the server offers the tool that shows trades only then. Switch it on only on a host whose installed package has that tool (`show_backtest_trades`) in the release where its filters are one `filters` list. The first shape of the tool had one argument for each filter, and a model given that shape may fill in every one, so that the card shows nothing. On an older package the page would still say it can draw the card, the assistant would read that with no tool and no rule behind it, and no card would ever come. Update the package first, then set the switch and build.

The same order holds for `VITE_RUN_ASSISTANT_BREAKDOWN` and `VITE_RUN_ASSISTANT_STATS`. With either on, the page sends a list named `cards` with the run (`"trades"`, `"breakdown"`, `"stats"`: the ones it can draw), and the server offers `show_backtest_breakdown` and `show_backtest_stats` only for a name in that list. The package release that has those two tools and reads the list must be installed first. On an older package the list would reach the assistant as a key it knows nothing about, and no card would come. With both switches off the page sends no list, and what it sends is exactly what it sent before these cards. `"breakdown"` is listed only for a run whose every trade the page holds: a run that stored only some of its trades gets no breakdown card.

`VITE_RUN_ASSISTANT_EQUITY` works the same way: with it on the page adds `"equity"` to that list (and sends the list for it alone), and the server offers `show_backtest_equity` only then. Install the package release that has that tool first. A package that reads the list but does not know `"equity"` ignores that one name and keeps the other cards; no chart card comes. `"equity"` is listed only for a run whose equity curve the page holds: a saved run opened without one is not offered the card. With the switch off nothing the page sends or shows is different.

`VITE_ASSISTANT_HANDOFF` adds one name, `"handoff"`, to the same kind of list, on all three panels: on a backtest run it joins the names above (and brings the list by itself; under a sweep's results it is the only name), and on the Strategies page and in a strategy's settings the page sends a `cards` list for the first time, holding that one name. The server offers `suggest_main_assistant` only for a page that lists it. The page lists it only where the main AI Assistant can be opened: OHLCX Pro, signed in, with Embedded AI on, so that its drawer is on the page. The order of installing matters less here than for the other cards: a package that reads `cards` on a run ignores a name it does not know, and on the other two kinds of page the package builds what the model reads from the checked parts only, so a key it does not know is dropped and never reaches the model. Without the tool no card comes, and nothing else changes. With the switch off nothing the page sends or shows is different.

What the panels do, beyond the steps above:

- A panel's conversation is not saved to the user's assistant history and does not appear in the drawer. It lasts while the page is open.
- The backtest panel sends the run as figures only, at most 10,000 bytes. Trades and the equity curve are never sent.
- "Run as what-if" runs the run on screen again with the card's change and nothing else, over the same period. It is refused, with a plain message, when the strategy on the page is no longer the one the run was made from.
- "Show those trades" on a suggestion card narrows the trades tab to the hour, weekday, exit or side the suggestion names.
- The what-if comparison is judged by the page, on net profit, as one of nine fixed outcomes with one fixed sentence each. The assistant is handed that sentence and never works out a difference itself.
- A proposed sweep always holds back 30% of the period to check the best result.
- Creating a strategy from a draft has three outcomes: created, refused (nothing was stored, and the card offers the button again), or not known (the card says to check the strategies list and offers no second try).
- One draft creates at most one strategy: a second click on the same card does nothing.

### Undoing a change

With `VITE_RUN_ASSISTANT_UNDO=true`, a change run from a card can be taken back without reloading the page. Two buttons appear in the panel once a card's what-if or sweep has run:

- **Undo last change** puts back the run from before the most recent change, and the form with it. Press it again to go back one more.
- **Start over** puts back the run from before the first change, in one step.

What to know:

- The run comes back exactly as it was: trades, equity curve, metrics, charts, the comparison it had and the form's settings. Nothing is run again and nothing is written. One thing may be read again: the price chart of a saved run, if it was still loading when the change started.
- The cap is five: the page keeps the last five runs to go back to, besides the one on screen. The run to start over from is always one of them. After a sixth change in a row, the oldest step in between is dropped, and the last press of Undo then undoes several changes at once and goes straight to the start; its tooltip says how many.
- Opening one of the combinations of a sweep that a card ran is one more change, undoable like the others: one step back shows the sweep's results again, and Start over still returns to the first run.
- The conversation is not rewound. A line in it says "The last change was undone. The run on screen is the one before it." What was said about the undone run stays, marked by a line above it, and is no longer sent to the assistant. The assistant is told in one fixed sentence that the change was undone. After several steps back there is still one line at each end of what was undone, and the assistant still gets one sentence.
- The card that was tried says "This change was tried and then undone. It can be run again." and has its button back. Cards from answers about the undone run have no button.
- Pressing either button while a what-if, a sweep or an answer is still running stops it first. A what-if that was stopped is not saved.
- Nothing saved is changed or deleted. If the form saves runs, a what-if that finished is already in Run history and stays there after an undo; the line in the conversation says so.
- **New conversation** is something else: it clears what was said and leaves the run on screen as it is.
- Running the backtest yourself, running a sweep from the form (or opening one of its combinations), opening a saved run or a server sweep, applying changes to the strategy or leaving the page ends it: there is nothing to undo after that. Editing the form without running does not end it; going back then overwrites the edit.

---

## Cards: a proposal and a click

A proposing tool does one thing: it returns a proposal, which the page draws as a card with a button. Nothing changes until the user presses the button.

1. The page sends its context with the user's message.
2. The server reads the context and decides which proposing tool, if any, the assistant has for this answer. The tool is built with the list of what it may propose, taken from the page. The assistant cannot add to that list.
3. The assistant calls the tool. The tool checks the proposal against its list and returns either one sentence saying why not, or the proposal.
4. The page receives the proposal, checks it again against what it knows now, and draws the card. Names and labels on the card come from the page, not from the assistant.
5. The user presses the button. The page sends an ordinary request from the user's own session, the same request the form on that page would send. The server decides, as it does for the form.

An answer carries at most one proposal.

| Card | Button | What the click does |
| ---- | ------ | ------------------- |
| A change to test | Run as what-if | Runs the open backtest again with the change. The strategy is not changed. |
| A sweep | Run this sweep | Runs the sweep. The strategy is not changed. |
| A draft strategy | Create this strategy | Creates the strategy switched off: demo, paused, not deployed, with signals, trades, orders and notifications off. |
| Order accounts | Set these accounts | Saves which accounts receive the strategy's orders. It never switches orders on and never deploys the strategy. |

Trades are the one card that is not a proposal. Asked to see trades of the open backtest run, the assistant shows them as a card and never writes them as a table: the page draws the card from the trades it already holds, with the same columns as the Trades tab, the totals of every match, and a button that opens them in the Trades tab. The assistant is not shown those trades. An answer can carry this card and a proposal together. For a saved run the assistant can also read single trades itself (at most 50 rows at a time, with totals); for a run that was never saved it cannot, and says so.

Three more cards show something and propose nothing, each behind its own switch:

- **A breakdown.** Asked which hours, weekdays, exits, sides, calls or puts, or months did well or badly, the assistant shows the trades split into groups: one row for each group with its loss and profit as two bars, its trades, its win rate and its result, the best and the worst group marked, and a last row for all of them together. It can narrow the trades first ("the losing trades by entry hour"), which no tab of the page does. Each row has a button that opens that group in the Trades tab, except a group of trades the tab cannot filter for (a side or an exit the engine does not know, a trade that is neither a call nor a put).
- **Headline figures.** Asked for an overview or for several figures side by side, the assistant shows one to six tiles like the ones at the top of the results. A figure the page does not hold is a dash, never zero. When the run on screen is a what-if the page is comparing with the run it came from, each tile also says what separates it from that run. The page decides that; the assistant cannot ask for it.
- **Equity and drawdown.** Asked to see the equity curve, the drawdown over time or how the equity moved, the assistant shows the chart of the results page inside the answer: the equity as a line and, under it, how far it was below its peak. It is always the whole run; the assistant cannot ask for a part of it. Under the title one line written by the page says where the equity started and ended, the change, and the largest fall from a peak with the day it was at its lowest. The amounts are the ones the results header shows. The header's largest fall in money and its largest in percent can be two different falls; the line then says them apart ("Largest fall from a peak: $4,000.00, at its lowest on Jan 10, 2026. Largest in percent: 12.0%.") and never as one. "Show as table" replaces the chart with a short table (the end of each day, or of each week or month for a long run, at most 31 rows: the equity then and how far that was below its peak), and "Open the chart" goes to the chart in the results, which has the zoom and the other controls. The assistant is shown no point of the curve: it is told not to describe its shape and to state no value or date from it. When several answers of one conversation show the chart, only the newest draws it by itself; an older one keeps its line and a button that draws it there too.

The page draws all three from the run it holds. The assistant is shown no number by any of them and is told to state none from them. An answer may carry trades, a breakdown, figures, the equity chart and one proposal together, one of each. The cards, the results header and the Metrics tab write a win rate and a sum of profits by one rule (a win rate to one decimal, money to the cent, worked out as the server works them out), so no two of them show different numbers for the same trades. After a what-if, or after a change is undone, a card that was drawn for another run says so and shows no live figure: a breakdown shows its title only, the tiles become one line of the figures as they were shown then, under "Figures of an earlier run", and the equity card becomes its title and the line it had then, under "Equity and drawdown of an earlier run", with no chart.

### The hand-off card

Each panel's assistant has only the tools that fit its page. Asked for anything else (an account balance on a backtest run, a watchlist on the Strategies page), it says the page cannot do that and, with `VITE_ASSISTANT_HANDOFF` on, shows a small card under its answer:

- One line: "This page can't do that. Ask the main AI Assistant."
- One button: "Ask in the AI Assistant". It opens the AI Assistant drawer of the right sidebar and asks the user's own question from that turn there, as if they had typed and sent it. When the drawer already holds a conversation (one in progress, or the last one, which it opens by itself), a new chat is started first, as the drawer's New chat button does, so the question is not answered on top of something unrelated. The earlier conversation is not deleted: it stays in the drawer's history list. In an empty drawer the question is simply asked. What the user was typing in the drawer's message box is kept; pictures they had chosen there are dropped when a new chat is started, since they belonged to the conversation that is left.
- Once the question was sent the button reads "Sent to the AI Assistant" and cannot be pressed again for that card. Asking the same thing again in the panel gives a new card.
- If the drawer is busy (an answer is arriving there, or the microphone is on), or the question is longer than one message may be (16,000 characters), the question is put in the drawer's message box and not sent, and no new chat is started. It takes the place of what was typed there. The card then says "Opened in the AI Assistant. Your question was put in its message box, not sent." and its button becomes "Open the AI Assistant", which opens the drawer and puts the question in the box once more. It never sends it and leaves the drawer's conversation as it is. During a voice session the next spoken turn sends what was spoken, not the question.
- If the drawer is closed, or leaves the page, before it took the question, the button comes back. The buttons are drawn only while the main AI Assistant can be opened.

What travels is the user's question and nothing else: the tool returns no text, and nothing the panel's assistant wrote is passed on. The card is about the question, not about a run, so it works the same on a message kept from before a what-if or an undo. It proposes nothing, so an answer can carry it beside any other card. The panel under a sweep's results has it too. Where the main AI Assistant cannot be opened the page does not list the card, and the assistant only says in words where to ask.

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
