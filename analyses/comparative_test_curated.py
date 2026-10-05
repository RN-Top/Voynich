#!/usr/bin/env python3
"""
COMPARATIVE TEST WITH CURATED VOCABULARY
Test Voynich against REAL medical terms only (common words removed).
"""

import pandas as pd
from pathlib import Path
from Levenshtein import distance as lev_distance

def load_voynich():
    voynich_path = Path("data/ZL3b-n.txt")
    with open(voynich_path) as f:
        text = f.read()
    return list(set(text.split()))

def load_medical_vocab_curated():
    """Load curated medical vocabulary (common words removed)."""
    vocab_path = Path("analyses/fermoy_medical_vocab_curated.csv")
    df = pd.read_csv(vocab_path)
    return df['term'].unique().tolist()

def extract_vocabulary_from_fermoy():
    """Extract all unique words from Fermoy."""
    fermoy_path = Path("data/fermoy_ms23e29.txt")
    with open(fermoy_path) as f:
        text = f.read()

    words = [w.strip('.,;:\'"-()[]{}') for w in text.split()]
    words = [w for w in words if len(w) > 2 and w.isalpha()]
    return list(set(words))

def count_matches(source_vocab, target_vocab, threshold=3):
    """Count Levenshtein matches."""
    count = 0
    for source in source_vocab:
        for target in target_vocab:
            if lev_distance(source, target) <= threshold:
                count += 1
    return count

def main():
    print("=" * 80)
    print("CURATED VOCABULARY TEST: Real Medical Terms vs Voynich")
    print("=" * 80)

    # Load data
    print("\nLoading data...")
    voynich = load_voynich()
    medical_curated = load_medical_vocab_curated()
    fermoy_all = extract_vocabulary_from_fermoy()

    # Create control: non-medical Fermoy
    medical_lower = [m.lower() for m in medical_curated]
    non_medical = [w for w in fermoy_all if w.lower() not in medical_lower]

    print(f"  Voynich unique words: {len(voynich)}")
    print(f"  Medical vocabulary (curated): {len(medical_curated)}")
    print(f"  Non-medical Fermoy (control): {len(non_medical)}")

    # Test at threshold 3
    print(f"\n" + "=" * 80)
    print("RESULTS: Levenshtein distance ≤3")
    print("=" * 80)

    medical_matches = count_matches(medical_curated, voynich, 3)
    control_matches = count_matches(non_medical, voynich, 3)

    medical_per_word = medical_matches / len(medical_curated)
    control_per_word = control_matches / len(non_medical)

    ratio = medical_matches / control_matches if control_matches > 0 else 0

    print(f"\nCurated medical vocabulary: {medical_matches:,} matches ({medical_per_word:.1f} per term)")
    print(f"Non-medical control:       {control_matches:,} matches ({control_per_word:.1f} per word)")
    print(f"Signal strength (ratio):   {ratio:.2f}x")

    print(f"\n" + "=" * 80)
    print("INTERPRETATION")
    print("=" * 80)

    if ratio > 2:
        print(f"\n✓ CURATED MEDICAL VOCABULARY SIGNAL IS REAL")
        print(f"  Medical terms match {ratio:.1f}x better than non-medical Fermoy.")
        print(f"  This suggests genuine connection to medical content.")
    elif ratio > 1:
        print(f"\n⚠ WEAK SIGNAL")
        print(f"  Medical vocabulary only matches {ratio:.1f}x better than control.")
    else:
        print(f"\n✗ NO SIGNAL")
        print(f"  Medical vocabulary matches WORSE than control.")
        print(f"  The connection is not medical-specific.")

    # Also test individual medical categories
    print(f"\n" + "=" * 80)
    print("BY CATEGORY")
    print("=" * 80)

    vocab_df = pd.read_csv(Path("analyses/fermoy_medical_vocab_curated.csv"))

    for category in vocab_df['category'].unique():
        cat_words = vocab_df[vocab_df['category'] == category]['term'].tolist()
        cat_matches = count_matches(cat_words, voynich, 3)
        cat_per_word = cat_matches / len(cat_words) if len(cat_words) > 0 else 0
        print(f"{category:12s}: {cat_matches:6,} matches ({cat_per_word:6.1f} per term) | {len(cat_words):3d} terms")

if __name__ == "__main__":
    main()
