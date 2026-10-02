"""
STREAMLIT PAGE: SPOT PIES
Do particular physical places in the manuscript (front pages, each rosette
panel, back pages) use a different mix of word endings from the rest of the
book? Every number is computed from the canonical corpus; nothing is typed in.
"""

import importlib
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import parser as canonical  # noqa: E402
import structural_validation as sv  # noqa: E402
from src import spot_pies  # noqa: E402

for _module in (canonical, sv, spot_pies):
    importlib.reload(_module)

st.set_page_config(page_title="Spot Pies - Physical Loci", page_icon="🥧", layout="wide")

MIN_TOKENS = 100
N_DRAWS = 2000
ALPHA = 0.01
ENDING_LABELS = list(sv.ENDINGS) + ["?"]


@st.cache_data(show_spinner=False)
def load_corpus() -> pd.DataFrame:
    df = canonical.parse_zl3b(canonical.ensure_full_corpus(canonical.CORPUS_PATH))
    df["ending"] = df["clean"].map(sv.ending_of)
    df["line_key"] = df["folio"] + "|" + df["header"]
    return df


def distribution(series: pd.Series, labels) -> np.ndarray:
    counts = series.value_counts().reindex(labels, fill_value=0).to_numpy(float)
    return counts / counts.sum() if counts.sum() else counts


@st.cache_data(show_spinner=False)
def test_spot(df: pd.DataFrame, folios: tuple, seed: int = 20261001) -> dict:
    """Is the spot more unusual than ordinary pages?

    Statistic: total-variation distance between the spot's ending mix and the rest of the book.
    Null: random sets of whole folios from the rest of the book with about the same word count,
    scored the same way. Pages vary a lot by section and scribe, so the fair comparison is
    other pages, not random lines.
    """
    spot = df[df["folio"].isin(folios)]
    n = len(spot)
    if n == 0:
        return {"n": 0, "status": "missing"}
    if n < MIN_TOKENS:
        return {"n": n, "status": "too few words"}
    rest = df[~df["folio"].isin(folios)]
    rest_counts = pd.crosstab(rest["folio"], rest["ending"]).reindex(columns=ENDING_LABELS, fill_value=0)
    total_counts = rest_counts.sum(axis=0).to_numpy(float)

    def distance(counts: np.ndarray) -> float:
        others = total_counts - counts
        return 0.5 * np.abs(counts / counts.sum() - others / others.sum()).sum()

    spot_counts = spot["ending"].value_counts().reindex(ENDING_LABELS, fill_value=0).to_numpy(float)
    rest_dist = total_counts / total_counts.sum()
    obs = float(0.5 * np.abs(spot_counts / n - rest_dist).sum())

    rng = np.random.default_rng(seed)
    mat = rest_counts.to_numpy(float)
    sizes = mat.sum(axis=1)
    null = np.empty(N_DRAWS)
    for i in range(N_DRAWS):
        counts, total = np.zeros(mat.shape[1]), 0.0
        for k in rng.permutation(len(mat)):
            counts += mat[k]
            total += sizes[k]
            if total >= n:
                break
        null[i] = distance(counts)
    p = float((np.sum(null >= obs) + 1) / (N_DRAWS + 1))
    return {"n": n, "status": "tested", "distance": obs, "null_mean": float(null.mean()), "p": p}


def render_svg_pie(counts: dict, colors: dict, size=140) -> str:
    tot = sum(counts.values())
    cx = cy = size / 2
    r = size / 2 - 8
    if tot == 0:
        return f"<svg width='{size}' height='{size}'><circle cx='{cx}' cy='{cy}' r='{r}' fill='#333'/></svg>"
    svg, curr = [f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}'>"], 0.0
    for key, count in counts.items():
        if count == 0:
            continue
        frac = count / tot
        ang = frac * 2 * math.pi
        x1, y1 = cx + r * math.cos(curr), cy + r * math.sin(curr)
        x2, y2 = cx + r * math.cos(curr + ang), cy + r * math.sin(curr + ang)
        if frac >= 0.999:
            d = f"M {cx} {cy - r} A {r} {r} 0 1 1 {cx - 0.001} {cy - r} Z"
        else:
            d = f"M {cx} {cy} L {x1} {y1} A {r} {r} 0 {1 if ang > math.pi else 0} 1 {x2} {y2} Z"
        svg.append(f"<path d='{d}' fill='{colors.get(key, '#808080')}' stroke='#111' stroke-width='1'/>")
        curr += ang
    return "".join(svg) + "</svg>"


