# Quaternionic Logic: A G-Lattice Unifying Boolean and Fuzzy Frameworks

**Author:** J. Arturo Ornelas Brand — arturoornelas62@gmail.com
**Paper DOI:** [10.5281/zenodo.19562014](https://doi.org/10.5281/zenodo.19562014) (v0.1.1, all versions: [10.5281/zenodo.19560986](https://doi.org/10.5281/zenodo.19560986))
**Status:** Published on Zenodo.

## Result

A formal logic defined as a **G-lattice**: a bounded residuated lattice on [0,1] x R^3 equipped with an SU(2) group action by quaternionic conjugation.

- **Connectives** (AND, OR, NOT, IMPLIES) define _what_ is true
- **Conjugation** q\*a\*q^{-1} defines _from which perspective_ you evaluate
- **Central theorem:** connectives commute with context transformations if and only if they operate only on the real component
- **Corollary:** Boolean logic is the context-free special case. Full quaternionic logic is context-dependent.

Six known logics (Boolean, fuzzy, modal, trivalent, ordinal, probabilistic) are recovered as dimensional restrictions. No exact precedent for this combination (residuated lattice + SU(2) conjugation with real-part invariance) was found in the literature.

## Key findings

| Property | Evidence |
|---------|---------|
| 7/7 specializations verified | `scripts/connectives.py` |
| Re invariant under all context changes | max error 5.55e-16 |
| Soundness (modus ponens in all contexts) | 0 violations / 50K tests |
| Domain [0,1] x R^3 closed | 0 violations / 50K tests |
| (i,j,k) operationally distinguishable | decisions change 49.6%, truth changes 0% |
| Panorama = Boolean logic | Im averages to ~0 over SU(2) |

Full results: [`RESULTS.md`](RESULTS.md)

## Repository structure

```
README.md                              This file
RESULTS.md                             Complete computational results and theoretical findings
LICENSE                                BUSL-1.1
scripts/
  connectives.py                       Connective definitions + 7/7 specialization verification
  explore_quaternion_interaction.py     Product-connective interaction exploration
  bridge_exploration.py                Failed and successful bridge attempts
  context_bridge.py                    G-lattice: conjugation as context transformation
  verify_resolutions.py                Verification of domain, soundness, non-decoration
  verify_completeness.py               Completeness reduction to G~ (Godel with involutive negation)
  verify_embedding.py                  k-axis embeddings of 5 generative algebras
research/
  open_questions.md                    7 open questions (5 resolved, 2 deferred to P11.1)
  OQ3_embedding.md                     Detailed analysis of the embedding question
  bibliography.md                      Working bibliography (~35 refs)
  actionable_next.md                   Follow-up items post-publication
paper/
  quaternionic_logic.tex               Paper source
  quaternionic_logic.pdf               Compiled paper (24 pp)
```

## Dependencies

- Python 3.8+
- NumPy

## Running

```bash
# Verify all specializations (7/7)
python scripts/connectives.py

# Explore product-connective interaction
python scripts/explore_quaternion_interaction.py

# Bridge exploration (failed attempts + alpha family)
python scripts/bridge_exploration.py

# G-lattice verification (central theorem)
python scripts/context_bridge.py

# Verify resolved open problems (domain, soundness, non-decoration)
python scripts/verify_resolutions.py

# Verify completeness via reduction to G~
python scripts/verify_completeness.py

# Verify k-axis embeddings of generative algebras
python scripts/verify_embedding.py
```

## Companion papers

Three companion papers extend the framework developed here:

- **P11.1** — *Toward a Non-Commutative Residuated Lattice from Quaternion Multiplication*. DOI: [10.5281/zenodo.19561407](https://doi.org/10.5281/zenodo.19561407). Investigates whether the Hamilton product can serve as a genuinely non-commutative conjunction; proves a trilemma on the semantic domain V and on the full ball B^4.
- **P12** — *Duality Synthesis in Quaternionic Logic: How Opposites Generate Truth*. DOI: [10.5281/zenodo.19561634](https://doi.org/10.5281/zenodo.19561634). Develops the synthesis operation on the prime algebra and shows that opposites generate new truth at higher algebraic layers.
- **P13** — *Pre-Logical States and the Birth of Information*. DOI: [10.5281/zenodo.19561722](https://doi.org/10.5281/zenodo.19561722). Formalises pre-logical states (points where the truth axis is undefined) and proves that information emerges as the compound concept of the pre-logical/logical duality.

## Citation

This paper:

```
Ornelas Brand, J.A. (2026). Quaternionic Logic: A G-Lattice Unifying
Boolean and Fuzzy Frameworks (v0.1.1). Zenodo.
https://doi.org/10.5281/zenodo.19562014
```

Concept DOI (all versions): [10.5281/zenodo.19560986](https://doi.org/10.5281/zenodo.19560986)

Companion papers:

```
Ornelas Brand, J.A. (2026). Toward a Non-Commutative Residuated Lattice
from Quaternion Multiplication (v0.1.0). Zenodo.
https://doi.org/10.5281/zenodo.19561407
```

```
Ornelas Brand, J.A. (2026). Duality Synthesis in Quaternionic Logic:
How Opposites Generate Truth (v0.1.0). Zenodo.
https://doi.org/10.5281/zenodo.19561634
```

```
Ornelas Brand, J.A. (2026). Pre-Logical States and the Birth of
Information (v0.1.0). Zenodo.
https://doi.org/10.5281/zenodo.19561722
```

## License

Business Source License 1.1 (BSL 1.1). Non-production use is permitted. On the Change Date (**2030-04-09**), or the fourth anniversary of the first publicly available distribution of a given version, whichever comes first, the work becomes available under the Change License (**Apache License, Version 2.0**).

For alternative licensing arrangements, contact arturoornelas62@gmail.com. See [`LICENSE`](LICENSE) for full terms.
