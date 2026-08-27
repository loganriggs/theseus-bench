#!/usr/bin/env bash
# Watch the bqrunner lanes: completions, results, and failures.
#
# The runners (ops/bqrunner.sh, ops/bqrunner2.sh) pop absolute paths from
# queue.txt / queue2.txt, write per-script logs to runlogs/<name>.log, and
# append "HH:MM <name> exit=N" to runlogs/_completed.txt.
#
# Coverage note: this greps failure signatures as well as result lines on
# purpose. A watcher matching only the happy path stays silent through a
# crashloop, and silence is indistinguishable from "still running" — which on a
# billed GPU is the expensive mistake.

BQ=${BQ:-/workspace/tensor_language/basis_aligned/bilinear_quotient}
RUNLOGS="$BQ/runlogs"
POLL=${POLL:-15}
PATTERN='Traceback|CUDA out of memory|OutOfMemoryError|Killed|no kernel image|NVML|Unknown Error|FAILED|UNEVALUABLE|PASS|FAIL|selectivity|class_rise|held-out|NR=1920'

mkdir -p "$RUNLOGS"
declare -A offset

# Seed every log that already exists, SILENTLY. The repo carries ~1000 historical
# runlogs from previous sessions; announcing them as "new" floods the channel and
# gets the monitor rate-limited. Only files created after startup are events.
for f in "$RUNLOGS"/*.log; do
  [ -e "$f" ] || continue
  offset[$f]=$(stat -c %s "$f" 2>/dev/null || echo 0)
done

# _completed.txt is the authoritative "a run ended" signal, including exit!=0
COMPLETED="$RUNLOGS/_completed.txt"
touch "$COMPLETED"
comp_offset=$(stat -c %s "$COMPLETED")

while true; do
  # 1. completions (every terminal state, not just exit=0)
  size=$(stat -c %s "$COMPLETED" 2>/dev/null || echo 0)
  if [ "$size" -lt "$comp_offset" ]; then comp_offset=0; fi
  if [ "$size" -gt "$comp_offset" ]; then
    tail -c +$((comp_offset + 1)) "$COMPLETED" | while read -r line; do
      [ -z "$line" ] && continue
      case "$line" in
        *exit=0*) echo "[runner] COMPLETED $line — write it up, commit, push" ;;
        *)        echo "[runner] NONZERO EXIT $line — check runlogs, requeue or fix" ;;
      esac
    done
    comp_offset=$size
  fi

  # 2. result and failure lines from the live logs
  for f in "$RUNLOGS"/*.log; do
    [ -e "$f" ] || continue
    name=$(basename "$f")
    case "$name" in runner.log|*watchdog*) continue ;; esac

    if [ -z "${offset[$f]+x}" ]; then
      echo "[runner] new log: $name"
      # scan from the top, not from the current end: a run that crashes in its
      # first seconds must not have its traceback skipped
      offset[$f]=0
    fi

    size=$(stat -c %s "$f" 2>/dev/null || echo 0)
    if [ "$size" -lt "${offset[$f]}" ]; then offset[$f]=0; fi   # truncated per run
    if [ "$size" -gt "${offset[$f]}" ]; then
      tail -c +$(( ${offset[$f]} + 1 )) "$f" 2>/dev/null \
        | grep -E --line-buffered "$PATTERN" \
        | sed "s/^/[$name] /"
      offset[$f]=$size
    fi
  done

  sleep "$POLL"
done
