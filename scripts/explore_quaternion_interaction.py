"""
Exploration: Interaction between logical connectives and quaternionic product.

The logical connectives (AND, OR, NOT) operate on [0,1]^4 (hypercube).
The quaternionic product operates on S^3 (unit sphere in R^4).

Key questions:
1. Does the quaternionic product distribute over AND/OR?
2. Can quaternionic division define a non-commutative implication?
3. What algebraic structure emerges from combining both?
4. What do dual pair products mean logically?

Author: J. Arturo Ornelas Brand
"""

import math
import random
from typing import Tuple

random.seed(42)

Vec4 = Tuple[float, float, float, float]

# ═══════════════════════════════════════════════════════════════════
# HAMILTON QUATERNION PRODUCT
# ═══════════════════════════════════════════════════════════════════

def norm(q: Vec4) -> float:
    return math.sqrt(sum(x*x for x in q))

def normalize(q: Vec4) -> Vec4:
    n = norm(q)
    if n < 1e-15:
        return (1.0, 0.0, 0.0, 0.0)  # default to real unit
    return tuple(x/n for x in q)

def hamilton(q1: Vec4, q2: Vec4) -> Vec4:
    """Hamilton quaternion product: q1 * q2
    Convention: q = (r, i, j, k) = r + i*i + j*j + k*k"""
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return (
        a1*a2 - b1*b2 - c1*c2 - d1*d2,  # real
        a1*b2 + b1*a2 + c1*d2 - d1*c2,  # i
        a1*c2 - b1*d2 + c1*a2 + d1*b2,  # j
        a1*d2 + b1*c2 - c1*b2 + d1*a2,  # k
    )

def conjugate(q: Vec4) -> Vec4:
    """Quaternion conjugate: (r, -i, -j, -k)"""
    return (q[0], -q[1], -q[2], -q[3])

def inverse(q: Vec4) -> Vec4:
    """Quaternion inverse: conj(q) / |q|^2"""
    n2 = sum(x*x for x in q)
    if n2 < 1e-15:
        return (1.0, 0.0, 0.0, 0.0)
    c = conjugate(q)
    return tuple(x/n2 for x in c)

def qmul(s1: Vec4, s2: Vec4) -> Vec4:
    """Semantic quaternionic product on S^3:
    normalize(Hamilton(normalize(s1), normalize(s2)))"""
    n1 = normalize(s1)
    n2 = normalize(s2)
    return normalize(hamilton(n1, n2))

def qdiv_left(s1: Vec4, s2: Vec4) -> Vec4:
    """Left quaternionic division: s1^{-1} * s2"""
    return qmul(tuple(x for x in inverse(normalize(s1))), s2)

def qdiv_right(s1: Vec4, s2: Vec4) -> Vec4:
    """Right quaternionic division: s1 * s2^{-1}"""
    return qmul(s1, tuple(x for x in inverse(normalize(s2))))

# ═══════════════════════════════════════════════════════════════════
# LOGICAL CONNECTIVES (from connectives.py)
# ═══════════════════════════════════════════════════════════════════

def AND(s1: Vec4, s2: Vec4) -> Vec4:
    return tuple(min(a, b) for a, b in zip(s1, s2))

def OR(s1: Vec4, s2: Vec4) -> Vec4:
    return tuple(max(a, b) for a, b in zip(s1, s2))

def NOT(s: Vec4) -> Vec4:
    return tuple(1.0 - a for a in s)

# ═══════════════════════════════════════════════════════════════════
# EXPLORATION 1: DISTRIBUTIVITY
# ═══════════════════════════════════════════════════════════════════

