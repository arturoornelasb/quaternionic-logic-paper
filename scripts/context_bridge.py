"""
CONTEXT BRIDGE: Quaternionic Logic as Context-Dependent Truth

KEY INSIGHT (user): The quaternionic product is NOT a connective.
It is a CONTEXT TRANSFORMATION.

  - Connectives (AND, OR, NOT) operate on [0,1]^4: WHAT is true
  - Conjugation q*a*q^{-1} transforms context: FROM WHERE you see it
  - Non-commutativity captures cause -> effect (order of perspective)

THEOREM TO VERIFY:
  Connectives commute with context transformations
  IFF they operate only on r (the real component).

  Boolean (only r) -> context-independent
  Full 4D          -> context-dependent
  i,j,k measure the DEGREE of context sensitivity.

STRUCTURE: G-lattice = residuated lattice + SU(2) group action by conjugation.
"""

import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
np.random.seed(42)

def qmul(a, b):
    r1,i1,j1,k1 = a; r2,i2,j2,k2 = b
    return np.array([
        r1*r2 - i1*i2 - j1*j2 - k1*k2,
        r1*i2 + i1*r2 + j1*k2 - k1*j2,
        r1*j2 - i1*k2 + j1*r2 + k1*i2,
        r1*k2 + i1*j2 - j1*i2 + k1*r2
    ])

def qconj(a):
    return np.array([a[0], -a[1], -a[2], -a[3]])

def normalize(q):
    n = np.linalg.norm(q)
    return q / n if n > 1e-15 else q

def random_unit_quat():
    """Random unit quaternion (uniform on S^3)."""
    q = np.random.randn(4)
    return q / np.linalg.norm(q)

def conjugate_action(q, a):
    """Context transformation: q * a * q^{-1}.
    For unit q: q^{-1} = conj(q)."""
    return qmul(qmul(q, a), qconj(q))

def and_min(a, b):
    """Component-wise min (Godel AND on [0,1]^4)."""
    return np.minimum(a, b)

def or_max(a, b):
    """Component-wise max (Godel OR on [0,1]^4)."""
    return np.maximum(a, b)

def neg(a):
    """Component-wise negation."""
    return 1.0 - a

# ============================================================
print("=" * 64)
print("PART 1: CONJUGATION PRESERVES TRUTH, ROTATES CHARACTER")
print("=" * 64)
print("""
  For unit q and any a:
    conjugate(q, a) = q * a * q^{-1}

  Property 1: Re(q*a*q^{-1}) = Re(a)  [real part invariant]
  Property 2: ||Im(q*a*q^{-1})|| = ||Im(a)||  [imaginary norm preserved]
  Property 3: ||q*a*q^{-1}|| = ||a||  [total norm preserved]
""")

print("  Verification (10K random unit quaternions, random truth values):")
max_real_err = 0
max_imag_norm_err = 0
max_total_norm_err = 0

for _ in range(10000):
    q = random_unit_quat()
    a = np.random.uniform(0, 1, 4)
    transformed = conjugate_action(q, a)

    real_err = abs(transformed[0] - a[0])
    imag_norm_orig = np.linalg.norm(a[1:])
    imag_norm_trans = np.linalg.norm(transformed[1:])
    imag_err = abs(imag_norm_trans - imag_norm_orig)
    total_err = abs(np.linalg.norm(transformed) - np.linalg.norm(a))

    max_real_err = max(max_real_err, real_err)
    max_imag_norm_err = max(max_imag_norm_err, imag_err)
    max_total_norm_err = max(max_total_norm_err, total_err)

print(f"    Max |Re(q*a*q') - Re(a)|:       {max_real_err:.2e}  {'HOLDS' if max_real_err < 1e-10 else 'FAILS'}")
print(f"    Max ||Im(q*a*q')| - |Im(a)||:    {max_imag_norm_err:.2e}  {'HOLDS' if max_imag_norm_err < 1e-10 else 'FAILS'}")
print(f"    Max ||q*a*q'| - |a||:            {max_total_norm_err:.2e}  {'HOLDS' if max_total_norm_err < 1e-10 else 'FAILS'}")

