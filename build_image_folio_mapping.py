#!/usr/bin/env python3
"""
Build detailed mapping from Yale images to folio IDs in voynich_integrated.json
Handles simple pages, multi-page foldouts, and complex panel spreads.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

print("=" * 80)
print("BUILDING YALE IMAGE TO FOLIO MAPPING")
print("=" * 80)

IMAGE_DIR = Path("images/yale")
INTEGRATED_FILE = "voynich_integrated.json"

# Load integrated data to get all folio IDs
with open(INTEGRATED_FILE) as f:
    integrated_data = json.load(f)

all_folios = {folio['folio_id'] for folio in integrated_data['folios']}

# Parse Yale index.csv to get official labels
print("\nPhase 1: Parse Yale image index...")
image_index = {}
with open(IMAGE_DIR / "index.csv") as f:
    lines = f.readlines()
    headers = lines[0].strip().split(',')
    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) >= 2:
            filename = parts[0].strip()
            label = parts[1].strip().strip("[]'\"")
            image_index[filename] = label

print(f"✓ Loaded {len(image_index)} images from index")

# Build mapping strategy
mapping = []
unmapped = []
mapped_folios = set()

print("\nPhase 2: Create folio mappings...")

for filename in sorted(image_index.keys()):
    yale_label = image_index[filename]

    # Extract page order from filename
    match = re.match(r'(\d+)_(.+)', filename.replace('.jpg', ''))
    page_order = int(match.group(1)) if match else -1

    # Strategy: Map Yale labels to folio IDs

    # Skip front/back matter
    if yale_label in ['Front cover', 'Inside front cover', 'Back flyleaf recto',
                      'Back flyleaf verso/inside back cover', 'Back cover',
                      'Spine', 'Fore-edge', 'Head', 'Tail']:
        continue

    # Strategy 1: Simple pages (1r, 1v, 2r, etc.)
    simple_match = re.match(r'^(\d+)([rv])$', yale_label)
    if simple_match:
        folio_num = simple_match.group(1)
        side = simple_match.group(2)
        folio_id = f"f{folio_num}{side}"

        if folio_id in all_folios:
            mapping.append({
                "page_order": page_order,
                "image_file": filename,
                "yale_label": yale_label,
                "folio_ids": [folio_id],
                "type": "simple_page",
                "notes": ""
            })
            mapped_folios.add(folio_id)
            continue

    # Strategy 2: Multi-page spreads (e.g., "69v and 70r", "88v and 89r")
    multipage_match = re.match(r'^(\d+)([rv])\s+and\s+(\d+)([rv])$', yale_label)
    if multipage_match:
        folio1 = f"f{multipage_match.group(1)}{multipage_match.group(2)}"
        folio2 = f"f{multipage_match.group(3)}{multipage_match.group(4)}"
        folios = []
        if folio1 in all_folios:
            folios.append(folio1)
            mapped_folios.add(folio1)
        if folio2 in all_folios:
            folios.append(folio2)
            mapped_folios.add(folio2)

        if folios:
            mapping.append({
                "page_order": page_order,
                "image_file": filename,
                "yale_label": yale_label,
                "folio_ids": folios,
                "type": "multi_page_spread",
                "notes": "Single image shows two adjacent pages"
            })
            continue

    # Strategy 3: Partial foldout pages (e.g., "70v part", "89v part")
    partial_match = re.match(r'^(\d+)([rv])\s+part$', yale_label)
    if partial_match:
        folio_num = partial_match.group(1)
        side = partial_match.group(2)
        folio_id = f"f{folio_num}{side}"

        if folio_id in all_folios:
            mapping.append({
                "page_order": page_order,
                "image_file": filename,
                "yale_label": yale_label,
                "folio_ids": [folio_id],
                "type": "partial_page",
                "notes": "Part of a large foldout spread"
            })
            mapped_folios.add(folio_id)
            continue

    # Strategy 4: Complex foldout panels
    # Pattern: "85r part..." or "85r part 86v part..."
    complex_foldout_match = re.search(r'(\d+)([rv])', yale_label)
    if complex_foldout_match and 'part' in yale_label and 'foldout' in yale_label:
        # These are parts of complex foldouts
        # Need to map based on folio structure
        folio_base = f"f{complex_foldout_match.group(1)}{complex_foldout_match.group(2)}"

        # Find matching panel numbers in our dataset
        matching_panels = [f for f in all_folios if f.startswith(folio_base) and len(f) > len(folio_base)]

        if matching_panels:
            mapping.append({
                "page_order": page_order,
                "image_file": filename,
                "yale_label": yale_label,
                "folio_ids": sorted(matching_panels),
                "type": "complex_foldout",
                "notes": f"Complex foldout - maps to panels: {', '.join(sorted(matching_panels))}"
            })
            mapped_folios.update(matching_panels)
            continue

    # If we get here, it's unmapped
    unmapped.append({
        "page_order": page_order,
        "image_file": filename,
        "yale_label": yale_label
    })

# Find unmapped folios
unmapped_folios = all_folios - mapped_folios

# Generate report
print("\n" + "=" * 80)
print("MAPPING RESULTS")
print("=" * 80)

print(f"\n✓ Successfully mapped: {len(mapping)} images")
print(f"⚠ Unmapped images: {len(unmapped)}")
print(f"⚠ Unmapped folios: {len(unmapped_folios)}")

# Show summary by type
type_counts = defaultdict(int)
for m in mapping:
    type_counts[m['type']] += 1

print(f"\nMapped by type:")
for mtype, count in sorted(type_counts.items()):
    print(f"  {mtype:25s}: {count:3d}")

# Show some examples
print(f"\nExample mappings:")
for m in mapping[:10]:
    print(f"  {m['image_file']:30s} → {', '.join(m['folio_ids'])}")

if unmapped:
    print(f"\nUnmapped images (first 10):")
    for u in unmapped[:10]:
        print(f"  {u['image_file']:30s} ({u['yale_label']})")

if unmapped_folios:
    print(f"\nUnmapped folios (first 20):")
    for f in sorted(unmapped_folios)[:20]:
        print(f"  {f}")

# Save detailed mapping
print("\n" + "=" * 80)
print("SAVING MAPPING FILES")
print("=" * 80)

with open('image_to_folio_detailed.json', 'w') as f:
    json.dump(mapping, f, indent=2)
print(f"✓ Saved detailed mapping: image_to_folio_detailed.json ({len(mapping)} mappings)")

with open('unmapped_images.json', 'w') as f:
    json.dump(unmapped, f, indent=2)
print(f"✓ Saved unmapped images: unmapped_images.json ({len(unmapped)} images)")

with open('unmapped_folios.json', 'w') as f:
    json.dump(sorted(unmapped_folios), f, indent=2)
print(f"✓ Saved unmapped folios: unmapped_folios.json ({len(unmapped_folios)} folios)")

# Final summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total Yale images:        {len(image_index)}")
print(f"Front/back matter:        {len(image_index) - len(mapping) - len(unmapped)}")
print(f"Mapped to folios:         {len(mapping)}")
print(f"Unmapped images:          {len(unmapped)}")
print(f"Folios with images:       {len(mapped_folios)}")
print(f"Folios without images:    {len(unmapped_folios)}")
print("=" * 80)
