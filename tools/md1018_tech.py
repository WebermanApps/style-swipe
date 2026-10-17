"""UpKeep Tech App decks (report 1a): walkthrough full list + step screens, check-in + before photos, moisture readings + walk report.
Settled and not re-asked: full list first then step by step with a way back (Walkthrough And Check-In 01 note), proposed order + skip, a Take Before Photo
button blocks start, slide to check in, check out with the report, dry/watch/wet live as you type, timer in the header, full-screen preview, chips by area,
info-only fading alert, map-first Today, checkbox + photo, type a number. Queued decks' asks (Walk Steps, Check-In And Home Map; Today, Directions And
Checklist Order; Tech App Day Flow) are not repeated."""
from md1018_kit import *
TA = "UpKeep Tech App"
def steps_list(done=2, times=False, groups=False, start="bottom"):
    rows = [("Before photo, furnace room", "2 min"), ("Furnace filter", "5 min"), ("Water heater", "6 min"), ("Moisture scan, basement", "8 min"), ("Sump pit", "4 min"), ("Dryer vent", "5 min")]
    b = [("h", "Full List", 15)]
    if start == "top": b.append(("btn", "Start Walk", "fill", TERRA))
    if groups:
        b += [("checks", [r[0] for r in rows[done:5]], JUNGLE, 0), ("lbl", "DONE (2)", JUNGLE), ("checks", [r[0] for r in rows[:done]], JUNGLE, done)]
    else:
        b.append(("checks", [r[0] + ("  ·  " + r[1] if times else "") for r in rows[:5]], JUNGLE, done))
    if start == "bottom": b.append(("btn", "Start Walk", "fill", TERRA))
    return b
def step_screen(head=None, photo_first=False, extra=()):
    b = list(head or [("bar", .33, TERRA, "Step 4 of 12", "Basement")])
    ins = [("h", "Moisture Scan, Basement", 13), ("p", "Hold the meter flat on the wall 30 cm above the floor, three spots.")]
    ph = [("photo", 70, LAGOON, "room", "Before photo")]
    b += (ph + ins) if photo_first else (ins + ph)
    return b + list(extra)