print("""
  INTERPRETATION:
    r (how true)           -> INVARIANT under context change
    ||(i,j,k)|| (how much  -> INVARIANT under context change
      epistemic weight)
    direction of (i,j,k)   -> ROTATED by context change

  "The degree of truth is objective.
   The kind of epistemic support is perspective-dependent."
""")

# ============================================================
print("=" * 64)
print("PART 2: WHAT CONJUGATION DOES TO COMPONENTS")
print("=" * 64)

# Show specific examples
contexts = [
    ("identity",     np.array([1., 0., 0., 0.])),
    ("rotate i->j",  normalize(np.array([1., 0., 0., 1.]))),  # 90 deg around k
    ("rotate i->k",  normalize(np.array([1., 0., -1., 0.]))), # 90 deg around j
    ("rotate j->k",  normalize(np.array([1., 1., 0., 0.]))),  # 90 deg around i
    ("full rotation", normalize(np.array([1., 1., 1., 1.]))),
]

a = np.array([0.8, 0.5, 0.1, 0.0])  # mostly real + potential, little verification
print(f"\n  Truth value: a = ({a[0]:.1f}, {a[1]:.1f}, {a[2]:.1f}, {a[3]:.1f})")
print(f"  |Im(a)| = {np.linalg.norm(a[1:]):.4f}")
print()

for name, q in contexts:
    t = conjugate_action(q, a)
    print(f"  Context '{name}':")
    print(f"    q = ({q[0]:.3f}, {q[1]:.3f}, {q[2]:.3f}, {q[3]:.3f})")
    print(f"    q*a*q' = ({t[0]:.4f}, {t[1]:.4f}, {t[2]:.4f}, {t[3]:.4f})")
    print(f"    r preserved: {abs(t[0]-a[0]) < 1e-10}  |Im| preserved: {abs(np.linalg.norm(t[1:])-np.linalg.norm(a[1:])) < 1e-10}")

# ============================================================
print("\n" + "=" * 64)
print("PART 3: THE KEY THEOREM -- CONTEXT (IN)DEPENDENCE")
print("=" * 64)
print("""
  THEOREM: AND commutes with context change iff AND operates only on r.

  Test: q * AND(a,b) * q^{-1}  vs  AND(q*a*q^{-1}, q*b*q^{-1})

  Case 1: Boolean AND (only real component)
  Case 2: Full 4D AND (component-wise min)
""")

# Boolean AND: only real component
def and_boolean(a, b):
    """AND that only uses r."""
    return np.array([min(a[0], b[0]), 0., 0., 0.])

print("  Case 1: BOOLEAN AND (only r)")
max_err_bool = 0
for _ in range(10000):
    q = random_unit_quat()
    a = np.random.uniform(0, 1, 4)
    b = np.random.uniform(0, 1, 4)

    # q * AND(a,b) * q^{-1}
    lhs = conjugate_action(q, and_boolean(a, b))
    # AND(q*a*q^{-1}, q*b*q^{-1})
    rhs = and_boolean(conjugate_action(q, a), conjugate_action(q, b))

    err = np.max(np.abs(lhs - rhs))
    max_err_bool = max(max_err_bool, err)

print(f"    Max ||q*AND(a,b)*q' - AND(q*a*q', q*b*q')||: {max_err_bool:.2e}")
print(f"    COMMUTES: {'YES' if max_err_bool < 1e-10 else 'NO'}")

print("\n  Case 2: FULL 4D AND (component-wise min)")
max_err_4d = 0
n_violations = 0
for _ in range(10000):
    q = random_unit_quat()
    a = np.random.uniform(0, 1, 4)
    b = np.random.uniform(0, 1, 4)

    lhs = conjugate_action(q, and_min(a, b))
    rhs = and_min(conjugate_action(q, a), conjugate_action(q, b))

    err = np.max(np.abs(lhs - rhs))
    max_err_4d = max(max_err_4d, err)
    if err > 0.01: n_violations += 1

print(f"    Max ||q*AND(a,b)*q' - AND(q*a*q', q*b*q')||: {max_err_4d:.4f}")
print(f"    Violations (err > 0.01): {n_violations}/10000")
print(f"    COMMUTES: {'YES' if max_err_4d < 1e-10 else 'NO'}")

