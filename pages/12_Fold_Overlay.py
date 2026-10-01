"""
STREAMLIT PAGE: FOLD OVERLAY
Fold one page onto another and see which words land on each other, then
compare with every other page folded onto the same target.
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

import parser as canonical  # noqa: E402
import structural_validation as sv  # noqa: E402
import fold_overlay as fo  # noqa: E402

for _module in (canonical, sv, fo):
    importlib.reload(_module)

st.set_page_config(page_title="Fold Overlay", page_icon="📄", layout="wide")
st.title("📄 Fold Overlay")
st.markdown("""
Fold one page onto another and see which words land on each other. If folding reveals a key,
the words that land together should match much better than when **any other page** is folded onto
the same target in the same way.

**Approximation:** the transcription has line numbers and word order, not exact positions. A word's
position is the middle of its letters as a fraction of the line length, and line *k* lands on line *k*.
With **Mirror** on, the folded page is flipped left-to-right, as a real fold would do.
""")


@st.cache_data(show_spinner=False)
def load_pages():
    return fo.page_lines(canonical.parse_zl3b(canonical.ensure_full_corpus(canonical.CORPUS_PATH)))


pages = load_pages()
names = sorted(pages, key=lambda f: (int("".join(c for c in f[1:] if c.isdigit())[:3] or 0), f))
c1, c2, c3 = st.columns(3)
folded = c1.selectbox("Page you fold over", names, index=names.index("f1r") if "f1r" in names else 0)
target = c2.selectbox("Page it lands on", names, index=names.index("f58r") if "f58r" in names else 1)
mirror = c3.checkbox("Mirror (real fold)", value=True)

if folded == target:
    st.info("Pick two different pages.")
    st.stop()

landed = fo.overlay(pages[folded], pages[target], mirror)
with st.spinner("Folding every other page onto the same target for comparison..."):
    res = fo.rank_against_all(pages, folded, target, mirror)
obs = res["observed"]

m1, m2, m3 = st.columns(3)
m1.metric("Word pairs that land together", f"{obs['pairs']:,}")
m2.metric("Same word", f"{obs['same_word']:.1%}",
          f"typical page {res['same_word_typical']:.1%}", delta_color="off")
m3.metric("Same ending", f"{obs['same_ending']:.1%}",
          f"typical page {res['same_ending_typical']:.1%}", delta_color="off")

p_word = res["same_word_share_of_pages_scoring_at_least_as_high"]
p_end = res["same_ending_share_of_pages_scoring_at_least_as_high"]
best = min(p_word, p_end)
msg = (f"Compared with {res['n_other_pages']} other pages folded onto {target}: "
       f"{p_word:.0%} score at least as high on same word, {p_end:.0%} on same ending.")
if best < 0.01:
    st.success(msg + " This pair stands out. Before trusting it, remember how many pairs you tried: "
                     "write the pair down and test it again on a fresh question.")
else:
    st.info(msg + " This pair does not stand out from ordinary pages.")

with st.expander(f"All {len(landed)} word pairs that land together"):
    st.dataframe(pd.DataFrame(landed), use_container_width=True)

st.caption("Trying many pairs and keeping the best one will eventually 'find' something by chance. "
           "A real key should stand out on the first pair you predicted, before looking.")