def T1():
    pairs, P = make("md18tw_", "UpKeep"); L = TA + " · Walk"
    P("Walkthrough", TA + " Walkthrough", "Step progress", "on each step screen should progress show as a thin bar with Step 4 of 12 or as a swipe strip of small step cards?",
      ("bar", "Thin Bar, Step 4 Of 12", "One slim bar and a count over the step.", "calm", S(L, step_screen(), ("Thin bar with a count", "Basement area named on the right"))),
      ("strip", "Swipe Strip Of Step Cards", "A small carousel of step cards, this one lit.", "playful", S(L, step_screen([("carousel", [("3  Water heater", "Done", JUNGLE), ("4  Moisture scan", "Now", TERRA), ("5  Sump pit", "Next", LAGOON)], 96, 40, False)]), ("Step cards in a swipe strip", "Done, now and next at a glance"))))
    P("Walkthrough", TA + " Walkthrough", "Next step", "should the tech move on with a big Next Step button or by swiping the step card sideways like a carousel?",
      ("btn", "Big Next Step Button", "A full-width button under the step.", "practical", S(L, step_screen(extra=[("btn", "Next Step", "fill", INK)]), ("One clear button", "No accidental swipes"))),
      ("swipe", "Swipe The Step Card", "Swipe left for the next step, right to go back.", "playful", S(L, [("carousel", [("Step 4", "Moisture scan, basement", TERRA), ("Step 5", "Sump pit", LAGOON)], 170, 150, True, False, 0)], ("Steps sit in a carousel", "Swipe left for the next one"))))
    P("Walkthrough", TA + " Walkthrough", "Step how-to", "should each step show a short line with a small drawn diagram or a short looping clip of a tech doing it?",
      ("diagram", "Line Plus Drawn Diagram", "One sentence and a simple drawing.", "calm", S(L, [("h", "Furnace Filter", 13), ("p", "Slide the old filter out, arrow on the new one points to the blower."), ("photo", 80, JUNGLE, "room")], ("Drawn diagram", "Loads fast, no sound"))),
      ("clip", "Short Looping Clip", "A five-second silent clip shows the move.", "playful", S(L, [("h", "Furnace Filter", 13), ("p", "Slide the old filter out, arrow on the new one points to the blower."), ("photo", 80, LAGOON, "person", "Clip loops, muted")], ("Short silent clip", "Shows the real move"))))
    P("Full List", TA + " Full List", "Step times", "should each row in the full list show its expected minutes or only the step name?",
      ("times", "Show Minutes Per Step", "Each row ends with about how long it takes.", "practical", S(L, steps_list(2, True), ("Minutes on every row", "About 30 minutes in total"))),
      ("names", "Step Names Only", "A clean list of steps, no times.", "calm", S(L, steps_list(2, False), ("Names only", "Timer in the header keeps time"))))
    P("Full List", TA + " Full List", "Tools for the walk", "should the full list open with a short row of tools and parts to grab first or go straight to the steps?",
      ("tools", "Tools Row First", "Meter, filter and ladder chips above the steps.", "practical", S(L, [("h", "Full List", 15), ("lbl", "GRAB BEFORE YOU START"), ("tags", ["Moisture meter", "Filter 16x25", "Ladder", "Shoe covers"]), ("checks", ["Before photo, furnace room", "Furnace filter", "Water heater"], JUNGLE, 0), ("btn", "Start Walk", "fill", TERRA)], ("Tools and parts first", "From the job's bring list"))),
      ("steps", "Straight To The Steps", "The list starts with step one.", "calm", S(L, steps_list(0), ("Steps only", "Bring list stays on the job card"))))
    P("Full List", TA + " Full List", "Finished steps", "in the full list should done steps stay in place with a green tick or drop into a Done group at the bottom?",
      ("place", "Stay In Place, Ticked", "The order never changes; done rows go grey.", "calm", S(L, steps_list(2), ("Same order all visit", "Done rows greyed with a tick"))),
      ("group", "Done Group At The Bottom", "What's left sits on top; done rows fold below.", "practical", S(L, steps_list(2, groups=True), ("Open steps on top", "Done group underneath"))))
    P("Full List", TA + " Full List", "Start Walk button", "should the Start Walk button stay pinned at the bottom of the screen or sit at the top above the first step?",
      ("bottom", "Pinned At The Bottom", "Always under the thumb while the list scrolls.", "practical", S(L, steps_list(0, start="bottom"), ("Pinned under the thumb", "List scrolls above it"))),
      ("top", "At The Top", "Read the button first, then the list under it.", "calm", S(L, steps_list(0, start="top"), ("Button above the list", "Scrolls away with the page"))))
    P("Walkthrough", TA + " Walkthrough", "Problem found", "should each step screen carry its own Flag A Problem button or should problems be logged on one screen at the end of the walk?",
      ("step", "Flag On Every Step", "A small terracotta Flag A Problem under each step.", "practical", S(L, step_screen(extra=[("btn2", "Next Step", "Flag A Problem", INK)]), ("Flag it where you see it", "Photo and note stay with the step"))),
      ("end", "One Problems Screen At The End", "All problems written up after the last step.", "calm", S(L, [("h", "Problems Found", 14), ("cards", [("Damp patch, basement wall", "Step 4", "tag:WET"), ("Loose dryer vent clamp", "Step 6", "tag:WATCH")], None, "dot"), ("btn", "Add A Problem", "line", INK), ("btn", "Next: Preview Report", "fill", TERRA)], ("One screen after the walk", "Steps stay simple"))))
    P("Walkthrough", TA + " Walkthrough", "Step screen order", "should the instructions sit on top with the photo box below or the big photo box first with the instructions under it?",
      ("text", "Instructions On Top", "Read what to do, then take the photo.", "calm", S(L, step_screen(), ("Words first", "Photo box under them"))),
      ("photo", "Photo Box First", "The big photo box leads; words sit under it.", "practical", S(L, step_screen(photo_first=True), ("Photo first", "Matches the before photo rule"))))
    P("Walkthrough", TA + " Walkthrough", "Area change", "when the walk moves into a new area should a short area card show first or should the next step simply appear?",
      ("card", "Short Area Card First", "A one-second card: Now In The Basement, 3 steps.", "playful", S(L, [("raw", rect(14, 0, 212, 150, CREAM, "none", 10) + t(120, 60, "NOW IN THE", 8, MUTE, "hind", 600, "middle", 'letter-spacing="1.2"') + t(120, 92, "Basement", 26, INK, "khand", anchor="middle") + t(120, 112, "3 steps  ·  about 15 min", 8.5, MUTE, anchor="middle"), 158), ("btn", "Start Area", "fill", TERRA)], ("Area card between areas", "Shows steps and time left there"))),
      ("next", "Next Step Appears", "The area name just changes in the step header.", "calm", S(L, step_screen(), ("No extra screen", "Area name in the progress row"))))
    return pairs
