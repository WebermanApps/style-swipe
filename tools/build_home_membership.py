#!/usr/bin/env python3
"""Build Style Swipe deck home-membership-1: brand deck for Max's home maintenance membership (working product name 'Home Record').
Run from the repo root: python3 tools/build_home_membership.py. Writes decks/home-membership-1.json (fetched via ?date=home-membership-1)."""
import json, datetime as dt, os, random
DID = "home-membership-1"; TEAL = "#4F8A8B"; TERRA = "#C1502E"; LAGOON = "#05668D"; JUNGLE = "#0B6E4F"
FEEL = {"neighbor": "Trusted neighbor who handles it", "system": "Calm, organized system for your home",
        "concierge": "Premium concierge for your house (quiet quality)", "crew": "No-nonsense pro trade crew"}

# ---- Name conflict check (Oct 11, 2026): quick web + .com check only, NOT a trademark search ----
NAME_CHECK = {
 "candidates_considered": 56,
 "dropped_conflicts": {
  "Tended": "Tended (tendedhome.com, Westwood KS) sells a home maintenance membership; also usetended.com maintenance reports",
  "Home Ledger": "HomeLedger home maintenance app (App Store, homeledger.app)",
  "Kepthouse": "Kepthouse home maintenance tracker app (kepthouse.app)",
  "House Record": "HouseRecord home maintenance tracker (houserecordapp.com)",
  "Homefile": "Homefile, 'making home ownership easy' (homefile.com)",
  "Upkept": "UpKept Services property maintenance (upkept.com)",
  "House Tune": "HomeTune preventive home maintenance subscription, Louisville KY",
  "Steady / Steady House": "Steady Home Maintenance memberships, Flowood MS",
  "Kindred Home": "Kindred Home Support home maintenance service",
  "Housemark": "Housemark homebuying AI (housemark.io) and UK housing inspections app",
  "Rounds": "Rounds Home, Frisco/Plano home services (roundshome.com)",
  "Housewell": "Housewell real estate (housewell.com)", "Dwello": "dwello.com active business",
  "Good House": "goodhouse.com redirects to Good Housekeeping", "Hearth": "Hearth contractor financing / hearth.com",
  "Homewise": "Homewise mortgage/insurance brands", "Plumb Line": "Plumbline bathroom and kitchen products",
  "Housekept": "HouseKept cleaning (AU), same idea", "Porch & Co": "porchandco.com active", "Porchlight": "porchlight.com active, Porch home-services family",
  "Keel Home": "Keel Home Development, home builder", "Hearthwise": "hearthwise.com active", "Next Door Tech": "close to Nextdoor (well-known mark)",
  "Hello House": "HelloHouse residential communities", "Square Home": "squarehome.com active", "Upkeep Club": "upkeepclub.com 'Coming Soon' (likely taken)"},
 "note": "Survivors passed a quick check only (no clear same-name US home-services brand or app found; .com not an obvious active business). EVERY survivor still needs a real USPTO/TESS trademark search and a domain purchase check before use. 'Home Record' is crowded (Home Record Keeper app, houserecordapp.com, homerecord.com active energy-software business): keep it as the in-app feature name, not the company name."}
