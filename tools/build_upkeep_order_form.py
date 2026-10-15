#!/usr/bin/env python3
"""Oct 15 2026 (Max via Blueprint 19:14 ICT, clarified 19:19): two UpKeep shelf decks about the smartupkeep.ai ORDER FORM
(Sign Up step after choosing a plan, app.js signup()). Facts only from funnel-app/app.js + pricing-config.js.
Writes banks/src-upkeep-order-form.json and banks/src-upkeep-order-form-details.json; publish with tools/ready_shelf.py build --source."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__)); os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from team_kit import deck, TERRA, LAGOON, JUNGLE, SAFFRON, INK
def mk(prefix, sub):
    pairs, O, add = deck(prefix, "UpKeep"); HD = ("hdr", "Smart Upkeep", sub, SAFFRON, "logo", "S")
    def P(g, ask, a, b): add(g, g, O(a[0], a[1], a[2], a[3], [HD] + a[4]), O(b[0], b[1], b[2], b[3], [HD] + b[4]), ask)
    return pairs, P
B = lambda s, c=SAFFRON: ("btn", s, "fill", c)
L = lambda s, c=LAGOON: ("btn", s, "link", c)
W = lambda s, c=INK, sub="": ("word", s, 20, c, sub)
TX = lambda s: ("p", s)
IN = lambda s, k="home": ("input", s, INK, k)

# ---------------- Order Form Deck: structure, fields, order, trust, confirm ----------------
a, P = mk("of1_", "Sign Up")
P("Layout", "Order Form: One Long Page Or Short Steps With Next?",
  ("lay_one", "One Long Page", "Everything on one scroll, as live.", "calm", [W("Sign Up for Plus"), IN("Service Address"), IN("Full Name"), ("cards", [("Membership Agreement", "", ""), ("Payment Plan", "", "")], None, "dot", "line", 24), B("Complete Sign Up")]),
  ("lay_steps", "Short Steps", "Details, Sign, Pay: one card each.", "focused", [("steps", ["Details", "Sign", "Pay"], SAFFRON, 0), IN("Service Address"), IN("Full Name"), B("Next")]))
P("Layout", "Progress At The Top: Keep The 4-Step Rail Or A Simple Bar?",
  ("pr_rail", "4-Step Rail", "Icons with Sign Up as the last step, as live.", "calm", [("steps", ["Home", "Price", "Extras", "Sign Up"], SAFFRON, 3), W("Sign Up for Plus")]),
  ("pr_bar", "Simple Bar", "\"Almost Done\" bar near full.", "quick", [("bar", .9, SAFFRON, "Almost Done", "Last Step"), W("Sign Up for Plus")]))
P("Field Order", "First Field: Service Address Or Full Name?",
  ("fo_addr", "Service Address First", "As live; filled in from your ZIP.", "calm", [IN("Service Address"), IN("Full Name", "star"), IN("Phone", "phone")]),
  ("fo_name", "Full Name First", "Name, then contact, then address.", "focused", [IN("Full Name", "star"), IN("Phone", "phone"), IN("Service Address")]))
P("Field Order", "Phone And Name: Side By Side Or Stacked?",
  ("pn_side", "Side By Side", "Two half-width fields, as live.", "focused", [("tiles", [("Full Name", "star"), ("Phone", "phone")], 2, 40), IN("Email", "tag")]),
  ("pn_stack", "Stacked", "One field per line, bigger on phones.", "calm", [IN("Full Name", "star"), IN("Phone", "phone"), IN("Email", "tag")]))
P("Field Order", "Referral Code Box: Always Open Or Behind \"Have A Code?\"",
  ("rc_open", "Always Open", "Optional field shown, as live.", "calm", [IN("Email", "tag"), IN("Referral Code (Optional)", "tag")]),
  ("rc_link", "Have A Code? Link", "Tap to open the box.", "quick", [IN("Email", "tag"), L("Have A Referral Code?")]))
P("Field Order", "Yard Sign Box: Under Your Details Or Near The Total?",
  ("ys_det", "Under Your Details", "Checkbox at the end of the details card, as live.", "calm", [IN("Email", "tag"), ("toggles", [("Yard Sign OK? Free Battery Swap", True)])]),
  ("ys_tot", "Near The Total", "Next to Due at Sign Up as a little extra.", "focused", [("table", [("Due at Sign Up", "$1,970")]), ("toggles", [("Yard Sign OK? Free Battery Swap", True)])]))
P("Home Details", "Home Details You Gave Earlier: Show A Short Recap Or Leave Off?",
  ("hd_show", "Short Recap", "Sq ft, furnaces, AC, water heater on the form.", "focused", [("table", [("Home", "Under 2,000 sq ft"), ("Furnaces", "1"), ("Water Heater", "Tank")])]),
  ("hd_hide", "Leave It Off", "Form only asks what's new.", "calm", [IN("Service Address"), IN("Full Name", "star")]))
P("Home Details", "Edit Home Details: Link Back To The Questions Or No Edit Link?",
  ("ed_link", "Edit Link", "\"Change Home Details\" goes back.", "focused", [("table", [("Home", "Under 2,000 sq ft")]), L("Change Home Details")]),
  ("ed_none", "No Edit Link", "Back button at the top only, as live.", "calm", [L("‹ Back", INK), W("Sign Up for Plus")]))
P("Plan Summary", "Plan Summary: At The Top Or Just Above Payment?",
  ("ps_top", "At The Top", "Plan and total first, then fill in.", "focused", [("table", [("Plan", "Plus (4 visits a year)"), ("Due at Sign Up", "$1,970")]), IN("Service Address")]),
  ("ps_pay", "Above Payment", "Under the signatures, as live.", "calm", [("cards", [("Liability Waiver", "Signed", "")], None, "dot", "line", 24), ("table", [("Plan", "Plus (4 visits a year)"), ("Due at Sign Up", "$1,970")])]))
P("Plan Summary", "Running Total: Stays Pinned At The Bottom Or Only In The Summary?",
  ("rt_pin", "Pinned Bar", "Total and Complete button always in view.", "quick", [IN("Full Name", "star"), ("gap", 30), ("table", [("Due at Sign Up", "$1,970")], True), B("Complete Sign Up")]),
  ("rt_sum", "Only In The Summary", "One place, as live.", "calm", [("table", [("Plan", "Plus"), ("Add-ons", "None selected"), ("Due at Sign Up", "$1,970")])]))
P("Plan Summary", "Selected Extras In The Summary: Each On Its Own Line Or One Extras Total?",
  ("ex_each", "Each On Its Own Line", "Add-on: Chimney Sweep $255/yr, as live.", "focused", [("table", [("Add-on: Chimney Sweep", "$255/yr"), ("Add-on: Radon Test", "$100/yr")])]),
  ("ex_one", "One Extras Total", "Tap to see the list.", "calm", [("table", [("Extras (2)", "$355/yr")]), L("See Extras")]))
P("Signatures", "Agreement And Waiver: Two Signatures Or Sign Once For Both?",
  ("sg_two", "Two Signatures", "One for the Agreement, one for the Waiver, as live.", "calm", [IN("Sign: Membership Agreement", "check"), IN("Sign: Liability Waiver", "check")]),
  ("sg_one", "Sign Once", "One signature covers both boxes.", "quick", [("toggles", [("I agree to the Agreement", True), ("I accept the Waiver", True)]), IN("Sign Once", "check")]))
P("Signatures", "Agreement Text: Fold-Out \"Read Agreement\" Or Scroll Box Shown Open?",
  ("ag_fold", "Fold-Out", "Tap Read Agreement, as live.", "calm", [("cards", [("Read Agreement", "", "▾")], None, "dot", "line", 26), ("toggles", [("I agree", False)])]),
  ("ag_box", "Open Scroll Box", "Short scrolling box of terms.", "focused", [("checks", ["Membership and term", "Pricing and payment", "Cancel anytime, no fee"], INK, 0), ("toggles", [("I agree", False)])]))
P("Trust", "Trust Row On The Form: Show Badges Or Keep The Form Plain?",
  ("tb_show", "Show Badges", "Certified Techs, Honest Refund, Report Every Visit.", "focused", [("tags", ["Certified Techs", "Honest Refund", "Report Every Visit"], True), IN("Service Address")]),
  ("tb_plain", "Plain Form", "Badges stay on the home page, as live.", "calm", [W("Sign Up for Plus"), IN("Service Address")]))
P("Trust", "Cancel Anytime Line: Next To The Button Or In The Cancel Policy Card Only?",
  ("ca_btn", "Next To The Button", "\"Cancel anytime, no fee\" under Complete Sign Up.", "quick", [B("Complete Sign Up"), TX("Cancel anytime, no fee.")]),
  ("ca_card", "Cancel Policy Card Only", "As live.", "calm", [("cards", [("Cancel Policy", "Refund = prepaid minus work done", "")], None, "dot", "line", 30), B("Complete Sign Up")]))
P("Trust", "Michigan 3-Day Cancel Notice: Beside The Agreement Signature Or At The Bottom?",
  ("mi_sig", "Beside The Signature", "As live, next to where you sign.", "calm", [("banner", "3-Day Cancel Right", SAFFRON, "check"), IN("Signature", "check")]),
  ("mi_bot", "At The Bottom", "Above Complete Sign Up.", "focused", [IN("Signature", "check"), ("banner", "3-Day Cancel Right", SAFFRON, "check"), B("Complete Sign Up")]))
P("Confirm Button", "Confirm Button Words: \"Complete Sign Up\" Or \"Join Plus\"?",
  ("cb_comp", "Complete Sign Up", "As live.", "calm", [("table", [("Due at Sign Up", "$1,970")]), B("Complete Sign Up")]),
  ("cb_join", "Join Plus", "Names the plan you picked.", "quick", [("table", [("Due at Sign Up", "$1,970")]), B("Join Plus")]))
P("Confirm Button", "Confirm Button: Show The Amount On It Or Words Only?",
  ("cm_amt", "Show The Amount", "\"Complete Sign Up · $1,970\"", "focused", [B("Complete Sign Up · $1,970")]),
  ("cm_words", "Words Only", "Amount stays in the summary.", "calm", [("table", [("Due at Sign Up", "$1,970")]), B("Complete Sign Up")]))
P("Errors And Help", "Missing Field Errors: One Message Above The Button Or Under Each Field?",
  ("er_one", "One Message", "\"Enter your service address.\" above the button, as live.", "calm", [IN("Service Address"), ("banner", "Enter your service address.", TERRA, "x"), B("Complete Sign Up")]),
  ("er_field", "Under Each Field", "Red line right under what's missing.", "focused", [IN("Service Address"), TX("Enter your service address."), IN("Full Name", "star")]))
P("Errors And Help", "Help On The Form: Call Or Text Line Or No Help Line?",
  ("hp_line", "Call Or Text Line", "\"Questions? Call or text\" at the bottom.", "focused", [B("Complete Sign Up"), L("Questions? Call Or Text Us")]),
  ("hp_none", "No Help Line", "FAQ stays on the home page, as live.", "calm", [B("Complete Sign Up")]))
assert len(a) == 20, len(a)

# ---------------- Order Form Details Deck: payment wording, offers, start date, upsell ----------------
b, P = mk("of2_", "Sign Up")
P("Payment Wording", "Re-Ask, Monthly Card: Add A Pay-Monthly-By-Card Option, Or Keep Annual Up Front And 2-Year Prepay Only?",
  ("mc_add", "Add Pay Monthly By Card", "New choice, e.g. Plus from $164/mo.", "quick", [("cards", [("Pay Monthly by Card", "Charged each month", "$164/mo"), ("Paid in Full Annually", "Up front", "")], None, "dot", "line", 30)]),
  ("mc_keep", "Keep Prepay Only", "Annual up front or 2-year prepay, as live.", "calm", [("cards", [("Paid in Full Annually", "Up front", ""), ("Pay for 2 Years", "6 extra months free", "")], None, "dot", "line", 30)]))
P("Welcome Offers", "Re-Ask, Stacked Offers: Let Pay-2-Years (6 Months Free) And Refer-A-Neighbor (1 Month Each) Stack, Or One Offer Per Customer?",
  ("st_yes", "Let Them Stack", "2-year prepay plus referral months, as live.", "focused", [("cards", [("Pay for 2 Years", "+6 free months", ""), ("Refer a Neighbor", "+1 month each", "")], None, "dot", "line", 30), TX("Offers stack.")]),
  ("st_no", "One Offer Only", "Pick the 2-year prepay or a referral.", "calm", [("btn2", "6 Free Months", "Referral Month", SAFFRON), TX("One welcome offer per sign-up.")]))
P("Payment Wording", "Payment Plan Name: \"Paid In Full Annually, Up Front\" Or \"Pay Yearly\"?",
  ("pn_full", "Paid In Full Annually, Up Front", "As live.", "calm", [("cards", [("Plus: Paid in Full Annually, Up Front", "", "$1,970")], None, "dot", "line", 30)]),
  ("pn_short", "Pay Yearly", "Shorter, details underneath.", "quick", [("cards", [("Pay Yearly", "One payment a year", "$1,970")], None, "dot", "line", 30)]))
P("Payment Wording", "2-Year Option Name: Full Wording Or Short \"Pay 2 Years, Get 30 Months\"?",
  ("tw_full", "Full Wording", "\"Pay for 2 Years, Get 6 Extra Months Free at the End of Your Term\", as live.", "calm", [TX("Pay for 2 Years, Get 6 Extra Months Free at the End of Your Term")]),
  ("tw_short", "Pay 2 Years, Get 30 Months", "Same deal, shorter title.", "quick", [W("Pay 2 Years, Get 30 Months", SAFFRON), TX("6 extra months free at the end")]))
P("Payment Wording", "Total Label: \"Due At Sign Up\" Or \"Today's Payment\"?",
  ("tl_due", "Due At Sign Up", "As live.", "calm", [("table", [("Due at Sign Up (Estimated)", "$1,970")])]),
  ("tl_today", "Today's Payment", "Plain everyday words.", "quick", [("table", [("Today's Payment (Estimated)", "$1,970")])]))
P("Payment Wording", "Big Price In Payment Plan: Per Month Or The Full Payment?",
  ("bp_mo", "Per Month", "$164/mo big, full amount small.", "quick", [W("$164/mo", SAFFRON), TX("Paid $1,970 up front")]),
  ("bp_full", "Full Payment", "$1,970 big, per month small.", "calm", [W("$1,970", INK), TX("About $164/mo")]))
P("Payment Wording", "Complete Plan Payments: Show 4 Quarterly Payments First Or Annual Save 10% First?",
  ("cq_q", "Quarterly First", "4 Quarterly Payments on top, as live.", "calm", [("cards", [("4 Quarterly Payments", "", ""), ("Pay Annually, Save 10%", "Draft", "")], None, "dot", "line", 28)]),
  ("cq_a", "Save 10% First", "Discount option on top.", "focused", [("cards", [("Pay Annually, Save 10%", "Draft", ""), ("4 Quarterly Payments", "", "")], None, "dot", "line", 28)]))
P("Payment Wording", "Card Fields: Show Card Boxes On The Form Or A Separate Secure Pay Step?",
  ("cf_form", "On The Form", "Card Number, Expiry, CVC at the bottom, as live.", "calm", [IN("Card Number", "card"), ("tiles", [("MM / YY", "cal"), ("CVC", "card")], 2, 36)]),
  ("cf_step", "Secure Pay Step", "Button opens a card page.", "focused", [("table", [("Due at Sign Up", "$1,970")]), B("Continue To Secure Payment")]))
P("Welcome Offers", "Offer Terms On The Form: Short Line Or Fold-Out Full Terms?",
  ("ot_line", "Short Line", "\"Free months are added at the end of your term.\"", "quick", [TX("Free months are added at the end of your term and apply once you complete it.")]),
  ("ot_fold", "Fold-Out Terms", "Tap for the full welcome offer terms.", "calm", [("cards", [("Welcome Offer Terms", "", "▾")], None, "dot", "line", 26)]))
P("Welcome Offers", "Referral Applied Line: Full Explanation Or Short \"+1 Free Month\"?",
  ("ra_full", "Full Explanation", "Free month after your payment clears, at end of term, as live.", "calm", [("table", [("Referral Code Applied", "SU-HOME-1234")]), TX("Free month after your payment clears, added at the end of your term.")]),
  ("ra_short", "+1 Free Month", "Short, with a terms link.", "quick", [("table", [("Referral Code", "+1 Free Month")]), L("Terms")]))
P("Welcome Offers", "Free-Months Line In The Summary: Shown As \"No Charge\" Or As A Dollar Value?",
  ("fm_nc", "No Charge", "+6 Free Months ... No Charge, as live.", "calm", [("table", [("+6 Free Months", "No Charge")])]),
  ("fm_val", "Dollar Value", "Show what 6 months is worth.", "focused", [("table", [("+6 Free Months", "Worth $985")]), TX("Example value, Plus plan")]))
P("Start Date", "First Visit Date: Pick It On The Form Or After Sign Up?",
  ("sd_form", "On The Form", "Date before you pay.", "focused", [("cal", (6,), SAFFRON), B("Complete Sign Up")]),
  ("sd_after", "After Sign Up", "Book Your First Visit on the welcome screen, as live.", "calm", [W("You're In"), B("Book Your First Visit")]))
P("Start Date", "Start Date Wording: \"Membership Starts At Your First Visit\" Or No Start Note?",
  ("sw_note", "Show The Note", "Term runs 12 months from your first visit.", "focused", [TX("Your 12 months start at your first visit."), B("Complete Sign Up")]),
  ("sw_none", "No Note", "Only in the Agreement, as live.", "calm", [B("Complete Sign Up")]))
P("Add-On Upsell", "Last-Extra Pop-Up Before Submit: Keep It Or Drop It?",
  ("fo_keep", "Keep It", "One \"Add Chimney Sweep?\" pop-up, as live.", "quick", [W("Add Chimney Sweep?"), TX("$129-$381 per service"), ("btn2", "No Thanks", "Add", SAFFRON)]),
  ("fo_drop", "Drop It", "Submit goes straight through.", "calm", [B("Complete Sign Up"), W("You're In", JUNGLE)]))
P("Add-On Upsell", "Pop-Up Extra Picked: Take Turns Through The List Or Random?",
  ("fr_rr", "Take Turns", "Windows, Chimney, Radon, Gutters, Pressure, Ducts in order, as live.", "calm", [("tags", ["Windows", "Chimney", "Radon", "Gutters"], False)]),
  ("fr_rand", "Random", "Any one of the six.", "quick", [("tags", ["Radon"], True)]))
P("Add-On Upsell", "Upsell At Checkout: One Pop-Up Or A Small \"Add Extras\" Row On The Form?",
  ("ur_pop", "One Pop-Up", "Shown once at Submit, as live.", "focused", [W("Add Radon Test?"), ("btn2", "No Thanks", "Add", SAFFRON)]),
  ("ur_row", "Add Extras Row", "Small tiles above the total.", "calm", [("tiles", [("Radon Test", "check"), ("Chimney Sweep", "check")], 2, 40), ("table", [("Due at Sign Up", "$1,970")])]))
P("Add-On Upsell", "Pop-Up Buttons: \"No Thanks / Add\" Or \"Skip / Add To My Plan\"?",
  ("pb_nt", "No Thanks / Add", "As live.", "calm", [("btn2", "No Thanks", "Add", SAFFRON)]),
  ("pb_plan", "Skip / Add To My Plan", "Clear it joins your plan.", "focused", [("btn2", "Skip", "Add To My Plan", SAFFRON)]))
P("Demo Wording", "Demo Labels Before Launch: Keep \"Demo: No Card Charged\" Or Hide For Testers?",
  ("dm_keep", "Keep Demo Labels", "Clear nothing is charged, as live.", "calm", [("banner", "Demo: No Card Charged", SAFFRON, "card"), B("Complete Sign Up (Demo)")]),
  ("dm_hide", "Hide For Testers", "Looks like the real launch form.", "focused", [IN("Card Number", "card"), B("Complete Sign Up")]))
P("Errors And Help", "Error Wording: Short Commands Or Friendly Sentences?",
  ("ew_short", "Short Commands", "\"Enter a valid email.\" as live.", "quick", [("banner", "Enter a valid email.", TERRA, "x")]),
  ("ew_kind", "Friendly Sentences", "\"That email looks off, check it?\"", "calm", [("banner", "That email looks off. Check it?", TERRA, "x")]))
P("Errors And Help", "Phone Field Help: Example Under The Field Or No Example?",
  ("ph_ex", "Example Under It", "\"e.g. 248-555-0123\"", "focused", [IN("Phone", "phone"), TX("e.g. 248-555-0123")]),
  ("ph_none", "No Example", "Plain field, as live.", "calm", [IN("Phone", "phone")]))
assert len(b) == 20, len(b)
for nm, ps in (("src-upkeep-order-form", a), ("src-upkeep-order-form-details", b)):
    json.dump({"pairs": ps}, open(f"banks/{nm}.json", "w"), indent=1, ensure_ascii=False); print(nm, len(ps))
