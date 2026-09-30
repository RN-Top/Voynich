pandas as pd
import numpy as np
import re
from collections import Counter, defaultdict
import random

st.set\_page\_config(page\_title="Voynich Decipherment Workbench", layout="wide")

st.title("Voynich Decipherment Workbench")
st.caption("Morphological Analysis, Syntactic Evaluation \& Permutation Tournaments")

# ---------------------------------------------------------

# Default / Fallback Sample Data Generator

# ---------------------------------------------------------

@st.cache\_data
def get\_sample\_data():
"""Generates synthetic Voynich EVA sample data if no file is uploaded."""
sample\_lines = \[
"fachys ykal ar ataiin shol shory cthesos chey keo dal chedy qokedy",
"otaiin cthy shey dain qokaiin or chey cthey qotedy ol shedy chol",
"daiin chedy ctheor otaiin chey shedy ctedy chekeor chedy",
"qokeedy qokaiin sol cheol daiin ctheo qokedy cthee dal shey",
"shedy qokain or cheor chedy dar shey daiin ctheor dal",
"fachys ykey otaiin chey keor qokedy chedy qotedy ol chey",
"otaiin shey qokaiin cthey cthes cheor keol chedy qotedy",
"qotedy chedy otaiin daiin chey ctheo qokedy cheor shedy dal",
"ykal ar chey keo cthesos qokaiin daiin shedy qotedy ol",
"qokedy shedy chol otaiin ctheor chey daiin qokeedy chedy"
\]
records = \[\]
for i, line in enumerate(sample\_lines):
folio = f"f{i//2 + 1}r"
currier = "A" if (i % 4 \< 2) else "B"
for pos, word in enumerate(line.split()):
records.append({
"folio": folio,
"currier": currier,
"line": i + 1,
"position": pos + 1,
"word": word
})
return pd.DataFrame(records)

# ---------------------------------------------------------

# Sidebar: Data Source \& Config

# ---------------------------------------------------------

st.sidebar.header("Data \& Configuration")
uploaded\_file = st.sidebar.file\_uploader("Upload EVA Transcription (CSV/TXT)", type=\["csv", "txt"\])

if uploaded\_file is not None:
try:
if uploaded\_file.name.endswith(".csv"):
df = pd.read\_csv(uploaded\_file)
else:
raw\_text = uploaded\_file.read().decode("utf-8")
lines = \[l.strip() for l in raw\_text.splitlines() if l.strip() and not l.startswith("#")\]
parsed = \[\]
for idx, line in enumerate(lines):
tokens = re.findall(r"\[a-z0-9\*\]+", line.lower())
for pos, tok in enumerate(tokens):
parsed.append({
"folio": f"line\_{idx+1}",
"currier": "A" if idx % 2 == 0 else "B",
"line": idx + 1,
"position": pos + 1,
"word": tok
})
df = pd.DataFrame(parsed)
st.sidebar.success("Custom data loaded successfully.")
except Exception as e:
st.sidebar.error(f"Error parsing file: {e}")
df = get\_sample\_data()
else:
df = get\_sample\_data()
st.sidebar.info("Using built-in EVA sample corpus. Upload a file above to analyze full folios.")

# Ensure required columns

required\_cols = {"folio", "currier", "word"}
if not required\_cols.issubset(df.columns):
st.error(f"Data must contain at least columns: {required\_cols}")
st.stop()

# ---------------------------------------------------------

# Helper Functions: Morphological Parsing \& Transition Scores

# ---------------------------------------------------------

PREFIXES = ("qo", "ch", "sh", "da", "ot", "cth", "y", "sa")
SUFFIXES = ("edy", "aiin", "iin", "ey", "ol", "or", "ar", "al", "y")

def parse\_affixes(word):
"""Splits an EVA word into Prefix, Core, Suffix."""
w = str(word).lower()
prefix = ""
suffix = ""
for p in sorted(PREFIXES, key=len, reverse=True):
if w.startswith(p) and len(w) \> len(p):
prefix = p
w = w\[len(p):\]
break
for s in sorted(SUFFIXES, key=len, reverse=True):
if w.endswith(s) and len(w) \> len(s):
suffix = s
w = w\[:-len(s)\]
break
core = w if w else "\_"
return prefix or "none", core, suffix or "none"

df\["prefix"\], df\["core"\], df\["suffix"\] = zip(\*df\["word"\].apply(parse\_affixes))
df\["affix\_role"\] = df\["prefix"\] + "+" + df\["suffix"\]

def compute\_bigram\_mutual\_information(tokens):
"""Calculates average pointwise mutual information or sequential transition likelihood."""
if len(tokens) \< 2:
return 0.0
bigrams = list(zip(tokens\[:-1\], tokens\[1:\]))
n\_bigrams = len(bigrams)
n\_unigrams = len(tokens)

    bi_counts = Counter(bigrams)
    uni_counts = Counter(tokens)
    
    score = 0.0
    for (t1, t2), count in bi_counts.items():
        p_bi = count / n_bigrams
        p1 = uni_counts[t1] / n_unigrams
        p2 = uni_counts[t2] / n_unigrams
        pmi = np.log2(p_bi / (p1 * p2) + 1e-9)
        score += count * pmi
    return float(score / n_bigrams)

# ---------------------------------------------------------

# Tabs: Workbench Navigation

# ---------------------------------------------------------

tab\_corpus, tab\_affix\_tourney, tab\_semantic\_tourney = st.tabs(\[
"1. Corpus Overview",
"2. Affix-Role Tournament",
"3. Semantic Permutation Tournament (Item 6)"
\])

