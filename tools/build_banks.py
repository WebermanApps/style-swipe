#!/usr/bin/env python3
"""Build / refill Style Swipe question banks: banks/<slug>.json, 100 ready this-or-that pairs per category.
Same pair schema as decks/*.json, drawn with tools/personal_kit.py (on draft_svg.py). Example data only.
Bank option ids are reserved in banks/bank_ids.json (NOT shown_options.json; they are not counted as shown).

  python3 tools/build_banks.py            # build: keep current banks, fill to 100 (same as --refill)
  python3 tools/build_banks.py --refill   # drop pairs in banks/used.json, retire pairs >14 days old, top up to 100
Idempotent: running twice in a row changes nothing. Run from the repo root."""
import sys, os, json, re, glob, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
from personal_kit import *
import personal_kit as PK

TARGET, MAX_AGE = 100, 14
TODAY = dt.date.today().isoformat()
FEED = "/workspace/ops/team-feed.md"

# ---------- apparel on people ----------
SKIN = "#D9C3A5"
def person(x, y, s, c, kind="tee", mark="M"):
    g = f'<circle cx="{x}" cy="{y}" r="{9*s}" fill="{SKIN}"/>'
    if kind == "cap": g += f'<path d="M{x-9*s} {y-3*s} Q{x} {y-14*s} {x+9*s} {y-3*s} Z" fill="{c}"/><rect x="{x}" y="{y-4*s}" width="{11*s}" height="{2.5*s}" fill="{c}"/>'
    g += f'<path d="M{x-16*s} {y+50*s} V{y+22*s} Q{x-16*s} {y+12*s} {x-6*s} {y+11*s} H{x+6*s} Q{x+16*s} {y+12*s} {x+16*s} {y+22*s} V{y+50*s} Z" fill="{c}"/>'
    if kind == "polo": g += f'<path d="M{x-5*s} {y+11*s} L{x} {y+18*s} L{x+5*s} {y+11*s}" fill="#FFFFFF"/>'
    if kind == "jacket": g += f'<line x1="{x}" y1="{y+12*s}" x2="{x}" y2="{y+50*s}" stroke="#FFFFFF" stroke-width="{1.2*s}"/>'
    if kind == "apron": g += rect(x - 9 * s, y + 20 * s, 18 * s, 30 * s, "#FFFFFF", c, 2, 1)
    g += rect(x - 16 * s, y + 50 * s, 32 * s, 26 * s, INK, "none", 2)
    g += t(x + 8 * s, y + 26 * s, mark, 6 * s, "#FFFFFF" if kind != "apron" else c, "khand", anchor="middle")
    return g
def b_wear(a, items, c, r, gap, pk):
    n, d, v = items[a % len(items)]; mk_ = items[0][2][:2] or "M"; s = ""
    if a == 0: s += rect(14, 56, 212, 150, c + "10", "none", r) + person(120, 84, 1.7, c, "polo", mk_)
    elif a == 1: s += rect(14, 56, 212, 150, SOFT, "none", r) + person(84, 90, 1.4, c, "tee", mk_) + person(156, 90, 1.4, INK, "tee", mk_)
    elif a == 2: s += rect(14, 56, 212, 150, c + "10", "none", r) + person(120, 88, 1.6, c, "cap", mk_)
    elif a == 3: s += rect(14, 56, 212, 150, SOFT, "none", r) + person(120, 84, 1.7, c, "jacket", mk_)
    else: s += rect(14, 56, 212, 150, c + "10", "none", r) + "".join(person(60 + i * 60, 100, 1.1, [c, INK, c][i], "apron" if i == 1 else "tee", mk_) for i in range(3))
    return s + t(14, 222, n, 12, INK, "khand") + t(14, 236, d, 7, MUTE)
PK.BODIES["wear"] = b_wear
PK.LABELS["wear"] = ["Polo On Person", "Tee On Two People", "Cap And Tee", "Zip Jacket On Person", "Crew Of Three"]

