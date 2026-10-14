#!/usr/bin/env python3
"""Build Style Swipe deck folio-dashboard-2: Folio Dashboard Details (Oct 14 2026), 20 pairs.
Follows folio-dashboard (submission 4878114f, 19/20, 1 skip). Carried first: folio-dashboard-01 (Typography, skipped).
Builds on the picks: big title + greeting eyebrow, report first as one big card with a stripe, urgent closed as a small pill,
two-column tiles and list rows with a small corner lock, clean line chart with dashed 100/200-day lines and legend on top,
donut and category bars for spending, airy, terracotta leads, centred two columns on big monitors, centred lock.
New: Portfolio thumbnail icon variations (Max's favourite: a dollar sign with a green growth chart), drawn line icons.
Shapes only: no figures, nothing from the locked /s/ pages. Submit -> agent 'portfolio'."""
import sys, os, json, copy; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish
from draft_svg import TERRA, LAGOON, JUNGLE
from dash_kit import *
from carry_over import carried_first
DID = "folio-dashboard-2"; TOPIC = "folio-dashboard"
B = dict(name="Portfolio", bg="#FFFFFF", ink="#0A0A0A", mute="#525252", line="#E5E0D8", soft="#F5F3EF", acc=[TERRA, LAGOON, JUNGLE],
         head="Khand, sans-serif", body="Hind, sans-serif", r=8, hw=600)
pairs, O, add = deck("fd2_", "Portfolio")
def P(g, ask, a, b): add(g, g, O(*a), O(*b), ask)
base = dict(hdr="eyebig", sub="Good Morning, Max", report="banner", rc=TERRA, rname="Morning Report", urgent="pill", uc=TERRA, dens=12, tn=4)
def M(order, **k): return mock(B, order, **{**base, **k})

# ---------- Thumbnail icon: dollar sign + green growth chart, drawn line icons ----------
G2 = JUNGLE
def dollar(cx, cy, h, c, sw):
    w = h * .32
    return (f'<path d="M{cx+w} {cy-h*.28} C{cx+w*.6} {cy-h*.42} {cx-w} {cy-h*.42} {cx-w} {cy-h*.16} C{cx-w} {cy+h*.04} {cx+w} {cy-h*.02} {cx+w} {cy+h*.2} '
            f'C{cx+w} {cy+h*.44} {cx-w*.6} {cy+h*.44} {cx-w} {cy+h*.3}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="M{cx} {cy-h*.5} V{cy+h*.5}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>')
def glyph(k, c=G2, sw=5, d=100):
    """Icon drawn in a 100x100 box at origin."""
    if k == "beside":   # $ left, rising line right
        return dollar(30, 50, 56, c, sw) + f'<path d="M52 74 L64 60 L74 66 L90 40" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/><path d="M80 38 H91 V49" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    if k == "circle":   # $ in a ring with a rising line through the bottom
        return f'<circle cx="50" cy="50" r="38" fill="none" stroke="{c}" stroke-width="{sw}"/>' + dollar(50, 46, 44, c, sw) + f'<path d="M20 78 L40 70 L56 74 L82 58" fill="none" stroke="{c}" stroke-width="{sw*.8}" stroke-linecap="round" stroke-linejoin="round"/>'
    if k == "bars":     # rising bars with $ above the tallest
        return "".join(f'<rect x="{18+i*22}" y="{84-hh}" width="14" height="{hh}" rx="2" fill="none" stroke="{c}" stroke-width="{sw}"/>' for i, hh in enumerate([18, 30, 44])) + dollar(83, 30, 34, c, sw * .9) + f'<path d="M12 88 H90" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>'
    if k == "arrow":    # axis + rising arrow, $ in the corner
        return f'<path d="M16 16 V84 H88" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/><path d="M26 72 L44 54 L56 62 L82 34" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/><path d="M70 32 H84 V46" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>' + dollar(40, 30, 28, c, sw * .8)
    if k == "coin":     # coin with $ and a sprout-like growth line
        return f'<circle cx="42" cy="56" r="28" fill="none" stroke="{c}" stroke-width="{sw}"/>' + dollar(42, 56, 32, c, sw * .85) + f'<path d="M66 40 L76 30 L84 34 L94 18" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    return ""
