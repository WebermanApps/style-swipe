"""Light and medium decks: member profile, employee attire, sign-up form (UpKeep shelf), Legal Questions Center grouping (Legal shelf),
Research (Machan launch + checkout, tech certs + training + cool tech) and WellNest new tea ideas (baby steps only, R73).
Settled and not re-asked: profile header picks (photo hero, quick actions, header colours), attire polo/pants/shoes/cap/covers/layers picks,
sign-up label, error, agreement, summary and code picks, Machan mark picks, Smart Upkeep checkout platform picks, existing tea line picks."""
from md1018_kit import *
ORG = ORANGE
def person(x, y, shirt, pants="#3F3F46", shoe="#1F1F1F", extra="", sleeve=True, shorts=False):
    s = f'<circle cx="{x}" cy="{y}" r="11" fill="#E9D5C3"/>'
    s += f'<path d="M{x-20} {y+18} q20 -8 40 0 v42 h-40 z" fill="{shirt}"/>'
    if sleeve: s += f'<path d="M{x-20} {y+18} l-10 26 h8 l6 -14 M{x+20} {y+18} l10 26 h-8 l-6 -14" fill="{shirt}"/>'
    lh = 26 if shorts else 50
    s += rect(x - 18, y + 60, 16, lh, pants, "none", 3) + rect(x + 2, y + 60, 16, lh, pants, "none", 3)
    if shorts: s += rect(x - 16, y + 86, 12, 24, "#E9D5C3", "none", 3) + rect(x + 4, y + 86, 12, 24, "#E9D5C3", "none", 3)
    s += rect(x - 22, y + 110, 20, 8, shoe, "none", 3) + rect(x + 2, y + 110, 20, 8, shoe, "none", 3)
    s += f'<circle cx="{x-9}" cy="{y+28}" r="3" fill="#FFFFFF" opacity=".85"/>' + extra
    return s
def fig(*people, h=136):
    return ("raw", "".join(people), h)
def T_PROFILE():
    pairs, P = make("md18mp_", "UpKeep"); L = "UpKeep Member App · Profile"; MP = "UpKeep Member Profile"
    def ok(c=ORG, txt="All good at home"): return ("raw", rect(14, 0, 212, 56, c + "14", c, 12) + ic("check", 26, 14, 28, c) + t(64, 26, txt, 13, INK, "khand") + t(64, 40, "Last whole-house scan, Oct 12", 7.5, MUTE), 62)
    P("Member Profile", MP, "All good sign colour", "should the all-good sign be in member orange or a calm jungle green?",
      ("orange", "Member Orange", "Orange tick and border, the member colour.", "playful", S(L, [ok()], ("Matches the member app", ""))),
      ("green", "Jungle Green", "Green tick, the usual all-clear colour.", "calm", S(L, [ok(JUNGLE)], ("Reads as all-clear", ""))))
    PR = [("Gutter clog", "Found Oct 12", TERRA), ("Attic damp", "Watch", SAFFRON), ("Dryer lint", "Found Oct 12", TERRA)]
    P("Member Profile", MP, "Problems found", "when a scan finds problems should they show as a swipe carousel of problem cards or a short list?",
      ("car", "Problem Card Carousel", "One problem per card with its photo.", "playful", S(L, [("h", "2 Things To Fix", 14), ("carousel", PR, 150, 90, True, False, 0, True, None, False, "photo")], ("One problem at a time", ""))),
      ("list", "Short List", "Name, where and when on each row.", "calm", S(L, [("h", "2 Things To Fix", 14), ("cards", [(a, b) for a, b, c in PR], [c for a, b, c in PR])], ("See them all at once", ""))))
    P("Member Profile", MP, "How serious", "should each problem show how serious it is with a word tag like Fix Soon or a coloured left edge?",
      ("tag", "Word Tag", "Fix Soon or Keep An Eye On It.", "practical", S(L, [("raw", rect(14, 0, 212, 50, "#FFFFFF", LINE, 10) + t(24, 22, "Gutter clog", 10, INK, "khand") + rect(150, 10, 64, 16, TERRA + "18", "none", 8) + t(182, 21, "Fix soon", 7.5, TERRA, "hind", 700, "middle"), 56)], ("No guessing", ""))),
      ("edge", "Coloured Left Edge", "Terracotta for soon, saffron for watch.", "calm", S(L, [("raw", rect(14, 0, 212, 50, "#FFFFFF", LINE, 10) + rect(14, 0, 4, 50, TERRA) + t(26, 22, "Gutter clog", 10, INK, "khand") + t(26, 36, "Found Oct 12", 7.5, MUTE), 56)], ("Quieter cards", ""))))
    P("Member Profile", MP, "Where the problem is", "should the whole-house scan show problems as pins on a simple house drawing or as a line naming the area?",
      ("pins", "Pins On A House Drawing", "A drawn house with a pin per problem.", "playful", S(L, [("raw", f'<path d="M50 70 L120 20 L190 70 V130 H50 Z" fill="{SOFT}" stroke="{INK}" stroke-width="1.4"/>' + dot(90, 40, 6, TERRA) + dot(160, 110, 6, SAFFRON) + t(120, 146, "2 problems found", 8, MUTE, anchor="middle"), 152)], ("See it at a glance", ""))),
      ("line", "Area Line", "Roof and gutters, attic, laundry.", "calm", S(L, [("kv", [("Roof and gutters", "1"), ("Attic", "1"), ("Laundry", "0")])], ("Plain words", ""))))
    P("Member Profile", MP, "Scan date", "should the date of the last whole-house scan sit under the all-good sign or in the header?",
      ("under", "Under The Sign", "Last scan Oct 12 right under All good.", "calm", S(L, [ok()], ("Sign and date together", ""))),
      ("header", "In The Header", "Scanned Oct 12 next to the address.", "practical", S(L, [("raw", t(14, 12, "12 Oak Lane  ·  scanned Oct 12", 8, MUTE), 18), ("raw", rect(14, 0, 212, 44, ORG + "14", ORG, 12) + ic("check", 26, 10, 24, ORG) + t(60, 27, "All good at home", 13, INK, "khand"), 50)], ("Cleaner sign", ""))))
    P("Member Profile", MP, "Fixed problems", "once a problem is fixed should it slide into a Fixed carousel or leave the profile?",
      ("fixed", "Fixed Carousel", "Fixed problems with before and after photos.", "playful", S(L, [ok(), ("h", "Fixed", 12), ("carousel", [("Gutter clog", "Fixed Oct 14", JUNGLE), ("Dryer lint", "Fixed Oct 14", JUNGLE)], 150, 50)], ("Proof the work got done", ""))),
      ("leave", "Leaves The Profile", "Only open problems ever show.", "calm", S(L, [ok()], ("Only what needs you", "Visit report keeps the record"))))
    P("Member Profile", "UpKeep Tech App Member Profile", "Tech view colour", "when a tech opens a member's profile should the blue tech colour run as a top band or only on the name and buttons?",
      ("band", "Blue Top Band", "A lagoon band across the top.", "focused", S("UpKeep Tech App · Member Profile", [("raw", rect(0, -8, 240, 40, LAGOON, "none", 0) + t(14, 18, "12 Oak Lane", 13, "#FFFFFF", "khand"), 40), ("cards", [(a, b) for a, b, c in PR[:2]], [TERRA, SAFFRON])], ("Clearly the tech view", ""))),
      ("accent", "Blue Accents Only", "White header, lagoon name and buttons.", "calm", S("UpKeep Tech App · Member Profile", [("raw", t(14, 18, "12 Oak Lane", 13, LAGOON, "khand"), 28), ("cards", [(a, b) for a, b, c in PR[:2]], [TERRA, SAFFRON]), ("btn", "Start Visit", "fill", LAGOON)], ("Lighter screen", ""))))
    P("Member Profile", MP, "Member orange shade", "should member orange be the brand terracotta or a brighter warm orange?",
      ("terra", "Brand Terracotta", "The same terracotta as the site.", "calm", S(L, [ok(TERRA)], ("One brand colour", ""))),
      ("warm", "Brighter Warm Orange", "A warmer orange just for members.", "playful", S(L, [ok("#E07B39")], ("Members get their own colour", ""))))
    P("Member Profile", MP, "Nothing found yet", "before the first whole-house scan should the profile show a Scan Booked card or a calm Not Scanned Yet line?",
      ("card", "Scan Booked Card", "Your first scan: Oct 22 with your tech.", "practical", S(L, [("card", "First scan booked", "Oct 22  ·  your tech maps your home", ORG, "", "dot", 40)], ("Something to look forward to", ""))),
      ("line", "Not Scanned Yet Line", "One grey line until the first visit.", "calm", S(L, [("p", "Not scanned yet", 46, MUTE)], ("Quiet until there is news", ""))))
    P("Member Profile", MP, "Problem photo", "on each problem card should the photo be the tech's close-up or a wider room photo with a circle?",
      ("close", "Close-Up Photo", "The problem fills the frame.", "focused", S(L, [("photo", 110, TERRA, "room", "Gutter clog, close-up")], ("See the problem clearly", ""))),
      ("wide", "Wide With A Circle", "The area with the spot circled.", "practical", S(L, [("raw", photo(14, 0, 212, 110, TERRA, "house") + f'<circle cx="160" cy="34" r="16" fill="none" stroke="{TERRA}" stroke-width="2"/>', 116), ("p", "Gutter clog, front left", 46, MUTE)], ("See where it is", ""))))
    return pairs
