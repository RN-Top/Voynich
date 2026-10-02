# Do the two halves of the same zodiac sign share label vocabulary?

Pre-registration: `analyses/zodiac_halves_prereg.md`. Labels per page: f70v1 15, f70v2 30, f71r 15, f71v 15, f72r1 15, f72r2 29, f72r3 30, f72v1 30, f72v2 30, f72v3 30, f73r 30, f73v 30.

| | Similarity of label beginnings |
|---|---:|
| Aries halves (f70v1 + f71r) | 0.980 |
| Taurus halves (f71v + f72r1) | 0.900 |
| **Same-sign mean S** | **0.940** |
| All different-sign pairs, mean | 0.634 |
| Physically close different-sign pairs, mean | 0.726 |

- Z1: p = 0.00248 (2,016 pairs of different-sign pairs) → **PASS**
- Z2: S > close-pair mean → **PASS**

**Verdict: SUPPORTED.**

Exact words shared by the two halves (descriptive): f70v1+f71r: none; f71v+f72r1: char, otaiin.

## Extra check (added after the run, not pre-registered): this changes the interpretation

All four half-pages (15 labels each) are compared with each other, across signs:

| Pair | Same sign? | Similarity |
|---|---|---:|
| f70v1 + f71r | Aries + Aries | 0.980 |
| f71v + f72r1 | Taurus + Taurus | 0.900 |
| f70v1 + f71v | Aries + Taurus | 0.904 |
| f70v1 + f72r1 | Aries + Taurus | 0.908 |
| f71r + f71v | Aries + Taurus | 0.895 |
| f71r + f72r1 | Aries + Taurus | 0.913 |

The Taurus halves are no more alike than Aries–Taurus pairs. All four half-pages are similar because their labels
are dominated by `ot-` (6–12 of 15). The pre-registered control (Z2) did not include half-page pairs of different
signs, so it missed this.

**Conclusion:** the test passed by its rule, but the effect comes from the half-page format, not from the sign.
This is **not** counted as evidence that zodiac labels relate to their sign. Only the Aries pair stands out, and one
pair is too little to build on.