S = lambda st, dom: {"status": st, "domain": dom}
NAMES = {  # name: (feeling, style, sub, font, upper, check)
 "Home Record": ("system","descriptive","Every system, visit and warranty in one place.","khand",False,S("crowded: feature name only; needs TM search","homerecord.com taken (active)")),
 "House Friend": ("neighbor","warm-human","Your house person, every month.","hind",False,S("no conflict found; needs TM search","housefriend.com registered, no active site seen")),
 "The House Steward": ("concierge","descriptive","We look after your house, quietly.","khand",False,S("no conflict found; needs TM search","thehousesteward.com registered, not resolving")),
 "Wrench & Record": ("crew","trade-honest","Real techs. Real records.","khand",True,S("no conflict found; needs TM search","wrenchandrecord.com appears unregistered")),
 "Monthly Rounds": ("system","descriptive","Same day, same tech, every month.","khand",False,S("no conflict found; needs TM search","monthlyrounds.com appears unregistered")),
 "Your House Person": ("neighbor","warm-human","Someone who knows your house.","hind",False,S("no conflict found; needs TM search","yourhouseperson.com appears unregistered")),
 "Sill & Key": ("concierge","coined","Care for the whole house.","khand",True,S("no conflict found; needs TM search","sillandkey.com appears unregistered")),
 "Filter Day": ("crew","trade-honest","Filters, gutters, flushes. Done monthly.","khand",True,S("no conflict found; needs TM search","filterday.com appears unregistered")),
 "The House File": ("system","descriptive","The whole story of your house.","khand",False,S("no conflict found; needs TM search","thehousefile.com registered, parked")),
 "Quiet House": ("concierge","one-word","Nothing breaks. Nobody calls.","hind",False,S("no conflict found; needs TM search","quiethouse.com registered, not resolving")),
 "Well Kept House": ("neighbor","warm-human","Looked after, like a neighbor would.","hind",False,S("no conflict found; needs TM search","wellkepthouse.com registered, placeholder")),
 "Square & Level": ("crew","trade-honest","Done right. Written down.","khand",True,S("no conflict found; needs TM search","squareandlevel.com registered, not resolving")),
 "Home Logbook": ("system","descriptive","Your home's logbook, kept for you.","khand",False,S("no conflict found; needs TM search","homelogbook.com registered, not resolving")),
 "Housecall Club": ("concierge","descriptive","A house call, every month.","khand",False,S("no conflict found; needs TM search","housecallclub.com appears unregistered")),
 "Hommly": ("neighbor","coined","Home, handled.","hind",False,S("no conflict found; needs TM search","hommly.com registered, blank page")),
 "House OS": ("system","coined","The operating system for your house.","khand",True,S("no conflict found in quick check; needs TM search","houseos.com registered, not resolving")),
 "Tendwell": ("neighbor","coined","Tended well, every month.","hind",False,S("similar: TendWell Studios (web agency, WI), not home services; needs TM search","tendwell.com appears unregistered")),
 "Monthly Crew": ("crew","trade-honest","Your crew, on the calendar.","khand",True,S("no conflict found; needs TM search","monthlycrew.com registered, not resolving")),
 "Home Index": ("system","descriptive","Know your house.","khand",False,S("no conflict found; needs TM search","homeindex.com appears unregistered")),
 "Abodi": ("concierge","coined","Your house, cared for.","hind",False,S("no conflict found; needs TM search","abodi.com registered ('Hello!' page)")),
 "Kept": ("neighbor","one-word","Your house, kept.","khand",True,S("no conflict found; needs TM search (common word)","kept.com unknown; kepthome.com registered")),
 "True Square": ("crew","trade-honest","Straight answers. Square work.","khand",True,S("no conflict found; needs TM search","truesquare.com for sale")),
 "The Monthly Visit": ("crew","trade-honest","One visit a month keeps the house right.","hind",False,S("no conflict found; needs TM search","themonthlyvisit.com appears unregistered")),
 "Level House": ("system","trade-honest","Everything level, everything logged.","khand",False,S("no conflict found; needs TM search","levelhouse.com registered, not resolving")),
 "Filter & Flush": ("crew","trade-honest","The boring stuff, done right.","khand",True,S("no conflict found; needs TM search","filterandflush.com appears unregistered")),
 "House Rounds": ("concierge","descriptive","Rounds for your house, like a good doctor.","khand",False,S("no conflict found; needs TM search","houserounds.com registered, parked")),
 "Home Checkup": ("crew","trade-honest","A monthly checkup for your house.","khand",False,S("generic term used by others (e.g. RyboHome); weak as a mark","homecheckup.com registered")),
 "Rooftrue": ("system","coined","True to the roof.","khand",False,S("no conflict found; needs TM search","rooftrue.com registered, blank page")),
}
NAME_PAIRS = [("Home Record","House Friend"),("The House Steward","Wrench & Record"),("Monthly Rounds","Your House Person"),("Sill & Key","Filter Day"),
 ("The House File","Quiet House"),("Well Kept House","Square & Level"),("Home Logbook","Housecall Club"),("Hommly","House OS"),("Tendwell","Monthly Crew"),
 ("Home Index","Abodi"),("Kept","True Square"),("The Monthly Visit","Level House"),("Filter & Flush","House Rounds"),("Home Checkup","Rooftrue")]