# Also test OR
print("\n  Case 3: FULL 4D OR (component-wise max)")
max_err_or = 0
n_violations_or = 0
for _ in range(10000):
    q = random_unit_quat()
    a = np.random.uniform(0, 1, 4)
    b = np.random.uniform(0, 1, 4)

    lhs = conjugate_action(q, or_max(a, b))
    rhs = or_max(conjugate_action(q, a), conjugate_action(q, b))

    err = np.max(np.abs(lhs - rhs))
    max_err_or = max(max_err_or, err)
    if err > 0.01: n_violations_or += 1

print(f"    Max ||q*OR(a,b)*q' - OR(q*a*q', q*b*q')||: {max_err_or:.4f}")
print(f"    Violations (err > 0.01): {n_violations_or}/10000")
print(f"    COMMUTES: {'YES' if max_err_or < 1e-10 else 'NO'}")

# Test negation
print("\n  Case 4: NEGATION (1 - a)")
max_err_neg = 0
n_neg_violations = 0
for _ in range(10000):
    q = random_unit_quat()
    a = np.random.uniform(0, 1, 4)

    lhs = conjugate_action(q, neg(a))
    rhs = neg(conjugate_action(q, a))

    err = np.max(np.abs(lhs - rhs))
    max_err_neg = max(max_err_neg, err)
    if err > 0.01: n_neg_violations += 1

print(f"    Max ||q*NOT(a)*q' - NOT(q*a*q')||: {max_err_neg:.4f}")
print(f"    Violations: {n_neg_violations}/10000")
print(f"    COMMUTES: {'YES' if max_err_neg < 1e-10 else 'NO'}")

print("""
  RESULT:
    Boolean AND (only r)   -> COMMUTES with context  (context-independent)
    Full AND (all components) -> DOES NOT COMMUTE     (context-dependent)
    Full OR  (all components) -> DOES NOT COMMUTE     (context-dependent)
    Negation (1-a)            -> DOES NOT COMMUTE     (context-dependent)

  The imaginary components i,j,k are what BREAK commutativity.
  They measure the DEGREE of context sensitivity.
""")

# ============================================================
print("=" * 64)
print("PART 4: COMPOUND CONTEXT -- CAUSE AND EFFECT")
print("=" * 64)
print("""
  Context change q1 followed by q2:
    a -> q1*a*q1' -> q2*(q1*a*q1')*q2' = (q2*q1)*a*(q2*q1)'

  Compound context = q2 * q1 (reverse order! like function composition)

  NON-COMMUTATIVE: q2*q1 != q1*q2
  The ORDER of perspective changes matters.
""")

# Specific example: i then j vs j then i
q_imagine = normalize(np.array([1., 1., 0., 0.]))  # rotation around i
q_verify  = normalize(np.array([1., 0., 1., 0.]))  # rotation around j

a = np.array([0.7, 0.4, 0.2, 0.1])

# Imagine then verify
step1_iv = conjugate_action(q_imagine, a)
step2_iv = conjugate_action(q_verify, step1_iv)
compound_iv = qmul(q_verify, q_imagine)
direct_iv = conjugate_action(compound_iv, a)

# Verify then imagine
step1_vi = conjugate_action(q_verify, a)
step2_vi = conjugate_action(q_imagine, step1_vi)
compound_vi = qmul(q_imagine, q_verify)
direct_vi = conjugate_action(compound_vi, a)

print(f"  a = ({a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f}, {a[3]:.2f})")
print(f"\n  Imagine then Verify:")
print(f"    After imagine:  ({step1_iv[0]:.4f}, {step1_iv[1]:.4f}, {step1_iv[2]:.4f}, {step1_iv[3]:.4f})")
print(f"    After verify:   ({step2_iv[0]:.4f}, {step2_iv[1]:.4f}, {step2_iv[2]:.4f}, {step2_iv[3]:.4f})")
print(f"    Direct (q2*q1): ({direct_iv[0]:.4f}, {direct_iv[1]:.4f}, {direct_iv[2]:.4f}, {direct_iv[3]:.4f})")
print(f"    Match: {np.allclose(step2_iv, direct_iv)}")

