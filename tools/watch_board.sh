#!/usr/bin/env bash
# Notify on new AGENT_BOARD.md entries written by another agent.
#
#   ME=Claude tools/watch_board.sh
#
# AGENT_BOARD.md (in the tensor_language repo) is the Claude<->Codex channel:
# append-only, entries headed `### <UTC timestamp> - <agent>`.
#
# IMPORTANT: this reads the board out of `origin/main` via `git show`, and never
# touches the working tree. An earlier version used `git pull --rebase`, which
# FAILS whenever the bqrunner lanes have result JSONs and runlogs checked out
# dirty -- i.e. exactly whenever experiments are running. On failure the watcher
# fell back to reading a stale local file and went quiet, which is
# indistinguishable from "Codex has not posted". Fetch + show has no such mode.

TL=${TL:-/workspace/tensor_language}
ME=${ME:-Claude}
POLL=${POLL:-60}
CACHE=$(mktemp)
NEXT=$(mktemp)
trap 'rm -f "$CACHE" "$NEXT"' EXIT

git -C "$TL" fetch -q origin main 2>/dev/null
git -C "$TL" show origin/main:AGENT_BOARD.md > "$CACHE" 2>/dev/null || : > "$CACHE"

while true; do
  if git -C "$TL" fetch -q origin main 2>/dev/null &&
     git -C "$TL" show origin/main:AGENT_BOARD.md > "$NEXT" 2>/dev/null &&
     [ -s "$NEXT" ]; then

    if ! cmp -s "$CACHE" "$NEXT"; then
      # append-only board: the added lines are the new entries
      diff "$CACHE" "$NEXT" | sed -n 's/^> //p' | ME="$ME" python3 -c '
import sys, os, re
me = os.environ["ME"].lower()
text = sys.stdin.read()
parts = re.split(r"^(### .*)$", text, flags=re.M)
for i in range(1, len(parts), 2):
    header = parts[i].strip()
    body = " ".join(parts[i + 1].split())[:400] if i + 1 < len(parts) else ""
    # header form: "### <timestamp> - <agent>"; author is the trailing field
    author = re.split(r"[-—]", header)[-1].strip().lower()
    if author.startswith(me):        # our own entry, do not echo back
        continue
    print(f"[board] {header}\n        {body}")
'
      cp "$NEXT" "$CACHE"
    fi
  fi
  sleep "$POLL"
done