def ci_screen(extra=(), photo_on=False):
    b = [("h", "12 Birch Lane", 15), ("p", "Essentials plan  ·  10:30 AM visit")]
    if photo_on: b.insert(0, ("photo", 70, LAGOON, "house"))
    return b + list(extra)
def slider(y=None):
    return ("raw", rect(14, 0, 212, 30, JUNGLE + "1A", "none", 15) + rect(16, 2, 26, 26, JUNGLE, "none", 13) + ic("chev", 21, 7, 16, "#FFFFFF", 2.4) + t(130, 19, "Slide to check in", 9, JUNGLE, "hind", 600, "middle"), 38)
def T2():
    pairs, P = make("md18tc_", "UpKeep"); L = TA + " · Check-In"
    P("Check-In", TA + " Check-In", "Arrival prompt", "when the phone sees the tech has arrived should the check-in slider pop up by itself or wait until the tech opens the job?",
      ("pop", "Pops Up On Arrival", "A sheet slides up: You're here, slide to check in.", "practical", S(L, [("photo", 80, SOFT, "house"), ("raw", rect(0, 0, 240, 120, "#FFFFFF", LINE, 14) + t(14, 28, "You're at 12 Birch Lane", 13, INK, "khand") + t(14, 42, "Arrived 10:27 AM", 7.5, MUTE), 50), slider()], ("Slider shows up by itself", "Location used only on visit days"))),
      ("wait", "Waits For The Tech", "Nothing pops up; check in from the job card.", "calm", S(L, ci_screen([("cards", [("Job card", "Open to check in")], [LAGOON], "ic:home"), slider()]), ("Tech opens the job first", "No pop-ups while driving"))))
    P("Check-In", TA + " Check-In", "Right home check", "should the check-in screen show the home's front photo above the address or the address alone?",
      ("photo", "Front Photo And Address", "The first-visit photo of the house over the address.", "practical", S(L, ci_screen([slider()], True), ("See it is the right house", "Photo from the first visit"))),
      ("addr", "Address Alone", "Big street address and visit time.", "calm", S(L, ci_screen([("gap", 30), slider()]), ("Short and plain", "Address in big type"))))
    LC = TA + " · Camera"
    def cam(outline):
        g = rect(14, 0, 212, 170, "#2a2622", "none", 10) + photo(24, 10, 192, 150, LAGOON, "room", 6)
        if outline: g += rect(70, 40, 100, 90, "none", "#FFFFFF", 8, 2, 'stroke-dasharray="6 4"') + t(120, 148, "Fit the furnace inside the box", 8, "#FFFFFF", "hind", 600, "middle")
        return [("raw", g, 178), ("btn", "Take Before Photo", "fill", TERRA)]
    P("Photos", TA + " Camera", "Before photo guide", "should the camera show a faint outline of what to frame for each step or open as a plain camera?",
      ("guide", "Faint Framing Outline", "A dashed box shows what the photo must hold.", "practical", S(LC, cam(True), ("Same framing every visit", "Easy to compare later"))),
      ("plain", "Plain Camera", "The camera opens with nothing drawn on it.", "calm", S(LC, cam(False), ("Nothing in the way", "Tech frames it by eye"))))
    P("Photos", TA + " Camera", "Before photos per step", "should each step take one wide before photo or up to three close-ups?",
      ("one", "One Wide Photo", "One photo of the whole area before touching.", "calm", S(LC, [("photo", 110, LAGOON, "room", "Before  ·  1 photo"), ("btn", "Start Step", "fill", TERRA)], ("One photo, every step", "Quick and consistent"))),
      ("three", "Up To Three Close-Ups", "Wide shot plus up to two close-ups.", "practical", S(LC, [("photo", 80, LAGOON, "room", "Before  ·  wide"), ("photos", 2, 56, ["leaf", "sun"]), ("btn", "Start Step", "fill", TERRA)], ("Wide plus close-ups", "Better proof for problems"))))
    P("Photos", TA + " Walkthrough", "Before photo strip", "should the visit's before photos show as a swipe carousel at the top of each step or as a small grid in a Photos tab?",
      ("carousel", "Swipe Carousel On Top", "Before photos swipe along the top of the step.", "playful", S(L, [("carousel", [("Furnace", "Before", TERRA), ("Water heater", "Before", LAGOON), ("Sump pit", "Before", JUNGLE)], 100, 74, True, False, 0, True, None, False, "photo"), ("h", "Moisture Scan, Basement", 13), ("p", "Hold the meter flat on the wall, three spots.")], ("Photos ride along each step", "Swipe to compare"))),
      ("grid", "Grid In A Photos Tab", "All before photos in one tab of their own.", "calm", S(L, [("tabs", ["Steps", "Photos", "Notes"], "line"), ("photos", 3, 56), ("photos", 3, 56, ["leaf", "room", "house"]), ("p", "6 before photos this visit")], ("All photos in one place", "Step screen stays clean"))))
    P("Photos", TA + " Camera", "Photo stamp", "should every photo carry a small time stamp in the corner or stay clean with the time kept only in the report?",
      ("stamp", "Small Time Stamp", "10:41 AM  ·  Oct 18 printed in a corner.", "practical", S(LC, [("raw", photo(14, 0, 212, 150, LAGOON, "room", 8) + rect(150, 128, 70, 16, "#FFFFFFDD", "none", 3) + t(185, 139, "10:41 AM · Oct 18", 7.5, INK, "hind", 600, "middle"), 158)], ("Time on the photo itself", "Proof travels with the picture"))),
      ("clean", "Clean Photo", "No marks; the time lives in the report.", "calm", S(LC, [("photo", 150, LAGOON, "room"), ("p", "Taken 10:41 AM (saved with the report)")], ("Clean photo for the member", "Time kept in the data"))))
    P("Check-In", TA + " Check-In", "Nobody home", "when no one answers at a visit should the walk carry on with the outside steps only or end with a reschedule?",
      ("outside", "Carry On Outside", "Inside steps move to next visit; outside goes ahead.", "practical", S(L, [("h", "Nobody Home", 15), ("checks", ["Gutters and downspouts", "Dryer vent outside", "Roof from the ground"], JUNGLE, 0), ("note", "Inside steps saved for next visit", "Member gets a note"), ("btn", "Start Outside Steps", "fill", TERRA)], ("Visit still counts", "Outside steps only"))),
      ("resched", "End And Reschedule", "The visit closes and three new times are offered.", "calm", S(L, [("h", "Nobody Home", 15), ("p", "We'll offer the member three new times."), ("cards", [("Tue 9:00 AM", ""), ("Wed 1:30 PM", ""), ("Thu 10:00 AM", "")], None, "dot"), ("btn", "Send Times And Check Out", "fill", TERRA)], ("Whole walk next time", "No half visits"))))
    LJ = TA + " · Job Card"
    P("Check-In", TA + " Job Card", "Running late", "should the job card carry a one-tap Running Late note to the member or leave timing messages to the office?",
      ("tap", "One-Tap Running Late", "Pick 10, 20 or 30 minutes and it sends.", "practical", S(LJ, ci_screen([("lbl", "RUNNING LATE?"), ("tags", ["10 min", "20 min", "30 min"]), ("btn", "Start Route", "fill", INK)]), ("Member told in one tap", "Tech never types while driving"))),
      ("office", "Office Handles It", "No late button; the office sees the delay and calls.", "calm", S(LJ, ci_screen([("note", "Office can see you are late", "They update the member"), ("btn", "Start Route", "fill", INK)]), ("Tech just drives", "One voice to the member"))))
    LO = TA + " · Check-Out"
    P("Check-Out", TA + " Check-Out", "Check-out guard", "should check out stay locked until every step is done or skipped with a reason or be allowed any time with open steps flagged?",
      ("lock", "Locked Until Every Step Is Closed", "Done or skipped with a reason, then send.", "focused", S(LO, [("h", "Send Report And Check Out", 13), ("checks", ["Furnace filter", "Water heater", "Sump pit  ·  skipped: no access"], JUNGLE, 3), ("banner", "1 step still open", TERRA, "x"), ("btn", "Send Report And Check Out", "line", "#BDB6AA")], ("Nothing missed", "Button wakes when all are closed"))),
      ("flag", "Any Time, Open Steps Flagged", "Check out works; open steps go to the office.", "practical", S(LO, [("h", "Send Report And Check Out", 13), ("checks", ["Furnace filter", "Water heater", "Dryer vent"], JUNGLE, 2), ("banner", "1 open step sent to the office", SAFFRON, "clock"), ("btn", "Send Report And Check Out", "fill", TERRA)], ("Never stuck at a home", "Office follows up"))))
    P("Check-Out", TA + " Check-Out", "After check out", "should the next stop's card slide in right away or should the app go back to the Today map?",
      ("next", "Next Stop Slides In", "The next job card with Start Route comes up.", "practical", S(LO, [("banner", "Checked out of 12 Birch Lane", JUNGLE, "check"), ("lbl", "NEXT STOP"), ("cards", [("48 Cedar Court", "11:45 AM  ·  14 min away")], [LAGOON], "ic:home", "line", 44), ("btn", "Start Route", "fill", INK)], ("Straight on to the next job", "One tap to drive"))),
      ("map", "Back To The Today Map", "The day's map with this stop ticked.", "calm", S(LO, [("banner", "Checked out of 12 Birch Lane", JUNGLE, "check"), ("map", 110), ("cards", [("3 of 5 stops done", "")], [JUNGLE], "dot")], ("See the whole day again", "Pick the next stop yourself"))))
    return pairs
