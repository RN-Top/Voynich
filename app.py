"""
Voynich Manuscript Decipherment Engine & Dual-Dialect Workbench
Author: Voynich Decipherment Working Group (RN-Top/Voynich)
Corpus Standard: IVTFF EVA 2.0 / ZL3b-n Standard
Dependencies: streamlit, pandas, numpy

Every number displayed by this app is computed from the currently loaded
corpus. When a value cannot be computed it is shown as "not computed";
there are no numerical fallbacks. Tokenisation and morphology come from
the canonical parser in parser.py.
"""

import json
from collections import Counter, defaultdict
import numpy as np
import pandas as pd
import streamlit as st

import parser as canonical
import structural_validation as sv
from lexicon import MASTER_LEXICON

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

PREFIXES = ("qo", "ch", "sh", "da", "ot", "cth", "y", "sa")
SUFFIXES = ("edy", "aiin", "iin", "ey", "ol", "or", "ar", "al", "y")

QUARANTINED_FOLIOS = list(canonical.HOLDOUT_FOLIOS)
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

def predict_apparatus_role(token: str) -> str:
    parsed = VoynichParser.parse(token)
    tok = parsed["clean"]
    ctrl = parsed["control"]
    port = parsed["exit_port"]
    
    if ctrl in ("qo", "qok", "qot"):
        return "heat"
    if parsed["is_terminal_m"] or tok.endswith(("am", "aim", "daim")):
        return "drain"
    if port in ("aiin", "ain") or tok.endswith(("aiin", "ain")):
        return "medium"
    if port in ("al", "ar") or tok.endswith(("al", "ar", "eos")):
        return "outlet"
    if port in ("y", "dy") or any(tok.endswith(s) for s in ("y", "dy", "eey", "eody", "ey", "edy")):
        return "reflux"
    return "outlet" if "al" in tok or "ar" in tok else "medium"

def get_expected_role(folio: str, token: str) -> str:
    tok = clean_raw_token(token)
    outlet_keywords = ("otal", "arar", "ar", "lar", "tar", "al", "keodar", "eos", "okydy", "otaly", "otald", "okeol", "okeoly", "daiiamd")
    medium_keywords = ("aiin", "ain", "alain", "daiin", "dain")
    drain_keywords = ("am", "tam", "eeam", "ypaim", "otam", "karam", "alam")
    heat_keywords = ("qokar", "qokedy", "qok", "qo")

    if any(k in tok for k in drain_keywords) or tok.endswith(("am", "aim", "m")):
        return "drain"
    if any(tok.startswith(k) for k in heat_keywords):
        return "heat"
    if any(tok == k or tok.endswith(k) for k in medium_keywords):
        return "medium"
    if any(k in tok for k in outlet_keywords):
        return "outlet"
    return "reflux"

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
    st.markdown("### Directional Routing")
    st.markdown(f"## Δ = {fmt(dir_delta, '.3f')}")
    st.caption("↑ log-odds of k-/d- successor after -al vs -ar")

st.markdown("---")

# -----------------------------------------------------------------------------
# WORKBENCH NAVIGATION TABS
# -----------------------------------------------------------------------------
(
    tab_paper,
    tab_holdout,
    tab_parser,
    tab_transition_tourney,
    tab_semantic_tourney,
    tab_affix_tourney,
    tab_dialect,
    tab_tests,
    tab_omega,
    tab_reader,
    tab_lexicon,
    tab_colophons,
    tab_export,
) = st.tabs([
    "📄 Academic Paper",
    "🎯 Holdout Permutation Audit",
    "🔬 Canonical Token Breakdown",
    "📊 Macrostate Transition Consistency",
    "🎲 Semantic Tournament (Item 6)",
    "⚔️ Affix-Role Tournament",
    "🏛️ Dual-Dialect Bridge",
    "🧪 Automated Verification Suite",
    "⚡ Invariant Slot Ω Miner",
    "📖 Parallel Folio Reader",
    "📚 Grounded Master Lexicon",
    "🖋️ Author & Colophon Audit",
    "💾 Export Master CSV Ledgers",
])

