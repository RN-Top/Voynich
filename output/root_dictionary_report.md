# Root dictionary

Pre-registration: `analyses/root_dictionary_prereg.md`. 2,000 page shuffles within Currier language, seed 20261002. Paragraph text, 35,038 words, 3,168 distinct roots.

## T1. Do roots follow the topic?

- Root–section information: 0.2144 bits; shuffled 0.1033; p = 0.0005 → **PASS**

## T2. Section roots (FDR 5%; 23 of 256 roots with 10+ uses)

| Root | Uses | Main section | Share there | Section's share of text | p | Example words |
|---|---:|---|---:|---:|---:|---|
| alk | 28 | Stars/Recipes | 79% | 31% | 0.0005 | alkain, alkar, alkam, alkaiin |
| cheeo | 44 | Stars/Recipes | 73% | 31% | 0.0005 | cheeo, cheeody, ycheeo, cheeoy |
| cheed | 16 | Stars/Recipes | 88% | 31% | 0.0005 | cheedar, cheedaiin, cheed, cheedain |
| ched | 153 | Stars/Recipes | 71% | 31% | 0.0005 | chedaiin, chedar, chedal, chedain |
| kech | 49 | Stars/Recipes | 67% | 31% | 0.0005 | qokechy, kechy, okechy, qokechedy |
| lke | 41 | Stars/Recipes | 68% | 31% | 0.0005 | olkeeey, olkeol, lkeeey, lkeol |
| lk | 535 | Stars/Recipes | 51% | 31% | 0.0005 | lkaiin, olkeedy, lkeey, olkeey |
| lkee | 12 | Stars/Recipes | 83% | 31% | 0.0005 | lkeeor, olkeeol, lkeeol, olkeear |
| pair | 15 | Stars/Recipes | 80% | 31% | 0.0005 | pair, opair, ypair, opairam |
| ted | 54 | Stars/Recipes | 63% | 31% | 0.0005 | otedar, tedain, qoted, tedaiin |
| lsh | 141 | Biological | 58% | 19% | 0.001 | lshedy, olshedy, lshey, olshey |
| tched | 19 | Stars/Recipes | 79% | 31% | 0.001 | qotched, tchedar, qotchedar, tchedor |
| rsh | 18 | Biological | 72% | 19% | 0.001 | rshedy, rsheedy, orshy, rshey |
| teed | 28 | Stars/Recipes | 75% | 31% | 0.001 | oteed, qoteedar, qoteed, teedar |
| sheckh | 46 | Biological | 65% | 19% | 0.0015 | sheckhy, sheckhey, sheckhedy, sheckhdy |
| keed | 60 | Stars/Recipes | 62% | 31% | 0.0015 | qokeed, qokeedar, okeedal, keed |
| lch | 363 | Biological | 50% | 19% | 0.002 | lchedy, lchey, olchedy, olchey |
| lkch | 46 | Stars/Recipes | 72% | 31% | 0.0025 | lkchedy, lkchey, lkchdy, olkchdy |
| lr | 15 | Stars/Recipes | 73% | 31% | 0.0025 | lr, olr, lror |
| rar | 11 | Stars/Recipes | 82% | 31% | 0.0035 | raraiin, raram, rary, raraiiin |
| chd | 93 | Stars/Recipes | 52% | 31% | 0.0035 | chdal, chdaiin, chdar, chdam |
| tair | 43 | Stars/Recipes | 67% | 31% | 0.0035 | otair, tair, ytair, qotair |
| lkeeo | 17 | Stars/Recipes | 76% | 31% | 0.004 | lkeeody, olkeeody, olkeeo, lkeeo |

## Roots in both herbal openings and star labels (descriptive)

ch (2329 uses in paragraphs), cho (226 uses in paragraphs), chod (87 uses in paragraphs), cph (73 uses in paragraphs), k (4219 uses in paragraphs), kcho (52 uses in paragraphs), kod (24 uses in paragraphs), ksh (99 uses in paragraphs), t (2345 uses in paragraphs), tch (568 uses in paragraphs), tol (25 uses in paragraphs), tsh (88 uses in paragraphs)

## Reading the result

- **Roots follow the topic** (T1: 0.214 vs 0.103 bits, p = 0.0005), confirming at the root level what word
  beginnings showed.
- **Correct baseline for T2:** the column "section's share of text" is over the whole book, but the test shuffles
  pages within each Currier language. All 23 section roots belong to Currier-B sections, and within Currier B,
  Stars/Recipes is **46%** of the text and Biological **29%**. Judged against that baseline:
  - **Strong section roots:** *cheed* (88% in Stars/Recipes), *lkee* (83%), *rar* (82%), *pair* (80%), *alk*
    (79%), *tched* (79%), *lkeeo* (76%), *teed* (75%), *cheeo* (73%), *lr* (73%); Biological: *rsh* (72%),
    *sheckh* (65%), *lsh* (58%), *lch* (50%).
  - **Weaker** (common, only modestly above baseline): *lk* (51% vs 46%), *chd* (52% vs 46%).
- **Recipe pages and bath pages have their own vocabulary.** The bath pages favour roots with *l/r + sh/ch*
  (lsh-, rsh-, lch-) and *sheckh*. The recipe pages favour *lk*-, *ched*-, *cheeo*-, *pair*, *alk*.
- **No Herbal or Pharmacy roots pass.** Within Currier A, plant and jar pages use much the same roots.
- **Roots shared by herbal openings and star labels** come out as very common roots (ch, k, t…) under this crude
  rule. The plant–star link in `plant_star_report.md` lies in longer, rarer chunks, which this root rule cuts away.
