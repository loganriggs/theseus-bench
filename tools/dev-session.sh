#!/usr/bin/env bash
# Start (or re-attach to) the two-agent tmux session: claude | codex.
#
#   ./dev.sh          -> attach, creating the session if needed
#   ./dev.sh kill     -> tear the session down
#
# Detach with Ctrl-b then d. The session keeps running after you detach or
# after ssh drops; re-run ./dev.sh to get back to it.

set -euo pipefail

SESSION=dev
WORKDIR=/workspace/theseus-bench
NVM_INIT='. /opt/nvm/nvm.sh'

if [ "${1:-}" = "kill" ]; then
  tmux kill-session -t "$SESSION" 2>/dev/null && echo "killed $SESSION" || echo "no $SESSION session"
  exit 0
fi

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  # pane 1 (left): claude, resuming the most recent conversation in this repo
  tmux new-session -d -s "$SESSION" -c "$WORKDIR" \
    "$NVM_INIT; printf '\033]2;claude\033\\'; claude --continue || claude; exec bash"

  # pane 2 (right): codex
  tmux split-window -h -t "$SESSION" -c "$WORKDIR" \
    "$NVM_INIT; printf '\033]2;codex\033\\'; codex; exec bash"

  tmux select-pane -t "$SESSION".1
fi

exec tmux attach -t "$SESSION"
