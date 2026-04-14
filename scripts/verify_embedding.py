"""
OQ3: Verify the layer-based embedding Φ -> (r, i, j, k).

Loads the 72 primitives from primitivos.json, defines the embedding,
and verifies the key structural properties.
"""

import json
import numpy as np

# ── Load primitives ──
with open('C:/Github/dualidad_emergente/data/primitivos.json', encoding='utf-8') as f:
    data = json.load(f)

prims = data['primitivos']
N = len(prims)
print(f"Loaded {N} primitives across {len(data['capas'])} layers\n")

# ── Build layer sets ──
layers = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
bit_to_layer = {}
bit_to_name = {}
for p in prims:
    layers[p['capa']].append(p['bit'])
    bit_to_layer[p['bit']] = p['capa']
    bit_to_name[p['bit']] = p['nombre']

for l in sorted(layers):
    print(f"  Layer {l}: {len(layers[l])} primitives")

# ── Define axis contributing sets (from P11 Table 1) ──
R_set = set(layers[1] + layers[2] + layers[4] + layers[6])  # r-axis
I_set = set(layers[4] + layers[6])                           # i-axis
J_set = set(layers[3] + layers[5] + layers[6])               # j-axis
K_set = set(layers[6])                                       # k-axis

print(f"\n  |R| = {len(R_set)}, |I| = {len(I_set)}, |J| = {len(J_set)}, |K| = {len(K_set)}")

# ── Embedding function ──
all_bits = sorted(bit_to_layer.keys())

def embed(active_bits):
    """Map a set of active bit positions to (r, i, j, k) ∈ [0,1]^4."""
    s = set(active_bits)
    r = len(s & R_set) / len(R_set) if R_set else 0
    i = len(s & I_set) / len(I_set) if I_set else 0
    j = len(s & J_set) / len(J_set) if J_set else 0
    k = len(s & K_set) / len(K_set) if K_set else 0
    return np.array([r, i, j, k])

def embed_rescaled(active_bits):
    """Map to [0,1] × [-1,1]^3 (G-lattice domain V)."""
    e = embed(active_bits)
    return np.array([e[0], 2*e[1]-1, 2*e[2]-1, 2*e[3]-1])

# ── P1: Layer consistency ──
print("\n" + "="*60)
print("P1: LAYER CONSISTENCY")
print("="*60)

for test_layer, expected in [
    ([1,2], "i=j=k=0"),
    ([3],   "r=i=k=0"),
    ([4],   "j=k=0"),
    ([6],   "all potentially active"),
]:
    test_bits = []
    for l in test_layer:
        test_bits.extend(layers[l])
    e = embed(test_bits)
    print(f"  Layers {test_layer} only -> (r={e[0]:.3f}, i={e[1]:.3f}, j={e[2]:.3f}, k={e[3]:.3f})  [{expected}]")

    # Verify zeros
    if test_layer == [1,2]:
        assert e[1] == 0 and e[2] == 0 and e[3] == 0, "FAIL"
    elif test_layer == [3]:
        assert e[0] == 0 and e[1] == 0 and e[3] == 0, "FAIL"
    elif test_layer == [4]:
        assert e[2] == 0 and e[3] == 0, "FAIL"
    elif test_layer == [6]:
        assert e[0] > 0 and e[1] > 0 and e[2] > 0 and e[3] > 0, "FAIL"

print("  OK All layer consistency checks passed")

# ── P3: Divisibility -> componentwise <= ──
print("\n" + "="*60)
print("P3: DIVISIBILITY PRESERVES ORDER")
print("="*60)

# Generate random concept pairs where A subset B (divisibility)
np.random.seed(42)
violations = 0
n_tests = 10000

for _ in range(n_tests):
    # Random B
    b_bits = set(np.random.choice(all_bits, size=np.random.randint(1, N+1), replace=False))
    # A subset B (random subset)
    if len(b_bits) <= 1:
        continue
    a_size = np.random.randint(1, len(b_bits))
    a_bits = set(np.random.choice(list(b_bits), size=a_size, replace=False))

    ea = embed(a_bits)
    eb = embed(b_bits)

    if not np.all(ea <= eb + 1e-15):
        violations += 1

print(f"  {n_tests} random (AsubsetB) pairs tested")
print(f"  Violations of embed(A) <= embed(B): {violations}")
print(f"  {'OK HOLDS' if violations == 0 else 'FAIL FAILS'}")

# ── P4: lcm preserves max ──
print("\n" + "="*60)
print("P4: r(lcm(A,B)) >= max(r(A), r(B))")
print("="*60)

violations = 0
strict_increases = 0
n_tests = 10000

for _ in range(n_tests):
    a_bits = set(np.random.choice(all_bits, size=np.random.randint(1, 20), replace=False))
    b_bits = set(np.random.choice(all_bits, size=np.random.randint(1, 20), replace=False))
    lcm_bits = a_bits | b_bits  # lcm = union of active bits

    ea = embed(a_bits)
    eb = embed(b_bits)
    elcm = embed(lcm_bits)

    emax = np.maximum(ea, eb)

    if not np.all(elcm >= emax - 1e-15):
        violations += 1
    if np.any(elcm > emax + 1e-15):
        strict_increases += 1

print(f"  {n_tests} random pairs tested")
print(f"  Violations of embed(lcm) >= max(embed(A), embed(B)): {violations}")
print(f"  Cases with strict increase on some axis: {strict_increases}")
print(f"  {'OK HOLDS' if violations == 0 else 'FAIL FAILS'}")

# ── SYNTHESIS: duality pairs ──
print("\n" + "="*60)
print("SYNTHESIS: DUALITY PAIRS")
print("="*60)

