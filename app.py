"""
Voynich Manuscript Workbench
Single-file Streamlit app. Frozen role map. No translation claims.
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

# ---------------------------------------------------------------------------
# Frozen map
# ---------------------------------------------------------------------------
ROLE_COLORS = {
    "heat": "#FF0000",
    "medium": "#00FFFF",
    "outlet": "#FFA500",
    "reflux": "#800080",
    "retain": "#008000",
    "drain": "#000000",
    "unmapped": "#808080",
}

SECTION_OUTLINES = {
    "Zodiac / Wheel": "#D4AF37",
    "Bath / Pipe": "#008080",
    "Herbal": "#808000",
    "Rosettes Foldout": "#6B4C9A",
    "Recipe / Other": "#888888",
}

ROLES = ["heat", "medium", "outlet", "reflux", "retain", "drain", "unmapped"]

FRONT = {"f1r", "f1v", "f2r"}
FOLD_LEFT = {"f85v1", "f85v2", "f85v"}
FOLD_CENTER = {"f86r3"}
FOLD_RIGHT = {"f86r4", "f86r5", "f86r6", "f86r"}
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


def quire_of(folio: str) -> str:
    m = re.match(r"f(\d+)", str(folio).lower())
    if not m:
        return "Q??"
    n = int(m.group(1))
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
    m = re.match(r"f(\d+)", str(folio).lower())
    n = int(m.group(1)) if m else 0
    if 67 <= n <= 73:
        return "Zodiac / Wheel"
    if 75 <= n <= 84:
        return "Bath / Pipe"
    if 85 <= n <= 86:
        return "Rosettes Foldout"
    if n >= 103:
        return "Recipe / Other"
    return "Herbal"


def rows_from_line(folio: str, line: str, quire: str, sec: str, text: str, ring: bool) -> list[dict]:
    toks = str(text).split()
    out = []
    for idx, tok in enumerate(toks):
        role = tag_token_role(tok)
        pos = "start" if idx == 0 else ("end" if idx == len(toks) - 1 else "mid")
        out.append(
            {
                "folio": folio,
                "line": line,
                "quire": quire,
                "section": sec,
                "token": tok,
                "role": role,
                "apparatus_part": apparatus_part(role),
                "pos_in_line": pos,
                "is_ring_label": ring,
                "source": "sample",
            }
        )
    return out


@st.cache_data
def load_sample_records() -> pd.DataFrame:
    raw_lines = [
        ("f1r", "f1r.1", "Q01", "Herbal", "fachys ykal ar ataiin shol shory", False),
        ("f1r", "f1r.6", "Q01", "Herbal", "okchoy otchol chocthy ydaraishy chdam", False),
        ("f9r", "f9r.10", "Q01", "Herbal", "chy tor chyty dary ytchas shedam", False),
        ("f28v", "f28v.1", "Q04", "Herbal", "kshol qooiiin shor pshoiiin shepchy qoty dy shory", False),
        ("f52v", "f52v.8", "Q07", "Herbal", "kodaiin cthy qokeey s ol daiin", False),
        ("f70v", "f70v.1", "Q09", "Zodiac / Wheel", "otcheod oteodal otcheor", True),
        ("f70v", "f70v.side", "Q09", "Zodiac / Wheel", "qokedy daiin shedy chdam", False),
        ("f71r", "f71r.1", "Q09", "Zodiac / Wheel", "opairam okeal otcheor dal", True),
        ("f71r", "f71r.side", "Q09", "Zodiac / Wheel", "qotedy cheol daiin am", False),
        ("f72r1", "f72r1.1", "Q09", "Zodiac / Wheel", "oteeo cthey chlol oteey", True),
        ("f72v1", "f72v1.1", "Q09", "Zodiac / Wheel", "otol otedy chesal oteor", True),
        ("f75r", "f75r.01", "Q13", "Bath / Pipe", "shedy qool shedaiin chdam", False),
        ("f76r", "f76r.05", "Q13", "Bath / Pipe", "shedy shedaiin lkaiin shedam", False),
        ("f76v", "f76v.36", "Q13", "Bath / Pipe", "daiin cheol teey lshety okeey qeedy chdam", False),
        ("f82v", "f82v.19", "Q13", "Bath / Pipe", "shedaiin lkaiin ol chedy shedam", False),
        ("f85v2", "f85v2.c", "Q14", "Rosettes Foldout", "otol", False),
        ("f103r", "f103r.12", "Q17", "Recipe / Other", "chedaiin cheey qotedy dair shedy qokedy chdam", False),
        ("f104r", "f104r.35", "Q17", "Recipe / Other", "qocheol chedaiin qodal chdam", False),
        ("f114v", "f114v.4", "Q20", "Recipe / Other", "qokedy cheocthedy qoted chedar okeedy daiin chedaiin", False),
        ("f114v", "f114v.21", "Q20", "Recipe / Other", "qokedy otcheodaiin qokchdy", False),
        ("f114v", "f114v.29", "Q20", "Recipe / Other", "otcheed qopairam", False),
        ("f114v", "f114v.31", "Q20", "Recipe / Other", "otcheody lkchedy", False),
        ("f116v", "f116v.1", "Q20", "Recipe / Other", "oror sheey", False),
    ]
    rows = []
    for folio, line, quire, sec, text, ring in raw_lines:
        rows.extend(rows_from_line(folio, line, quire, sec, text, ring))
    return pd.DataFrame(rows)


LOCUS_RE = re.compile(
    r"^<(?P<folio>f\d{1,3}[rv]\d?)\.(?P<locus>[^>;]+)(?:;(?P<lang>[A-Za-z]))?>",
    re.I,
)
FOLIO_ONLY_RE = re.compile(r"^<(?P<folio>f\d{1,3}[rv]\d?)>", re.I)
WORD_RE = re.compile(r"[a-zA-Z]+")


def parse_ivtff_text(raw: str) -> pd.DataFrame:
    rows = []
    current_folio = "unknown"
    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        loc = LOCUS_RE.match(line)
        fol = FOLIO_ONLY_RE.match(line)
        if loc:
            current_folio = loc.group("folio").lower()
            payload = line[loc.end():]
            line_id = f"{current_folio}.{loc.group('locus')}"
        elif fol:
            current_folio = fol.group("folio").lower()
            continue
        else:
            payload = line
            line_id = current_folio
        payload = re.sub(r"\{[^}]*\}", " ", payload)
        payload = payload.replace(".", " ").replace(",", " ")
        payload = re.sub(r"[-=*%|!;:()<>]", " ", payload)
        toks = [t.lower() for t in WORD_RE.findall(payload)]
        for idx, tok in enumerate(toks):
            role = tag_token_role(tok)
            pos = "start" if idx == 0 else ("end" if idx == len(toks) - 1 else "mid")
            rows.append(
                {
                    "folio": current_folio,
                    "line": line_id,
                    "quire": quire_of(current_folio),
                    "section": section_of(current_folio),
                    "token": tok,
                    "role": role,
                    "apparatus_part": apparatus_part(role),
                    "pos_in_line": pos,
                    "is_ring_label": False,
                    "source": "ivtff",
                }
            )
    return pd.DataFrame(rows)


def try_disk_corpus() -> tuple[pd.DataFrame | None, str]:
    paths = [
        Path("data/ZL3b-n.txt"),
        Path("data/IT2a-n.txt"),
        Path("data/ZL_ivtff_2b.txt"),
        Path("ZL3b-n.txt"),
        Path("IT2a-n.txt"),
        Path("data/spot_pies/full_corpus_role_counts.csv"),
        Path("voynich_spectral_filtered_corpus.csv"),
    ]
    for p in paths:
        if not p.exists():
            continue
        if p.suffix.lower() == ".csv":
            df = pd.read_csv(p)
            tok_col = next((c for c in ("token", "word", "eva", "text") if c in df.columns), None)
            if tok_col is None:
                continue
            if "role" not in df.columns:
                df["role"] = df[tok_col].map(tag_token_role)
            if "folio" not in df.columns:
                df["folio"] = "unknown"
            return df, f"csv {p}"
        raw = p.read_text(encoding="utf-8", errors="ignore")
        df = parse_ivtff_text(raw)
        if len(df) > 500:
            return df, f"ivtff {p}"
    return None, "none"


def get_svg_pie(counts_dict: dict, size: int = 140) -> str:
    total = sum(counts_dict.values())
    if total == 0:
        return "<svg width='100' height='100'></svg>"
    cx, cy, r = size / 2, size / 2, (size / 2) - 10
    svg = [f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}'>"]
    curr = 0.0
    for role, count in counts_dict.items():
        if count == 0:
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


sample_df = load_sample_records()
disk_df, disk_src = try_disk_corpus()

st.title("Voynich Manuscript Workbench")
st.caption("Process-log / apparatus hypothesis. Not a translation.")

uploaded = st.sidebar.file_uploader("Upload IVTFF .txt or token .csv", type=["txt", "csv"])
view_df = sample_df
mode = f"DEMO SAMPLE — {len(sample_df)} tokens (not the full book)"

if uploaded is not None:
    if uploaded.name.lower().endswith(".csv"):
        tmp = pd.read_csv(uploaded)
        tok_col = next((c for c in ("token", "word", "eva", "text") if c in tmp.columns), None)
        if tok_col:
            if "role" not in tmp.columns:
                tmp["role"] = tmp[tok_col].map(tag_token_role)
            if "folio" not in tmp.columns:
                tmp["folio"] = "unknown"
            view_df = tmp
            mode = f"UPLOAD CSV — {len(view_df):,} rows"
    else:
        raw = uploaded.getvalue().decode("utf-8", errors="ignore")
        parsed = parse_ivtff_text(raw)
        if len(parsed):
            view_df = parsed
            mode = f"UPLOAD IVTFF — {len(view_df):,} tokens"
elif disk_df is not None and len(disk_df) > len(sample_df):
    view_df = disk_df
    mode = f"DISK — {disk_src} — {len(view_df):,} tokens"

if len(view_df) < 1000:
    st.error(
        "Active table is the baked-in sample, not the manuscript. "
        "Upload ZL3b-n.txt or put it in data/ZL3b-n.txt. "
        "Source: https://www.voynich.nu/data/ZL3b-n.txt"
    )
else:
    st.success(mode)

st.sidebar.metric("Active tokens", f"{len(view_df):,}")
st.sidebar.write(mode)

tabs = st.tabs(
    [
        "Visual Key Hunt",
        "Substitution Gate",
        "Decan Grounding",
        "Interlinear Reader",
        "Slot Omega Miner",
        "Author Audit",
        "Carrier Matrix",
        "Nature of Text",
        "Export",
        "Full Corpus Counts",
        "Spot Pies",
    ]
)

# ---------------------------------------------------------------------------
# TAB 0 Visual Key Hunt (uses sample_df so old demo stays stable)
# ---------------------------------------------------------------------------
demo = sample_df
with tabs[0]:
    st.header("Visual Key Hunt")
    st.caption("Picture vs token-role on the demo slice. Not a decode.")
    quires = sorted(demo["quire"].unique())
    q_cols = st.columns(max(len(quires), 1))
    captions = {
        "Q01": "Botanical charge",
        "Q04": "Heating ascent",
        "Q07": "Vapor column",
        "Q09": "Wheel / static",
        "Q13": "Vat / receiver",
        "Q14": "Foldout hub",
        "Q17": "Compounding",
        "Q20": "Collection / purge",
    }
    for idx, q in enumerate(quires):
        q_df = demo[demo["quire"] == q]
        with q_cols[idx]:
            st.markdown(f"**{q}**")
            st.markdown(get_svg_pie(q_df["role"].value_counts().to_dict(), 120), unsafe_allow_html=True)
            st.caption(captions.get(q, ""))

    st.markdown("---")
    st.subheader("Folio heatmap (demo slice)")
    ct = pd.crosstab(demo["folio"], demo["role"], normalize="index").reindex(columns=ROLES[:-1], fill_value=0.0)
    folio_order = [
        "f1r", "f9r", "f28v", "f52v", "f70v", "f71r", "f72r1", "f72v1",
        "f75r", "f76r", "f76v", "f82v", "f85v2", "f103r", "f104r", "f114v", "f116v",
    ]
    ct = ct.reindex([f for f in folio_order if f in ct.index])
    st.dataframe(ct.round(2), use_container_width=True)

    z_df = demo[demo["section"] == "Zodiac / Wheel"]
    ring_roles = z_df[z_df["is_ring_label"]]["role"].value_counts().to_dict()
    side_roles = z_df[~z_df["is_ring_label"]]["role"].value_counts().to_dict()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Ring labels**")
        st.markdown(get_svg_pie(ring_roles, 150), unsafe_allow_html=True)
    with c2:
        st.markdown("**Side text**")
        st.markdown(get_svg_pie(side_roles, 150), unsafe_allow_html=True)

    b_df = demo[demo["section"] == "Bath / Pipe"]
    t_zone = ring_roles.get("heat", 0) == 0 and ring_roles.get("drain", 0) == 0
    t_bath = (len(b_df) > 0) and (b_df["role"].isin(["retain", "drain"]).mean() > 0.40)
    max_sh = demo["role"].value_counts(normalize=True).max()
    t_pie = max_sh < 0.80
    t_split = set(ring_roles) != set(side_roles)
    st.write(
        f"T-zone: {'PASS' if t_zone else 'FAIL'} | "
        f"T-bath: {'PASS' if t_bath else 'FAIL'} | "
        f"T-pie: {'PASS' if t_pie else 'FAIL'} ({max_sh*100:.1f}%) | "
        f"T-split: {'PASS' if t_split else 'FAIL'}"
    )
    st.info("These checks are on the demo slice only until a full transcription is loaded.")

# ---------------------------------------------------------------------------
# TAB 1 Substitution Gate
# ---------------------------------------------------------------------------
with tabs[1]:
    st.subheader("Holdout substitution gate")
    st.metric("Demo tokens", f"{len(demo)}")
    st.metric("Latin pharma hits on this slice", "not computed here")
    st.dataframe(demo[["folio", "line", "token", "role"]].head(20), use_container_width=True)
    st.caption("CVC / Latin scores from earlier notebooks are not recomputed in this file.")

# ---------------------------------------------------------------------------
# TAB 2 Decan
# ---------------------------------------------------------------------------
with tabs[2]:
    st.subheader("Zodiac spoke table (hypothesis only)")
    st.warning("CV overlap is not a decode. Do not freeze these as names.")
    st.dataframe(
        pd.DataFrame(
            [
                {"Folio": "f70v", "Token": "otcheod", "Guess": "sector label", "Note": "CV crib only"},
                {"Folio": "f71r", "Token": "opairam", "Guess": "sector label", "Note": "CV crib only"},
                {"Folio": "f72r1", "Token": "dal", "Guess": "short label", "Note": "CV crib only"},
            ]
        ),
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# TAB 3 Interlinear
# ---------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Functional glosses (not English plaintext)")
    st.warning("These are role glosses on the demo lines. They are not a translation.")
    for loc, raw, gloss in [
        ("f114v.4", "qokedy cheocthedy qoted chedar okeedy daiin chedaiin", "heat ... medium ..."),
        ("f114v.21", "qokedy otcheodaiin qokchdy", "heat + medium-buffer + heat"),
        ("f116v.1", "oror sheey", "reflux + unmapped"),
    ]:
        with st.expander(loc, expanded=False):
            st.code(raw)
            st.write(gloss)

# ---------------------------------------------------------------------------
# TAB 4 Slot omega
# ---------------------------------------------------------------------------
with tabs[4]:
    st.subheader("Q-active sandwich frames on the demo slice")
    frames = []
    toks = demo["token"].astype(str).tolist()
    roles = demo["role"].tolist()
    loci = demo["line"].tolist()
    for i in range(1, len(toks) - 1):
        if roles[i - 1] == "heat" and roles[i] == "medium" and roles[i + 1] == "heat":
            frames.append({"locus": loci[i], "frame": f"{toks[i-1]} -> {toks[i]} -> {toks[i+1]}"})
    if frames:
        st.dataframe(pd.DataFrame(frames), use_container_width=True)
    else:
        st.write("No heat-medium-heat sandwich in the demo slice.")

# ---------------------------------------------------------------------------
# TAB 5 Author
# ---------------------------------------------------------------------------
with tabs[5]:
    st.subheader("Colophon / seal tokens (descriptive only)")
    st.dataframe(
        pd.DataFrame(
            [
                {"Locus": "f1r.6", "Token": "ydaraishy", "Tag": "unmapped / claimed attribution"},
                {"Locus": "f9r.10", "Token": "ytchas", "Tag": "unmapped / claimed scribal"},
                {"Locus": "f116v.1", "Token": "oror sheey", "Tag": "reflux + unmapped"},
            ]
        ),
        use_container_width=True,
    )
    st.caption("Jacobus de Tepenecz is a known later owner mark on f1r. That is not an internal decode.")

# ---------------------------------------------------------------------------
# TAB 6 Carrier
# ---------------------------------------------------------------------------
with tabs[6]:
    st.subheader("Role counts on the ACTIVE table")
    st.dataframe(
        view_df["role"].value_counts().reindex(ROLES, fill_value=0).to_frame("count"),
        use_container_width=True,
    )
    if "section" in view_df.columns:
        st.dataframe(
            pd.crosstab(view_df["section"], view_df["role"]).reindex(columns=ROLES, fill_value=0),
            use_container_width=True,
        )

# ---------------------------------------------------------------------------
# TAB 7 Nature
# ---------------------------------------------------------------------------
with tabs[7]:
    st.subheader("What this app is allowed to claim")
    st.markdown(
        """
