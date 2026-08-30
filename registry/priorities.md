# Priority board — where to start looking

Ranked by **unexplained global CE** = Δ_opt × (1 − best fidelity).
A low-importance head at 100% understood ranks below a big MLP at 50%.
Anchors from the optimal-ablation sweep (198/198 components so far;
attention layers land last). Generated 2026-08-26 10:42 UTC; regenerate with
`python bench/make_priorities.py` after any frontier move or sweep progress.

## Top targets

1. **mlp1** — unexplained 0.181 nats (Δ_opt 7.253, fidelity 0.97) — tok table + residual ridge [attn1,mlp0] + quad, fid_opt, S1438
2. **mlp0** — unexplained 0.062 nats (Δ_opt 0.908, fidelity 0.93) — tok map + residual ridge [attn0,embed] + quad, fid_opt, S1439
3. **mlp2** — unexplained 0.041 nats (Δ_opt 0.726, fidelity 0.94) — lin2+quad S1437; rank frontier S1440 (r128 .82@7Mbit)
4. **mlp3** — unexplained 0.030 nats (Δ_opt 0.610, fidelity 0.95) — own-basis projection r256, S1130
5. **attn0** — unexplained 0.011 nats (Δ_opt 0.239, fidelity 0.96) — whitened per-head r32 QK, 23.6 Mbit, S1474
6. **attn5** — unexplained 0.011 nats (Δ_opt 0.136, fidelity 0.92) — roster-live 5.7 + whitened r32 QK others, 30.4 Mbit, S1472
7. **attn3** — unexplained 0.010 nats (Δ_opt 0.116, fidelity 0.91) — whitened per-head r32 QK, 23.6 Mbit, S1474
8. **attn2** — unexplained 0.010 nats (Δ_opt 0.159, fidelity 0.94) — whitened per-head r32 QK, 23.6 Mbit, S1474
9. **mlp17** — unexplained 0.009 nats (Δ_opt 0.332, fidelity 0.97) — top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541
10. **attn1** — unexplained 0.008 nats (Δ_opt 0.219, fidelity 0.96) — whitened per-head r32 QK, 23.6 Mbit, S1474

## Full table