def explore_distributivity():
    print("=" * 60)
    print("EXPLORATION 1: DISTRIBUTIVITY OF PRODUCT OVER CONNECTIVES")
    print("=" * 60)
    print()
    print("Question: Does a (x) AND(b,c) = AND(a(x)b, a(x)c)?")
    print("Note: product on S^3, AND on [0,1]^4 -- different spaces.")
    print()

    # First, check if product is even closed on [0,1]^4
    n_negative = 0
    n_tests = 10000
    for _ in range(n_tests):
        s1 = tuple(random.random() for _ in range(4))
        s2 = tuple(random.random() for _ in range(4))
        prod = hamilton(normalize(s1), normalize(s2))
        if any(x < -1e-10 for x in prod):
            n_negative += 1

    print(f"  Closure on [0,1]^4: Hamilton product gives negative components")
    print(f"  in {n_negative}/{n_tests} = {100*n_negative/n_tests:.1f}% of cases.")
    print(f"  --> Product lives on S^3 (R^4), NOT [0,1]^4. Different spaces.")
    print()

    # Test distributivity on S^3 using the normalized product
    # Map AND to S^3: normalize(AND(s1,s2)) vs AND on sphere?
    # This doesn't type-check well because AND operates component-wise on [0,1]
    # and the sphere has components in [-1,1]

    # Alternative: define AND on S^3 as component-wise min of ABSOLUTE values
    # preserving signs... this doesn't make sense either.

    # The honest answer: the two operations live on different spaces.
    # Let's explore what bridge operations exist.

    print("  The operations live on INCOMPATIBLE spaces:")
    print("    - Connectives: [0,1]^4 (hypercube, unsigned)")
    print("    - Product:     S^3 (unit sphere in R^4, signed)")
    print()
    print("  Possible bridges:")
    print("    (a) Restrict product to [0,1]^4 cap S^3 (positive orthant of sphere)")
    print("    (b) Extend connectives to R^4 via signed operations")
    print("    (c) Use |components| to map S^3 -> [0,1]^4")
    print()

    # Let's test option (a): restrict to positive orthant
    print("  --- Option (a): Positive orthant of S^3 ---")
    n_positive_closed = 0
    n_pos_tests = 10000
    for _ in range(n_pos_tests):
        # Generate points in positive orthant of S^3
        s1 = normalize(tuple(random.random() for _ in range(4)))
        s2 = normalize(tuple(random.random() for _ in range(4)))
        prod = hamilton(s1, s2)
        if all(x >= -1e-10 for x in prod):
            n_positive_closed += 1

    print(f"  Product of positive-orthant S^3 stays positive:")
    print(f"  {n_positive_closed}/{n_pos_tests} = {100*n_positive_closed/n_pos_tests:.1f}%")
    print(f"  --> NOT closed on positive orthant.")
    print()

    # Test option (c): absolute value mapping
    print("  --- Option (c): Absolute value bridge S^3 -> [0,1] ---")
    print("  Define |q| = (|r|, |i|, |j|, |k|) as bridge back to [0,1]^4")
    print()

    def abs_bridge(q):
        return tuple(abs(x) for x in q)

    # Test distributivity with bridge: |a*AND(b,c)| vs AND(|a*b|, |a*c|)
    max_err_dist = 0.0
    for _ in range(1000):
        a = normalize(tuple(random.random() for _ in range(4)))
        b = tuple(random.random() for _ in range(4))
        c = tuple(random.random() for _ in range(4))

        # LHS: |a * normalize(AND(b,c))|
        bc_and = AND(b, c)
        lhs = abs_bridge(hamilton(a, normalize(bc_and)))

        # RHS: AND(|a*normalize(b)|, |a*normalize(c)|)
        ab = abs_bridge(hamilton(a, normalize(b)))
        ac = abs_bridge(hamilton(a, normalize(c)))
        rhs = AND(ab, ac)

        err = max(abs(l-r) for l, r in zip(lhs, rhs))
        max_err_dist = max(max_err_dist, err)

    print(f"  |a * AND(b,c)| vs AND(|a*b|, |a*c|):")
    print(f"  Max error: {max_err_dist:.4f}")
    print(f"  --> {'HOLDS' if max_err_dist < 0.01 else 'DOES NOT HOLD'} (threshold 0.01)")


# ═══════════════════════════════════════════════════════════════════
# EXPLORATION 2: QUATERNIONIC IMPLICATION
# ═══════════════════════════════════════════════════════════════════

