#!/usr/bin/env python3
"""
COMPARATIVE IRISH TEXT TEST
============================
Tests whether Voynich matches Fermoy specifically, or if it matches
any Irish text from the same period equally well.

This answers: Is there a real connection to Fermoy, or is it just
that Voynich uses Irish-like vocabulary from ~1400?

Run: python3 analyses/comparative_irish_text_test.py
"""

import pandas as pd
from pathlib import Path
from Levenshtein import distance as lev_distance
from collections import Counter

def load_voynich():
    """Load Voynich vocabulary."""
    voynich_path = Path("data/ZL3b-n.txt")
    if not voynich_path.exists():
        print(f"ERROR: {voynich_path} not found")
        return None

    with open(voynich_path) as f:
        text = f.read()
    return list(set(text.split()))

def extract_vocabulary(text):
    """Extract cleaned vocabulary from text."""
    words = [w.strip('.,;:\'"-()[]{}') for w in text.split()]
    words = [w for w in words if len(w) > 2 and w.isalpha()]
    return list(set(words))

def load_fermoy_sections():
    """Load Fermoy and split into sections."""
    fermoy_path = Path("data/fermoy_ms23e29.txt")
    if not fermoy_path.exists():
        print(f"ERROR: {fermoy_path} not found")
        return None

    with open(fermoy_path) as f:
        text = f.read()

    # Split by major sections (marked by ## in the text)
    sections = text.split("##")

    # Extract vocabulary from each section
    fermoy_sections = {}
    for i, section in enumerate(sections):
        if len(section.strip()) > 100:  # Only use substantial sections
            vocab = extract_vocabulary(section)
            if len(vocab) > 50:  # Only if section has enough words
                fermoy_sections[f"Fermoy_Section_{i}"] = vocab

    return fermoy_sections

def count_matches_at_threshold(source_vocab, target_vocab, threshold=3):
    """Count pairs matching at Levenshtein distance <= threshold."""
    count = 0
    for source_word in source_vocab:
        for target_word in target_vocab:
            if lev_distance(source_word, target_word) <= threshold:
                count += 1
    return count

def run_test():
    """Run comparative test across Irish text sections."""

    print("=" * 80)
    print("COMPARATIVE IRISH TEXT TEST")
    print("=" * 80)
    print("\nQuestion: Does Voynich match Fermoy specifically, or any Irish text?")
    print("Method: Compare Voynich vocabulary against multiple Fermoy sections\n")

    # Load data
    print("Loading data...")
    voynich = load_voynich()
    fermoy_sections = load_fermoy_sections()

    if not voynich or not fermoy_sections:
        print("ERROR: Could not load required data")
        return

    print(f"  Voynich unique words: {len(voynich)}")
    print(f"  Fermoy sections found: {len(fermoy_sections)}")

    # Test each section
    print("\n" + "=" * 80)
    print("RESULTS: Voynich Matches Across Fermoy Sections")
    print("=" * 80)
    print(f"\nThreshold: Levenshtein distance ≤3\n")

    results = {}
    for section_name, section_vocab in sorted(fermoy_sections.items()):
        matches = count_matches_at_threshold(section_vocab, voynich, threshold=3)
        per_word = matches / len(section_vocab) if len(section_vocab) > 0 else 0

        results[section_name] = {
            'matches': matches,
            'vocab_size': len(section_vocab),
            'per_word': per_word
        }

        print(f"{section_name:20s} | Vocab: {len(section_vocab):5d} | Matches: {matches:7,} | Per-word: {per_word:6.1f}")

    # Analysis
    print("\n" + "=" * 80)
    print("INTERPRETATION")
    print("=" * 80)

    per_word_values = [r['per_word'] for r in results.values()]

    if per_word_values:
        avg_per_word = sum(per_word_values) / len(per_word_values)
        max_per_word = max(per_word_values)
        min_per_word = min(per_word_values)

        print(f"\nPer-word matching across sections:")
        print(f"  Average: {avg_per_word:6.1f} matches per word")
        print(f"  Maximum: {max_per_word:6.1f}")
        print(f"  Minimum: {min_per_word:6.1f}")

        if max_per_word > min_per_word * 1.3:
            print(f"\n✓ SECTIONS VARY SIGNIFICANTLY")
            print(f"  Some Fermoy sections match Voynich better than others.")
            print(f"  This suggests Voynich connects to SPECIFIC Fermoy content,")
            print(f"  not just generic Irish text from the period.")
        else:
            print(f"\n⚠ SECTIONS MATCH SIMILARLY")
            print(f"  All Fermoy sections match Voynich about equally well.")
            print(f"  This suggests Voynich matches ANY Irish text from ~1400,")
            print(f"  not specifically Fermoy medical content.")

    # Recommendation
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)

    if max_per_word > min_per_word * 1.3:
        print("""
The sections that match BEST are likely the most relevant.
Next: Examine what's in those high-matching sections.
Are they medical? Linguistic? Structural?
""")
    else:
        print("""
All sections match equally, which suggests Voynich just uses
Irish-like vocabulary from the ~1400 period.

To prove a real connection to your ancestor, you need to find:
1. Rare words unique to Fermoy medical texts + Voynich
2. Structural patterns Voynich follows from Fermoy specifically
3. Other Irish texts that DON'T match as well

Otherwise, the connection might just be the language.
""")

    print("=" * 80)

if __name__ == "__main__":
    run_test()
