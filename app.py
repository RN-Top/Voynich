"""
VOYNICH PIE-OF-PIE & SPOT LOCUS DECOMPOSITION
Generates the nested breakout pie (Screenshot 25) comparing:
- Primary operational states: heat, medium, outlet, reflux, retain, drain
- Exploded secondary partition: unmapped carrier roots vs. peripheral tokens
"""

import os
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np

# Frozen role mapping
ROLE_COLORS = {
    "heat": "#FF0000",
    "medium": "#00FFFF",
    "outlet": "#FFA500",
    "reflux": "#800080",
    "retain": "#008000",
    "drain": "#000000",
    "unmapped": "#808080"
}

def tag_token(token: str) -> str:
    t = re.sub(r"[^a-z]", "", str(token).lower().strip())
    if not t: return "unmapped"
    if t.endswith("am") or t.endswith("m") or t in ["chdam", "shedam"] or t.endswith("dam"): return "drain"
    if t.startswith("shed"): return "retain"
    if t.startswith("qok") or t.startswith("qo") or t.startswith("ok"): return "heat"
    if t == "daiin" or t.endswith("aiin") or t.endswith("ain"): return "medium"
    if t.endswith("ol") or t.endswith("al"): return "outlet"
    if t.endswith("or") or t.endswith("ar"): return "reflux"
    return "unmapped"

def load_master_table():
    candidates = [
        "voynich_active_table (1).csv",
        "voynich_active_table.csv",
        "voynich_master_corpus_extracted.csv",
        "voynich_master_corpus_extracted (1).csv",
        "voynich_master_corpus_extracted_2.csv"
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 5000:
            df = pd.read_csv(c)
            if "token" in df.columns:
                if "role" not in df.columns:
                    df["role"] = df["token"].apply(tag_token)
                return df
    return None

def generate_exploded_pie(df, output_path="data/spot_pies/exploded_spot_pie.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    counts = Counter(df["role"])
    total_tokens = sum(counts.values())

    # Split into mapped apparatus roles vs unmapped pool
    mapped_roles = ["heat", "medium", "outlet", "reflux", "retain", "drain"]
    mapped_counts = [counts.get(r, 0) for r in mapped_roles]
    unmapped_count = counts.get("unmapped", 0)

    # Primary pie: Mapped roles + aggregated unmapped slice
    main_labels = mapped_roles + ["unmapped (exploded)"]
    main_sizes = mapped_counts + [unmapped_count]
    main_colors = [ROLE_COLORS[r] for r in mapped_roles] + ["#A0A0A0"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(wspace=0.3)

    # Primary Pie
    wedges, texts, autotexts = ax1.pie(
        main_sizes,
        labels=main_labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=main_colors,
        explode=[0]*len(mapped_roles) + [0.1]
    )
    ax1.set_title("Apparatus Roles (Primary)")

    # Secondary Sub-Pie / Breakdown (Top Unmapped Carrier Groups)
    unmapped_tokens = df[df["role"] == "unmapped"]["token"].astype(str)
    top_unmapped = Counter(unmapped_tokens).most_common(4)
    sub_labels = [k for k, v in top_unmapped] + ["other unmapped"]
    top_sum = sum(v for k, v in top_unmapped)
    sub_sizes = [v for k, v in top_unmapped] + [max(0, unmapped_count - top_sum)]

    ax2.pie(
        sub_sizes,
        labels=sub_labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=["#606060", "#787878", "#909090", "#A8A8A8", "#C0C0C0"]
    )
    ax2.set_title(f"Unmapped Sub-Structure (N={unmapped_count:,})")

    # Connect wedges with boundary lines
    theta1, theta2 = wedges[-1].theta1, wedges[-1].theta2
    center, r = wedges[-1].center, wedges[-1].r
    width = 0.2

    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con1 = ConnectionPatch(xyA=(-width / 2, 0.5), coordsA=ax2.transAxes,
                           xyB=(x, y), coordsB=ax1.transData)
    con1.set_color("#444")
    con1.set_linewidth(1.5)
    ax2.add_artist(con1)

    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con2 = ConnectionPatch(xyA=(-width / 2, -0.5), coordsA=ax2.transAxes,
                           xyB=(x, y), coordsB=ax1.transData)
    con2.set_color("#444")
    con2.set_linewidth(1.5)
    ax2.add_artist(con2)

    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    return total_tokens, counts

if __name__ == "__main__":
    df = load_master_table()
    if df is not None:
        N, role_counts = generate_exploded_pie(df)
        print(f"Generated exploded pie for N={N:,} tokens.")
    else:
        print("Master table not found.")
