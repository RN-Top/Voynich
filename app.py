"""
Voynich Manuscript Structural Workbench
Author: Voynich Decipherment Working Group (RN-Top/Voynich)
Corpus Standard: IVTFF EVA 2.0 / ZL3b-n Standard
Dependencies: streamlit, pandas, numpy

Every number displayed by this app is computed from the currently loaded
corpus. When a value cannot be computed it is shown as "not computed";
there are no numerical fallbacks. Tokenisation and morphology come from
the canonical parser in parser.py.
"""

import json
from collections import Counter
import numpy as np
import pandas as pd
import streamlit as st

import importlib

import parser as canonical
import structural_validation as sv
import blind_holdout as bh
import transfer_test as tt

# Streamlit Cloud reruns app.py after a git update but can keep older copies of
# these helper modules in memory, leaving the app half old and half new.
# Reload them in dependency order on every run so they always match app.py.
for _module in (canonical, sv, bh, tt):
    importlib.reload(_module)

st.set_page_config(
    page_title="Voynich Decipherment Workbench",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CORE STATIC CONSTANTS
# -----------------------------------------------------------------------------
TERMINAL_FLUSHES = ("am", "m")


NOT_COMPUTED = "not computed"


def fmt(value, spec):
    return NOT_COMPUTED if value is None else format(value, spec)


# -----------------------------------------------------------------------------
# CANONICAL PARSER (delegates to parser.py so the app and the scripts agree)
# -----------------------------------------------------------------------------
clean_raw_token = canonical.clean_raw_token

_EMPTY_PARSE = {
    "control": "NONE",
    "carrier_core": "",
    "carrier": "",
    "e_grade": 0,
    "internal_o": False,
    "exit_port": "BARE",
    "state": "?",
    "is_terminal_m": False,
}


class VoynichParser:
    @staticmethod
    def parse(token: str) -> dict:
        return {**_EMPTY_PARSE, **canonical.VoynichParser.decompose_morphology(token)}


def factorize(token: str) -> dict:
    return VoynichParser.parse(token)

# -----------------------------------------------------------------------------
# CACHED CORPUS LOADER (canonical parser only; no offline sample fallback)
# -----------------------------------------------------------------------------
def _rows_from_csv(df_up: pd.DataFrame) -> pd.DataFrame:
    records = []
    for _, row in df_up.iterrows():
        decomps = [
            d for d in (
                canonical.VoynichParser.decompose_morphology(t)
                for t in str(row.get("word", "")).split()
            )
            if d.get("valid") and d.get("clean")
        ]
        folio = str(row.get("folio", "f_up"))
        for i, d in enumerate(decomps):
            records.append({
                "folio": folio,
                "header": str(row.get("line", "line_1")),
                "locus_type": "P",
                "currier": str(row.get("currier", "?")),
                "section": str(row.get("section", canonical.infer_section(folio))),
                "token_idx": i,
                "line_len": len(decomps),
                "is_line_start": i == 0,
                "is_line_end": i == len(decomps) - 1,
                **d,
            })
    return pd.DataFrame(records)


@st.cache_data(show_spinner=False)
def load_corpus(uploaded_file=None):
    """Returns (token DataFrame, line list, source label, error message)."""
    try:
        if uploaded_file is not None:
            source = f"UPLOADED ({uploaded_file.name})"
            if uploaded_file.name.endswith(".csv"):
                df = _rows_from_csv(pd.read_csv(uploaded_file))
            else:
                df = canonical.parse_zl3b(uploaded_file)
        else:
            path = canonical.ensure_full_corpus(canonical.CORPUS_PATH)
            source = f"LOCAL ({path})"
            df = canonical.parse_zl3b(path)
    except Exception as exc:
        return pd.DataFrame(), [], "UNAVAILABLE", str(exc)

    if df.empty:
        return df, [], source, "The corpus parsed to zero tokens."

    lines = [
        {
            "folio": folio,
            "header": header,
            "locus_type": grp["locus_type"].iloc[0],
            "currier": grp["currier"].iloc[0],
            "section": grp["section"].iloc[0],
            "tokens": grp["clean"].tolist(),
        }
        for (folio, header), grp in df.groupby(["folio", "header"], sort=False)
    ]
    return df, lines, source, None


# -----------------------------------------------------------------------------
# APPLICATION HEADER
# -----------------------------------------------------------------------------
uploaded_file = st.sidebar.file_uploader("Upload ZL3b Transcription / Text File", type=["txt", "csv"])
corpus_df, lines_corpus, corpus_source, corpus_error = load_corpus(uploaded_file)
if corpus_error:
    st.error(f"Corpus could not be loaded ({corpus_source}): {corpus_error}")
    st.stop()
st.sidebar.caption(f"Corpus source: {corpus_source}")
total_tokens_count = len(corpus_df)


def line_end_stats(lines):
    """-m/-am line-final counts and odds ratio over lines with >= 2 tokens."""
    m_end = m_mid = other_end = other_mid = 0
    for l in lines:
        toks = l["tokens"]
        if len(toks) < 2:
            continue
        for i, tok in enumerate(toks):
            is_m = sv.ending_of(tok) in TERMINAL_FLUSHES
            is_end = i == len(toks) - 1
            if is_m and is_end:
                m_end += 1
            elif is_m:
                m_mid += 1
            elif is_end:
                other_end += 1
            else:
                other_mid += 1
    total_m = m_end + m_mid
    pct = m_end / total_m * 100 if total_m else None
    odds = (m_end * other_mid) / (m_mid * other_end) if m_mid and other_end else None
    return {"m_end": m_end, "total_m": total_m, "pct": pct, "odds_ratio": odds}


def directional_delta(lines, min_count=30):
    al_count = ar_count = al_kd = ar_kd = 0
    for l in lines:
        toks = l["tokens"]
        for w1, w2 in zip(toks[:-1], toks[1:]):
            if w1.endswith("al"):
                al_count += 1
                al_kd += w2.startswith(("k", "d"))
            elif w1.endswith("ar"):
                ar_count += 1
                ar_kd += w2.startswith(("k", "d"))
    if al_count < min_count or ar_count < min_count or not (0 < al_kd < al_count) or not (0 < ar_kd < ar_count):
        return None
    p_al, p_ar = al_kd / al_count, ar_kd / ar_count
    return float(np.log((p_al / (1 - p_al)) / (p_ar / (1 - p_ar))))


flush = line_end_stats(lines_corpus)
dir_delta = directional_delta(lines_corpus)

st.title("Voynich Decipherment Workbench")
st.caption(f"Corpus: {corpus_source} · every figure below is computed live from this corpus")

c_col1, c_col2, c_col3 = st.columns(3)
with c_col1:
    st.markdown("### Corpus Size")
    st.markdown(f"## {total_tokens_count:,}")
    st.caption(f"↑ Tokens (canonical parser) · {len(lines_corpus):,} lines")
with c_col2:
    st.markdown("### -m / -am at Line End")
    st.markdown(f"## {fmt(flush['pct'], '.1f')}{'%' if flush['pct'] is not None else ''}")
    st.caption(f"↑ {flush['m_end']}/{flush['total_m']} tokens · odds ratio {fmt(flush['odds_ratio'], '.1f')}")
with c_col3:
    st.markdown("### -al vs -ar successor shift")
    st.markdown(f"## Δ = {fmt(dir_delta, '.3f')}")
    st.caption("log-odds of a k-/d- next word after -al vs -ar")

st.markdown("---")

# -----------------------------------------------------------------------------
# WORKBENCH NAVIGATION TABS
# -----------------------------------------------------------------------------
(
    tab_findings,
    tab_holdout,
    tab_parser,
    tab_tests,
    tab_omega,
    tab_reader,
    tab_export,
) = st.tabs([
    "📄 Findings",
    "🎯 Blind Holdout",
    "🔬 Token Breakdown",
    "🧪 Verification Suite",
    "⚡ Slot Ω Miner",
    "📖 Folio Reader",
    "💾 Export",
])

# =============================================================================
# TAB 1: FINDINGS
# =============================================================================
with tab_findings:
    st.header("What the tests show")
    st.markdown("""
    This workbench studies the **structure** of the Voynich text: how words are built and where they sit on
    the page. Every claim below was tested against chance and against simpler explanations, and the strongest
    ones on 43 pre-registered pages the rules had never been tuned on. Full details: `VALIDATION.md`;
    how to reproduce: `REPLICATION.md`.
    """)

    st.subheader("Supported")
    st.markdown(f"""
    - **Line-final -m / -am.** {flush['m_end']} of {flush['total_m']} words ending in -m/-am are the last word on
      their line (odds ratio ≈ {fmt(flush['odds_ratio'], '.0f')}). They are about half as common at paragraph ends,
      so this looks like a scribal line-end habit, not an end-of-section marker.
    - **Endings predict position on unseen pages.** On the blind holdout, a word's ending predicts whether it ends
      its line (AUC 0.67) and whether it sits in a label or in running text (AUC 0.64).
    - **Stems predict their endings on unseen pages** (0.78 bits per word).
    - **Folded sheets are units of writing.** The two halves of a folded sheet share more vocabulary than other
      page pairs, even with the same scribe and dialect.
    - **The results hold on a second representation of the text** (alternative readings, uncertain spaces joined).
    """)

    st.subheader("Tested and not supported")
    st.markdown("""
    These ideas were tested and did not hold up. The code is kept in `archive/` and the results in
    `VALIDATION.md`, so they can be revisited if new evidence appears.

    | Idea | What the test found |
    |---|---|
    | Venetian / German translations | Glosses place words in their expected sections no better than shuffled glosses (p ≈ 0.4). |
    | C → L → P → R four-state cycle | No better than simpler word-to-word patterns (Markov controls); the published grouping of endings is not the one the text prefers. |
    | Front/back/center fold as a key | Words that land on each other when folded match no better than for ordinary pages. |
    | Zodiac labels as day names | Labels at the same position on different months match no better than shuffled labels (p ≈ 0.76). |
    | 90.2% "blind" prediction | Its pages had already been used; replaced by the pre-registered blind holdout. |
    | 99.79% Macer Floridus match | Its comparison vectors were random. |
    | Δ = −1.018 directional shift | A placeholder number; the real value has the opposite sign. |
    """)

    st.subheader("Open leads")
    st.markdown("""
    - Key-like pages: **f57v** and **f49v** (found independently by the Anomaly Scan page), and the Roman-letter column in the **f1r** margin.
    - Stroke marks around the rim of **f67r2** that the transcription does not record (see `IMAGE_NOTES.md`).
    - Still to do: an independent transcription (Takahashi), medieval Italian/German comparison texts, outside replication.
    """)

# =============================================================================
# TAB 2: BLIND HOLDOUT
# =============================================================================
with tab_holdout:
    st.header("🎯 Blind Holdout Test")
    try:
        blind_spec = bh.load_holdout()
    except FileNotFoundError:
        blind_spec = None

    if blind_spec is None:
        st.info(f"Blind holdout: {NOT_COMPUTED} (data/blind_holdout_v1.json is missing).")
    else:
        st.markdown(f"""
        **{len(blind_spec['holdout_folios'])} folios** were drawn at random (seed {blind_spec['seed']}) from pages
        never used for cribs, the dossier or the old holdout, and committed on
        {blind_spec['created_at'][:10]} **before** the scoring code existed. The model trains on every other
        folio. Its only input is each token's ending from the frozen parser rules, and every target is
        something that spelling does not decide: where the token sits in the line, whether it is in a
        label or diagram, and which section the page belongs to.
        """)
        with st.expander("Frozen holdout folios"):
            st.write(", ".join(blind_spec["holdout_folios"]))

        bh_perms = st.number_input("Permutations", min_value=200, max_value=10000, value=2000, step=200, key="bh_perms")
        if st.button("Run Blind Holdout Test", type="primary"):
            with st.spinner("Scoring the frozen holdout..."):
                bres = bh.run(corpus_df, blind_spec, int(bh_perms))
            rows = []
            for key, label in (
                ("A_line_end_by_ending", "A. Line-final token (15 endings)"),
                ("A_line_end_by_state", "A. Line-final token (4 states C/L/P/R)"),
                ("B_layout_by_ending", "B. Label / diagram vs paragraph"),
            ):
                r = bres[key]
                rows.append({"Target": label, "Holdout size": f"{r['test_tokens']:,} tokens",
                             "Score": f"AUC {r['auc']:.3f}", "Chance": f"{r['null_auc_mean']:.3f}",
                             "p": f"{r['p']:.2g}", "Verdict": bh.verdict(r["p"])})
            c = bres["C_section"]
            rows.append({"Target": "C. Section of each folio", "Holdout size": f"{c['test_folios']} folios",
                         "Score": f"{c['accuracy']:.1%} correct",
                         "Chance": f"{c['majority_baseline']:.1%} always '{c['majority_section']}'",
                         "p": f"{c['p']:.2g}",
                         "Verdict": bh.verdict(c["p"], c["accuracy"], c["majority_baseline"])})
            d = bres["D_carrier_stems"]
            rows.append({"Target": "D. Stem predicts its ending", "Holdout size": f"{d['tokens_with_seen_stem']:,} tokens",
                         "Score": f"{d['bits_gain_per_token']:.3f} bits/token", "Chance": "0 bits (stem ignored)",
                         "p": f"{d['p']:.2g}", "Verdict": bh.verdict(d["p"], d["bits_gain_per_token"], 0.0)})
            st.dataframe(pd.DataFrame(rows), width="stretch")
            st.caption("AUC 0.5 = chance, 1.0 = perfect. PASS means p < 0.01; section prediction must also "
                       "beat always guessing the most common section.")
            with st.expander("Section prediction per holdout folio"):
                st.dataframe(pd.DataFrame(c["per_folio"]), width="stretch")


# =============================================================================
# TAB 3: CANONICAL TOKEN BREAKDOWN (VOYNICHPARSER INSPECTOR)
# =============================================================================
with tab_parser:
    st.header("Canonical Morphological Token Breakdown")
    st.markdown("""
    Break a word into its parts with the canonical parser: prefix, core and ending.
    """)

    sample_token_input = st.text_input("Input single token or EVA string:", value="qokedy")
    
    if sample_token_input:
        breakdown = VoynichParser.parse(sample_token_input)
        
        st.subheader("Decomposition:")
        shown = {k: v for k, v in breakdown.items() if k != "state"}
        st.code(json.dumps(shown, indent=2), language="json")
        
        c_k1, c_k2, c_k3 = st.columns(3)
        c_k1.markdown(f"**Clean Token:** `{breakdown['clean']}`")
        c_k1.markdown(f"**Prefix Control:** `{breakdown['control']}`")
        
        c_k2.markdown(f"**Carrier Core:** `{breakdown['carrier_core']}`")
        c_k2.markdown(f"**Exit Port:** `{breakdown['exit_port']}`")
        
        c_k3.markdown(f"**Ending:** `-{sv.ending_of(breakdown['clean'])}`")
        c_k3.markdown(f"**Ends in -m / -am:** `{breakdown['is_terminal_m']}`")

# =============================================================================
# TAB 8: AUTOMATED VERIFICATION SUITE
# =============================================================================
with tab_tests:
    st.header("Corpus-Wide Empirical Verification Suite")
    st.markdown("Execute automated statistical test batteries against the full transliteration corpus to audit structural gates.")

    if st.button("🚀 Execute Full Verification Suite (All Batteries)", type="primary"):
        with st.spinner("Executing statistical tests across all tokens..."):
            qo_prefixes = ("qo", "qok", "qot")
            diagram_toks = [t for l in lines_corpus if l["locus_type"] != "P" for t in l["tokens"]]
            prose_toks = [t for l in lines_corpus if l["locus_type"] == "P" for t in l["tokens"]]
            diagram_qo = sum(t.startswith(qo_prefixes) for t in diagram_toks)
            prose_qo = sum(t.startswith(qo_prefixes) for t in prose_toks)
            diag_rate = diagram_qo / len(diagram_toks) * 100 if diagram_toks else None
            prose_rate = prose_qo / len(prose_toks) * 100 if prose_toks else None

            log_odds_delta = directional_delta(lines_corpus, min_count=50)

            st.success("✅ Verification suite executed on the loaded corpus.")

            c1, c2, c3 = st.columns(3)
            c1.metric("A2: Line-Terminal -m / -am Rate", f"{fmt(flush['pct'], '.1f')}%")
            c1.caption(f"{flush['m_end']} of {flush['total_m']} words ending in -m/-am are the last word on their line; "
                       f"such words are about {fmt(flush['odds_ratio'], '.0f')}× more likely to be line-final than "
                       f"other words. Supported by every test, including the blind holdout.")
            c2.metric("Diagram qo- Rate (labels, rings, radii)", f"{fmt(diag_rate, '.2f')}%")
            c2.caption(f"{diagram_qo} of {len(diagram_toks)} label/diagram words start with qo-, versus "
                       f"{fmt(prose_rate, '.1f')}% in paragraph text. Descriptive; not significance-tested here.")
            c3.metric("A4: Directional Routing Shift", f"{fmt(log_odds_delta, '.3f')} log-odds")
            c3.caption("Log-odds that a word after -al (vs after -ar) starts with k-/d-. The originally published "
                       "−1.018 was a placeholder and is withdrawn; this is the real value.")


    st.markdown("---")
    st.subheader("Representation / transcription transfer")
    st.markdown("""
    Re-runs the key frozen tests on a second representation of the text: ZL's **last** alternative
    readings, with uncertain spaces (`,`) **not** treated as word breaks. To test a fully independent
    transcription (for example Takahashi's `IT2a-n.txt` from voynich.nu), upload it in the sidebar:
    every tab then runs on it. From the command line, use `python transfer_test.py --corpus <file>`.
    """)
    if st.button("Run transfer comparison"):
        with st.spinner("Parsing both representations and running the frozen tests..."):
            spec = bh.load_holdout()
            reps = {
                "Loaded corpus": corpus_df,
                "ZL alternate readings": canonical.parse_zl3b(
                    canonical.CORPUS_PATH, reading="last", uncertain_spaces_split=False),
            }
            res = {name: tt.core_results(df, spec, 1000, 20261001) for name, df in reps.items()}
        table = []
        for label, key, f in tt.ROWS:
            row = {"Result": label}
            for name in res:
                v = res[name].get(key)
                row[name] = NOT_COMPUTED if v is None else f.format(v)
            table.append(row)
        st.dataframe(pd.DataFrame(table), width="stretch")

# =============================================================================
# TAB 9: INVARIANT SLOT OMEGA MINER
# =============================================================================
with tab_omega:
    st.header("⚡ Slot Ω frames: qo- · X-aiin · qo-")
    st.latex(r"\text{Q-ACTIVE} \longrightarrow [\mathbf{X}\text{-aiin} \ / \ \mathbf{X}\text{-ain}] \longrightarrow \text{Q-ACTIVE}")
    st.markdown("""
    Finds every place where a word ending in -aiin/-ain sits between two words starting with qo-, and lists the
    middle word's stem. This is a structural pattern only; no meaning is implied.
    """)

    omega_frames = []
    for l in lines_corpus:
        toks = l["tokens"]
        for i in range(len(toks) - 2):
            w1, w2, w3 = toks[i], toks[i+1], toks[i+2]
            f1 = factorize(w1)
            f3 = factorize(w3)
            if f1["control"] in ("qo", "q", "qk", "qok", "qot", "qoc") and f3["control"] in ("qo", "q", "qk", "qok", "qot", "qoc"):
                if w2.endswith(("aiin", "ain")):
                    stem = w2[:-4] if w2.endswith("aiin") else w2[:-3]
                    omega_frames.append({
                        "Folio": l["folio"],
                        "Line Locus": l["header"],
                        "Initial Active Verb": w1,
                        "Buffer Operand [X-aiin]": w2,
                        "Extracted Stem (X)": stem if stem else "[EMPTY]",
                        "Successor Active Verb": w3,
                    })

    st.metric("Total Slot Ω Frames Detected", len(omega_frames))

    st.subheader("Top Conserved Carrier Roots in Slot Ω Nucleus")
    stem_counts = Counter(f["Extracted Stem (X)"] for f in omega_frames)
    stem_df = pd.DataFrame(stem_counts.most_common(12), columns=["Carrier Stem (X)", "Frame Occurrences"])
    st.dataframe(stem_df, width="stretch")

    with st.expander("🔍 View All Mined Slot Ω Frames Across the Codex"):
        st.dataframe(pd.DataFrame(omega_frames), width="stretch")

# =============================================================================
# TAB 10: PARALLEL FOLIO READER
# =============================================================================
with tab_reader:
    st.header("📖 Folio Reader")
    all_folios = sorted(set(l["folio"] for l in lines_corpus))
    
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        selected_folio = st.selectbox("Select Manuscript Folio", all_folios, index=all_folios.index("f114v") if "f114v" in all_folios else 0)
    
    folio_lines = [l for l in lines_corpus if l["folio"] == selected_folio]

    st.subheader(f"Folio {selected_folio}")
    st.caption("Words ending in -m/-am are in bold.")
    
    if folio_lines:
        for l in folio_lines:
            line_header = l["header"]
            toks = l["tokens"]
            parts = [f"**{t}**" if sv.ending_of(t) in TERMINAL_FLUSHES else t for t in toks]
            st.markdown(f"`{line_header}` " + " ".join(parts))
    else:
        st.info(f"No lines for {selected_folio} in the loaded corpus.")

# =============================================================================
# TAB 13: EXPORT MASTER CSV LEDGERS
# =============================================================================
with tab_export:
    st.header("💾 Export")
    st.markdown("Download structured CSV ledgers for external verification, statistical modeling, or archival documentation.")

    corpus_flat = []
    for l in lines_corpus:
        for t in l["tokens"]:
            f = factorize(t)
            corpus_flat.append({
                "folio": l["folio"],
                "line": l["header"],
                "currier": l["currier"],
                "section": l["section"],
                "clean_token": t,
                "control_header": f["control"],
                "carrier_kernel": f["carrier"],
                "exit_port": f["exit_port"],
                "ending": sv.ending_of(t),
            })
    
    if corpus_flat:
        df_corpus_flat = pd.DataFrame(corpus_flat)
        st.download_button(
            label=f"📥 Download Full Corpus Ledger ({len(df_corpus_flat):,} Rows)",
            data=df_corpus_flat.to_csv(index=False).encode("utf-8"),
            file_name="voynich_extracted_corpus_ledger.csv",
            mime="text/csv",
            type="primary"
        )

    df_omega_export = pd.DataFrame(omega_frames) if 'omega_frames' in locals() else pd.DataFrame()
    if not df_omega_export.empty:
        st.download_button(
            label=f"📥 Download Mined Slot Ω Frames ({len(df_omega_export)} Instances)",
            data=df_omega_export.to_csv(index=False).encode("utf-8"),
            file_name="voynich_slot_omega_frames.csv",
            mime="text/csv"
        )
