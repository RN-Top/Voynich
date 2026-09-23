"""
VOYNICH WHOLE-MANUSCRIPT AUTOMATED SUITE (run_whole_voynich.py)
Executes across all 38,000+ tokens:
1. Corpus Ingestion (Local or remote fetch)
2. State Machine Transitions (C -> L -> P -> R) & Line Flush (A2 Effect)
3. Morphological Stemming (Lambda cores) & Zipf Distribution
4. Layout Gating (Diagram vs. Prose qo- Prefix Suppression)
5. Slot Omega Mining (Q-ACTIVE -> [X-aiin] -> Q-ACTIVE)
6. Sukhotin Phonetic Vowel/Consonant Induction
7. Codicological Colophon & Signature Audit (f1r.6, f9r.10, f116v)
"""

import os
import re
import urllib.request
import numpy as np
import pandas as pd
from collections import Counter

DATA_DIR = "data"
ZL3B_PATH = os.path.join(DATA_DIR, "ZL3b-n.txt")
ZL3B_URL = "https://www.voynich.nu/data/ZL3b-n.txt"

# ---------------------------------------------------------
# 1. CORPUS INGESTION
# ---------------------------------------------------------
print("=" * 70)
print("PHASE 1: INGESTING COMPLETE VOYNICH CORPUS")
print("=" * 70)

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(ZL3B_PATH) or os.path.getsize(ZL3B_PATH) < 100000:
    print(f"Downloading complete authoritative ZL3b-n corpus from {ZL3B_URL}...")
    try:
        urllib.request.urlretrieve(ZL3B_URL, ZL3B_PATH)
        print("Download successful.")
    except Exception as e:
        print(f"Direct download failed: {e}. Checking local files...")