def explore_quaternionic_implication():
    print()
    print("=" * 60)
    print("EXPLORATION 2: QUATERNIONIC IMPLICATION")
    print("=" * 60)
    print()
    print("Define: a ->_q b = a^{-1} * b (left division)")
    print("This is non-commutative: a->b != b->a in general.")
    print()

    # Test basic properties on unit quaternions
    i_hat = (0.0, 1.0, 0.0, 0.0)
    j_hat = (0.0, 0.0, 1.0, 0.0)
    k_hat = (0.0, 0.0, 0.0, 1.0)
    one = (1.0, 0.0, 0.0, 0.0)

    # i ->_q j = i^{-1} * j = -i * j = -k... wait
    # i^{-1} = conj(i)/|i|^2 = -i/1 = -i = (0,-1,0,0)
    # (-i) * j = -(ij) = -k = (0,0,0,-1)
    ij = hamilton(inverse(i_hat), j_hat)
    print(f"  i ->_q j = i^(-1) * j = {tuple(round(x,4) for x in ij)}")
    print(f"  Expected: -k = (0, 0, 0, -1)")

    ji = hamilton(inverse(j_hat), i_hat)
    print(f"  j ->_q i = j^(-1) * i = {tuple(round(x,4) for x in ji)}")
    print(f"  Expected: +k = (0, 0, 0, +1)")

    print(f"\n  Non-commutativity: i->j = -k, j->i = +k")
    print(f"  The ORDER of implication matters -- direction has a sign.")
    print()

    # Self-implication: a ->_q a = a^{-1} * a = 1
    print("  Self-implication a ->_q a:")
    for name, q in [("i", i_hat), ("j", j_hat), ("k", k_hat)]:
        result = hamilton(inverse(q), q)
        print(f"    {name} ->_q {name} = {tuple(round(x,4) for x in result)}")
    print(f"  All give (1,0,0,0) = identity. TAUTOLOGY property holds.")
    print()

    # Modus ponens check: if a and a->b, then b
    # a * (a^{-1} * b) = (a * a^{-1}) * b = 1 * b = b  (by associativity)
    print("  Modus ponens: a * (a ->_q b) = a * a^{-1} * b = b")
    a = normalize((0.3, 0.7, 0.2, 0.5))
    b = normalize((0.6, 0.1, 0.8, 0.3))
    imp_ab = hamilton(inverse(a), b)
    result = normalize(hamilton(a, imp_ab))
    err = max(abs(r - e) for r, e in zip(result, b))
    print(f"    a = {tuple(round(x,3) for x in a)}")
    print(f"    b = {tuple(round(x,3) for x in b)}")
    print(f"    a * (a->b) = {tuple(round(x,3) for x in result)}")
    print(f"    Error vs b: {err:.2e}")
    print(f"    Modus ponens: {'HOLDS' if err < 1e-10 else 'FAILS'}")
    print()

    # Contraposition: a ->_q b  vs  NOT(b) ->_q NOT(a)?
    # In quaternions, NOT doesn't have a natural meaning on S^3
    # But conjugation does: conj(q) = (r, -i, -j, -k)
    print("  Contraposition with conjugation as 'NOT':")
    print("  Define NOT_q(a) = conj(a)")
    a = normalize((0.3, 0.7, 0.2, 0.5))
    b = normalize((0.6, 0.1, 0.8, 0.3))

    imp_ab = hamilton(inverse(a), b)
    imp_nb_na = hamilton(inverse(conjugate(b)), conjugate(a))

    print(f"    a ->_q b      = {tuple(round(x,4) for x in normalize(imp_ab))}")
    print(f"    ~b ->_q ~a    = {tuple(round(x,4) for x in normalize(imp_nb_na))}")
    eq = max(abs(x-y) for x, y in zip(normalize(imp_ab), normalize(imp_nb_na))) < 1e-10
    print(f"    Equal? {eq}")
    if not eq:
        # Check if they're conjugates of each other
        conj_test = conjugate(normalize(imp_ab))
        eq2 = max(abs(x-y) for x, y in zip(conj_test, normalize(imp_nb_na))) < 1e-10
        print(f"    Conjugates? {eq2}")
        if not eq2:
            # What IS the relationship?
            ratio = hamilton(inverse(normalize(imp_ab)), normalize(imp_nb_na))
            print(f"    Ratio (a->b)^(-1) * (~b->~a) = {tuple(round(x,4) for x in ratio)}")
    print()

    # Non-commutativity statistics
    print("  Non-commutativity measure:")
    diffs = []
    for _ in range(10000):
        a = normalize(tuple(random.random() for _ in range(4)))
        b = normalize(tuple(random.random() for _ in range(4)))
        ab = hamilton(inverse(a), b)
        ba = hamilton(inverse(b), a)
        diff = math.sqrt(sum((x-y)**2 for x, y in zip(ab, ba)))
        diffs.append(diff)

    mean_diff = sum(diffs) / len(diffs)
    max_diff = max(diffs)
    min_diff = min(diffs)
    print(f"    ||a->b - b->a|| over 10K random pairs:")
    print(f"    Mean: {mean_diff:.4f}, Min: {min_diff:.4f}, Max: {max_diff:.4f}")
    print(f"    --> Strongly non-commutative (mean distance ~{mean_diff:.2f})")


