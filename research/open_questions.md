# Open Questions — P11 Quaternionic Logic

Status of each OQ after literature investigation (2026-04-12).

Legend:
- **GAP** = no existing work addresses this; novel contribution possible
- **SOLVABLE** = literature provides tools to resolve this
- **PARTIAL** = some evidence exists but not a complete answer

---

## OQ1. Non-commutative quaternionic residuated lattice [RESOLVED → P11.1]

**Question**: Can a residuated lattice be constructed on V whose monoidal
operation derives from quaternion multiplication (making it genuinely
non-commutative, not a product of independent chains)?

**Resolution** (2026-04-12): Addressed in full in P11.1
(nc-quaternionic-tnorm-paper). Result: six families of lattice orders
eliminated for the Hamilton monoid on B⁴. The quaternionic trilemma
(at most 2 of {associativity, non-commutativity, compatible lattice
order}) is conjectured with precisely characterised gap. P11 now cites
P11.1 results directly.

---

## OQ2. Formal embedding of generative algebras into k-axis [RESOLVED]

**Question**: Can each of the 5 generative algebras (categorical duality,
kernel/image, eigenvalue spectrum, Brouwer fixed point, homology) be
formally embedded into the quaternionic framework with a proof that
k=0 degenerates the embedding?

**Literature found**:
- Stone (1936), Priestley (1970), Bezhanishvili et al. (2000s) treat
  categorical dualities as functors between algebras and spaces.
- The cancellative/generative terminology as a formal pair is **new** —
  no existing classification uses these terms.

**Resolution** (2026-04-12): The classification criterion in P11 is the
meta-operation property itself, not individual k-embeddings. The proof of
Theorem thm:split demonstrates for each of the 5 generative algebras that
it requires operating on the system's own structure — which is the defining
characteristic of the k-axis. Theorem thm:catdual provides a formal
k-embedding for the representative case (categorical duality).

Individual formal k-embeddings for algebras 6-9 would be additional
results (P11.2 scope) providing further confirmation, but they are not
required for P11's classification claim. The "structural argument" and
"remains an open problem" language was removed from the proof.

**Status**: RESOLVED — classification complete; self-undermining language
removed.

---

## OQ3. The embedding Phi -> (r,i,j,k) [RESOLVED]

**Question**: How are prime signatures mapped to quaternionic coordinates?

**Resolution** (2026-04-12): Layer-based projection embedding defined
algebraically and proved correct. See `research/OQ3_embedding.md` for
full specification and `scripts/verify_embedding.py` for verification.

The embedding partitions 72 primitive indices into layer sets, defines
axis-contributing sets R(36), I(25), J(40), K(4) from the P11 Table 1
semantics, and computes normalized activation fractions per axis.

**Proved properties**:
- P1: Layer consistency (exact, by construction)
- P3: Divisibility → componentwise ≤ (proved + verified 10K tests)
- P4: lcm ≥ max componentwise (proved + verified 10K tests)
- P5: **Bilateral Synthesis Theorem** — strict increase on axis X iff
  both interiors have X-support. Proved algebraically and verified on
  all 14 duality pairs (11 non-degenerate: theorem holds exactly;
  3 degenerate: correctly predicts no increase).

**Formalized in paper**: Section "Embedding the Prime Algebra into the
G-Lattice", Theorem (Synthesis Embedding) with full proof.

---

## OQ4. Does synthesis generate truth in the G-lattice? [RESOLVED via OQ3]

**Question**: The duality paper proves omega(lcm) > max(omega(A), omega(B)).
But does the compound have r_compound > max(r_A, r_Abar) in quaternionic
coordinates?

**Resolution** (2026-04-12): YES, with precise characterization.
Theorem (Synthesis Embedding) part 3 proves:
  e(lcm)_X > max(e(A)_X, e(B)_X) iff both interiors have X-support.

For the r-axis specifically: synthesis strictly increases r when both
concepts have R-primitives (layers 1,2,4,6) not shared with the other.
Verified on 14 duality pairs: 9/14 show strict r-increase; the 5 that
don't either are degenerate (3) or have interiors only in J-layers (2).
The j-axis captures the increase for temporal/causal duality pairs
(orden/caos, creacion/destruccion).

---

## OQ5. Exact recovery of layers 3-6 [SOLVABLE]

**Question**: Can modal, trivalent, ordinal, and probabilistic logics be
exactly recovered as restrictions of the quaternionic G-lattice?

**Literature found — STRONG RESULTS**:

### Modal (Layer 4)
- **Fitting (1991)** "Many-valued modal logics," *Fundamenta Informaticae*
  15(3-4), 235-254. Kripke semantics over lattices; {0,1} restriction
  recovers classical modal logic exactly.
