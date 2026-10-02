# Pre-registration: does the C → L → P → R cycle work with a fifth element?

Committed 2026-10-02, **before** the test below is run. Amend only below the line at the end.

## Idea (from the project author)

The four-step cycle C → L → P → R (archived: it did not beat lower-order controls) may have failed because
it is missing a fifth, "grounding" element, like the quintessence added to the four classical elements.

## How the fifth element is defined

The cycle assigns every word a role from its ending. About 14% of paragraph words have **no** role (state `?`
in `structural_validation.py`). These are the natural candidate for a missing fifth element, so `?` becomes
the fifth state. Nothing else changes: same corpus (ZL3b, paragraph text, 35,038 words), same endings.

The fifth element can sit in 4 distinct places in the cycle: C?LPR, CL?PR, CLP?R, CLPR? (CLPR? is the same
cycle as ?CLPR). All four are tried; observed and null both take the **best** of the four, so trying four does
not inflate the result.

## Statistic

Share of 5-word windows (all five words on the same line) that run one full step of the cycle in order,
e.g. C L ? P R or L ? P R C. A cycle that exists in the text should produce these runs more often than
the controls do. (The 2-word version cannot beat a Markov-1 control by construction, so it is reported but
not used for the verdict.)

## Controls

1. Within-line shuffle (2,000): same words, random order within each line.
2. Markov-1 twins (1,000): random text with the same word-to-next-word role statistics.
3. Markov-2 twins (1,000): same, using the previous two roles.

Seed 20261002.

## Decision rule

- **Supported:** p < 0.01 against **both** Markov-1 and Markov-2 twins (5-word windows).
- **Not supported:** otherwise.

Also reported, descriptively: the rank of the best five-element cycle among all 24 possible orders of the five
states, and which endings make up the `?` group.

---
Amendments (dated, below this line only):