def T_ATTIRE():
    pairs, P = make("md18at_", "UpKeep"); L = "UpKeep Crew Uniform"; U = "UpKeep Crew Uniform"
    CH, KH, TC = "#3F3F46", "#B9A27E", TERRA
    P("Crew Uniform", U, "Hot-day option", "on hot days should techs be allowed charcoal work shorts or stay in long work pants?",
      ("shorts", "Charcoal Work Shorts", "Knee-length, same charcoal as the pants.", "playful", S(L, [fig(person(120, 14, TC, CH, shorts=True))], ("Cooler outdoors", "Long pants for crawl spaces"))),
      ("pants", "Long Pants Always", "Charcoal pants every day.", "calm", S(L, [fig(person(120, 14, TC, CH))], ("One look", "Knees covered"))))
    P("Crew Uniform", U, "Blue for techs", "since techs are blue in the apps should there be a lagoon blue polo option beside the terracotta one?",
      ("blue", "Add A Lagoon Polo", "Terracotta or lagoon, tech's pick.", "playful", S(L, [fig(person(80, 14, TC, CH), person(160, 14, LAGOON, CH))], ("Matches the tech app", ""))),
      ("terra", "Terracotta Only", "The brand colour on every tech.", "calm", S(L, [fig(person(120, 14, TC, CH))], ("Always on brand", ""))))
    P("Crew Uniform", U, "Shirt for estimates", "for estimate visits should techs have a button-up work shirt option or wear the polo?",
      ("button", "Button-Up Option", "A charcoal button-up with the small mark.", "focused", S(L, [fig(person(120, 14, CH, KH, extra=f'<line x1="120" y1="34" x2="120" y2="74" stroke="#FFFFFF" stroke-width="1"/>'))], ("A bit smarter", ""))),
      ("polo", "Polo For Everything", "Same polo for every visit.", "calm", S(L, [fig(person(120, 14, TC, CH))], ("Simple", ""))))
    P("Crew Uniform", U, "Wet-weather shoe", "for rainy days should techs get a waterproof boot option beside the work shoe?",
      ("boot", "Add A Waterproof Boot", "Black boot for wet yards.", "practical", S(L, [("raw", rect(40, 30, 60, 70, "#1F1F1F", "none", 8) + rect(30, 90, 80, 20, "#1F1F1F", "none", 8) + rect(140, 70, 70, 40, "#1F1F1F", "none", 10) + t(70, 128, "Boot", 9, INK, "khand", anchor="middle") + t(175, 128, "Work shoe", 9, INK, "khand", anchor="middle"), 136)], ("Dry feet", ""))),
      ("shoe", "Work Shoe Only", "One work shoe all year.", "calm", S(L, [("raw", rect(85, 70, 70, 40, "#1F1F1F", "none", 10) + t(120, 128, "Work shoe", 9, INK, "khand", anchor="middle"), 136)], ("Fewer things to buy", ""))))
    P("Crew Uniform", U, "Work gloves", "should work gloves be charcoal with a small terracotta cuff or plain grey?",
      ("cuff", "Charcoal, Terracotta Cuff", "A small brand touch on the hands.", "playful", S(L, [("raw", rect(60, 20, 50, 80, CH, "none", 14) + rect(60, 90, 50, 18, TC, "none", 4) + rect(130, 20, 50, 80, CH, "none", 14) + rect(130, 90, 50, 18, TC, "none", 4), 116)], ("On brand", ""))),
      ("grey", "Plain Grey", "Any grey work glove.", "calm", S(L, [("raw", rect(60, 20, 50, 88, "#9CA3AF", "none", 14) + rect(130, 20, 50, 88, "#9CA3AF", "none", 14), 116)], ("Easy to replace", ""))))
    P("Crew Uniform", U, "Roadside safety", "for roadside or street work should techs have a light hi-vis vest with the logo or no vest?",
      ("vest", "Hi-Vis Vest With Logo", "Safety yellow with a small white mark.", "practical", S(L, [fig(person(120, 14, "#E3D24A", CH))], ("Safe near traffic", ""))),
      ("none", "No Vest", "The polo is enough.", "calm", S(L, [fig(person(120, 14, TC, CH))], ("Simpler kit", ""))))
    P("Crew Uniform", U, "Shirt fit", "should shirts come in a fitted cut and a relaxed cut, or one relaxed cut for everyone?",
      ("two", "Fitted And Relaxed", "Two cuts, tech's pick.", "practical", S(L, [fig(person(80, 14, TC, CH), person(160, 14, TC, CH, sleeve=False))], ("Looks neat on everyone", ""))),
      ("one", "One Relaxed Cut", "Same shirt for all.", "calm", S(L, [fig(person(120, 14, TC, CH))], ("Easy ordering", ""))))
    P("Crew Uniform", U, "Cold-day hat", "for cold days should techs get a charcoal beanie with a small mark or keep the cap?",
      ("beanie", "Charcoal Beanie", "Small terracotta mark on the fold.", "playful", S(L, [("raw", f'<path d="M70 90 Q70 30 120 30 Q170 30 170 90 Z" fill="{CH}"/>' + rect(66, 84, 108, 20, CH, "none", 4) + rect(110, 88, 20, 12, TC, "none", 2), 116)], ("Warm and on brand", ""))),
      ("cap", "Cap All Year", "The white cap stays.", "calm", S(L, [("raw", f'<path d="M80 80 Q80 40 120 40 Q160 40 160 80 Z" fill="#FFFFFF" stroke="{INK}"/>' + rect(140, 74, 50, 8, "#FFFFFF", INK, 4), 116)], ("One hat", ""))))
    P("Crew Uniform", U, "Belt", "should the uniform include a plain black belt or leave belts to each tech?",
      ("black", "Plain Black Belt", "Part of the kit.", "calm", S(L, [fig(person(120, 14, TC, CH, extra=rect(100, 72, 40, 5, "#111111", "none", 1)))], ("Same look on every tech", ""))),
      ("own", "Tech's Own Belt", "Any plain belt.", "practical", S(L, [fig(person(120, 14, TC, CH))], ("Less to hand out", ""))))
    P("Crew Uniform", "UpKeep Tech App Uniform", "Choosing the day's outfit", "in the tech app should the day's outfit be a swipe carousel of the options or a simple checklist?",
      ("car", "Outfit Carousel", "Swipe shirts, pants and shoes.", "playful", S("UpKeep Tech App · Uniform", [("h", "Today's Kit", 14), ("carousel", [("Terracotta polo", "Shirt", TC), ("Charcoal pants", "Pants", CH), ("Work shoe", "Shoes", INK)], 140, 60)], ("Pick in seconds", ""))),
      ("check", "Simple Checklist", "Tick what you are wearing.", "calm", S("UpKeep Tech App · Uniform", [("h", "Today's Kit", 14), ("checks", ["Polo", "Pants", "Shoes", "Shoe covers"], JUNGLE, 2)], ("Nothing to swipe", ""))))
    return pairs