FTAGS = {"neighbor":["friendly","warm","personal"],"system":["clear","calm","organized"],"concierge":["calm","premium-quiet","personal"],"crew":["direct","industrial","honest"]}
def slug(s): return "".join(c if c.isalnum() else "_" for c in s.lower()).strip("_")
def nm(n):
    f, st, sub, font, up, chk = NAMES[n]
    return {"id": f"hm1_name_{slug(n)}", "label": n, "desc": f"{st.title()} name. {sub}", "tags": [f, "name-"+st]+FTAGS[f][:2], "feeling": f,
            "name_check": chk, "visual": {"type":"hm","m":"name","name":n,"style":f"{FEEL[f].split(' (')[0]}","sub":sub,"font":font,"upper":up,"acc":TEAL,"domain":chk["domain"]}}
pairs = []
def add(cat, a, b, ask=None, purpose="refine"): pairs.append({"category":cat,"app":"Home Membership","ask":ask,"optionA":a,"optionB":b,"purpose":purpose})
for a, b in NAME_PAIRS: add("Brand Name", nm(a), nm(b), "Which Name Fits The Home Membership?")
def o(i, label, desc, tags, feel, vis): return {"id":"hm1_"+i,"label":label,"desc":desc,"tags":tags+([feel] if feel else []),"feeling":feel,"visual":{"type":"hm",**vis}}
# Tagline & tone (6)
T=lambda i,l,line,body,feel,tags,font="khand",bg=None:o(i,l,line,tags,feel,{"m":"tag","line":line,"body":body,"font":font,"acc":TEAL,**({"bg":bg} if bg else {})})
add("Tagline & Tone",T("tg_neighbor","Neighbor: We've Got Your House","We've got your house.","Hi Sarah, Danny here. Swapped your furnace filter and flushed the water heater. All good. See you Nov 4.","neighbor",["friendly","warm"]),
    T("tg_system","System: Every System, On Record","Every system. Every visit. On record.","Visit complete: furnace filter replaced, water heater flushed. Added to your Home Record. Next visit: Nov 4.","system",["clear","calm"]))
add("Tagline & Tone",T("tg_concierge","Concierge: Your House, Looked After","Your house, looked after.","Good afternoon, Sarah. Today's visit is complete and your Home Record is up to date. Nothing needs your attention.","concierge",["calm","premium-quiet"]),
    T("tg_crew","Crew: Filters. Gutters. Flushes. Done.","Filters. Gutters. Flushes. Done.","Done: filter (16x25x1), water heater flush, 6 smoke detectors tested. Photos in the app. Nov 4 next.","crew",["direct","honest"]))
add("Tagline & Tone",T("tg_neighbor2","Neighbor: The Tech Who Knows Your House","The tech who knows your house.","Hey Sarah, noticed the gutter by the garage was pulling away. Snapped a photo and tightened it. No charge.","neighbor",["friendly","personal"]),
    T("tg_concierge2","Concierge: Never Think About It Again","Never think about your house again.","Your November visit is booked for Tuesday, 9 to 11. We'll take care of everything. Reply only if you need us.","concierge",["calm","premium-quiet"]))
add("Tagline & Tone",T("tg_system2","System: Know Your Home","Know your home.","Your water heater is 9 years old. Typical life: 10 to 12. We'll keep flushing it and flag it a year ahead.","system",["clear","organized"]),
    T("tg_crew2","Crew: Show Up. Fix It. Write It Down.","Show up. Fix it. Write it down.","Smoke detector in hall was dead. Replaced battery. Logged. Done.","crew",["direct","industrial"]))
add("Tagline & Tone",T("tg_quietprem","Quiet Premium: Small Visits, Big Peace","Small visits. Big peace of mind.","Your visit is done. Everything checked, nothing urgent. Details are in your Home Record.","concierge",["calm","premium-quiet","minimal"]),
    T("tg_neighbor4","Neighbor: Your House, In Good Hands","Your house is in good hands.","All done today, Sarah. Everything looks good. I'll be back the first Tuesday of December. - Danny","neighbor",["friendly","warm"]),"Which Tagline Feels Right?")
add("Tagline & Tone",T("tg_neighbor3","Neighbor: Like Having A Handy Neighbor","Like having a handy neighbor. On call.","Text me anytime. If it's quick, I'll handle it on the next visit. - Danny","neighbor",["friendly","warm"]),
    T("tg_formal","Formal: Comprehensive Residential Maintenance","Comprehensive residential maintenance solutions.","Pursuant to your service agreement, the scheduled preventive maintenance has been completed in accordance with our standards.","system",["formal","corporate"]),None,"check")
