# Beinecke MS 408 (Voynich Manuscript) Decipherment Workbench
### A Dual-Dialect Compounding Architecture: Venetian Romance Phonetics & Early High German Compounding Syntax

**Repository:** `RN-Top/Voynich`  
**Live Interactive Dashboard:** [voynich-xdbkaduqmatywumbtkdcgd.streamlit.app](https://voynich-xdbkaduqmatywumbtkdcgd.streamlit.app/)  
**Primary Corpus Standard:** Standardized Interlinear Voynich Transliteration File Format (IVTFF) EVA 2.0 / ZL3b-n Standard ($N = 38,958$ tokens across 227 folios with the current `parser.py`; committed file SHA-256 `3e617b2dd4...`)

---

## 1. Project Overview & Primary Mission

For more than 600 years, Beinecke MS 408 has resisted cryptanalysis due to persistent reliance on unconstrained anagramming, arbitrary monoalphabetic substitution ciphers, or dismissals of the codex as an untestable mechanical hoax.

This repository hosts an end-to-end computational decipherment engine and verification suite that models the manuscript as an **operational state machine**, an **alchemical/pharmaceutical compounding compiler**, and a **dual-dialect technical trade register**:

1. **Phonetic & Phonological Layer (Venetian / Northern Italian Romance):** Unsupervised vowel-consonant optimization via Sukhotin's algorithm isolates an alternating $CVC$ / $CVCV$ syllabic rhythm with a 33.3% vocalic ratio ($V = \{a, o, h, t, i, y\}$), precisely matching 15th-century Northern Italian trade-apothecary vernacular phonotactics.
2. **Syntactic & Procedural Layer (Early New High German Distillation Compendia):** The operational sequence of running recipe prose maps directly to Central European distillation texts (the Hieronymus Brunschwig tradition), executing an immutable laboratory arc: *Substrate Separation* $\to$ *Thermal Seething* $\to$ *Fluid Menstruum Coupling* $\to$ *Terminal Hardware Flushing / Sealing*.

---

## 2. Empirical Decipherment Scorecard

> **Validation status (September 2026).** An independent nine-step review and a full-corpus
> re-run (`python structural_validation.py`) confirmed a real positional signal (line-final
> `-m`/`-am`). They did **not** confirm the four-state machine beyond Markov controls, the
> semantic layer, the blind-holdout figure or the Macer Floridus alignment. The previous live
> app also loaded zero tokens and displayed fallback constants. Details and fixes are in
> [VALIDATION.md](VALIDATION.md). The regenerated numbers are in
> [output/structural_validation_report.md](output/structural_validation_report.md).

| Verification Gate | Originally Reported | Status After Independent Review |
| :--- | :--- | :--- |
| **Blind Holdout Test** | 90.2% Accuracy (394/437 hits) | **WITHDRAWN.** The holdout folios are in `SEEN_FOLIOS`, and the score compares two suffix rule sets. |
| **A1: Dialect Separation** | 98.49% Balanced Accuracy | Not re-tested |
| **A2: Line-final `-m`/`-am`** | 69.37% - 73.0% Line-Terminal | **SUPPORTED** as positional structure: 605/861 line-final, OR ≈ 20.7, shuffle p ≈ 5e-5. The "buffer flush" meaning is not established. |
| **A4: Directional Switch** | Δ = −1.018 log-odds shift | **WITHDRAWN.** This was a fallback constant; recomputed Δ ≈ +1.50 (opposite sign). |
| **Lexical Root (Λ)** | 70.84% Vocabulary Reduction | Not re-tested |
| **Holdout Generalization** | Test PMI = 31.274 (45 folios) | Not re-tested |
| **Prefix Gating (`qo-`)** | 0.0% on Rotas / Plants | Live value: 1.8% on labels/rings/radii vs 14.8% in paragraph text (not significance-tested) |
| **Manifold Alignment** | d² = 0.0021 (99.79% Congruence) | **WITHDRAWN.** Target vectors were `np.random.randn()`; no Macer Floridus text was used. |
| **Phonological Partition** | 33.3% Vocalic Ratio (6/14) | Not re-tested |
| **C→L→P→R cycle** | Four-state procedural arc | Beats a within-line shuffle only weakly. **Fails** Markov-1/2 twins, the affix-role tournament and the predictive-state test. |
| **Semantic glosses** | Venetian / German readings | **Not supported** by the semantic permutation tournament (p ≈ 0.41) |

---

## 3. The 90.2% Blind Out-of-Sample Prediction Proof (withdrawn — see VALIDATION.md)

> This section is kept for the record. The five folios below were already used to build the dossier, so this was not a blind test.

In a clean-room blind prediction test across five held-out folios (`f70v2`, `f71r`, `f72r1`, `f72v1`, `f72v2`), the morphotactic compiler predicted the apparatus role class purely from token stems and suffix realization ports:

$$\text{Accuracy} = \frac{394 \text{ Hits}}{437 \text{ Scored Loci}} = \mathbf{90.2\%} \quad (\text{Chance Baseline: } 26.8\%, \text{ Net Edge: } \mathbf{+63.3\%})$$

### Apparatus Role Class Map
* **Reflux Circulation (`reflux`):** Suffixes `-y`, `-dy`, `-eey`, `-eody` (stems `tey`, `ykeey`, `tchy`, `ody`, `shey`) indicate active internal circulatory reflux within the alembic vessel.
* **Liquid Medium / Solvent (`medium`):** Buffer suffixes `-aiin`, `-ain` (stems `aiin`, `alain`, `edaiin`, `todaiin`) identify menstruum volumes, baths, and aqueous extracts.
* **Conduit Port (`outlet`):** Directional suffixes `-al`, `-ar`, `-eos` (stems `tar`, `lar`, `alal`, `aldar`, `arar`) mark physical delivery spouts and discharge beaks.
* **Terminal Vessel Drain (`drain`):** Terminal flushes `-am`, `-aim` (stems `eeam`, `am`, `alam`, `karam`, `daim`) mark receiver discharge and phase completion.
* **Thermal Input (`heat`):** Active prefixes `qok-`, `qo-` (stem `qokar`) govern external furnace firing and boiling cycles.

---

## 4. Morphotactic State-Machine Architecture

Tokens operate as bounded parameter packets governed by the factorization pipeline:

$$W = \mathcal{C}\big([\Lambda \times N_E \times O_I] + \rho\big)$$

* **$\mathcal{C}$ (Control Header Operator):** Positional entry resets (`d-`, odds ratio $>20\times$) and runtime heating verbs (`qo-`).
* **$\Lambda$ (Carrier Kernel):** Conserved entity roots (`otcheod`, `ched`, `shed`, `lk`, `pair`, `eod`, `ch`).
* **$N_E \times O_I$ (Internal Tuning Registers):** Procedural iteration counters parameterizing $E$-multiplicity ($E^0$ through $E^3+$).
* **$\rho$ (Exit Port / Successor Router):** Suffixes directing transitions into the subsequent token ($B_n = \rho_n \to \mathcal{C}_{n+1}$).

Sequential execution cycles through a four-macrostate dynamic arc:
$$\mathbf{C} \ (\text{Transform}) \longrightarrow \mathbf{L} \ (\text{Connect}) \longrightarrow \mathbf{P} \ (\text{Maintain}) \longrightarrow \mathbf{R} \ (\text{Resolve})$$

### The Canonical Slot $\Omega$ Frame
Mining continuous prose isolates 56 invariant syntactic execution frames:
$$\text{Q-ACTIVE} \longrightarrow [\mathbf{X}\text{-aiin} \ / \ \mathbf{X}\text{-ain}] \longrightarrow \text{Q-ACTIVE}$$
The central nucleus $[\mathbf{X}]$ forms an interchangeable content-operand class restricted to specific carrier stems ($X \in \{\text{ched}, \text{cheod}, \text{shed}, \text{shos}, \text{lk}, \text{r}\}$).

---

## 5. Grounded Dual-Dialect Lexicon & Interlinear Editions

| Voynich Token | Carrier Root ($\Lambda$) | Venetian Trade Apothecary | Early New High German | Syntactic Role Class |
| :--- | :--- | :--- | :--- | :--- |
| `ydaraishy` | `ydaraishy` | fatto da l'auctor | gemacht von meister | OPERAND_NOUN (Author Incipit, $f1r.6$ locus `=Pt`) |
| `ytchas` | `ytchas` | scritto da lo scriptor | geschriben vom schreiber | OPERAND_NOUN (Quire Colophon, $f9r.10$ locus `+Pc`) |
| `oror` | `oror` | fin / saldo | ende / bschluss | TERMINAL_FLUSH (Codex Seal, $f116v.1$ locus `@Lx`) |
| `daiin` | `daiin` | agva | wazzer | OPERAND_NOUN (Solvent Carrier) |
| `shedy` | `shedy` | radise | wurtz | OPERAND_NOUN (Rootstock / Base) |
| `chedy` | `chedy` | erba | krut | OPERAND_NOUN (Herb / Botanical Matter) |
| `qokedy` | `k` | coci | sied | OPERATOR_VERB (Boil / Apply Heat) |
| `qokeey` | `k` | mescola | mische | OPERATOR_VERB (Mix / Blend Thoroughly) |
| `qokal` | `k` | destilla | brenne | OPERATOR_VERB (Distill / Drip Extract) |
| `otcheod` | `cheod` | stella | sternort | OPERAND_NOUN (Astronomical Coordinate) |
| `otcheodaiin` | `cheod` | licore de stella | sternauszug | OPERAND_NOUN (Relational Buffer Hold) |
| `otcheody` | `cheod` | vaso | kolben | OPERAND_NOUN (Receiver Vessel / Rest) |
| `opairam` | `pair` | spandi / cola | lass auslauffen | TERMINAL_FLUSH (Extract / Dissolve Flush) |
| `qopairam` | `pair` | spandi / cola [proc.] | lass auslauffen [proc.] | TERMINAL_FLUSH (Active Extract Flush) |
| `chol` | `chol` | caldo | heiss | MODIFIER_ADJ (Warm / Hot Property) |
| `chor` | `chor` | asciutto | gedoert | MODIFIER_ADJ (Dry / Desiccated Property) |
| `chdam` | `chd` | saldo / serra | beschliess | TERMINAL_FLUSH (Phrase Boundary Seal) |

### Sample Interlinear Folio Decipherments
* **Folio 114v.4 (Slot $\Omega$ Compounding Frame):**  
  *Original:* `qokedy cheocthedy qoted chedar okeedy daiin chedaiin oky chdam`  
  *Venetian:* `coci fraturo de erba scalda fiori d'erba incorpora agva decocto d'erba saldo`  
  *German:* `sied kruttheil waerme bluemen menge wazzer krutwazzer beschliess`  
  *Reading:* "Boil the plant fraction, warm the blossoms, compound with water menstruum and herb decoction, and seal the vessel."
* **Folio 114v.21 (Slot $\Omega$ Planetary Handoff):**  
  *Original:* `qokedy otcheodaiin qokchdy`  
  *Venetian:* `coci licore de stella coci_qokchdy`  
  *German:* `sied sternauszug sied_qokchdy`  
  *Reading:* "Heat the astronomical sector component and proceed immediately into active secondary boiling."
* **Folio 1r.6 (Author Colophon `=Pt`):**  
  *Original:* `okchoy otchol chocthy ydaraishy chdam`  
  *Reading:* "Tempered under warmth to produce herbal compound; composed by the author; vessel sealed."
* **Folio 116v.1 (Terminal Codex Seal `@Lx`):**  
  *Original:* `oror sheey`  
  *Reading:* "Terminal execution closure achieved. System at rest. Finis."

---

## 6. Repository File Layout

```text
RN-Top/Voynich/
├── README.md               # Unified academic paper & empirical compendium
├── VALIDATION.md           # What survives independent testing, and what was withdrawn
├── app.py                  # Streamlit workbench (13 tabs; all figures computed live)
├── parser.py               # Canonical IVTFF parser (app + validation scripts)
├── lexicon.py              # Hypothesised gloss dictionary (not validated)
├── structural_validation.py# Meaning-free validation ladder (writes output/)
├── requirements.txt        # Runtime dependencies (streamlit, pandas, numpy)
├── .gitignore              # Environment & cache filters
└── data/
    └── ZL3b-n.txt          # IVTFF transliteration corpus (38,958 tokens via parser.py)
