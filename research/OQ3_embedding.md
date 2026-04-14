# OQ3: The Embedding Φ → (r, i, j, k)

## Data

72 primitives distributed across 6 layers:
- Layer 1 (Point): 3 primitives — vacío, información, uno
- Layer 2 (Line): 8 primitives — fuerza, eje_profundidad, contención, más, menos, unión, separación, parte_de
- Layer 3 (Time): 13 primitives — mover, posición_temporal, flujo_temporal, hacer, creación, destrucción, orden, caos, porque, si_entonces, atracción, proporción, quietud
- Layer 4 (Plane): 21 primitives — eje_vertical, eje_lateral, equilibrio, vista, bien, mal, verdad, mentira, libertad, control, tipo_de, algunos, muchos, todo, puede, debe, tal_vez, decaimiento, aversión, cooperación, pérdida
- Layer 5 (Volume): 23 primitives — tierra, agua, aire, fuego, tacto, oído, gusto, olfato, interocepción, vida, muerte, placer, dolor, consciente, ausente, individual, colectivo, querer, saber, pensar, decir, atención, intención
- Layer 6 (Observer): 4 primitives — temporal_obs, eterno_obs, receptivo, creador_obs

## Layer → Axis mapping (from P11 Table 1)

| Layer | Active axes | Semantic content |
|-------|------------|-----------------|
| 1 Point | r only (discrete) | Existence |
| 2 Line | r only (continuous) | Comparison, direction |
| 3 Time | j pure | Causality, ordering |
| 4 Plane | r × i | Modality, possibility |
| 5 Volume | j± (polarity) | Body, verification, polarity |
| 6 Observer | r × i × j × k | Self-reference, recursion |

## The Embedding

### Step 1: Binary exponent vector

Each concept C has a prime signature Φ(C) = ∏ p_i^{s_i}.
Map to the exponent vector: s(C) = (s_1, ..., s_72) ∈ {0,1}^72.

This preserves: gcd → component-wise min, lcm → component-wise max,
divisibility → component-wise ≤. (Classical; Birkhoff 1967.)

### Step 2: Layer partition

Partition the 72 indices into layer sets:
- L₁ = {indices of Layer 1 primitives} (|L₁| = 3)
- L₂ = {indices of Layer 2 primitives} (|L₂| = 8)
- L₃ = {indices of Layer 3 primitives} (|L₃| = 13)
- L₄ = {indices of Layer 4 primitives} (|L₄| = 21)
- L₅ = {indices of Layer 5 primitives} (|L₅| = 23)
- L₆ = {indices of Layer 6 primitives} (|L₆| = 4)

### Step 3: Axis activation per layer

From P11 Table 1, define which axes each layer contributes to:

| Layer | r | i | j | k |
|-------|---|---|---|---|
| 1 | ✓ | | | |
| 2 | ✓ | | | |
| 3 | | | ✓ | |
| 4 | ✓ | ✓ | | |
| 5 | | | ✓ | |
| 6 | ✓ | ✓ | ✓ | ✓ |

Define the contributing layer sets for each axis:
- R = L₁ ∪ L₂ ∪ L₄ ∪ L₆  (|R| = 3+8+21+4 = 36)
- I = L₄ ∪ L₆             (|I| = 21+4 = 25)
- J = L₃ ∪ L₅ ∪ L₆        (|J| = 13+23+4 = 40)
- K = L₆                   (|K| = 4)

### Step 4: The embedding formula

For a concept C with exponent vector s = (s_1, ..., s_72):

```
r(C) = Σ_{i∈R} s_i / |R|     ∈ [0, 1]

i(C) = Σ_{i∈I} s_i / |I|     ∈ [0, 1]

j(C) = Σ_{i∈J} s_i / |J|     ∈ [0, 1]

k(C) = Σ_{i∈K} s_i / |K|     ∈ [0, 1]
```

NOTE: This gives values in [0,1]^4, not [0,1]×[-1,1]^3.
The imaginary components need rescaling to [-1,1] for the G-lattice.
Option: i' = 2i-1, j' = 2j-1, k' = 2k-1. Then a concept with no
active primitives in I has i' = -1 (minimal potentiality), and one
with all has i' = 1.

## Properties to verify

### P1: Layer consistency
- If C has only L₁∪L₂ primitives active → i(C)=0, j(C)=0, k(C)=0 ✓
  (because I∩(L₁∪L₂) = ∅, J∩(L₁∪L₂) = ∅, K∩(L₁∪L₂) = ∅)
- If C has only L₃ primitives active → r(C)=0, i(C)=0, k(C)=0 ✓
- If C has only L₄ primitives active → j(C)=0, k(C)=0 ✓
- If C has only L₆ primitives active → all four axes potentially active ✓

### P2: Complexity ordering
ω(Φ(C)) = Σ s_i = total number of active primitives.
The embedding distributes these across axes by layer.
More active primitives → higher values on the relevant axes.
But this is NOT monotone in general: adding an L₃ primitive
increases j but not r.