# Logo (6)
L=lambda i,l,kind,feel,tags,desc,acc=TEAL,mono=None:o(i,l,desc,tags,feel,{"m":"logo","kind":kind,"name":"Home Record","acc":acc,**({"mono":mono} if mono else {})})
add("Logo Mark",L("lg_housecheck","House With A Check","house-check","system",["clear","minimal"],"Line house outline with a teal check inside."),
    L("lg_doorsmile","Door With A Smile","door-smile","neighbor",["friendly","warm"],"Rounded front door; the knob line is a small smile."))
add("Logo Mark",L("lg_record","Record With A Tab","record-tab","system",["organized","clear"],"A file card with a colored tab: the Home Record."),
    L("lg_wrench","Wrench In A House","wrench-house","crew",["industrial","direct"],"Solid house shape with a wrench cut out."))
add("Logo Mark",L("lg_ring","Ring And Dot","ring-dot","concierge",["minimal","premium-quiet"],"A quiet circle with a small accent dot. Abstract and calm."),
    L("lg_mono","Square Monogram HR","monogram","crew",["bold","industrial"],"Bold HR in a square frame, like a stamp on a toolbox.",mono="HR"))
add("Logo Mark",L("lg_key","Key Line","key","concierge",["calm","premium-quiet"],"Simple key: we hold the keys to your house's care."),
    L("lg_crest","Gold Crest","crest","concierge",["luxe","gold","dark","formal"],"Dark shield crest with gold serif monogram."),"Quiet Premium Or Overt Luxe?","check")
add("Logo Mark",L("lg_housecheck_terra","House Check In Terracotta","house-check","neighbor",["warm","friendly"],"Same house-check mark in warm terracotta.",acc=TERRA),
    L("lg_record_lagoon","Record Tab In Lagoon","record-tab","system",["clear","calm"],"Record mark in lagoon blue.",acc=LAGOON))
add("Logo Mark",L("lg_ring_jungle","Ring And Dot In Jungle","ring-dot","system",["natural","calm"],"Ring-dot mark in jungle green."),
    L("lg_door_teal","Door Smile In Teal","door-smile","neighbor",["friendly","calm"],"Door-smile in the explainer's muted teal."))
pairs[-1]["optionA"]["visual"]["acc"]=JUNGLE
# Accent (4)
PAL=lambda c:[c,"#1F1F1F","#737373","#E5E5E5"]
A_=lambda i,l,c,feel,tags,desc:o(i,l,desc,tags,feel,{"m":"accent","acc":c,"pal":PAL(c)})
add("Accent Color",A_("ac_teal","Muted Teal (Explainer)",TEAL,"system",["calm","clear"],"The explainer's muted teal #4F8A8B on cream, black, white and grey."),
    A_("ac_terra","Terracotta",TERRA,"neighbor",["warm","friendly"],"Max's terracotta #C1502E: warm, human, earthy."))
add("Accent Color",A_("ac_lagoon","Lagoon",LAGOON,"system",["clear","calm"],"Lagoon blue #05668D: trustworthy, a little cooler."),
    A_("ac_jungle","Jungle",JUNGLE,"crew",["natural","honest"],"Jungle green #0B6E4F: natural, 'done' green."))
add("Accent Color",A_("ac_teal2","Muted Teal",TEAL,"concierge",["calm","premium-quiet"],"Muted teal as the only accent: quiet."),
    A_("ac_lagoon2","Lagoon",LAGOON,"crew",["direct","clear"],"Lagoon as the accent: sharper, more 'work order'."))
add("Accent Color",A_("ac_terra2","Terracotta",TERRA,"crew",["warm","industrial"],"Terracotta: work-wear warmth."),
    A_("ac_safety","Safety Orange","#F26A1B","crew",["bold","vibrant","loud"],"Hi-vis safety orange, like a trade brand."),None,"check")
# App home & Home Record (6)
P=lambda i,l,s,feel,tags,desc,title="Home Record":o(i,l,desc,tags,feel,{"m":"app","style":s,"acc":TEAL,"title":title})
add("App Home & Home Record",P("ap_systems","Systems Grid With AI Labels","systems","system",["clear","organized"],"Home opens on your 4 systems: photo tiles with the AI label and model."),
    P("ap_next","Next Visit First","next","neighbor",["friendly","personal"],"Home opens on 'Your tech, Danny, visits Tue Nov 4' and three counts."))
