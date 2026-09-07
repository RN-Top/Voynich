# Voynich Computational Research Workbench

A reproducible Python and Streamlit research environment for exploring structural patterns in the Voynich Manuscript transcription.

This project analyzes token morphology, positional behavior, state transitions, section specificity, astronomical-domain associations, and possible colophon or marginalia evidence.

> **Research status:** This project does not claim that the Voynich Manuscript has been deciphered. Statistical measurements are kept separate from exploratory semantic hypotheses.

---

## What This Project Does

The workbench provides:

- IVTFF / ZL-style Voynich corpus ingestion
- Automatic recovery of the default transcription if the local corpus is missing or truncated
- Token cleaning and morphological decomposition
- Control-prefix analysis
- Carrier-core extraction
- Exit-port classification
- Macrostate classification
- Previous/next-token structural context
- Folio and manuscript-section classification
- Carrier × section PMI analysis
- State-transition analysis
- Exit-port → successor-control routing
- Astronomical-domain carrier analysis
- Author / colophon / marginalia auditing
- Exploratory lexical hypotheses with explicit evidence and confidence labels
- Interactive Streamlit interface
- CSV export of parsed corpus data and lexical hypotheses

---

## Research Architecture

```text
data/ZL3b-n.txt
      |
      v
  parser.py
      |
      +--> analyzer.py
      |      Structural and transition evidence
      |
      +--> decoder.py
      |      Astronomical-domain comparisons
      |
      +--> author_audit.py
      |      Colophon and marginalia audit
      |
      +--> engine_decipher.py
      |      Exploratory lexical hypotheses
      |
      v
    app.py
      |
      v
 Streamlit Workbench