# ═══════════════════════════════════════════════════════════════════
# EXPLORATION 3: DUAL PAIR PRODUCTS AND LOGIC
# ═══════════════════════════════════════════════════════════════════

def explore_dual_products():
    print()
    print("=" * 60)
    print("EXPLORATION 3: DUAL PAIR PRODUCTS")
    print("=" * 60)
    print()
    print("P9 found: dual_pair product ~= -1 (real inversion).")
    print("What does this mean logically?")
    print()

    # Simulate dual pairs: a and NOT(a) on S^3
    # If a = (r,i,j,k), a "logical dual" could be NOT(a) = (1-r,1-i,1-j,1-k)
    # But on S^3, the natural dual is -a = (-r,-i,-j,-k) (antipodal point)
    # Or conjugate: conj(a) = (r,-i,-j,-k)

    # Test: a * conj(a) = |a|^2 * (1,0,0,0) = (1,0,0,0) for unit quaternions
    print("  Product a * conj(a) for unit quaternions:")
    for _ in range(5):
        a = normalize(tuple(random.random() for _ in range(4)))
        prod = hamilton(a, conjugate(a))
        print(f"    {tuple(round(x,3) for x in a)} * conj = {tuple(round(x,4) for x in prod)}")
    print(f"  --> Always (1,0,0,0). Conjugation is the algebraic inverse.")
    print()

    # Test: a * (-a) = -|a|^2 = (-1,0,0,0) for unit quaternions
    print("  Product a * (-a) for unit quaternions:")
    for _ in range(5):
        a = normalize(tuple(random.random() for _ in range(4)))
        neg_a = tuple(-x for x in a)
        prod = hamilton(a, neg_a)
        print(f"    {tuple(round(x,3) for x in a)} * (-a) = {tuple(round(x,4) for x in prod)}")
    print(f"  --> Always (-1,0,0,0). Antipodal product = real inversion.")
    print()

    # This matches P9's finding: dual pairs give ~= -1
    # Semantically: if a and b are opposites (antipodal on S^3),
    # their product is -1 (pure real inversion).
    # This means: combining a concept with its opposite produces
    # NEGATION of the real axis -- the "crystallization" axis inverts.

    print("  INTERPRETATION:")
    print("  If concept and its opposite are antipodal on S^3:")
    print("    a (x) (-a) = -1")
    print("  Meaning: combining opposites produces INVERSION of reality.")
    print("  This is the algebraic signature of k^2 = i^2 = j^2 = -1:")
    print("  any pure axis interacting with itself negates.")
    print()

    # Now: what about the LOGICAL AND of a concept and its opposite?
    # AND(a, NOT(a)) in [0,1]^4:
    print("  Compare with LOGICAL AND of concept and its complement:")
    for _ in range(3):
        a = tuple(random.random() for _ in range(4))
        not_a = NOT(a)
        and_result = AND(a, not_a)
        print(f"    a = {tuple(round(x,2) for x in a)}")
        print(f"    AND(a, NOT(a)) = {tuple(round(x,2) for x in and_result)}")
        print(f"    min component = {min(and_result):.2f}")
        print()

    print("  AND(a, NOT(a)) = component-wise min(a, 1-a)")
    print("  Maximum value is 0.5 (at a=0.5 on each component)")
    print("  This is the FUZZY contradiction: partial truth, never full.")
    print()
    print("  CONTRAST:")
    print("  - Logical:     AND(a, NOT(a)) -> partial (fuzzy contradiction)")
    print("  - Quaternionic: a * (-a)       -> -1 (total inversion)")
    print("  These are DIFFERENT operations capturing DIFFERENT aspects")
    print("  of opposition.")