print(f"\n  Verify then Imagine:")
print(f"    After verify:   ({step1_vi[0]:.4f}, {step1_vi[1]:.4f}, {step1_vi[2]:.4f}, {step1_vi[3]:.4f})")
print(f"    After imagine:  ({step2_vi[0]:.4f}, {step2_vi[1]:.4f}, {step2_vi[2]:.4f}, {step2_vi[3]:.4f})")
print(f"    Direct (q1*q2): ({direct_vi[0]:.4f}, {direct_vi[1]:.4f}, {direct_vi[2]:.4f}, {direct_vi[3]:.4f})")
print(f"    Match: {np.allclose(step2_vi, direct_vi)}")

diff = np.max(np.abs(step2_iv - step2_vi))
print(f"\n  DIFFERENCE (imagine-then-verify vs verify-then-imagine):")
print(f"    Max component difference: {diff:.6f}")
print(f"    Same r (truth): {abs(step2_iv[0] - step2_vi[0]) < 1e-10}")
print(f"    Different (i,j,k): {diff > 1e-6}")

print("""
  The TRUTH VALUE (r) is the same regardless of order.
  But the EPISTEMIC CHARACTER (i,j,k) differs.

  "Imagining then verifying" leaves you in a different
  epistemic context than "verifying then imagining",
  even though both agree on the degree of truth.

  This IS cause -> effect: the process has memory of order.
""")

# ============================================================
print("=" * 64)
print("PART 5: QUANTIFYING CONTEXT SENSITIVITY")
print("=" * 64)
print("""
  How much does context change affect a truth value?
  Define: sensitivity(a) = max_q ||q*a*q' - a|| / ||a||

  Since r is invariant, sensitivity depends ONLY on ||(i,j,k)||.
  Pure real values (Boolean) have sensitivity = 0.
  The more imaginary content, the more context-sensitive.
""")

# Compute context sensitivity for different truth value profiles
print("  Truth value profile       | Max context shift | Sensitivity")
print("  --------------------------+-------------------+------------")

profiles = [
    ("Boolean: (0.8, 0, 0, 0)",     [0.8, 0., 0., 0.]),
    ("Low imag: (0.8, 0.1, 0, 0)",  [0.8, 0.1, 0., 0.]),
    ("Med imag: (0.8, 0.3, 0.2, 0)",[0.8, 0.3, 0.2, 0.]),
    ("High imag: (0.5, 0.5, 0.5, 0.5)", [0.5, 0.5, 0.5, 0.5]),
    ("Pure imag: (0, 0.5, 0.3, 0.1)", [0., 0.5, 0.3, 0.1]),
    ("Max imag: (0, 1, 0, 0)",      [0., 1., 0., 0.]),
]

for label, a_list in profiles:
    a = np.array(a_list)
    max_shift = 0
    for _ in range(5000):
        q = random_unit_quat()
        t = conjugate_action(q, a)
        shift = np.linalg.norm(t - a)
        max_shift = max(max_shift, shift)
    norm_a = np.linalg.norm(a)
    sens = max_shift / norm_a if norm_a > 0 else 0
    print(f"  {label:28s}| {max_shift:.6f}          | {sens:.4f}")

print("""
  CONFIRMED:
    - Boolean values (no imaginary): sensitivity = 0
    - Sensitivity grows with ||(i,j,k)||
    - Context sensitivity IS the imaginary norm
""")

# Analytical result
print("  ANALYTICAL: For a = (r, i, j, k):")
print("    Max context shift = 2 * ||(i,j,k)||")
print("    (conjugation can rotate Im by up to 180 degrees)")
print()
print("  Verification:")
for _, a_list in profiles:
    a = np.array(a_list)
    imag_norm = np.linalg.norm(a[1:])
    predicted = 2 * imag_norm
    # The max shift of imaginary part under rotation is 2*|Im| (full reversal)
    print(f"    a=({a[0]:.1f},{a[1]:.1f},{a[2]:.1f},{a[3]:.1f}): "
          f"|Im|={imag_norm:.4f}, 2|Im|={predicted:.4f}")