# =============================================================================
# TAB 1: ACADEMIC PAPER & EVIDENCE COMPENDIUM
# =============================================================================
with tab_paper:
    st.header("A Dual-Dialect Compounding Architecture for Beinecke MS 408: Romance Morphophonology & Germanic Procedural Syntax")
    st.markdown("""
    **Authors:** Voynich Decipherment Working Group  
    **Archive Reference:** Beinecke Rare Book and Manuscript Library, Yale University, MS 408  
    **Corpus Standard:** Standardized Interlinear Voynich Transliteration File Format (IVTFF) EVA 2.0 / ZL3b-n standard  
    """)
    st.markdown("---")
    
    st.subheader("1. Executive Summary & Verification Milestones")
    st.markdown("""
    For more than six centuries, Beinecke MS 408 has resisted cryptanalysis due to persistent attempts to force arbitrary 
    monoalphabetic substitution ciphers or subjective anagrams onto its text. This paper documents the dual-dialect computational 
    architecture: a **Northern Italian / Venetian Romance phonetic sound inventory** coupled with an **Early New High German 
    procedural compounding syntax**.
    """)
    
    st.warning(
        "**Independent review (September 2026).** An external nine-step validation found real, "
        "non-random positional morphology (strongest: line-final -m/-am), but did **not** establish "
        "the four-state C→L→P→R machine beyond Markov controls, the Venetian/German semantics, the "
        "90.2% blind-prediction figure (its holdout folios were already in the project's seen set), "
        "or the Macer Floridus alignment (its target vectors were random). The status column below "
        "reflects that review; see VALIDATION.md and `python structural_validation.py`."
    )

    scorecard_data = {
        "Verification Gate": [
            "Blind Stem-Context Prediction",
            "A1: Currier Dialect Separation",
            "A2: Buffer Flushing (-m / -am)",
            "A4: Successor Directional Routing",
            "Lexical Core Normalization (Λ)",
            "80/20 Holdout Generalization",
            "Diagram Prefix Suppression (qo-)",
            "Procrustes Manifold Alignment",
            "Sukhotin Phonological Vowels",
        ],
        "Originally Reported": [
            "90.2% Accuracy (394/437 hits)",
            "98.49% Balanced Accuracy",
            "69.37% - 73.0% Line-Terminal",
            "Δ = -1.018 log-odds shift",
            "Zipf α = 1.065 (70.84% red.)",
            "Test PMI = 31.274 (45 folios)",
            "0.0% qo- on Rotas / Plants",
            "d² = 0.0021 (99.79% Match)",
            "33.3% Vocalic Ratio (6/14)",
        ],
        "Live Value (this corpus)": [
            "see Holdout tab",
            NOT_COMPUTED,
            f"{fmt(flush['pct'], '.1f')}% ({flush['m_end']}/{flush['total_m']})",
            f"Δ = {fmt(dir_delta, '.3f')}",
            NOT_COMPUTED,
            NOT_COMPUTED,
            "see Verification Suite tab",
            NOT_COMPUTED,
            NOT_COMPUTED,
        ],
        "Status After Independent Review": [
            "WITHDRAWN as blind test: holdout folios are in SEEN_FOLIOS; score compares two suffix rule sets",
            "Not re-tested",
            "SUPPORTED as positional structure; functional meaning ('flush') not established",
            "Not re-tested",
            "Not re-tested",
            "Not re-tested",
            "Not re-tested",
            "WITHDRAWN: target vectors were np.random.randn(); no Macer Floridus corpus used",
            "Not re-tested",
        ],
    }
    st.dataframe(pd.DataFrame(scorecard_data), use_container_width=True)

    st.subheader("2. The Token Factorization Formula")
    st.latex(r"W = \mathcal{C}\big([\Lambda \times N_E \times O_I] + \rho\big)")
    st.markdown("""
    * **Control Header Operator ($\mathcal{C} \in \{d, q, k, t\}$):** Positional line-entry and runtime execution operators.
    * **Carrier Kernel / Operand Core ($\Lambda$):** Stable lexical stems preserving entity specificity across changing syntactic environments.
    * **Internal Tuning Registers ($N_E \times O_I$):** Iterative feature counters parameterizing $E$-multiplicity and internal $O$-presence.
    * **Exit Ports / Successor Routers ($\rho \in \{y, ar, al, aiin, m\}$):** Interface realization suffixes parameterizing transitions into the subsequent token header.
    """)

