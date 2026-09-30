import io
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Voynich Decipherment Workbench", layout="wide")

# =========================================================================
# 1. FROZEN APPARATUS CONTRACT & MORPHOTACTIC RULES
# =========================================================================
# Role Map:
# C (heat/start): qo-, qok-, ok-
# L (medium): daiin, -aiin, -ain, -iin, -in
# P (retain/process): shed-, ch-, sh-, da-, -al, -ol, -ar, -or
# R (outlet/drain/close): -m, -am, -dy, -edy, -y
PREFIX_RULES = {
    'qo': 'C', 'qok': 'C', 'ok': 'C', 'ot': 'C',
    'shed': 'P', 'ch': 'P', 'sh': 'P', 'da': 'P',
    's': 'L', 't': 'L',
    'd': 'R', 'y': 'R'
}

SUFFIX_RULES = {
    'shedam': 'R', 'chdam': 'R', 'am': 'R', 'm': 'R',
    'daiin': 'L', 'aiin': 'L', 'ain': 'L', 'iin': 'L', 'in': 'L',
    'al': 'P', 'ol': 'P', 'ar': 'P', 'or': 'P',
    'edy': 'C', 'dy': 'C', 'y': 'C'
}

ORIGINAL_SEMANTIC_MAP = {
    'C': 'heat',
    'L': 'medium',
    'P': 'retain',
    'R': 'outlet'
}

# The canonical directed cyclic apparatus sequence: C -> L -> route -> P -> R
VALID_TRANSITIONS = {
    ('heat', 'medium'),
    ('medium', 'retain'),
    ('retain', 'outlet'),
    ('outlet', 'heat')
}

# =========================================================================
# 2. DEFAULT EVALUATION DATASET (Folio f70v2)
# =========================================================================
DEFAULT_CSV = """,folio,token,carrier,predicted,expected,match
1,f70v2,dar,EMPTY,outlet,medium,false
2,f70v2,otey,ote,reflux,reflux,true
3,f70v2,ykeey,ykee,reflux,reflux,true
4,f70v2,tchy,tch,reflux,reflux,true
6,f70v2,oteotey,oteote,reflux,reflux,true
7,f70v2,shey,she,reflux,reflux,true
10,f70v2,dateey,atee,reflux,reflux,true
11,f70v2,sal,s,outlet,medium,false
12,f70v2,ody,od,reflux,reflux,true
13,f70v2,choteey,chotee,reflux,reflux,true
14,f70v2,choeteedy,choeteed,reflux,reflux,true
16,f70v2,yteos,yteos,outlet,,false
17,f70v2,alain,al,medium,medium,true
18,f70v2,sheodaly,sheodal,reflux,reflux,true
20,f70v2,aiin,EMPTY,medium,medium,true
21,f70v2,cholkal,cholk,outlet,medium,false
22,f70v2,chokear,choke,outlet,medium,false
23,f70v2,oteody,oteod,reflux,reflux,true
24,f70v2,cholaiin,chol,medium,medium,true
25,f70v2,oteeoal,oteeo,outlet,medium,false
26,f70v2,al,EMPTY,outlet,medium,false
27,f70v2,sheeos,sheeos,outlet,,false
28,f70v2,okey,oke,reflux,reflux,true
30,f70v2,dy,EMPTY,reflux,reflux,true
34,f70v2,olar,ol,outlet,medium,false
35,f70v2,otoaiin,oto,medium,medium,true
36,f70v2,oteeody,oteeod,reflux,reflux,true
38,f70v2,todaiin,tod,medium,medium,true
39,f70v2,chokain,chok,medium,medium,true
40,f70v2,otalal,otal,outlet,medium,false
41,f70v2,oteeam,otee,positional,positional,true
43,f70v2,ykary,ykar,reflux,reflux,true
44,f70v2,otar,ot,outlet,medium,false
45,f70v2,oty,ot,reflux,reflux,true
46,f70v2,oky,ok,reflux,reflux,true
47,f70v2,ody,od,reflux,reflux,true
48,f70v2,oty,ot,reflux,reflux,true
49,f70v2,ar,EMPTY,outlet,medium,false
51,f70v2,otody,otod,reflux,reflux,true
53,f70v2,otaldar,otald,outlet,medium,false
54,f70v2,okody,okod,reflux,reflux,true
55,f70v2,opysam,opys,positional,positional,true
56,f70v2,chy,ch,reflux,reflux,true
57,f70v2,otaly,otal,reflux,reflux,true
58,f70v2,otal,ot,outlet,medium,false
59,f70v2,arar,ar,outlet,medium,false
60,f70v2,otaldy,otald,reflux,reflux,true
61,f70v2,okeoly,okeol,reflux,reflux,true
62,f70v2,okydy,okyd,reflux,reflux,true
64,f70v2,daiiamdy,aiiamd,reflux,reflux,true"""

# =========================================================================
# 3. HELPER FUNCTIONS
# =========================================================================
def classify_token(token: str) -> str:
    """Classifies a Voynich token into structural roles C, L, P, R."""
    t = str(token).strip().lower()
    if not t or t == "empty":
        return "UNKNOWN"

    for sfx, role in sorted(SUFFIX_RULES.items(), key=lambda x: len(x[0]), reverse=True):
        if t.endswith(sfx):
            return role

    for pfx, role in sorted(PREFIX_RULES.items(), key=lambda x: len(x[0]), reverse=True):
        if t.startswith(pfx):
            return role

    return "UNKNOWN"