# ---------- categories: name, app header, sub, pic, accent, abbr, decisions ----------
# decision: key, group, title, [(name, desc, value) x5]
def D(key, group, cat, *items): return (key, group, cat, [tuple(i.split("|")) for i in items])
CATS = {
 "upkeep": ("Up Keep", "Smart Upkeep", "Member App", "house", JUNGLE, "uk", [
  D("tier", "Plans", "Plan Tier Cards", "Essentials|Core yearly visits|Plan", "Plus|More visits and checks|Plan", "Complete|Whole home care|Plan", "Compare Plans|Side by side|Open", "Membership Starting at $99/Month|Pick a plan|Price"),
  D("wait", "Plans", "Waitlist Card", "Join The Waitlist|Your area opens soon|Soon", "Your Zip Code|Example 60614|Field", "Notify Me|One email when open|Email", "Friends Nearby|Share the waitlist|Share", "Spots Left|Example 40|Count"),
  D("appl", "Home Record", "Appliances First", "Water Heater|Example 2019 model|Added", "Furnace|Example 2017 model|Added", "Dishwasher|Example 2021 model|Added", "Fridge|Add a photo|To Add", "Washer|Add a photo|To Add"),
  D("warr", "Home Record", "Warranty List", "Roof Warranty|Ends 2031|Active", "Furnace Warranty|Ends 2027|Active", "Window Warranty|Ends 2029|Active", "Water Heater|Ends 2026|Ending", "Garage Door|No warranty|None"),
  D("visit", "Visits", "Visit Summary", "Fall Visit Done|Your Licensed Tech checked 12 items|Done", "Gutters Cleared|Front and back|Done", "Filter Changed|Furnace|Done", "Caulk Check|Tub needs touch-up|Note", "Next Visit|Example Jan 12|Booked"),
  D("pause", "Plans", "Pause Plan", "Pause Membership|Up to two months|Pause", "Pick A Month|Example December|Month", "Keep Records|Your home record stays|Kept", "Resume Date|Example Feb 1|Date", "Talk To Us|Questions first|Help"),
  D("form", "Booking", "Form Warnings", "Check This Field|Zip code looks short|Fix", "Home Size|Example 2,400 sq ft|Field", "Year Built|Example 1998|Field", "Auto-Fill Then Confirm|We fill, you check|Confirm", "Looks Good|Ready to book|Next"),
  D("tech", "Visits", "Your Licensed Tech Card", "Your Licensed Tech|Example: Sam R.|License On File", "License Checked|State license|Checked", "Arrives|Example 9 to 11 AM|Window", "Message|Ask before the visit|Chat", "Past Visits|Example 3|Count"),
  D("lawn", "Add-Ons", "Lawn Add-On", "Lawn Mowing|Weekly in season|Add-On", "Edging|Every visit|Included", "Leaf Pickup|Fall only|Add-On", "Ask For A Quote|Your Licensed Tech measures|Quote", "Skip A Week|Tap to skip|Skip"),
  D("wear", "Field Brand", "Uniform On People", "Lagoon Polo|Your Licensed Tech on visits|SU", "Crew Tee|Two-person visits|SU", "Cap And Tee|Yard work days|SU", "Zip Jacket|Winter visits|SU", "Full Crew|Big job days|SU"),
 ]),
 "prop": ("Prop", "Prop", "Rentals · Example", "house", LAGOON, "pr", [
  D("close", "Close-Out", "Move-Out Close-Out", "Mellow Wood Close-Out|Example unit|Open", "Final Walk|Photos needed|To Do", "Deposit Return|Example due Oct 30|Due", "Keys Back|Two of two|Done", "Utilities Off|Call made|Done"),
  D("lease", "Leases", "Lease Renewal Ask", "Renew Lease|Wickfield example|Ask", "Twelve Months|Same terms|Option", "Six Months|Short term|Option", "Rent Change|Example none|Note", "Reply By|Example Nov 1|Date"),
  D("req", "Tenants", "Repair Request", "Leaky Faucet|Kitchen, example|New", "Photo Added|One photo|Photo", "Urgency|Not urgent|Low", "Vendor|Example plumber|Pick", "Tenant Told|Text sent|Sent"),
  D("task", "Tasks", "Open Tasks", "Smoke Detectors|Test all units|Due", "Gutter Clean|Fall|Due", "Insurance Renewal|Example Dec|Soon", "Tax Bill|Example Nov|Soon", "Filter Swap|Every unit|Done"),
  D("rent", "Money", "Rent Status", "October Rent|All example units|Paid", "Unit A|Example|Paid", "Unit B|Example|Paid", "Late Fees|None|Zero", "Next Due|Nov 1|Date"),
  D("photo", "Close-Out", "Walkthrough Photos", "Living Room|Four photos|Done", "Kitchen|Six photos|Done", "Bath|Two photos|To Do", "Bedroom|Three photos|To Do", "Garage|One photo|To Do"),
  D("vend", "Tenants", "Vendor List", "Example Plumbing|Fast replies|Plumber", "Example Electric|Licensed|Electric", "Example Lawn|Weekly|Lawn", "Example Locks|Same day|Locks", "Example Clean|Turnover|Clean"),
  D("hand", "Tasks", "Portfolio Handoffs", "Sent To Portfolio|Rent totals|Sent", "Tax Pack|Example receipts|Queued", "Insurance Docs|Example|Queued", "Loan Statement|Example|Asked", "Done List|This week|Open"),
  D("rem", "Leases", "Deadline Reminder", "Lease Ends Soon|Example 45 days|Soon", "Notice Due|Example Nov 15|Date", "Tenant Reply|Waiting|Wait", "Draft Letter|Ready to review|Draft", "Calendar|Add the date|Add"),
  D("card", "Money", "Property Card", "Mellow Wood|Example duplex|2 Units", "Wickfield|Example house|1 Unit", "Occupancy|Example full|Full", "Open Items|Example 3|Count", "Next Event|Close-out|Next"),
 ]),
 "construction": ("Construction", "Home Guide", "Owner Guide · Example", "house", TERRA, "cn", [
  D("warr", "Home Guide", "Warranty Cards With Dates", "Roof|Ends 2036, example|Active", "Windows|Ends 2031|Active", "Furnace|Ends 2030|Active", "Walls|Great Lakes Walls, example|Check", "Paint|Ends 2027|Active"),
  D("shut", "Home Guide", "Shutoff List", "Water Main|Basement, north wall|Room", "Gas|Utility room|Room", "Power Panel|Garage|Room", "Outdoor Water|Mud room|Room", "Sump Pump|Basement|Room"),
  D("walk", "Site Walk", "Site Walk Items", "Trim Gap|Upstairs hall|Open", "Paint Touch-Up|Kitchen|Open", "Door Adjust|Primary bath|Open", "Grade Check|Back yard|Done", "Caulk|Laundry|Done"),
  D("bid", "Bids", "Bid Compare", "Example Bid A|Drywall|Lower", "Example Bid B|Drywall|Middle", "Example Bid C|Drywall|Higher", "Due Date|Nov 5|Due", "Pick One|Owner call|Pick"),
  D("fin", "Finish Questions", "Finish Question Card", "Kitchen Hardware|Brass or black|Ask", "Skip|No reason needed|Skip", "Paint Sheen|Satin or eggshell|Ask", "Grout Color|Warm gray|Ask", "Done|Send answers|Send"),
  D("sched", "Schedule", "Build Schedule", "Framing|Done|Done", "Mechanicals|This week|Now", "Drywall|Next week|Next", "Trim|Example Nov|Later", "Walkthrough|Example Dec|Later"),
  D("co", "Bids", "Change Order", "Change Order 4|Add a pantry shelf|New", "Reason|Owner ask|Note", "Days Added|Zero|Zero", "Approve|Owner signs|Sign", "History|Three before|List"),
  D("trade", "Site Walk", "Trade Directory", "Example Framing|Crew lead|Framing", "Example Electric|Licensed|Electric", "Example Plumbing|Licensed|Plumbing", "Example HVAC|Licensed|HVAC", "Example Paint|Crew|Paint"),
  D("hand", "Home Guide", "Owner Handoff", "Welcome Home|Your guide is ready|Ready", "Manuals|Example 14|Files", "Paint Colors|Example 6|List", "Warranty Cards|Example 9|List", "Call Us|Questions|Help"),
  D("wear", "Field Brand", "Crew Shirts On People", "Terracotta Polo|Site lead|MW", "Crew Tee|Two on site|MW", "Cap And Tee|Summer days|MW", "Zip Jacket|Cold mornings|MW", "Full Crew|Walkthrough day|MW"),
 ]),
 "scout": ("Scout", "Scout", "Shorts · Example", "page", TERRA, "sc", [
  D("abc", "Packaging", "Thumbnail A-B-C Test", "Version A|Bold text|A", "Version B|Face first|B", "Version C|Before and after|C", "Winner|After 48 hours|Pick", "Next Test|Example|Next"),
  D("slot", "Timing", "Publish Slot", "Slot A|7 PM ICT|Test", "Slot B|9 AM ICT|Test", "Slot C|Noon ICT|Test", "Views Early|Example 1.2K|Stat", "Pick Slot|After two weeks|Pick"),
  D("idea", "Ideas", "Short Ideas Board", "Framing In A Day|Time-lapse|Idea", "Flat Fee Explained|Talk to camera|Idea", "Before And After|Kitchen|Idea", "Site Walk Tips|Owner advice|Idea", "Tool Of The Week|Quick|Idea"),
  D("stat", "Channel", "Channel Stats", "Subscribers|Example 1,430|Count", "Shorts|23 posted|Count", "Avg Views|Example 900|Avg", "Best Short|Example|Top", "This Week|Up a little|Trend"),
  D("edit", "Ideas", "Edit Request", "Send An Edit|Max records, Scout cuts|Ask", "Raw Clip|Upload|Step", "Cut|Scout trims|Step", "Text|Add captions|Step", "Post|Slot A|Step"),
  D("title", "Packaging", "Title Style", "How We Frame A Wall|Plain|Style", "Watch A Wall Go Up|Action|Style", "Framing, Fast|Short|Style", "One Day Of Framing|Time|Style", "Wall Framing 101|Lesson|Style"),
  D("plan", "Timing", "30-Day Plan", "Week One|Four Shorts|Plan", "Week Two|Four Shorts|Plan", "Week Three|Four Shorts|Plan", "Week Four|Three Shorts|Plan", "Review|Day 30|Review"),
  D("desc", "Packaging", "Description Template", "Hook Line|One sentence|Line", "What You See|Two lines|Block", "Links|Site and blog|Block", "Tags|Five tags|Block", "Call To Action|Subscribe|Line"),
  D("open", "Ideas", "Opening Frame", "Finished Room|Show the end|Frame", "Bare Studs|Show the start|Frame", "Max On Camera|Face first|Frame", "Big Text|Question first|Frame", "Tool Close-Up|Detail|Frame"),
  D("rep", "Channel", "Weekly Report", "Views|Example 21K|Stat", "Watch Time|Example 140 hrs|Stat", "New Subs|Example 60|Stat", "Top Short|Example|Top", "Next Step|Post Thursday|Next"),
 ]),
 "wellnest": ("WellNest", "WellNest", "Retreats · Example", "cottage", JUNGLE, "wn", [
  D("soon", "Launch", "Coming Soon Page", "Coming Soon|Retreats near the lake|Soon", "Join The List|One email at launch|Join", "First Dates|Example spring|Dates", "Our Space|Photos soon|Photos", "Questions|Write to us|Help"),
  D("svc", "Services", "Service Cards", "Morning Yoga|60 min|Class", "Sound Bath|45 min|Class", "Massage|60 min|Service", "Nature Walk|90 min|Class", "Stay|Weekend|Stay"),
  D("book", "Booking", "Booking Flow", "Pick A Date|Example May 3|Step", "Pick A Room|Garden room|Step", "Add Classes|Two picked|Step", "Your Details|Name and email|Step", "Confirm|Review and book|Step"),
  D("sched", "Services", "Retreat Schedule", "7 AM Yoga|Lawn|Class", "9 AM Breakfast|Main house|Meal", "11 AM Walk|Trail|Class", "3 PM Free Time|Rest|Free", "7 PM Sound Bath|Studio|Class"),
  D("guest", "Booking", "Guest Welcome", "Welcome Note|Your stay starts Friday|Note", "What To Bring|Layers and shoes|List", "Arrival|Example 3 PM|Time", "Parking|By the barn|Info", "House Rules|Quiet after 10|Info"),
  D("ig", "Social", "Instagram Grid", "Lake Morning|Photo post|Post", "Class Clip|Video|Post", "Quote Card|Text|Post", "Room Tour|Carousel|Post", "Coming Soon|Story|Post"),
  D("att", "Launch", "Follow-Up Checklist", "Attorney Name|Example follow-up|Draft", "Business Filing|Example|Check", "Insurance|Example|Check", "Domain|Example|Done", "Logo|Picked|Done"),
  D("rooms", "Services", "Room Cards", "Garden Room|Queen bed|Room", "Lake Room|King bed|Room", "Loft|Two twins|Room", "Cabin|Private|Room", "Shared Bath|Hall|Note"),
  D("faq", "Launch", "FAQ Layout", "What Is Included|Meals and classes|Q", "Can I Cancel|Example policy|Q", "Is It For Beginners|Yes|Q", "Where Is It|Example lake|Q", "How Do I Book|Online|Q"),
  D("wear", "Brand", "Staff Wear On People", "Jungle Polo|Front desk|WN", "Class Tee|Two teachers|WN", "Cap And Tee|Trail guide|WN", "Zip Jacket|Cool mornings|WN", "Full Staff|Opening day|WN"),
 ]),
 "blueprint": ("Blueprint", "Blueprint", "Weberman Residence · Example", "plan", LAGOON, "bp", [
  D("queue", "Decisions", "Decision Queue", "Kitchen Island|Size and seats|Open", "Stair Rail|Wood or steel|Open", "Fireplace|Gas or wood|Open", "Mudroom Bench|Built-in|Open", "Pantry Door|Pocket or swing|Open"),
  D("ctr", "Kitchen", "Counter Pick", "Quartz|White, example|Pick", "Soapstone|Dark|Pick", "Butcher Block|Warm|Pick", "Edge|Eased|Detail", "Backsplash|Tile|Detail"),
  D("floor", "Rooms", "Floor Pick", "White Oak|Wide plank|Pick", "Walnut|Narrow|Pick", "Tile|Mud room|Pick", "Finish|Matte|Detail", "Stairs|Match floor|Detail"),
  D("light", "Rooms", "Lighting Plan", "Pendants|Over island|Kitchen", "Cans|Low glare|All", "Sconces|Hall|Hall", "Dimmers|Every room|All", "Exterior|Dark sky|Outside"),
  D("bath", "Rooms", "Primary Bath", "Walk-In Shower|No curb|Pick", "Tub|Freestanding|Pick", "Double Vanity|Floating|Pick", "Heated Floor|Yes|Detail", "Window|Frosted|Detail"),
  D("energy", "Systems", "Energy Choices", "Heat Pump|All electric|Pick", "Solar Ready|Roof prep|Pick", "Spray Foam|Attic|Pick", "Triple Pane|North side|Pick", "EV Charger|Garage|Pick"),
  D("out", "Outdoor", "Outdoor Space", "Screened Porch|Back|Pick", "Patio|Stone|Pick", "Fire Pit|Side yard|Pick", "Garden Beds|South|Pick", "Pool Later|Plan space|Later"),
  D("store", "Rooms", "Storage", "Mudroom Lockers|Four|Pick", "Pantry Shelves|Walk-in|Pick", "Garage Wall|Hooks|Pick", "Closet System|Primary|Pick", "Attic|Pull-down stair|Pick"),
  D("draw", "Decisions", "Drawing Set", "Floor Plan|Rev 4|Sheet", "Elevations|Rev 3|Sheet", "Sections|Rev 2|Sheet", "Electrical|Rev 1|Sheet", "Site Plan|Rev 2|Sheet"),
  D("chg", "Decisions", "Change Notice", "Window Moved|Kitchen, east|New", "Who Asked|Max|Note", "Cost Effect|Example none|Note", "Drawing|Rev 5|Sheet", "OK It|Approve|Ask"),
 ]),
 "thai": ("Thai", "Thai Study", "Daily Practice · Example", "page", SAFFRON, "th", [
  D("tip", "Daily", "Daily Tip Card", "Today's Tip|Ao ... Duay pattern|Tip", "Example One|I want rice too|Ex", "Example Two|Coffee too|Ex", "Say It|Tap to hear|Audio", "Saved|Add to review|Save"),
  D("known", "Progress", "Known Words", "Known|32 words|Count", "Active|94 words|Count", "Patterns|13 tips|Count", "New Today|Example 5|Count", "Streak|Example 6 days|Count"),
  D("quiz", "Quiz", "Quiz Answer Style", "Pick One|Four choices|Style", "Type It|Write the word|Style", "Hear It|Listen and pick|Style", "Match|Pairs|Style", "Speak|Say it out loud|Style"),
  D("rev", "Review", "Review Queue", "Due Now|Example 12|Due", "Tomorrow|Example 20|Due", "Hard Words|Example 6|List", "Bring Back|Old words|List", "Done Today|Example 30|Done"),
  D("word", "Quiz", "Word Card", "Rice|Khao, example|Noun", "Water|Naam|Noun", "Eat|Gin|Verb", "Go|Pai|Verb", "Hot|Ron|Adj"),
  D("tone", "Review", "Tone Hints", "Mid Tone|Flat|Tone", "Low Tone|Down a bit|Tone", "Falling|Up then down|Tone", "High|Up|Tone", "Rising|Low then up|Tone"),
  D("home", "Daily", "Home Screen", "Start Practice|10 min|Start", "Daily Tip|New|Tip", "Review|12 due|Due", "Progress|Week view|Stat", "Settings|Light only|Gear"),
  D("aud", "Quiz", "Audio Controls", "Play|Normal speed|Play", "Slow|Half speed|Slow", "Repeat|Three times|Loop", "Record|Your voice|Rec", "Compare|You and teacher|Check"),
  D("week", "Progress", "Week Chart", "Monday|Example 20 min|Day", "Tuesday|Example 15 min|Day", "Wednesday|Example 25 min|Day", "Thursday|Example 10 min|Day", "Friday|Example 20 min|Day"),
  D("phr", "Daily", "Phrase Packs", "Market|Prices and counts|Pack", "Taxi|Directions|Pack", "Cafe|Orders|Pack", "Polite|Please and thanks|Pack", "Numbers|One to 100|Pack"),
 ]),
 "blog": ("Blog", "Blog", "maxweberman.com · Drafts", "page", TERRA, "bl", [
  D("flat", "Topics", "Flat Fee Post", "Flat Fee Vs Percentage|Which is fairer|Draft", "What It Covers|Plain list|Section", "Example Math|Simple numbers|Section", "When It Fits|Custom homes|Section", "Ask Us|Contact|End"),
  D("bids", "Topics", "Real Bids Post", "Real Sub Bids|Vs padded estimates|Draft", "Why It Matters|Trust|Section", "How We Show Bids|Open book|Section", "Red Flags|Three signs|Section", "Next Step|Ask for bids|End"),
  D("co", "Topics", "Change Orders Post", "How Change Orders Work|Plain steps|Draft", "Step One|Ask in writing|Step", "Step Two|Price it|Step", "Step Three|Sign it|Step", "Step Four|Track it|Step"),
  D("pick", "Topics", "Pick A Builder Post", "How To Pick A Builder|Six questions|Draft", "Licensed|Check it|Q", "References|Call three|Q", "Pricing|Flat or percent|Q", "Warranty|In writing|Q"),
  D("plan", "Topics", "First Five Decisions", "Planning A Custom Home|First five decisions|Draft", "Lot|Where|Step", "Budget|How much|Step", "Size|How big|Step", "Team|Who builds|Step"),
  D("voice", "Style", "I Vs We", "I Write It|Personal|Voice", "We Write It|Company|Voice", "Mix|I for stories|Voice", "Example Line|We price flat|Line", "Example Line|I price flat|Line"),
  D("case", "Style", "Heading Case", "Title Case Headings|Like This One|Case", "Sentence Case|Like this one|Case", "Caps Label|Small caps tag|Case", "Example H2|How Draws Work|Case", "Example H3|What to sign|Case"),
  D("photo", "Style", "Photo-Led Vs Headline-First", "Photo First|Big site photo|Style", "Headline First|Words up top|Style", "Split|Half and half|Style", "Caption|Short line|Detail", "Credit|Example|Detail"),
  D("steps", "Style", "Numbered Steps Block", "Numbered Steps|One idea each|Block", "Check Box Steps|Tick as you go|Block", "Short Lines|Under ten words|Block", "Tip Box|One tip|Block", "Summary|Three lines|Block"),
  D("cta", "Site", "Post Ending", "Talk To Max|Book a call|End", "Read Next|Related post|End", "Get The Guide|Example PDF|End", "Share|Send to a friend|End", "Subscribe|One email a month|End"),
 ]),
 "portfolio": ("Portfolio", "Portfolio", "Finance Review · Example", "chart", JUNGLE, "pf", [
  D("mix", "Allocation", "Target Mix", "Stocks|Example 60%|Mix", "Bonds|Example 20%|Mix", "Cash|Example 10%|Mix", "Real Estate|Example 10%|Mix", "Drift|Example 2%|Note"),
  D("basis", "Taxes", "Cost Basis Ask", "Cost Basis Needed|Example lots|Ask", "Upload|Broker file|Step", "Check|Totals match|Step", "Done|Sent to CPA|Step", "Help|Ask Portfolio|Help"),
  D("cpa", "Taxes", "CPA Reply Tracker", "CPA Reply|Waiting, example|Wait", "Asked|Oct 10|Date", "Docs Sent|Five|Count", "Next Nudge|Oct 17|Date", "Notes|Example|Note"),
  D("spend", "Spending", "Spending Categories", "Home|Example|Cat", "Travel|Example|Cat", "Food|Example|Cat", "Kids|Example|Cat", "Other|Example|Cat"),
  D("due", "Spending", "Bills Due", "Card Payment Due|Example today|Due", "Utilities|Example Oct 20|Due", "Insurance|Example Nov 1|Due", "Autopay|On|Status", "Paid This Month|Example 6|Count"),
  D("prices", "Allocation", "Price Refresh", "Stocks|Last close, example|Price", "BTC|Live, example|Price", "Updated|Example 7:24 PM|Time", "Market Opens|8:30 PM ICT|Time", "Refresh|Tap|Action"),
  D("eq", "Decisions", "Equity Questions", "Vesting|Example schedule|Q", "Sell Or Hold|Open|Q", "Tax Effect|Ask CPA|Q", "Lockup|Example|Q", "Decide By|Example Dec|Date"),
  D("month", "Spending", "Monthly Summary", "In|Example|Total", "Out|Example|Total", "Saved|Example|Total", "Top Category|Home|Cat", "Vs Last Month|Example|Trend"),
  D("lane", "Decisions", "Lane Status", "Portfolio|Ready|Lane", "Spending|Ready|Lane", "Finance Review|Ready|Lane", "Tax Pack|Waiting|Lane", "Property|Handoff|Lane"),
  D("goal", "Allocation", "Goal Tracker", "College Fund|Example|Goal", "Emergency Fund|Example|Goal", "Retirement|Example|Goal", "House Fund|Example|Goal", "Travel|Example|Goal"),
 ]),
 "japan-cottage": ("Japan Cottage", "Japan Cottage", "Akiya Search · Example", "cottage", TERRA, "jc", [
  D("list", "Listings", "Listing Card", "Example Farmhouse|Nagano area|Listing", "Example Machiya|Kyoto area|Listing", "Example Cabin|Hokkaido|Listing", "Example Seaside|Chiba|Listing", "Example Village|Gifu|Listing"),
  D("light", "App", "Light Mode Pick", "Light Mode Only|White base|Mode", "Soft Paper|Warm white|Mode", "Bright White|Pure|Mode", "Card Shadows|Soft|Detail", "Lines|Thin|Detail"),
  D("share", "App", "Share Button", "Share Listing|Send a link|Share", "Copy Link|Tap|Action", "Text|Phone|Action", "Email|Mail|Action", "Save First|Then share|Action"),
  D("vote", "Listings", "Vote Card", "Love It|Keep|Vote", "Maybe|Hold|Vote", "Pass|Skip|Vote", "Notes|Why|Note", "Next|Swipe on|Nav"),
  D("area", "Areas", "Area Pick", "Nagano|Mountains|Area", "Kyoto|Old town|Area", "Hokkaido|Snow|Area", "Chiba|Coast|Area", "Gifu|Villages|Area"),
  D("reno", "Plans", "Renovation Plan", "Roof|First|Step", "Bath|Second|Step", "Kitchen|Third|Step", "Garden|Later|Step", "Engawa|Later|Step"),
  D("filt", "Listings", "Filters", "Near Train|Under 2 km|Filter", "Land Size|Example|Filter", "Year Built|Any|Filter", "Needs Work|Light|Filter", "Price|Example|Filter"),
  D("alert", "Listings", "New Listing Alerts", "New Listing|Example Gifu|New", "Price Drop|Example|Drop", "Saved Area|Nagano|Area", "Daily Digest|One email|Mode", "Instant|Push|Mode"),
  D("color", "Plans", "Exterior Color", "Charred Wood|Dark|Color", "White Plaster|Bright|Color", "Natural Cedar|Warm|Color", "Indigo Trim|Accent|Color", "Tile Roof|Gray|Color"),
  D("trip", "Plans", "Visit Trip", "Day One|Fly in|Day", "Day Two|See two houses|Day", "Day Three|Meet agent|Day", "Day Four|Village walk|Day", "Day Five|Fly home|Day"),
 ]),
 "miles": ("Miles", "Miles", "Points · Example", "card", LAGOON, "mi", [
  D("card", "Cards", "New Card Pick", "Example Card A|Travel bonus|Pick", "Example Card B|Cash back|Pick", "Example Card C|Airline|Pick", "Priorities|Your call|Ask", "Fee|Example|Note"),
  D("inv", "Points", "Points Inventory", "Example Points A|Balance needed|Ask", "Example Miles B|Balance needed|Ask", "Example Points C|Balance needed|Ask", "Hotel Points|Balance needed|Ask", "Totals|After balances|Wait"),
  D("priv", "Mom's Apps", "Private Submit", "Private Submit|Only Max sees|Mode", "Public Link|Anyone with link|Mode", "Code Word|Example|Mode", "Who Sees|Max only|Note", "Switch|One tap|Action"),
  D("off", "Offers", "Offer List", "Example Hotel Offer|Ends soon|Offer", "Example Dining|Ends Nov|Offer", "Example Shop|Ends Dec|Offer", "Saved|Example 3|Count", "Used|Example 1|Count"),
  D("xfer", "Points", "Transfer Partners", "Example Airline A|1 to 1|Partner", "Example Airline B|1 to 1|Partner", "Example Hotel|1 to 2|Partner", "Best Use|Example|Note", "Steps|Three|Help"),
  D("bonus", "Cards", "Bonus Tracker", "Spend Goal|Example|Goal", "Spent So Far|Example|Now", "Days Left|Example 40|Days", "On Track|Yes|Status", "Bonus|Example points|Prize"),
  D("trip", "Points", "Trip Plan", "Example Trip|Spring|Trip", "Flights|Points|Plan", "Hotel|Points|Plan", "Points Needed|Example|Count", "Book By|Example|Date"),
  D("alert", "Offers", "Offer Alerts", "Ends Soon|Example 3 days|Soon", "New Offer|Example|New", "Daily Note|One a day|Mode", "Weekly|One a week|Mode", "Off|No alerts|Mode"),
  D("wallet", "Cards", "Card Wallet", "Example Card A|Daily use|Card", "Example Card B|Travel|Card", "Example Card C|Dining|Card", "Example Card D|Backup|Card", "Add Card|Example|Add"),
  D("redeem", "Points", "Redeem Steps", "Pick Trip|Step one|Step", "Check Space|Step two|Step", "Move Points|Step three|Step", "Book|Step four|Step", "Save Proof|Step five|Step"),
 ]),
 "jokes": ("Jokes", "Jokes", "Set Builder · Example", "mic", SAFFRON, "jk", [
  D("prem", "Writing", "New Premise Card", "Example Premise|Contractor dad|Raw", "Example Premise|Thai class|Raw", "Example Premise|Smart home|Raw", "Example Premise|Airport|Raw", "Example Premise|Gym|Raw"),
  D("punch", "Writing", "Punch-Up Board", "Example Bit A|Punched up|Up", "Example Bit B|Punched up|Up", "Example Bit C|Raw|Raw", "Example Bit D|Raw|Raw", "Example Bit E|Raw|Raw"),
  D("set", "Sets", "Set List", "Opener|Example bit|1", "Second|Example bit|2", "Middle|Example bit|3", "Strong|Example bit|4", "Closer|Example bit|5"),
  D("time", "Sets", "Set Timer", "Five Minutes|Open mic|Set", "Seven Minutes|Showcase|Set", "Ten Minutes|Feature|Set", "Warn At|One minute|Note", "Light|Example|Note"),
  D("rate", "Sets", "Bit Ratings", "Killed|Example|Top", "Good|Example|Mid", "Okay|Example|Mid", "Flat|Example|Low", "Cut|Example|Low"),
  D("fresh", "Writing", "Fresh Joke Ideas", "Fresh Idea|4:47 AM, example|New", "Save|Keep it|Action", "Skip|Not funny|Action", "Tag|Topic|Action", "Write Now|Open bit|Action"),
  D("tag", "Library", "Tag Picks", "Family|Example|Tag", "Travel|Example|Tag", "Work|Example|Tag", "Home|Example|Tag", "Food|Example|Tag"),
  D("lib", "Library", "Bit Library", "All Bits|Example 40|Count", "Raw|Example 6|Count", "Punched Up|Example 2|Count", "Stage Ready|Example 10|Count", "Retired|Example 5|Count"),
  D("share", "Library", "Share In Page", "Share Bit|Send a link|Share", "Copy|Tap|Action", "Text|Phone|Action", "Notes|Add a note|Action", "Back|To list|Nav"),
  D("rec", "Sets", "Show Recording", "Example Show|Oct 10|Show", "Laughs|Example|Stat", "Best Bit|Example|Top", "Fix|Example|Note", "Next Show|Example|Date"),
 ]),
 "jane-amex": ("Jane Amex", "Mom's Offers", "Amex Offers · Example", "card", LAGOON, "ja", [
  D("off", "Offers", "Offer Card", "Example Coffee|Save on coffee|Offer", "Example Grocer|Save on food|Offer", "Example Pharmacy|Save on health|Offer", "Example Garden|Save on plants|Offer", "Example Books|Save on books|Offer"),
  D("save", "Offers", "Save Button", "Add To Card|One tap|Save", "Saved|Done|Done", "Undo|Changed mind|Undo", "Remind Me|Later|Later", "Skip|Not for me|Skip"),
  D("ends", "Alerts", "Ends Soon", "Ends Friday|Example coffee|Soon", "Ends Next Week|Example grocer|Soon", "Ends This Month|Example books|Later", "New Today|Example|New", "Used|Example|Done"),
  D("steps", "Help", "Three Plain Steps", "Step One|Find an offer|Step", "Step Two|Tap Add|Step", "Step Three|Shop with the card|Step", "Done|Savings come later|Note", "Help|Call Max|Help"),
  D("greet", "Home", "Greeting", "Good Morning|Example|Hello", "New Offers|Example 4|Count", "Ending Soon|Example 2|Count", "Saved|Example 6|Count", "Help|Call Max|Help"),
  D("cat", "Offers", "Offer Categories", "Food|Example|Cat", "Health|Example|Cat", "Home|Example|Cat", "Travel|Example|Cat", "Gifts|Example|Cat"),
  D("chart", "Home", "Savings Chart", "Saved This Year|Example|Total", "This Month|Example|Total", "Best Offer|Example|Top", "Offers Used|Example 9|Count", "Goal|Example|Goal"),
  D("az", "Offers", "A To Z List", "A To C|Example|Group", "D To H|Example|Group", "I To M|Example|Group", "N To S|Example|Group", "T To Z|Example|Group"),
  D("big", "Help", "Bigger Text Mode", "Big Text|Easier to read|Mode", "Bigger Buttons|Easier to tap|Mode", "High Contrast|Black on white|Mode", "Read Aloud|Speaker|Mode", "Reset|Normal|Mode"),
  D("call", "Help", "Call Max Button", "Call Max|One tap|Call", "Text Max|One tap|Text", "Send Screenshot|One tap|Send", "Hours|Example|Info", "Back|Home|Nav"),
 ]),
 "dashboards": ("Agent Dashboards", "Agent Dashboard", "Team · Example", "chart", LAGOON, "db", [
  D("fresh", "Report Bars", "Fresh Start Bar", "Fresh Start|Ready for Max now|Bar", "Top Three|Example items|List", "Needs From Max|Collapsed|Fold", "Updated|Example 7:25 PM|Time", "Open Apps|Links|Links"),
  D("eve", "Report Bars", "Evening Report", "Evening Report|Today and tomorrow|Bar", "Today|Example 5 items|List", "Tomorrow|Example 3 items|List", "Waiting|Example 2|Count", "Shipped|Example 4|Count"),
  D("wait", "Decisions", "Waiting On Max", "Waiting On Max|Example 3|Count", "Decide|Example item|Ask", "Approve|Example item|Ask", "Reply|Example item|Ask", "Later|Example item|Later"),
  D("decks", "Decks", "Deck Building Page", "Decks Waiting|Example 20|Count", "Finished|Example 9|Count", "Requests|Example 3|Count", "Newest|Example|Top", "Submit Status|In|Status"),
  D("tiles", "Layout", "App Tiles", "Dashboard|Home|App", "Swipe|Decks|App", "Quiz|Questions|App", "Guide|Docs|App", "Settings|Light only|App"),
  D("feed", "Layout", "Team Feed Panel", "Shipped|Example 12|Count", "Handoffs|Example 4|Count", "Reports|Example 15|Count", "Today|Example|Filter", "All|Example|Filter"),
  D("nav", "Layout", "Apps Home Link", "Apps Home|Back to all|Link", "Dashboard|This lane|Link", "Decks|Style Swipe|Link", "Feed|Team|Link", "Help|Docs|Link"),
  D("ptr", "Layout", "Pull To Refresh Cue", "Pull To Refresh|Release to load|Cue", "Updated|Just now|Status", "Loading|Example|Status", "Offline|Try again|Status", "Done|Fresh|Status"),
  D("status", "Decisions", "Status Chips", "Ready|Green|Chip", "Waiting|Saffron|Chip", "Blocked|Terracotta|Chip", "Done|Gray|Chip", "Draft|Outline|Chip"),
  D("icons", "Layout", "Agent Icons", "Upkeep|Example icon|Icon", "Construction|Example icon|Icon", "Blog|Example icon|Icon", "Thai|Example icon|Icon", "Miles|Example icon|Icon"),
 ]),
 "variety": ("Variety", "Style Swipe", "Mixed · Example", "page", SAFFRON, "va", [
  D("btns", "Swipe Controls", "Swipe Buttons", "Pass|Left|Pill", "Hold|Down|Pill", "Love|Up|Pill", "Keep|Right|Pill", "Notes|Tap|Pill"),
  D("lagoon", "Color", "Lagoon And Saffron", "Lagoon Lead|Teal first|Color", "Saffron Pop|Small accent|Color", "Jungle Support|Green|Color", "Terracotta Spark|Rare|Color", "White Base|Always|Color"),
  D("card", "Swipe Controls", "Card Frame", "Rounded Card|Soft|Frame", "Square Card|Sharp|Frame", "Shadow|Light|Frame", "Outline|Thin|Frame", "Full Bleed|Edge to edge|Frame"),
  D("type", "Type", "Headline Feel", "Khand Big|Bold|Type", "Khand Caps|Spaced|Type", "Hind Bold|Calm|Type", "Mixed|Khand plus Hind|Type", "Small Label|Caps|Type"),
  D("prog", "Swipe Controls", "Deck Progress", "Progress Bar|Top|Style", "Dots|Bottom|Style", "Count|12 Of 50|Style", "Ring|Corner|Style", "None|Clean|Style"),
  D("end", "Swipe Controls", "End Screen", "All Done|Submit now|End", "Your Picks|Summary|End", "Share|Send|End", "Next Deck|Start|End", "Back|Home|End"),
  D("icon", "Type", "Icon Style", "Line Icons|Thin|Icon", "Filled Icons|Solid|Icon", "Duotone|Two tone|Icon", "Rounded|Soft|Icon", "Square|Sharp|Icon"),
  D("photo", "Color", "Photo Treatment", "Full Color|Natural|Photo", "Warm Tint|Saffron wash|Photo", "Cool Tint|Lagoon wash|Photo", "Black And White|Plain|Photo", "Framed|White border|Photo"),
  D("notes", "Swipe Controls", "Notes Box", "Notes|Type a note|Box", "Voice Note|Speak|Box", "Quick Tags|Tap|Box", "Skip|No note|Box", "Save|Done|Box"),
  D("space", "Type", "Spacing", "Roomy|Air|Space", "Compact|Tight|Space", "Mixed|Roomy top|Space", "Grid|Even|Space", "Stacked|One column|Space"),
 ]),
}
NAMES_FIX = {}
BODY_PAIRS = [("list", "tiles"), ("detail", "buttons"), ("chart", "list"), ("nav", "type"), ("notice", "detail"),
              ("tiles", "chart"), ("buttons", "notice"), ("type", "nav"), ("list", "detail"), ("tiles", "buttons")]
