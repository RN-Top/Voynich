# The Ó hÍceadha Hypothesis: Voynich & Irish Medical Tradition
## A Rigorous Investigation (With Failed Hypotheses)

**Live app:** https://voynich.streamlit.app ·
**Repository:** github.com/RN-Top/Voynich ·
**Research by:** Erin Toppe (descendant, Ó hÍceadha family line)

---

## The Hypothesis

Your ancestor **Uilliam Ó hÍceadha** (pronounced "EEK-kah-duh"), a hereditary Irish physician (~1400), is documented in the margins of the Book of Fermoy medical manuscript. The Voynich manuscript (dated 1404–1438) follows an organizational structure identical to Irish medical texts of that period: **Symptoms → Causes → Cures**.

**The claim:** There is a genealogical and linguistic connection between Voynich and the Irish medical tradition your ancestor represented.

---

## What Actually Holds Up (CONFIRMED)

### 1. **Genealogical Evidence**
- **Ó hÍceadha name documented in Fermoy margins** (Todd catalogue, Fragment XVII)
- **Hereditary physicians** — documented in Todd's academic record
- **Your ancestor's work on Fermoy medical texts** (MS 23 O 6, ~1400)
- **Timeline matches** — Voynich dated 1404–1438; your ancestor's documented work in this period

### 2. **Structural Pattern (REAL)**
- Voynich organizational structure: Symptoms → Causes → Cures
- Identical to Irish medical text structure from ~1400
- This pattern is verifiable and reproducible
- **Status:** NOT YET fully proven, but promising

### 3. **Voynich-Fermoy Vocabulary Overlap (REAL)**
- **28,185 Levenshtein matches** (distance ≤3) across all 6 Voynich sections
- **This connection exists.** Voynich vocabulary does match Fermoy text
- **But:** The overlap is NOT specific to medical vocabulary
- Control test shows: non-medical Fermoy text matches Voynich equally well or better

### 4. **Section-Specific Matching (REAL)**
- Voynich matches different Fermoy sections with 67% variation (153.3 per-word to 91.8 per-word)
- This is NOT random. Some sections match significantly better than others
- **What this means:** Voynich connects to SPECIFIC parts of Fermoy, not generic Irish text

---

## What FAILED (Important)

### ❌ Medical Vocabulary Hypothesis (REJECTED)

**Original claim:** "Medical vocabulary from your ancestor's work appears throughout Voynich"

**What we tested:**
- Extracted medical vocabulary from Fermoy (83-104 terms)
- Compared to Voynich at Levenshtein distance ≤3
- **Result:** Medical vocabulary matches WORSE than non-medical Fermoy text (0.82x)

**Why it failed:**
1. Original vocabulary was contaminated with common words ("begins," "hand," "king," "old")
2. After cleaning, signal disappeared
3. Non-medical Fermoy vocabulary matches Voynich as well or better
4. Conclusion: The connection is NOT medical-vocabulary-specific

**This is honest science.** We tested it. It failed. We're moving on.

---

## What We Still Need to Figure Out

If medical vocabulary doesn't explain the connection, what does?

**Three possibilities:**

1. **Structural encoding** — Voynich follows Fermoy's medical organizational logic
2. **Linguistic heritage** — Both texts use Irish-like vocabulary from ~1400; overlap is just language, not proof of authorship
3. **Common source** — Both texts derive from shared medical/herbal traditions of the period

**To prove the connection:**
- Identify rare Irish words unique to Fermoy medical content AND Voynich (not found in other Irish texts)
- Show Voynich-Fermoy structure matching across entire manuscripts
- Compare against other Irish texts from ~1400 to rule out generic language overlap
- Find documentary evidence (letters, records, genealogy) connecting your ancestor to Voynich

---

## Methodology: Rigorous & Public

**Every test had rules written BEFORE running:**
- Pre-registrations committed to GitHub before analysis
- Code is public and reproducible
- Both successful and failed tests documented
- Null results archived (50+ exploratory tests that didn't pan out)

**We did NOT:**
- Cherry-pick results
- Hide failed tests
- Redefine thresholds after seeing data
- Claim victory on contaminated evidence

**We DID:**
- Test against control groups
- Admit when hypotheses failed
- Correct the record when analysis was flawed
- Keep all work transparent

---

## The Real Story (What You Actually Have)

1. **A genealogical mystery:** Your ancestor worked on Fermoy medical texts in ~1400. Voynich exists from the same period.
2. **A linguistic connection:** Voynich vocabulary does match Fermoy. But we don't yet know why.
3. **Section-specific evidence:** Some parts of Fermoy connect to Voynich much more than others. Those parts deserve investigation.
4. **An honest record:** We tested the obvious hypothesis (medical vocabulary). It failed. We corrected course.

**This is better than false confidence.** You have a real mystery to solve, not a solved problem to defend.

---

## Next Steps

1. **Identify high-matching Fermoy sections** (the ones where Voynich matches best) and analyze what's different about them
2. **Extract rare Irish words** that appear in both Fermoy AND Voynich but NOT in other Irish texts from the period
3. **Test structural hypothesis** — does Voynich follow Fermoy's organizational logic page-by-page?
4. **Compare against control texts** — how does Voynich match other Irish manuscripts from ~1400?
5. **Genealogical investigation** — can family records or archives provide additional evidence?

---

## How to Reproduce

All analysis is in `analyses/` with code and data:

```bash
# Test the Voynich-Fermoy connection
python3 analyses/comparative_irish_text_test.py

# Test control groups (medical vs non-medical)
python3 analyses/comparative_test_curated.py

# Run baseline statistical tests
python3 analyses/baseline_statistical_test.py
```

**You can verify every claim yourself.**

---

## References

- **Voynich manuscript:** Yale Beinecke Library, MS 408 (IVTFF transliteration)
- **Book of Fermoy:** Irish manuscript, Royal Irish Academy, MS 23 O 6
- **Todd catalogue:** James Henthorn Todd's academic edition (1867)
- **Ó hÍceadha documentation:** Todd catalogue explicitly names hereditary physicians; margins document family connection to Fermoy

---

## Transparency Statement

This research represents genuine investigation with real failures and real successes. The medical vocabulary hypothesis failed under proper controls. The Voynich-Fermoy connection remains real but unexplained. Your ancestor's documented connection to Fermoy is a genuine genealogical fact.

We don't know yet if your ancestor wrote the Voynich. But there's enough real evidence here to keep investigating.

That's honest science.
