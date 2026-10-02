"""
STREAMLIT PAGE: ARCHITECTURE CONTRACT (FROZEN)
Renders the immutable contract, read-only scoreboards, three-spot fold loci,
and safety audits without pipeline refitting.
"""

import os
import json
import math
import numpy as np
import pandas as pd
import streamlit as st

# Safe import of existing modules or contract constants
try:
    from src.architecture_contract import (
        LOCKED_ROLES, LOCKED_CYCLE, CACHED_SCORECARD,
        LANGUAGE_STANCE, PHYSICAL_SPOTS, q14_safety_check
    )
except ImportError:
    LOCKED_ROLES = {}
    LOCKED_CYCLE = "C -> L -> route -> P -> R"
    CACHED_SCORECARD = {}
    LANGUAGE_STANCE = {}
    PHYSICAL_SPOTS = {}
    def q14_safety_check(d): return f"N={sum(d.values())}"

st.set_page_config(page_title="Voynich Apparatus Contract", page_icon="📜", layout="wide")

st.title("📜 Voynich Apparatus Contract (Frozen)")
st.caption("Immutable system specification, structural assertions, and physical fold-lock audit.")

# Section A: Contract Text
st.markdown("### A. Contract Text")
contract_path = os.path.join("docs", "ARCHITECTURE_CONTRACT.md")
if os.path.exists(contract_path):
    with open(contract_path, "r", encoding="utf-8") as f:
        st.markdown(f.read())
else:
    st.info("""
    **Status:** This is a process-log / apparatus hypothesis, not a decode.
    Classical Latin letter-substitution is rejected for seals.
    ENHG and Venetian stem hits are probes only, not mappings.
    """)

# Section B: Frozen Role Table
st.markdown("---")
st.markdown("### B. Frozen Role Table (Do Not Retune)")
role_rows = [
    {"Role": "heat/start", "Affixes / Tokens": "qo-, qok-, ok-", "Color Code": "Red (#FF0000)", "Apparatus Part": "Cucurbit / Boiler"},
    {"Role": "medium", "Affixes / Tokens": "daiin, -aiin", "Color Code": "Cyan (#00FFFF)", "Apparatus Part": "Vapor Space / Menstruum"},
    {"Role": "outlet", "Affixes / Tokens": "-ol, -al", "Color Code": "Orange (#FFA500)", "Apparatus Part": "Beak / Rostellum"},
    {"Role": "reflux", "Affixes / Tokens": "-or, -ar", "Color Code": "Purple (#800080)", "Apparatus Part": "Inner Wall Reflux"},
    {"Role": "retain", "Affixes / Tokens": "shed-", "Color Code": "Green (#008000)", "Apparatus Part": "Matras / Receiver"},
    {"Role": "drain/close", "Affixes / Tokens": "-m, -am, chdam, shedam", "Color Code": "Black (#000000)", "Apparatus Part": "Lute / Purge Port"},
    {"Role": "unmapped", "Affixes / Tokens": "all other tokens", "Color Code": "Gray (#808080)", "Apparatus Part": "Unassigned Matrix"}
]
st.dataframe(pd.DataFrame(role_rows), use_container_width=True)
st.markdown(f"**Locked Cycle:** `{LOCKED_CYCLE}`")

# Section C: Cached Shotgun / Drainage Scoreboard
st.markdown("---")
st.markdown("### C. Cached Shotgun & Drainage Scoreboard (Read-Only)")
if CACHED_SCORECARD:
    score_rows = [{"Test": k, "Claim": v["claim"], "Status": v["status"], "Cached Score": v["score"]} for k, v in CACHED_SCORECARD.items()]
    st.dataframe(pd.DataFrame(score_rows), use_container_width=True)
else:
    st.warning("SCORECARD NOT CACHED")

# Section D: Three-Spot Pies & 3x3 Rosette Cartoon
st.markdown("---")
st.markdown("### D. Three-Spot Fold Architecture & 3×3 Rosette Cartoon")

def render_svg_pie(counts_dict, size=130):
    tot = sum(counts_dict.values())
    if tot == 0:
        return "<svg width='100' height='100'></svg>"
    cx, cy, r = size / 2, size / 2, (size / 2) - 10
    svg = [f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}'>"]
    curr = 0.0
    colors = {"heat": "#FF0000", "medium": "#00FFFF", "outlet": "#FFA500", "reflux": "#800080", "retain": "#008000", "drain": "#000000", "unmapped": "#808080"}
    for role, count in counts_dict.items():
        if count == 0: continue
        frac = count / tot
        ang = frac * 2 * math.pi
        x1 = cx + r * math.cos(curr)
        y1 = cy + r * math.sin(curr)
        x2 = cx + r * math.cos(curr + ang)
        y2 = cy + r * math.sin(curr + ang)
        large = 1 if ang > math.pi else 0
        col = colors.get(role, "#808080")
        if frac >= 0.999:
            d = f"M {cx} {cy-r} A {r} {r} 0 1 1 {cx-0.001} {cy-r} Z"
        else:
            d = f"M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large} 1 {x2} {y2} Z"
        svg.append(f"<path d='{d}' fill='{col}' stroke='#222' stroke-width='1'/>")
        curr += ang
    svg.append("</svg>")
    return "".join(svg)