| component | Δ_opt | best fidelity | unexplained CE | current best |
|---|---|---|---|---|
| mlp1 | 7.2533 | 0.97 | 0.1813 | tok table + residual ridge [attn1,mlp0] + quad, fid_opt, S1438 |
| mlp0 | 0.9080 | 0.93 | 0.0617 | tok map + residual ridge [attn0,embed] + quad, fid_opt, S1439 |
| mlp2 | 0.7260 | 0.94 | 0.0407 | lin2+quad S1437; rank frontier S1440 (r128 .82@7Mbit) |
| mlp3 | 0.6099 | 0.95 | 0.0305 | own-basis projection r256, S1130 |
| attn0 | 0.2395 | 0.96 | 0.0107 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn5 | 0.1362 | 0.92 | 0.0105 | roster-live 5.7 + whitened r32 QK others, 30.4 Mbit, S1472 |
| attn3 | 0.1162 | 0.91 | 0.0105 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn2 | 0.1585 | 0.94 | 0.0102 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| mlp17 | 0.3323 | 0.97 | 0.0093 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| attn1 | 0.2186 | 0.96 | 0.0079 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn11 | 0.0460 | 0.84 | 0.0072 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn4 | 0.2226 | 0.97 | 0.0065 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| mlp5 | 0.0821 | 0.93 | 0.0061 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp4 | 0.1051 | 0.94 | 0.0061 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp16 | 0.1399 | 0.96 | 0.0059 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp7 | 0.0563 | 0.90 | 0.0058 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp15 | 0.0379 | 0.85 | 0.0056 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp10 | 0.0409 | 0.87 | 0.0054 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp13 | 0.0393 | 0.86 | 0.0054 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp12 | 0.0416 | 0.87 | 0.0053 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp14 | 0.0301 | 0.83 | 0.0052 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp11 | 0.0460 | 0.89 | 0.0051 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp9 | 0.0496 | 0.90 | 0.0051 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp6 | 0.0760 | 0.94 | 0.0047 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| mlp8 | 0.0474 | 0.91 | 0.0044 | top-3072-unit sub-MLP zero-shot, 171 Mbit (PRICE-HEAVY; K=2048 = economic knee), S1541 |
| attn6 | 0.0642 | 0.94 | 0.0041 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn7 | 0.0594 | 0.95 | 0.0032 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn8 | 0.0479 | 0.93 | 0.0031 | roster-live 8.{1,2,3,7} + whitened r32 QK others, 50.7 Mbit, S1472 |
| attn14 | 0.0296 | 0.90 | 0.0030 | per-head rank-32 QK, xin-whitened, 23.6 Mbit, S1469 |
| head0.3 | 0.0621 | 0.96 | 0.0028 | inherited from attn0 stand-in |
| attn9 | 0.0640 | 0.96 | 0.0027 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn17 | 0.0118 | 0.80 | 0.0024 | per-head rank-32 QK, plain SVD, 23.6 Mbit, S1469 |
| attn10 | 0.0263 | 0.92 | 0.0021 | per-head rank-32 QK, xin-whitened, 23.6 Mbit, S1469 |
| head2.5 | 0.0284 | 0.94 | 0.0018 | inherited from attn2 stand-in |
| attn13 | 0.0164 | 0.89 | 0.0017 | per-head rank-32 QK, xin-whitened, 23.6 Mbit, S1469 |
| head11.2 | 0.0103 | 0.84 | 0.0016 | inherited from attn11 stand-in |
| head11.6 | 0.0102 | 0.84 | 0.0016 | inherited from attn11 stand-in |
| attn16 | 0.0135 | 0.90 | 0.0014 | kernel+committee live S1448 |
| head6.3 | 0.0211 | 0.94 | 0.0013 | inherited from attn6 stand-in |
| attn12 | 0.0095 | 0.89 | 0.0011 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| attn15 | 0.0074 | 0.86 | 0.0010 | whitened per-head r32 QK, 23.6 Mbit, S1474 |
| head3.5 | 0.0109 | 0.91 | 0.0010 | inherited from attn3 stand-in |
| head5.5 | 0.0125 | 0.92 | 0.0010 | inherited from attn5 stand-in |
| head7.8 | 0.0180 | 0.95 | 0.0010 | inherited from attn7 stand-in |
| head3.8 | 0.0106 | 0.91 | 0.0010 | inherited from attn3 stand-in |
| head1.1 | 0.0259 | 0.96 | 0.0009 | inherited from attn1 stand-in |
| head6.1 | 0.0128 | 0.94 | 0.0008 | inherited from attn6 stand-in |
| head9.7 | 0.0191 | 0.96 | 0.0008 | inherited from attn9 stand-in |
| head14.4 | 0.0075 | 0.90 | 0.0008 | inherited from attn14 stand-in |
| head7.0 | 0.0136 | 0.95 | 0.0007 | inherited from attn7 stand-in |
| head8.3 | 0.0107 | 0.93 | 0.0007 | inherited from attn8 stand-in |
| head5.6 | 0.0085 | 0.92 | 0.0007 | inherited from attn5 stand-in |
| head5.3 | 0.0085 | 0.92 | 0.0007 | inherited from attn5 stand-in |
| head2.6 | 0.0102 | 0.94 | 0.0007 | inherited from attn2 stand-in |
| head5.8 | 0.0080 | 0.92 | 0.0006 | inherited from attn5 stand-in |
| head2.3 | 0.0094 | 0.94 | 0.0006 | inherited from attn2 stand-in |
| head3.4 | 0.0065 | 0.91 | 0.0006 | inherited from attn3 stand-in |
| head13.0 | 0.0053 | 0.89 | 0.0006 | inherited from attn13 stand-in |
| head17.2 | 0.0028 | 0.80 | 0.0006 | inherited from attn17 stand-in |
| head11.3 | 0.0036 | 0.84 | 0.0006 | inherited from attn11 stand-in |
| head2.2 | 0.0083 | 0.94 | 0.0005 | inherited from attn2 stand-in |
| head11.1 | 0.0034 | 0.84 | 0.0005 | inherited from attn11 stand-in |
| head3.6 | 0.0057 | 0.91 | 0.0005 | inherited from attn3 stand-in |
| head3.0 | 0.0055 | 0.91 | 0.0005 | inherited from attn3 stand-in |
| head6.7 | 0.0076 | 0.94 | 0.0005 | inherited from attn6 stand-in |
| head1.4 | 0.0126 | 0.96 | 0.0005 | inherited from attn1 stand-in |
| head13.8 | 0.0039 | 0.89 | 0.0004 | inherited from attn13 stand-in |
| head10.5 | 0.0052 | 0.92 | 0.0004 | inherited from attn10 stand-in |
| head2.7 | 0.0062 | 0.94 | 0.0004 | inherited from attn2 stand-in |
| head11.5 | 0.0025 | 0.84 | 0.0004 | inherited from attn11 stand-in |
| head4.0 | 0.0133 | 0.97 | 0.0004 | inherited from attn4 stand-in |
| head5.0 | 0.0049 | 0.92 | 0.0004 | inherited from attn5 stand-in |
| head4.5 | 0.0125 | 0.97 | 0.0004 | inherited from attn4 stand-in |
| head8.1 | 0.0055 | 0.93 | 0.0004 | inherited from attn8 stand-in |
| head3.3 | 0.0039 | 0.91 | 0.0004 | inherited from attn3 stand-in |
| head16.3 | 0.0034 | 0.90 | 0.0003 | inherited from attn16 stand-in |
| head14.6 | 0.0034 | 0.90 | 0.0003 | inherited from attn14 stand-in |
| head1.3 | 0.0094 | 0.96 | 0.0003 | inherited from attn1 stand-in |
| head4.1 | 0.0114 | 0.97 | 0.0003 | inherited from attn4 stand-in |
| head15.1 | 0.0023 | 0.86 | 0.0003 | inherited from attn15 stand-in |
| head11.8 | 0.0020 | 0.84 | 0.0003 | inherited from attn11 stand-in |
| head5.2 | 0.0037 | 0.92 | 0.0003 | inherited from attn5 stand-in |
| head2.8 | 0.0043 | 0.94 | 0.0003 | inherited from attn2 stand-in |
| head8.4 | 0.0041 | 0.93 | 0.0003 | inherited from attn8 stand-in |
| head1.8 | 0.0073 | 0.96 | 0.0003 | inherited from attn1 stand-in |
| head4.7 | 0.0089 | 0.97 | 0.0003 | inherited from attn4 stand-in |
| head10.2 | 0.0030 | 0.92 | 0.0002 | inherited from attn10 stand-in |
| head5.4 | 0.0031 | 0.92 | 0.0002 | inherited from attn5 stand-in |
| head16.0 | 0.0023 | 0.90 | 0.0002 | inherited from attn16 stand-in |
| head3.7 | 0.0026 | 0.91 | 0.0002 | inherited from attn3 stand-in |
| head14.0 | 0.0022 | 0.90 | 0.0002 | inherited from attn14 stand-in |
| head8.8 | 0.0034 | 0.93 | 0.0002 | inherited from attn8 stand-in |
| head3.1 | 0.0024 | 0.91 | 0.0002 | inherited from attn3 stand-in |
| head16.4 | 0.0021 | 0.90 | 0.0002 | inherited from attn16 stand-in |
| head8.7 | 0.0033 | 0.93 | 0.0002 | inherited from attn8 stand-in |
| head10.4 | 0.0027 | 0.92 | 0.0002 | inherited from attn10 stand-in |
| head5.1 | 0.0027 | 0.92 | 0.0002 | inherited from attn5 stand-in |
| head0.8 | 0.0043 | 0.96 | 0.0002 | inherited from attn0 stand-in |
| head1.5 | 0.0051 | 0.96 | 0.0002 | inherited from attn1 stand-in |
| head0.6 | 0.0041 | 0.96 | 0.0002 | inherited from attn0 stand-in |
| head9.8 | 0.0044 | 0.96 | 0.0002 | inherited from attn9 stand-in |
| head5.7 | 0.0119 | 0.98 | 0.0002 | ONE fixed vector (the bias-head), S1089/S1091 |
| head9.6 | 0.0042 | 0.96 | 0.0002 | inherited from attn9 stand-in |
| head2.0 | 0.0027 | 0.94 | 0.0002 | inherited from attn2 stand-in |
| head9.1 | 0.0041 | 0.96 | 0.0002 | inherited from attn9 stand-in |
| head8.2 | 0.0026 | 0.93 | 0.0002 | inherited from attn8 stand-in |
| head0.7 | 0.0034 | 0.96 | 0.0002 | inherited from attn0 stand-in |
| head7.1 | 0.0027 | 0.95 | 0.0001 | inherited from attn7 stand-in |
| head7.2 | 0.0026 | 0.95 | 0.0001 | inherited from attn7 stand-in |
| head7.3 | 0.0024 | 0.95 | 0.0001 | inherited from attn7 stand-in |
| head6.5 | 0.0020 | 0.94 | 0.0001 | inherited from attn6 stand-in |
| head1.7 | 0.0034 | 0.96 | 0.0001 | inherited from attn1 stand-in |
| head7.7 | 0.0021 | 0.95 | 0.0001 | inherited from attn7 stand-in |
| head7.5 | 0.0021 | 0.95 | 0.0001 | inherited from attn7 stand-in |
| head4.6 | 0.0032 | 0.97 | 0.0001 | inherited from attn4 stand-in |
| head4.4 | 0.0032 | 0.97 | 0.0001 | inherited from attn4 stand-in |
| head4.8 | 0.0030 | 0.97 | 0.0001 | inherited from attn4 stand-in |
| head4.3 | 0.0029 | 0.97 | 0.0001 | inherited from attn4 stand-in |