add("App Home & Home Record",P("ap_timeline","Record As A Timeline","timeline","system",["calm","organized"],"The Home Record reads as a dated timeline of visits."),
    P("ap_list","Record As A Status List","list","crew",["direct","minimal"],"One row per system with a status dot: Good, Flush due."))
add("App Home & Home Record",P("ap_warranty","Warranty Bars","warranty","system",["clear","organized"],"Each system shows warranty time left as a bar."),
    P("ap_dash","Dark Health Score Dashboard","dash","system",["dark","techy","bold"],"Dark dashboard with a 'home health' score and chart."),None,"check")
add("App Home & Home Record",P("ap_next2","Next Visit, Calm","next","concierge",["calm","premium-quiet"],"Big date card, nothing else to do."),
    P("ap_systems2","Systems, Photo Proof","systems","crew",["honest","direct"],"Your systems with the photos the tech took."))
add("App Home & Home Record",P("ap_list2","Status List, Neighborly","list","neighbor",["friendly","clear"],"Plain status list with a friendly note from your tech."),
    P("ap_timeline2","Timeline, Full Detail","timeline","crew",["honest","organized"],"Every visit, every part, dated."))
add("App Home & Home Record",P("ap_warranty2","Warranties Up Front","warranty","concierge",["calm","organized"],"We watch your warranties so you don't have to."),
    P("ap_next3","Next Visit Up Front","next","system",["clear","calm"],"Date first, counts second."))
# Uniform & van (3)
add("Tech Uniform & Van",o("un_chest","Cream Shirt, Small Chest Logo","Light cream work shirt, small teal logo on the chest, name tag.",["minimal","calm","premium-quiet"],"concierge",{"m":"uniform","shirt":"#F4F1EA","place":"chest","acc":TEAL,"name2":True,"note":"Small chest logo + name tag. Quiet, tidy."}),
    o("un_big","Grey Shirt, Big Back Name","Grey work shirt with the name big across the back.",["direct","industrial","bold"],"crew",{"m":"uniform","shirt":"#D6D3CC","place":"big","acc":TEAL,"name":"Home Record","note":"Big name, readable from the driveway."}))
add("Tech Uniform & Van",o("vn_white","White Van, Wordmark + Thin Stripe","White van, black wordmark, thin teal stripe.",["clear","minimal","calm"],"system",{"m":"van","wrap":"stripe","acc":TEAL,"line":"Monthly home maintenance · Every visit on record"}),
    o("vn_full","White Van, Bold Teal Lower Half","Big teal band on the lower half, white text.",["bold","direct","industrial"],"crew",{"m":"van","wrap":"full","acc":TEAL,"line":"Filters · Gutters · Water heaters · Smoke detectors"}))
add("Tech Uniform & Van",o("vn_quiet","Cream Van, Small Wordmark","Cream van, small wordmark, nothing else.",["minimal","calm","premium-quiet"],"concierge",{"m":"van","wrap":"none","body":"#F4F1EA","acc":TEAL,"line":"homerecord"}),
    o("vn_dark","Charcoal Van, White Wordmark","Dark charcoal van with a white wordmark.",["dark","bold","industrial"],"crew",{"m":"van","wrap":"none","body":"#2B2B2B","ink":"#FFFFFF","acc":TEAL,"line":"Monthly home maintenance"}),None,"check")
# Explainer video (5)
V=lambda i,l,desc,tags,feel,**k:o(i,l,desc,tags,feel,{"m":"video","acc":TEAL,**k})
add("Explainer Video Style",V("vd_illus_calm","Line Illustration, Calm Pace","Simple line drawings, 4 scenes in 45s, calm VO.",["calm","clear","minimal"],"system",look="illus",chips=["4 scenes / 45s","Voiceover","Soft piano"],vo="VO: \"Snap your furnace. We label it. A tech comes monthly. It all goes in your Home Record.\""),
    V("vd_photo_people","Real Photos, Real Tech","Real photos of a tech in a real house, captions.",["warm","honest","personal"],"neighbor",look="photo",chips=["8 shots / 45s","Captions","Acoustic guitar"],frames=["Meet Danny","He checks the furnace","Flushes the heater","Logs it for you"],vo="Captions only, no voice. Warm daylight footage."))