# ═══════════════════════════════════════════════════════════════════
# EXPLORATION 4: ALGEBRAIC STRUCTURE
# ═══════════════════════════════════════════════════════════════════

def explore_algebraic_structure():
    print()
    print("=" * 60)
    print("EXPLORATION 4: COMBINED ALGEBRAIC STRUCTURE")
    print("=" * 60)
    print()

    # The full structure is:
    # Space: S^3 (unit quaternions)
    # Operations:
    #   1. Hamilton product (x): group operation, non-commutative
    #   2. Component-wise min/max: lattice operations on [0,1]^4
    #      (but S^3 has components in [-1,1], not [0,1])
    #
    # For the lattice to work on S^3, we need to extend to [-1,1]^4
    # or restrict to the positive orthant.

    print("  The system has TWO algebraic layers:")
    print()
    print("  Layer 1 (Lattice): ([0,1]^4, AND=min, OR=max, NOT=1-x)")
    print("    -> Residuated lattice (verified)")
    print("    -> Commutative")
    print("    -> Specializes to Boolean, Fuzzy, Modal, Trivalent")
    print()
    print("  Layer 2 (Group): (S^3, product=Hamilton, inverse=conjugate)")
    print("    -> Non-abelian group")
    print("    -> Non-commutative")
    print("    -> Dual products = -1 (inversion)")
    print()
    print("  The two layers capture DIFFERENT aspects of information:")
    print("    Lattice: TRUTH (how much is present/absent)")
    print("    Group:   INTERACTION (what happens when concepts combine)")
    print()

    # Test: is there a natural homomorphism between the two?
    # f: [0,1]^4 -> S^3 via normalization
    # Does f(AND(a,b)) relate to f(a) * f(b)?
    print("  Homomorphism test: normalize(AND(a,b)) vs normalize(a)*normalize(b)")
    for _ in range(5):
        a = tuple(random.random() for _ in range(4))
        b = tuple(random.random() for _ in range(4))

        lhs = normalize(AND(a, b))
        rhs = normalize(hamilton(normalize(a), normalize(b)))
        err = math.sqrt(sum((x-y)**2 for x, y in zip(lhs, rhs)))
        print(f"    a={tuple(round(x,2) for x in a)}")
        print(f"    b={tuple(round(x,2) for x in b)}")
        print(f"    n(AND) = {tuple(round(x,3) for x in lhs)}")
        print(f"    n(a)*n(b) = {tuple(round(x,3) for x in rhs)}")
        print(f"    distance: {err:.4f}")
        print()

    print("  --> No homomorphism. The two operations are INDEPENDENT.")
    print("  This is the key structural finding: the operator O supports")
    print("  two independent algebraic structures on the same space,")
    print("  one commutative (logic) and one non-commutative (interaction).")
    print()

    # What IS the combined structure called?
    print("  CLASSIFICATION:")
    print("  The combined structure ([0,1]^4, min, max, 1-x, Hamilton)")
    print("  is a 'bi-algebraic' system:")
    print("    - A bounded distributive lattice (for truth)")
    print("    - With a non-commutative group action (for interaction)")
    print("  This resembles a 'quantale' but with a non-abelian group")
    print("  instead of a commutative monoid.")
    print()
    print("  In the literature:")
    print("    - Quantales (Mulvey 1986): complete lattice + monoid")
    print("    - Girard quantales: add involution (negation)")
    print("    - THIS: bounded lattice + non-abelian group (quaternions)")
    print("  No exact precedent found for this combination.")