# =============================================================================
# TAB 2: HOLDOUT PERMUTATION AUDIT
# =============================================================================
with tab_holdout:
    st.header("🎯 Holdout Permutation Audit")

    seen_overlap = sorted(set(QUARANTINED_FOLIOS) & sv.SEEN_FOLIOS)
    if seen_overlap:
        st.error(
            "**Not a clean blind test.** These holdout folios are also listed in the project's "
            f"SEEN_FOLIOS (used for dossier recipes / cribs): {', '.join(seen_overlap)}. "
            "In addition, `predict_apparatus_role` and `get_expected_role` are both suffix rules "
            "applied to the same token string, so their agreement measures rule overlap, not "
            "prediction of independent ground truth."
        )

    holdout_tokens = []
    for l in lines_corpus:
        if l["folio"] in QUARANTINED_FOLIOS:
            for tok in l["tokens"]:
                parsed = VoynichParser.parse(tok)
                pred = predict_apparatus_role(tok)
                exp = get_expected_role(l["folio"], tok)
                holdout_tokens.append({
                    "folio": l["folio"],
                    "token": tok,
                    "carrier": parsed["carrier_core"],
                    "predicted": pred,
                    "expected": exp,
                    "match": pred == exp,
                })

    if not holdout_tokens:
        st.info(f"Holdout folios not present in the loaded corpus: {NOT_COMPUTED}.")
    else:
        total_loci = len(holdout_tokens)
        hits = sum(1 for x in holdout_tokens if x["match"])
        obs_acc = hits / total_loci * 100

        # Chance agreement: shuffle predicted labels against expected labels.
        rng = np.random.default_rng(42)
        pred_arr = np.array([x["predicted"] for x in holdout_tokens])
        exp_arr = np.array([x["expected"] for x in holdout_tokens])
        null = np.array([np.mean(rng.permutation(pred_arr) == exp_arr) * 100 for _ in range(5000)])
        null_mean, null_sd = float(null.mean()), float(null.std())
        p_val = float((np.sum(null >= obs_acc) + 1) / (len(null) + 1))
        z_val = (obs_acc - null_mean) / null_sd if null_sd > 0 else None

        h_col1, h_col2, h_col3, h_col4 = st.columns(4)
        with h_col1:
            st.markdown("### Scored Tokens")
            st.markdown(f"## {total_loci} Loci")
            st.caption("↑ " + ", ".join(QUARANTINED_FOLIOS))
        with h_col2:
            st.markdown("### Rule Agreement")
            st.markdown(f"## {obs_acc:.1f}%")
            st.caption(f"↑ {hits} / {total_loci} matches")
        with h_col3:
            st.markdown("### Shuffled Baseline")
            st.markdown(f"## {null_mean:.1f}%")
            st.caption(f"↑ ± {null_sd:.1f}% (5,000 label shuffles)")
        with h_col4:
            st.markdown("### Empirical p-value")
            st.markdown(f"## {p_val:.4f}")
            st.caption(f"↑ Z = {fmt(z_val, '.2f')}σ")

        st.subheader("Holdout Token Verification Ledger")
        st.dataframe(pd.DataFrame(holdout_tokens), use_container_width=True)

