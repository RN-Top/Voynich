"""
STREAMLIT PAGE: LANGUAGE STRUCTURE
Does the text behave like a language? Word order, set phrases, grammar links and where
topic sits in a word. Everything is recomputed from the transcription on load.
"""

import importlib
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "analyses"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import numpy as np  # noqa: E402
import parser as canonical  # noqa: E402
import phrases_test as pt  # noqa: E402
import writing_types_test as wt  # noqa: E402

for _module in (canonical, wt, pt):
    importlib.reload(_module)

# Fewer shuffles than the pre-registered runs so the page loads quickly; the full runs are in output/.
APP_SHUFFLES = 200
wt.N_W1, wt.N_W2, pt.N_PERMS = APP_SHUFFLES, APP_SHUFFLES, APP_SHUFFLES
SEED = 20261002

st.set_page_config(page_title="Language Structure", page_icon="🔤", layout="wide")
st.title("🔤 Language Structure")
st.markdown("""
Does the Voynich text behave like a language? These tests don't translate anything. They ask whether word
order, word pairs and word parts carry structure that shuffled text does not. Each test's rules were written
down before it was first run (see the pre-registrations in `analyses/`).
""")


@st.cache_data(show_spinner="Computing from the transcription…")
def compute():
    df = canonical.parse_zl3b(canonical.ensure_full_corpus(canonical.CORPUS_PATH))
    df = df[df["clean"].str.len() > 0]
    rng = np.random.default_rng(SEED)
    types = wt.types(df)
    para = df[df.locus_type == "P"]
    profiles = []
    for name, g in types.items():
        other = para[para.currier != g["currier"].iloc[0]] if name.startswith("Paragraph") else para
        profiles.append(wt.profile(name, g, set(other["clean"])))
    order = {name: wt.w1(g, rng) for name, g in types.items()}
    topic = wt.w2(para, rng)
    phrases = [pt.analyse(para[para.currier == c], rng, f"Currier {c}") for c in ("A", "B")]
    return profiles, order, topic, phrases


profiles, order, topic, phrases = compute()
fmt_p = lambda p: f"{p:.3f}" if p >= 0.001 else "< 0.001"
floor = 1 / (APP_SHUFFLES + 1)

st.markdown("### 1. The kinds of writing")
st.dataframe(pd.DataFrame(profiles).rename(columns={
    "type": "Type", "words": "Words", "distinct": "Distinct", "mean_len": "Mean length",
    "top_beginnings": "Common beginnings", "top_endings": "Common endings",
    "in_other_paragraph_text": "Also in other paragraph text"}), width="stretch", hide_index=True)

st.markdown("### 2. Does word order matter?")
st.caption("Neighbouring words on the same line, leaving out the first and last word of each line (known "
           "line-layout habits). Compared with the same words shuffled within their lines.")
rows = []
for name, r in order.items():
    if r is None:
        rows.append({"Type": name, "Result": "too little text"})
    else:
        rows.append({"Type": name, "Pairs": r["pairs"], "Real text (bits)": round(r["mi"], 3),
                     "Shuffled (bits)": round(r["null_mean"], 3), "Extra": round(r["excess"], 3),
                     "p": fmt_p(r["p"]), "Result": "order matters" if r["p"] < 0.01 else "no clear effect"})
st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

st.markdown("### 3. Set phrases")
st.caption("Word pairs seen 5+ times and at least 3× more often than their words' frequencies predict.")
c1, c2 = st.columns(2)
for col, r in zip((c1, c2), phrases):
    x = r["r1"]
    col.metric(f"{r['name']}: set phrases", x["obs"], f"{x['obs'] - x['null_mean']:+.1f} vs shuffled")
    col.dataframe(pd.DataFrame(r["top"], columns=["Phrase", "Count", "Times expected", "Main sections"])
                  .assign(**{"Times expected": lambda d: d["Times expected"].round(1)}),
                  width="stretch", hide_index=True)

st.markdown("### 4. Grammar links: which parts of neighbouring words go together?")
st.caption("Beginning = first 2 letters, ending = last 2 letters. 'Extra' is how much more the real text shows "
           "than shuffled text. The strongest link is a word's ending predicting how the next word starts.")
rows = []
for r in phrases:
    for k, x in sorted(r["r2"].items(), key=lambda kv: -kv[1]["excess"]):
        a, b = k.split("->")
        rows.append({"Text": r["name"], "Link": f"{a} of word 1 → {b} of word 2",
                     "Extra (bits)": round(x["excess"], 4), "p": fmt_p(x["p"])})
st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

st.markdown("### 5. Which part of a word follows the topic?")
st.caption("How much a word's beginning or ending tells you about the page's section (plants, baths, stars…), "
           "compared with section labels shuffled between pages of the same Currier language.")
st.dataframe(pd.DataFrame([{"Word part": k, "Extra (bits)": round(v["excess"], 4), "p": fmt_p(v["p"])}
                           for k, v in topic.items()]), width="stretch", hide_index=True)

st.info(f"This page uses {APP_SHUFFLES} shuffles so it loads quickly, so the smallest p it can show is about "
        f"{floor:.3f}. The pre-registered full runs, with 1,000–2,000 shuffles, are in "
        "`output/writing_types_report.md` and `output/phrases_report.md`. "
        "These results describe the text's structure. They do not decode it.")
