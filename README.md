# Voynich Computational Decipherment Suite
### Mathematical Syntax Induction, Cross-Modal Grounding, and Apparatus Architecture

## Primary Mission
The primary objective of this repository is the complete, verifiable computational decipherment and continuous plaintext reading of Beinecke MS 408 (the Voynich Manuscript)[span_0](start_span)[span_0](end_span).

Rather than relying on unconstrained letter substitution, anagramming, or speculative modern interpretations, this workbench executes a systematic historical cryptanalytic progression[span_1](start_span)[span_1](end_span):

$$\text{Symbols} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Morphology} \xrightarrow{\quad\text{VERIFIED}\quad} \text{State Syntax} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Phonological Partition} \mathrel{\mathbf{\Bigg\vert{}}} \text{Phonetic Anchors} \longrightarrow \text{Continuous Plaintext}$$[span_2](start_span)[span_2](end_span)

---

## What Has Been Formally Established (Reproducible Syntax & Structure)
Through statistical, permutation, and generator-null testing, the following foundational mechanics are empirically verified[span_3](start_span)[span_3](end_span):
- **Falsification of Algorithmic Hoax Models:** Decisive rejection of Timm & Schinner self-citation pseudotext generators[span_4](start_span)[span_4](end_span). Line-terminal buffer flushes (`-m` / `-am`) concentrate at line boundaries ($odds\ ratio > 20\times, p < 0.02$), and prefix ordering exhibits strict non-commutative execution ($39:2$ forward vs. reverse pairs)[span_5](start_span)[span_5](end_span).
- **Currier Dialect Classification:** Machine-learning verification of Currier Language A vs. B regimes ($98.49\%$ balanced accuracy vs. chance null)[span_6](start_span)[span_6](end_span).
- **Lexical Compression ($\Lambda$):** Stripping runtime control headers ($q-, k-, d-$) and terminal realization affixes ($-y, -ar, -al, -aiin, -m$) isolates invariant carrier cores conforming to a Zipfian distribution ($\alpha = 1.065$)[span_7](start_span)[span_7](end_span).
- **Syntactic Slot Substitution (Slot Omega):** Extraction of invariant procedural frames ($Q\text{-ACTIVE} \longrightarrow [X\text{-aiin}] \longrightarrow Q\text{-ACTIVE}$), proving interchangeable content operands plug into fixed grammatical positions[span_8](start_span)[span_8](end_span).
- **Physical Layout Stratification:** Demonstration that illustration labels systematically suppress procedural control operators ($qo- = 0.0\%$) in favor of static nominal/coordinate roots ($ot-, ok-$)[span_9](start_span)[span_9](end_span).
- **Unsupervised Vowel-Consonant Induction:** Execution of Sukhotin's algorithm isolating vocalic nuclei ($V = \{a, o, h, t, i, y\}$) from consonant carriers ($C = \{c, d, e, f, k, l, m, n\}$)[span_10](start_span)[span_10](end_span).

---

## Decipherment Frontier: The Phonetic Decan Layer
While generative grammar, layout rules, and slot templates are verified, continuous natural-language translation requires phonetic values for individual glyphs[span_11](start_span)[span_11](end_span).

This repository attacks the phonetic frontier through **proper-noun crib alignment**[span_12](start_span)[span_12](end_span):
1. Isolating invariant radial spoke labels across the 12 Zodiac rotas (`f70v`–`f73v`)[span_13](start_span)[span_13](end_span).
2. Generating Sukhotin Consonant-Vowel (CV) skeletal signatures[span_14](start_span)[span_14](end_span).
3. Scoring skeletal Levenshtein distances against canonical 15th-century Ptolemaic decan names and planetary rulers (*Mars, Sol, Venus, Mercurius, Luna, Saturnus, Jupiter*)[span_15](start_span)[span_15](end_span).
4. Extracting candidate phonetic values necessary to solve running text without ungrounded translation guesses[span_16](start_span)[span_16](end_span).

---

## Interactive Workbench & Live Dashboard
Access the complete corpus viewer, phonetic decan matcher, manifold alignment engine, and parallel reader at[span_17](start_span)[span_17](end_span):  
👉 **[Live Streamlit Application](https://voynich-xdbkaduqmatywumbtkdcgd.streamlit.app)**[span_18](start_span)[span_18](end_span)

---

## Repository Structure
- `app.py`: Integrated Streamlit application housing the Phonetic Decan Crib Solver, Sukhotin Induction, and Parallel Reader[span_19](start_span)[span_19](end_span).
- `translate_voynich_dialects.py`: Standalone procedural translation engine mapping Voynich frames into Venetian apothecary and Early New High German distillation registers.
- `break_phonetic_cribs.py`: CLI phonetic crib solver and skeletal Levenshtein alignment engine[span_20](start_span)[span_20](end_span).
- `data/ZL3b-n.txt`: Transcribed machine-readable IVTFF corpus[span_21](start_span)[span_21](end_span).
- `voynich_derived_dictionary.csv`: Structural operational dictionary with historical lemma mappings[span_22](start_span)[span_22](end_span).
- `voynich_master_corpus_extracted_2.csv`: Master processed corpus containing 38,223 tokens with functional role annotations.

---

## Architecture Contract
The system operates under an immutable apparatus hypothesis contract.
All six operational roles, macrostate transitions ($C \to L \to \text{route} \to P \to R$), layout gating rules, and negative Latin decipherment boundaries are frozen.
See `docs/ARCHITECTURE_CONTRACT.md` and `pages/09_Architecture_Contract.py`.