add("Explainer Video Style",V("vd_fast","Fast Cuts, Big Captions","Quick cuts every 1.5s with big Khand captions.",["direct","bold"],"crew",look="photo",cap="big",chips=["24 cuts / 45s","Big captions","Percussion"],frames=["FILTERS","GUTTERS","FLUSH","DONE"],vo="No VO. Captions punch each task."),
    V("vd_slow","Slow, One Idea Per Scene","Few scenes, long holds, gentle VO.",["calm","premium-quiet"],"concierge",look="illus",chips=["3 scenes / 45s","Soft VO","Ambient"],frames=["Your house","Looked after","On record"],vo="VO: \"You don't have to remember any of it. We do.\""))
add("Explainer Video Style",V("vd_vo_max","Max Voiceover","Max explains it himself, on camera at the start.",["personal","warm","friendly"],"neighbor",look="photo",chips=["Max on camera","His voice","Light music"],frames=["Hi, I'm Max","Here's how","Monthly visits","Your record"],vo="\"I built this because my own furnace filter was two years old.\""),
    V("vd_vo_pro","Pro Narrator","Neutral pro narrator, no faces.",["clear","calm"],"system",look="illus",chips=["Narrator","No faces","Soft synth"],vo="Clean, neutral voice. Steps appear as simple icons."))
add("Explainer Video Style",V("vd_music_warm","Warm Acoustic Mood","Acoustic guitar, morning light, kitchen sounds.",["warm","natural","friendly"],"neighbor",look="photo",chips=["Acoustic","Morning light","Room tone"],frames=["Morning","Knock knock","Quick check","Coffee's on"],vo="Music: light acoustic, 90 bpm."),
    V("vd_music_work","Work Sounds Beat","Beat built from drill, ratchet and van door sounds.",["industrial","direct"],"crew",look="photo",cap="big",chips=["Tool-sound beat","110 bpm","No VO"],frames=["Van door","Ratchet","Filter in","Logged"],vo="Music: rhythm made from real tool sounds."))
add("Explainer Video Style",V("vd_cream","Light Cream Illustration (Current)","The current explainer look: cream, line art, teal accent.",["light","calm","clear"],"system",look="illus",chips=["Current explainer","Cream + teal","Captions + VO"],vo="Keeps the existing 45s explainer style."),
    V("vd_dark","Dark Cinematic","Dark, moody footage with dramatic music.",["dark","cinematic","dramatic"],"concierge",look="dark",chips=["Dark grade","Trailer music","Slow push-ins"],frames=["Every home","Has a story","Protect it","Home Record"],vo="Deep trailer VO, low strings."),None,"check")
# Membership card & pricing (3)
add("Membership Card & Pricing",o("cd_clean","Clean White Member Card","White card, house-check mark, address and 'Member since'.",["clear","minimal","premium-quiet"],"concierge",{"m":"card","acc":TEAL,"name":"Home Record"}),
    o("cd_lux","Black And Gold Platinum Card","Black card, gold serif, 'Platinum', roman numerals.",["luxe","gold","dark","formal"],"concierge",{"m":"card","lux":True,"name":"Home Record"}),"Quiet Premium Or Overt Luxe?","check")
add("Membership Card & Pricing",o("pr_three","Three Plans, Middle Highlighted","Basic / Home / Whole Home with prices up front.",["clear","direct"],"system",{"m":"price","acc":TEAL,"hi":1,"head":"Pick Your Plan","tiers":[["Basic","$49","Filters + smoke detectors"],["Home","$89","+ gutters, water heater flush"],["Whole Home","$149","+ AC/furnace tune-ups"]],"foot":"Cancel anytime · Price set after your photo quote"}),
    o("pr_one","One Plan, Your Quote","One membership; price comes from your photos.",["calm","minimal","personal"],"neighbor",{"m":"price","acc":TEAL,"hi":0,"head":"One Membership","tiers":[["Your house","$79*","Monthly visit, all 4 systems, Home Record included"]],"foot":"*Typical. Your exact price comes from the photos you send."}))
