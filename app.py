import io
import itertools
from collections import Counter
import random
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Canonical Parser Integration (Item 1)
from parser import (
    HOLDOUT_FOLIOS,
    VoynichParser,
    clean_raw_token,
    get_train_test_split,
    parse_zl3b,
)

st.set_page_config(
    page_title="Voynich Decipherment Workbench",
    page_icon="📜",
    layout="wide",
)

st.title("Voynich Decipherment Workbench")
st.caption(
    "Scientific audit pipeline: canonical morphology parsing, structural "
    "isolation, and non-parametric permutation verification."
)


# -----------------------------------------------------------------------------
# CORPUS INGESTION & CACHING (Items 1 & 2)
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Parsing canonical Voynich corpus (ZL3b-n)...")
def load_corpus_data():
    try:
        df = parse_zl3b()
        return df
    except Exception as e:
        st.error(f"Error loading canonical corpus: {e}")
        return pd.DataFrame()


corpus_df = load_corpus_data()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.header("Corpus & Evaluation Scope")

if corpus_df.empty:
    st.sidebar.warning("Corpus data is unavailable.")
    available_folios = []
else:
    available_folios = sorted(corpus_df["folio"].dropna().unique().tolist())

scope_option = st.sidebar.radio(
    "Analysis Target:",
    options=[
        "Full Corpus (Excluding Holdout)",
        "Strict Holdout Set Only",
        "Individual Folio Selection",
    ],
    index=0,
)

selected_folio = None
if scope_option == "Individual Folio Selection":
    default_idx = (
        available_folios.index("f70v2") if "f70v2" in available_folios else 0
    )
    selected_folio = st.sidebar.selectbox(
        "Select Folio:",
        available_folios,
        index=default_idx,
    )

# Filter corpus based on strict partition boundaries (Item 4)
if corpus_df.empty:
    active_df = pd.DataFrame()
elif scope_option == "Full Corpus (Excluding Holdout)":
    active_df = corpus_df[~corpus_df["is_holdout"]].copy()
elif scope_option == "Strict Holdout Set Only":
    active_df = corpus_df[corpus_df["is_holdout"]].copy()
else:
    active_df = corpus_df[corpus_df["folio"] == selected_folio].copy()

# -----------------------------------------------------------------------------
# MAIN APP TABS
# -----------------------------------------------------------------------------
tab_overview, tab_morphology, tab_tournament, tab_affix_tournament, tab_audit = st.tabs(
    [
        "📊 Corpus Overview",
        "🔬 Canonical Parser & States",
        "🎲 Semantic Tournament (Item 6)",
        "🧬 Affix-Role Tournament (Item 7)",
        "📋 Verification Audit Ledger",
    ]
)

# -----------------------------------------------------------------------------
# TAB 1: CORPUS OVERVIEW
# -----------------------------------------------------------------------------
with tab_overview:
    st.subheader("Corpus Partition & Inventory")

    if active_df.empty:
        st.info("No tokens available for the current selection.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Selected Tokens", f"{len(active_df):,}")
        col2.metric("Unique Folios", f"{active_df['folio'].nunique():,}")
        col3.metric(
            "Currier Dialects",
            ", ".join(
                [c for c in active_df["currier"].unique() if c != "UNKNOWN"]
            )
            or "N/A",
        )
        col4.metric(
            "Quarantined Holdout?",
            "YES (Zero-Leakage)"
            if active_df["is_holdout"].all()
            else ("NO" if not active_df["is_holdout"].any() else "Mixed"),
        )

        st.markdown("### Structural Class Distribution")
        state_counts = (
            active_df[active_df["state"] != "?"]["state"]
            .value_counts()
            .to_dict()
        )
        total_classified = sum(state_counts.values())

        if total_classified > 0:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(
                "Class C",
                f"{state_counts.get('C', 0):,} ({state_counts.get('C', 0)/total_classified:.1%})",
            )
            c2.metric(
                "Class L",
                f"{state_counts.get('L', 0):,} ({state_counts.get('L', 0)/total_classified:.1%})",
            )
            c3.metric(
                "Class P",
                f"{state_counts.get('P', 0):,} ({state_counts.get('P', 0)/total_classified:.1%})",
            )
            c4.metric(
                "Class R",
                f"{state_counts.get('R', 0):,} ({state_counts.get('R', 0)/total_classified:.1%})",
            )

        st.dataframe(
            active_df[
                [
                    "folio",
                    "currier",
                    "section",
                    "clean",
                    "control",
                    "carrier",
                    "exit_port",
                    "state",
                    "is_line_start",
                    "is_line_end",
                ]
            ].head(50),
            use_container_width=True,
        )

