import io
import itertools
from collections import Counter

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
tab_overview, tab_morphology, tab_tournament, tab_audit = st.tabs(
    [
        "📊 Corpus Overview",
        "🔬 Canonical Parser & States",
        "🎲 Permutation Tournament",
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
                "Class C (Cycle / Heat)",
                f"{state_counts.get('C', 0):,} ({state_counts.get('C', 0)/total_classified:.1%})",
            )
            c2.metric(
                "Class L (Liquid / Medium)",
                f"{state_counts.get('L', 0):,} ({state_counts.get('L', 0)/total_classified:.1%})",
            )
            c3.metric(
                "Class P (Phlegm / Retain)",
                f"{state_counts.get('P', 0):,} ({state_counts.get('P', 0)/total_classified:.1%})",
            )
            c4.metric(
                "Class R (Release / Outlet)",
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
# TAB 3: SEMANTIC PERMUTATION TOURNAMENT (Item 6 & Item 7)
# -----------------------------------------------------------------------------
with tab_tournament:
    st.subheader("Semantic Permutation Tournament")
    st.markdown(
        "Tests whether the observed sequence of states significantly adheres to a directed "
        "cycle ($C \\to L \\to P \\to R$) compared to null permutations of state definitions."
    )

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        n_permutations = st.selectbox(
            "Permutation Count (Monte Carlo):",
            options=[1000, 5000, 10000, 15000],
            index=1,
        )
    with col_t2:
        random_seed = st.number_input(
            "Random Seed (Reproducibility):",
            value=42,
            step=1,
        )

    # Transition tracking helper
    def calculate_cycle_score(states: list[str], cycle_map: dict[str, str]) -> float:
        if len(states) < 2:
            return 0.0
        hits = sum(
            1 for i in range(len(states) - 1)
            if cycle_map.get(states[i]) == states[i + 1]
        )
        return hits / (len(states) - 1)

    if st.button("Run Permutation Tournament", type="primary"):
        seq = [s for s in active_df["state"].tolist() if s in {"C", "L", "P", "R"}]

        if len(seq) < 10:
            st.warning("Insufficient classified tokens in selection to run tournament.")
        else:
            canonical_cycle = {"C": "L", "L": "P", "P": "R", "R": "C"}
            observed_score = calculate_cycle_score(seq, canonical_cycle)

            # Generate all possible derangements / state assignment maps
            unique_states = ["C", "L", "P", "R"]
            all_perms = list(itertools.permutations(unique_states))

            np.random.seed(random_seed)
            null_scores = []

            for _ in range(n_permutations):
                # Pick a random reassignment of the 4 structural classes
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
# TAB 4: AUDIT LEDGER & ROADMAP STATUS (Items 2, 3, 4)
# -----------------------------------------------------------------------------
with tab_audit:
    st.subheader("Verification Roadmap Status")

    roadmap_data = [
        {"Item": 1, "Task": "Unify parser with canonical parser.py", "Status": "Complete"},
        {"Item": 2, "Task": "Remove numerical fallbacks & fake defaults", "Status": "Complete"},
        {"Item": 3, "Task": "Withdraw unanchored 99.79% historical claims", "Status": "Withdrawn / Pending Real Corpus Ingestion"},
        {"Item": 4, "Task": "Quarantine 5-folio holdout from training metrics", "Status": "Enforced in Sidebar Partitions"},
        {"Item": 5, "Task": "Strip linguistic interpretations (pure C-L-P-R)", "Status": "Active"},
        {"Item": 6, "Task": "Semantic permutation tournament", "Status": "Active Engine"},
        {"Item": 7, "Task": "Affix-role permutation tournament", "Status": "Pending Next Implementation"},
        {"Item": 8, "Task": "Multifactorial structural checks (lines/currier)", "Status": "Pending Next Implementation"},
        {"Item": 9, "Task": "Independent external transfer test (Currier/Takahashi)", "Status": "Pending Next Implementation"},
        {"Item": 10, "Task": "Replication packaging (Standalone CLI/Docker)", "Status": "Pending Next Implementation"},
    ]

    st.table(pd.DataFrame(roadmap_data))