### P3: Lattice preservation (PARTIAL)
For the r-axis: if Φ(A) | Φ(B), then s(A) ≤ s(B) componentwise,
so Σ_{i∈R} s_i(A) ≤ Σ_{i∈R} s_i(B), hence r(A) ≤ r(B).
Same for i, j, k. So divisibility → componentwise ≤ in (r,i,j,k). ✓

For lcm: r(lcm(A,B)) = Σ_{i∈R} max(s_i(A), s_i(B)) / |R|
                      = max over R of individual bits
                      ≥ max(r(A), r(B))? NO, not in general.
Counter: if A has 10 R-bits active and B has 10 different R-bits,
r(lcm) = 20/36 while max(r(A),r(B)) = 10/36. So r(lcm) > max.
This is STRONGER than ≥.

Actually: r(lcm(A,B)) ≥ max(r(A), r(B)) always holds because
max(s_i(A), s_i(B)) ≥ s_i(A) for all i. ✓

### P4: Synthesis compatibility
r(a⊕ā) = r(lcm(Φ(a),Φ(ā))) ≥ max(r(a), r(ā)). ✓
Strict inequality when a and ā have at least one R-primitive
not shared. Which is guaranteed when the duality has interiors
with R-support.

## Verified properties (computational, 2026-04-12)

### P1: Layer consistency — PASSED
- L1+L2 only → i=j=k=0 ✓
- L3 only → r=i=k=0 ✓
- L4 only → j=k=0 ✓
- L6 only → all axes active ✓

### P3: Divisibility preserves order — PASSED (10K random tests, 0 violations)
If A ⊂ B (as bit sets), then e(A) ≤ e(B) componentwise.

### P4: lcm ≥ max — PASSED (10K random tests, 0 violations)
e(lcm(A,B)) ≥ max(e(A), e(B)) componentwise. 97.8% of pairs show strict
increase on some axis.

### P5: Synthesis bilateral theorem — PROVED + VERIFIED

**Definition**: For concepts A, B with dependency-expanded bit sets
S(A), S(B), define the *interiors*:
  Int(A|B) = S(A) \ S(B)   (primitives in A not in B)
  Int(B|A) = S(B) \ S(A)   (primitives in B not in A)

**Theorem**: The synthesis e(lcm(A,B)) strictly exceeds max(e(A),e(B))
on axis X if and only if both interiors have X-support:
  e(lcm)[X] > max(e(A)[X], e(B)[X])  ⟺  Int(A|B) ∩ X_set ≠ ∅ AND Int(B|A) ∩ X_set ≠ ∅

**Proof**: On axis X, e(lcm)[X] = |S(A)_X ∪ S(B)_X| / |X_set| where
S(A)_X = S(A) ∩ X_set. The union exceeds max(|S(A)_X|, |S(B)_X|) iff
neither is a subset of the other on X, i.e., S(A)_X ⊄ S(B)_X and
S(B)_X ⊄ S(A)_X. The first holds iff Int(A|B) ∩ X_set ≠ ∅; the second
iff Int(B|A) ∩ X_set ≠ ∅. □

**Corollary (non-degenerate synthesis)**: If Φ(A) ∤ Φ(B) and Φ(B) ∤ Φ(A)
(both interiors non-empty), then synthesis strictly increases on every
axis with bilateral interior support.

**Corollary (degenerate pairs)**: If S(A) ⊂ S(B), then lcm = B and
e(lcm) = e(B). No axis shows strict increase. This occurs when one
concept's dependency chain subsumes the other's.

### Verification on 14 duality pairs:
- 11 non-degenerate: strict axes exactly match bilateral support axes
- 3 degenerate (vida⊂muerte, consciente⊂ausente, individual⊂colectivo):
  |Int(A|B)| = 0, confirming S(A) ⊂ S(B)
- Theorem holds for ALL 14 pairs

## Problem: the embedding is lossy

The projection {0,1}^72 → [0,1]^4 loses most of the 72 dimensions.
Two concepts with different binary signatures but the same counts
per axis-group map to the same quaternionic point.

This is inherent to ANY projection from 72 to 4 dimensions.
The question is whether the RELEVANT structure is preserved.

Answer: the layer structure, complexity ordering, divisibility order,
and synthesis increase are ALL preserved. The individual primitive
identities are not — but those live in the prime algebra, not the
G-lattice. The embedding is the structural bridge; the prime algebra
retains the full identity information.

## What this resolves

With this embedding:
1. P11 and P12 are formally connected: Φ(C) → s(C) → (r,i,j,k)(C).
2. "Synthesis generates truth" is now a THEOREM, not a claim:
   e(a⊕ā) ≥ max(e(a),e(ā)), with strict inequality precisely
   characterized by bilateral interior support on each axis.
3. Layer consistency is exact (by construction from P11 Table 1).
4. Divisibility → componentwise ≤ (lattice order preserved).
5. The degenerate case (one concept subsuming the other) is
   correctly handled: no synthesis occurs because there is no
   genuine opposition.

## Status: OQ3 RESOLVED
