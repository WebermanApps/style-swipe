# Style Swipe

Daily A/B taste test for Max Weberman's personal brand.

- Open `index.html` (works offline from file://; today's deck and images are embedded).
- Swipe or tap left/right, or use Neither / Skip / Undo (keys: ← → ↓ S Z).
- At the end: Export JSON, Copy JSON, or Share. Progress auto-saves in localStorage per deck date.

Live: https://webermanapps.github.io/style-swipe/ (older decks: add `?date=<deck id>`, e.g. `?date=2026-10-12`).

Daily loop:
    python3 generate_deck.py --ingest ~/Downloads/style-swipe-results-2026-10-09.json --date 2026-10-10
This updates `profile.json`, writes `decks/2026-10-10.json`, and re-renders `index.html` with that deck embedded.
`index.template.html` is the HTML source; `fetch_images.py` re-downloads the Wikimedia Commons images (credits in `img/credits.json`).

Freshness:
- Every deck uses only options that have never appeared in any earlier deck. `shown_options.json` is the
  ledger (option id -> dates shown); it is updated automatically each time a deck is generated.
- Each option appears at most once per deck. When the unseen pool runs low the generator warns and makes a
  shorter deck (or use `--allow-repeats`). Extend `POOL_EXTRA` in `generate_deck.py` to add runway.

Focus and deck ids:
- `--focus "Cat A,Cat B"` boosts those categories x3 so most pairs match what Max is working on now; `--focus-note` saves why. Add each day's work-specific options as a new `POOL_<date>` block in `generate_deck.py`.
- Without `--date`, the deck id is today's date, or the next free suffix (`2026-10-10b`, `c`, ...) if today's id is taken.

## Ready Deck Shelf (R66, Oct 14 2026)
Every agent dashboard shows 3-5 already-built 20-card decks at the top (`kit/deck-shelf.js` + `.css`, data in the agent's `shelf.json`, schema `kit/shelf.schema.json`). No request launcher (`kit/deck-launcher.js` is retired and now just loads the shelf for old pages).
Build a deck onto a shelf: `python3 tools/ready_shelf.py build <bank-topic> --shelf /path/to/shelf.json --agent <agent>`
Refill after a submission is handled (Style Swipe Submissions routine, after saving results and `carry_over.py record`):
`python3 tools/ready_shelf.py refill <deck_id> --shelf /workspace/branding-dashboard/shelf.json --agent branding`
then commit + push style-swipe and the dashboard repo. Skips come first, reworded when the carry note has a rewording; a pair skipped twice is dropped (R64).

## Shared ledgers (many agents commit here)
`banks/used.json`, `banks/index.json`, `decks/pages.json`, `decks/sizes.json` and `shown_options.json` are shared by every agent.
1. `git pull --rebase --autostash` BEFORE building a deck (so the ledgers you write on top of are current).
2. Build/publish, then `git pull --rebase --autostash` again and commit the ledgers TOGETHER WITH your own deck files in one commit (`git add` named paths only, never `git add -A`).
3. On a ledger conflict, merge both sides (they are JSON maps/lists: keep every entry), then `python3 tools/write_sizes.py` to regenerate sizes.json. Never `reset --hard`, never drop another agent's entries, never commit another agent's untracked deck files.
4. Deck pages: header Deck Building and Back to Deck Building follow `submit_agent` via `kit/agent-dashboards.json`; after adding pages run `python3 tools/agent_links.py`.

## Deck cap (Max, Oct 14 2026 19:43 ICT)
No agent dashboard shows more than 5 decks, ready-shelf AND pinned unfinished together. Only exception: the Deck Building page (branding /decks/).
`kit/deck-shelf.js` enforces it: pinned unfinished decks (`shelf.json` `pinned`/`unfinished`, or `DeckShelf.render(el, json, {pinned:[...]})`) go first, then ready decks, cut at 5; the rest are queued (`DeckShelf.queued(el)`) and show only when a slot opens. Do not render a separate pinned/unfinished strip next to the shelf; pass it in so the cap counts it. Deck Building page only: `data-shelf-nocap`.

## Custom shelves: deck-queue.json optional fields (Oct 14 2026 20:04 ICT)
Agents with their own carousel (e.g. WellNest `deck-queue.json`) may add per deck:
- `answered` (int): cards answered so far; > 0 shows Continue and moves the deck first.
- `added` (ISO time the deck was built): orders the rest newest first.
Same meaning as `answered` / `added` in kit `shelf.json`. Fill from ops/submit/inbox/<agent> submissions and queue/carry_over.json.
