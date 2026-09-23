"""
Drop this file in your repo as: pages/11_Full_Corpus_Counts.py

Does NOT edit app.py.
Uses the frozen role map only.
Writes: data/spot_pies/full_corpus_role_counts.csv
"""

from __future__ import annotations

from pathlib import Path
import re

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Frozen role map — do not retune
# ---------------------------------------------------------------------------
HEAT_RE = re.compile(r"^(qo|qok|ok)", re.I)
MEDIUM_RE = re.compile(r"(daiin|aiin)$", re.I)
OUTLET_RE = re.compile(r"(ol|al)$", re.I)
REFLUX_RE = re.compile(r"(or|ar)$", re.I)
RETAIN_RE = re.compile(r"^shed", re.I)
DRAIN_RE = re.compile(r"(am|m)$", re.I)
DRAIN_EXACT = {"chdam", "shedam"}

FRONT = {"f1r", "f1v", "f2r"}
FOLD_LEFT = {"f85v1", "f85v2", "f85v"}
FOLD_CENTER = {"f86r3"}
FOLD_RIGHT = {"f86r4", "f86r5", "f86r6", "f86r"}
BACK = {"f116r", "f116v"}


def role_of(token: str) -> str:
    t = str(token).strip().lower()
    if not t or t == "nan":
        return "unmapped"
    if t in DRAIN_EXACT or DRAIN_RE.search(t):
        # drain before outlet/reflux so -am wins over -al overlap on 'am'
        if t.endswith("am") or t.endswith("m"):
            if t in DRAIN_EXACT or t.endswith("am") or (t.endswith("m") and not t.endswith("am") and not t.endswith("um")):
                if t.endswith("am") or t in DRAIN_EXACT or re.search(r"[^aeiou]m$", t):
                    if t.endswith("am") or t in DRAIN_EXACT:
                        return "drain"
                    if t.endswith("m") and not t.endswith(("om", "um", "im", "em")):
                        return "drain"
    if HEAT_RE.match(t):
        return "heat"
    if RETAIN_RE.match(t):
        return "retain"
    if MEDIUM_RE.search(t):
        return "medium"
    if OUTLET_RE.search(t) and not t.endswith("am"):
        return "outlet"
    if REFLUX_RE.search(t) and not t.endswith("am"):
        return "reflux"
    return "unmapped"


def find_corpus() -> pd.DataFrame | None:
    """Reuse whatever table the app already loaded."""
    for key in ("corpus", "tokens", "df", "voynich", "event_log"):
        obj = st.session_state.get(key)
        if isinstance(obj, pd.DataFrame) and not obj.empty:
            return obj

    candidates = [
        Path("data/spot_pies/full_corpus_role_counts.csv"),
        Path("data/voynich_spectral_filtered_corpus.csv"),
        Path("voynich_spectral_filtered_corpus.csv"),
        Path("data/event_log.csv"),
    ]
    for p in candidates:
        if p.exists():
            return pd.read_csv(p)
    return None


def token_column(df: pd.DataFrame) -> str:
    for c in ("token", "word", "eva", "text"):
        if c in df.columns:
            return c
    return df.columns[-1]


def folio_column(df: pd.DataFrame) -> str | None:
    for c in ("folio", "page", "fol"):
        if c in df.columns:
            return c
    return None


def quire_column(df: pd.DataFrame) -> str | None:
    for c in ("quire", "Q", "section"):
        if c in df.columns:
            return c
    return None


def normalize_folio(val) -> str:
    s = str(val).strip().lower().replace(" ", "")
    return s


st.set_page_config(page_title="Full Corpus Counts", layout="wide")
st.title("Full Corpus Role Counts")
st.caption("Frozen map. Does not change Pi or the skeleton. app.py is not modified.")

df = find_corpus()
if df is None:
    uploaded = st.file_uploader("No corpus in session. Upload a token CSV.", type=["csv"])
    if uploaded is None:
        st.error("No corpus found. Load the app's data page first, or upload the token CSV.")
        st.stop()
    df = pd.read_csv(uploaded)