duals = data['ejes_duales']
name_to_bit = {p['nombre']: p['bit'] for p in prims}
name_to_deps = {}
for p in prims:
    # Collect all dependency bits recursively
    deps = set()
    stack = list(p.get('deps', []))
    while stack:
        d = stack.pop()
        if d in name_to_bit and name_to_bit[d] not in deps:
            deps.add(name_to_bit[d])
            for p2 in prims:
                if p2['nombre'] == d:
                    stack.extend(p2.get('deps', []))
    name_to_deps[p['nombre']] = deps | {p['bit']}

print(f"  {len(duals)} dual pairs\n")

axis_names = ['r', 'i', 'j', 'k']
all_strict = True
pair_results = []

for a_name, b_name in duals:
    a_bits = name_to_deps.get(a_name, {name_to_bit.get(a_name, -1)})
    b_bits = name_to_deps.get(b_name, {name_to_bit.get(b_name, -1)})
    lcm_bits = a_bits | b_bits

    ea = embed(a_bits)
    eb = embed(b_bits)
    elcm = embed(lcm_bits)
    emax = np.maximum(ea, eb)

    # Check each axis for strict increase
    strict_axes = []
    for ax in range(4):
        if elcm[ax] > emax[ax] + 1e-10:
            strict_axes.append(axis_names[ax])

    has_strict = len(strict_axes) > 0
    if not has_strict:
        all_strict = False

    # Show detail for each pair
    axes_str = ','.join(strict_axes) if strict_axes else 'NONE'
    print(f"  {a_name:15s} / {b_name:15s}  "
          f"a=({ea[0]:.3f},{ea[1]:.3f},{ea[2]:.3f},{ea[3]:.3f})  "
          f"b=({eb[0]:.3f},{eb[1]:.3f},{eb[2]:.3f},{eb[3]:.3f})  "
          f"syn=({elcm[0]:.3f},{elcm[1]:.3f},{elcm[2]:.3f},{elcm[3]:.3f})  "
          f"UP:{axes_str}")

    # Also track layer composition of each pair
    a_layers = {bit_to_layer[b] for b in a_bits if b in bit_to_layer}
    b_layers = {bit_to_layer[b] for b in b_bits if b in bit_to_layer}
    pair_results.append((a_name, b_name, strict_axes, a_layers, b_layers,
                         len(a_bits), len(b_bits), len(lcm_bits)))

print(f"\n  SYNTHESIS STRICT INCREASE ON >= 1 AXIS: {'OK ALL PAIRS' if all_strict else 'FAIL'}")

# Classify all pairs: degenerate (one subset of other) vs non-degenerate
print(f"\n  DETAIL:")
degenerate = []
non_degenerate = []

for a_name, b_name, strict_axes, a_l, b_l, a_n, b_n, lcm_n in pair_results:
    a_bits = name_to_deps.get(a_name, {name_to_bit.get(a_name, -1)})
    b_bits = name_to_deps.get(b_name, {name_to_bit.get(b_name, -1)})
    a_minus_b = a_bits - b_bits
    b_minus_a = b_bits - a_bits

    is_degenerate = len(a_minus_b) == 0 or len(b_minus_a) == 0
    tag = "DEG" if is_degenerate else "OK "

    # For non-degenerate, check which axes have support from BOTH interiors
    axes_with_bilateral_support = []
    if not is_degenerate:
        for ax, ax_set in enumerate([R_set, I_set, J_set, K_set]):
            a_interior_on_ax = a_minus_b & ax_set
            b_interior_on_ax = b_minus_a & ax_set
            if len(a_interior_on_ax) > 0 and len(b_interior_on_ax) > 0:
                axes_with_bilateral_support.append(axis_names[ax])

    bilateral_str = ','.join(axes_with_bilateral_support) if axes_with_bilateral_support else '-'
    print(f"    [{tag}] {a_name:15s}/{b_name:15s}  "
          f"|a\\b|={len(a_minus_b):2d}  |b\\a|={len(b_minus_a):2d}  "
          f"strict:{','.join(strict_axes) if strict_axes else 'NONE':8s}  "
          f"bilateral:{bilateral_str}")

    if is_degenerate:
        degenerate.append((a_name, b_name, strict_axes))
    else:
        non_degenerate.append((a_name, b_name, strict_axes, axes_with_bilateral_support))

# Verify theorem: for non-degenerate pairs, strict axes == bilateral support axes
print(f"\n  THEOREM CHECK: strict_axes == bilateral_support_axes for non-degenerate pairs")
theorem_holds = True
for a_name, b_name, strict_axes, bilateral in non_degenerate:
    match = set(strict_axes) == set(bilateral)
    if not match:
        print(f"    MISMATCH: {a_name}/{b_name}: strict={strict_axes}, bilateral={bilateral}")
        theorem_holds = False

print(f"  Result: {'OK THEOREM HOLDS' if theorem_holds else 'FAIL'}")
print(f"  Non-degenerate pairs: {len(non_degenerate)}/{len(pair_results)}")
print(f"  Degenerate pairs (a subset b or b subset a): {len(degenerate)}/{len(pair_results)}")
print(f"  All non-degenerate have strict increase on >= 1 axis: "
      f"{'OK' if all(len(s[2]) > 0 for s in non_degenerate) else 'FAIL'}")

# ── Embed each primitive individually ──
print("\n" + "="*60)
print("INDIVIDUAL PRIMITIVE EMBEDDINGS")
print("="*60)

for l in sorted(layers):
    print(f"\n  Layer {l}:")
    for bit in sorted(layers[l]):
        name = bit_to_name[bit]
        e = embed_rescaled({bit})
        print(f"    {name:20s}  ({e[0]:.2f}, {e[1]:.2f}, {e[2]:.2f}, {e[3]:.2f})")