def icon(k, cx, cy, d, style="plain", sw=5):
    sc = d / 100; x, y = cx - d / 2, cy - d / 2
    if style == "tile": bg = R(x - d * .1, y - d * .1, d * 1.2, d * 1.2, "#FFFFFF", "#E5E0D8", d * .26, 1); c = G2
    elif style == "solid": bg = R(x - d * .1, y - d * .1, d * 1.2, d * 1.2, G2, "none", d * .26); c = "#FFFFFF"
    elif style == "tint": bg = R(x - d * .1, y - d * .1, d * 1.2, d * 1.2, G2 + "1A", "none", d * .26); c = G2
    else: bg = ""; c = G2
    return bg + f'<g transform="translate({x:.1f},{y:.1f}) scale({sc:.3f})">{glyph(k, c, sw)}</g>'
def thumb(k, style="tile", sw=5, cap=""):
    s = icon(k, 120, 92, 110, style, sw) + T(B, 120, 186, "Portfolio", 18, None, True, a="middle") + T(B, 120, 200, cap, 7, B["mute"], a="middle")
    s += L(24, 214, 216, 214, B["line"]) + T(B, 24, 230, "SMALL SIZES", 6, B["mute"], w=600, ex='letter-spacing="1.2"')
    for i, d in enumerate([40, 28, 18, 12]): s += icon(k, 46 + i * 50, 262, d, style, sw)
    return screen(s, "#FFFFFF")
def small(k, style, sw=5):
    s = T(B, 120, 26, "At Small Sizes", 14, None, True, a="middle")
    s += R(14, 40, 212, 46, "#FFFFFF", B["line"], 10) + icon(k, 36, 63, 24, style, sw) + T(B, 58, 60, "Portfolio", 10, None, True) + R(58, 66, 120, 3, B["mute"] + "55", r=1.5)
    s += R(14, 94, 212, 70, "#FFFFFF", B["line"], 10) + "".join(icon(k, 46 + i * 50, 122, 26, style, sw) if i == 1 else R(29 + i * 50, 105, 34, 34, "#EEEBE5", r=8) for i in range(4)) + T(B, 120, 156, "Home screen", 6.5, B["mute"], a="middle")
    s += R(14, 172, 212, 34, "#FFFFFF", B["line"], 10) + icon(k, 30, 189, 13, style, sw) + T(B, 44, 192, "Browser tab, 16 px", 7.5, B["ink"])
    s += R(14, 214, 212, 34, "#FFFFFF", B["line"], 10) + icon(k, 30, 231, 16, style, sw) + R(44, 226, 100, 3, B["ink"] + "44", r=1.5) + R(44, 233, 70, 3, B["mute"] + "44", r=1.5)
    return screen(s, "#FFFFFF")
G = "Portfolio Thumbnail"
P(G, "Thumbnail: Dollar Beside A Growth Line Or Dollar In A Ring?",
  ("th_beside", "Dollar Beside A Growth Line", "Dollar sign left, green line rising right.", "focused", thumb("beside", cap="Line icon on a white tile")),
  ("th_circle", "Dollar In A Ring", "Dollar in a circle, growth line along the base.", "calm", thumb("circle", cap="Line icon on a white tile")))
P(G, "Thumbnail: Rising Bars Or Chart With An Arrow?",
  ("th_bars", "Rising Bars With A Dollar", "Three bars, dollar over the tallest.", "visual", thumb("bars", cap="Line icon on a white tile")),
  ("th_arrow", "Chart Axis With A Rising Arrow", "Axis, arrow up, small dollar.", "action", thumb("arrow", cap="Line icon on a white tile")))
P(G, "Thumbnail: Dollar Coin With Growth Or Dollar Beside A Line?",
  ("th_coin", "Coin With A Growth Line", "A dollar coin, line climbing off it.", "visual", thumb("coin", cap="Line icon on a white tile")),
  ("th_beside_b", "Dollar Beside A Growth Line", "Same as before, for a direct match.", "focused", thumb("beside", cap="Line icon on a white tile")))
P(G, "Thumbnail Colour: Green Line On White Or White On Green?",
  ("th_onwhite", "Green Line On White", "Green strokes, white tile, thin border.", "calm", thumb("beside", "tile", cap="Green on white")),
  ("th_ongreen", "White Line On Green", "White strokes on a jungle green tile.", "visual", thumb("beside", "solid", cap="White on green")))
