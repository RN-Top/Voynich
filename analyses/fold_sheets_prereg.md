# Pre-registration: do the two halves of a folded sheet belong together?

Committed before any code for this test was written or run. Amend only below the line at the end.

## Idea (from the project author)

Folding the book brings its front, back and center fold together, and pages that come together that way act
as a key. The physical version: each gathering (quire) is made of sheets folded in half and nested, so in
a gathering whose leaves are numbered `lo..hi`, leaf `k` and leaf `lo + hi - k` are the two halves of one
sheet (the outermost sheet holds the gathering's front and back, the innermost is its center fold).

## Data

- Canonical `parser.parse_zl3b()`, all text on the leaf (both sides, all panels).
- A leaf is a folio number (f1r + f1v = leaf 1).
- Gatherings come from the `$Q=` codes in ZL3b.
- Sheet partner of leaf `k` is `lo + hi - k` within its gathering. Pairs where either leaf is missing,
  or where the leaf is its own partner, are skipped.
- This is an approximation. Foldouts and missing leaves make the real sheet structure uncertain in
  places.

## Statistics

- **S1 shared vocabulary:** cosine similarity of the two leaves' word-count vectors.
- **S2 word line-up:** for each side of leaf A and each side of leaf B, the share of positions (same line
  number, same word number) holding the identical word; averaged over side pairings.

## Test

Observed value: the mean of S over all sheet pairs. Null: within each gathering, randomly re-pair the
present leaves (10,000 times, seed 20261001), and take the mean of S over the same number of pairs per
gathering. One-sided p (sheet pairs more similar).

Report two versions:
- **(a)** all sheet pairs
- **(b)** sheet pairs that are **not** next to each other. Center-fold pairs are adjacent leaves, and
  adjacent leaves can share text simply because the writing continues across them.

## Decision rule

- **Supported:** S1 **or** S2 has p < 0.01 in version (b).
- **Adjacency only:** significant in (a) but not in (b). The effect is explained by neighbouring leaves.
- **Not supported:** otherwise.

---
Amendments (dated, below this line only):
