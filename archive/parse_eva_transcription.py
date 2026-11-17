#!/usr/bin/env python3
"""
Parse EVA (Extensible Voynich Alphabet) transcription format
and convert to standard transcription format for build_integrated.py
"""

import re
from pathlib import Path
from collections import defaultdict

print("=" * 80)
print("PARSING VOYNICH EVA TRANSCRIPTION")
print("=" * 80)

EVA_FILE = "Data/Zl3b-n.txt"
OUTPUT_FILE = "voynich_transcription_eva.txt"

if not Path(EVA_FILE).exists():
    print(f"ERROR: {EVA_FILE} not found")
    exit(1)

print(f"\nParsing {EVA_FILE}...")

# Parse EVA format
folios = defaultdict(lambda: {"lines": []})
current_folio = None
current_lines = []

with open(EVA_FILE, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        line = line.rstrip()

        # Folio marker: <f1r>, <f1v>, etc.
        folio_match = re.match(r'<(f\d+[rv])>', line)
        if folio_match:
            folio_id = folio_match.group(1)
            current_folio = folio_id
            print(f"  Found folio: {folio_id}")
            continue

        # Line content: <f1r.1,@P0> text goes here
        line_match = re.match(r'<(f\d+[rv])\.(\d+),([^>]+)>\s+(.+)', line)
        if line_match:
            folio_id = line_match.group(1)
            line_num = line_match.group(2)
            locus = line_match.group(3)
            text = line_match.group(4)

            # Clean up locus labels
            if locus.startswith('@'):
                locus_label = locus
            elif 'P0' in locus:
                locus_label = 'm'  # main area
            elif 'P' in locus:
                locus_label = locus
            else:
                locus_label = 'm'

            folios[folio_id]["lines"].append({
                "locus": locus_label,
                "text": text
            })

print(f"\n✓ Parsed {len(folios)} folios")
total_lines = sum(len(f['lines']) for f in folios.values())
print(f"✓ Parsed {total_lines} text lines")

# Convert to transcription format for build_integrated.py
# Format: folio_id: m: text | l: text | r: text
output_lines = []

for folio_id in sorted(folios.keys(), key=lambda x: (x[:-1], x[-1] == 'v')):
    lines = folios[folio_id]["lines"]

    # Group lines by locus
    by_locus = defaultdict(list)
    for line_entry in lines:
        locus = line_entry['locus']
        text = line_entry['text']
        by_locus[locus].append(text)

    # Build line: folio_id: m: text | l: text | r: text
    folio_line = f"{folio_id}: "
    parts = []

    for locus in ['m', '@P0', '@P1', '@P2']:  # main loci in order
        if locus in by_locus:
            locus_text = " ".join(by_locus[locus])
            if locus == 'm':
                parts.append(f"m: {locus_text}")
            elif locus == '@P0':
                parts.append(f"p0: {locus_text}")
            elif locus == '@P1':
                parts.append(f"p1: {locus_text}")
            elif locus == '@P2':
                parts.append(f"p2: {locus_text}")

    # Add any other loci not explicitly marked
    for locus in by_locus:
        if locus not in ['m', '@P0', '@P1', '@P2']:
            locus_text = " ".join(by_locus[locus])
            parts.append(f"{locus}: {locus_text}")

    folio_line += " | ".join(parts)
    output_lines.append(folio_line)

# Save output
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"\n✓ Converted to standard format")
print(f"✓ Saved to: {OUTPUT_FILE}")
print(f"✓ Ready for build_integrated.py")

print("\n" + "=" * 80)
print("NEXT STEP: Copy output to voynich_transcription.txt and run:")
print("  cp voynich_transcription_eva.txt voynich_transcription.txt")
print("  python3 build_integrated.py")
print("  python3 build_control.py")
print("=" * 80)
