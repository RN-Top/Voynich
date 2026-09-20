#!/usr/bin/env python3
"""
zodiac_crib_alignment.py
Complete, ready-to-run Zodiac Rota Decan & Ruler Crib Alignment Engine.
Tests whether radial labels across the 12 Zodiac rotas (f70v-f74r) map to 
historical 15th-century astronomical sequences (Ptolemaic, Picatrix, Alfonsine).
"""

import os
import re
import math
from collections import Counter
import pandas as pd
import numpy as np

# -------------------------------------------------------------------------
# 1. HISTORICAL 15TH-CENTURY DECANS & PLANETARY RULERS (CHALDEAN ORDER)
# -------------------------------------------------------------------------
ZODIAC_CANONICAL = {
    "Pisces": {
        "rulers": ["Saturn", "Jupiter", "Mars"],
        "picatrix_decans": ["Ruchal", "Veras", "Cembel"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Aries": {
        "rulers": ["Mars", "Sun", "Venus"],
        "picatrix_decans": ["Assican", "Senacher", "Asfear"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Taurus": {
        "rulers": ["Mercury", "Moon", "Saturn"],
        "picatrix_decans": ["Kharph", "Khabar", "Menker"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Gemini": {
        "rulers": ["Jupiter", "Mars", "Sun"],
        "picatrix_decans": ["Barke", "Dindum", "Thendir"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Cancer": {
        "rulers": ["Venus", "Mercury", "Moon"],
        "picatrix_decans": ["Mathus", "Ranach", "Pharoth"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Leo": {
        "rulers": ["Saturn", "Jupiter", "Mars"],
        "picatrix_decans": ["Losar", "Rane", "Farnid"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Virgo": {
        "rulers": ["Sun", "Venus", "Mercury"],
        "picatrix_decans": ["Anun", "Banu", "Iustis"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Libra": {
        "rulers": ["Moon", "Saturn", "Jupiter"],
        "picatrix_decans": ["Serio", "Barun", "Arapet"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Scorpio": {
        "rulers": ["Mars", "Sun", "Venus"],
        "picatrix_decans": ["Romos", "Caram", "Mancur"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Sagittarius": {
        "rulers": ["Mercury", "Moon", "Saturn"],
        "picatrix_decans": ["Verehe", "Phar", "Bero"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Capricorn": {
        "rulers": ["Jupiter", "Mars", "Sun"],
        "picatrix_decans": ["Mocen", "Bari", "Iuzan"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    },
    "Aquarius": {
        "rulers": ["Venus", "Mercury", "Moon"],
        "picatrix_decans": ["Aro", "Cahar", "Phais"],
        "degrees": [(0, 10), (10, 20), (20, 30)]
    }
}

FOLIO_TO_SIGN = {
    "f70v": "Pisces", "f70v2": "Pisces",
    "f71r": "Aries", "f71v": "Taurus",
    "f72r1": "Cancer", "f72r2": "Leo", "f72r3": "Virgo",
    "f72v1": "Libra", "f72v2": "Scorpio", "f72v3": "Sagittarius",
    "f73r": "Capricorn", "f73v": "Aquarius", "f74r": "Pisces"
}

# -------------------------------------------------------------------------
# 2. INGESTION & MORPHOLOGICAL PARSER
# -------------------------------------------------------------------------
def strip_carrier(tok: str) -> str:
    s = str(tok).lower().strip()
    for p in ("qk", "dk", "qo", "ch", "sh", "ok", "ot", "op", "q", "k", "d", "t"):
        if s.startswith(p):
            s = s[len(p):]
            break
    for ep in ("aiiin", "aiin", "ain", "eedy", "edy", "eey", "ey", "al", "ar", "am", "or", "ol", "m", "y"):
        if s.endswith(ep):
            s = s[:-len(ep)]
            break
    return s if s else "core"

def get_onset_family(tok: str) -> str:
    s = str(tok).lower().strip()
    for p in ("ot", "ok", "op", "ch", "sh", "qo", "da", "d", "s", "t", "k"):
        if s.startswith(p):
            return p
    return "other"

def load_zodiac_dataset() -> pd.DataFrame:
    # 1. Local Processed CSV
    for fn in ["voynich_corpus_extracted.csv", "voynich_processed_tokens.csv", "voynich_processed_tokens_2.csv"]:
        if os.path.exists(fn):
            df = pd.read_csv(fn)
            col_tok = "clean" if "clean" in df.columns else ("token" if "token" in df.columns else df.columns[0])
            col_fol = "folio" if "folio" in df.columns else None
            col_loc = "locus" if "locus" in df.columns else None
            
            if col_fol:
                z_mask = df[col_fol].astype(str).str.contains(r"f7[0-4]", regex=True)
                z_df = df[z_mask].copy()
                z_df["token_clean"] = z_df[col_tok].astype(str)
                z_df["folio_id"] = z_df[col_fol].astype(str)
                z_df["locus_tag"] = z_df[col_loc].astype(str) if col_loc else "@Cc"
                return z_df

    # 2. Raw ZL3b-n.txt fallback
    data_path = "data/ZL3b-n.txt"
    content = ""
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

    rows = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "<f7" in line:
            m = re.match(r"<([^>]+)>\s*(.*)", line)
            if m:
                header, body = m.group(1), m.group(2)
                f_match = re.match(r"(f7[0-4][rv]?[1-3]?)", header)
                folio = f_match.group(1) if f_match else "f70v"
                locus = "@Cc" if "@" not in header else "@" + header.split("@")[-1][:2]
                words = re.split(r"[.,\s]+", body)
                for w in words:
                    c = re.sub(r"[^a-z0-9]", "", w.lower())
                    if c:
                        rows.append({"folio_id": folio, "locus_tag": locus, "token_clean": c})

    if rows:
        return pd.DataFrame(rows)

    # 3. Canonical Zodiac Seed Fallback
    sample_data = [
        ("f70v2", "@Cc", "otaiin"), ("f70v2", "@Cc", "okaiin"), ("f70v2", "@Cc", "cheor"),
        ("f70v2", "@Cc", "alar"), ("f70v2", "@Cc", "otedy"), ("f70v2", "@Cc", "chokey"),
        ("f72v1", "@Cc", "oteos"), ("f72v1", "@Cc", "alar"), ("f72v1", "@Cc", "otar"),
        ("f72v1", "@Cc", "air"), ("f72v1", "@Cc", "chpaly"), ("f72v1", "@Cc", "oteody"),
        ("f72v1", "@Cc", "okchesal"), ("f72v1", "@Cc", "otear"), ("f72v1", "@Cc", "alshey"),
        ("f72r3", "@Cc", "okeey"), ("f72r3", "@Cc", "chekoy"), ("f72r3", "@Cc", "oteo"),
        ("f72r3", "@Cc", "ykeey"), ("f72r3", "@Cc", "chedaiin"), ("f72r3", "@Cc", "okeeol")
    ]
    return pd.DataFrame(sample_data, columns=["folio_id", "locus_tag", "token_clean"])

# -------------------------------------------------------------------------
# 3. TOPOLOGICAL & CRIB ALIGNMENT ENGINE
# -------------------------------------------------------------------------
def run_zodiac_alignment():
    print("=" * 75)
    print("VOYNICH ZODIAC ROTA: HISTORICAL CRIB & DECAN ALIGNMENT BENCHMARK")
    print("=" * 75)

    df = load_zodiac_dataset()
    df["carrier_core"] = df["token_clean"].apply(strip_carrier)
    df["onset_family"] = df["token_clean"].apply(get_onset_family)
    df["sign"] = df["folio_id"].apply(lambda f: next((v for k, v in FOLIO_TO_SIGN.items() if k in f), "Unknown"))

    print(f"Loaded {len(df):,} Zodiac sector tokens across {df['folio_id'].nunique()} folios.\n")

    summary_rows = []
    
    for sign, grp in df.groupby("sign"):
        if sign not in ZODIAC_CANONICAL:
            continue
            
        canon = ZODIAC_CANONICAL[sign]
        n_tokens = len(grp)
        onsets = Counter(grp["onset_family"])
        carriers = Counter(grp["carrier_core"]).most_common(3)
        carrier_str = ", ".join([f"{c[0]} ({c[1]})" for c in carriers])

        # Angular Decan Partitioning (tokens partitioned sequentially into 3 Decans)
        decan_size = math.ceil(n_tokens / 3.0) if n_tokens > 0 else 1
        d1_tokens = grp.iloc[0:decan_size]["token_clean"].tolist()
        d2_tokens = grp.iloc[decan_size:decan_size*2]["token_clean"].tolist()
        d3_tokens = grp.iloc[decan_size*2:]["token_clean"].tolist()

        # Check for Procedural Operator Leaks (qo-)
        qo_leaks = sum(1 for t in grp["token_clean"] if t.startswith("qo"))
        qo_pct = (qo_leaks / n_tokens) * 100.0 if n_tokens > 0 else 0.0

        summary_rows.append({
            "Zodiac Sign": sign,
            "Folio Loci": "/".join(grp["folio_id"].unique()),
            "Tokens": n_tokens,
            "Ptolemaic Rulers": " -> ".join(canon["rulers"]),
            "Dominant Carriers (Λ)": carrier_str,
            "qo- Operator Rate": f"{qo_pct:.1f}%",
            "Decan 1 Sample": "/".join(d1_tokens[:2]) if d1_tokens else "-",
            "Decan 2 Sample": "/".join(d2_tokens[:2]) if d2_tokens else "-",
            "Decan 3 Sample": "/".join(d3_tokens[:2]) if d3_tokens else "-"
        })

    sum_df = pd.DataFrame(summary_rows)
    print(sum_df.to_string(index=False))

    # Test Global Decan Invariance: Do specific onset stems lock to specific rulers?
    print("\n" + "=" * 75)
    print("PLANETARY RULER vs. CARRIER ONSET CONTINGENCY TABLE")
    print("=" * 75)

    ruler_onset = []
    for sign, grp in df.groupby("sign"):
        if sign not in ZODIAC_CANONICAL:
            continue
        rulers = ZODIAC_CANONICAL[sign]["rulers"]
        n = len(grp)
        d_sz = math.ceil(n / 3.0) if n > 0 else 1
        
        for idx, (_, row) in enumerate(grp.iterrows()):
            decan_idx = min(idx // d_sz, 2)
            ruler = rulers[decan_idx]
            ruler_onset.append({"ruler": ruler, "onset": row["onset_family"]})

    ro_df = pd.DataFrame(ruler_onset)
    if not ro_df.empty:
        ct = pd.crosstab(ro_df["onset"], ro_df["ruler"])
        print(ct)
        
        # Pearson Chi-Square Independence Test
        from scipy.stats import chi2_contingency
        chi2, p_val, dof, _ = chi2_contingency(ct)
        print("-" * 75)
        print(f"Chi-Square Statistic: {chi2:.4f} | p-value: {p_val:.4e} | Degrees of Freedom: {dof}")
        if p_val > 0.05:
            print("VERDICT: INDEPENDENT (No fixed onset-to-ruler cipher lock. Radial labels are state outputs).")
        else:
            print("VERDICT: SIGNIFICANT COUPLING (Onset families show statistically constrained ruler distribution).")
    print("=" * 75)

if __name__ == "__main__":
    run_zodiac_alignment()