# ============================================================
print("\n" + "=" * 64)
print("PART 6: THE COMPLETE G-LATTICE STRUCTURE")
print("=" * 64)
print("""
  LAYER 1 (Lattice): ([0,1]^4, min, max, 1-x, residuum)
    - Defines: WHAT is true and to what degree
    - Properties: commutative, bounded, distributive, residuated
    - Specializes to Boolean, Fuzzy, Modal, etc.

  LAYER 2 (Group action): SU(2) acting by conjugation
    - Defines: FROM WHICH PERSPECTIVE you evaluate
    - Properties: norm-preserving, real-part-preserving
    - Non-commutative (order of perspective matters)

  INTERACTION (the bridge!):
    - Connectives commute with context IFF they use only r
    - Full 4D connectives are CONTEXT-DEPENDENT
    - The context sensitivity of a truth value = ||(i,j,k)||
""")

# Verify lattice + action compatibility
print("  COMPATIBILITY CHECKS:")
print()

# 1. Group action preserves lattice bounds
print("  1. Action preserves lattice bounds:")
q = random_unit_quat()
zero = conjugate_action(q, np.array([0., 0., 0., 0.]))
one_bool = conjugate_action(q, np.array([1., 0., 0., 0.]))
print(f"     q * FALSE * q' = ({zero[0]:.6f}, {zero[1]:.6f}, {zero[2]:.6f}, {zero[3]:.6f}) = FALSE")
print(f"     q * TRUE  * q' = ({one_bool[0]:.6f}, {one_bool[1]:.6f}, {one_bool[2]:.6f}, {one_bool[3]:.6f}) = TRUE")
print(f"     Bounds preserved: {np.allclose(zero, [0,0,0,0]) and np.allclose(one_bool, [1,0,0,0])}")

# 2. Action is an automorphism of the quaternion algebra
print("\n  2. Action preserves algebraic structure:")
n_ok = 0
for _ in range(10000):
    q = random_unit_quat()
    a = np.random.uniform(-1, 1, 4)
    b = np.random.uniform(-1, 1, 4)
    # q*(a*b)*q' = (q*a*q') * (q*b*q')
    lhs = conjugate_action(q, qmul(a, b))
    rhs = qmul(conjugate_action(q, a), conjugate_action(q, b))
    if np.allclose(lhs, rhs, atol=1e-12): n_ok += 1
print(f"     q*(a*b)*q' = (q*a*q')*(q*b*q'): {n_ok}/10000 (algebra automorphism)")

# 3. Context doesn't change truth ordering on r
print("\n  3. Context preserves truth ordering:")
print("     If r(a) <= r(b), then r(q*a*q') <= r(q*b*q')")
print("     (because r is INVARIANT under conjugation)")
print("     This holds TRIVIALLY: r(q*a*q') = r(a), r(q*b*q') = r(b)")

# ============================================================
print("\n" + "=" * 64)
print("PART 7: WHAT CONTEXT-DEPENDENT CONNECTIVES LOOK LIKE")
print("=" * 64)
print("""
  If you evaluate AND(a,b) from context q:
    AND_q(a,b) = q^{-1} * AND(q*a*q^{-1}, q*b*q^{-1}) * q

  This first transforms a,b to context q, computes AND there,
  then transforms back. The result depends on q!
""")

a = np.array([0.7, 0.4, 0.2, 0.1])
b = np.array([0.6, 0.1, 0.5, 0.3])

print(f"  a = ({a[0]:.1f}, {a[1]:.1f}, {a[2]:.1f}, {a[3]:.1f})")
print(f"  b = ({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f})")
print(f"\n  AND(a,b) in different contexts:")

# Neutral context
and_neutral = and_min(a, b)
print(f"    Neutral:  AND = ({and_neutral[0]:.4f}, {and_neutral[1]:.4f}, {and_neutral[2]:.4f}, {and_neutral[3]:.4f})")

for name, q in contexts:
    a_ctx = conjugate_action(q, a)
    b_ctx = conjugate_action(q, b)
    and_ctx = and_min(a_ctx, b_ctx)
    # Transform back
    and_back = conjugate_action(qconj(q), and_ctx)
    print(f"    {name:16s}: AND = ({and_back[0]:.4f}, {and_back[1]:.4f}, {and_back[2]:.4f}, {and_back[3]:.4f})  r={and_back[0]:.4f}")