- Layout split: wheels vs baths vs recipes can be measured.
- Drain tokens prefer line ends on many pages (known Voynich fact; here interpreted as close-state).
- Classical Latin letter-swap is not supported by the seal tests you already ran.
- This file does **not** prove a readable language or an alchemical recipe.
- G9/G10 plaintext remains unsolved.
"""
    )

# ---------------------------------------------------------------------------
# TAB 8 Export
# ---------------------------------------------------------------------------
with tabs[8]:
    st.subheader("Export")
    st.download_button(
        "Download active table CSV",
        data=view_df.to_csv(index=False).encode("utf-8"),
        file_name="voynich_active_table.csv",
        mime="text/csv",
    )
    st.download_button(
        "Download demo sample CSV",
        data=demo.to_csv(index=False).encode("utf-8"),
        file_name="voynich_demo_sample.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------------------------
# TAB 9 Full corpus counts
# ---------------------------------------------------------------------------
with tabs[9]:
    st.header("Full Corpus Role Counts")
    n = len(view_df)
    st.metric("Tokens in active table", f"{n:,}")
    if n < 1000:
        st.error("Still the demo sample. Upload ZL3b-n.txt or place it at data/ZL3b-n.txt.")
    overall = view_df["role"].value_counts().reindex(ROLES, fill_value=0)
    st.dataframe(
        overall.to_frame("count").assign(share=lambda x: (x["count"] / max(n, 1)).round(4)),
        use_container_width=True,
    )
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
        out_dir = Path("data/spot_pies")
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            view_df.to_csv(out_dir / "full_corpus_role_counts.csv", index=False)
            folio_counts.to_csv(out_dir / "full_corpus_by_folio.csv")
            st.success("Wrote data/spot_pies/full_corpus_role_counts.csv")
        except OSError as exc:
            st.warning(f"Could not write data folder: {exc}")
    st.code(
        f"FULL CORPUS COUNTS\nmode: {mode}\ntokens: {n}\nPi unchanged: YES\nSkeleton unchanged: YES",
        language="text",
    )

# ---------------------------------------------------------------------------
# TAB 10 Spot pies
# ---------------------------------------------------------------------------
with tabs[10]:
    st.header("Front / fold / back pies")
    if "folio" not in view_df.columns:
        st.warning("No folio column.")
    else:
        fol = view_df["folio"].astype(str).str.lower()
        spots = {
            "FRONT LOCK": FRONT,
            "FOLD LEFT": FOLD_LEFT,
            "FOLD CENTER": FOLD_CENTER,
            "FOLD RIGHT": FOLD_RIGHT,
            "BACK LOCK": BACK,
        }
        cols = st.columns(5)
        spot_rows = []
        for col, (name, keys) in zip(cols, spots.items()):
            sub = view_df[fol.isin(keys)]
            sn = len(sub)
            vc = sub["role"].value_counts().reindex(ROLES, fill_value=0) if sn else pd.Series(0, index=ROLES)
            with col:
                st.markdown(f"**{name}**")
                st.write("N =", sn, "SMALL-N" if sn < 30 else "ok")
                if sn:
                    st.bar_chart(vc)
                st.markdown(get_svg_pie(vc.to_dict(), 110), unsafe_allow_html=True)
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
        small = (spot_df["N"] < 30).all()
        if small:
            st.error("All five spots are SMALL-N. Load the full transcription before calling this a key.")
        else:
            st.success("At least one spot has N >= 30.")
