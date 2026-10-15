#!/usr/bin/env bash
# Keeps Apps Home "decks today" current while the Deck Results Router is paused (Max Oct 15 2026).
# One pass: pull every agent's submissions into ops/submit/inbox (read only, no routing), rebuild swipe-stats.json,
# sync kit/swipe-stats.json + kit/deck-counts.json, commit + push only those two files when they changed.
# Loop: tools/refresh_deck_counts.sh --loop  (every 10 min; log /tmp/refresh_deck_counts.log)
set -uo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)"; S=/workspace/ops/submit
once(){
  for a in "$S"/inbox/*/; do a="$(basename "$a")"; [[ "$a" == *. ]] && continue; "$S/pull.sh" "$a" >/dev/null 2>&1 || true; done
  python3 "$S/swipe_stats.py" >/dev/null && python3 "$R/tools/sync_swipe_stats.py" >/dev/null
  cd "$R" && git add kit/swipe-stats.json kit/deck-counts.json
  git diff --cached --quiet -- kit/swipe-stats.json kit/deck-counts.json || { git commit -qm "kit: refresh swipe stats + deck counts $(TZ=Asia/Bangkok date '+%F %H:%M') ICT" -- kit/swipe-stats.json kit/deck-counts.json && git pull -q --rebase --autostash && git push -q; }
  echo "$(date '+%F %T') ok"
}
if [ "${1:-}" = "--loop" ]; then while true; do once; sleep 600; done; else once; fi