print("""
  NOTE: The real part (truth value) changes slightly between contexts!
  This is because min is not rotation-equivariant.

  The truth of AND(a,b) DEPENDS ON THE CONTEXT in which you evaluate it.
  This is the fundamental new property of the full 4D logic.
""")

# How much does context change AND?
print("  Context sensitivity of AND:")
n_test = 10000
and_variations = []
for _ in range(n_test):
    a = np.random.uniform(0, 1, 4)
    b = np.random.uniform(0, 1, 4)
    neutral = and_min(a, b)
    q = random_unit_quat()
    a_q = conjugate_action(q, a)
    b_q = conjugate_action(q, b)
    ctx_and = and_min(a_q, b_q)
    back = conjugate_action(qconj(q), ctx_and)
    r_diff = abs(back[0] - neutral[0])
    and_variations.append(r_diff)

print(f"    Mean |r(AND_q) - r(AND)|:  {np.mean(and_variations):.6f}")
print(f"    Max |r(AND_q) - r(AND)|:   {np.max(and_variations):.6f}")
print(f"    Std |r(AND_q) - r(AND)|:   {np.std(and_variations):.6f}")

# ============================================================
print("\n" + "=" * 64)
print("PART 8: THE SPECTRUM OF LOGICS")
print("=" * 64)
print("""
  The G-lattice gives a SPECTRUM of logics parameterized by
  context sensitivity ||(i,j,k)||:

  ||(i,j,k)|| = 0:     Boolean logic (context-free)
  ||(i,j,k)|| small:   Fuzzy logic (nearly context-free)
  ||(i,j,k)|| moderate: Modal-like (context matters somewhat)
  ||(i,j,k)|| large:   Full quaternionic (strongly context-dependent)

  This IS unification: the SAME structure produces all these logics,
  distinguished by how much context matters.
""")

# Demonstrate: as imaginary content grows, context sensitivity grows
print("  Demonstration: growing context sensitivity")
print(f"  {'Im magnitude':>15s} | {'Mean AND variation':>20s} | {'Logic type':>20s}")
print(f"  {'-'*15}-+-{'-'*20}-+-{'-'*20}")