def T_SIGNUP():
    pairs, P = make("md18su_", "UpKeep"); L = "Smart Upkeep · Sign Up, Phone"; F = "Smart Upkeep Site Sign Up Form"
    P("Sign Up Form", "UpKeep Sales Call Sign Up", "Cancel notice in person", "for in-person and sales-call sign-ups, where the 3-day cancel notice is required, should it be its own step or a box on the signing screen?",
      ("step", "Its Own Step", "A full screen to read before signing.", "focused", S("UpKeep Sales Call · Tablet", [("steps", ["Plan", "Home", "Notice", "Sign"], TERRA, 2), ("h", "Your Right To Cancel", 14), ("p", "You may cancel within 3 business days. Sample wording only.", 44, MUTE), ("btn", "I Have Read This", "fill", TERRA)], ("Cannot be missed", ""))),
      ("box", "Box On The Signing Screen", "A tinted box right above the signature.", "calm", S("UpKeep Sales Call · Tablet", [("raw", rect(14, 0, 212, 46, CREAM, "none", 8) + t(24, 18, "Your right to cancel", 9, INK, "khand") + t(24, 32, "3 business days. Sample wording.", 7.5, MUTE), 52), ("raw", rect(14, 0, 212, 50, "#FFFFFF", INK, 8) + t(24, 30, "Sign here", 8, FAINT), 56)], ("One less step", ""))))
    P("Sign Up Form", F, "Online cancel line", "online, where the notice is not required, should the form still show a short cancel-anytime line or show nothing?",
      ("line", "Short Cancel Line", "Cancel anytime from your app.", "calm", S(L, [("btn", "Continue", "fill", TERRA), ("p", "Cancel anytime from your app", 46, MUTE, True)], ("Still reassuring", ""))),
      ("none", "Nothing Extra", "The form ends at Continue.", "practical", S(L, [("btn", "Continue", "fill", TERRA)], ("Shorter form", ""))))
    P("Sign Up Form", F, "Form length", "should sign-up be one page you scroll or short steps with Continue?",
      ("one", "One Page", "Everything on one scroll.", "calm", S(L, [("input", "Street address", INK, "home"), ("input", "Email", INK, "search"), ("tabs", ["Essentials", "Plus", "Complete"], "pill"), ("btn", "Start Membership", "fill", TERRA)], ("See it all", ""))),
      ("steps", "Short Steps", "Home, plan, details, pay.", "focused", S(L, [("steps", ["Home", "Plan", "Details", "Pay"], TERRA, 0), ("input", "Street address", INK, "home"), ("btn", "Continue", "fill", TERRA)], ("One thing at a time", ""))))
    P("Sign Up Form", F, "Step marker", "if sign-up uses steps should progress show as named steps or a thin bar?",
      ("named", "Named Steps", "Home, Plan, Details, Pay across the top.", "practical", S(L, [("steps", ["Home", "Plan", "Details", "Pay"], TERRA, 1), ("tabs", ["Essentials", "Plus", "Complete"], "pill")], ("Know what is next", ""))),
      ("bar", "Thin Bar", "A bar that fills.", "calm", S(L, [("bar", .5, TERRA), ("tabs", ["Essentials", "Plus", "Complete"], "pill")], ("Less to read", ""))))
    P("Sign Up Form", F, "Choosing a plan", "should plans show as a swipe carousel of plan cards or three stacked cards?",
      ("car", "Plan Card Carousel", "Swipe Essentials, Plus, Complete.", "playful", S(L, [("h", "Pick Your Plan", 14), ("carousel", [("Essentials", "$XX a month", JUNGLE), ("Plus", "$XX a month", LAGOON), ("Complete", "$XX a month", TERRA)], 150, 90, True, False, 1)], ("Room for each plan", ""))),
      ("stack", "Three Stacked Cards", "All three plans in view.", "calm", S(L, [("h", "Pick Your Plan", 14), ("cards", [("Essentials", "$XX a month"), ("Plus", "$XX a month"), ("Complete", "$XX a month")], [JUNGLE, LAGOON, TERRA])], ("Compare at once", ""))))
    P("Sign Up Form", F, "Lawn care add-on", "since lawn care is the only add-on should it show as a simple on and off switch or a small card with a photo?",
      ("switch", "On And Off Switch", "Add lawn care, one switch.", "calm", S(L, [("toggles", [("Add lawn care", True)])], ("Quick", ""))),
      ("card", "Card With A Photo", "A small lawn photo and Add.", "playful", S(L, [("raw", rect(14, 0, 212, 70, "#FFFFFF", LINE, 10) + photo(22, 8, 60, 54, JUNGLE, "leaf") + t(92, 30, "Lawn care", 11, INK, "khand") + t(92, 44, "Add to your plan", 7.5, MUTE), 76), ("btn", "Add", "line", JUNGLE)], ("Shows what you get", ""))))
    P("Sign Up Form", F, "Address entry", "should the address box suggest addresses as you type or show a map pin to drop?",
      ("type", "Suggestions As You Type", "A short list drops under the box.", "practical", S(L, [("input", "12 Oak", INK, "home"), ("cards", [("12 Oak Lane", ""), ("12 Oak Street", "")], [INK], "none", "line", 24)], ("Fast and exact", ""))),
      ("pin", "Map Pin", "Drop a pin on your home.", "playful", S(L, [("map", 110), ("btn", "This Is My Home", "fill", TERRA)], ("Visual", ""))))
    P("Sign Up Form", F, "Finish later", "should a half-done sign-up keep its answers on the phone for next time or start fresh?",
      ("keep", "Keeps Your Answers", "Pick up where you left off.", "practical", S(L, [("banner", "Welcome back, you were on step 2", LAGOON, "clock"), ("btn", "Continue", "fill", TERRA)], ("No retyping", ""))),
      ("fresh", "Starts Fresh", "Nothing saved on the phone.", "calm", S(L, [("steps", ["Home", "Plan", "Details", "Pay"], TERRA, 0), ("btn", "Continue", "fill", TERRA)], ("Nothing left behind", ""))))
    P("Sign Up Form", F, "Continue button", "on a phone should the Continue button stick to the bottom of the screen or sit at the end of the form?",
      ("stick", "Sticks To The Bottom", "Always in reach.", "practical", S(L, [("input", "Street address", INK, "home"), ("input", "Email", INK, "search"), ("raw", rect(0, 70, 240, 44, "#FFFFFF", LINE, 0) + rect(14, 78, 212, 28, TERRA, "none", 8) + t(120, 96, "CONTINUE", 8, "#FFFFFF", "hind", 700, "middle"), 116)], ("Never scroll to find it", ""))),
      ("end", "At The End", "Under the last box.", "calm", S(L, [("input", "Street address", INK, "home"), ("input", "Email", INK, "search"), ("btn", "Continue", "fill", TERRA)], ("Calmer screen", ""))))
    P("Sign Up Form", F, "Pay screen order", "on the pay step should phone wallet buttons come first or the card form first?",
      ("wallet", "Phone Wallet First", "Apple Pay and Google Pay on top.", "practical", S(L, [("btn", "Pay With Phone Wallet", "fill", INK), ("p", "or pay by card", 46, MUTE, True), ("input", "Card number", INK, "card")], ("Two taps to pay", ""))),
      ("card", "Card Form First", "Card boxes on top, wallet under.", "calm", S(L, [("input", "Card number", INK, "card"), ("btn", "Start Membership", "fill", TERRA), ("btn", "Pay With Phone Wallet", "line", INK)], ("Familiar", ""))))
    return pairs
