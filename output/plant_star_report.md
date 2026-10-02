# Do plant-page opening words share unusual spellings with star labels?

Pre-registration: `analyses/plant_star_prereg.md`. 116 herbal opening words; 86 star-label words; 1113 other label words; 10,000 draws, seed 20261002.

- Opening words sharing an unusual chunk with star labels: **13**
- Same number of words drawn from other labels: 4.4 on average
- p = 0.0002 → **SUPPORTED**

## Matches (descriptive)

| Plant page | Opening word | Star page | Star label | Shared chunk(s) |
|---|---|---|---|---|
| f1r | fachys | f67r2 | octhys | hys |
| f3v | koaiin | f68r1 | okoaly | koa |
| f6v | koary | f68r1 | okoaly | koa |
| f9r | tydlo | f68r1 | otydy | tyd |
| f9r | tydlo | f68r3 | otydg | tyd |
| f13v | koair | f68r1 | okoaly | koa |
| f16r | pocheody | f68r2 | opocphor | poc |
| f19v | pochaiin | f68r2 | opocphor | poc |
| f23r | pydchdom | f68r2 | oydchy | ydc |
| f27v | pochof | f68r2 | opocphor | poc |
| f30v | c@132hsc@133hain | f68r2 | o@167olchc@133hy | c@133h |
| f37r | tocphol | f68r1 | otochedy | toc |
| f52r | tdokchcfhy | f68r1 | chocfhy | fhy |
| f56r | o@167chal | f68r2 | o@167olchc@133hy | ^o@167 |

## Extra check (added after the run, not pre-registered)

Many matches have the form *star label = "o" + start of plant opening word* (koaiin ~ okoaly, pocheody ~ opocphor,
tydlo ~ otydy, o@167chal ~ o@167olch…). Herbal openings usually begin with a gallows letter, and labels often begin
"o" + gallows, so this could be a generic label habit. But 36 of 86 star-label words start with o + gallows/rare
symbol, against 441 of 1,113 other label words (42% vs 40%). Drawing comparison labels matched on that
(3,000 draws): 13 vs 4.5 expected, p = 0.0003. **The result holds.**

## Reading the result

- Plant-page opening words share unusual spellings with **star names** about 3× more than with other labels.
- The repeated form is **"o" + plant opening**: star labels look like the plant-page opening word with an "o" in
  front (and a different ending).
- Strongest groups: *koa-* (f3v, f6v, f13v ↔ okoaly, f68r1); *poc-* (f16r, f19v, f27v ↔ opocphor, f68r2);
  *tyd-* (f9r ↔ otydy, otydg); *o@167* (f56r ↔ f68r2).
- Caveats: 13 of 116 opening words is a minority; a shared 3-letter chunk is a weak link one by one; the
  transcription's star-label order cannot be matched to specific drawn stars from the PDF images.
- What it suggests: plant names and star names may be **built from the same stems**. That fits a herb–star system
  like the medieval *Fifteen Stars* tradition, but it does not prove it. A next test would ask whether the plants on
  the matched pages correspond to the herbs that tradition assigns to stars.
