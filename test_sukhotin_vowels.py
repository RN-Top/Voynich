#!/usr/bin/env python3
"""
test_sukhotin_vowels.py

Unsupervised vowel identification on Voynichese tokens using Sukhotin's algorithm.
Analyzes bigram contact matrices across the entire transcribed corpus.
"""

import os
import re
from collections import Counter
import numpy as np
import pandas as pd

# Load tokens from local CSV or fallback to ZL3b-n.txt
def load_tokens():
    if os.path.exists("voynich_processed_tokens.csv"):
        df = pd.read_csv("voynich_processed_tokens.csv")
        col = "clean" if "clean" in df.columns else df.columns[0]
        return [str(t).lower() for t in df[col].dropna() if str(t).strip()]
    
    if os.path.exists("data/ZL3b-n.txt"):
        with open("data/ZL3b-n.txt", "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        tokens = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(">")
            words = re.split(r"[.,\s]+", parts[-1])
            for w in words:
                c = re.sub(r"[^a-z0-9]", "", w.lower())
                if c:
                    tokens.append(c)
        return tokens
    
    # Minimal fallback sample
    return ["fachys", "ykal", "ar", "ataiin", "shol", "daiin", "chedy", "qokedy", "chdam"]

tokens = load_tokens()
print(f"Loaded {len(tokens):,} tokens for phonological analysis.")

# 1. Build alphabet and symmetric contact matrix
chars = sorted(list(set("".join(tokens))))
c2i = {c: i for i, c in enumerate(chars)}
M = np.zeros((len(chars), len(chars)), dtype=int)

for tok in tokens:
    for c1, c2 in zip(tok[:-1], tok[1:]):
        if c1 in c2i and c2 in c2i:
            M[c2i[c1], c2i[c2]] += 1
            M[c2i[c2], c2i[c1]] += 1

# 2. Iterative Sukhotin extraction
V = set()
freq = Counter("".join(tokens))

print("\n--- Running Sukhotin Vowel Extraction ---")
iteration = 1
while True:
    scores = {}
    for c in chars:
        if c in V:
            continue
        i = c2i[c]
        non_vowel_contacts = sum(M[i, c2i[cp]] for cp in chars if cp not in V)
        scores[c] = 2 * non_vowel_contacts - freq[c]
    
    if not scores:
        break
    best_c, best_val = max(scores.items(), key=lambda x: x[1])
    if best_val <= 0:
        break
    V.add(best_c)
    print(f"Iteration {iteration}: Isolated vowel candidate '{best_c}' (Score: {best_val:,}, Frequency: {freq[best_c]:,})")
    iteration += 1

consonants = [c for c in chars if c not in V]

print("\n" + "=" * 50)
print(f"DEDUCED VOWEL INVENTORY     ({len(V)} units): {sorted(list(V))}")
print(f"DEDUCED CONSONANT INVENTORY ({len(consonants)} units): {sorted(consonants)}")
print("=" * 50)