def T_LEGAL():
    pairs, P = make("md18lq_", "Legal"); L = "Legal Questions Center · Phone"; Q = "Legal Questions Center"
    G = [("Tech Cam And Privacy", "11"), ("Membership Terms And Billing", "10"), ("Platform Terms", "10"), ("Trademark, IP And Data", "6"), ("Entity And Licensing", "3")]
    def groups(gs=G, c=None): return ("cards", [(a, b + " questions") for a, b in gs], c or [LAGOON, TERRA, JUNGLE, SAFFRON, INK])
    P("Grouping", Q, "Main grouping", "should the Questions Center group questions by topic or by how soon they need an answer?",
      ("topic", "By Topic", "Tech cam, terms, platform, trademark.", "calm", S(L, [("h", "Questions", 14), groups()], ("Related questions together", ""))),
      ("soon", "By How Soon", "Soon first, then open.", "practical", S(L, [("h", "Questions", 14), ("cards", [("Soon", "2 questions"), ("Open", "39 questions")], [TERRA, INK])], ("Urgent ones first", ""))))
    P("Grouping", Q, "Small groups", "should tiny groups like Brand And Trademark (1 question) merge into a bigger group or keep their own?",
      ("merge", "Merge Into Bigger Groups", "Brand joins Trademark, IP And Data.", "calm", S(L, [groups()], ("Fewer, fuller groups", ""))),
      ("keep", "Keep Their Own", "Every topic gets its own group.", "practical", S(L, [groups(G + [("Brand And Trademark", "1")])], ("Exact topics", ""))))
    P("Grouping", Q, "Spending questions", "should questions that need your OK to spend money get their own Needs Your OK group or stay in their topic with a tag?",
      ("group", "Needs Your OK Group", "All spend decisions in one place.", "focused", S(L, [("cards", [("Needs Your OK", "spend decisions"), ("Tech Cam And Privacy", "11 questions")], [TERRA, LAGOON])], ("Money calls in one spot", ""))),
      ("tag", "Tag In The Topic", "A small Needs OK tag on the card.", "calm", S(L, [("raw", rect(14, 0, 212, 44, "#FFFFFF", LINE, 10) + t(24, 20, "Cyber cover tier", 10, INK, "khand") + rect(150, 8, 64, 16, TERRA + "18", "none", 8) + t(182, 19, "Needs OK", 7.5, TERRA, "hind", 700, "middle"), 50)], ("Topics stay whole", ""))))
    P("Grouping", Q, "Group order", "should the biggest group come first or the group with the most Soon questions?",
      ("big", "Biggest First", "Tech Cam And Privacy on top.", "calm", S(L, [groups()], ("Steady order", ""))),
      ("soon", "Most Urgent First", "Order changes as questions come in.", "practical", S(L, [groups([G[3], G[0], G[1], G[2], G[4]])], ("Urgent on top", ""))))
    P("Grouping", Q, "Review before sending", "should Platform Terms (Review Before Sending) stay its own group or become a Review tag on each question?",
      ("group", "Own Group", "All drafts to review in one group.", "practical", S(L, [groups()], ("One place to review", ""))),
      ("tag", "Review Tag", "Questions sit in their topic with a tag.", "calm", S(L, [groups([g for g in G if g[0] != "Platform Terms"])], ("Fewer groups", ""))))
    P("Grouping", Q, "Jump to a group", "should a row of group chips sit at the top to jump to a group or should you just scroll?",
      ("chips", "Group Chips On Top", "Tap a chip to jump.", "practical", S(L, [("tags", ["Tech Cam", "Terms", "Platform", "Trademark", "Entity"], True), groups(G[:3])], ("Quick to reach", ""))),
      ("scroll", "Just Scroll", "Groups one under another.", "calm", S(L, [groups(G[:4])], ("Cleaner top", ""))))
    P("Grouping", Q, "Order inside a group", "inside a group should Soon questions sit first or the newest questions first?",
      ("soon", "Soon First", "Then the rest.", "practical", S(L, [("h", "Tech Cam And Privacy", 13), ("cards", [("Camera notice wording", "Soon"), ("Clip storage time", "Open"), ("Member photo rules", "Open")], [TERRA, INK, INK])], ("Urgent never buried", ""))),
      ("new", "Newest First", "Latest question on top.", "calm", S(L, [("h", "Tech Cam And Privacy", 13), ("cards", [("Member photo rules", "Oct 17"), ("Clip storage time", "Oct 16"), ("Camera notice wording", "Oct 14")], [INK])], ("See what is new", ""))))
    P("Grouping", Q, "Answered questions", "once answered should a question move to an Answered group at the bottom or leave the center?",
      ("group", "Answered Group At The Bottom", "Folded, with a count.", "practical", S(L, [groups(G[:3]), ("card", "Answered", "12 questions", JUNGLE, "", "dot", 34)], ("Easy to look back", ""))),
      ("leave", "Leaves The Center", "Only open questions show.", "calm", S(L, [groups(G[:3])], ("Only what needs you", ""))))
    P("Grouping", Q, "Group look on a phone", "on a phone should groups show as a swipe carousel of group cards or a stacked list?",
      ("car", "Group Card Carousel", "One group per card with its count.", "playful", S(L, [("h", "Questions", 14), ("carousel", [(a, b + " questions", c) for (a, b), c in zip(G, [LAGOON, TERRA, JUNGLE])], 150, 70)], ("Short page", ""))),
      ("list", "Stacked List", "Groups one under another.", "calm", S(L, [("h", "Questions", 14), groups(G[:4])], ("See all groups", ""))))
    P("Grouping", Q, "Group names", "should group names be short like Tech Cam or full like Tech Cam And Privacy?",
      ("short", "Short Names", "Tech Cam, Terms, Platform.", "calm", S(L, [groups([("Tech Cam", "11"), ("Terms And Billing", "10"), ("Platform", "10")])], ("Quick to read", ""))),
      ("full", "Full Names", "Tech Cam And Privacy and so on.", "practical", S(L, [groups(G[:3])], ("Clear what is inside", ""))))
    return pairs