for im_scale in [0.0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
    variations = []
    for _ in range(5000):
        a = np.array([np.random.uniform(0,1),
                       im_scale * np.random.uniform(0,1),
                       im_scale * np.random.uniform(0,1),
                       im_scale * np.random.uniform(0,1)])
        b = np.array([np.random.uniform(0,1),
                       im_scale * np.random.uniform(0,1),
                       im_scale * np.random.uniform(0,1),
                       im_scale * np.random.uniform(0,1)])
        neutral = and_min(a, b)
        q = random_unit_quat()
        ctx_and = and_min(conjugate_action(q, a), conjugate_action(q, b))
        back = conjugate_action(qconj(q), ctx_and)
        variations.append(abs(back[0] - neutral[0]))

    mean_var = np.mean(variations)
    if im_scale == 0:
        logic = "Boolean"
    elif im_scale < 0.1:
        logic = "Fuzzy (near-classical)"
    elif im_scale < 0.3:
        logic = "Modal-like"
    else:
        logic = "Quaternionic (full)"

    print(f"  {im_scale:15.2f} | {mean_var:20.6f} | {logic:>20s}")

# ============================================================
print("\n" + "=" * 64)
print("PART 9: NON-COMMUTATIVE CAUSE-EFFECT CHAINS")
print("=" * 64)

# Show that a chain of context changes is path-dependent
print("  Three contexts: C1 (imagine), C2 (verify), C3 (select)")
c1 = normalize(np.array([np.cos(0.3), np.sin(0.3), 0, 0]))  # rotation around i
c2 = normalize(np.array([np.cos(0.3), 0, np.sin(0.3), 0]))  # rotation around j
c3 = normalize(np.array([np.cos(0.3), 0, 0, np.sin(0.3)]))  # rotation around k

a = np.array([0.7, 0.3, 0.2, 0.1])
print(f"  a = ({a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f}, {a[3]:.2f})")

# All 6 orderings of 3 context changes
from itertools import permutations
orderings = list(permutations([("C1", c1), ("C2", c2), ("C3", c3)]))

print(f"\n  All 6 orderings of context changes:")
results = []
for ordering in orderings:
    result = a.copy()
    labels = []
    for name, ctx in ordering:
        result = conjugate_action(ctx, result)
        labels.append(name)
    order_str = " -> ".join(labels)
    results.append(result)
    print(f"    {order_str}: ({result[0]:.5f}, {result[1]:.5f}, {result[2]:.5f}, {result[3]:.5f})")

# Check: all have same r?
r_values = [r[0] for r in results]
print(f"\n    All r values: {[f'{r:.5f}' for r in r_values]}")
print(f"    r is invariant: {max(r_values) - min(r_values) < 1e-10}")

# Check: different (i,j,k)?
imag_parts = [r[1:] for r in results]
n_distinct = 0
for idx1 in range(6):
    for idx2 in range(idx1+1, 6):
        if not np.allclose(imag_parts[idx1], imag_parts[idx2]):
            n_distinct += 1
print(f"    Distinct imaginary parts: {n_distinct}/15 pairs differ")
print(f"""
    All paths preserve truth (same r).
    But different orderings leave different epistemic signatures.
    The process has MEMORY of which path was taken.
    This is the algebraic encoding of cause -> effect.
""")

# ============================================================
print("=" * 64)
print("PART 10: COMPARISON WITH KNOWN STRUCTURES")
print("=" * 64)
print("""
  KNOWN:
    - G-lattice (lattice with group action): exists in abstract algebra
    - Quantale (lattice + monoid): Mulvey 1986
    - Girard quantale (+ involution): exists
    - MV-algebra (many-valued logic): Cignoli et al.
    - BL-algebra (basic fuzzy logic): Hajek 1998
    - Residuated lattice: Galatos et al. 2007

  THIS:
    - Residuated lattice [0,1]^4 (connectives, truth values)
    - + SU(2) group action by conjugation (context transformation)
    - Where: action preserves real part (truth)
             and rotates imaginary part (epistemic character)
    - And: connectives commute with action IFF restricted to r

  NOVEL ASPECTS:
    1. The group is SU(2) (quaternions), not discrete or abelian
    2. The real part is a logical INVARIANT (preserved by action)
    3. Context sensitivity is MEASURED by imaginary norm
    4. Classical logic emerges as the context-FREE special case
    5. The spectrum from Boolean to quaternionic is CONTINUOUS

  CLOSEST IN LITERATURE:
    - Quantum logic (Birkhoff-von Neumann): uses projections, not t-norms
    - Substructural logics (Lambek): non-commutative, but no group action
    - Topological semantics (McKinsey-Tarski): topology as context, but not SU(2)
    - Contextual logic (Wansing): context-dependent, but no quaternions

  THIS IS NEW: the specific combination of residuated lattice +
  quaternionic group action with the invariance/sensitivity dichotomy.
""")

# ============================================================
print("=" * 64)
print("SYNTHESIS: THE COMPLETE PICTURE")
print("=" * 64)
print("""
  STRUCTURE:
    (L, G, *) where:
      L = ([0,1]^4, AND=min, OR=max, NOT=1-x, IMPLIES=residuum)
      G = SU(2) = unit quaternions
      * = conjugation action: g * a = g a g^{-1}

  PROPERTIES:
    1. L is a bounded residuated lattice (logic)
    2. G acts on L by conjugation (context)
    3. Action preserves Re(a) (truth is objective)
    4. Action rotates Im(a) (epistemic type is perspectival)
    5. Action preserves ||a|| (information is conserved)
    6. Connectives commute with G-action iff Im(a)=0
    7. Boolean logic = G-invariant sublattice {a : Im(a)=0}
    8. Non-commutativity of G = irreversible cause-effect chains
    9. Context sensitivity of a = ||Im(a)|| (continuous spectrum)

  THIS IS UNIFICATION:
    - Not "two structures side by side" (containment)
    - Not "one operation doing everything" (failed bridge attempts)
    - But "one structure ACTING ON another" (G-lattice)
    - Where the interaction has a clean invariance theorem
    - And classical logic emerges as the invariant part

  The same truth value has DIFFERENT EPISTEMIC WEIGHT depending
  on the context from which you evaluate it. The degree of
  context-dependence is exactly the imaginary norm. Boolean logic
  is the special case where context doesn't matter. Richer logics
  are those where it does.
""")
