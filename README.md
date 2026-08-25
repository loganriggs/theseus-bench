# theseus-bench

The ship of Theseus, except every plank is replaced with a **glass** plank — the ship
must sail exactly as before, but you can see through it. Headline metric: how much of
the ship is glass?

This is the in-house practice build of the TheseusBench spec
(SPEC.md, v0.2), built against the
bilin18 546M bilinear substrate using the bilinear_quotient program's assets:

- **Anchors (§9)**: the 198-component optimal-ablation sweep (all MLPs, heads, attn
  layers; loss curves + data budget recorded) -> bench/anchors/ via
  bench/make_anchors.py once the sweep completes.
- **Baseline zoo**: mean constant + optimal constant per component (from the sweep);
  identity; k-cluster (from the program's class-table experiments).
- **Worked example (bias-head)**: head 5.7, the attention sink — ONE fixed vector
  scores ~0.985 (program §1089/§1091). Our literal bias-head.
- **Mode A pre-seeds**: mlp1 token table (~.93), mlp4 = W[attn4; mlp3] (fidelity .69
  opt-anchored, §1428/§1433), mlp16/17 linear reads (.81/.84).
- **Mode B pre-seeds**: the four certified family kits + removal tests (closer,
  comparative, question, capitalized) and the unified bill as the composite prototype.

Status (2026-08-25): **anchors FROZEN** — 198/198 components swept (median
opt/mean = .9964), bench/anchors/ + _meta.json are the fixed targets. Priority board
live at registry/priorities.md (unexplained CE = delta_opt x (1 - best fid); current
top: mlp1 .181, mlp0 .062, mlp7 .056). First VERIFIED plank: mlp1 tiered-token-table
+ rank-128 ridge = fid .9507 @ 96.6 Mbit (vs 255 Mbit module). Standing lesson from
the first all-18-attention composite: local fidelity does not compose — data-dependent
stand-in parts must be re-validated inside the composite.

The GPU program that generates entries lives in the tensor_language repo
(basis_aligned/bilinear_quotient/ — BILIN18_CONNECTION.md is the numbered ledger);
results freeze into this repo as anchors, registry seeds, and priced frontier entries.