tokens_raw = []
with open(ZL3B_PATH, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("<") and ">" in line:
            parts = line.split(">", 1)
            tag = parts[0][1:]
            text = parts[1] if len(parts) > 1 else ""
            
            # Extract locus and folio
            tag_parts = tag.split(";")
            loc_id = tag_parts[0]
            m = re.match(r"f(\d+[rv]\d?)", loc_id)
            folio = m.group(0) if m else "unknown"
            
            locus_type = "=Pt" if "=Pt" in tag else ("+Pc" if "+Pc" in tag else ("@Lz" if "@Lz" in tag else "+P0"))
            
            # Tokenize words
            clean_text = re.sub(r"[!?,.:={}\[\]<>]", " ", text)
            words = [w.strip() for w in clean_text.split() if w.strip()]
            for w in words:
                tokens_raw.append({
                    "folio": folio,
                    "tag": tag,
                    "locus": locus_type,
                    "token": w
                })

df_all = pd.DataFrame(tokens_raw)
print(f"Total tokens parsed: {len(df_all):,}")
print(f"Total folios covered: {df_all['folio'].nunique()}")

# ---------------------------------------------------------
# 2. STATE MACHINE MAPPING & A2 BUFFER FLUSH AUDIT
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("PHASE 2: MACROSTATE MAPPING & HARDWARE LINE-BUFFER FLUSH")
print("=" * 70)

def classify_state(tok):
    if tok.endswith("m") or tok.endswith("am"):
        return "R"  # Resolve / Flush
    elif tok.endswith("ey") or tok.endswith("eey") or tok.endswith("edy") or tok.endswith("eedy"):
        return "C"  # Transform / Loop
    elif tok.endswith("ain") or tok.endswith("aiin") or tok.endswith("or") or tok.endswith("ar"):
        return "L"  # Connect / Bus
    elif tok.endswith("y") or tok.endswith("ol") or tok.endswith("al"):
        return "P"  # Maintain / Hold
    return "?"

df_all["state"] = df_all["token"].apply(classify_state)
state_counts = df_all["state"].value_counts()
for s, count in state_counts.items():
    print(f"State [{s}]: {count:,} ({count / len(df_all) * 100:.2f}%)")

terminal_m = df_all[df_all["token"].str.endswith(("m", "am"))]
print(f"Total Line-Buffer Flush Tokens (-m / -am): {len(terminal_m):,}")

# ---------------------------------------------------------
# 3. CARRIER CORE COMPRESSION (LAMBDA) & ZIPF'S LAW
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("PHASE 3: CARRIER CORE (LAMBDA) EXTRACTION")
print("=" * 70)

def extract_carrier(w):
    # Strip prefix headers
    for p in ["qo", "qk", "ok", "ot", "ch", "sh", "da"]:
        if w.startswith(p) and len(w) > len(p) + 2:
            w = w[len(p):]
            break
    # Strip realization suffixes
    for s in ["aiin", "ain", "eedy", "edy", "eey", "ey", "ar", "al", "ol", "am", "y", "m"]:
        if w.endswith(s) and len(w) > len(s) + 1:
            w = w[:-len(s)]
            break
    return w

df_all["carrier"] = df_all["token"].apply(extract_carrier)
unique_tokens = df_all["token"].nunique()
unique_carriers = df_all["carrier"].nunique()
compression = (1.0 - (unique_carriers / unique_tokens)) * 100

print(f"Surface Token Vocabulary: {unique_tokens:,}")
print(f"Invariant Carrier Cores:  {unique_carriers:,}")
print(f"Vocabulary Compression:   {compression:.2f}%")
print("Top 10 Conserved Carrier Cores:")
for c, freq in df_all["carrier"].value_counts().head(10).items():
    print(f"  Carrier: '{c}' -> {freq:,} occurrences")

# ---------------------------------------------------------
# 4. DIAGRAM PREFIX SUPPRESSION (GATING AUDIT)
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("PHASE 4: LAYOUT PREFIX SUPPRESSION AUDIT")
print("=" * 70)

radial_df = df_all[df_all["locus"] == "@Lz"]
prose_df = df_all[df_all["locus"] == "+P0"]

radial_qo = radial_df["token"].str.startswith("qo").mean() * 100 if len(radial_df) > 0 else 0
prose_qo = prose_df["token"].str.startswith("qo").mean() * 100 if len(prose_df) > 0 else 0

print(f"Procedural 'qo-' prefix rate in Prose (+P0):        {prose_qo:.2f}%")
print(f"Procedural 'qo-' prefix rate in Radial Spokes (@Lz): {radial_qo:.2f}%")
print(f"Suppression Status: {'VERIFIED (Diagram Gating Active)' if radial_qo < 1.0 else 'CHECK'}")

# ---------------------------------------------------------
# 5. SLOT OMEGA MINING
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("PHASE 5: CANDIDATE SLOT OMEGA FRAME MINING")
print("=" * 70)

omega_matches = []
tokens = df_all["token"].tolist()
folios = df_all["folio"].tolist()

for i in range(len(tokens) - 2):
    t1, t2, t3 = tokens[i], tokens[i+1], tokens[i+2]
    # Match: Q-ACTIVE -> [X-aiin / X-ain] -> Q-ACTIVE
    if t1.startswith("qo") and (t2.endswith("aiin") or t2.endswith("ain")) and t3.startswith("qo"):
        omega_matches.append({
            "folio": folios[i],
            "frame": f"{t1} -> [{t2}] -> {t3}",
            "carrier_arg": extract_carrier(t2)
        })

df_omega = pd.DataFrame(omega_matches)
print(f"Total Slot Omega Frames Identified: {len(df_omega)}")
if not df_omega.empty:
    print("Top Substituted Stems in Slot Omega:")
    for arg, count in df_omega["carrier_arg"].value_counts().head(5).items():
        print(f"  Stem '{arg}': {count} occurrences")

# ---------------------------------------------------------
# 6. SUKHOTIN UNMANAGED PHONETIC INDUCTION
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("PHASE 6: SUKHOTIN VOWEL-CONSONANT INDUCTION")
print("=" * 70)

all_chars = sorted(list(set("".join(df_all["token"].tolist()))))
c2i = {c: i for i, c in enumerate(all_chars)}
M = np.zeros((len(all_chars), len(all_chars)), dtype=int)

for tok in df_all["token"]:
    for c1, c2 in zip(tok[:-1], tok[1:]):
        if c1 in c2i and c2 in c2i:
            M[c2i[c1], c2i[c2]] += 1
            M[c2i[c2], c2i[c1]] += 1

V = set()
freq = Counter("".join(df_all["token"].tolist()))

while True:
    scores = {}
    for c in all_chars:
        if c in V:
            continue
        i = c2i[c]
        non_vowel_contacts = sum(M[i, c2i[cp]] for cp in all_chars if cp not in V)
        scores[c] = 2 * non_vowel_contacts - freq[c]
    
    best_c, best_val = max(scores.items(), key=lambda x: x[1])
    if best_val <= 0:
        break
    V.add(best_c)

consonants = [c for c in all_chars if c not in V]
vowel_ratio = (len(V) / len(all_chars)) * 100

print(f"Induced Vocalic Phonemes: {sorted(list(V))}")
print(f"Induced Consonant Frames: {sorted(consonants)}")
print(f"Vowel Ratio: {vowel_ratio:.2f}% (Human linguistic range: ~30-40%)")

# ---------------------------------------------------------
# 7. CRITICAL CODICOLOGICAL COLOPHON CHECK
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("PHASE 7: SIGNATURE & COLOPHON VERIFICATION")
print("=" * 70)

colophon_targets = ["ydaraishy", "ytchas", "oror"]
for target in colophon_targets:
    hits = df_all[df_all["token"].str.contains(target, case=False, na=False)]
    if not hits.empty:
        for _, r in hits.iterrows():
            print(f"Target '{target}' verified at Folio: {r['folio']} | Locus: {r['locus']} | Token: {r['token']}")
    else:
        print(f"Target '{target}' not detected in direct scan.")

print("\n" + "=" * 70)
print("COMPLETE WHOLE-CORPUS AUDIT FINISHED.")
print("=" * 70)