## Notes — 2026-08-30 (observability arc, tensor_language §2101–§2124)

- **Unit-selection rows can be upgraded at zero price.** Every "top-K-unit sub-MLP" entry above selects units
  by output norm. tensor_language §2116/§2119/§2124 certified (eight fresh pile-10k windows) that ranking
  mlp4/mlp5's kept units by the top-8 eigen-directions of the loss-gradient (or true-Fisher with model-sampled
  labels — label-free) Gramian at the block after the MLP beats norm selection by a median +0.082–0.086 nat at
  identical stored values. The selector is 8×1152 values per site and needs weights + unlabeled inputs only.
  Candidate rows: the mlp4–mlp15 sub-MLP entries (mlp16/17 untested; c6–c9-style selection was NEGATIVE in the
  assembly context, §2106 — certify per row before crediting).
- **Projection/span programs must state coverage.** §2121/§2122: a program that replaces only a subspace of a
  module's output (rank-k span, dictionary target) can lower its measured cost arbitrarily by choosing a
  low-variance subspace (gain tracks covered variance at ρ = −0.976). Credit such entries as
  fidelity × covered-energy share, and record the share. The assembly's tail-span stand-ins over-credit by
  this factor; the sub-MLP rows here are full replacements and unaffected.
- The priority *ordering* above stands: across the certified arm's thirteen pieces, own-output error energy
  ranks CE recovery at ρ = 0.81 (§2117). The energy/price separation is attn5-internal (sink head 5.7).
