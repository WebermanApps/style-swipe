"""R105 card caption rule (Max, Oct 17 2026 19:46 ICT): every pick's question starts with a location label, then the element,
then ONE plain sentence:  "<Screen/App>: <Element>, <one sentence>"
  e.g. "Member Profile: Problem photo, how the photo of the reported problem shows at the top of the member's profile."
The label names the exact app/screen (UpKeep Member App, UpKeep Tech App, Operator Console, Branding Board, Deck Page ...),
never a vague word like "Dashboard" or "App" on its own.
  check(ask) -> list of problems ([] = ok);  guard(pairs) raises ValueError on the first bad pick (builders call it).
  python3 tools/caption_rule.py decks/<id>.json ...   (report)"""
import re, sys, json
VAGUE = {"dashboard", "app", "screen", "page", "board", "deck", "main", "main dashboard", "the app", "home", "site", "website",
         "tool", "view", "section", "card", "ui", "layout", "design", "this", "that", "it", "misc", "general", "other"}
RX = re.compile(r"^(?P<loc>[A-Z0-9][^:,?]{1,48}?): (?P<el>[^,:]{2,60}?), (?P<s>.+)$")
def check(ask):
    a = (ask or "").strip(); m = RX.match(a); out = []
    if not m: return ["missing '<Screen/App>: <Element>, <one sentence>' format"]
    loc = m.group("loc").strip()
    if loc.lower() in VAGUE: out.append(f"vague location label '{loc}'")
    s = m.group("s").strip()
    if len(re.findall(r"[.!?](\s|$)", s.rstrip(".?!") + " ")) > 0: out.append("more than one sentence")
    if len(s) < 12: out.append("sentence too short")
    return out
def guard(pairs, did=""):
    for i, p in enumerate(pairs, 1):
        q = p.get("ask") or (p.get("option") or {}).get("ask") or ""
        bad = check(q)
        if bad: raise ValueError(f"R105 caption rule: {did} pick {i} '{q}': " + "; ".join(bad))
    return True
if __name__ == "__main__":
    rc = 0
    for f in sys.argv[1:]:
        d = json.load(open(f))
        for i, p in enumerate(d.get("pairs") or d.get("cards") or [], 1):
            b = check(p.get("ask", ""))
            if b: rc = 1; print(f"{f} #{i}: {p.get('ask','')!r}: {'; '.join(b)}")
    sys.exit(rc)