# -----------------------------------------------------------------------------
# TAB 2: CANONICAL PARSER & STATES (Item 1 & Item 5)
# -----------------------------------------------------------------------------
with tab_morphology:
    st.subheader("Canonical Morphological Token Breakdown")
    st.markdown(
        "Evaluate individual tokens against `VoynichParser` rules. Affixes are mapped "
        "directly into structural macrostates without subjective gloss overlays."
    )

    test_input = st.text_input(
        "Input single token or EVA string:",
        value="qokedy",
    )

    if test_input.strip():
        decomp = VoynichParser.decompose_morphology(test_input)
        col_res1, col_res2 = st.columns([1, 2])

        with col_res1:
            st.write("**Decomposition:**")
            st.json(decomp)

        with col_res2:
            st.markdown(f"**Clean Token:** `{decomp['clean']}`")
            st.markdown(f"**Prefix Control:** `{decomp['control']}`")
            st.markdown(f"**Carrier Core:** `{decomp['carrier']}`")
            st.markdown(f"**Exit Port:** `{decomp['exit_port']}`")
            st.markdown(f"**Macrostate Class:** `{decomp['state']}`")
            st.markdown(f"**Terminal Flush (-m):** `{decomp['is_terminal_m']}`")

# -----------------------------------------------------------------------------
# HELPER: CYCLE SCORE ENGINE
# -----------------------------------------------------------------------------
def calculate_cycle_score(states: list[str], cycle_map: dict[str, str]) -> float:
    if len(states) < 2:
        return 0.0
    hits = sum(
        1 for i in range(len(states) - 1)
        if cycle_map.get(states[i]) == states[i + 1]
    )
    return hits / (len(states) - 1)