FINS = list(FIN)

# ---------- upkeep banned-word check ----------
UK_PRICE = "Membership Starting at $99/Month"
UK_BANNED = [r"\bsilver\b", r"\bgold\b", r"\bplatinum\b", r"\bai\b", r"artificial", r"intelligen", r"health score", r"forecast", r"predict",
             r"technician", r"\bbuilt by\b", r"\bby max\b", r"byline", r"weberman", r"\bsmart ?keep\b", r"\.ai\b"]
def visible(o): return " ".join([o["label"], o["desc"]] + re.findall(r">([^<]*)</text>", o["visual"]["svg"]))
def upkeep_bad(o):
    txt = visible(o).replace("&amp;", "&"); low = txt.lower().replace(UK_PRICE.lower(), "")
    bad = [b for b in UK_BANNED if re.search(b, low)]
    if "$" in low: bad.append("$ outside price line")
    if re.search(r"\btechs?\b", low.replace("your licensed tech", "")): bad.append("tech wording")
    return bad
def emoji(s): return re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", s)

class Bank(Deck):
    def __init__(s, slug, app, sub, pk, c, prefix):
        s.slug = slug; super().__init__(slug, prefix, app, sub, pk, c)
    def draw(s, body, a, items, fin):
        svg = super().draw(body, a, items, fin)
        if s.slug == "upkeep": svg = re.sub(r"<text[^>]*>MAX WEBERMAN</text>", "", svg.replace(foot(), ""))   # no byline on Up Keep
        return svg

