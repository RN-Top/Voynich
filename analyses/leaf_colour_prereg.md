# Pre-registration: two-colour leaves (f1v type)

Date: 2026-10-04. Written and committed before any page is classified.

## Idea

On f1v (Erin's photo, `uploads/yale_hires/f1v.jpg`), the leaves are painted in **two colours**, green and tan/gold,
mixed on the same plant. On f67r2 the moons are red and gold. In the period colour key, green is Venus/copper and
gold is the Sun/gold, so two-colour leaves might mark a special class of plant.

## Step 1: classification (by eye, from the existing contact sheets of the low-resolution facsimile)

For every herbal page, record `leaf2`:

- **yes:** leaves of the same plant are painted in two clearly different colours (for example green and tan/gold,
  or green and red), and the second colour covers at least about a quarter of the leaves;
- **no:** all leaves are one colour, or the plant is uncoloured.

Red or brown veins, stems, roots and flowers do not count, only leaf blades. The table is saved to
`analyses/leaf_colours.csv` and committed before step 2.

## Step 2: test

Same machinery as `flower_colour_test.py`:

- **Pages:** herbal pages with paragraph text.
- **Similarity:** cosine of root-count vectors.
- **Statistic:** mean similarity of yes–yes pairs − mean similarity of yes–no pairs.
- **Null:** shuffle `leaf2` within Currier language, 10,000 times, seed 20261006.
- **Threshold:** one-sided p < 0.05.
- **Requirement:** at least 4 `yes` pages, otherwise the test is reported as not runnable.

## Secondary (descriptive)

- The opening words of the `yes` pages.
- Whether any of them is one of the 13 openings that share a root with star labels (`plant_star_report.md`), with a
  Fisher exact test.

## Weakness

The paint may have discoloured. Tan could be oxidised green, which would make `yes` partly reflect damage, not
intention.
