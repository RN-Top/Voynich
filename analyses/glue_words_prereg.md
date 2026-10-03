# Pre-registration: does the vocabulary split into glue words and content words?

Committed 2026-10-03, **before** the test below is run. Amend only below the line at the end.

## Idea

In known languages, function ("glue") words such as *the, of, and* are short and spread evenly across topics,
while content words are longer and tied to topics. If the Voynich text is language-like, among words of **similar
frequency**, shorter words should be more evenly spread across sections.

## Data

Currier B paragraph text (it covers five sections and three scribes). Words occurring at least 30 times there.

## Measures

- **Unevenness:** KL divergence (bits) between the word's distribution over sections and Currier B's overall
  section distribution, with +0.5 added to each section count. Low = even (glue-like), high = topic-bound.
- **Length:** number of letters (EVA).

## Test

Statistic: Spearman correlation between length and unevenness. Null: unevenness values shuffled among words in the
same frequency band (bands: 30–49, 50–99, 100–199, 200–499, 500+), 10,000 times, seed 20261003. This removes the
plain effect of frequency. Prediction: positive correlation (longer = more topic-bound). Pass: one-sided p < 0.01.

## Descriptive

The 20 most even common words (glue candidates) and the 20 most topic-bound (content candidates), with their
counts, lengths and main section.

---
Amendments (dated, below this line only):
