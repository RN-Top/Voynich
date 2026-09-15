"""
voynich-state-viewer: Slot Omega Mining & Content Carrier Validator
Scans for the syntactic frame: Q-ACTIVE -> [X-AIIN] -> Q-ACTIVE
"""

import os
import re
import pandas as pd
from collections import Counter
from parser import parse_zl3b


def is_q_active(token: str) -> bool:
    """Checks if a token exhibits active Q-control prefixing."""
    if not token or not isinstance(token, str):
        return False
    t = token.lower().strip()
    return t.startswith("qo") or t.startswith("qok") or t.startswith("qot") or t.startswith("qoc")


def extract_carrier_from_aiin(token: str) -> str:
    """Extracts candidate carrier kernel X from an X-aiin / X-ain realization."""
    if not token or not isinstance(token, str):
        return ""
    t = token.lower().strip()
    if t.endswith("aiin"):
        return t[:-4]
    elif t.endswith("ain"):
        return t[:-3]
    return ""


def mine_omega_slots(corpus_path: str = "data/ZL3b-n.txt"):
    if not os.path.exists(corpus_path):
        print(f"Error: {corpus_path} not found.")
        return pd.DataFrame()

    df = parse_zl3b(corpus_path)
    if df.empty:
        print("Corpus parsed empty.")
        return pd.DataFrame()

    token_col = "clean" if "clean" in df.columns else "token"
    records = []

    # Group by folio and line to preserve physical syntactic boundaries
    grouped = df.groupby(["folio", "header" if "header" in df.columns else "line"])

    for (folio, line), group in grouped:
        tokens = group[token_col].dropna().astype(str).tolist()
        n = len(tokens)
        if n < 3:
            continue

        for i in range(1, n - 1):
            prev_tok = tokens[i - 1]
            curr_tok = tokens[i]
            next_tok = tokens[i + 1]

            # Frame condition: Q-ACTIVE -> X-AIIN -> Q-ACTIVE
            if is_q_active(prev_tok) and is_q_active(next_tok):
                carrier_core = extract_carrier_from_aiin(curr_tok)
                if carrier_core:
                    records.append({
                        "folio": folio,
                        "line": line,
                        "position": i,
                        "q_entry": prev_tok,
                        "target_token": curr_tok,
                        "carrier_candidate": carrier_core,
                        "q_exit": next_tok,
                        "section": group["section"].iloc[0] if "section" in group.columns else "Unknown"
                    })

    omega_df = pd.DataFrame(records)
    return omega_df


def summarize_carrier_performance(omega_df: pd.DataFrame):
    if omega_df.empty:
        print("No Omega frames detected matching criteria.")
        return

    print("\n" + "=" * 60)
    print("SLOT OMEGA MINING RESULTS: Q-ACTIVE -> [X-AIIN] -> Q-ACTIVE")
    print("=" * 60)
    print(f"Total Candidate Frames Found: {len(omega_df)}")

    carrier_counts = Counter(omega_df["carrier_candidate"])
    print("\nTop Carriers Occupying Slot Omega:")
    for carrier, count in carrier_counts.most_common(12):
        print(f"  - Stem '{carrier}': {count} frame occurrences")

    summary = omega_df.groupby("carrier_candidate").agg(
        total_occurrences=("target_token", "count"),
        distinct_folios=("folio", "nunique"),
        sections=("section", lambda s: ", ".join(sorted(set(s))))
    ).reset_index().sort_values(by="total_occurrences", ascending=False)

    print("\nCarrier Distribution & Section Portability:")
    print(summary.head(15).to_string(index=False))
    print("=" * 60)


if __name__ == "__main__":
    df_omega = mine_omega_slots("data/ZL3b-n.txt")
    summarize_carrier_performance(df_omega)
