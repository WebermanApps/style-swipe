#!/bin/sh
# Build-time checks for style-swipe. Fails (exit 1) if the card-media max-height:100% rule returns.
# Run after any build/refresh and before push; also runs in CI (.github/workflows/media-rule.yml).
set -e
cd "$(dirname "$0")/.."
python3 tools/media_rule.py check
