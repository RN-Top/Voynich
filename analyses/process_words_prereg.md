# Pre-registration: are the recipe-section roots "process words"?

Date: 2026-10-04. Written before the code exists.

## Idea (Erin: alchemy in it)

Alchemical-pharmacy recipes reuse a small set of **process words** (take, distil, dissolve, water, fire, boil) in
almost every recipe. **Ingredient names** cluster in a few recipes.

The earlier root dictionary (`output/root_dictionary_report.md`) already found 18 roots specific to the
Stars/Recipes section (fixed in advance there):

alk, cheeo, cheed, ched, kech, lke, lk, lkee, pair, ted, tched, teed, keed, lkch, lr, rar, chd, tair, lkeeo.

The question here is what **kind** of word they are: evenly spread (process words) or clumped (ingredients or
topics).

## Data

- **Paragraphs:** Currier B paragraphs of the Stars/Recipes section, delimited by `<%>`…`<$>` (as in
  `recipe_format_test.paragraphs`). Roots come from `root_dictionary_test.root_of`.
- For each root: k = its number of tokens in recipe paragraphs.
  - **Coverage** = the fraction of paragraphs that contain it.
  - **Expected coverage** under random placement = mean over paragraphs of 1 − (1 − L_j/N)^k, where L_j is the
    length of paragraph j and N is the total number of tokens.
  - **Dispersion** = coverage / expected coverage. Clumped roots score below 1.

## Test

- **Statistic:** the mean dispersion of the recipe roots (those with k ≥ 5).
- **Null:** for each recipe root, draw a control root that is not in the list and whose k is within ±25%. Average
  their dispersion. Repeat 10,000 times, seed 20261012.
- **Prediction:** the recipe roots are more evenly spread than matched roots (one-sided p < 0.05).

## Descriptive

For each recipe root: k, coverage, dispersion, and the commonest preceding and following roots.