# TAB 1: Corpus Overview

with tab\_corpus:
st.subheader("Corpus Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tokens", len(df))
col2.metric("Unique Types", df\["word"\].nunique())
col3.metric("Folios Covered", df\["folio"\].nunique())
col4.metric("Dialect Split (A / B)", f"{sum(df\['currier'\]=='A')} / {sum(df\['currier'\]=='B')}")

    st.dataframe(df.head(25), use_container_width=True)

# TAB 2: Affix-Role Tournament

with tab\_affix\_tourney:
st.subheader("Affix-Role Sequential Constraint Tournament")
st.write(
"Tests whether prefix-to-suffix roles adhere to strict transition grammar "
"compared against shuffled role sequences."
)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        n_affix_perms = st.number_input("Affix Permutations", min_value=100, max_value=20000, value=2000, step=500)
    with col_a2:
        affix_seed = st.number_input("Random Seed (Affix)", value=42, step=1)
    
    if st.button("Run Affix-Role Tournament"):
        np.random.seed(int(affix_seed))
        roles = df["affix_role"].tolist()
        observed_score = compute_bigram_mutual_information(roles)
    
        null_distribution = []
        shuffled = roles.copy()
        for _ in range(int(n_affix_perms)):
            np.random.shuffle(shuffled)
            null_distribution.append(compute_bigram_mutual_information(shuffled))
    
        null_dist = np.array(null_distribution)
        z_score = (observed_score - np.mean(null_dist)) / (np.std(null_dist) + 1e-9)
        p_val = float(np.mean(null_dist &gt;= observed_score))
    
        res1, res2, res3 = st.columns(3)
        res1.metric("Observed Transition Score", f"{observed_score:.4f}")
        res2.metric("Mean Shuffled Score", f"{np.mean(null_dist):.4f}")
        res3.metric("Z-Score", f"{z_score:.2f}")
    
        if p_val &lt; 0.001:
            st.success(f"Significant syntactic rigidity detected (p &lt; 0.001, z = {z_score:.2f}).")
        else:
            st.warning(f"No significant deviation from randomized roles (p = {p_val:.4f}).")

# TAB 3: Semantic Permutation Tournament (Item 6)

with tab\_semantic\_tourney:
st.subheader("Item 6: Semantic Permutation Tournament")
st.write(
"Evaluates whether context-word dependencies, semantic clustering, or dialect transitions "
"surpass empirical baseline models across controlled randomized trials."
)

    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        permutations = st.number_input("Permutations", min_value=1000, max_value=50000, value=10000, step=1000)
    with t_col2:
        seed = st.number_input("Permutation Seed", value=42, step=1)
    with t_col3:
        target_currier = st.selectbox("Currier Dialect Filter", ["All", "Currier A", "Currier B"])
    
    # Filter data according to dialect selection
    sub_df = df.copy()
    if target_currier == "Currier A":
        sub_df = sub_df[sub_df["currier"] == "A"]
    elif target_currier == "Currier B":
        sub_df = sub_df[sub_df["currier"] == "B"]
    
    if st.button("Execute 10,000-Permutation Tournament", type="primary"):
        with st.spinner("Computing observed bigram transition metrics and running Monte Carlo permutations..."):
            np.random.seed(int(seed))
            random.seed(int(seed))
    
            tokens = sub_df["word"].tolist()
            obs_stat = compute_bigram_mutual_information(tokens)
    
            # Fast vector-based permutation execution
            token_arr = np.array(tokens)
            null_stats = np.empty(int(permutations), dtype=np.float32)
    
            progress_bar = st.progress(0)
            batch_size = max(1, int(permutations) // 20)
    
            for i in range(int(permutations)):
                permuted_arr = np.random.permutation(token_arr)
                null_stats[i] = compute_bigram_mutual_information(permuted_arr.tolist())
                if (i + 1) % batch_size == 0 or (i + 1) == int(permutations):
                    progress_bar.progress((i + 1) / int(permutations))
    
            null_mean = float(np.mean(null_stats))
            null_std = float(np.std(null_stats))
            z_val = (obs_stat - null_mean) / (null_std + 1e-9)
            empirical_p = float(np.sum(null_stats &gt;= obs_stat) / int(permutations))
    
        st.subheader("Tournament Results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Observed Transition Metric", f"{obs_stat:.4f}")
        m2.metric("Monte Carlo Mean", f"{null_mean:.4f}")
        m3.metric("Z-Score", f"{z_val:+.2f}")
        m4.metric("Empirical p-value", f"{empirical_p:.6f}")
    
        # Summary findings
        st.markdown("---")
        if empirical_p &lt; 0.0001:
            st.success(
                f"**Hypothesis Confirmed:** Observed transition predictability significantly exceeds "
                f"the 10,000 randomized permutations ($z = {z_val:.2f}$, $p &lt; 0.0001$). "
                f"This indicates strict non-random word-order constraints consistent with structured procedural syntax."
            )
        else:
            st.info(
                f"Tournament concluded with empirical $p = {empirical_p:.4f}$ ($z = {z_val:.2f}$). "
                f"Transition scores fall within expected bounds of the shuffled distribution."
            )
    
        # Distribution plot data summary
        hist_df = pd.DataFrame({
            "Shuffled Distribution": null_stats
        })
        st.bar_chart(hist_df.iloc[:200])
        st.caption("Distribution snapshot of permutation metric samples.")

```
```
