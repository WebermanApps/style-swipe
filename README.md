# Style Swipe

Daily A/B taste test for Max Weberman's personal brand.

- Open `index.html` (works offline from file://; today's deck and images are embedded).
- Swipe or tap left/right, or use Neither / Skip / Undo (keys: ← → ↓ S Z).
- At the end: Export JSON, Copy JSON, or Share. Progress auto-saves in localStorage per deck date.

Daily loop:
    python3 generate_deck.py --ingest ~/Downloads/style-swipe-results-2026-10-09.json --date 2026-10-10
This updates `profile.json`, writes `decks/2026-10-10.json`, and re-renders `index.html` with that deck embedded.
`index.template.html` is the HTML source; `fetch_images.py` re-downloads the Wikimedia Commons images (credits in `img/credits.json`).