# =============================================================================
# TAB 3: CANONICAL TOKEN BREAKDOWN (VOYNICHPARSER INSPECTOR)
# =============================================================================
with tab_parser:
    st.header("Canonical Morphological Token Breakdown")
    st.markdown("""
    Evaluate individual tokens against `VoynichParser` rules. Affixes are mapped directly into 
    structural macrostates without subjective gloss overlays.
    """)

    sample_token_input = st.text_input("Input single token or EVA string:", value="qokedy")
    
    if sample_token_input:
        breakdown = VoynichParser.parse(sample_token_input)
        
        st.subheader("Decomposition:")
        st.code(json.dumps(breakdown, indent=2), language="json")
        
        c_k1, c_k2, c_k3 = st.columns(3)
        c_k1.markdown(f"**Clean Token:** `{breakdown['clean']}`")
        c_k1.markdown(f"**Prefix Control:** `{breakdown['control']}`")
        
        c_k2.markdown(f"**Carrier Core:** `{breakdown['carrier_core']}`")
        c_k2.markdown(f"**Exit Port:** `{breakdown['exit_port']}`")
        
        c_k3.markdown(f"**Macrostate Class:** `{breakdown['state']}`")
        c_k3.markdown(f"**Terminal Flush (-m):** `{breakdown['is_terminal_m']}`")

# =============================================================================
# SHARED: STRUCTURAL VALIDATION CORPUS (structural_validation.py)
# =============================================================================
@st.cache_data(show_spinner=False)
def validation_corpus(df: pd.DataFrame, paragraph_only: bool):
    sub = df[df["locus_type"] == "P"] if paragraph_only else df
    return sv.Corpus(sub)


def validation_controls(key: str):
    c1, c2, c3 = st.columns(3)
    perms = c1.number_input("Permutations", min_value=500, max_value=50000, value=5000, step=500, key=f"{key}_perms")
    seed = c2.number_input("Seed", value=42, step=1, key=f"{key}_seed")
    para = c3.checkbox("Paragraph text only (exclude labels / rings / radii)", value=True, key=f"{key}_para")
    return int(perms), int(seed), para