P(G, "Thumbnail Stroke: Fine Or Bold?",
  ("th_fine", "Fine Stroke", "Light line, more detail.", "calm", small("beside", "tint", 3.5)),
  ("th_bold", "Bold Stroke", "Thick line, reads at tab size.", "focused", small("beside", "tint", 7)))

# ---------- Deeper on what the picks settled ----------
P("Header", "Greeting Eyebrow: Terracotta Or Quiet Grey?",
  ("hd_eterra", "Terracotta Greeting", "Greeting in terracotta, title below.", "visual", M(["hdr", "report", "urgent", "tiles"], tiles="row", locked="icon")),
  ("hd_egrey", "Grey Greeting", "Greeting in grey, terracotta only on the rule.", "calm", M(["hdr", "report", "urgent", "tiles"], ec="#525252", tiles="row", locked="icon")))
P("Morning And Evening Report", "Report Card: Bullet Points Or Short Paragraph?",
  ("rp_bul", "Bullet Points", "A few dotted lines with Show More.", "quick", M(["hdr", "report", "urgent"], report="more", rn=4)),
  ("rp_par", "Short Paragraph", "A big card with a few lines of text.", "calm", M(["hdr", "report", "urgent"], report="big", rc=TERRA)))
P("Morning And Evening Report", "Report Stripe: Terracotta Or Lagoon?",
  ("rp_sterra", "Terracotta Stripe", "Matches the lead colour.", "visual", M(["hdr", "report", "urgent", "tiles"], tiles="row", locked="icon")),
  ("rp_slagoon", "Lagoon Stripe", "Report in lagoon, terracotta saved for urgent.", "calm", M(["hdr", "report", "urgent", "tiles"], rc=LAGOON, tiles="row", locked="icon")))
P("Urgent Items Pill", "Urgent Pill: Count Bubble Or Tinted Text?",
  ("ur_count", "Count In A Bubble", "Terracotta bubble, plain label.", "focused", M(["hdr", "urgent", "report", "tiles"], urgent="pillcount")),
  ("ur_tint", "Tinted Pill", "Soft terracotta pill with the count in the words.", "calm", M(["hdr", "urgent", "report", "tiles"])))
P("Urgent Items Pill", "Urgent Pill: Under The Header Or Under The Report?",
  ("ur_top", "Under The Header", "Seen before the report.", "action", M(["hdr", "urgent", "report", "tiles"], urgent="pillcount")),
  ("ur_after", "Under The Report", "Report first, then the pill.", "calm", M(["hdr", "report", "urgent", "tiles"], urgent="pillcount")))
P("Tiles And Unlock", "Tiles: Two Columns Or List Rows?",
  ("tl_two", "Two Columns, Small Lock", "Outlined tiles, lock in the corner.", "visual", M(["hdr", "report", "tiles"], tn=6, locked="icon")),
  ("tl_rows", "List Rows, Small Lock", "One row per area, lock before the chevron.", "quick", M(["hdr", "report", "tiles"], tn=6, tiles="row", locked="icon")))
P("Portfolio Chart", "Average Lines: Terracotta And Green Or Lagoon And Grey?",
  ("ch_tg", "Terracotta And Green", "Dashed 100-day terracotta, 200-day green.", "visual", M(["hdr", "chart", "tiles"], ch=140, tn=2)),
  ("ch_lg", "Lagoon And Grey", "Price line ink, averages lagoon and grey.", "calm", M(["hdr", "chart", "tiles"], ch=140, tn=2, cc="#0A0A0A", smac=(LAGOON, "#9A948A"))))
P("Portfolio Chart", "Chart Line: Fine Or Medium?",
  ("ch_fine", "Fine Line", "Thin price line.", "calm", M(["hdr", "chart", "spend"], ch=130, seed=4, lw=1.2, spend="donut")),
  ("ch_med", "Medium Line", "Heavier price line, easier at a glance.", "focused", M(["hdr", "chart", "spend"], ch=130, seed=4, lw=2.6, spend="donut")))
