#!/usr/bin/env python3
"""
Build voynich_control.json: negative control for integration analysis.
Takes voynich_integrated.json and shuffles INDIVIDUAL WORDS across folios
while preserving each folio's word count and overall word frequencies.
This breaks any real folio-to-folio relationships while keeping the
manuscript "text realistic" for comparison.
"""

import json
import random
from collections import Counter
from pathlib import Path

print("=" * 80)
print("BUILDING VOYNICH_CONTROL.JSON - NEGATIVE CONTROL")
print("=" * 80)

# Load integrated data
INPUT_FILE = 'voynich_integrated.json'

if not Path(INPUT_FILE).exists():
    print(f"ERROR: {INPUT_FILE} not found")
    print("Run build_integrated.py first")
    exit(1)

print(f"\nLoading {INPUT_FILE}...")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    integrated_data = json.load(f)

print(f"✓ Loaded {len(integrated_data['folios'])} folios")

# Extract all words and remember each folio's word count
all_words = []
folio_word_counts = []  # Track how many words each folio should have

for folio in integrated_data['folios']:
    folio_word_count = 0
    for line in folio['text_lines']:
        if 'words' in line:
            words = line['words']
        else:
            # Fallback: if words not in text_lines, extract from text
            import re
            text = line['text']
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'<![^>]*>', '', text)
            text = re.sub(r'@[A-Za-z0-9;]+', '', text)
            text = re.sub(r'<%[^>]*>', '', text)
            text = re.sub(r'<\$>', '', text)
            words = [w.strip() for w in re.split(r'[.,]', text) if w.strip()]

        all_words.extend(words)
        folio_word_count += len(words)

    folio_word_counts.append(folio_word_count)

print(f"✓ Extracted {len(all_words)} total words")

# Count word frequencies (for validation)
word_freq_original = Counter(all_words)
print(f"✓ Original vocabulary: {len(word_freq_original)} unique forms")
print(f"  Sample frequency distribution:")
for word, count in list(word_freq_original.most_common(5)):
    print(f"    {word}: {count} occurrences")

# Shuffle individual words across folios
print("\nShuffling words across folios (preserving each folio's word count)...")
random.seed(42)  # Fixed seed for reproducibility
shuffled_words = all_words.copy()
random.shuffle(shuffled_words)

# Verify word frequencies are preserved
word_freq_shuffled = Counter(shuffled_words)
print(f"✓ Shuffled vocabulary: {len(word_freq_shuffled)} unique forms")
print(f"  Sample frequency distribution:")
for word, count in list(word_freq_shuffled.most_common(5)):
    print(f"    {word}: {count} occurrences")

# Verify they match
if word_freq_original == word_freq_shuffled:
    print("✓ Word frequencies preserved (exact match)")
else:
    print("⚠ Word frequencies differ (ERROR!)")
    exit(1)

# Rebuild folios with shuffled words
control_data = {
    "metadata": integrated_data['metadata'].copy(),
    "folios": []
}

control_data['metadata']['control_type'] = "negative_control_shuffled_words"
control_data['metadata']['shuffle_seed'] = 42

word_index = 0
for i, folio in enumerate(integrated_data['folios']):
    num_words = folio_word_counts[i]

    # Get shuffled words for this folio
    shuffled_folio_words = shuffled_words[word_index:word_index + num_words]
    word_index += num_words

    # Rebuild text_lines with shuffled words
    # We need to distribute shuffled words back into the line structure
    new_text_lines = []
    words_used = 0

    for line_entry in folio['text_lines']:
        line_word_count = line_entry['word_count']

        # Get words for this line
        line_words = shuffled_folio_words[words_used:words_used + line_word_count]
        words_used += line_word_count

        # Reconstruct text from words (rejoin with dots as separators)
        new_text = '.'.join(line_words)

        # Build new line entry with shuffled text
        new_line = {
            "locus": line_entry['locus'],
            "text": new_text,
            "words": line_words,
            "word_count": len(line_words)
        }
        new_text_lines.append(new_line)

    # Build folio entry with shuffled words
    folio_entry = {
        "folio_id": folio['folio_id'],
        "type": folio['type'],
        "image_paths": folio['image_paths'],
        "text_lines": new_text_lines,
        "has_text": folio['has_text'],
        "has_image": folio['has_image'],
        "word_count": num_words
    }

    control_data['folios'].append(folio_entry)

print(f"\n✓ Redistributed {len(shuffled_words)} words across {len(control_data['folios'])} folios")
print(f"  Word distribution matches original (each folio's word count preserved)")

# Save control file
output_file = 'voynich_control.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(control_data, f, indent=2, ensure_ascii=False)

print(f"✓ Saved: {output_file}")

print("\n" + "=" * 80)
print("CONTROL FILE PROPERTIES")
print("=" * 80)
print(f"Same folio structure:  ✓ Yes (word count per folio preserved)")
print(f"Same word frequencies: ✓ Yes (vocabulary preserved exactly)")
print(f"Same images:           ✓ Yes (image paths unchanged)")
print(f"Different text layout: ✓ Yes (words shuffled across folios)")
print("\nThis file can be used to test whether analysis results are specific")
print("to the REAL text-image relationships or just artifact of statistics.")
print("=" * 80)
