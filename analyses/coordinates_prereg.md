# Pre-registration: are the diagram labels measurements (coordinates)?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author)

Star and figure labels may be coordinates or measurements, i.e. numbers. Numbers for nearby positions are similar
(12° and 13° differ by one step). So labels that sit next to each other on a diagram should be more alike than
labels far apart. Names would show no such gradient.

## Data

ZL3b label loci with a recorded clock position (`<!hh:mm>`), on the circular diagrams. Each label's first word is
used, cleaned with the canonical cleaner. Clock positions become angles (12 hours = 360°). Diagrams (pages) with at
least 8 positioned labels are used.

## Statistic

Within each diagram, for every pair of labels: angular distance d (0–180°) and dissimilarity (normalized edit
distance = Levenshtein distance / length of the longer word). The statistic is the Spearman correlation between d
and dissimilarity over all within-diagram pairs, pooled. A measurement-like gradient predicts a **positive**
correlation: farther apart means less alike.

A second, simpler version: the mean dissimilarity of **angular neighbours** (each label with its nearest label on
the same diagram) against all other pairs.

## Null

Labels shuffled among the positions within each diagram (10,000 shuffles, seed 20261003).

## Decision

**Supported** if the correlation is positive with p < 0.01. The neighbour comparison is reported with its own p, but
the decision rests on the correlation.

---
Amendments (dated, below this line only):