LR = TA + " · Readings"
def rd(val="22", word="Wet", c=TERRA, extra=(), sub="Spot: basement, north wall"):
    return [("h", "Moisture Reading", 14), ("reading", val, word, c, sub)] + list(extra)
def T3():
    pairs, P = make("md18tm_", "UpKeep")
    P("Readings", TA + " Readings", "Dry, watch and wet scale", "should a small three-part scale under the number show where the reading falls or should only the label show?",
      ("scale", "Small Three-Part Scale", "Dry, Watch, Wet bar with a marker.", "practical", S(LR, rd("17", "Watch", SAFFRON, [("scale", .52)]), ("See how close to wet", "Marker moves as you type"))),
      ("label", "Label Only", "Just the number and its label.", "calm", S(LR, rd("17", "Watch", SAFFRON), ("Short and clean", "One word says it"))))
    P("Readings", TA + " Readings", "Wet reading photo", "when a reading comes out wet should a photo of that spot be required or stay optional?",
      ("req", "Photo Required When Wet", "The step won't close until the spot is shot.", "focused", S(LR, rd(extra=[("photo", 70, TERRA, "room", "Photo of the wet spot  ·  required"), ("btn", "Take Photo", "fill", TERRA)]), ("Every wet reading has proof", "Member sees where it is"))),
      ("opt", "Photo Optional", "An Add Photo link, never required.", "calm", S(LR, rd(extra=[("btn", "Add Photo (Optional)", "link", LAGOON), ("btn", "Save Reading", "fill", INK)]), ("Faster at busy homes", "Tech decides"))))
    P("Readings", TA + " Readings", "Wet follow-up", "should a wet reading add a recheck to the next visit by itself or let the tech choose?",
      ("auto", "Recheck Added By Itself", "Wet means it comes back next visit, always.", "focused", S(LR, rd(extra=[("banner", "Recheck added to next visit", LAGOON, "cal")]), ("Never forgotten", "Shows on the next walk"))),
      ("choose", "Tech Chooses", "A toggle: Recheck next visit, on or off.", "practical", S(LR, rd(extra=[("toggles", [("Recheck next visit", True), ("Tell the member now", False)])]), ("Tech's call on site", "Some wet spots are known"))))
    P("Readings", TA + " Readings", "Reading trend", "should each spot show a small trend line of past visits or a simple up or down arrow from last time?",
      ("line", "Small Trend Line", "Last five visits drawn as a tiny line.", "practical", S(LR, rd("17", "Watch", SAFFRON, [("lbl", "LAST FIVE VISITS"), ("line", [.2, .25, .3, .4, .55], SAFFRON, 50)]), ("Whole history at a glance", "Rising readings stand out"))),
      ("arrow", "Up Or Down Arrow", "Up 3 since last visit, nothing more.", "calm", S(LR, rd("17", "Watch", SAFFRON, [("raw", ic("chev", 14, 0, 18, TERRA, 2.4).replace('scale(0.75)', 'scale(0.75) rotate(-90 12 12)') + t(38, 13, "Up 3 since last visit", 9, TERRA, "hind", 600), 24)]), ("One plain line", "Easy to read in a dark basement"))))
    P("Readings", TA + " Readings", "Reading spots", "should the tech take readings at the spots saved on the first-visit map or add spots freely each visit?",
      ("saved", "Saved Spots From The Map", "The same five spots every visit, in order.", "focused", S(LR, [("h", "Reading Spots", 14), ("cards", [("Basement, north wall", "Last: 14  Dry"), ("Under kitchen sink", "Last: 12  Dry"), ("Bath floor by tub", "Last: 17  Watch")], [JUNGLE, JUNGLE, SAFFRON], "num"), ("btn", "Add A New Spot", "link", LAGOON)], ("Same spots, every visit", "Readings compare fairly"))),
      ("free", "Add Spots Freely", "Name a spot and type the reading each time.", "calm", S(LR, [("h", "Reading Spots", 14), ("input", "Name this spot", LAGOON, "search"), ("reading", "14", "Dry", JUNGLE), ("btn", "Save And Add Another", "fill", INK)], ("Tech picks the spots", "Nothing to set up first"))))
    LV = TA + " · Visit Report"
    P("Visit Report", TA + " Visit Report", "Readings summary", "should the report show the readings as a swipe carousel of spot cards or as one table?",
      ("carousel", "Carousel Of Spot Cards", "One card per spot with its label.", "playful", S(LV, [("h", "Moisture Readings", 14), ("carousel", [("Basement wall", "14  Dry", JUNGLE), ("Kitchen sink", "12  Dry", JUNGLE), ("Bath floor", "17  Watch", SAFFRON)], 120, 70, True, False, 0)], ("Swipe spot by spot", "Colour shows the label"))),
      ("table", "One Table", "Spot, number and label in rows.", "calm", S(LV, [("h", "Moisture Readings", 14), ("kv", [("Basement wall", "14  Dry", JUNGLE), ("Kitchen sink", "12  Dry", JUNGLE), ("Bath floor", "17  Watch", SAFFRON), ("Laundry floor", "11  Dry", JUNGLE)])], ("All spots at once", "Short to scan"))))
    P("Readings", TA + " Readings", "Meter type", "should each reading note which meter was used or show the number and label alone?",
      ("meter", "Note The Meter", "Pin meter or pinless, saved with the number.", "practical", S(LR, rd("17", "Watch", SAFFRON, [("tabs", ["Pinless meter", "Pin meter"], "pill")]), ("Readings stay comparable", "Pinless set as the default"))),
      ("alone", "Number And Label Alone", "One meter for the whole team; nothing to pick.", "calm", S(LR, rd("17", "Watch", SAFFRON), ("Fewer taps", "Team uses one meter"))))
    P("Readings", TA + " Readings", "Watch label help", "should the Watch label carry a short line saying what it means or stay one word?",
      ("line", "Short What-It-Means Line", "Watch: a little high, we check it next visit.", "practical", S(LR, rd("17", "Watch", SAFFRON, [("note", "Watch: a little high", "We check this spot again next visit", SAFFRON)]), ("Clear for new techs", "Same line the member sees"))),
      ("word", "One Word", "Dry, Watch or Wet and nothing else.", "calm", S(LR, rd("17", "Watch", SAFFRON), ("Quick and calm", "Training covers the meaning"))))
    P("Visit Report", TA + " Visit Report", "Walk recap", "before sending should the tech see a carousel recap of every step's after photo or a checklist recap with ticks?",
      ("carousel", "After Photo Carousel", "Swipe through every step's after photo.", "playful", S(LV, [("h", "Walk Recap", 14), ("carousel", [("Furnace filter", "After", JUNGLE), ("Water heater", "After", LAGOON), ("Sump pit", "After", TERRA)], 130, 100, True, False, 0, True, None, False, "photo"), ("btn", "Preview Report", "fill", TERRA)], ("See the work, step by step", "Spot a missing photo fast"))),
      ("checks", "Checklist With Ticks", "Every step ticked, skipped steps marked.", "calm", S(LV, [("h", "Walk Recap", 14), ("checks", ["Before photo", "Furnace filter", "Water heater", "Moisture scan", "Sump pit"], JUNGLE, 5), ("btn", "Preview Report", "fill", TERRA)], ("One short list", "Quick last look"))))
    P("Readings", TA + " Readings", "Second reading", "when a reading is wet should the app ask for a second reading a short way off or accept the first number?",
      ("second", "Ask For A Second Reading", "Wet? Take one more a hand's width away.", "focused", S(LR, rd(extra=[("note", "Take one more reading", "A hand's width from the first spot", LAGOON), ("reading", "21", "Wet", TERRA)]), ("Confirms it is really wet", "Fewer false alarms"))),
      ("first", "Accept The First Number", "One reading per spot, always.", "calm", S(LR, rd(extra=[("btn", "Save Reading", "fill", INK)]), ("Quick walk", "One number per spot"))))
    return pairs
