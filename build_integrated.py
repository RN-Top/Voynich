#!/usr/bin/env python3
"""
Build voynich_integrated.json: unified file with folios in order.
Reads directly from EVA transcription file (Data/Zl3b-n.txt).
Combines folio ID, image paths, transcribed text (with locus labels),
and classification flags (text-only, image-only, foldout).
"""

import json
import re
from pathlib import Path
from collections import defaultdict, OrderedDict

print("=" * 80)
print("BUILDING VOYNICH_INTEGRATED.JSON FROM EVA TRANSCRIPTION")
print("=" * 80)

EVA_FILE = "Data/Zl3b-n.txt"
IMAGE_DIR = "voynich_manuscript/pages"

if not Path(EVA_FILE).exists():
    print(f"ERROR: {EVA_FILE} not found")
    exit(1)

# Parse EVA format directly from source file
print(f"\nReading {EVA_FILE}...")
folio_data = OrderedDict()  # Preserve insertion order
folio_order = []

with open(EVA_FILE, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        line = line.rstrip()

        # Folio marker: <f1r>, <f116v>, <f67r1>, <f67r2>, etc.
        folio_match = re.match(r'<(f\d+[rv](?:\d)?)>', line)
        if folio_match:
            folio_id = folio_match.group(1)
            if folio_id not in folio_data:
                folio_order.append(folio_id)
                folio_data[folio_id] = {"lines": []}
            continue

        # Line content: <f1r.1,@P0> text | <f116v.1,@Lx> text | etc.
        line_match = re.match(r'<(f\d+[rv](?:\d)?)\.\d+,([^>]+)>\s+(.+)', line)
        if line_match:
            folio_id = line_match.group(1)
            locus = line_match.group(2)
            text = line_match.group(3)

            if folio_id not in folio_data:
                folio_order.append(folio_id)
                folio_data[folio_id] = {"lines": []}

            folio_data[folio_id]["lines"].append({
                "locus": locus,
                "text": text
            })

print(f"✓ Parsed {len(folio_order)} folios from EVA file")

total_lines = sum(len(f['lines']) for f in folio_data.values())
print(f"✓ Total text lines: {total_lines}")

# Build integrated data structure
integrated_data = {
    "metadata": {
        "description": "Voynich Manuscript integrated data: folio order with text and images",
        "folios_total": 0,
        "text_only_count": 0,
        "image_only_count": 0,
        "integrated_count": 0,
        "foldout_count": 0,
        "unmatched_count": 0
    },
    "folios": []
}

# Foldout pages (multi-panel spreads)
FOLDOUTS = {
    'f67r1', 'f67r2', 'f67v2', 'f67v1',
    'f68r1', 'f68r2', 'f68r3', 'f68v3', 'f68v2', 'f68v1',
    'f70r1', 'f70r2', 'f70v2', 'f70v1',
    'f72r1', 'f72r2', 'f72r3', 'f72v3', 'f72v2', 'f72v1',
    'f85r1', 'f85r2',
    'f86v4', 'f86v6', 'f86v5', 'f86v3',
    'f89r1', 'f89r2', 'f89v2', 'f89v1',
    'f90r1', 'f90r2', 'f90v2', 'f90v1',
    'f95r1', 'f95r2', 'f95v2', 'f95v1',
    'f102r1', 'f102r2', 'f102v2', 'f102v1'
}

print("\nMatching folios with images and building entries...")

stats = defaultdict(int)
for folio_id in folio_order:
    # Find image file (multiple image formats possible)
    image_paths = []
    for pattern in [f"{folio_id}.png", f"{folio_id}.jpg", f"*{folio_id}*"]:
        matches = list(Path(IMAGE_DIR).glob(pattern)) if Path(IMAGE_DIR).exists() else []
        image_paths.extend([str(m) for m in matches])

    # Remove duplicates and sort
    image_paths = sorted(list(set(image_paths)))

    # Classify folio
    has_text = folio_id in folio_data and len(folio_data[folio_id]['lines']) > 0
    has_image = len(image_paths) > 0
    is_foldout = folio_id in FOLDOUTS

    if is_foldout:
        folio_type = "foldout"
        stats['foldout'] += 1
    elif has_text and has_image:
        folio_type = "integrated"
        stats['integrated'] += 1
    elif has_text:
        folio_type = "text-only"
        stats['text_only'] += 1
    elif has_image:
        folio_type = "image-only"
        stats['image_only'] += 1
    else:
        folio_type = "unmatched"
        stats['unmatched'] += 1

    # Get text lines for this folio
    text_lines = []
    if has_text:
        text_lines = folio_data[folio_id]['lines']

    # Build folio entry
    folio_entry = {
        "folio_id": folio_id,
        "type": folio_type,
        "image_paths": image_paths,
        "text_lines": text_lines,
        "has_text": has_text,
        "has_image": has_image
    }

    integrated_data['folios'].append(folio_entry)

print(f"✓ Processed {len(folio_order)} folios")
print(f"  - Integrated (text + image): {stats['integrated']}")
print(f"  - Text-only: {stats['text_only']}")
print(f"  - Image-only: {stats['image_only']}")
print(f"  - Foldout: {stats['foldout']}")
print(f"  - Unmatched: {stats['unmatched']}")

# Update metadata
integrated_data['metadata']['folios_total'] = len(integrated_data['folios'])
integrated_data['metadata']['integrated_count'] = stats['integrated']
integrated_data['metadata']['text_only_count'] = stats['text_only']
integrated_data['metadata']['image_only_count'] = stats['image_only']
integrated_data['metadata']['foldout_count'] = stats['foldout']
integrated_data['metadata']['unmatched_count'] = stats['unmatched']

print("\nSaving integrated file...")
with open('voynich_integrated.json', 'w', encoding='utf-8') as f:
    json.dump(integrated_data, f, indent=2, ensure_ascii=False)

print("✓ Saved: voynich_integrated.json")

print("\n" + "=" * 80)
print("OUTPUT SUMMARY")
print("=" * 80)
print(f"Folios processed:        {integrated_data['metadata']['folios_total']}")
print(f"Total text lines:        {total_lines}")
print(f"Integrated (text+image): {integrated_data['metadata']['integrated_count']}")
print(f"Text-only:               {integrated_data['metadata']['text_only_count']}")
print(f"Image-only:              {integrated_data['metadata']['image_only_count']}")
print(f"Foldouts:                {integrated_data['metadata']['foldout_count']}")
print(f"Unmatched:               {integrated_data['metadata']['unmatched_count']}")
print("=" * 80)