def score_semantic_transitions(tokens: list, role_to_meaning: dict) -> float:
    """Computes transition consistency under a specified role-meaning dictionary."""
    assigned = [
        role_to_meaning[classify_token(t)]
        for t in tokens
        if classify_token(t) in role_to_meaning
    ]
    if len(assigned) < 2:
        return 0.0

    transitions = list(zip(assigned[:-1], assigned[1:]))
    matches = sum(1 for pair in transitions if pair in VALID_TRANSITIONS)
    return matches / len(transitions)


# =========================================================================
# 4. STREAMLIT APPLICATION TABS
# =========================================================================
st.title("Voynich Decipherment Workbench")

tab_corpus, tab_morphology, tab_tournament = st.tabs([
    "Corpus Data", 
    "Morphological Classifier", 
    "Semantic Permutation Tournament"
])

# -------------------------------------------------------------------------
# TAB 1: Corpus Data Viewer
# -------------------------------------------------------------------------
with tab_corpus:
    st.subheader("Corpus Dataset")
    uploaded_file = st.file_uploader("Upload corpus CSV (optional, defaults to f70v2)", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Uploaded custom corpus successfully.")
    else:
        df = pd.read_csv(io.StringIO(DEFAULT_CSV.strip()))
        st.info("Loaded default folio f70v2 dataset.")

    st.dataframe(df, use_container_width=True)

# -------------------------------------------------------------------------
# TAB 2: Morphological Classifier & Stats
# -------------------------------------------------------------------------
with tab_morphology:
    st.subheader("Token Role Classification")
    tokens = df["token"].dropna().tolist() if "token" in df.columns else []

    if tokens:
        roles = [classify_token(t) for t in tokens]
        role_counts = Counter(roles)

        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Role Distribution Across Current Corpus:**")
            stats_df = pd.DataFrame(role_counts.items(), columns=["Role", "Count"]).sort_values("Count", ascending=False)
            st.dataframe(stats_df, use_container_width=True)

        with col_b:
            fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
            ax_bar.bar(role_counts.keys(), role_counts.values(), color="#4C72B0")
            ax_bar.set_ylabel("Count")
            ax_bar.set_title("Structural Class Occurrences")
            st.pyplot(fig_bar)
    else:
        st.warning("No 'token' column found in the loaded dataset.")

# -------------------------------------------------------------------------
# TAB 3: Semantic Permutation Tournament
# -------------------------------------------------------------------------
with tab_tournament:
    st.subheader("Permutation Tournament: Morphological Semantic Significance")
    st.markdown("""
    This test verifies whether the hypothesis sequence:
    $$\\text{heat } (C) \\longrightarrow \\text{medium } (L) \\longrightarrow \\text{retain } (P) \\longrightarrow \\text{outlet } (R)$$
    produces cycle transition consistency that significantly outperforms random role permutations across the tokens.
    """)

    col1, col2 = st.columns([1, 2])
    with col1:
        num_perms = st.slider("Permutations", min_value=500, max_value=20000, value=5000, step=500)
        random_seed = st.number_input("Random Seed", value=42, step=1)
        run_button = st.button("Run Tournament", type="primary")

    if run_button:
        token_list = df["token"].dropna().tolist() if "token" in df.columns else []

        if len(token_list) < 2:
            st.error("Insufficient tokens in the dataset to perform the tournament.")
        else:
            roles = list(ORIGINAL_SEMANTIC_MAP.keys())
            labels = list(ORIGINAL_SEMANTIC_MAP.values())

            # Baseline score for hypothesis
            actual_score = score_semantic_transitions(token_list, ORIGINAL_SEMANTIC_MAP)

            # Null permutation loop
            np.random.seed(int(random_seed))
            null_scores = np.empty(num_perms)
            for i in range(num_perms):
                shuffled = np.random.permutation(labels)
                perm_map = dict(zip(roles, shuffled))
                null_scores[i] = score_semantic_transitions(token_list, perm_map)

            mean_null = float(np.mean(null_scores))
            std_null = float(np.std(null_scores))
            p_val = float(np.mean(null_scores >= actual_score))
            z_score = float((actual_score - mean_null) / std_null) if std_null > 0 else 0.0

            st.divider()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Hypothesis Score", f"{actual_score:.4f}")
            m2.metric("Null Mean (Chance)", f"{mean_null:.4f}")
            m3.metric("Z-Score", f"{z_score:+.2f}")
            m4.metric("Empirical p-value", f"{p_val:.5f}")

            if p_val < 0.05:
                st.success(f"**Statistically Significant (p = {p_val:.5f})**: The sequence outperforms chance.")
            else:
                st.warning(f"**Not Statistically Significant (p = {p_val:.5f})**: The sequence does not beat chance on this token set.")

            # Distribution Plot
            fig, ax = plt.subplots(figsize=(8, 3.5))
            ax.hist(null_scores, bins=30, color="#888888", alpha=0.7, edgecolor="black", label="Null Distribution")
            ax.axvline(actual_score, color="red", linestyle="--", linewidth=2, label=f"Hypothesis ({actual_score:.4f})")
            ax.set_xlabel("Transition Consistency Score")
            ax.set_ylabel("Frequency")
            ax.legend()
            st.pyplot(fig)