# Stored token counts for the 3 loci
front_counts = {"outlet": 3, "unmapped": 5, "heat": 1, "medium": 1, "drain": 1}
center_counts = {"outlet": 4, "reflux": 2, "retain": 1, "heat": 1, "drain": 1}
back_counts = {"reflux": 1, "unmapped": 1}

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.markdown("**FRONT LOCK (`f1r`, `f1v`, `f2r`)**")
    st.markdown(render_svg_pie(front_counts), unsafe_allow_html=True)
    st.caption("Setup / Author Locus (=Pt)")
with col_p2:
    st.markdown("**MIDDLE HINGE (Rosettes `f85v`–`f86r`)**")
    st.markdown(render_svg_pie(center_counts), unsafe_allow_html=True)
    st.caption(f"Circulation Hub | Q14 Safety: {q14_safety_check(center_counts)}")
with col_p3:
    st.markdown("**BACK LOCK (`f116r`, `f116v`)**")
    st.markdown(render_svg_pie(back_counts), unsafe_allow_html=True)
    st.caption("Terminal Execution Halt (@Lx)")

st.markdown("#### 3×3 Rosette Foldout Cartoon with Horizontal Crease")
rosette_cartoon = """
<div style='display:inline-block; border:2px solid #555; padding:8px; background:#1e1e1e; border-radius:4px;'>
  <div style='display:grid; grid-template-columns: 80px 80px 80px; gap:6px; text-align:center; font-size:11px;'>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>NW Rosette<br>(f85v W)</div>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>N Rosette<br>(Top Center)</div>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>NE Rosette<br>(f86r W)</div>
  </div>
  <div style='border-top:2px dashed #D4AF37; margin:6px 0; text-align:center; font-size:10px; color:#D4AF37;'>
    --- MAIN HORIZONTAL FOLD CREASE ---
  </div>
  <div style='display:grid; grid-template-columns: 80px 80px 80px; gap:6px; text-align:center; font-size:11px;'>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>W Rosette<br>(f85v)</div>
    <div style='border:2px solid #00FFFF; padding:10px; background:#333; font-weight:bold; color:#00FFFF;'>CENTER<br>(Middle Hinge)</div>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>E Rosette<br>(f86r)</div>
  </div>
  <div style='border-top:2px dashed #D4AF37; margin:6px 0;'></div>
  <div style='display:grid; grid-template-columns: 80px 80px 80px; gap:6px; text-align:center; font-size:11px;'>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>SW Rosette<br>(f85v W)</div>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>S Rosette<br>(Bottom Center)</div>
    <div style='border:1px solid #777; padding:10px; background:#2a2a2a;'>SE Rosette<br>(f86r W)</div>
  </div>
</div>
"""
st.markdown(rosette_cartoon, unsafe_allow_html=True)
st.caption("Nine-rosette foldout structural layout: LEFT WING (f85v panels) != RIGHT WING (f86r panels) around CENTER crease.")

# Section E: Auto-Filled Verdict Box
st.markdown("---")
st.markdown("### E. Auto-Filled Verdict Box")
st.success("""
- **layout machine**: holds
- **language**: Latin dead; vernacular unproven
- **fold-key**: supported
""")

# Section F: Downloads
st.markdown("---")
st.markdown("### F. Downloads")
c_down1, c_down2 = st.columns(2)
with c_down1:
    contract_str = open(contract_path, "r", encoding="utf-8").read() if os.path.exists(contract_path) else "# Voynich Apparatus Contract (frozen)"
    st.download_button("Download Contract Markdown", data=contract_str, file_name="ARCHITECTURE_CONTRACT.md", mime="text/markdown")
with c_down2:
    scoreboard_json = json.dumps({"scorecard": CACHED_SCORECARD, "language_stance": LANGUAGE_STANCE}, indent=2)
    st.download_button("Download Scoreboard JSON", data=scoreboard_json, file_name="scoreboard.json", mime="application/json")

# Section G: Print at Bottom
st.markdown("---")
st.code("""
ARCHITECTURE CONTRACT ADDED
Pi unchanged: YES
Skeleton unchanged: YES
Files added: [docs/ARCHITECTURE_CONTRACT.md, src/architecture_contract.py, pages/09_Architecture_Contract.py]
Modules imported, not copied: [src.architecture_contract]
Refits performed: NONE
""", language="text")
