#!/usr/bin/env python3
"""CEO Management Deck (Oct 14 2026): 20 this-or-that cards on how Grok Bot runs Max's agent team.
4 categories x 5: Priorities & Focus, Delegation & Routing, Usage & Cost, Follow-through & Reporting. Submit -> grok-bot."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from team_kit import deck, publish, render, TERRA, LAGOON, JUNGLE, SAFFRON, INK
pairs, O, add = deck("ceo_", "Grok Bot")
HD = ("hdr", "Grok Bot", "CEO of the agent team", LAGOON, "logo", "G")
def V(h, sub, c): return [HD, ("h", h, 13), ("p", sub), ("btn", h[:22], "fill", c)]
C = {}
def P(g, ask, a, b):
    add(g, g, O(a[0], a[1], a[2], "focused", V(a[1], a[2], LAGOON)), O(b[0], b[1], b[2], "quick", V(b[1], b[2], SAFFRON)), ask)
G = "Priorities & Focus"
P(G, "Top Priority Each Day: Set By Max Or Picked By Grok Bot?", ("pr_max", "Max Sets It", "Grok Bot asks each morning."), ("pr_gb", "Grok Bot Picks It", "From deadlines and open tasks; Max can override."))
P(G, "How Many Priorities At Once?", ("pr_three", "Top Three", "Three focus items across the team."), ("pr_one", "One Big Thing", "Everything else waits."))
P(G, "Deadline Work Like Taxes: Pause Other Agents Or Keep Them Running?", ("pr_pause", "Pause Others", "All effort on the deadline."), ("pr_keep", "Keep Running", "Deadline gets first slot, others continue."))
P(G, "New Idea From Max Mid-Day: Start Now Or Queue For Tomorrow?", ("pr_now", "Start Now", "Bump current work."), ("pr_queue", "Queue It", "Slot into the next plan."))
P(G, "Stale Tasks Over A Week Old: Ask Max Or Close Quietly?", ("pr_ask", "Ask Max", "List them in the brief."), ("pr_close", "Close Quietly", "Archive with a note."))
G = "Delegation & Routing"
P(G, "Check In With Agents: Every Few Hours Or Only At Milestones?", ("dl_hours", "Every Few Hours", "Regular status pulls."), ("dl_mile", "At Milestones", "Agents report when something lands."))
P(G, "Relays To Max: Batch Them Or Send Immediately?", ("dl_batch", "Batch Them", "Grouped twice a day."), ("dl_now", "Immediately", "Each item as it comes."))
P(G, "Stuck Agent: Stop It Or Let It Retry?", ("dl_stop", "Stop It", "After one failed retry, reassign."), ("dl_retry", "Let It Retry", "Up to three tries first."))
P(G, "Work That Fits Two Agents: Split It Or Give One Owner?", ("dl_split", "Split It", "Each takes a part."), ("dl_owner", "One Owner", "Clear accountability."))
P(G, "Grok Bot Doing Small Tasks Itself Or Always Delegating?", ("dl_self", "Do It Itself", "Faster for quick fixes."), ("dl_deleg", "Always Delegate", "Keeps Grok Bot free to manage."))
G = "Usage & Cost"
P(G, "Deck Results Router: Run Often Or Run Less To Save Usage?", ("us_often", "Run Often", "Every hour."), ("us_less", "Run Less", "Three times a day."))
P(G, "Near The Usage Limit: Pause Low Priority Or Slow Everyone?", ("us_pause", "Pause Low Priority", "Top work keeps full speed."), ("us_slow", "Slow Everyone", "All agents keep going, slower."))
P(G, "Helper Agents: Spin Up Freely Or Keep To A Minimum?", ("us_free", "Spin Up Freely", "Faster parallel work."), ("us_min", "Keep To A Minimum", "One batched pass."))
P(G, "Screenshots On Every Publish Or Only On Big Changes?", ("us_every", "Every Publish", "Always verified."), ("us_big", "Big Changes Only", "Saves usage."))
P(G, "Usage Report To Max: Daily Line Or Weekly Summary?", ("us_daily", "Daily Line", "One line in the Evening Report."), ("us_week", "Weekly Summary", "Trends once a week."))
G = "Follow-through & Reporting"
P(G, "How Much Detail In Updates: Short Headline Or Full Detail?", ("fr_short", "Short Headline", "One line each, details on tap."), ("fr_full", "Full Detail", "Everything spelled out."))
P(G, "Morning Brief Format: Bullet List Or Short Story?", ("fr_bul", "Bullet List", "Scannable items."), ("fr_story", "Short Story", "A few plain sentences."))
P(G, "Decisions Needed: Grouped By Agent Or By Urgency?", ("fr_agent", "By Agent", "One group per agent."), ("fr_urg", "By Urgency", "Most urgent first, any agent."))
P(G, "Unanswered Question To Max: Re-Ask Next Day Or Wait?", ("fr_reask", "Re-Ask Next Day", "Carry it into the next brief."), ("fr_wait", "Wait For Max", "No repeat nudges."))
P(G, "Done Work: Confirm Each Item Or Weekly Wrap-Up?", ("fr_each", "Confirm Each", "A Done note per item."), ("fr_wrap", "Weekly Wrap-Up", "One list of what shipped."))
N = len(pairs); assert N == 20, N
cnt = {}
for p in pairs: cnt[p["group"]] = cnt.get(p["group"], 0) + 1
publish("ceo-management", "CEO Management Deck", "Grok Bot", pairs,
        {"brands": ["How Grok Bot runs Max's agent team as CEO", "Light cream page, white cards"],
         "submit_agent": "grok-bot", "submit_to": "Grok Bot", "section_counts": cnt, "deck_size": N, "one_card_per_screen": True,
         "categories": list(cnt)}, seed=1014, n=N)
