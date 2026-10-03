# Can a letter-for-letter key turn the Voynich into Latin?

Pre-registration: `analyses/freqmatch_prereg.md`. Latin model: letter pairs from three Latin texts (80%); 5 restarts × 20,000 swaps per solve; seed 20261003.

- Ceiling (real held-out Latin): -3.370 bits/char
- Control (Latin under a random key, solved): -3.370; letters recovered **100%** → method works
- Floor (Latin letters shuffled within words, solved): -4.754

| Text | Symbols | Best score | Position (0 = floor, 1 = Latin) | f1r line 1 under best key |
|---|---|---:|---:|---|
| Voynich A | S1 | -3.549 | 0.87 | foaued ebos om oronnt duis duime arumld e bim duisce |
| Voynich A | S2 | -3.531 | 0.88 | qeuam aces et enerro pis pita ftlm a cit pisda |
| Voynich B | S1 | -3.458 | 0.94 | faqutd tcas am arallo dues duemt qrumid t cem duesnt |
| Voynich B | S2 | -3.460 | 0.94 | qauth tcas am arallo des demt gmih t cem desnt |

**Verdict: CONSISTENT WITH SUBSTITUTION.**

## Extra checks (added after the run, not pre-registered): the formal verdict does not hold

The pre-registered score only measures how Latin-like the **letter pairs** are. The Voynich text is unusually
regular, so its symbols can be mapped onto letters that pair plausibly without producing Latin. Two checks:

| Text, solved the same way | Score | Decoded words that exist in the Latin training vocabulary |
|---|---:|---:|
| Real held-out Latin (unciphered) | −3.370 | **86%** |
| Latin with every word reversed (structured, not Latin) | −4.090 | 12% |
| Voynich A | −3.482 | **16%** |
| Voynich B | −3.458 | **10%** |

The decoded Voynich has Latin-like letter pairs but **not Latin words**: 10–16%, about the level of reversed Latin,
and mostly very short forms (a, e, am). **Conclusion: the Voynich is not simple-substitution Latin.** The
pre-registered decision rule was too weak (letter-pair score alone), and this is recorded here rather than claimed
as a result. A real substitution would decode to real words, as the control does (100% of letters recovered).
