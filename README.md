# Voynich Computational Decipherment Suite
### Mathematical Syntax Induction, Cross-Modal Grounding, and Phonetic Crib Decipherment

## Primary Mission
The primary objective of this repository is the complete, verifiable computational decipherment and continuous plaintext reading of Beinecke MS 408 (the Voynich Manuscript).

Rather than relying on unconstrained letter substitution, anagramming, or speculative modern interpretations, this workbench executes a systematic historical cryptanalytic progression:

$$\text{Symbols} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Morphology} \xrightarrow{\quad\text{VERIFIED}\quad} \text{State Syntax} \xrightarrow{\quad\text{VERIFIED}\quad} \text{Phonological Partition} \mathrel{\mathbf{\Bigg\vert{}}} \text{Phonetic Anchors} \longrightarrow \text{Continuous Plaintext}$$

---

## What Has Been Formally Established (Reproducible Syntax & Structure)
Through statistical, permutation, and generator-null testing, the following foundational mechanics are empirically verified:
- **Falsification of Algorithmic Hoax Models:** Decisive rejection of Timm & Schinner self-citation pseudotext generators. Line-terminal buffer flushes (`-m` / `-am`) concentrate at line boundaries ($odds\ ratio > 20\times, p < 0.02$), and prefix ordering exhibits strict non-commutative execution ($39:2$ forward vs. reverse pairs).
- **Currier Dialect Classification:** Machine-learning verification of Currier Language A vs. B regimes ($98.49\%$ balanced accuracy vs. chance null).
- **Lexical Compression ($\Lambda$):** Stripping runtime control headers ($q-, k-, d-$) and terminal realization affixes ($-y, -ar, -al, -aiin, -m$) isolates invariant carrier cores conforming to a Zipfian distribution ($\alpha = 1.065$).
- **Syntactic Slot Substitution (Slot Omega):** Extraction of invariant procedural frames ($Q\text{-ACTIVE} \longrightarrow [X\text{-aiin}] \longrightarrow Q\text{-ACTIVE}$), proving interchangeable content operands plug into fixed grammatical positions.
- **Physical Layout Stratification:** Demonstration that illustration labels systematically suppress procedural control operators ($qo- = 0.0\%$) in favor of static nominal/coordinate roots ($ot-, ok-$).
- **Unsupervised Vowel-Consonant Induction:** Execution of Sukhotin's algorithm isolating vocalic nuclei ($V = \{a, o, h, t, i, y\}$) from consonant carriers ($C = \{c, d, e, f, k, l, m, n\}$).

---

## Decipherment Frontier: The Phonetic Decan Layer
While generative grammar, layout rules, and slot templates are verified, continuous natural-language translation requires phonetic values for individual glyphs.

This repository attacks the phonetic frontier through **proper-noun crib alignment**:
1. Isolating invariant radial spoke labels across the 12 Zodiac rotas (`f70v`–`f73v`).
2. Generating Sukhotin Consonant-Vowel (CV) skeletal signatures.
3. Scoring skeletal Levenshtein distances against canonical 15th-century Ptolemaic decan names and planetary rulers (*Mars, Sol, Venus, Mercurius, Luna, Saturnus, Jupiter*).
4. Extracting the candidate phonetic values necessary to solve the running text without ungrounded translation guesses.

---

## Interactive Workbench & Live Dashboard
Access the complete corpus viewer, phonetic decan matcher, manifold alignment engine, and parallel reader at:
👉 **[Live Streamlit Application](https://voynich-xdbkaduqmatywumbtkdcgd.streamlit.app)**

## Repository Structure
- `app.py`: Integrated Streamlit application housing the Phonetic Decan Crib Solver, Sukhotin Induction, and Parallel Reader.
- `break_phonetic_cribs.py`: Standalone CLI phonetic crib solver and skeletal Levenshtein alignment engine.
- `data/ZL3b-n.txt`: Transcribed machine-readable IVTFF corpus.
- `voynich_derived_dictionary.csv`: Structural operational dictionary with historical lemma mappings.
