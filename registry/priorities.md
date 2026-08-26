# Priority board — where to start looking

Ranked by **unexplained global CE** = Δ_opt × (1 − best fidelity).
A low-importance head at 100% understood ranks below a big MLP at 50%.
Anchors from the optimal-ablation sweep (198/198 components so far;
attention layers land last). Generated 2026-08-26 01:13 UTC; regenerate with
`python bench/make_priorities.py` after any frontier move or sweep progress.

## Top targets

1. **mlp1** — unexplained 0.181 nats (Δ_opt 7.253, fidelity 0.97) — tok table + residual ridge [attn1,mlp0] + quad, fid_opt, S1438
2. **mlp0** — unexplained 0.062 nats (Δ_opt 0.908, fidelity 0.93) — tok map + residual ridge [attn0,embed] + quad, fid_opt, S1439
3. **attn2** — unexplained 0.051 nats (Δ_opt 0.159, fidelity 0.68) — distance kernel S1447
4. **mlp17** — unexplained 0.048 nats (Δ_opt 0.332, fidelity 0.86) — linread+quad, S1443
5. **mlp8** — unexplained 0.047 nats (Δ_opt 0.047, fidelity 0.00) — baseline zoo only
6. **mlp11** — unexplained 0.046 nats (Δ_opt 0.046, fidelity 0.00) — baseline zoo only
7. **attn3** — unexplained 0.044 nats (Δ_opt 0.116, fidelity 0.62) — distance kernel S1447
8. **attn4** — unexplained 0.042 nats (Δ_opt 0.223, fidelity 0.81) — distance kernel S1446
9. **mlp12** — unexplained 0.042 nats (Δ_opt 0.042, fidelity 0.00) — baseline zoo only
10. **mlp10** — unexplained 0.041 nats (Δ_opt 0.041, fidelity 0.00) — baseline zoo only

## Full table