def T_RES1():
    pairs, P = make("md18rm_", "Research"); L = "Research · Machan Launch"; M = "Machan Launch Presentation"; C = "Checkout Options PDF"
    def mslide(title, body=""): return ("raw", rect(14, 0, 212, 120, "#FFFFFF", "#D6D0C6", 6) + t(24, 18, title.upper(), 7.5, MUTE, "hind", 700, extra='letter-spacing="1"') + body, 128)
    P("Machan Launch", M, "First thing to offer", "for the Machan launch should the first offer be a free dashboard link or a small item at about $10?",
      ("free", "Free Dashboard Link", "Try it free, build a following first.", "calm", S(L, [mslide("First Offer", t(24, 60, "Free dashboard", 16, INK, "khand") + t(24, 76, "link in the post", 9, MUTE))], ("More people try it", ""))),
      ("ten", "About $10 Item", "A small paid item from day one.", "practical", S(L, [mslide("First Offer", t(24, 60, "$10 item", 16, INK, "khand") + t(24, 76, "price is a sample", 9, MUTE))], ("Proves people will pay", ""))))
    P("Machan Launch", M, "Presentation format", "should the launch plan be a short swipe deck of slides or a one-page site?",
      ("slides", "Short Slide Deck", "Six slides you swipe.", "playful", S(L, [mslide("Launch Plan"), ("cdots", 6, 0)], ("Easy to present", ""))),
      ("page", "One-Page Site", "One scrolling page.", "calm", S(L, [("h", "Machan Launch Plan", 14), ("cards", [("Who it is for", ""), ("What we offer", ""), ("Launch week", "")], [LAGOON, JUNGLE, TERRA], "num")], ("Easy to share", ""))))
    P("Machan Launch", M, "Where it launches", "should Machan launch with a thread on X or with a landing page linked from one post?",
      ("thread", "Thread On X", "Five posts telling the story.", "playful", S(L, [("bubble", "1 of 5: why Machan exists"), ("bubble", "2 of 5: what you can try")], ("Meets people where they are", ""))),
      ("page", "Landing Page Link", "One post with a link.", "calm", S(L, [("bubble", "Machan is live, try it here"), ("raw", rect(14, 0, 212, 50, CREAM, LINE, 8) + t(24, 28, "Machan landing page", 10, INK, "khand"), 56)], ("Everything in one place", ""))))
    P("Machan Launch", M, "What the $10 item is", "if there is a $10 item should it be a digital template pack or a printed sticker set?",
      ("digital", "Digital Template Pack", "Download right away.", "practical", S(L, [("tiles", [("Templates", "card"), ("Guide", "star")], 2, 60)], ("No shipping", ""))),
      ("sticker", "Printed Sticker Set", "Machan stickers by post.", "playful", S(L, [("raw", "".join(f'<circle cx="{60+i*60}" cy="50" r="24" fill="{c}22" stroke="{c}"/>' for i, c in enumerate((LAGOON, JUNGLE, TERRA))), 90)], ("Something to hold", ""))))
    P("Machan Launch", M, "Machan in the plan", "should the Machan mascot appear on every slide or only on the cover and the end?",
      ("every", "Every Slide", "A small mascot in the corner.", "playful", S(L, [mslide("Launch Week", f'<circle cx="200" cy="100" r="10" fill="{LAGOON}"/>')], ("Friendly throughout", ""))),
      ("ends", "Cover And End Only", "The middle stays plain.", "calm", S(L, [mslide("Launch Week")], ("Content first", ""))))
    P("Checkout PDF", C, "Option layout", "should the checkout options PDF compare options in one table or give each option its own card?",
      ("table", "One Comparison Table", "Rows of options, columns of scores.", "practical", S(L, [("table", [("Option A", "Secure  Easy  Tracks"), ("Option B", "Secure  Easy"), ("Option C", "Easy  Tracks")], True)], ("Compare at a glance", ""))),
      ("cards", "Card Per Option", "A short card for each option.", "calm", S(L, [("carousel", [("Option A", "Secure, easy, tracks", JUNGLE), ("Option B", "Secure, easy", LAGOON)], 150, 70)], ("Room to explain", ""))))
    P("Checkout PDF", C, "Scores", "should security, ease and tracking scores show as small bars or as plain Good, Fair and Weak words?",
      ("bars", "Small Bars", "Three bars per option.", "practical", S(L, [("bar", .9, JUNGLE, "Security", ""), ("bar", .7, LAGOON, "Ease", ""), ("bar", .5, TERRA, "Tracking", "")], ("Quick to compare", ""))),
      ("words", "Plain Words", "Good, Fair, Weak.", "calm", S(L, [("kv", [("Security", "Good"), ("Ease", "Good"), ("Tracking", "Fair")])], ("No reading charts", ""))))
    P("Checkout PDF", C, "Fees", "should fees show as a range like 3 to 5 percent or as the cost on a sample $100 sale?",
      ("range", "Percent Range", "About X to X percent.", "calm", S(L, [("kv", [("Fee", "X to X%"), ("Payout", "X days")])], ("Standard way", ""))),
      ("sale", "Cost On A $100 Sale", "You keep $XX of $100.", "practical", S(L, [("word", "$XX", 30, INK, "kept from a sample $100 sale")], ("Easy to picture", ""))))
    P("Checkout PDF", C, "Order tracking view", "for reliable tracking should the PDF show a sample order timeline or a list of what each option tracks?",
      ("timeline", "Sample Order Timeline", "Paid, sent, delivered, each with a time.", "practical", S(L, [("timeline", [("Paid", "sample"), ("Sent", "sample"), ("Delivered", "sample")])], ("See tracking in action", ""))),
      ("list", "What Each Tracks", "A checklist per option.", "calm", S(L, [("checks", ["Payment receipts", "Order status", "Refund record"], JUNGLE, 3)], ("Clear and complete", ""))))
    P("Checkout PDF", C, "Top pick", "should the PDF open with a recommended pick or let the options speak first?",
      ("pick", "Recommended Pick First", "Our pick and why, then the rest.", "focused", S(L, [("card", "Our pick: Option A", "secure, easy, tracks every order", JUNGLE, "", "dot", 40), ("cards", [("Option B", ""), ("Option C", "")], [INK])], ("Fast decision", ""))),
      ("options", "Options First", "Pick on the last page.", "calm", S(L, [("cards", [("Option A", ""), ("Option B", ""), ("Option C", "")], [INK])], ("No nudge", ""))))
    return pairs
