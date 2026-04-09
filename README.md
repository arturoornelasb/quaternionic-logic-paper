# Quaternionic Logic: A G-Lattice Unifying Boolean and Fuzzy Frameworks

**Author:** J. Arturo Ornelas Brand — arturoornelas62@gmail.com
**Status:** Computational verification complete. Paper in preparation.

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
paper/
  quaternionic_logic.tex               Paper (forthcoming)
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
```

## Companion work

This project builds on:

- **P9:** [The Primitive Equation of Information](../primitive-equation-paper/) — provides the operator O = {0, 1, +, i, j, k}, the Four Kingdoms, and the 72 semantic primitives
- **La Danza Cosmica de los Opuestos** (book, in preparation) — philosophical framework establishing the anchor/perspective system that this paper formalizes

## Citation

```
Ornelas Brand, J.A. (2026). Quaternionic Logic: A G-Lattice Unifying
Boolean and Fuzzy Frameworks. In preparation.
```

## License

Business Source License 1.1 (BUSL-1.1)
