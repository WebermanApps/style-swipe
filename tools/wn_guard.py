"""WellNest no-dashboard-layout guard (Max rule, Oct 15 2026 12:45 ICT).
Other partners swipe WellNest decks, so no WellNest deck or refill may ask about dashboard LAYOUT or STRUCTURE
(sections, order, placement, card layout, shelf, header, banner, navigation, tabs, menus, columns, feed/open-item rows,
charts/progress widgets, upload/chat/projects/deck-card blocks...). Dashboard COLOUR and FONT questions are allowed.
All non-dashboard WellNest topics (brand, farm, tea, wellness, rentals, classes, voice, products, online) stay.
Used by tools/ready_shelf.py (refills/builds) and tools/build_banks.py (wellnest bank generation)."""
import re
RULE = "Max Oct 15 2026 12:45/13:04 ICT: WellNest decks carry no dashboard layout/structure questions and no deck-building questions (deck design, controls, swipe buttons, shelf, launcher, deck tags); dashboard colour and font only."
# dashboard-only surfaces: always blocked in a WellNest pair's group/category/ask
DASH = re.compile(r"\b(from the feed|latest open items|open items|deck cards?|deck progress|swipe decks|a started deck|apps and links|"
                  r"brand decisions|report dropdown|weekly report|open projects|each project|team chat|message box|unread messages|"
                  r"upload link|upload wording|upload icon|dropbox upload|older renders|render thumbnails|header render|header banner|"
                  r"shelf layout|dashboard (layout|order|sections?|structure|header|navigation|cards?))\b", re.I)
# widgets / navigation structures: always blocked (Max listed navigation explicitly)
STRUCT = re.compile(r"\b(bar chart|line chart|progress ring|progress bars?|big number|bottom tabs|top pill tabs|side menu|"
                    r"pop-out menu|swipe pages)\b", re.I)
# generic structure words: blocked only inside a dashboard deck/bank (ctx_dash=True)
GEN = re.compile(r"\b(sections?|section order|first section|header|banner|logo placement|placement|layout|order|cards?|"
                 r"columns?|carousel|density|big screen|laptop|on phone|phone crop|thumbnails?|render|frame|tap the banner|"
                 r"collapsed|dropdown|on top|top:|tiles?|stacked|side by side|list)\b", re.I)
ALLOW = re.compile(r"\b(colou?rs?|fonts?|typefaces?|serif|cormorant|dm sans|typography|text size|italic|tags? colou?r|headings?:)\b", re.I)
# deck-building surfaces (Max rule Oct 15 2026 13:04 ICT): never in a WellNest deck, colour or font included
DECKB = re.compile(r"\b(swipe decks?|style swipe|deck[- ](tags?|design|cards?|controls?|buttons?|colou?rs?|shelf|launcher|building|builder|look|page|progress|header|footer|results?)|"
                   r"swipe (buttons?|controls?|cards?)|this/that|love button|skip button|neither button|both button|notes? button|share button|submit button|"
                   r"ready shelf|deck shelf|shelf decks?|launcher|deck queue)\b", re.I)
def is_wellnest(p, topic=""):
    return "wellnest" in (topic or "").lower() or str(p.get("app", "")).lower() == "wellnest" or str(p.get("id", "")).lower().startswith(("wellnest", "bkwn"))
def head(p): return " ".join(str(p.get(k, "")) for k in ("group", "category", "ask"))
def _colour_font_only(ask):
    """An ask that is purely about colour or font (no structure words)."""
    a = re.sub(r"(?i)section titles?", "titles", ask)
    return bool(ALLOW.search(a)) and not GEN.search(a) and not STRUCT.search(a)
def blocked(p, ctx_dash=False):
    """True when a WellNest pair is about dashboard layout or structure. Pure colour/font asks are allowed."""
    h, ask = head(p), str(p.get("ask", ""))
    if DECKB.search(h): return True
    if DASH.search(h) or STRUCT.search(h): return not _colour_font_only(ask)
    if ctx_dash and GEN.search(h):
        return not (ALLOW.search(h) and not GEN.search(re.sub(r"(?i)section titles?", "titles", ask)))
    return False
def filter_pairs(pairs, topic="", ctx_dash=None):
    if ctx_dash is None: ctx_dash = "dashboard" in (topic or "").lower()
    return [p for p in pairs if not (isinstance(p, dict) and is_wellnest(p, topic) and blocked(p, ctx_dash))]
