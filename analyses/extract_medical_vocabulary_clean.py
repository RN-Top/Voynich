#!/usr/bin/env python3
"""
CLEAN MEDICAL VOCABULARY EXTRACTION
====================================
Extracts medical vocabulary from ONLY the documented medical fragments
(XVII, XVIII, XIX) in the Fermoy manuscript, filtering out common words.

This replaces the contaminated vocabulary extraction that included common words
like "begins," "hand," "king," "old," etc.
"""

from pathlib import Path
import re

def load_fermoy():
    """Load Fermoy manuscript."""
    fermoy_path = Path("data/fermoy_ms23e29.txt")
    if not fermoy_path.exists():
        print(f"ERROR: {fermoy_path} not found")
        return None

    with open(fermoy_path) as f:
        return f.read()

def extract_medical_fragments(text):
    """Extract sections XVII, XVIII, XIX from Fermoy."""

    # Find sections by their markers
    fragments = {}

    section_markers = [
        ("XVII", r"\(XVII\.\)"),
        ("XVIII", r"\(XVIII\.\)"),
        ("XIX", r"\(XIX\.\)")
    ]

    for label, pattern in section_markers:
        match = re.search(pattern, text)
        if match:
            start = match.start()
            # Find next section marker to know where this section ends
            next_match = re.search(r"\(XX\.\)", text[start:])
            if next_match:
                end = start + next_match.start()
            else:
                end = len(text)

            fragments[label] = text[start:end]
            print(f"✓ Found section {label}: {end - start} characters")
        else:
            print(f"✗ Section {label} not found")

    return fragments

def extract_words(text):
    """Extract and clean words from text."""
    # Remove special characters, keep only alphanumeric
    words = re.findall(r"\b[a-záéíóúàèìòùâêîôûäëïöü]+\b", text, re.IGNORECASE)
    return [w.lower() for w in words if len(w) > 2]

def filter_common_words(words):
    """Remove common English and Irish words."""

    # Common stop words to exclude
    common = {
        # English
        "the", "and", "that", "with", "this", "from", "was", "for", "are", "but",
        "have", "been", "will", "can", "not", "all", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine", "ten", "page", "leaf", "leaves",
        "part", "text", "line", "word", "letters", "hand", "begins", "beginning",
        "end", "ending", "following", "fragment", "consists", "consists", "marked",
        "margin", "margins", "page", "pages", "paging", "pagination",
        # Generic medical words already extracted
        "medical", "begins", "lying", "old", "king", "declared", "road", "latin",
        "mss", "obscure", "disease", "ill", "fatal", "cure", "physicians",
        # Irish common
        "an", "in", "is", "or", "on", "at", "to", "do", "be", "go", "see",
    }

    return [w for w in words if w not in common and len(w) > 3]

def main():
    """Extract clean medical vocabulary."""

    print("=" * 80)
    print("CLEAN MEDICAL VOCABULARY EXTRACTION")
    print("=" * 80)

    # Load text
    text = load_fermoy()
    if not text:
        return

    # Extract medical fragments
    print("\nExtracting medical fragments (XVII, XVIII, XIX)...\n")
    fragments = extract_medical_fragments(text)

    if not fragments:
        print("ERROR: Could not extract medical fragments")
        return

    # Extract and clean vocabulary from each fragment
    print("\nExtracting medical vocabulary...\n")

    all_medical_words = []

    for fragment_label, fragment_text in fragments.items():
        words = extract_words(fragment_text)
        print(f"Fragment {fragment_label}: {len(words)} total words extracted")

        # Get unique words
        unique_words = list(set(words))
        print(f"  → {len(unique_words)} unique words")

        all_medical_words.extend(unique_words)

    # Get unique words across all fragments
    medical_vocab = list(set(all_medical_words))
    medical_vocab.sort()

    print(f"\nTotal unique medical words (all fragments): {len(medical_vocab)}")

    # Filter out common words
    clean_vocab = filter_common_words(medical_vocab)
    clean_vocab.sort()

    print(f"After filtering common words: {len(clean_vocab)} medical terms")

    # Show sample
    print(f"\nSample of extracted medical vocabulary:")
    for word in clean_vocab[:50]:
        print(f"  {word}")

    # Save to file
    output_path = Path("analyses/fermoy_medical_vocab_clean.txt")
    with open(output_path, 'w') as f:
        f.write('\n'.join(clean_vocab))

    print(f"\n✓ Saved to: {output_path}")

    # Create CSV version for consistency
    import csv
    csv_path = Path("analyses/fermoy_medical_vocab_clean.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'category', 'latin_root', 'meaning'])
        for term in clean_vocab:
            writer.writerow([term, 'medical', '', ''])

    print(f"✓ Saved CSV to: {csv_path}")

if __name__ == "__main__":
    main()
