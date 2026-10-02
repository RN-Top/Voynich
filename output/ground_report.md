# Does a page's text mention that page's labels? (ground test)

Pre-registration: `analyses/ground_prereg.md`. 10,000 shuffles within section, seed 20261002.

| Test | Labels | Label words | Pages | Found in own page's text | Shuffled mean | p | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| G1 bath pages (Biological) | 110 | 117 | 11 | 24 | 23.2 | 0.448 | FAIL |
| G2 all sections | 615 | 691 | 37 | 60 | 58.2 | 0.38 | FAIL |

**Verdict: NOT SUPPORTED.**

**G1 bath pages (Biological), label words found in their own page's text:** f75v: dal, lol, olol, otedy, oteey, qokal, qotedy; f77r: otedy; f77v: shedy; f78r: dar; f80r: okaly, olky; f81v: otain; f82r: okal; f82v: okain, olkeedy, olkol, oteedy; f83v: okaiin, okchdy; f84r: dshedy, okedy, otedy

**G2 all sections, label words found in their own page's text:** f102v1: okeody; f102v2: cheor; f66r: daiin, dary, qokal; f67r2: air, daiin, dal, ofar; f68r1: otor; f69r: chey, daiin; f75v: dal, lol, olol, otedy, oteey, qokal, qotedy; f77r: otedy; f77v: shedy; f78r: dar; f80r: okaly, olky; f81v: otain; f82r: okal; f82v: okain, olkeedy, olkol, oteedy; f83v: okaiin, okchdy; f84r: dshedy, okedy, otedy; f88r: okol; f89r1: chol; f89r2: cheody, opcheor; f89v2: chody, sheol; f99r: dar, okeoly, okor; f99v: chor, doldam, oldy; fRos: okar, okchy, opar, otedy, oteedy, oteey

## Reading the result

- Label words show up in their own page's paragraph text **no more often** than in the text of other pages of the
  same section (bath pages: 24 vs 23.2 expected; all sections: 60 vs 58.2).
- The words that do match are mostly common words that turn up everywhere (otedy, daiin, okal, shedy). They are
  not page-specific names.
- So the running text does not visibly refer to its own page's labelled pictures, at least not by repeating the
  label words exactly. The labels may be names the text never repeats, or the text may describe the pictures in
  other words or forms.
