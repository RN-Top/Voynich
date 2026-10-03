# Star-name crib and sound shapes

Pre-registration: `analyses/sound_shapes_prereg.md`. Seed 20261003.

## Part A: star-name crib

- 32 star names; 86 star-label words; 1100 other label words.
- Star names whose consonant/vowel pattern matches a star label: **10**; drawing the same number of other labels: 9.3 on average.
- p = 0.451 → **NOT SUPPORTED**

| Star name | Pattern | Star labels with the same pattern |
|---|---|---|
| algol | VCCVC | okchor, okshor |
| rigel | CVCVC | chodar, cholar |
| wega | CVCV | chocfhy, cphocthy |
| altair | VCCVVC | ofcheor |
| deneb | CVCVC | chodar, cholar |
| markab | CVCCVC | saldal |
| menkar | CVCCVC | saldal |
| mirach | CVCVCC | darall |
| alhena | VCCVCV | odchecthy, okchody, ytchody |
| enif | VCVC | octhys, okos, olor, otar, otol, otor, otys |

## Part B: closest languages by sound shape (descriptive)

**Voynich A** (distance to its own shuffled-letter version: 0.250). Closest: fr 0.234, en 0.251, ca 0.251, tr 0.263, nb 0.277, nl 0.279, el 0.282, sv 0.282. Farthest: it 0.366, fi 0.367, sh 0.374.

Most common Voynich A word shapes: CVC 14%, CV 7%, CVCCC 6%, CVCV 4%, VCVC 4%, CVVC 3%

**Voynich B** (distance to its own shuffled-letter version: 0.247). Closest: en 0.273, lv 0.296, tr 0.308, lt 0.309, ms 0.317, ca 0.320, hu 0.320, ro 0.322. Farthest: sh 0.391, sl 0.407, fi 0.414.

Most common Voynich B word shapes: CVCV 7%, CVC 7%, VC 5%, CVCVC 4%, VCVC 4%, CVCCC 3%

## Reading the result

- **Part A, star-name crib: not supported.** Star labels share consonant/vowel patterns with medieval star names no
  more often than other labels do (10 vs 9.3, p = 0.45). The listed pairs are coincidences of shape (e.g. *rigel* and
  *chodar* are both CVCVC).
- **Part B, no close language.** The nearest languages by word shape are French, English, Catalan and Turkish for
  Voynich A, and English, Latvian and Turkish for Voynich B. But every language is about as far from the Voynich as
  the Voynich is from **a letter-shuffled copy of itself** (0.25), or farther. The ranking orders distant languages
  and does not identify one.
- The Voynich word shapes are dominated by short closed shapes (CVC, CV, CVCV), with notable runs of consonant-like
  symbols (CVCCC). That fits its slot structure more than any of the languages tested.
- Caveats: modern word lists and spelling. Arabic and Hebrew could not be compared on vowels. The vowel set
  {a, e, o, y} comes from Sukhotin, and a different reading of i or of the ch/sh clusters would change the shapes.
