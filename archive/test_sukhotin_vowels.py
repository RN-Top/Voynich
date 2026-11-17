"""
Unsupervised Vowel-Consonant Induction via Sukhotin's Algorithm.
Analyzes character bigram adjacency matrices across the Voynich Manuscript (ZL3b-n.txt)
to determine vocalic nuclei vs. consonantal frames without linguistic assumptions.
"""

import os
import re
import urllib.request
from collections import Counter
import numpy as np

DATA_PATH = "data/ZL3b-n.txt"
FALLBACK_URL = "https://www.voynich.nu/data/ZL3b-n.txt"


def load_tokens():
    raw_text = ""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
    else:
        print(f"Local file {DATA_PATH} not found. Fetching from web...")
        req = urllib.request.Request(FALLBACK_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            raw_text = resp.read().decode("utf-8", errors="ignore")

    tokens = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Strip transcription tags <...>
        clean_line = re.sub(r"<[^>]+>", "", line)
        parts = re.split(r"[.,\s]+", clean_line)
        for p in parts:
            tok = re.sub(r"[^a-z0-9]", "", p.lower())
            if tok:
                tokens.append(tok)
    return tokens


def run_sukhotin(tokens):
    # Filter for standard characters
    char_counts = Counter("".join(tokens))
    # Retain characters that appear at least 10 times
    alphabet = sorted([c for c, cnt in char_counts.items() if cnt >= 10 and c.isalpha()])
    c2i = {c: i for i, c in enumerate(alphabet)}
    n = len(alphabet)

    # Construct symmetric contact matrix M
    M = np.zeros((n, n), dtype=int)
    for tok in tokens:
        for c1, c2 in zip(tok[:-1], tok[1:]):
            if c1 in c2i and c2 in c2i:
                i, j = c2i[c1], c2i[c2]
                M[i, j] += 1
                M[j, i] += 1

    V = set()
    freq = {c: char_counts[c] for c in alphabet}

    # Sukhotin iterative selection
    while True:
        scores = {}
        for c in alphabet:
            if c in V:
                continue
            i = c2i[c]
            # Non-vowel contacts: contacts with characters not currently in V
            non_vowel_contacts = sum(M[i, c2i[c_prime]] for c_prime in alphabet if c_prime not in V)
            # Score formula: 2 * contacts - total occurrences
            scores[c] = 2 * non_vowel_contacts - freq[c]

        best_c, best_val = max(scores.items(), key=lambda x: x[1])
        if best_val <= 0:
            break
        V.add(best_c)

    consonants = sorted([c for c in alphabet if c not in V])
    vowels = sorted(list(V))
    return vowels, consonants, freq


def main():
    print("================================================================")
    print("     SUKHOTIN VOWEL-CONSONANT INDUCTION BENCHMARK")
    print("================================================================")
    tokens = load_tokens()
    print(f"Loaded {len(tokens):,} tokens from corpus.")

    vowels, consonants, freq = run_sukhotin(tokens)

    total_chars = sum(freq.values())
    vowel_vol = sum(freq[c] for c in vowels)
    vowel_ratio = (vowel_vol / total_chars) * 100 if total_chars else 0

    print("\n--- RESULTS ---")
    print(f"Deduced Vocalic Nuclei (V): {vowels}")
    print(f"Deduced Consonantal Set (C): {consonants}")
    print(f"Corpus Vowel Volume: {vowel_ratio:.2f}% (Expected Romance/Latin range: 30-45%)")
    print("================================================================")


if __name__ == "__main__":
    main()