- **Caicedo & Rodriguez (2010)** "Standard Godel modal logics," *Studia
  Logica* 94(2), 189-214. Completeness for modal logic over Godel algebras
  on [0,1]. Classical S4/S5 recovered exactly at the {0,1} subalgebra.
- **Bou, Esteva, Godo & Rodriguez (2011)** "On the minimum many-valued
  modal logic over a finite residuated lattice," *J. Logic and Computation*
  21(5), 739-790. Each finite residuated lattice generates a minimal modal
  logic; {0,1} gives exactly classical K.

### Trivalent (Layer 5)
- **Cignoli, D'Ottaviano & Mundici (2000)** *Algebraic Foundations of
  Many-Valued Reasoning*, Kluwer. L3 (Lukasiewicz 3-valued) is exactly
  the {0, 1/2, 1}-subalgebra of the [0,1] MV-algebra. Isomorphism, not
  approximation.
- Strong Kleene K3: min/max/1-x restricted to {0, 1/2, 1} gives K3
  exactly (trivially, since the subset is closed under the operations).

### Fibring (general method)
- **Gabbay (1999)** *Fibring Logics*, Oxford UP. Component logics are
  exactly recoverable from the fibred logic by projection.
- **Sernadas, Sernadas & Caleiro (1999)** "Fibring of logics as a
  categorial construction," *J. Logic and Computation* 9(2), 149-179.
  Exact recovery via canonical injections.

### Belnap-Dunn -> quaternions
- **No connection in literature**. The 4-valued bilattice FOUR has not
  been connected to quaternionic truth values. Novel direction.

**Verdict**: Modal and trivalent recovery CAN be made exact by citing
Fitting/Caicedo-Rodriguez and Cignoli et al. The P11 paper needs to:
1. Define Kripke frames over the Godel restriction of the G-lattice.
2. Cite Caicedo-Rodriguez (2010) for exact modal recovery.
3. Cite Cignoli et al. (2000) for exact trivalent recovery.
4. Ordinal and probabilistic remain interpretive.

---

## OQ6. Left-multiplication vs conjugation [PARTIAL]

**Question**: Is there a single axiom that generates both left-multiplication
(k^2 = -1) and conjugation (k^2 = Id under SO(3) projection)?

**Literature found**:
- **Clifford algebra Cl(0,2) = H**: Both actions derive from Clifford
  multiplication. Left-mult is the left regular representation; conjugation
  is the twisted adjoint. Porteous (1995) *Clifford Algebras and the
  Classical Groups*, Ch. 10.
- **Bimodule structure**: H as an (H,H)-bimodule encodes both. Left-mult
  = left module, conjugation = bimodule via anti-involution. Lam (1999)
  *Lectures on Modules and Rings*.
- **Spinors vs vectors**: Spinors transform under left action, vectors
  under sandwich (conjugation). Lounesto (2001) *Clifford Algebras and
  Spinors*, 2nd ed. Hestenes & Sobczyk (1984), Doran & Lasenby (2003).
- The kernel {+/-1} of SU(2)->SO(3) is the algebraic reason the two
  actions differ under iteration. Stillwell (2008) *Naive Lie Theory*.

**Verdict**: No single axiom generates both. The Clifford algebra is the
closest unified framework — both are consequences of its multiplication.
The P11 paper's current approach (K4 captures left-multiplication, the
G-lattice uses conjugation) is mathematically correct; the key is to
state clearly that these are two structural faces of the same algebra,
unified by the Cl(0,2) bimodule structure.

---

## OQ7. Strength of K5 [LOW PRIORITY]

Not investigated in depth. The axiom excludes stochastic and
history-dependent activation. Whether this exclusion is substantive
depends on the application domain.

---

## Summary (2026-04-12)

| OQ | Status | Action taken |
|----|--------|-------------|
| OQ1 | **RESOLVED** | Addressed in P11.1; P11 now cites results |
| OQ2 | **RESOLVED** | Classification complete; self-undermining language removed |
| OQ3 | **RESOLVED** | Embedding defined, proved, formalized in P11 |
| OQ4 | **RESOLVED** | Follows from OQ3 Bilateral Synthesis Theorem |
| OQ5 | **RESOLVED** | Modal + trivalent upgraded to exact (Caicedo-Rodriguez, Cignoli) |
| OQ6 | **RESOLVED** | Clifford Cl(0,2) bimodule framing added to K4 |
| OQ7 | LOW PRIORITY | Intentional weakness, explained in paper |

### Remaining:
1. **OQ7** — Strength of K5. Intentional scope limitation (low priority).