# ═══════════════════════════════════════════════════════════════════
# EXPLORATION 5: THE ORDER MATTERS (NON-COMMUTATIVITY)
# ═══════════════════════════════════════════════════════════════════

def explore_order_matters():
    print()
    print("=" * 60)
    print("EXPLORATION 5: SEMANTIC NON-COMMUTATIVITY")
    print("=" * 60)
    print()
    print("  ij = k   but   ji = -k")
    print("  'Imagining then verifying' != 'Verifying then imagining'")
    print()

    i_hat = normalize((0.0, 1.0, 0.0, 0.0))
    j_hat = normalize((0.0, 0.0, 1.0, 0.0))
    k_hat = normalize((0.0, 0.0, 0.0, 1.0))

    products = [
        ("i*j", i_hat, j_hat),
        ("j*i", j_hat, i_hat),
        ("j*k", j_hat, k_hat),
        ("k*j", k_hat, j_hat),
        ("k*i", k_hat, i_hat),
        ("i*k", i_hat, k_hat),
    ]

    print(f"  {'Product':>6} | {'Result':>24} | Meaning")
    print(f"  {'-'*6}-+-{'-'*24}-+-{'-'*40}")
    meanings = {
        "i*j": "+k: imagining + verifying = selecting",
        "j*i": "-k: verifying + imagining = anti-selecting",
        "j*k": "+i: verifying + selecting = new potential",
        "k*j": "-i: selecting + verifying = anti-potential",
        "k*i": "+j: selecting + imagining = new direction",
        "i*k": "-j: imagining + selecting = anti-direction",
    }

    for name, q1, q2 in products:
        result = hamilton(q1, q2)
        r_str = tuple(round(x, 0) for x in result)
        print(f"  {name:>6} | {str(r_str):>24} | {meanings[name]}")

    print()
    print("  The sign flip captures ASYMMETRY of cognitive operations:")
    print("  - First imagine, then verify -> you SELECT (create hypothesis)")
    print("  - First verify, then imagine -> you ANTI-SELECT (falsify)")
    print("  - This IS Popper vs Bayes in algebraic form!")
    print()
    print("  In logical terms: the quaternionic product encodes")
    print("  the PROCEDURAL order of epistemic operations,")
    print("  while the lattice connectives encode the DECLARATIVE")
    print("  truth values. Two orthogonal aspects of reasoning.")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("QUATERNIONIC LOGIC: Exploring Product-Connective Interaction")
    print()

    explore_distributivity()
    explore_quaternionic_implication()
    explore_dual_products()
    explore_algebraic_structure()
    explore_order_matters()

    print()
    print("=" * 60)
    print("KEY FINDINGS")
    print("=" * 60)
    print("""
  1. INCOMPATIBLE SPACES: Connectives live on [0,1]^4, product on S^3.
     No distributivity -- they are independent operations.

  2. QUATERNIONIC IMPLICATION: a^{-1}*b satisfies:
     - Tautology: a -> a = 1
     - Modus ponens: a * (a -> b) = b
     - Non-commutative: a -> b != b -> a
     - Contraposition does NOT hold classically

  3. DUAL PRODUCTS = -1: Combining opposites produces real inversion.
     Logically: AND(a, NOT(a)) = fuzzy contradiction (partial).
     Algebraically: a * (-a) = -1 (total inversion). Different!

  4. BI-ALGEBRAIC STRUCTURE: The operator supports TWO independent
     algebraic structures -- a commutative lattice (truth) and a
     non-commutative group (interaction). No exact precedent found.

  5. NON-COMMUTATIVITY = PROCEDURAL ORDER: ij=k but ji=-k.
     The sign encodes whether you imagine-then-verify (hypothesis)
     or verify-then-imagine (falsification). Popper vs Bayes.
""")
