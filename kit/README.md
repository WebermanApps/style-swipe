# Style Swipe shared kit

> Docs reconstructed Oct 16 2026 after box restore (from the kit source comments). Source of truth is the code in this folder.

Include from any board: `https://webermanapps.github.io/style-swipe/kit/<file>?v=<version>`.

| File | What |
|---|---|
| dash-theme.css | Board theme (light only, square corners) incl. section separation (cc6/cc7) |
| cc-header.js | Command Center header |
| deck-shelf.js/.css | Ready Deck Shelf (R66), data from the board's shelf.json (shelf.schema.json) |
| routines-section.js/.css | Routines section v4 (R78): compact tap-to-expand list, one row per routine (short name, short time, Active/Paused), last on the page (routines.schema.json; optional short, short_time, note) |
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

## ly1: uniform board layout (R76, Max Oct 16 2026 12:09 ICT)
```html
<link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/mw-layout.css?v=ly8">
<script src="https://webermanapps.github.io/style-swipe/kit/mw-layout.js?v=ly8" defer></script>
```
- **Branded header** (`.mw-branded-header`): `.mw-bh-cc` Command Center header, `.mw-bh-decks` deck shelf + counter, `.mw-bh-morning` Morning Report dropdown (closed by default).
- Middle content: everything else; `data-mw-slot="hero"` items go first (WellNest hero, Grok Bot Top Priorities).
- **Branded footer** (`.mw-branded-footer`): `.mw-bf-routines` Routines, then `.mw-bf-standard` standard footer (Share + Machan mark + "Built by Machan" -> maxweberman.com; kit ly5; added if missing).
- **R81 (ly6)**: `body.mw-hero-behind-header` makes `#mw-bh.mw-branded-header` background transparent with no box-shadow (opt-in; WellNest render behind the header). Other boards unaffected.
- **ly7**: stray rows under the header (`nav.topnav`, `.mw-cc-extras`, `.mw-topbar`) are emptied: Share removed (footer has it), "Updated ..." and Add To Home Screen move into `.mw-bf-extras` in the standard footer next to Share; the empty row is hidden.
- Markers override detection: `data-mw-slot="header|shelf|counter|morning|hero|routines|footer-pre|footer"`; `data-mw-keep` skips the Morning Report wrap.
- Every agent board, no exceptions (UpKeep, WellNest included). Apps Home is excluded (Max 12:11).
- ly2 (R77, Max 12:39): visible "Apps Home" button (`a.mw-apps-home`, `.mw-bh-home`) opens the branded header and links to https://webermanapps.github.io/a-o956qercs5ubd57y/. Agent boards only; never deck pages or the share page.
- ly3: removes older duplicate "Apps Home" links so only the standard button remains (opt out per link: `data-mw-keep-home`).
- ly4 (R79 STRICT, Max 13:21-13:23): branded header (#mw-bh) and branded footer (#mw-bf) are built as body-level blocks, pixel-identical on all boards (white + light beige, Khand/Hind), locked with scoped tokens, :where() resets and !important. 1px beige dividers under the header and above the footer. Routines (routines-section v5) is a dropdown, closed by default ("Routines (N)"). Agent branding lives only in the middle.
- ly4 update (Max 14:19): the middle content moves into #mw-mid, the same 1100px centered column as the branded header/footer (inner wrappers lose their narrower max-width / side padding / negative margins; full-bleed bands stay full width).

## ly8: Working On dropdown (R85, Max Oct 16 2026 23:39 ICT)
- Branded header: "Working On" dropdown directly above Morning Report, same style, closed by default, only while the board's agent is working; body is one short line (`doing`).
- Data: ONE shared file `kit/agent-status.json` (`{"as_of","agents":[{"agent","working","doing"}]}`), fetched with `cache:'no-store'` + `?t=` cache-bust, refreshed every 60s and on tab focus. Published by `/workspace/ops/agent-activity/publish_kit_status.py` (sanitized copy of agent_status.json).
- Board agent: `data-mw-agent` on any element, else `<meta name="mw-agent-name">`, else mw-chat `data-agent-name`, else `.mw-cc-header[data-cc-name]`, else the page title ("X Command Center"). Names match ignoring "Agent", case and "&".
