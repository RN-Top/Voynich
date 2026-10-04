#!/usr/bin/env python3
"""
Test: Do Voynich closing words match O'Hickey medical vocabulary?

Pre-registration: analyses/fermoy_vocab_comparison_prereg.md
"""

import pandas as pd
from collections import Counter
from scipy.stats import binom_test
import numpy as np

def levenshtein(s1, s2):
    """Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def load_voynich_closing_words():
    """Load the 44 Voynich closing words from the report."""
    # From output/recipe_closing_report.md
    words = [
        "qodaiin", "olcheey", "ychedy", "chey", "sheody", "okeody",
        "cheeo", "alkam", "olor", "olaiin", "cheody", "chol",
        "chodaiin", "lkchedy", "dair", "chody", "okaly", "qoy",
        "lain", "chos", "y", "o", "chedal", "dchedy", "cheky"
    ]
    return words

def load_fermoy_vocabulary(filename=None):
    """
    Load medical vocabulary from Fermoy.

    Expected format: CSV with columns [term, category, latin_root, meaning]
    Categories: symptoms, cures, herbs, methods, tools, qualities

    If file doesn't exist, return empty list so test can still run
    (waiting for transcription to be added).
    """
    if filename is None:
        filename = "analyses/fermoy_medical_vocab.csv"

    try:
        df = pd.read_csv(filename)
        return df['term'].tolist()
    except FileNotFoundError:
        print(f"[INFO] {filename} not found. Using empty vocabulary.")
        print("       Waiting for Fermoy transcription to be added.")
        return []

def find_levenshtein_matches(voynich_words, fermoy_vocab, max_distance=3):
    """
    For each Voynich word, find Fermoy terms within Levenshtein distance.
    """
    matches = []
    for vword in voynich_words:
        for fterm in fermoy_vocab:
            dist = levenshtein(vword.lower(), fterm.lower())
            if dist <= max_distance:
                matches.append({
                    'voynich_word': vword,
                    'fermoy_term': fterm,
                    'distance': dist
                })
    return matches

def find_substring_matches(voynich_words, fermoy_vocab):
    """
    Find cases where Voynich word contains Fermoy term or vice versa.
    """
    substring_matches = []
    for vword in voynich_words:
        for fterm in fermoy_vocab:
            if len(fterm) >= 3:  # Only meaningful substrings
                if fterm.lower() in vword.lower():
                    substring_matches.append({
                        'voynich_word': vword,
                        'fermoy_term': fterm,
                        'match_type': 'fermoy_in_voynich'
                    })
                elif vword.lower() in fterm.lower():
                    substring_matches.append({
                        'voynich_word': vword,
                        'fermoy_term': fterm,
                        'match_type': 'voynich_in_fermoy'
                    })
    return substring_matches

def run_null_hypothesis_test(voynich_words, fermoy_vocab, num_matches_observed):
    """
    Binomial test: is the number of observed matches unlikely under the null?

    Null: random Voynich word to random Fermoy term has ~5% chance of Lev ≤ 3.
    Probability is rough; refined once Fermoy vocab is loaded.
    """
    if len(fermoy_vocab) == 0:
        return None

    n_comparisons = len(voynich_words) * len(fermoy_vocab)
    p_null = 0.05  # rough estimate

    p_value = binom_test(num_matches_observed, n_comparisons, p_null, alternative='greater')
    return p_value

def main():
    print("=" * 70)
    print("Fermoy Vocabulary Comparison Test")
    print("=" * 70)
    print()

    # Load Voynich closing words
    voynich_words = load_voynich_closing_words()
    print(f"Loaded {len(voynich_words)} Voynich closing words")
    print(f"Example: {voynich_words[:5]}")
    print()

    # Load Fermoy vocabulary
    fermoy_vocab = load_fermoy_vocabulary()

    if len(fermoy_vocab) == 0:
        print("[WAITING] Fermoy medical vocabulary not yet loaded.")
        print("          Please add: analyses/fermoy_medical_vocab.csv")
        print()
        print("Expected format:")
        print("  term,category,latin_root,meaning")
        print("  eg. 'galar,symptoms,dolor,pain'")
        print()
        return

    print(f"Loaded {len(fermoy_vocab)} Fermoy medical terms")
    print(f"Example: {fermoy_vocab[:5]}")
    print()

    # Run Levenshtein test
    print("=" * 70)
    print("LEVENSHTEIN DISTANCE TEST (distance ≤ 3)")
    print("=" * 70)
    lev_matches = find_levenshtein_matches(voynich_words, fermoy_vocab, max_distance=3)

    if lev_matches:
        lev_df = pd.DataFrame(lev_matches)
        print(f"\n{len(lev_matches)} matches found:")
        print(lev_df.to_string(index=False))

        # Group by Voynich word
        print("\nMatches by Voynich word:")
        for vword in voynich_words:
            hits = [m for m in lev_matches if m['voynich_word'] == vword]
            if hits:
                print(f"  {vword}: {len(hits)} match(es)")
                for hit in hits:
                    print(f"    → {hit['fermoy_term']} (distance={hit['distance']})")

        # Statistical test
        p_value = run_null_hypothesis_test(voynich_words, fermoy_vocab, len(lev_matches))
        print(f"\nBinomial test (null = 5% random match rate):")
        print(f"  Observed: {len(lev_matches)} matches")
        print(f"  p-value: {p_value:.4f}")
        if p_value < 0.05:
            print("  Result: SIGNIFICANT (p < 0.05)")
        else:
            print("  Result: NOT SIGNIFICANT")
    else:
        print("\nNo Levenshtein matches found.")

    print()

    # Run substring test
    print("=" * 70)
    print("SUBSTRING OVERLAP TEST")
    print("=" * 70)
    substring_matches = find_substring_matches(voynich_words, fermoy_vocab)

    if substring_matches:
        substr_df = pd.DataFrame(substring_matches)
        print(f"\n{len(substring_matches)} substring matches found:")
        print(substr_df.to_string(index=False))
    else:
        print("\nNo substring matches found.")

    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Pre-registration: analyses/fermoy_vocab_comparison_prereg.md")
    print(f"Voynich closing words: {len(voynich_words)}")
    print(f"Fermoy medical terms: {len(fermoy_vocab)}")
    print(f"Levenshtein matches (≤3): {len(lev_matches) if lev_matches else 0}")
    print(f"Substring matches: {len(substring_matches) if substring_matches else 0}")

    prediction = "≥8 Levenshtein matches AND ≥5 phonetic matches"
    actual = f"{len(lev_matches) if lev_matches else 0} Levenshtein + {len(substring_matches) if substring_matches else 0} substring"
    print(f"\nPrediction: {prediction}")
    print(f"Actual: {actual}")

    if len(lev_matches) >= 8 and len(substring_matches) >= 5:
        print("\nResult: SUPPORTED ✓")
    else:
        print("\nResult: NOT YET TESTED (waiting for full Fermoy vocabulary)")

if __name__ == "__main__":
    main()
