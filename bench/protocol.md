# Protocol (practice build, v0)
- Substrate: bilin18 (Elriggs/gpt2-bilinear-sqrd-attn-18l-9h-1152embd), D=1152, T=256.
- Dev split: FineWeb rows skip=80 (fit) — public iteration data.
- Eval split: FineWeb rows skip=7000, 960 rows, CE on positions >= 64 (184,320
  positions). Private + OOD splits: M2.
- Anchors: per-component mean constant + optimal constant (Adam 3e-3, mean-init,
  150 steps MLPs/attn layers, 100 heads, batch 8) — see bench/anchors/_meta.json.
- Fidelity: (delta_opt - delta_repl) / delta_opt. Optimal constant = 0, identity = 1.
- Head convention: a head's "output" is its 128-dim c_proj input slice.

## Handle scores (three-property evaluation of a compression)

A compression is judged not only by fidelity x simplicity but by whether its parts
work as OPERATIONAL HANDLES (user directive 2026-08-26). For a basis B at a site:

- **Extraction**: replace the module's output with mean + its B-subspace component.
  Score = fraction of a target CLASS effect kept vs fraction of the global effect
  kept; the ratio is the basis's SELECTIVITY.
- **Removal**: subtract the B-subspace component. Score = CE cost vs a random
  subspace of the same rank (specificity control).
- **Generalization**: both scores must replicate on a disjoint row set with the same
  sign and >= half magnitude, no refit.

Reference results (bilin18, mlp0's block-1 channel, S1486-88): weight-composed
basis = selectivity 3.8-4.3x, PCA = 1.2-1.3x but higher raw coverage; random = inert.
Single named axes fail as handles (S1484) — the operational grain is 8-32 direction
channels. Suite template: basis_aligned/bilinear_quotient/channel_circuit.py +
channel_generalize.py (program repo); repeatable scorecard: handle_score_mlp1.py.
