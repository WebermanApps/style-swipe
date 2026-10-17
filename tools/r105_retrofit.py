#!/usr/bin/env python3
"""R105 caption retrofit (Max Oct 17 2026 19:46 ICT; Branding). Rewrites each failing pick 'ask' of an UNFINISHED deck to
'<Screen/App>: <Element>, <one plain sentence>' in place: same deck id, same pick order, option ids untouched (Max's votes kept).
The old text is kept in pick['ask_old']. Deck pages load decks/<id>.json at runtime (pages with an embedded copy are re-embedded
separately by the caller). usage: r105_retrofit.py [--write] deck_id [deck_id...]"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import caption_rule as cr
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = re.compile(r"\b(cards?|rows?|headlines?|accent|corners|charts?|buttons?|grid|box|sheet|dropdowns?|tabs?|ring|picture|lines|title|caps|steps|sections|roomy|compact|badge|icons?|banner|strip|font|layout|chips?|list|tiles?|pill|outline|band|header|menu)\b", re.I)
SCREEN = {"Home Guide": "Home Guide App", "Mom's Amex Offers": "Mom's Amex Offers App", "Miles Agent": "Miles Board", "Miles": "Miles Board",
  "Style Swipe": "Deck Page", "Thai Study": "Thai Study App", "Blueprint": "Blueprint Board", "Portfolio": "Portfolio Board", "Prop": "Prop Board",
  "Blog": "Blog Board", "Branding": "Deck Building Page", "UpKeep": "UpKeep Board", "Coach": "Coach Board", "Smart Upkeep": "Smart Upkeep App",
  "Ready To Swipe Finishing Deck": "Ready To Swipe Shelf", "Grok Bot": "Grok Bot Board", "Security": "Security Board", "Dump": "Dump Board",
  "Household": "Household Board", "Jokes": "Jokes Board", "Video & Photo": "Video & Photo Board", "Research": "Research Board", "Grok Bot Team": "Team Improvement Deck"}
GROUP_SCREEN = {"Grok Bot (Apps Home)": "Apps Home", "Portfolio": "Portfolio Board", "Deck Building": "Deck Building Page", "Grok Bot": "Grok Bot Board",
  "Security": "Security Board", "Construction": "Construction Board", "Legal": "Legal Board", "Research": "Research Board", "UpKeep": "UpKeep Board",
  "WellNest": "WellNest Board", "Household": "Household Board", "Miles": "Miles Board", "Blog": "Blog Board", "Thai": "Thai Study App", "Jokes": "Jokes Board"}
UPKEEP = {"Investor Pitch": "UpKeep Investor Deck", "Customer Profile": "UpKeep Member Profile", "Clear Picks": "UpKeep Member App",
  "Sign Up Form": "UpKeep Sign-Up Form", "Phone Home Top Section": "UpKeep Phone Home Page", "Technician Page": "UpKeep Tech App",
  "Trust Tags": "UpKeep Home Page", "Video Hooks": "UpKeep Promo Video", "Pricing": "Smart Upkeep Pricing Page", "Pause Plan": "Smart Upkeep Pause Plan Screen",
  "Pause Plan Screens": "Smart Upkeep Pause Plan Screen", "Visit Summary Screens": "Smart Upkeep Visit Summary", "Warranty & Form Warnings": "Smart Upkeep Warranty Screen",
  "UpKeep Board Details": "UpKeep Board"}
DECK_LOC = {"new-ideas-wellnest-upkeep-ai-coding-vcllwx": "Research New Ideas Deck", "team-improvement-deck-round-three": "Team Improvement Deck",
  "questions-center-two": "Grok Bot Questions Center", "checkout-selling-checkout-and-selling-billing-risk": "Smart Upkeep Checkout",
  "checkout-selling-checkout-and-selling-offer-go-to-market": "Smart Upkeep Checkout", "deck-board-2": "Deck Building Page",
  "dashboard-layout-dashboard-layout-deck": "Coach Board", "miles-ready-1": "Miles Board", "prop-dashboard-dashboard-deck": "Prop Board",
  "miles-1": "Miles Board", "jane-amex-2": "Mom's Amex Offers App"}
PREFIX_LOC = {"SmartKeep Video": "SmartKeep Video", "Social Clips": "Social Clips", "Video Style": "Video & Photo Style Guide", "WellNest Photo": "WellNest Photo Set"}
KEEP = {"I", "I'm", "I'll", "I've", "I'd", "OK", "TV", "AI", "PDF", "CPA", "EUR", "USD", "THB", "2FA", "ICT", "URL", "SMS", "ID", "FAQ", "Q4", "UpKeep", "WellNest", "SmartKeep"}
PROPER = {"Max", "Thomas", "Maple", "Niko", "Vivian", "Jane", "Mom", "Mom's", "Ethan", "Agnes", "Nozomi", "Grok", "Tally", "Amex", "Google", "Apple",
  "Dropbox", "GitHub", "Slack", "Gmail", "Kraken", "Tesla", "Instagram", "TikTok", "YouTube", "Facebook", "Stripe", "Thai", "Thailand", "Japan", "Japanese",
  "Bangkok", "Roselle", "PowerHaus", "Vanni", "Khand", "Hind", "Machan", "Branding", "Coach", "Blueprint", "Miles", "Prop", "Portfolio", "Dump", "Scout",
  "Legal", "Research", "Security", "Construction", "Household", "Akiya", "Michigan", "Wickfield", "Clinton", "Sal", "Brett", "Church", "Claude", "Monet",
  "Asia", "Europe", "America", "American", "Mandon", "Jakarta", "Bali", "Tokyo", "Kyoto", "Osaka", "Hokkaido", "Seoul", "Singapore", "Vietnam", "Laos",
  "Cambodia", "Taiwan", "Korea", "Hanoi", "Mekong", "Phuket", "Krabi", "Samui", "Hua", "Hin", "Pai", "Lampang", "Nan", "Sukhothai", "Ayutthaya",
  "Mondays", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "January", "February", "March", "April", "June", "July",
  "August", "September", "October", "November", "December", "Christmas", "English", "Expo", "Notion", "Canva", "Figma", "Shopify", "Etsy", "Amazon",
  "Lazada", "Shopee", "Grab", "LINE", "WhatsApp", "Telegram", "Venmo", "PayPal", "Chase", "Sapphire", "Hilton", "Marriott", "Hyatt", "Delta", "United",
  "Emirates", "Qatar", "Turo", "Airbnb", "Agoda", "Zillow", "Redfin", "QuickBooks", "TurboTax", "Fidelity", "Vanguard", "Schwab", "Coinbase"}
COMMON = set()
def learn_proper():
    import glob
    for f in glob.glob(os.path.join(ROOT, "decks", "*.json")):
        try: d = json.load(open(f, encoding="utf-8"))
        except Exception: continue
        txt = []
        for p in d.get("pairs") or d.get("cards") or []:
            txt.append(p.get("ask") or "")
            for k in ("optionA", "optionB", "option"):
                o = p.get(k) or {}
                if isinstance(o, dict): txt.append(o.get("desc") or "")
        for m in re.finditer(r"(?<![A-Za-z\-])([a-z][a-z'’]+)(?![A-Za-z\-])", " ".join(txt)): COMMON.add(m.group(1))
PHRASES = ["Apps Home", "Ready To Swipe", "Smart Upkeep", "Grok Bot", "Tally Pro", "Hidden Valley", "Mellow Wood", "Questions Center", "Deck Building",
           "Morning Report", "Document Center", "Max's Picks", "Team Improvement Deck", "Chiang Mai", "Khao Yai", "Doi Ang Khang", "Koh Kood", "Buds Station", "Mae Hong Son", "Chiang Rai", "Hua Hin", "Koh Samui", "Koh Lanta", "Koh Chang", "Mount Fuji", "New York", "Hong Kong", "Kuala Lumpur", "Ho Chi Minh", "Luang Prabang", "Siem Reap"]
def decap(s):
    keep = {}
    for i, ph in enumerate(PHRASES):
        if ph in s: tok = f"\x00{i}\x00"; keep[tok] = ph; s = s.replace(ph, tok)
    def w(m):
        x = m.group(0)
        if x in KEEP or x in PROPER or (len(x) > 1 and x.isupper()) or re.search(r"\d", x) or re.search(r"[a-z][A-Z]", x): return x
        lo = x[0].lower() + x[1:]
        if x == "A": return "a"
        return lo if (x[:1].isupper() and lo.lower() in COMMON) else x
    s = re.sub(r"[A-Za-z][A-Za-z'’]*", w, s)
    for t, ph in keep.items(): s = s.replace(t, ph)
    return s
def clean_el(x):
    x = re.sub(r"\s+", " ", x.replace(":", " ").replace(",", " ")).strip(" ?.-")
    return x[:58].rsplit(" ", 1)[0] if len(x) > 58 else x
def deck_loc(did, d, p):
    app = p.get("app") or d.get("app") or ""
    title = d.get("title") or ""
    pre = title.split(":")[0].strip() if ":" in title else re.sub(r"\s*Deck( Two)?$", "", title).strip()
    if did in DECK_LOC: return DECK_LOC[did], pre
    for k, v in PREFIX_LOC.items():
        if title.startswith(k): return v, pre
    if app == "Agent Dashboards Deck Two": return GROUP_SCREEN.get(p.get("group") or "", (p.get("group") or "Agent").split(" (")[0] + " Board"), pre
    if app in ("UpKeep", "Smart Upkeep") or "upkeep" in did:
        for k, v in UPKEEP.items():
            if pre.startswith(k) or title.startswith(k): return v, pre
        return ("Smart Upkeep App" if app == "Smart Upkeep" else "UpKeep Board"), pre
    return None, pre
def caption(did, d, p):
    ask = (p.get("ask") or "").strip()
    A = (p.get("optionA") or {}).get("label") or ""; Bl = (p.get("optionB") or {}).get("label") or ""
    loc, pre = deck_loc(did, d, p)
    ui = bool(UI.search(A + " " + Bl))
    app = p.get("app") or d.get("app") or ""
    if not loc:
        if ui: loc = SCREEN.get(app, (app or "Deck") + " Board")
        else:
            base = app if app not in ("Grok Bot Team",) else "Grok Bot Team"
            loc = pre if (base and base.split()[0].lower() in pre.lower()) else (f"{base} {pre}".strip() if pre else SCREEN.get(app, app + " Board"))
            if pre.lower() in ("dashboard", "from the feed", "decisions", "topics", "library", "sets", "progress", "quiz"): loc = SCREEN.get(app, app + " Board")
    loc = re.sub(r"[:,?]", "", loc).strip()[:48]
    if ":" in ask and 2 <= len(ask.split(":")[0].strip()) <= 60 and "," not in ask.split(":")[0]:
        el, rem = ask.split(":", 1); el = clean_el(el); rem = rem.strip()
    elif len(ask) < 30 and A and Bl and not re.search(r"\bor\b", ask, re.I):
        el = clean_el(ask); rem = f"{A} Or {Bl}, which one fits best?"
    else:
        el = clean_el(p.get("category") or p.get("group") or "Choice"); rem = ask
    if (not el or el.lower() == loc.lower() or el.lower() in loc.lower() or el.lower() == (p.get("group") or "").lower() == (p.get("category") or "").lower()) and rem and len(rem) < 45 and A and Bl and not re.search(r"\bor\b", rem, re.I):
        el = clean_el(rem); rem = f"{A} Or {Bl}, which one fits best?"
    if el.lower() == loc.lower() or not el: el = clean_el(p.get("category") or p.get("group") or "Choice")
    if el.lower() == loc.lower(): el = "Choice"
    m = re.match(r"^(.+?) or (.+?)\?$", rem, re.I)
    if ui and m and len(rem) < 90 and len(el) <= 28:
        s = f"{decap(m.group(1))} or {decap(m.group(2))} for the {decap(el)}?"
    else:
        s = decap(rem)
        w0 = re.match(r"[A-Za-z'’]+", s); w0 = w0.group(0) if w0 else ""
        if s[:1].isupper() and w0 not in KEEP and w0 not in PROPER and w0.lower() in COMMON and not any(s.startswith(ph) for ph in PHRASES): s = s[0].lower() + s[1:]
    if len(s) < 12 and A and Bl: s = f"{decap(A)} or {decap(Bl)}, which one fits best?"
    s = re.sub(r"\s+", " ", s).strip()
    # one sentence: '. ' / '! ' / '? ' inside -> join with a dash
    s = re.sub(r"([.!?])\s+(?=\S)", lambda m: ("; " if m.group(1) == "." else " - " if m.group(1) == "!" else ", "), s.rstrip()) if re.search(r"[.!?]\s+\S", s) else s
    if not re.search(r"[.?!]$", s): s += "."
    e2 = decap(el); el = (e2[:1].upper() + e2[1:]) if e2 else el
    return f"{loc}: {el}, {s}"
def main():
    write = "--write" in sys.argv; ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    learn_proper(); changed = {}
    for did in ids:
        f = os.path.join(ROOT, "decks", did + ".json"); d = json.load(open(f)); prs = d.get("pairs") or d.get("cards") or []
        n = 0
        for i, p in enumerate(prs, 1):
            if not cr.check(p.get("ask", "")): continue
            new = caption(did, d, p); bad = cr.check(new)
            if bad: print("STILL BAD", did, i, new, bad); continue
            if write: p.setdefault("ask_old", p.get("ask", "")); p["ask"] = new
            print(f"{did} #{i}: {new}"); n += 1
        if write and n:
            d["r105"] = "retrofit Oct 17 2026 (Branding): captions only; ids and pick order unchanged"
            json.dump(d, open(f, "w"), indent=1, ensure_ascii=False); open(f, "a").write("\n")
        changed[did] = n
    print(json.dumps(changed))
if __name__ == "__main__": main()