P("Spending Chart", "Spending: Donut Or Category Bars First?",
  ("sp_donut", "Donut First", "Donut, then bars below on tap.", "visual", M(["hdr", "spend", "tiles"], spend="donut", sh=110)),
  ("sp_bars", "Category Bars First", "Bars, donut on tap.", "focused", M(["hdr", "spend", "tiles"], spend="hbars", sh=100)))
P("Spending Chart", "Donut: Thin Ring Or Thick Ring?",
  ("sp_thin", "Thin Ring", "Light, airy ring.", "calm", M(["hdr", "spend", "report"], spend="donut", sh=110, dw=5)),
  ("sp_thick", "Thick Ring", "Bold slices.", "visual", M(["hdr", "spend", "report"], spend="donut", sh=110, dw=14)))
P("Big Monitor", "Centred Two Columns: Report Left Or Charts Left?",
  ("bm_rep", "Report Left", "Report, urgent and tiles left; charts right.", "focused", desk(B, [["hdr", "report", "urgent", "tiles"], ["chart", "spend"]], note="Centred, wide margins", **{**base, "spend": "donut"})),
  ("bm_ch", "Charts Left", "Charts left; report and tiles right.", "visual", desk(B, [["hdr", "chart", "spend"], ["report", "urgent", "tiles"]], note="Centred, wide margins", **{**base, "spend": "donut"})))
P("Unlock Screen", "Centred Lock: Plain Lock Or Lock In A Tinted Circle?",
  ("ul_plain", "Plain Lock", "As picked: lock, line, password, button.", "calm", mock(B, ["unlock"], y0=30)),
  ("ul_circle", "Lock In A Soft Circle", "Terracotta tint circle behind the lock.", "visual", screen(f'<circle cx="120" cy="78" r="26" fill="{TERRA}1A"/>' + stack(B, ["unlock"], {}, 30)[0], "#FFFFFF")))

def withthumb(on):
    g, _ = stack(B, ["hdr", "report", "urgent", "tiles"], {**base, "tiles": "row", "locked": "icon"}, 10)
    if on: g = icon("beside", 206, 38, 22, "tint", 6) + g
    return screen(g, "#FFFFFF")
P("Header", "Header: Thumbnail Beside The Title Or No Icon?",
  ("hd_thumb", "Thumbnail Beside The Title", "Small green icon at the top right.", "visual", withthumb(True)),
  ("hd_nothumb", "No Icon", "Greeting and title only.", "calm", withthumb(False)))
P("Morning And Evening Report", "More Detail: Show More Link Or Fold Row?",
  ("rp_link", "Show More Link", "Underlined link under the points.", "quick", M(["hdr", "report", "urgent", "tiles"], report="more", rn=3)),
  ("rp_fold", "Fold Row With Chevron", "A ruled row that opens the rest.", "calm", M(["hdr", "report", "urgent", "tiles"], report="more", rn=3, more="fold")))
# carried first, option ids renamed so they count as fresh
carried = carried_first(TOPIC, [], clear=False)
for p in carried:
    p.pop("id", None)
    for s in "AB": p["option" + s]["id"] = "fd2_rt_" + p["option" + s]["id"].split("_", 1)[1]
    p["purpose"] = "retest"; p["retest"] = True; p["notes"] = True; p["share"] = True
pairs[:0] = carried
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish(DID, "Folio Dashboard Details", "Portfolio", pairs,
        {"brands": ["Folio Dashboard Details: carried Typography pair first, Portfolio thumbnail icons (dollar sign with a green growth chart), then deeper on the picked header, report, urgent pill, tiles, chart, spending, big monitor and unlock",
                    "White cards on a light cream page, Khand/Hind, terracotta leads with lagoon and jungle green; drawn shapes only, no figures"],
         "submit_agent": "portfolio", "submit_to": "Portfolio Agent", "section_counts": cnt, "deck_size": N, "carried": len(carried),
         "follows": {"deck": "folio-dashboard", "submission": "4878114f-c4c1-437f-9cb4-a657860e84bf", "answered": 19, "total": 20},
         "sources": {"results": "/workspace/style-swipe/results/folio-dashboard.txt", "dashboard": "https://webermanapps.github.io/portfolio-dashboard/"}},
        seed=1018, n=N, first=len(carried))
carried_first(TOPIC, [], clear=True)