# =============================================================================
# TAB 4: MACROSTATE TRANSITION CONSISTENCY TOURNAMENT (C -> L -> P -> R)
# =============================================================================
with tab_transition_tourney:
    st.header("📊 Macrostate Transition Consistency Tournament")
    st.markdown(r"""
    Does the order $C \to L \to P \to R$ occur more often than expected? The statistic is the share of
    adjacent within-line state pairs that follow the cycle (pair score), plus the share of 4-token windows
    that run a full cycle step. Three nulls: within-line shuffle, and Markov-1 / Markov-2 twins that
    preserve the lower-order dependencies already present in Voynichese.
    """)
    n_sims, t_seed, t_para = validation_controls("trans")
    n_twins = st.number_input("Markov twins", min_value=100, max_value=5000, value=500, step=100)

    if st.button("Execute Transition Consistency Analysis", type="primary"):
        corpus_v = validation_corpus(corpus_df, t_para)
        with st.spinner("Generating null distributions..."):
            res = sv.test_cycle_nulls(corpus_v, n_sims, int(n_twins), np.random.default_rng(t_seed))
            ranks = sv.test_order_tournament(corpus_v, str(t_seed))

        tc1, tc2 = st.columns(2)
        tc1.metric("Observed pair score", f"{res['observed']['pair_score']:.4f}")
        tc2.metric("Observed 4-window cycle rate", f"{res['observed']['cycle4_rate']:.5f}")
        rows = [
            {
                "Null model": name,
                "n": res[name]["n"],
                "Pair-score null mean": round(res[name]["pair_null_mean"], 4),
                "Pair p": res[name]["pair_p"],
                "4-window null mean": round(res[name]["cycle4_null_mean"], 5),
                "4-window p": res[name]["cycle4_p"],
            }
            for name in ("within_line_shuffle", "markov1_twins", "markov2_twins")
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        st.caption("A Markov-1 twin reproduces the bigram table by construction, so only the 4-window "
                   "score can show structure beyond adjacent pairs.")

        st.subheader("State-order tournament (rank of C→L→P→R)")
        st.dataframe(pd.DataFrame([
            {"Split": k, "Tokens": v["tokens"], "Linear rank (of 24)": v["linear_rank_of_CLPR"],
             "Cyclic rank (of 6)": v["cyclic_rank_of_CLPR"],
             "Top linear orders": ", ".join(f"{o} ({n})" for o, n in v["linear_top3"])}
            for k, v in ranks.items()
        ]), use_container_width=True)

# =============================================================================
# TAB 5: SEMANTIC PERMUTATION TOURNAMENT (ITEM 6)
# =============================================================================
with tab_semantic_tourney:
    st.subheader("Item 6: Semantic Permutation Tournament")
    st.markdown("""
    The structural rules stay fixed; the published glosses (domains in `lexicon.py`) are shuffled among
    the glossed tokens. If the published assignment is right, it should place tokens in the manuscript
    section its meaning predicts better than shuffled assignments do. The domain → section map is
    pre-registered in `structural_validation.DOMAIN_EXPECTED_SECTIONS`.
    """)
    sem_perms, sem_seed, sem_para = validation_controls("sem")

    if st.button("Execute Semantic Permutation Tournament", type="primary"):
        res = sv.test_semantic_permutation(validation_corpus(corpus_df, sem_para), sem_perms, np.random.default_rng(sem_seed))
        if res.get("status") == NOT_COMPUTED:
            st.info(f"{NOT_COMPUTED}: {res['reason']}")
        else:
            sm1, sm2, sm3, sm4 = st.columns(4)
            sm1.metric("Published-gloss section hit rate", f"{res['observed_section_hit_rate']:.1%}")
            sm2.metric("Shuffled-gloss mean", f"{res['null_mean']:.1%}")
            sm3.metric("Shuffled-gloss SD", f"{res['null_sd']:.1%}")
            sm4.metric("Empirical p-value", f"{res['p']:.4f}")
            st.dataframe(pd.DataFrame(res["per_token"]), use_container_width=True)
            st.caption(res["note"])

# =============================================================================
# TAB 6: AFFIX-ROLE TOURNAMENT
# =============================================================================
with tab_affix_tourney:
    st.subheader("Affix-Role Tournament")
    st.markdown("""
    The observed endings stay untouched; which ending belongs to which of the four states (C/L/P/R) is
    shuffled, keeping group sizes. Each shuffled grouping gets its best of the six possible cycles. If the
    manuscript specifically selects the published role map, it should beat most shuffled groupings.
    """)
    af_perms, af_seed, af_para = validation_controls("affix")

    if st.button("Run Affix-Role Tournament"):
        with st.spinner("Executing role-map permutations..."):
            res = sv.test_affix_role(validation_corpus(corpus_df, af_para), af_perms, np.random.default_rng(af_seed))
        res1, res2, res3, res4 = st.columns(4)
        res1.metric("Published map best-cycle score", f"{res['observed_best_cycle_score']:.4f}", res["observed_best_cycle"])
        res2.metric("Shuffled maps mean", f"{res['null_mean']:.4f}")
        res3.metric("Shuffled maps SD", f"{res['null_sd']:.4f}")
        res4.metric("Empirical p-value", f"{res['p']:.4f}")
        if res["parser_consistency_mismatches"]:
            st.error(f"Ending map disagrees with parser.map_macrostate on {res['parser_consistency_mismatches']} tokens.")

# =============================================================================
# TAB 7: DUAL-DIALECT BRIDGE TEST
# =============================================================================
with tab_dialect:
    st.header("🏛 Dual-Dialect Linguistic Bridge Test")
    st.markdown("""
    Evaluating the linguistic divergence of Beinecke MS 408 across two historical technical traditions:
    **Northern Italian / Venetian Trade Apothecary** vs. **Early New High German Distillation Compendia**.
    """)

    all_chars = Counter("".join(corpus_df["clean"]))
    n_chars = sum(all_chars.values())
    h1 = -sum(c / n_chars * np.log2(c / n_chars) for c in all_chars.values()) if n_chars else None
    pairs = [(a, b) for l in lines_corpus for a, b in zip(l["tokens"][:-1], l["tokens"][1:])]
    doubling = sum(a == b for a, b in pairs) / len(pairs) * 100 if pairs else None

    st.caption(
        "The Venetian and German columns are reference values supplied by the author; the comparison "
        "texts are not in this repository, so those figures cannot be recomputed here. The Voynich "
        "column is computed live where possible."
    )
    test_metrics = [
        {"Statistical Dimension": "1. Character Entropy (H1)", "Whole Voynich": f"{fmt(h1, '.2f')} bits", "Venetian (1420)": "4.09 bits", "Early German": "4.06 bits"},
        {"Statistical Dimension": "2. Immediate Word Doubling", "Whole Voynich": f"{fmt(doubling, '.2f')}%", "Venetian (1420)": "0.00%", "Early German": "0.00%"},
        {"Statistical Dimension": "3. Line-Terminal -m / -am", "Whole Voynich": f"{fmt(flush['pct'], '.1f')}%", "Venetian (1420)": "8.2%", "Early German": "7.4%"},
        {"Statistical Dimension": "4. Compounding Transition Order", "Whole Voynich": "C -> L -> P -> R (not beyond Markov controls)", "Venetian (1420)": "Verb -> Direct Object", "Early German": "Substrate -> Verb-Final"},
        {"Statistical Dimension": "5. Phonetic Consonant-Vowel Partition", "Whole Voynich": NOT_COMPUTED, "Venetian (1420)": "34.1% Vowels", "Early German": "29.8% Vowels"},
    ]
    st.dataframe(pd.DataFrame(test_metrics), use_container_width=True)

    st.subheader("Dual-Dialect Translation Alignment")
    sample_dialect_lines = [
        {
            "Locus": "f114v.4",
            "Voynich Original": "qokedy cheocthedy qoted chedar okeedy daiin chedaiin oky chdam",
            "Venetian Trade Apothecary": "coci fraturo de erba scalda fiori d'erba incorpora agva decocto d'erba saldo",
            "Early New High German": "sied kruttheil waerme bluemen menge wazzer krutwazzer beschliess",
            "Operational English Reading": "Boil the plant fraction, warm the blossoms, compound with water menstruum and herb decoction, and seal the vessel."
        },
        {
            "Locus": "f114v.21",
            "Voynich Original": "qokedy otcheodaiin qokchdy",
            "Venetian Trade Apothecary": "coci licore de stella coci_qokchdy",
            "Early New High German": "sied sternauszug sied_qokchdy",
            "Operational English Reading": "Heat the astronomical sector component and proceed immediately into active secondary boiling."
        },
        {
            "Locus": "f1r.6",
            "Voynich Original": "okchoy otchol chocthy ydaraishy chdam",
            "Venetian Trade Apothecary": "coci_okchoy colato_otchol materia_chocthy fatto da l'auctor saldo",
            "Early New High German": "sied_okchoy auszug_otchol stoff_chocthy gemacht von meister beschliess",
            "Operational English Reading": "Tempered under warmth to produce herbal compound; composed by the author; vessel sealed."
        },
        {
            "Locus": "f116v.1",
            "Voynich Original": "oror sheey",
            "Venetian Trade Apothecary": "fin / saldo stasi",
            "Early New High German": "ende / bschluss ruhe",
            "Operational English Reading": "Terminal execution closure achieved. System at rest. Finis."
        }
    ]
    st.dataframe(pd.DataFrame(sample_dialect_lines), use_container_width=True)
    st.caption("Illustrative readings generated from the hypothesised gloss dictionary. "
               "The glosses have not been independently validated (see Semantic Tournament tab).")

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

            transitions = defaultdict(int)
            for l in lines_corpus:
                states = [factorize(t)["state"] for t in l["tokens"]]
                for i in range(len(states) - 1):
                    s1, s2 = states[i], states[i+1]
                    if s1 != "?" and s2 != "?":
                        transitions[f"{s1} -> {s2}"] += 1

            st.success("✅ Verification suite executed on the loaded corpus.")

            c1, c2, c3 = st.columns(3)
            c1.metric("A2: Line-Terminal -m / -am Rate", f"{fmt(flush['pct'], '.1f')}%",
                      f"{flush['m_end']}/{flush['total_m']} tokens · OR {fmt(flush['odds_ratio'], '.1f')}")
            c2.metric("Diagram qo- Rate (labels, rings, radii)", f"{fmt(diag_rate, '.2f')}%",
                      f"{diagram_qo}/{len(diagram_toks)} (vs {fmt(prose_rate, '.1f')}% paragraph text)")
            c3.metric("A4: Directional Routing Shift", f"{fmt(log_odds_delta, '.3f')} log-odds")

            st.subheader("4-Macrostate Sequential Transitions")
            if transitions:
                t_list = [{"Transition Cycle": k, "Occurrences": int(v)} for k, v in transitions.items()]
                t_df = pd.DataFrame(t_list).sort_values(by="Occurrences", ascending=False)
                st.dataframe(t_df, use_container_width=True)
            else:
                st.info(f"Transitions: {NOT_COMPUTED} (no adjacent classified tokens).")

# =============================================================================
# TAB 9: INVARIANT SLOT OMEGA MINER
# =============================================================================
with tab_omega:
    st.header("⚡ Canonical Slot Ω Execution Frame Mining")
    st.latex(r"\text{Q-ACTIVE} \longrightarrow [\mathbf{X}\text{-aiin} \ / \ \mathbf{X}\text{-ain}] \longrightarrow \text{Q-ACTIVE}")
    st.markdown("""
    The Slot $\Omega$ sandwich isolates an interchangeable content-operand class restricted to specific carrier stems 
    ($X \in \{\text{ched}, \text{cheod}, \text{shed}, \text{lk}, \text{r}\}$). The realization port `-aiin` functions as a relational 
    liquid buffer holding the nominal state between active operational operators.
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
    st.dataframe(stem_df, use_container_width=True)

    with st.expander("🔍 View All Mined Slot Ω Frames Across the Codex"):
        st.dataframe(pd.DataFrame(omega_frames), use_container_width=True)

# =============================================================================
# TAB 10: PARALLEL FOLIO READER
# =============================================================================
with tab_reader:
    st.header("📖 Parallel Interlinear Manuscript Reader")
    all_folios = sorted(set(l["folio"] for l in lines_corpus))
    
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        selected_folio = st.selectbox("Select Manuscript Folio", all_folios, index=all_folios.index("f114v") if "f114v" in all_folios else 0)
    
    folio_lines = [l for l in lines_corpus if l["folio"] == selected_folio]

    st.subheader(f"Folio {selected_folio} Execution Trace")
    
    if folio_lines:
        for l in folio_lines:
            line_header = l["header"]
            toks = l["tokens"]
            gloss_parts = []
            for t in toks:
                f = factorize(t)
                if t in MASTER_LEXICON:
                    entry = MASTER_LEXICON[t]
                    gloss_parts.append(f"**{t}** [{entry['en']}, {entry['role']}]")
                else:
                    gloss_parts.append(f"{t} [{f['state']}]")
            st.markdown(f"**{line_header}:** " + " · ".join(gloss_parts))
    else:
        st.info(f"No lines for {selected_folio} in the loaded corpus.")

# =============================================================================
# TAB 11: GROUNDED MASTER LEXICON
# =============================================================================
with tab_lexicon:
    st.header("📚 Grounded Master Lexicon & Syntactic Map")
    st.warning("These glosses are hypotheses. They have not been validated against the manuscript or against a historical corpus: the earlier Macer Floridus alignment used random target vectors and has been withdrawn, and the semantic permutation tournament does not currently favour these assignments over shuffled ones.")

    lex_rows = []
    for tok, info in MASTER_LEXICON.items():
        f = factorize(tok)
        lex_rows.append({
            "Voynich Token": tok,
            "Carrier Root (Λ)": f["carrier"],
            "15th-C. Latin Lemma": info["la"],
            "Venetian Apothecary": info["ven"],
            "Early High German": info["ger"],
            "English Gloss": info["en"],
            "Syntactic Role Class": info["role"],
            "Semantic Domain": info["domain"],
            "Realization Port (ρ)": f["exit_port"],
        })
    st.dataframe(pd.DataFrame(lex_rows), use_container_width=True)

# =============================================================================
# TAB 12: AUTHOR & COLOPHON AUDIT
# =============================================================================
with tab_colophons:
    st.header("🖋️ Codicological Colophons & Attribution Audit")
    st.markdown("""
    The Voynich Manuscript contains isolated structural loci functioning as scribal colophons, incipits, and signatures 
    that systematically diverge from continuous compounding prose.
    """)

    targets = ["ydaraishy", "ytchas", "oror"]
    audit_matches = []
    for l in lines_corpus:
        for t in l["tokens"]:
            for target in targets:
                if target in t:
                    audit_matches.append({
                        "Target Lemma": target,
                        "Folio": l["folio"],
                        "Line Locus": l["header"],
                        "Matched Token": t,
                        "Currier Dialect": l["currier"],
                        "Functional Assignment": MASTER_LEXICON.get(target, {}).get("en", "Colophon Marker")
                    })
    
    if not audit_matches:
        st.info("None of the target tokens occur in the loaded corpus.")

    st.subheader("Audited Authorial & Scribal Signatures")
    st.dataframe(pd.DataFrame(audit_matches), use_container_width=True)

    st.markdown("""
    ### Structural Significance
    1. **`ydaraishy` ($f1r.6$, locus `=Pt`):** Positioned at the conclusion of the manuscript's opening incipit paragraph. Demonstrates exact syntactic isolation, serving as an authorial signature anchored to Latin *auctor*.
    2. **`ytchas` ($f9r.10$, locus `+Pc`):** Indented paragraph-tail colophon closing the first gathering, matching scribal colophon formulas (anchored to Latin *scriptor*).
    3. **`oror.sheey` ($f116v.1$, locus `@Lx`):** Hard terminal seal marking the complete cessation of the compilation (anchored to Latin *finis*).
    """)

# =============================================================================
# TAB 13: EXPORT MASTER CSV LEDGERS
# =============================================================================
with tab_export:
    st.header("💾 Export Master Scientific Ledgers")
    st.markdown("Download structured CSV ledgers for external verification, statistical modeling, or archival documentation.")

    corpus_flat = []
    for l in lines_corpus:
        for t in l["tokens"]:
            f = factorize(t)
            lex = MASTER_LEXICON.get(t, {})
            corpus_flat.append({
                "folio": l["folio"],
                "line": l["header"],
                "currier": l["currier"],
                "section": l["section"],
                "clean_token": t,
                "control_header": f["control"],
                "carrier_kernel": f["carrier"],
                "exit_port": f["exit_port"],
                "macrostate": f["state"],
                "latin_lemma": lex.get("la", "unmapped"),
                "venetian_apothecary": lex.get("ven", "unmapped"),
                "early_high_german": lex.get("ger", "unmapped"),
                "english_gloss": lex.get("en", "unmapped"),
                "role_class": lex.get("role", "unmapped"),
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

    df_lex_export = pd.DataFrame(lex_rows) if 'lex_rows' in locals() else pd.DataFrame()
    if not df_lex_export.empty:
        st.download_button(
            label=f"📥 Download Master Lexicon CSV ({len(df_lex_export)} Terms)",
            data=df_lex_export.to_csv(index=False).encode("utf-8"),
            file_name="voynich_derived_dictionary.csv",
            mime="text/csv"
        )

    df_omega_export = pd.DataFrame(omega_frames) if 'omega_frames' in locals() else pd.DataFrame()
    if not df_omega_export.empty:
        st.download_button(
            label=f"📥 Download Mined Slot Ω Frames ({len(df_omega_export)} Instances)",
            data=df_omega_export.to_csv(index=False).encode("utf-8"),
            file_name="voynich_slot_omega_frames.csv",
            mime="text/csv"
        )
