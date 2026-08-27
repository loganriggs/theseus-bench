# tools/ — session ergonomics for the two-agent loop

Small helpers that sit *around* the existing bilin18 infrastructure. They do not
replace any of it. Before adding anything here, read what already exists:

| Concern | Where it already lives |
|---|---|
| Rebuild a recycled box | `tensor_language/…/bilinear_quotient/ops/restore.sh` |
| Claude ↔ Codex channel | `tensor_language/AGENT_BOARD.md` (append-only) |
| Experiment dispatch | `queue.txt` / `queue2.txt`, drained by `bqrunner` / `bqrunner2` |
| Run logs and completions | `…/bilinear_quotient/runlogs/`, `_completed.txt` |
| Session bootstrap + wave loop | `…/bilinear_quotient/SWARM_RUNBOOK.md` |
| GPU loss recovery | watchdog inside `ops/bqrunner.sh` (auto `vastai reboot`) |

**Do not add a second message board, a second queue, or a second restore script.**
That was tried on 2026-08-27 and reverted before it landed — two channels means
half the messages get missed.

## Rebuilding after a recycle

`${WORKSPACE}` is **not** volume-backed here (`workspace_is_volume: false`), so a
recycle wipes everything except what is pushed to git. The documented path:

```bash
git clone https://github.com/loganriggs/tensor_language.git /workspace/tensor_language
bash /workspace/tensor_language/basis_aligned/bilinear_quotient/ops/restore.sh
```

~5 min: venv (cu128 wheels — the 5090 is sm_120), rspd, the five Elriggs
checkpoints into `$HF_HOME`, FineWeb warm-up, the bqrunner services, and the
canary as the gate.

What `restore.sh` explicitly does **not** restore, because it cannot: the wake
cron and any monitors. Those are session-only — recreate them per
`SWARM_RUNBOOK.md` §0.

## Two-agent tmux session

```bash
tools/dev-session.sh          # attach (creates the session if needed)
tools/dev-session.sh kill     # tear down
```

Claude left, codex right. Mouse mode on; `Ctrl-b o` toggles panes, `Ctrl-b z`
zooms one fullscreen, `Ctrl-b d` detaches. **The session survives ssh drops** —
reattach and both agents are still there. This is the fix for losing a session to
a dropped connection; it does nothing about a recycle, where only git survives.

## Monitors (session-only — re-arm each session)

- **`watch_board.sh`** — `ME=Claude tools/watch_board.sh`. Notifies on new
  `AGENT_BOARD.md` entries by *other* agents. Pulls before checking, since
  entries arrive by push. Byte-offset polling, not `tail -f`: `git pull` replaces
  the file wholesale and breaks an inode-following tail.
- **`watch_runs.sh`** — watches `runlogs/_completed.txt` for every terminal state
  (calling out `exit != 0` separately) plus result and failure lines in the live
  logs.
- **`watch_gpu.sh`** — fires on GPU busy↔free transitions. Keys on CUDA compute
  processes holding memory, not utilization percent — utilization dips to 0
  between steps of a healthy run and would flap all night. Debounced over 3 polls.

The failure signatures in these filters are deliberate. A monitor that matches
only the happy path goes silent through a crashloop, and silence is
indistinguishable from "still running".

## Channel conventions (from AGENT_BOARD.md)

- Append-only, newest last, headed `### <UTC timestamp> — <agent>`. Never edit
  another agent's entry.
- `git pull --rebase origin main` before every push. Never force-push main.
- Claim multi-commit work with a one-line entry before starting.
- Lane 1 (`queue.txt`) is Claude's; lane 2 (`queue2.txt`) is Codex's when granted.
- The runner pops queue lines **even while the GPU is dead** and the run just
  fails — so queue only once a canary shows `exit=0`, or requeue on failure.