def T_RES2():
    pairs, P = make("md18rt_", "Research"); L = "Research · Tech Growth"; CP = "Tech Certs PDF"; CT = "Cool Tech List"; TW = "Tech Training Week"
    P("Tech Certs", CP, "Ranking chart", "should the certs PDF rank certs on a skill versus customer-love bubble chart or in a ranked table?",
      ("blob", "Skill Vs Customer-Love Chart", "Bubble size shows cost.", "playful", S(L, [("blobs", [("First aid", .7, .25, 12, TERRA), ("HVAC basics", .38, .45, 14, LAGOON), ("Mold check", .6, .6, 11, JUNGLE)], 110, ("Less skill", "More skill", "Customers shrug", "Customers love"))], ("See the sweet spot", ""))),
      ("table", "Ranked Table", "Cert, cost, skill, customer love.", "calm", S(L, [("table", [("First aid", "$XX  ·  high love"), ("HVAC basics", "$XXX  ·  high skill"), ("Mold check", "$XXX")], True)], ("Easy to read", ""))))
    P("Tech Certs", CP, "Costs", "should cert costs show as exact prices with sources or as $, $$ and $$$ bands?",
      ("exact", "Exact With Sources", "Price and where it came from.", "practical", S(L, [("kv", [("First aid", "$XX  source"), ("HVAC basics", "$XXX  source")])], ("Ready to budget", ""))),
      ("bands", "Price Bands", "$, $$ or $$$.", "calm", S(L, [("kv", [("First aid", "$"), ("HVAC basics", "$$$")])], ("Quick feel", ""))))
    P("Tech Certs", "Tech Profile Cert Badges", "Badges for members", "should certs a member would love, like first aid, show as badges on the tech's profile?",
      ("badge", "Badges On The Profile", "Small lagoon badges under the name.", "playful", S(L, [("thumb", "Your tech", LAGOON, "block", "person"), ("tags", ["First aid", "Mold check"])], ("Builds trust", ""))),
      ("none", "Keep Certs Inside", "Certs stay in the team records.", "calm", S(L, [("thumb", "Your tech", LAGOON, "block", "person")], ("Clean profile", ""))))
    P("Cool Tech", CT, "Wow gauge", "should the wow factor show as a half-circle gauge or as one to five stars?",
      ("gauge", "Half-Circle Gauge", "A needle from meh to wow.", "playful", S(L, [("h", "Thermal Camera", 14), ("gauge", .8, "Wow", TERRA)], ("Fun to read", ""))),
      ("stars", "One To Five Stars", "Stars next to each item.", "calm", S(L, [("h", "Thermal Camera", 14), ("raw", "".join(ic("star", 20 + i * 22, 0, 18, SAFFRON if i < 4 else "#D6D0C6") for i in range(5)), 24)], ("Familiar", ""))))
    P("Cool Tech", CT, "List layout", "should the cool tech list be a swipe carousel of item cards or a table with cost, difficulty and wow?",
      ("car", "Item Card Carousel", "Photo, cost, difficulty, wow per card.", "playful", S(L, [("carousel", [("Thermal camera", "$XXX  ·  easy", TERRA), ("Leak sensor", "$XX  ·  easy", LAGOON), ("Drone roof check", "$XXX  ·  hard", JUNGLE)], 150, 100, True, False, 0, True, None, False, "photo")], ("Each item shines", ""))),
      ("table", "Table", "Everything in rows.", "calm", S(L, [("table", [("Thermal camera", "$XXX easy"), ("Leak sensor", "$XX easy"), ("Drone roof", "$XXX hard")], True)], ("Compare fast", ""))))
    P("Cool Tech", CT, "Sort order", "should the list sort by wow factor or by cost?",
      ("wow", "By Wow", "Most impressive first.", "playful", S(L, [("cards", [("Drone roof check", "wow 5"), ("Thermal camera", "wow 4"), ("Leak sensor", "wow 3")], [TERRA], "num")], ("Lead with the exciting", ""))),
      ("cost", "By Cost", "Cheapest first.", "practical", S(L, [("cards", [("Leak sensor", "$XX"), ("Thermal camera", "$XXX"), ("Drone roof check", "$XXX")], [JUNGLE], "num")], ("Lead with easy wins", ""))))
    P("Training Week", TW, "Day order", "should Training Week start with the company vision or with the tech the business runs on?",
      ("vision", "Vision First", "Monday: why Smart Upkeep exists.", "calm", S(L, [("steps", ["Vision", "Build", "Tech", "Field", "Review"], TERRA, 0)], ("Purpose before tools", ""))),
      ("tech", "Tech First", "Monday: the apps and tools.", "practical", S(L, [("steps", ["Tech", "Build", "Vision", "Field", "Review"], TERRA, 0)], ("Useful from day one", ""))))
    P("Training Week", TW, "Month of study", "should the month of study topics show as a calendar or a checklist?",
      ("cal", "Calendar", "A topic on each day.", "playful", S(L, [("cal", (2, 5, 9, 12, 16, 19, 23), LAGOON)], ("Paced", ""))),
      ("check", "Checklist", "Tick topics in any order.", "calm", S(L, [("checks", ["Home systems", "Moisture readings", "Customer care", "App deep dive"], JUNGLE, 1)], ("Flexible", ""))))
    P("Training Week", TW, "End of each day", "should each training day end with a short quiz deck or a talk with Max?",
      ("quiz", "Short Quiz Deck", "Swipe a few checks.", "playful", S(L, [("h", "Day 1 Check", 14), ("btn2", "Option A", "Option B")], ("Measures learning", ""))),
      ("talk", "Talk With Max", "Ten minutes, no quiz.", "calm", S(L, [("h", "Day 1 Wrap", 14), ("cal", (1,), TERRA)], ("Personal", ""))))
    P("Training Week", TW, "Training format", "should each day's deck be read alone on the phone or presented together on a laptop?",
      ("phone", "Read Alone On The Phone", "Swipe through at their own pace.", "calm", S(L, [("h", "Day 2: How It Was Built", 13), ("cdots", 8, 2)], ("Own pace", ""))),
      ("laptop", "Presented Together", "Max walks through it on a laptop.", "focused", S("Tech Training Week · 1280", [("desk", t(10, 40, "Day 2: How It Was Built", 12, INK, "khand"), 90)], ("Questions answered live", ""))))
    return pairs
