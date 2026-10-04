# Pre-registration: are the starred paragraphs written in recipe format?

Date: 2026-10-04. Written before the code exists.

## Idea (Erin: alchemical pharmacy)

Medieval pharmacy and alchemical-medicine books, such as the *Antidotarium Nicolai* and Rupescissa's
*De consideratione quintae essentiae*, are collections of short recipes in a fixed format:

*Take … [ingredients with quantities] … ana (equal parts) … make … it is good for …*

If the starred paragraphs of the Stars/Recipes section (f103–f116) are such recipes, they should show this skeleton
more than other text in the same language.

## Data

- **Paragraphs:** from `parse_zl3b`, `P` loci only, split into paragraphs at `@P` headers. Only paragraphs of 5 or
  more words are used.
- **Recipe group:** Currier B paragraphs in section "Stars/Recipes".
- **Control group:** Currier B paragraphs in every other section (Biological, Herbal B, and so on). Using the same
  language removes the A/B dialect difference.
- **Repeat rate:** R(list) = the probability that two different items drawn from the list are the same word
  (Simpson index).

## Tests (Bonferroni over 3: each needs p < 0.0167, one-sided)

**T1. Opening formula.**
- Statistic: (R of first words − R of interior words) in recipes, minus the same in controls.
- Prediction: > 0.
- Null: shuffle the recipe/control label among paragraphs, 10,000 times, seed 20261011.

**T2. Closing formula.** As T1, using the last word of each paragraph.

**T3. Quantity words at regular spacing.**
- Within each recipe paragraph, take every word of 3 letters or fewer that occurs 3 or more times, and compute the
  coefficient of variation (CV) of the gaps between its occurrences.
- Statistic: mean CV across all such cases.
- Prediction: lower than when words are shuffled within each paragraph (regular spacing).
- Null: within-paragraph shuffles, 10,000 times.
- The same statistic for the control group is reported, not tested.

## Weaknesses

- Paragraph-first words in Voynich text are unusual everywhere (gallows letters). Comparing with control paragraphs
  of the same language removes that common effect.
- Line-end forms (-m) affect last words in all sections, and the same comparison removes that too.