| component | Δ_opt | best fidelity | unexplained CE | current best |
|---|---|---|---|---|
| mlp1 | 7.2533 | 0.97 | 0.1813 | tok table + residual ridge [attn1,mlp0] + quad, fid_opt, S1438 |
| mlp0 | 0.9080 | 0.93 | 0.0617 | tok map + residual ridge [attn0,embed] + quad, fid_opt, S1439 |
| attn2 | 0.1585 | 0.68 | 0.0510 | distance kernel S1447 |
| mlp17 | 0.3323 | 0.86 | 0.0479 | linread+quad, S1443 |
| mlp8 | 0.0474 | 0.00 | 0.0474 | baseline zoo only |
| mlp11 | 0.0460 | 0.00 | 0.0460 | baseline zoo only |
| attn3 | 0.1162 | 0.62 | 0.0438 | distance kernel S1447 |
| attn4 | 0.2226 | 0.81 | 0.0421 | distance kernel S1446 |
| mlp12 | 0.0416 | 0.00 | 0.0416 | baseline zoo only |
| mlp10 | 0.0409 | 0.00 | 0.0409 | baseline zoo only |
| mlp2 | 0.7260 | 0.94 | 0.0407 | lin2+quad S1437; rank frontier S1440 (r128 .82@7Mbit) |
| attn1 | 0.2186 | 0.82 | 0.0401 | distance kernel S1446 |
| mlp13 | 0.0393 | 0.00 | 0.0393 | baseline zoo only |
| mlp15 | 0.0379 | 0.00 | 0.0379 | baseline zoo only |
| mlp4 | 0.1051 | 0.69 | 0.0326 | lin5 ridge on [attn4,mlp0-3], opt-anchored, S1428/S1433 |
| mlp3 | 0.6099 | 0.95 | 0.0305 | own-basis projection r256, S1130 |
| attn6 | 0.0642 | 0.53 | 0.0301 | distance kernel S1447 |
| mlp14 | 0.0301 | 0.00 | 0.0301 | baseline zoo only |
| mlp6 | 0.0760 | 0.62 | 0.0289 | ladder linall+quad, S1436 |
| mlp5 | 0.0821 | 0.65 | 0.0287 | linall+quad ladder, S1434 |
| mlp7 | 0.0563 | 0.52 | 0.0272 | linall ridge + r256/F8192 quad over [attn7,mlp6], fid_opt, S1451 |
| attn11 | 0.0460 | 0.42 | 0.0268 | distance kernel S1447 |
| mlp16 | 0.1399 | 0.81 | 0.0266 | fitted linear read, S1131-32 |
| mlp9 | 0.0496 | 0.52 | 0.0238 | linall ridge + r256/F8192 quad over [attn9,mlp8], fid_opt, S1457 |
| attn7 | 0.0594 | 0.60 | 0.0236 | distance kernel S1447 |
| attn9 | 0.0640 | 0.69 | 0.0197 | distance kernel S1447 |
| attn0 | 0.2395 | 0.95 | 0.0120 | token+position pattern + per-token value table, sink arc (~1.00 claimed; conservatively seeded) |
| attn5 | 0.1362 | 0.92 | 0.0105 | roster-live 5.7 + whitened r32 QK others, 30.4 Mbit, S1472 |
| head6.3 | 0.0211 | 0.53 | 0.0099 | inherited from attn6 stand-in |
| head2.5 | 0.0284 | 0.68 | 0.0091 | inherited from attn2 stand-in |
| attn12 | 0.0095 | 0.21 | 0.0075 | distance kernel S1447 |
| head7.8 | 0.0180 | 0.60 | 0.0072 | inherited from attn7 stand-in |
| head11.2 | 0.0103 | 0.42 | 0.0060 | inherited from attn11 stand-in |
| head6.1 | 0.0128 | 0.53 | 0.0060 | inherited from attn6 stand-in |
| head11.6 | 0.0102 | 0.42 | 0.0059 | inherited from attn11 stand-in |
| head9.7 | 0.0191 | 0.69 | 0.0059 | inherited from attn9 stand-in |
| head7.0 | 0.0136 | 0.60 | 0.0054 | inherited from attn7 stand-in |
| attn15 | 0.0074 | 0.28 | 0.0053 | distance kernel S1447 |
| head1.1 | 0.0259 | 0.82 | 0.0048 | inherited from attn1 stand-in |
| head3.5 | 0.0109 | 0.62 | 0.0041 | inherited from attn3 stand-in |
| head3.8 | 0.0106 | 0.62 | 0.0040 | inherited from attn3 stand-in |
| head6.7 | 0.0076 | 0.53 | 0.0036 | inherited from attn6 stand-in |
| head2.6 | 0.0102 | 0.68 | 0.0033 | inherited from attn2 stand-in |
| attn8 | 0.0479 | 0.93 | 0.0031 | roster-live 8.{1,2,3,7} + whitened r32 QK others, 50.7 Mbit, S1472 |
| head0.3 | 0.0621 | 0.95 | 0.0031 | inherited from attn0 stand-in |
| head2.3 | 0.0094 | 0.68 | 0.0030 | inherited from attn2 stand-in |
| attn14 | 0.0296 | 0.90 | 0.0030 | per-head rank-32 QK, xin-whitened, 23.6 Mbit, S1469 |
| head2.2 | 0.0083 | 0.68 | 0.0027 | inherited from attn2 stand-in |
| head4.0 | 0.0133 | 0.81 | 0.0025 | inherited from attn4 stand-in |
| head3.4 | 0.0065 | 0.62 | 0.0025 | inherited from attn3 stand-in |
| attn17 | 0.0118 | 0.80 | 0.0024 | per-head rank-32 QK, plain SVD, 23.6 Mbit, S1469 |
| head4.5 | 0.0125 | 0.81 | 0.0024 | inherited from attn4 stand-in |
| head1.4 | 0.0126 | 0.82 | 0.0023 | inherited from attn1 stand-in |
| head4.1 | 0.0114 | 0.81 | 0.0022 | inherited from attn4 stand-in |
| head3.6 | 0.0057 | 0.62 | 0.0021 | inherited from attn3 stand-in |
| attn10 | 0.0263 | 0.92 | 0.0021 | per-head rank-32 QK, xin-whitened, 23.6 Mbit, S1469 |
| head11.3 | 0.0036 | 0.42 | 0.0021 | inherited from attn11 stand-in |
| head3.0 | 0.0055 | 0.62 | 0.0021 | inherited from attn3 stand-in |
| head2.7 | 0.0062 | 0.68 | 0.0020 | inherited from attn2 stand-in |
| head11.1 | 0.0034 | 0.42 | 0.0020 | inherited from attn11 stand-in |
| attn13 | 0.0164 | 0.89 | 0.0017 | per-head rank-32 QK, xin-whitened, 23.6 Mbit, S1469 |
| head1.3 | 0.0094 | 0.82 | 0.0017 | inherited from attn1 stand-in |
| head4.7 | 0.0089 | 0.81 | 0.0017 | inherited from attn4 stand-in |
| head15.1 | 0.0023 | 0.28 | 0.0017 | inherited from attn15 stand-in |
| head3.3 | 0.0039 | 0.62 | 0.0015 | inherited from attn3 stand-in |
| head11.5 | 0.0025 | 0.42 | 0.0015 | inherited from attn11 stand-in |
| attn16 | 0.0135 | 0.90 | 0.0014 | kernel+committee live S1448 |
| head2.8 | 0.0043 | 0.68 | 0.0014 | inherited from attn2 stand-in |
| head9.8 | 0.0044 | 0.69 | 0.0014 | inherited from attn9 stand-in |
| head1.8 | 0.0073 | 0.82 | 0.0013 | inherited from attn1 stand-in |
| head9.6 | 0.0042 | 0.69 | 0.0013 | inherited from attn9 stand-in |
| head9.1 | 0.0041 | 0.69 | 0.0013 | inherited from attn9 stand-in |
| head11.8 | 0.0020 | 0.42 | 0.0012 | inherited from attn11 stand-in |
| head7.1 | 0.0027 | 0.60 | 0.0011 | inherited from attn7 stand-in |
| head7.2 | 0.0026 | 0.60 | 0.0010 | inherited from attn7 stand-in |
| head3.7 | 0.0026 | 0.62 | 0.0010 | inherited from attn3 stand-in |
| head5.5 | 0.0125 | 0.92 | 0.0010 | inherited from attn5 stand-in |
| head7.3 | 0.0024 | 0.60 | 0.0010 | inherited from attn7 stand-in |
| head6.5 | 0.0020 | 0.53 | 0.0009 | inherited from attn6 stand-in |
| head1.5 | 0.0051 | 0.82 | 0.0009 | inherited from attn1 stand-in |
| head3.1 | 0.0024 | 0.62 | 0.0009 | inherited from attn3 stand-in |
| head2.0 | 0.0027 | 0.68 | 0.0009 | inherited from attn2 stand-in |
| head7.7 | 0.0021 | 0.60 | 0.0008 | inherited from attn7 stand-in |
| head7.5 | 0.0021 | 0.60 | 0.0008 | inherited from attn7 stand-in |
| head14.4 | 0.0075 | 0.90 | 0.0008 | inherited from attn14 stand-in |
| head8.3 | 0.0107 | 0.93 | 0.0007 | inherited from attn8 stand-in |
| head5.6 | 0.0085 | 0.92 | 0.0007 | inherited from attn5 stand-in |
| head5.3 | 0.0085 | 0.92 | 0.0007 | inherited from attn5 stand-in |
| head1.7 | 0.0034 | 0.82 | 0.0006 | inherited from attn1 stand-in |
| head5.8 | 0.0080 | 0.92 | 0.0006 | inherited from attn5 stand-in |
| head4.6 | 0.0032 | 0.81 | 0.0006 | inherited from attn4 stand-in |
| head4.4 | 0.0032 | 0.81 | 0.0006 | inherited from attn4 stand-in |
| head4.8 | 0.0030 | 0.81 | 0.0006 | inherited from attn4 stand-in |
| head13.0 | 0.0053 | 0.89 | 0.0006 | inherited from attn13 stand-in |
| head17.2 | 0.0028 | 0.80 | 0.0006 | inherited from attn17 stand-in |
| head4.3 | 0.0029 | 0.81 | 0.0005 | inherited from attn4 stand-in |
| head13.8 | 0.0039 | 0.89 | 0.0004 | inherited from attn13 stand-in |
| head10.5 | 0.0052 | 0.92 | 0.0004 | inherited from attn10 stand-in |
| head5.0 | 0.0049 | 0.92 | 0.0004 | inherited from attn5 stand-in |
| head8.1 | 0.0055 | 0.93 | 0.0004 | inherited from attn8 stand-in |
| head16.3 | 0.0034 | 0.90 | 0.0003 | inherited from attn16 stand-in |
| head14.6 | 0.0034 | 0.90 | 0.0003 | inherited from attn14 stand-in |
| head5.2 | 0.0037 | 0.92 | 0.0003 | inherited from attn5 stand-in |
| head8.4 | 0.0041 | 0.93 | 0.0003 | inherited from attn8 stand-in |
| head10.2 | 0.0030 | 0.92 | 0.0002 | inherited from attn10 stand-in |
| head5.4 | 0.0031 | 0.92 | 0.0002 | inherited from attn5 stand-in |
| head16.0 | 0.0023 | 0.90 | 0.0002 | inherited from attn16 stand-in |
| head14.0 | 0.0022 | 0.90 | 0.0002 | inherited from attn14 stand-in |
| head8.8 | 0.0034 | 0.93 | 0.0002 | inherited from attn8 stand-in |
| head16.4 | 0.0021 | 0.90 | 0.0002 | inherited from attn16 stand-in |
| head8.7 | 0.0033 | 0.93 | 0.0002 | inherited from attn8 stand-in |
| head10.4 | 0.0027 | 0.92 | 0.0002 | inherited from attn10 stand-in |
| head0.8 | 0.0043 | 0.95 | 0.0002 | inherited from attn0 stand-in |
| head5.1 | 0.0027 | 0.92 | 0.0002 | inherited from attn5 stand-in |
| head0.6 | 0.0041 | 0.95 | 0.0002 | inherited from attn0 stand-in |
| head5.7 | 0.0119 | 0.98 | 0.0002 | ONE fixed vector (the bias-head), S1089/S1091 |
| head8.2 | 0.0026 | 0.93 | 0.0002 | inherited from attn8 stand-in |
| head0.7 | 0.0034 | 0.95 | 0.0002 | inherited from attn0 stand-in |
