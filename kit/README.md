# Style Swipe shared kit

> Docs reconstructed Oct 16 2026 after box restore (from the kit source comments). Source of truth is the code in this folder.

Include from any board: `https://webermanapps.github.io/style-swipe/kit/<file>?v=<version>`.

| File | What |
|---|---|
| dash-theme.css | Board theme (light only, square corners) incl. section separation (cc6/cc7) |
| cc-header.js | Command Center header |
| deck-shelf.js/.css | Ready Deck Shelf (R66), data from the board's shelf.json (shelf.schema.json) |
| routines-section.js/.css | Routines section, last on the page (routines.schema.json) |
| mw-chat.js/.css | Pop-up chat button (R74, cc8-cc11) |
| agent-dashboards.json | submit_agent -> board URL/name for deck page links |
| deck-counts.json, swipe-stats.json | Deck counter data (R72: show 0 when no stats) |
| deck-launcher.* | Retired; only loads the shelf for old pages |

## cc6 / cc7: section separation (R71)
- `<main class="mw-sections">` (children are sections) or `<section class="mw-section">`.
- `.mw-section--plain`: spacing only, no hairline. `.mw-section--band`: full-width soft band.
- Vars: `--mw-divider` (#e3ddd2), `--mw-band` (#FAF6EE), `--mw-section-gap` (56px; 40px under 600px). Brands override on :root/wrapper.
- No hairline right after `.mw-cc-header`; `.mw-footer` keeps its own top rule.
- cc7: after the deck shelf (`.ds-sec`) the next section sits 32px below (24px on phone).

## cc8-cc11: mw-chat (R74)
```html
<script src="https://webermanapps.github.io/style-swipe/kit/mw-chat.js?v=cc11" data-agent-id="<uuid>" data-agent-name="Coach Agent" defer></script>
```
Or `<meta name="mw-agent-id">` (+ `mw-agent-name`), `data-agent="<slug>"` (registry in mw-chat.js), or `MWChat.mount({agent:'<slug>'})`.
- cc8: bottom-corner light 44px button, drawn SVG icon; opens `grokbot://app/v1/agent?id=<id>`; fallback note if the app does not open. Deck template + deck pages; share page excluded; Niko's customer apps excluded.
- cc9: hides while a row arrow (`.arr`, `[data-mw-chat-hide]`) is under it (Apps Home); more agent ids.
- cc10: lifts above fixed footers/bars in app layouts.
- cc11: also lifts above fixed tab bars and tap targets.
- Avoids `#share, .shic, .mw-share, footer, .mw-footer, #routines, .mw-sec-routines, [data-routines], [data-mw-chat-avoid]`.
