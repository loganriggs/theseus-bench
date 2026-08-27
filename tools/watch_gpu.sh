#!/usr/bin/env bash
# Emit an event when the GPU transitions between busy and free.
#
# "Busy" = at least one CUDA compute process holds memory. That is a far more
# reliable signal than utilization%, which dips to 0 between steps of a live run
# and would otherwise flap constantly.
#
# Transitions are debounced over DEBOUNCE consecutive polls so that the gap
# between two back-to-back python invocations in one experiment script does not
# read as "the run finished".

POLL=20
DEBOUNCE=3

state=""      # current confirmed state: busy | free
cand=""       # state we are currently counting toward
count=0

while true; do
  apps=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null)
  if [ -n "$apps" ]; then now=busy; else now=free; fi

  if [ "$now" = "$cand" ]; then
    count=$((count + 1))
  else
    cand=$now
    count=1
  fi

  if [ "$count" -ge "$DEBOUNCE" ] && [ "$now" != "$state" ]; then
    ts=$(date -u +%H:%M:%SZ)
    if [ "$now" = "busy" ]; then
      echo "[$ts] GPU BUSY — run started: $(echo "$apps" | tr '\n' ';')"
    else
      # only meaningful once we have actually seen a run; skip the initial boot report
      if [ -n "$state" ]; then
        echo "[$ts] GPU FREE — run ended (crashed or completed). Check the run log, record results, launch the next queued experiment."
      fi
    fi
    state=$now
  fi

  sleep "$POLL"
done