# -----------------------------------------------------------------------------
# TAB 3: SEMANTIC PERMUTATION TOURNAMENT (Item 6)
# -----------------------------------------------------------------------------
with tab_tournament:
    st.subheader("Semantic Permutation Tournament (Item 6)")
    st.markdown(
        "Keeps every structural affix rule fixed and tests whether the proposed "
        "directed cycle ($C \\to L \\to P \\to R$) significantly outperforms all "
        "permutations of the structural state order."
    )

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        n_permutations = st.selectbox(
            "Permutation Count (Monte Carlo):",
            options=[1000, 5000, 10000, 15000],
            index=1,
            key="sem_perms",
        )
    with col_t2:
        random_seed = st.number_input(
            "Random Seed (Reproducibility):",
            value=42,
            step=1,
            key="sem_seed",
        )

    if st.button("Run Semantic Tournament", type="primary", key="btn_sem"):
        seq = [s for s in active_df["state"].tolist() if s in {"C", "L", "P", "R"}]

        if len(seq) < 10:
            st.warning("Insufficient classified tokens in selection to run tournament.")
        else:
            canonical_cycle = {"C": "L", "L": "P", "P": "R", "R": "C"}
            observed_score = calculate_cycle_score(seq, canonical_cycle)

            unique_states = ["C", "L", "P", "R"]
            all_perms = list(itertools.permutations(unique_states))

            np.random.seed(int(random_seed))
            null_scores = []

            for _ in range(n_permutations):
                p = all_perms[np.random.randint(0, len(all_perms))]
                mapping = dict(zip(unique_states, p))
                permuted_cycle = {mapping[k]: mapping[v] for k, v in canonical_cycle.items()}
                null_scores.append(calculate_cycle_score(seq, permuted_cycle))

            null_scores = np.array(null_scores)
            p_value = float(np.mean(null_scores >= observed_score))

            st.write("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("Observed Hypothesis Score", f"{observed_score:.4f}")
            m2.metric("Null Distribution Mean", f"{np.mean(null_scores):.4f}")
            m3.metric(
                "p-value",
                f"{p_value:.4f}",
                delta="Statistically Significant" if p_value < 0.05 else "Non-Significant",
                delta_color="normal" if p_value < 0.05 else "inverse",
            )

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(
                null_scores,
                bins=25,
                color="silver",
                edgecolor="black",
                label="Null Distribution",
            )
            ax.axvline(
                observed_score,
                color="red",
                linestyle="--",
                linewidth=2,
                label=f"Hypothesis ({observed_score:.4f})",
            )
            ax.set_xlabel("Transition Consistency Score")
            ax.set_ylabel("Frequency")
            ax.legend()
            st.pyplot(fig)

# -----------------------------------------------------------------------------
# TAB 4: AFFIX-ROLE PERMUTATION TOURNAMENT (Item 7)
# -----------------------------------------------------------------------------
with tab_affix_tournament:
    st.subheader("Affix-Role Permutation Tournament (Item 7)")
    st.markdown(
        "Tests whether the manuscript specifically selects the C-L-P-R affix grouping. "
        "Observed endings remain intact, but are randomly scrambled across the 4 structural "
        "classes thousands of times to determine if the canonical model produces an anomalously high transition score."
    )

    AFFIX_LIST = [
        "am", "m",                      # Canonical R
        "eedy", "edy", "eey", "ey", "dy", # Canonical C
        "ain", "aiin", "aiiin", "or", "ar", # Canonical L
        "ol", "al", "y"                 # Canonical P
    ]

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        n_affix_perms = st.selectbox(
            "Permutation Count (Monte Carlo):",
            options=[500, 1000, 2000, 5000],
            index=1,
            key="affix_perms",
        )
    with col_a2:
        affix_seed = st.number_input(
            "Random Seed:",
            value=42,
            step=1,
            key="affix_seed",
        )

    def classify_with_affixes(clean_tokens: list[str], affix_map: dict[str, str]) -> list[str]:
        assigned = []
        for t in clean_tokens:
            state = "?"
            for affix, st_code in affix_map.items():
                if affix == "m":
                    if re.search(r"(?<![ai])m$", t):
                        state = st_code
                        break
                elif t.endswith(affix) or t == affix:
                    state = st_code
                    break
            assigned.append(state)
        return assigned

    if st.button("Run Affix-Role Tournament", type="primary", key="btn_affix"):
        tokens = active_df["clean"].dropna().tolist()

        if len(tokens) < 10:
            st.warning("Insufficient tokens available to run affix tournament.")
        else:
            canonical_affix_map = {
                "am": "R", "m": "R",
                "eedy": "C", "edy": "C", "eey": "C", "ey": "C", "dy": "C",
                "ain": "L", "aiin": "L", "aiiin": "L", "or": "L", "ar": "L",
                "ol": "P", "al": "P", "y": "P",
            }
            canonical_cycle = {"C": "L", "L": "P", "P": "R", "R": "C"}

            # Canonical baseline
            canon_states = [s for s in active_df["state"].tolist() if s in {"C", "L", "P", "R"}]
            observed_score = calculate_cycle_score(canon_states, canonical_cycle)

            random.seed(int(affix_seed))
            np.random.seed(int(affix_seed))
            affix_null_scores = []
            progress_bar = st.progress(0)

            classes_pool = ["R", "R"] + ["C"] * 5 + ["L"] * 5 + ["P"] * 3

            for idx in range(n_affix_perms):
                shuffled_classes = classes_pool.copy()
                random.shuffle(shuffled_classes)
                perm_map = dict(zip(AFFIX_LIST, shuffled_classes))

                perm_seq = classify_with_affixes(tokens, perm_map)
                filt_perm_seq = [s for s in perm_seq if s in {"C", "L", "P", "R"}]
                affix_null_scores.append(calculate_cycle_score(filt_perm_seq, canonical_cycle))

                if (idx + 1) % max(1, n_affix_perms // 10) == 0:
                    progress_bar.progress((idx + 1) / n_affix_perms)

            progress_bar.empty()
            affix_null_scores = np.array(affix_null_scores)
            p_val_affix = float(np.mean(affix_null_scores >= observed_score))

            st.write("---")
            am1, am2, am3 = st.columns(3)
            am1.metric("Canonical Affix Score", f"{observed_score:.4f}")
            am2.metric("Null Affix Distribution Mean", f"{np.mean(affix_null_scores):.4f}")
            am3.metric(
                "p-value",
                f"{p_val_affix:.4f}",
                delta="Statistically Significant" if p_val_affix < 0.05 else "Non-Significant",
                delta_color="normal" if p_val_affix < 0.05 else "inverse",
            )

            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.hist(
                affix_null_scores,
                bins=25,
                color="cornflowerblue",
                edgecolor="black",
                label="Permuted Affix Null Distribution",
            )
            ax2.axvline(
                observed_score,
                color="red",
                linestyle="--",
                linewidth=2,
                label=f"Canonical Rules ({observed_score:.4f})",
            )
            ax2.set_xlabel("Transition Consistency Score")
            ax2.set_ylabel("Frequency")
            ax2.legend()
            st.pyplot(fig2)

# -----------------------------------------------------------------------------
# TAB 5: AUDIT LEDGER & ROADMAP STATUS (Items 1–5)
# -----------------------------------------------------------------------------
with tab_audit:
    st.subheader("Verification Roadmap Status")

    roadmap_data = [
        {"Item": 1, "Task": "Unify parser with canonical parser.py", "Status": "Complete"},
        {"Item": 2, "Task": "Remove numerical fallbacks & fake defaults", "Status": "Complete"},
        {"Item": 3, "Task": "Withdraw unanchored 99.79% historical claims", "Status": "Withdrawn / Pending Real Corpus Ingestion"},
        {"Item": 4, "Task": "Quarantine 5-folio holdout from training metrics", "Status": "Enforced in Sidebar Partitions"},
        {"Item": 5, "Task": "Strip linguistic interpretations (pure C-L-P-R)", "Status": "Complete (Abstract Macrostates Only)"},
        {"Item": 6, "Task": "Semantic permutation tournament", "Status": "Complete (Tab 3)"},
        {"Item": 7, "Task": "Affix-role permutation tournament", "Status": "Complete (Tab 4)"},
        {"Item": 8, "Task": "Multifactorial structural checks (lines/currier)", "Status": "Pending Next Implementation"},
        {"Item": 9, "Task": "Independent external transfer test (Currier/Takahashi)", "Status": "Pending Next Implementation"},
        {"Item": 10, "Task": "Replication packaging (Standalone CLI/Docker)", "Status": "Pending Next Implementation"},
    ]

    st.table(pd.DataFrame(roadmap_data))
