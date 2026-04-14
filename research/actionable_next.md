# Actionable next steps — ordered by impact

## 1. UPGRADE MODAL + TRIVALENT RECOVERY [can do now]

**What**: Add Kripke frame construction over the Godel restriction of
the G-lattice. Cite Caicedo & Rodriguez (2010) for modal, Cignoli et al.
(2000) for trivalent. Change "interpretive correspondences" to "exact
recoveries" for these two layers.

**Where in P11**: Section 7 (Recovery), Remark 4 (interpretive
correspondences), and the abstract.

**Effort**: ~1 day. Requires writing the Kripke frame definition and
citing the completeness results.

**Impact**: Upgrades 2 of the 4 "interpretive" correspondences to exact
isomorphisms. The abstract could then say "four exact, two interpretive."

## 2. ADD CLIFFORD ALGEBRA FRAMING TO K4 [can do now]

**What**: Cite Porteous (1995) and Lounesto (2001) to frame the
left-multiplication / conjugation distinction as the standard Cl(0,2)
bimodule structure. Spinors transform under left action, vectors under
sandwich — this is the mathematical explanation for why K4 and the
G-lattice action differ.

**Where in P11**: The K4 discussion (Section 4), already partially
rewritten.

**Effort**: ~2 hours. Add references and one paragraph.

**Impact**: Grounds K4 in established mathematics rather than leaving
it as a novel observation.

## 3. DEFINE THE EMBEDDING Phi -> (r,i,j,k) [DONE]

Completed 2026-04-12. Layer-based projection embedding defined,
proved (Theorem: Synthesis Embedding), and verified computationally.
Added as Section "Embedding the Prime Algebra into the G-Lattice" in P11.
Bilateral synthesis theorem gives exact characterization of strict increase.
See `research/OQ3_embedding.md` for details.

## 4. CONNECT TO LAWVERE'S ADJOINT SYNTHESIS [enriches P12]

**What**: The synthesis operation a (+) abar = lcm(Phi(a), Phi(abar))
from P12 parallels Lawvere's formalization of Hegelian Aufhebung via
adjoint functors. The monad T = GF from an adjunction is the categorical
analogue of the synthesis producing new structure. Cite Lawvere (1969,
1996).

**Where**: P12 Discussion section.

**Effort**: ~1 day. Conceptual connection + citations.

**Impact**: Grounds the synthesis in established categorical foundations.

## 5. EXPLORE BELNAP-DUNN -> QUATERNIONS [novel territory]

**What**: Belnap's FOUR = {N, F, T, B} is a 4-valued bilattice. The
quaternionic truth values also have 4 dimensions. Is there a formal
connection? FOUR has two orderings (truth and information); the
G-lattice has Re (truth) and ||Im|| (epistemic weight). This might
yield a genuine embedding.

**Effort**: ~1 week. Speculative but potentially high-impact.

**Impact**: If successful, connects quaternionic logic to an established
4-valued framework.

## 6. FLAG AS FUTURE WORK (don't attempt now)

- OQ1 (quaternionic t-norm) — separate paper territory
- OQ2 (individual generative algebra embeddings) — program of 5+ results
- OQ7 (K5 strength) — low priority
