"""Security Dashboard Setup Deck (Max asked, Oct 15 2026 23:25 ICT): how the Security dashboard is laid out.
Pair: (group, ask, A, B); option = (label, desc, mockup kinds...). No overlap with Security Duties dashboard cards."""
def P(g, ask, a, ad, ak, b, bd, bk): return (g, ask, (a, ad, *ak), (b, bd, *bk))
NAME = "Security Dashboard Setup Deck"
ABOUT = "How the Security dashboard should be set up: what goes first, how each section looks, and the phone layout"
PAIRS = [
P("Top", "Right Under The Header: Status Overview Or Alerts?", "Status Overview", "A row of tiles for each area.", ["status", "list"], "Alerts First", "Anything that needs you now.", ["cards", "list"]),
P("Top", "Right Under The Header: Alerts Or To-Dos?", "Alerts", "Problems found, newest first.", ["cards", "list"], "To-Dos", "Your next fixes as tick boxes.", ["todo", "list"]),
P("Alerts", "Alerts: One Banner Or A Card List?", "Banner", "One strip across the top.", ["banner", "status"], "Card List", "One card per alert.", ["cards", "status"]),
P("Accounts", "Account Health: Light Per Account Or Checklist By Area?", "Light Per Account", "Green, amber or red next to each.", ["lights", "list"], "Checklist By Area", "Passwords, backups, devices with counts.", ["areas", "list"]),
P("Backups", "Backups Status: Last Backup Times Or Simple OK Light?", "Last Backup Times", "Each backup with its date.", ["table"], "Simple OK Light", "One light: backed up or not.", ["status"]),
P("Passwords", "Password Health: Count Tiles Or One Line Summary?", "Count Tiles", "Reused, weak and breached counts. Never the passwords.", ["counts"], "One Line", "\"3 passwords need attention.\"", ["banner"]),
P("2FA", "2FA Coverage: Progress Bar Or Account Table?", "Progress Bar", "How many accounts have 2FA.", ["bar"], "Account Table", "Each account, on or off.", ["table"]),
P("Domains", "Domain And SSL Expiry: Timeline Or Table?", "Timeline", "Dates on a line, soonest first.", ["timeline"], "Table", "Name, expiry date, days left.", ["table"]),
P("Family", "Family Accounts: Own Section Or A Tab?", "Own Section", "Nozomi, Maple and Mom on the page.", ["family"], "A Tab", "Switch between you and family.", ["tabs", "list"]),
P("Family", "Family Section: Light Per Person Or Shared Checklist?", "Light Per Person", "One status per family member.", ["family"], "Shared Checklist", "One list of family fixes.", ["todo"]),
P("Activity", "Recent Activity Log: Short Feed Or Fold-Out?", "Short Feed", "Last few events, always shown.", ["log"], "Fold-Out", "Hidden until you open it.", ["fold"]),
P("Activity", "Activity Log: Last 24 Hours Or Last 7 Days?", "Last 24 Hours", "Only today's events.", ["log"], "Last 7 Days", "A week of events, grouped.", ["table"]),
P("Report", "Weekly Report: Carousel Or Page?", "Carousel", "Swipe one slide per area.", ["carousel"], "Page", "One page to scroll.", ["page"]),
P("Style", "Sections: Swipeable Thumbnails Or Lists?", "Thumbnails", "Swipe through cards per area.", ["thumbs", "thumbs"], "Lists", "Plain rows you scroll.", ["list", "list"]),
P("Style", "Areas Overview: Carousel Or Grid?", "Carousel", "One row you swipe sideways.", ["carousel"], "Grid", "All areas visible at once.", ["grid"]),
P("Order", "Section Order: Problems First Or Fixed Order?", "Problems First", "Sections with issues move up.", ["cards", "areas"], "Fixed Order", "Same order every day.", ["areas", "list"]),
P("Order", "After The Top: Passwords Next Or Backups Next?", "Passwords Next", "Password health right after.", ["counts", "list"], "Backups Next", "Backups right after.", ["table", "list"]),
P("Amount", "How Much Shows: Everything Open Or Fold-Outs?", "Everything Open", "All details visible.", ["open"], "Fold-Outs", "Headlines; tap to open.", ["fold"]),
P("Phone", "Phone Layout: One Column Stack Or Swipe Between Sections?", "One Column", "Scroll down through sections.", ["stack"], "Swipe Sections", "Swipe left and right per section.", ["carousel"]),
P("Phone", "Phone Top: Alerts Only Or Full Overview?", "Alerts Only", "Just what needs you, rest below.", ["banner", "list"], "Full Overview", "All area tiles up top.", ["status", "grid"]),
]
assert len(PAIRS) == 20
DECKS = {"dashboard-setup": (NAME, ABOUT, PAIRS)}
