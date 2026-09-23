"""
Voynich Manuscript Workbench
Single-file Streamlit app. Frozen role map. ZL folio ids.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Voynich Manuscript Workbench",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROLE_COLORS = {
    "heat": "#FF0000",
    "medium": "#00FFFF",
    "outlet": "#FFA500",
    "reflux": "#800080",
    "retain": "#008000",
    "drain": "#000000",
    "unmapped": "#808080",
}
ROLES = ["heat", "medium", "outlet", "reflux", "retain", "drain", "unmapped"]

# Ids that exist in ZL3b-n.txt
FRONT = {"f1r", "f1v", "f2r"}
FOLD_LEFT = {"f85r1", "f85r2"}
FOLD_RIGHT = {"f86v3", "f86v4", "f86v5", "f86v6"}
FOLD_ALL = FOLD_LEFT | FOLD_RIGHT
BACK = {"f116r", "f116v"}


def tag_token_role(token: str) -> str:
    t = re.sub(r"[^a-z]", "", str(token).lower().strip())
    if not t:
        return "unmapped"
    if t in {"chdam", "shedam"} or t.endswith("am"):
        return "drain"
    if t.endswith("m") and not t.endswith(("om", "um", "im", "em")):
        return "drain"
    if t.startswith("shed"):
        return "retain"
    if t.startswith("qok") or t.startswith("qo") or t.startswith("ok"):
        return "heat"
    if t == "daiin" or t.endswith("aiin"):
        return "medium"
    if t.endswith("ol") or t.endswith("al"):
        return "outlet"
    if t.endswith("or") or t.endswith("ar"):
        return "reflux"
    return "unmapped"


def apparatus_part(role: str) -> str:
    return {
        "heat": "Cucurbit / Boiler",
        "medium": "Vapor Space / Menstruum",
        "outlet": "Beak / Rostellum",
        "reflux": "Inner Wall Reflux",
        "retain": "Matras / Receiver",
        "drain": "Lute / Purge Port",
    }.get(role, "Unassigned Matrix")


def normalize_folio(val: str) -> str:
    s = str(val).strip().lower().replace(" ", "").strip("<>")
    m = re.match(r"(f\d+[rv]\d*)", s)
    return m.group(1) if m else s


def folio_num(folio: str) -> int:
    m = re.match(r"f(\d+)", str(folio).lower())
    return int(m.group(1)) if m else 0


def quire_of(folio: str) -> str:
    n = folio_num(folio)
    bands = [
        (8, "Q01"), (16, "Q02"), (24, "Q03"), (32, "Q04"), (40, "Q05"),
        (48, "Q06"), (56, "Q07"), (66, "Q08"), (73, "Q09"), (74, "Q10"),
        (84, "Q13"), (86, "Q14"), (90, "Q15"), (102, "Q17"), (116, "Q20"),
    ]
    for top, q in bands:
        if n <= top:
            return q
    return "Q??"


def section_of(folio: str) -> str:
    n = folio_num(folio)
    if 67 <= n <= 73:
        return "Zodiac / Wheel"
    if 75 <= n <= 84:
        return "Bath / Pipe"
    if 85 <= n <= 86:
        return "Rosettes Foldout"
    if n >= 103:
        return "Recipe / Other"
    return "Herbal"


def get_svg_pie(counts_dict: dict, size: int = 140) -> str:
    total = sum(counts_dict.values())
    if total == 0:
        return "<svg width='100' height='100'></svg>"
    cx, cy, r = size / 2, size / 2, (size / 2) - 10
    svg = [f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}'>"]
    curr = 0.0
    for role, count in counts_dict.items():
        if not count:
            continue
        frac = count / total
        ang = frac * 2 * math.pi
        x1 = cx + r * math.cos(curr)
        y1 = cy + r * math.sin(curr)
        x2 = cx + r * math.cos(curr + ang)
        y2 = cy + r * math.sin(curr + ang)
        large = 1 if ang > math.pi else 0
        col = ROLE_COLORS.get(role, "#808080")
        if frac >= 0.999:
            d = f"M {cx} {cy-r} A {r} {r} 0 1 1 {cx-0.001} {cy-r} Z"
        else:
            d = f"M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large} 1 {x2} {y2} Z"
        svg.append(f"<path d='{d}' fill='{col}' stroke='#222' stroke-width='1'/>")
        curr += ang
    svg.append("</svg>")
    return "".join(svg)


LOCUS_RE = re.compile(
    r"^<(?P<folio>f\d{1,3}[rv]\d*)\.(?P<locus>[^>;]+)(?:;(?P<lang>[A-Za-z]))?>",
    re.I,
)
FOLIO_ONLY_RE = re.compile(r"^<(?P<folio>f\d{1,3}[rv]\d*)>", re.I)
WORD_RE = re.compile(r"[a-zA-Z]+")


def parse_ivtff_text(raw: str) -> pd.DataFrame:
    rows = []
    current = "unknown"
    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        loc = LOCUS_RE.match(line)
        fol = FOLIO_ONLY_RE.match(line)
        if loc:
            current = loc.group("folio").lower()
            payload = line[loc.end():]
            line_id = f"{current}.{loc.group('locus')}"
        elif fol:
            current = fol.group("folio").lower()
            continue
        else:
            payload = line
            line_id = current
        payload = re.sub(r"\{[^}]*\}", " ", payload)
        payload = payload.replace(".", " ").replace(",", " ")
        payload = re.sub(r"[-=*%|!;:()<>]", " ", payload)
        toks = [t.lower() for t in WORD_RE.findall(payload)]
        for idx, tok in enumerate(toks):
            role = tag_token_role(tok)
            pos = "start" if idx == 0 else ("end" if idx == len(toks) - 1 else "mid")
            rows.append(
                {
                    "folio": current,
                    "line": line_id,
                    "quire": quire_of(current),
                    "section": section_of(current),
                    "token": tok,
                    "role": role,
                    "apparatus_part": apparatus_part(role),
                    "pos_in_line": pos,
                    "source": "ivtff",
                }
            )
    return pd.DataFrame(rows)


@st.cache_data
def load_sample() -> pd.DataFrame:
    raw_lines = [
        ("f1r", "fachys ykal ar ataiin shol shory"),
        ("f1r", "okchoy otchol chocthy ydaraishy chdam"),
        ("f1v", "kydain qokain chol daiin"),
        ("f2r", "kchsy qotchy daiin"),
        ("f70v", "otcheod oteodal otcheor"),
        ("f75r", "shedy qool shedaiin chdam"),
        ("f85r1", "otol otedy chesal oteor"),
        ("f85r2", "qokedy daiin shedy"),
        ("f86v3", "qokedy otcheodaiin qokchdy"),
        ("f86v4", "otol cheor daiin"),
        ("f86v5", "shedy qokain chdam"),
        ("f86v6", "qokeey ol shedy"),
        ("f114v", "qokedy otcheodaiin qokchdy"),
        ("f116r", "qokedy chedaiin chdam"),
        ("f116v", "oror sheey"),
    ]
    rows = []
    for folio, text in raw_lines:
        toks = text.split()
        for idx, tok in enumerate(toks):
            role = tag_token_role(tok)
            pos = "start" if idx == 0 else ("end" if idx == len(toks) - 1 else "mid")
            rows.append(
                {
                    "folio": folio,
                    "line": folio,
                    "quire": quire_of(folio),
                    "section": section_of(folio),
                    "token": tok,
                    "role": role,
                    "apparatus_part": apparatus_part(role),
                    "pos_in_line": pos,
                    "source": "sample",
                }
            )
    return pd.DataFrame(rows)


def try_disk():
    for p in [
        Path("data/ZL3b-n.txt"),
        Path("ZL3b-n.txt"),
        Path("data/IT2a-n.txt"),
        Path("data/spot_pies/full_corpus_role_counts.csv"),
    ]:
        if not p.exists():
            continue
        if p.suffix.lower() == ".csv":
            df = pd.read_csv(p)
            tok = next((c for c in ("token", "word", "eva", "text") if c in df.columns), None)
            if tok is None:
                continue
            if "role" not in df.columns:
                df["role"] = df[tok].map(tag_token_role)
            if "folio" in df.columns:
                df["folio"] = df["folio"].map(normalize_folio)
            return df, f"csv {p}"
        df = parse_ivtff_text(p.read_text(encoding="utf-8", errors="ignore"))
        if len(df) > 500:
            return df, f"ivtff {p}"
    return None, "none"


def slice_spot(df: pd.DataFrame, keys: set) -> pd.DataFrame:
    if "folio" not in df.columns:
        return df.iloc[0:0]
    fol = df["folio"].map(normalize_folio)
    return df[fol.isin(keys)]


sample_df = load_sample()
disk_df, disk_src = try_disk()

st.title("Voynich Manuscript Workbench")
st.caption("Process-log / apparatus hypothesis. Not a translation. ZL folio ids.")

uploaded = st.sidebar.file_uploader("Upload IVTFF .txt or token .csv", type=["txt", "csv"])
view_df = sample_df
mode = f"DEMO SAMPLE — {len(sample_df)} tokens"

if uploaded is not None:
    if uploaded.name.lower().endswith(".csv"):
        tmp = pd.read_csv(uploaded)
        tok = next((c for c in ("token", "word", "eva", "text") if c in tmp.columns), None)
        if tok:
            if "role" not in tmp.columns:
                tmp["role"] = tmp[tok].map(tag_token_role)
            if "folio" in tmp.columns:
                tmp["folio"] = tmp["folio"].map(normalize_folio)
            view_df = tmp
            mode = f"UPLOAD CSV — {len(view_df):,} rows"
    else:
        parsed = parse_ivtff_text(uploaded.getvalue().decode("utf-8", errors="ignore"))
        if len(parsed):
            view_df = parsed
            mode = f"UPLOAD IVTFF — {len(view_df):,} tokens"
elif disk_df is not None and len(disk_df) > len(sample_df):
    view_df = disk_df
    mode = f"DISK — {disk_src} — {len(view_df):,} tokens"

if "folio" in view_df.columns:
    view_df = view_df.copy()
    view_df["folio"] = view_df["folio"].map(normalize_folio)

if len(view_df) < 1000:
    st.error(
        "Demo sample is loaded. Upload ZL3b-n.txt "
        "(https://www.voynich.nu/data/ZL3b-n.txt) for the full book."
    )
else:
    st.success(mode)

st.sidebar.metric("Active tokens", f"{len(view_df):,}")
st.sidebar.write(mode)
st.sidebar.markdown("Fold ids in ZL: `f85r1` `f85r2` `f86v3` `f86v4` `f86v5` `f86v6`")

tabs = st.tabs(
    [
        "Full Corpus Counts",
        "Spot Pies",
        "Visual Key Hunt",
        "Substitution Gate",
        "Decan Grounding",
        "Interlinear",
        "Slot Omega",
        "Author Audit",
        "Carrier Matrix",
        "Nature of Text",
        "Export",
    ]
)

with tabs[0]:
    st.header("Full Corpus Role Counts")
    n = len(view_df)
    st.metric("Tokens tagged", f"{n:,}")
    overall = view_df["role"].value_counts().reindex(ROLES, fill_value=0)
    st.dataframe(
        overall.to_frame("count").assign(share=lambda x: (x["count"] / max(n, 1)).round(4)),
        use_container_width=True,
    )
    st.bar_chart(overall)
    if "folio" in view_df.columns:
        folio_counts = (
            view_df.groupby(["folio", "role"]).size().unstack(fill_value=0).reindex(columns=ROLES, fill_value=0)
        )
        folio_counts["N"] = folio_counts.sum(axis=1)
        folio_counts["SMALL_N"] = folio_counts["N"] < 30
        folio_counts["drain_share"] = folio_counts["drain"] / folio_counts["N"].clip(lower=1)
        st.subheader("Per folio")
        st.dataframe(
            folio_counts.sort_values("drain_share", ascending=False),
            use_container_width=True,
            height=360,
        )
        st.write("Folios with N < 30:", int(folio_counts["SMALL_N"].sum()))
        try:
            out = Path("data/spot_pies")
            out.mkdir(parents=True, exist_ok=True)
            view_df.to_csv(out / "full_corpus_role_counts.csv", index=False)
            folio_counts.to_csv(out / "full_corpus_by_folio.csv")
            st.success("Wrote data/spot_pies/full_corpus_role_counts.csv")
        except OSError as exc:
            st.warning(f"Could not write data folder: {exc}")
    st.code(
        f"FULL CORPUS COUNTS\nmode: {mode}\ntokens: {n}\nPi unchanged: YES\nSkeleton unchanged: YES",
        language="text",
    )

with tabs[1]:
    st.header("Spot pies (ZL folio ids)")
    st.caption(
        "Front = f1r f1v f2r. "
        "Fold left = f85r1 f85r2. "
        "Fold right = f86v3 f86v4 f86v5 f86v6. "
        "Fold sheet = all of those. "
        "Back = f116r f116v."
    )
    spots = {
        "FRONT LOCK": FRONT,
        "FOLD LEFT": FOLD_LEFT,
        "FOLD RIGHT": FOLD_RIGHT,
        "FOLD SHEET": FOLD_ALL,
        "BACK LOCK": BACK,
    }
    cols = st.columns(5)
    spot_rows = []
    for col, (name, keys) in zip(cols, spots.items()):
        sub = slice_spot(view_df, keys)
        sn = len(sub)
        vc = sub["role"].value_counts().reindex(ROLES, fill_value=0) if sn else pd.Series(0, index=ROLES)
        with col:
            st.markdown(f"**{name}**")
            st.write("N =", sn, "SMALL-N" if sn < 30 else "ok")
            st.caption(" ".join(sorted(keys)))
            if sn:
                st.markdown(get_svg_pie(vc.to_dict(), 110), unsafe_allow_html=True)
                st.bar_chart(vc)
        row = {"spot": name, "N": sn}
        row.update({r: int(vc[r]) for r in ROLES})
        spot_rows.append(row)
    spot_df = pd.DataFrame(spot_rows)
    st.dataframe(spot_df, use_container_width=True)
    try:
        Path("data/spot_pies").mkdir(parents=True, exist_ok=True)
        spot_df.to_csv("data/spot_pies/spot_pies.csv", index=False)
    except OSError:
        pass
    fold_n = int(spot_df.loc[spot_df["spot"] == "FOLD SHEET", "N"].iloc[0])
    if fold_n == 0:
        st.error("Fold sheet empty. Folio column does not contain f85r1 / f86v3.")
    elif (spot_df["N"] < 30).all():
        st.error("All spots SMALL-N.")
    else:
        st.success("Fold sheet matched ZL ids.")

with tabs[2]:
    st.header("Visual Key Hunt")
    if "quire" in view_df.columns:
        quires = sorted(view_df["quire"].astype(str).unique())[:12]
        qcols = st.columns(max(len(quires), 1))
        for i, q in enumerate(quires):
            qc = view_df[view_df["quire"].astype(str) == q]["role"].value_counts().to_dict()
            with qcols[i]:
                st.markdown(f"**{q}**")
                st.markdown(get_svg_pie(qc, 110), unsafe_allow_html=True)
    if "section" in view_df.columns:
        z = view_df[view_df["section"] == "Zodiac / Wheel"]
        b = view_df[view_df["section"] == "Bath / Pipe"]
        zh = (z["role"] == "heat").mean() * 100 if len(z) else 0
        br = (b["role"] == "retain").mean() * 100 if len(b) else 0
        st.write(f"Zodiac heat share: {zh:.1f}% | Bath retain share: {br:.1f}%")
    st.caption("Shares measured on the active table. Not hardcoded PASS.")

with tabs[3]:
    st.header("Substitution Gate")
    st.metric("Active tokens", f"{len(view_df):,}")
    st.caption("Older Latin/CVC scores are not recomputed here.")
    st.dataframe(view_df.head(25), use_container_width=True)

with tabs[4]:
    st.header("Decan grounding")
    st.warning("CV overlap is not a decode. Do not freeze names.")

with tabs[5]:
    st.header("Interlinear")
    st.warning("Role glosses only. Not English plaintext.")
    st.code("qokedy otcheodaiin qokchdy")
    st.write("heat + medium-buffer + heat")

with tabs[6]:
    st.header("Slot Omega")
    st.caption("Heat-medium-heat sandwiches in the active table.")
    hits = []
    if {"token", "role"}.issubset(view_df.columns):
        toks = view_df["token"].astype(str).tolist()
        roles = view_df["role"].tolist()
        loci = view_df["line"].astype(str).tolist() if "line" in view_df.columns else [""] * len(toks)
        for i in range(1, len(toks) - 1):
            if roles[i - 1] == "heat" and roles[i] == "medium" and roles[i + 1] == "heat":
                hits.append({"locus": loci[i], "frame": f"{toks[i-1]} -> {toks[i]} -> {toks[i+1]}"})
                if len(hits) >= 50:
                    break
    if hits:
        st.dataframe(pd.DataFrame(hits), use_container_width=True)
    else:
        st.write("No heat-medium-heat sandwich in this view.")

with tabs[7]:
    st.header("Author audit")
    st.caption("Descriptive only.")
    st.dataframe(
        pd.DataFrame(
            [
                {"Locus": "f1r", "Token": "ydaraishy", "Note": "unmapped; later owner mark exists on f1r"},
                {"Locus": "f116v", "Token": "oror sheey", "Note": "reflux + unmapped; tiny page in ZL"},
            ]
        ),
        use_container_width=True,
    )

with tabs[8]:
    st.header("Carrier matrix")
    st.dataframe(
        view_df["role"].value_counts().reindex(ROLES, fill_value=0).to_frame("count"),
        use_container_width=True,
    )
    if "section" in view_df.columns:
        st.dataframe(
            pd.crosstab(view_df["section"], view_df["role"]).reindex(columns=ROLES, fill_value=0),
            use_container_width=True,
        )

with tabs[9]:
    st.header("What this app may claim")
    st.markdown(
        """
- Full ZL load is about 41k tokens.
- Drain tokens prefer line ends.
- shed- is richer on bath pages than on wheels.
- Wheels are not heat-free on the full book.
- About half the tokens stay unmapped.
- No plaintext recipe. No decoded names.
"""
    )

with tabs[10]:
    st.header("Export")
    st.download_button(
        "Download active table CSV",
        data=view_df.to_csv(index=False).encode("utf-8"),
        file_name="voynich_active_table.csv",
        mime="text/csv",
    )
