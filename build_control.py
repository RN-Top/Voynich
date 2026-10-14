#!/usr/bin/env python3
"""
Build voynich_control.json: negative control for integration analysis.
Takes voynich_integrated.json and shuffles text ACROSS folios while
preserving word frequencies and overall text statistics.
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

# Extract all text lines
all_text_lines = []
folio_structure = []

for folio in integrated_data['folios']:
    text_lines = folio['text_lines']
    all_text_lines.extend(text_lines)
    folio_structure.append(len(text_lines))  # Remember how many lines each folio had

print(f"✓ Extracted {len(all_text_lines)} text lines total")

# Count word frequencies (for validation)
all_words = []
for line_entry in all_text_lines:
    words = line_entry['text'].split()
    all_words.extend(words)

word_freq_original = Counter(all_words)
print(f"✓ Original vocabulary: {len(word_freq_original)} unique forms")
print(f"  Sample frequency distribution:")
for word, count in list(word_freq_original.most_common(5)):
    print(f"    {word}: {count} occurrences")

# Shuffle text lines ACROSS folios
print("\nShuffling text across folios...")
random.seed(42)  # Fixed seed for reproducibility
shuffled_text_lines = all_text_lines.copy()
random.shuffle(shuffled_text_lines)

# Verify word frequencies are preserved
shuffled_words = []
for line_entry in shuffled_text_lines:
    words = line_entry['text'].split()
    shuffled_words.extend(words)

word_freq_shuffled = Counter(shuffled_words)
print(f"✓ Shuffled vocabulary: {len(word_freq_shuffled)} unique forms")
print(f"  Sample frequency distribution:")
for word, count in list(word_freq_shuffled.most_common(5)):
    print(f"    {word}: {count} occurrences")

# Verify they match
if word_freq_original == word_freq_shuffled:
    print("✓ Word frequencies preserved (exact match)")
else:
    print("⚠ Word frequencies differ (minor differences OK)")

# Rebuild folios with shuffled text
control_data = {
    "metadata": integrated_data['metadata'].copy(),
    "folios": []
}

control_data['metadata']['control_type'] = "negative_control_shuffled_text"
control_data['metadata']['shuffle_seed'] = 42

line_index = 0
for i, folio in enumerate(integrated_data['folios']):
    num_lines = folio_structure[i]

    # Get shuffled lines for this folio
    shuffled_folio_lines = shuffled_text_lines[line_index:line_index + num_lines]
    line_index += num_lines

    # Build folio entry with shuffled text
    folio_entry = {
        "folio_id": folio['folio_id'],
        "type": folio['type'],
        "image_paths": folio['image_paths'],  # Keep same images
        "text_lines": shuffled_folio_lines,   # Shuffled text
        "has_text": folio['has_text'],
        "has_image": folio['has_image']
    }

    control_data['folios'].append(folio_entry)

print(f"\n✓ Redistributed {len(shuffled_text_lines)} lines across {len(control_data['folios'])} folios")
print(f"  Line distribution matches original")

# Save control file
output_file = 'voynich_control.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(control_data, f, indent=2, ensure_ascii=False)

print(f"✓ Saved: {output_file}")

print("\n" + "=" * 80)
print("CONTROL FILE PROPERTIES")
print("=" * 80)
print(f"Same folio structure:  ✓ Yes (line distribution preserved)")
print(f"Same word frequencies: ✓ Yes (vocabulary preserved)")
print(f"Same images:           ✓ Yes (image paths unchanged)")
print(f"Different text layout: ✓ Yes (text shuffled across folios)")
print("\nThis file can be used to test whether analysis results are specific")
print("to the REAL text-image relationships or just artifact of statistics.")
print("=" * 80)