def T_TEA():
    pairs, P = make("md18tn_", "WellNest"); L = "WellNest Teas · New Blends"; N = "WellNest New Tea Ideas"
    def pouch(name, c, sub=""): return ("raw", f'<path d="M80 10 h80 l8 120 h-96 z" fill="{c}22" stroke="{c}" stroke-width="1.5"/>' + rect(88, 50, 64, 40, "#FFFFFF", "none", 4) + t(120, 70, name, 11, INK, "khand", anchor="middle") + t(120, 84, sub, 7, MUTE, anchor="middle"), 140)
    def pick(cap, a, b): P("New Teas", N, cap[0], cap[1], a, b)
    pick(("Sleep tea", "for one of the six new teas, should there be a bedtime sleep tea or a slow afternoon unwind tea?"),
      ("sleep", "Bedtime Sleep Tea", "Soft and fully herbal for night.", "calm", S(L, [pouch("SLEEP", LAGOON, "bedtime blend")], ("For the end of the day", ""))),
      ("after", "Afternoon Unwind", "A gentle lift-free break.", "playful", S(L, [pouch("PAUSE", JUNGLE, "afternoon blend")], ("For a slow afternoon", ""))))
    pick(("Ginger warmer", "should one new tea be a warm ginger blend or a cooling mint blend?"),
      ("ginger", "Warm Ginger", "A spicy, cosy cup.", "playful", S(L, [pouch("WARM", TERRA, "ginger blend")], ("Cool evenings", ""))),
      ("mint", "Cooling Mint", "A fresh cup for hot days.", "calm", S(L, [pouch("COOL", JUNGLE, "mint blend")], ("Hot days", ""))))
    pick(("Iced tea", "should one new tea be made for cold brew in a bottle or stay a hot-brew loose tea?"),
      ("cold", "Cold Brew Bottle Tea", "Steep in cold water overnight.", "playful", S(L, [("raw", rect(100, 10, 40, 120, LAGOON + "22", LAGOON, 10) + t(120, 70, "COLD", 10, INK, "khand", anchor="middle"), 140)], ("Easy on hot days", ""))),
      ("hot", "Hot Brew Loose Tea", "The usual cup.", "calm", S(L, [pouch("HOT", TERRA, "loose tea")], ("Classic", ""))))
    pick(("Family tea", "should one new tea be a gentle caffeine-free tea for the whole family?"),
      ("family", "Whole-Family Tea", "Mild flavour, no caffeine.", "calm", S(L, [pouch("FAMILY", SAFFRON, "for everyone")], ("Wider audience", ""))),
      ("adult", "Grown-Up Blends Only", "Keep the line for adults.", "practical", S(L, [pouch("GROWN-UP", INK, "for adults")], ("Focused line", ""))))
    pick(("Floral tea", "should one new tea lean floral like jasmine or fruity like dried mango?"),
      ("floral", "Floral, Like Jasmine", "A scented, delicate cup.", "calm", S(L, [pouch("FLORAL", "#B5838D", "jasmine idea")], ("Elegant", ""))),
      ("fruit", "Fruity, Like Dried Mango", "A sweet, bright cup.", "playful", S(L, [pouch("FRUIT", SAFFRON, "mango idea")], ("Fun", ""))))
    pick(("Morning tea", "should one new tea be a strong morning black tea or a light green tea?"),
      ("black", "Strong Morning Black", "Bold enough for milk.", "practical", S(L, [pouch("MORNING", TERRA, "black tea")], ("Coffee swap", ""))),
      ("green", "Light Green", "Fresh and gentle.", "calm", S(L, [pouch("GREEN", JUNGLE, "green tea")], ("Light lift", ""))))
    pick(("Farm-grown tea", "should one new tea use only herbs from the WellNest farm or mix in partner growers?"),
      ("farm", "Our Farm Only", "Every herb grown on site.", "calm", S(L, [pouch("FARM", JUNGLE, "grown here")], ("A real farm story", ""))),
      ("mix", "Farm Plus Partners", "Farm herbs with partner leaves.", "practical", S(L, [pouch("HARVEST", LAGOON, "farm and friends")], ("More choices", ""))))
    pick(("Seasonal tea", "should one of the six be a seasonal tea that changes each season or a year-round tea?"),
      ("season", "Changes Each Season", "A new blend four times a year.", "playful", S(L, [pouch("SEASON", TERRA, "limited run")], ("Something new to try", ""))),
      ("year", "Year-Round", "Always on the shelf.", "calm", S(L, [pouch("ALWAYS", INK, "every month")], ("Easy to restock", ""))))
    pick(("Tea for guests", "should one new tea be made for WellNest guests on arrival or for selling in shops?"),
      ("guest", "Welcome Tea For Guests", "Served when guests arrive.", "calm", S(L, [("raw", f'<path d="M80 60 h80 v30 a40 30 0 0 1 -80 0 z" fill="{JUNGLE}22" stroke="{JUNGLE}"/>' + t(120, 130, "Welcome cup", 10, INK, "khand", anchor="middle"), 140)], ("A signature moment", ""))),
      ("shop", "Made For Shops", "Pouch first, sold in stores.", "practical", S(L, [pouch("SHOP", TERRA, "retail blend")], ("More sales", ""))))
    pick(("Tea strength", "for the new teas should most be bold blends or light, easy blends?"),
      ("bold", "Bold Blends", "Strong flavours that stand out.", "playful", S(L, [pouch("BOLD", TERRA, "strong cup")], ("Memorable", ""))),
      ("light", "Light, Easy Blends", "Gentle cups for any time.", "calm", S(L, [pouch("EASY", JUNGLE, "gentle cup")], ("Easy to love", ""))))
    return pairs