# -----------------------------------------------------------------------------
st.title("🥧 Spot Pies: Physical Locus Comparison")
st.caption(
    "Do particular places in the book (front pages, each rosette panel, back pages) use a different mix "
    "of word endings from the rest of the manuscript? Counts come from the canonical parser; nothing is typed in."
)

try:
    df = load_corpus()
except Exception as exc:
    st.error(f"Corpus could not be loaded: {exc}")
    st.stop()

ending_colors = {e: c for e, c in zip(ENDING_LABELS, [
    "#000000", "#444444", "#d62728", "#e377c2", "#ff7f0e", "#bcbd22", "#8c564b",
    "#1f77b4", "#17becf", "#aec7e8", "#9467bd", "#c5b0d5", "#2ca02c", "#98df8a", "#ffbb78", "#808080"])}

results = {name: test_spot(df, tuple(folios)) for name, folios in spot_pies.SPOTS.items()}
n_tested = sum(r["status"] == "tested" for r in results.values())
alpha_each = ALPHA / max(n_tested, 1)

# Pies
st.markdown("### Pies")
names = list(spot_pies.SPOTS)
for row_start in range(0, len(names), 4):
    cols = st.columns(4)
    for col, name in zip(cols, names[row_start:row_start + 4]):
        folios = spot_pies.SPOTS[name]
        sub = df[df["folio"].isin(folios)]
        with col:
            st.markdown(f"**{name}**")
            st.caption(", ".join(folios))
            st.markdown(f"N = **{len(sub):,}** words")
            if sub.empty:
                st.warning("No words found for these folios.")
                continue
            counts = sub["ending"].value_counts().reindex(ENDING_LABELS, fill_value=0).to_dict()
            colors = ending_colors
            st.markdown(render_svg_pie(counts, colors), unsafe_allow_html=True)
            with st.expander("Top 10 words"):
                for tok, c in sub["clean"].value_counts().head(10).items():
                    st.text(f"{tok} ({c})")

# Comparison table
st.markdown("---")
st.markdown("### Share of each ending, by spot")
col = "ending"
labels = ENDING_LABELS
table = pd.DataFrame({"Category": [f"-{x}" if x != "?" else x for x in labels]})
for name, folios in spot_pies.SPOTS.items():
    sub = df[df["folio"].isin(folios)]
    table[name] = [f"{v:.1%}" for v in distribution(sub[col], labels)] if len(sub) else ["—"] * len(labels)
table["Whole book"] = [f"{v:.1%}" for v in distribution(df[col], labels)]
st.dataframe(table, use_container_width=True)

# Test and verdict
st.markdown("---")
st.markdown("### Test: is each spot more unusual than ordinary pages?")
st.caption(
    f"Statistic: how far the spot's ending mix is from the rest of the book (total-variation distance). "
    f"Null: {N_DRAWS:,} random sets of whole pages from the rest of the book with about the same number of words, "
    f"so a spot only counts as different if it is more unusual than ordinary pages are. "
    f"Spots under {MIN_TOKENS} words are not tested. Threshold {ALPHA} split across the {n_tested} tested "
    f"spots (Bonferroni): p < {alpha_each:.4f}."
)
rows = []
for name, r in results.items():
    if r["status"] == "tested":
        verdict = "MORE UNUSUAL than ordinary pages" if r["p"] < alpha_each else "no detectable difference"
        rows.append({"Spot": name, "Words": r["n"], "Distance": round(r["distance"], 3),
                     "Typical for random pages": round(r["null_mean"], 3), "p": round(r["p"], 4), "Verdict": verdict})
    else:
        rows.append({"Spot": name, "Words": r["n"], "Distance": None, "Typical for random pages": None,
                     "p": None, "Verdict": r["status"]})
verdicts = pd.DataFrame(rows)
st.dataframe(verdicts, use_container_width=True)
st.info(
    "A difference means the spot's word endings are unusual for the book. It does not say why: the rosette "
    "panels are mostly circular and label text, which behaves differently from paragraph text everywhere in "
    "the manuscript (see the blind holdout, target B)."
)

# Downloads
st.markdown("---")
c1, c2 = st.columns(2)
c1.download_button("Download spot_pies.csv", data=table.to_csv(index=False).encode("utf-8"),
                   file_name="spot_pies.csv", mime="text/csv")
c2.download_button("Download spot_tests.csv", data=verdicts.to_csv(index=False).encode("utf-8"),
                   file_name="spot_tests.csv", mime="text/csv")