tok_col = token_column(df)
fol_col = folio_column(df)
q_col = quire_column(df)

work = df.copy()
work["_token"] = work[tok_col].astype(str)
work["_role"] = work["_token"].map(role_of)
if fol_col:
    work["_folio"] = work[fol_col].map(normalize_folio)
else:
    work["_folio"] = "unknown"
if q_col:
    work["_quire"] = work[q_col].astype(str)
else:
    work["_quire"] = "unknown"

total_n = len(work)
st.metric("Total tokens tagged", f"{total_n:,}")

roles = ["heat", "medium", "outlet", "reflux", "retain", "drain", "unmapped"]
overall = work["_role"].value_counts().reindex(roles, fill_value=0)
st.subheader("Whole book")
st.dataframe(overall.to_frame("count").assign(share=lambda x: x["count"] / total_n), use_container_width=True)

# per folio
folio_counts = (
    work.groupby(["_folio", "_role"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=roles, fill_value=0)
)
folio_counts["N"] = folio_counts.sum(axis=1)
folio_counts["SMALL_N"] = folio_counts["N"] < 30
folio_counts["dominant"] = folio_counts[roles].idxmax(axis=1)
folio_counts["drain_share"] = folio_counts["drain"] / folio_counts["N"].clip(lower=1)

st.subheader("Per folio (sorted by drain share)")
st.dataframe(
    folio_counts.sort_values("drain_share", ascending=False),
    use_container_width=True,
    height=360,
)
st.write("Folios with N < 30:", int(folio_counts["SMALL_N"].sum()))

# quires
st.subheader("Per quire")
quire_counts = (
    work.groupby(["_quire", "_role"])
    .size()
    .unstack(fill_value=0)
    .reindex(columns=roles, fill_value=0)
)
quire_counts["N"] = quire_counts.sum(axis=1)
st.dataframe(quire_counts, use_container_width=True)

# three spots with REAL n
st.subheader("Front / fold / back — real N")


def slice_folios(keys: set[str]) -> pd.DataFrame:
    mask = work["_folio"].isin(keys) | work["_folio"].isin({k.replace("f", "") for k in keys})
    return work.loc[mask]


spots = {
    "FRONT LOCK": slice_folios(FRONT),
    "FOLD LEFT": slice_folios(FOLD_LEFT),
    "FOLD CENTER": slice_folios(FOLD_CENTER),
    "FOLD RIGHT": slice_folios(FOLD_RIGHT),
    "BACK LOCK": slice_folios(BACK),
}

cols = st.columns(5)
spot_rows = []
for col, (name, sub) in zip(cols, spots.items()):
    n = len(sub)
    vc = sub["_role"].value_counts().reindex(roles, fill_value=0)
    share = (vc / n) if n else vc
    with col:
        st.markdown(f"**{name}**")
        st.write("N =", n, "SMALL-N" if n < 30 else "ok")
        st.bar_chart(share)
    row = {"spot": name, "N": n}
    row.update({r: int(vc[r]) for r in roles})
    spot_rows.append(row)

spot_df = pd.DataFrame(spot_rows)
st.dataframe(spot_df, use_container_width=True)

# save
out_dir = Path("data/spot_pies")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "full_corpus_role_counts.csv"
save_df = work[["_folio", "_quire", "_token", "_role"]].rename(
    columns={"_folio": "folio", "_quire": "quire", "_token": "token", "_role": "role"}
)
save_df.to_csv(out_path, index=False)
folio_counts.to_csv(out_dir / "full_corpus_by_folio.csv")
spot_df.to_csv(out_dir / "spot_pies.csv", index=False)
st.success(f"Wrote {out_path} ({len(save_df):,} rows)")

st.code(
    "FULL CORPUS COUNTS ADDED\n"
    "Pi unchanged: YES\n"
    "Skeleton unchanged: YES\n"
    f"Total tokens tagged: {total_n}\n"
    f"Folios with N<30: {int(folio_counts['SMALL_N'].sum())}\n"
    f"Files added: {out_path}, data/spot_pies/full_corpus_by_folio.csv, data/spot_pies/spot_pies.csv",
    language="text",
)
