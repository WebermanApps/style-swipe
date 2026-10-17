"""Auto-refill generator for the New Ideas bank (used by new_ideas.py when unshown ideas drop under 20).
Project x direction matrix: each of Max's real projects meets each direction pair once. Directions are plain choices
(how to reach people, who to serve, how to sell), so there are no facts or numbers to get wrong.
Rows use the compact format of new_ideas_more.py. Add projects or directions here to extend the runway."""
PROJECTS = [("Smart Upkeep", "Upkeep", "spinoff"), ("WellNest", "WellNest", "spinoff"), ("Style Swipe", "Swipe", "spinoff"),
            ("Thai Study", "Thai", "spinoff"), ("@AMomentInThai", "Channel", "spinoff"), ("Japan Cottage", "Cottage", "spinoff"),
            ("Weberman Construction", "Weberman", "spinoff"), ("Property Management", "Rentals", "spinoff"),
            ("Amex Offers App", "Offers", "spinoff"), ("Japan House Crew", "House Crew", "spinoff"), ("Site Walk", "Site Walk", "spinoff"),
            ("Agents", "Agent", "spinoff")]
DIRS = [
 ("reach", "How should {t} reach people?", "{p} Letter|A short monthly letter|list|This month:News;Next:Plans",
  "{p} Clips|Quick clips of the work|photo|Watch a clip;room"),
 ("form", "Which {t} format?", "{p} App|Everything in one app|tiles|Home;List;Notes;Help",
  "{p} Print Kit|Printed guide and cards|photo|Printed kit;house"),
 ("who", "Who should {t} serve next?", "{p} For Families|Made for households|photo|For families;person",
  "{p} For Business|Made for small firms|photo|For business;house"),
 ("pay", "How should {t} charge?", "{p} Monthly|A simple monthly plan|word|Monthly;plan",
  "{p} Pay Once|One clear price|word|Once;one price"),
 ("teach", "How could {t} teach others?", "{p} Workshop|Teach it in person|photo|Workshop;person",
  "{p} Course|Teach it online|steps|Lesson;Practice;Done"),
 ("place", "Where should {t} show up?", "{p} Pop-Up|One day in person|photo|Pop-up day;room",
  "{p} Web Shop|Order on a simple page|list|Item A:Add;Item B:Add"),
 ("team", "How should {t} grow?", "{p} Partner|Team up with a local brand|list|Partner:Talk;Plan:Draft",
  "{p} Solo|Prove it alone first|checks|Test;Learn;Repeat"),
 ("help", "What runs {t} busywork?", "{p} Agent|An agent does the busywork|chat|What's due?;Two tasks today",
  "{p} Checklist|A simple daily checklist|checks|Open;Check;Close"),
]
def generate():
    out = []
    for d, ask, a, b in DIRS:
        for th, p, kind in PROJECTS:
            A, B = a.replace("{p}", p), b.replace("{p}", p)
            if any(len(x.split("|")[0]) > 20 for x in (A, B)): continue
            out.append((f"gen-{d}-{p.lower().replace(' ', '-')}", th, kind, ask.replace("{t}", th), A, B))
    return out
