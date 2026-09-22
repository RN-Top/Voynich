"""
MODULE: spot_pies
Frozen role-tagger and physical locus distribution comparison across:
1. FRONT LOCK (f1r, f1v, f2r)
2. FOLD CENTER (f86r3 or crease center panel)
3. FOLD LEFT (f85v1, f85v2)
4. FOLD RIGHT (f86r4, f86r5, f86r6)
5. BACK LOCK (f116r, f116v)
"""

import os
import re
from collections import Counter
import numpy as np
import pandas as pd

# ---------------------------------------------------------
# FROZEN ROLE MAP (IMMUTABLE - DO NOT RETUNE)
# ---------------------------------------------------------
ROLE_COLORS = {
    "heat": "#FF0000",      # red: qo-, qok-, ok-
    "medium": "#00FFFF",    # cyan: daiin, -aiin
    "outlet": "#FFA500",    # orange: -ol, -al
    "reflux": "#800080",    # purple: -or, -ar
    "retain": "#008000",    # green: shed-
    "drain": "#000000",     # black: -m, -am, chdam, shedam
    "unmapped": "#808080"   # gray: all else
}

GRAY_COLOR = "#808080"

SPOTS = {
    "FRONT LOCK": ["f1r", "f1v", "f2r"],
    "FOLD CENTER": ["f86r3", "f85v2.c", "rosettes_center", "f86r.c"],
    "FOLD LEFT": ["f85v1", "f85v2"],
    "FOLD RIGHT": ["f86r4", "f86r5", "f86r6", "f86r"],
    "BACK LOCK": ["f116r", "f116v"]
}

def tag_token(token: str) -> str:
    """Strict operational role tagger. No new glosses. No refits."""
    t = re.sub(r"[^a-z]", "", str(token).lower().strip())
    if not t:
        return "unmapped"
    if t.endswith("am") or t.endswith("m") or t in ["chdam", "shedam"] or t.endswith("dam"):
        return "drain"
    if t.startswith("shed"):
        return "retain"
    if t.startswith("qok") or t.startswith("qo") or t.startswith("ok"):
        return "heat"
    if t == "daiin" or t.endswith("aiin") or t.endswith("ain"):
        return "medium"
    if t.endswith("ol") or t.endswith("al"):
        return "outlet"
    if t.endswith("or") or t.endswith("ar"):
        return "reflux"
    return "unmapped"

def load_spot_data():
    """Ingests corpus from existing CSV or fallback files."""
    candidates = [
        "voynich_master_corpus_extracted_2.csv",
        "voynich_master_corpus_extracted.csv",
        "voynich_corpus_extracted (5).csv",
        "data/ZL3b-n.txt",
        "ZL3b-n.txt"
    ]
    df = None
    for path in candidates:
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            if path.endswith(".csv"):
                try:
                    df = pd.read_csv(path)
                    break
                except Exception:
                    continue
    return df

def analyze_spot(df_corpus, folios):
    """Computes N, role counts, and top 10 tokens for a spot."""
    if df_corpus is None or df_corpus.empty:
        return {"N": 0, "counts": {}, "pcts": {}, "top10": [], "missing": True}
    
    # Check matching folios
    avail_folios = df_corpus["folio"].astype(str).unique()
    matched_folios = [f for f in folios if any(f.lower() in af.lower() for af in avail_folios)]
    
    if not matched_folios:
        return {"N": 0, "counts": {}, "pcts": {}, "top10": [], "missing": True}
    
    sub = df_corpus[df_corpus["folio"].astype(str).str.lower().apply(lambda x: any(m in x for m in matched_folios))]
    tokens = sub["token"].astype(str).tolist() if "token" in sub.columns else []
    
    N = len(tokens)
    if N == 0:
        return {"N": 0, "counts": {}, "pcts": {}, "top10": [], "missing": True}
    
    roles = [tag_token(tok) for tok in tokens]
    counts = dict(Counter(roles))
    pcts = {r: round((counts.get(r, 0) / N) * 100.0, 2) for r in ROLE_COLORS.keys()}
    
    # Top 10 tokens with roles
    tok_counts = Counter(tokens).most_common(10)
    top10 = [(tok, cnt, tag_token(tok)) for tok, cnt in tok_counts]
    
    return {
        "N": N,
        "counts": counts,
        "pcts": pcts,
        "top10": top10,
        "missing": False,
        "small_n": N < 30
    }

def get_comparison_table(results_dict):
    """Formats comparison matrix across all 5 spots."""
    roles = ["heat", "medium", "outlet", "reflux", "retain", "drain", "unmapped"]
    data = {"Role": roles}
    for name in ["FRONT LOCK", "FOLD CENTER", "FOLD LEFT", "FOLD RIGHT", "BACK LOCK"]:
        res = results_dict.get(name, {})
        if res.get("missing"):
            data[name] = ["MISSING"] * len(roles)
        else:
            pcts = res.get("pcts", {})
            data[name] = [f"{pcts.get(r, 0.0):.2f}%" for r in roles]
    return pd.DataFrame(data)