def feed_decision(slug, name):
    """One extra decision made from the newest team-feed line for this category (Title Case chunks)."""
    try: lines = open(FEED, encoding="utf-8").read().splitlines()
    except OSError: return None
    keys = {"dashboards": "dashboard", "variety": "branding", "jane-amex": "mom", "japan-cottage": "japan cottage"}
    k = keys.get(slug, name.lower())
    for ln_ in reversed(lines):
        if k in ln_.lower():
            body = re.sub(r"https?://\S+|commit \w+|\d{1,2}:\d\d|ICT|·", " ", ln_)
            chunks = [re.sub(r"[^A-Za-z ]", "", c).strip() for c in re.split(r"[,;()]", body)]
            chunks = [" ".join(w.capitalize() for w in c.split()) for c in chunks if 2 <= len(c.split()) <= 4 and len(c) <= 24]
            chunks = list(dict.fromkeys(chunks))[:5]
            if len(chunks) == 5:
                return ("feed", "From The Feed", "Latest Open Items", [(c, "From today's team feed", "Open") for c in chunks])
    return None

def candidates(slug):
    """Endless, deterministic stream of 5-pair topics; round r changes finish and layout pairing so ids are new."""
    name, app, sub, pk, c, ab, decs = CATS[slug]
    fd = feed_decision(slug, name)
    r = 0
    while r < 40:
        for i, (key, group, cat, items) in enumerate(([fd] if fd else []) + decs):
            bodies = ("wear", "wear") if key == "wear" else BODY_PAIRS[(i + r) % len(BODY_PAIRS)]
            for j, body in enumerate(bodies):
                fin = FINS[(i + j + r * 2) % len(FINS)]
                tag_ = f"{key}{'ab'[j]}{r}" + (f"f{TODAY.replace('-', '')}" if key == "feed" else "")
                B = Bank(slug, app, sub, pk, c, f"bk{ab}_")
                B.topic(tag_, group, cat, body, items, fin)
                yield B.pairs
        r += 1

