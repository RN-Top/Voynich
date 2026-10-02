"""
STREAMLIT PAGE: ANOMALY SCAN
Which pages behave least like their peers (same section, same Currier language)?
"""

import importlib
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "analyses"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import parser as canonical  # noqa: E402
import structural_validation as sv  # noqa: E402
import anomaly_scan as scan_mod  # noqa: E402

for _module in (canonical, sv, scan_mod):
    importlib.reload(_module)

st.set_page_config(page_title="Anomaly Scan", page_icon="🔎", layout="wide")
st.title("🔎 Anomaly Scan")
st.markdown("""
Each page is measured on a few text features and compared with pages from the **same section and the same
Currier language**, so ordinary section differences don't count. A high score means the page behaves
unusually for its peers. This is a list of **candidates to look at**, not proof of anything.

Check that it works: the transcription's notes call **f57v** and **f49v** "key-like", and the scan finds
both on its own. **f1r**'s key is a Roman alphabet in the margin, which is not part of the transcribed
Voynich text, so the scan cannot see it.
""")


@st.cache_data(show_spinner=False)
def run():
    df = canonical.parse_zl3b(canonical.ensure_full_corpus(canonical.CORPUS_PATH))
    return scan_mod.scan(df), scan_mod.key_sequences()


res, keys = run()
top_n = st.slider("Pages to show", 10, len(res), 25)
st.dataframe(res.head(top_n), width="stretch")
st.caption("Main reason = the feature on which the page is most unusual. Score = robust z-score (how many "
           "typical spreads away from its peers). f57v is filed under Herbal by page number, though it is a "
           "circular diagram, which inflates its score; its one-letter-word rate is extreme either way.")

st.markdown("### Key-like sequences recorded in the transcription")
for name, k in keys.items():
    st.markdown(f"**{name.replace('_', ' ')}**: `{k['sequence']}`")
    st.markdown(f"- Common running-text letters missing from it: {', '.join(k['running_text_top10_missing_from_sequence'])}")
st.info("Neither sequence contains the most common letters of the running text, so neither looks like a "
        "complete alphabet for the main script.")

st.download_button("Download anomaly_scan.csv", res.to_csv(index=False).encode("utf-8"),
                   file_name="anomaly_scan.csv", mime="text/csv")
