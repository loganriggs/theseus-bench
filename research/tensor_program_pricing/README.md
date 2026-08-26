# Canonical tensor-program pricing prototype

This research prototype is separate from `bench/complexity.py`. It tests a future
complexity policy without changing current frontier prices.

## Definition

For distortion budget `epsilon`, price the shortest canonical tensor program whose
quantized execution remains within that budget:

```
C_epsilon(f) = min [graph_bits + parameter_bits]
               subject to distortion(f, quantized_program) <= epsilon
```

The prototype uses an actual prefix-free compressed serialization as the bit count.
It canonicalizes two equivalence classes needed by the current bilin18 work:

- `linear` and `matrix_chain` are both reduced to a sign-fixed SVD of their product,
  removing the internal `GL(r)` factorization gauge.
- `bilinear_cp` normalizes and sign-fixes every CP component, orders the commutative
  left/right factors, and sorts components, removing scale, sign, and permutation
  gauges under the generic CP assumption.

This is not yet a general tensor-network canonicalizer. Looped networks, repeated
singular values, and nongeneric non-unique CP tensors require stronger machinery.

## Verification

`test_pricing.py` requires equivalent matrix gauges, dense/factorized linear maps,
and CP scale/permutation gauges to produce identical canonical bytes. The
rate-distortion test requires coarser quantization to reduce or preserve encoded bits
while increasing distortion.

## Benchmark adoption gate

Do not replace `bench/complexity.py` until the codec passes:

1. equivalence invariance on all library primitives;
2. monotone rate-distortion sweeps under the actual Theseus verifier;
3. no worse than 1% run-to-run bit variation;
4. matched-price rankings that are stable across at least two canonical grammars;
5. a red-team suite for constant smuggling, duplicated tensors, and library stuffing.