def load(p, d): return json.load(open(p)) if os.path.exists(p) else d
def shown_ids():
    ids = set(load("shown_options.json", {"options": {}})["options"])
    for fp in glob.glob("decks/*.json"):
        for pp in load(fp, {}).get("pairs", []):
            for k in "AB": ids.add((pp.get("option" + k) or {}).get("id"))
    return ids

def main(refill):
    os.makedirs("banks", exist_ok=True)
    used = load("banks/used.json", {"pairs": [], "options": []})
    used_pairs, used_opts = set(used.get("pairs", [])), set(used.get("options", []))
    reserved = load("banks/bank_ids.json", {"options": {}})
    res = reserved.setdefault("options", {})
    shown = shown_ids(); cutoff = (dt.date.today() - dt.timedelta(days=MAX_AGE)).isoformat()
    index, report = {}, {}
    for slug, spec in CATS.items():
        path = f"banks/{slug}.json"; bank = load(path, {"pairs": []})
        kept, dropped, retired = [], 0, 0
        for p in bank["pairs"]:
            oids = {p["optionA"]["id"], p["optionB"]["id"]}
            if p["id"] in used_pairs or oids & used_opts or oids & shown: dropped += 1
            elif p.get("generated", TODAY) < cutoff: retired += 1
            else: kept.append(p)
        have = {p["option" + k]["id"] for p in kept for k in "AB"}
        nxt = max([int(p["id"].rsplit("-", 1)[1]) for p in bank["pairs"]] + [0]) + 1; added = 0
        for chunk in candidates(slug):
            if len(kept) >= TARGET: break
            for p in chunk:
                if len(kept) >= TARGET: break
                ids = [p["optionA"]["id"], p["optionB"]["id"]]
                if any(i in shown or i in res or i in have for i in ids): continue  # never reuse a reserved/retired id
                if slug == "upkeep":
                    for k in "AB":
                        bad = upkeep_bad(p["option" + k]); assert not bad, (p["option" + k]["id"], bad)
                p.update(id=f"{slug}-bank-{nxt:03d}", repeat=False, share=True, notes=True, generated=TODAY); nxt += 1
                for k in "AB":
                    o = p["option" + k]; o["share"] = True; o["tags"] = list(dict.fromkeys(o["tags"]))
                kept.append(p); have.update(ids); added += 1
        assert len(kept) == TARGET, (slug, len(kept))
        for p in kept:
            for k in "AB":
                o = p["option" + k]; assert not emoji(json.dumps(o, ensure_ascii=False)), o["id"]
                if slug == "upkeep": assert not upkeep_bad(o), (o["id"], upkeep_bad(o))
                res.setdefault(o["id"], slug)
        ids = [p["option" + k]["id"] for p in kept for k in "AB"]; assert len(ids) == len(set(ids))
        changed = added or dropped or retired
        groups = {}
        for p in kept: groups[p["group"]] = groups.get(p["group"], 0) + 1
        out = {"slug": slug, "name": spec[0], "version": 4, "owner": "Max Weberman", "format": "pairs", "status": "bank",
               "english_only": True, "light_only": True, "example_data_only": True, "count": len(kept), "max_age_days": MAX_AGE,
               "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds") if changed or "generated_at" not in bank else bank["generated_at"],
               "groups": groups, "sources": {"team_feed": FEED, "builder": "tools/build_banks.py"}, "pairs": kept}
        json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
        index[slug] = {"name": spec[0], "count": len(kept)}; report[slug] = (len(kept), added, dropped, retired)
    reserved["note"] = "Option ids reserved by banks/. Not counted as shown; never reused. Move to shown_options.json only when served."
    reserved["options"] = dict(sorted(res.items())); reserved["count"] = len(res)
    json.dump(reserved, open("banks/bank_ids.json", "w"), indent=1)
    json.dump(index, open("banks/index.json", "w"), indent=1)
    if not os.path.exists("banks/used.json"):
        json.dump({"note": "Add served/shown bank pair ids (pairs) or option ids (options); --refill drops them.", "pairs": [], "options": []}, open("banks/used.json", "w"), indent=1)
    for k, v in report.items(): print(f"{k:14s} count={v[0]} added={v[1]} dropped={v[2]} retired={v[3]}")
    try:
        from write_sizes import main as write_sizes
        write_sizes()
    except Exception as e:
        print("write_sizes:", e)

if __name__ == "__main__":
    main("--refill" in sys.argv)