add("Membership Card & Pricing",o("cd_terra","Cream Card, Terracotta Tab","Cream card with a terracotta record tab.",["warm","friendly"],"neighbor",{"m":"card","acc":TERRA,"cardbg":"#FFFDF7","name":"Home Record"}),
    o("pr_crew","Itemized Like A Work Order","Plans as a checklist of tasks with times.",["direct","honest","industrial"],"crew",{"m":"price","acc":TEAL,"hi":0,"head":"What We Do Each Month","tiers":[["Every visit","$89","Filter · smoke test · leak check · 45 min"],["Seasonal","incl.","Gutters spring/fall · flush 2x/yr"]],"foot":"No upsells on site. Anything extra is quoted first."}))
# Swipe controls (3), reuse the controls renderer
EARTH=["#3F6E7D","#5A7D4F","#B5523B","#A0703C"]
C=lambda i,l,desc,tags,**k:{"id":"hm1_"+i,"label":l,"desc":desc,"tags":tags,"feeling":None,"visual":{"type":"controls","words":["This","Both","Love","That"],"icons":["◀","⇄","❤","▶"],"colors":EARTH,"bg":"#FAF6EE","font":"Hind","stampov":"word","press":None,**k}}
add("Swipe Controls",C("sc_teal_pill","Teal Outline Pills","Pills in the membership teal, outline until pressed.",["calm","clear"],fmt="pill",style="outline",press="fill",colors=[TEAL]*4,hint="edges"),
    C("sc_earth_round","Earthy Round, Outline","Max's current pick: earthy round outline buttons.",["warm","natural"],fmt="round",style="outline",hint="edges"))
add("Swipe Controls",C("sc_check_word","Stamp: Check Plus Word","Stamp shows a check icon plus the word.",["clear","friendly"],fmt="round",style="outline",stampov="icon",hint="edges"),
    C("sc_khand_caps","Stamp: Word In Khand Caps","Stamp is just the word, Khand caps.",["direct","bold"],fmt="round",style="outline",stampov="word",hint="edges"))
add("Swipe Controls",C("sc_seg","Segmented Bar","One bar split into four.",["minimal","organized"],fmt="segmented",style="outline",hint="above"),
    C("sc_thumb","Big Thumb Pads","Two big pads, This and That.",["direct","bold"],fmt="thumb",style="filled",hint="above"))
# finalize
random.seed(11)
first = pairs[:2]; rest = pairs[2:]; random.shuffle(rest); seq = first + rest
order=[]; pool=seq[:]                       # avoid same category twice in a row
while pool:
    k = next((i for i,p in enumerate(pool) if not order or p["category"]!=order[-1]["category"]), 0); order.append(pool.pop(k))
for i,p in enumerate(order,1):
    p["id"]=f"{DID}-{i:02d}"; p["retest"]=False; p["repeat"]=False
    p["optionA"].setdefault("feeling",None); p["ask"]=p["ask"] or ("Which Name Fits?" if p["category"]=="Brand Name" else f"Which {p['category']} Feels Right?")
alloc={}; [alloc.__setitem__(p["category"],alloc.get(p["category"],0)+1) for p in order]
feel={}
for p in order:
    for s in "AB":
        f=p["option"+s].get("feeling");
        if f: feel[f]=feel.get(f,0)+1
deck={"date":DID,"version":4,"owner":"Max Weberman","format":"pairs","english_only":True,"light_only":True,
 "title":"Home Membership Brand (Working Name: Home Record)",
 "brands":["Home maintenance membership: photo onboarding, AI system labels, monthly tech visits, the Home Record; US pilot, licensed to a Thai company","Base: light cream, black/white/grey, Khand/Hind; explainer accent muted teal #4F8A8B vs terracotta, lagoon, jungle"],
 "generated_at":dt.datetime.now().astimezone().isoformat(timespec="seconds"),
 "feelings":FEEL,"feeling_counts":feel,"allocation":alloc,"apps":{"Home Membership":len(order)},
 "pair_mix":{"refine":sum(p["purpose"]=="refine" for p in order),"check":sum(p["purpose"]=="check" for p in order)},
 "name_check":NAME_CHECK,"freshness":{"option_slots":2*len(order),"never_shown_before":2*len(order),"share":1.0},"warnings":[],"pairs":order}
os.makedirs("decks",exist_ok=True)
json.dump(deck,open(f"decks/{DID}.json","w"),indent=1,ensure_ascii=False)
print(len(order),"pairs",alloc,deck["pair_mix"],feel)
