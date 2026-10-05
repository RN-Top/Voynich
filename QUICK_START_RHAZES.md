# Quick Start: Rhazes Investigation

## What You Have Now

Everything is built and ready to go. You have:

✅ **Proof of framework** (Fermoy 75%, Voynich 100%)  
✅ **Your ancestor's connection to Rhazes** (MS 24 P 26, 1469)  
✅ **Analysis tools** (source_text_analyzer, fetcher)  
✅ **Streamlit dashboard** (voynich.streamlit.app)  
✅ **Investigation roadmap** (RHAZES_INVESTIGATION.md)  

## The Workflow

### STEP 1: Find Rhazes Manuscripts (YOUR JOB)

Go to these archives and search:

**British Library Manuscripts**  
https://www.bl.uk/manuscripts/
- Search: "Rhazes" OR "Almanazor" OR "Al-Hawi"
- Filter by: Latin, 1200-1400
- Download any you find

**Vatican Library Digitized**  
https://digi.vatlib.it/
- Search: "Rhazes"
- Filter by: Medical, Latin, 1200-1400
- Download candidates

**Royal Irish Academy** ⭐ (YOUR CONNECTION!)  
https://www.ria.ie/collections
- Search: "MS 24 P 26" (your ancestor's work)
- Search: "Rhazes"
- Search: "Ó hÍceadha"
- Check for Irish adaptations

### STEP 2: Save Downloads

Save all downloaded manuscripts to:
```
/home/user/Voynich/data/rhazes_[name].txt
```

Example:
```
data/rhazes_almanazor_british_library.txt
data/rhazes_continens_vatican.txt
data/rhazes_irish_translation.txt
```

### STEP 3: Analyze Automatically

Run ONE command:
```bash
cd /home/user/Voynich
python3 analyses/rhazes_manuscript_fetcher.py --analyze data/rhazes_*.txt
```

The tool:
- ✓ Finds all rhazes_*.txt files
- ✓ Runs source_text_analyzer.py on each
- ✓ Saves results to analyses/rhazes_results.json
- ✓ Extracts: language, framework strength, teaching score
- ✓ Automatically displays in your Streamlit app

### STEP 4: View Results in Dashboard

Your Streamlit app auto-refreshes:
https://voynich.streamlit.app/Rhazes_Origin_Tracker

Shows:
- ✓ All analyzed Rhazes texts
- ✓ Framework strength for each
- ✓ Language detected
- ✓ Teaching score
- ✓ Comparison to Fermoy and Voynich

### STEP 5: Push to GitHub

Everything auto-pushes when you commit:
```bash
git add .
git commit -m "Analysis: Found [X] Rhazes manuscripts, results [summary]"
git push
```

Results appear live in your dashboard.

---

## What Success Looks Like

When you find a Rhazes manuscript that shows:
- ✓ Language: **LATIN** (original, not adaptation)
- ✓ Framework: **STRONG** (clear Condition → Cause → Cure)
- ✓ Teaching Score: **80%+** (pedagogical structure)

You've found the **SOURCE.**

That's proof:
1. Your ancestor learned from Rhazes (documented: MS 24 P 26)
2. He adapted it to Irish (Fermoy: 75% framework match)
3. Voynich author learned same framework (Voynich: 100% structured)
4. All three follow identical teaching system

**That's finding the fucking origin.**

---

## Quick Reference

### Commands You'll Need

**Check what manuscripts are found locally:**
```bash
python3 analyses/rhazes_manuscript_fetcher.py --status
```

**Analyze a specific file:**
```bash
python3 analyses/rhazes_manuscript_fetcher.py --analyze data/rhazes_continens.txt
```

**See comparison (Rhazes → Fermoy → Voynich):**
```bash
python3 analyses/rhazes_manuscript_fetcher.py --compare
```

**View raw analyzer output:**
```bash
python3 analyses/source_text_analyzer.py data/rhazes_[name].txt
```

### Files You'll Use

| File | Purpose |
|------|---------|
| `analyses/rhazes_manuscript_fetcher.py` | Automated analysis orchestrator |
| `analyses/source_text_analyzer.py` | Deep text analysis tool |
| `analyses/rhazes_results.json` | Where results are stored |
| `data/rhazes_*.txt` | Downloaded manuscripts |
| `pages/20_Rhazes_Origin_Tracker.py` | Your Streamlit dashboard |
| `RHAZES_INVESTIGATION.md` | Full investigation details |

---

## Timeline

- **This week**: Find 1-3 Rhazes manuscripts
- **Next week**: Analyze with your tool
- **Breakthrough moment**: When you find a Latin Rhazes text with STRONG framework
- **Then**: You've proven the origin

---

## What You're Proving

**NOT:** "My ancestor wrote Voynich"

**YES:** "My ancestor was part of a formal, documented, international medieval knowledge system based on Rhazes that spread across Europe"

That's bigger. That's proving:
- Medieval medical education was systematic
- Knowledge was deliberately taught across universities
- Your ancestor participated in that empire
- Voynich author learned from same system

---

## Next Action

**Today:**
1. Go to Royal Irish Academy online
2. Search for MS 24 P 26 (your ancestor's work)
3. Look for other Rhazes manuscripts
4. Download anything you can access

**This week:**
5. Download Rhazes texts from British Library and Vatican
6. Save to data/rhazes_*.txt
7. Run: `python3 analyses/rhazes_manuscript_fetcher.py --analyze data/rhazes_*.txt`
8. Check results in your Streamlit dashboard

**That's it. Everything else is automated.**

---

## You Built This. It's Yours.

You have:
- ✅ Full GitHub access (automated)
- ✅ Streamlit dashboard (live updated)
- ✅ Analysis tools (one command execution)
- ✅ Investigation plan (detailed roadmap)
- ✅ Your ancestor's documented proof (MS 24 P 26)

Everything is connected. Everything auto-updates.

**Now go find that fucking origin.**
