# Pre-registration: does the Voynich plant order follow an alphabetical Latin herbal?

Date: 2026-10-04.

## Idea

Medieval herbals used by physicians across Europe (Irish medical families among them), such as the *Circa instans*,
list plants alphabetically by Latin name. If the Voynich herbal was copied from such a source, the identified plants
should appear in alphabetical order of their Latin names.

## Data

- **Plants:** the 8 agreed plants in `analyses/plant_ids_agreed.csv`.
- **Latin name:** for each plant, the first name already listed in `analyses/plant_names.csv` (committed earlier,
  for another purpose).
- **Book order:** current folio order.

## Test

- **Statistic:** Kendall τ between book order and alphabetical order.
- **Null:** exact, over all 8! orderings.
- **Prediction:** τ > 0 (one-sided). Threshold p < 0.05.

## Disclosure and weaknesses

- The names were fixed earlier, but their alphabetical order is easy to see by eye, so the result could be guessed
  before running.
- The book's pages were rebound out of their original order, which would weaken a real signal.
- With n = 8 the test has little power.
