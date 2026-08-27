#!/usr/bin/env bash
# Notify on new AGENT_BOARD.md entries written by another agent.
#
#   ME=Claude tools/watch_board.sh
#
# AGENT_BOARD.md (in the tensor_language repo) is the real Claude<->Codex
# channel. It is append-only, entries headed `### <UTC timestamp> — <agent>`.
# Other agents push their entries, so this pulls before checking.
#
# Byte-offset polling rather than `tail -f`: the file is replaced wholesale by
# `git pull`, which breaks an inode-following tail.

TL=${TL:-/workspace/tensor_language}
BOARD="$TL/AGENT_BOARD.md"
ME=${ME:-Claude}
POLL=${POLL:-60}

[ -f "$BOARD" ] || { echo "no board at $BOARD"; exit 1; }

offset=$(stat -c %s "$BOARD")

while true; do
  # the board lives in git; other agents' entries arrive by push
  git -C "$TL" pull --rebase --quiet origin main 2>/dev/null

  size=$(stat -c %s "$BOARD" 2>/dev/null || echo 0)
  if [ "$size" -lt "$offset" ]; then offset=0; fi   # rebase rewrote the file

  if [ "$size" -gt "$offset" ]; then
    tail -c +$((offset + 1)) "$BOARD" 2>/dev/null | ME="$ME" python3 -c '
import sys, os, re
me = os.environ["ME"].lower()
text = sys.stdin.read()
# split on entry headers, keep the header with its body
parts = re.split(r"^(### .*)$", text, flags=re.M)
for i in range(1, len(parts), 2):
    header = parts[i].strip()
    body = " ".join(parts[i + 1].split())[:400] if i + 1 < len(parts) else ""
    author = header.split("—")[-1].strip().lower() if "—" in header else ""
    if author.startswith(me):        # our own entry, do not echo back
        continue
    print(f"[board] {header}\n        {body}")
'
    offset=$size
  fi
  sleep "$POLL"
done
