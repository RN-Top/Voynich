#!/usr/bin/env python3
"""
Analyze downloaded Voynich images and create mapping to folio IDs in voynich_integrated.json
"""

import json
import re
from pathlib import Path
from collections import OrderedDict

print("=" * 80)
print("ANALYZING VOYNICH IMAGE TO FOLIO MAPPING")
print("=" * 80)

IMAGE_DIR = Path("images/yale")
INTEGRATED_FILE = "voynich_integrated.json"

if not IMAGE_DIR.exists():
    print(f"ERROR: {IMAGE_DIR} not found")
    exit(1)

# Extract folio labels from image filenames
print("\nPhase 1: Extract folio labels from images...")
image_files = sorted(IMAGE_DIR.glob("*.jpg"))
image_mapping = OrderedDict()

for img_path in image_files:
    filename = img_path.name
    # Format: NNN_LABEL.jpg where NNN is page order
    match = re.match(r'(\d+)_(.+)\.jpg$', filename)
    if match:
        page_order = int(match.group(1))
        label = match.group(2)
        image_mapping[filename] = {
            "page_order": page_order,
            "label": label,
            "path": str(img_path)
        }

print(f"✓ Found {len(image_mapping)} images")
print(f"  Page order: {min(m['page_order'] for m in image_mapping.values())} "
      f"to {max(m['page_order'] for m in image_mapping.values())}")

# Extract folio labels from images (deduplicate by label)
image_folios = []
image_labels = set()
for img_data in image_mapping.values():
    label = img_data['label']
    image_labels.add(label)
    image_folios.append(label)

print(f"✓ Unique folio labels in images: {len(image_labels)}")

# Load integrated data to get expected folios
print("\nPhase 2: Load expected folios from voynich_integrated.json...")
with open(INTEGRATED_FILE) as f:
    integrated_data = json.load(f)

expected_folios = [folio['folio_id'] for folio in integrated_data['folios']]
expected_labels = set(expected_folios)

print(f"✓ Expected folios in integrated data: {len(expected_labels)}")

# Compare
print("\n" + "=" * 80)
print("MAPPING ANALYSIS")
print("=" * 80)

images_in_expected = image_labels & expected_labels
images_not_in_expected = image_labels - expected_labels
expected_not_in_images = expected_labels - image_labels

print(f"\n✓ Matching images to expected folios: {len(images_in_expected)}")
print(f"⚠ Images NOT in expected folios: {len(images_not_in_expected)}")
if images_not_in_expected:
    for label in sorted(images_not_in_expected):
        print(f"    {label}")

print(f"\n⚠ Expected folios NOT in images: {len(expected_not_in_images)}")
if expected_not_in_images:
    # Group by type (foldout vs regular)
    foldouts = [l for l in expected_not_in_images if any(c.isdigit() for c in l.split('r')[1:] if c)]
    regular = [l for l in expected_not_in_images if l not in foldouts]

    if regular:
        print(f"\n  Regular pages missing ({len(regular)}):")
        for label in sorted(regular)[:10]:
            print(f"    {label}")
        if len(regular) > 10:
            print(f"    ... and {len(regular) - 10} more")

# Analyze foldouts in images
print("\n" + "=" * 80)
print("FOLDOUT ANALYSIS")
print("=" * 80)

foldout_images = {}
for img_name, img_data in image_mapping.items():
    label = img_data['label']
    if '_and_' in label or any(c.isdigit() for c in label.split('v')[1:] if c):
        foldout_images[img_name] = label

print(f"\nFoldouts in images: {len(foldout_images)}")
for img_name in sorted(foldout_images.keys()):
    print(f"  {img_name}")

# Generate mapping CSV
print("\n" + "=" * 80)
print("GENERATING MAPPING")
print("=" * 80)

mapping_data = []
for img_name, img_data in image_mapping.items():
    label = img_data['label']
    # Check if this label exists in integrated data
    exists_in_integrated = label in expected_labels

    mapping_data.append({
        "page_order": img_data['page_order'],
        "image_file": img_name,
        "folio_label": label,
        "in_integrated": "YES" if exists_in_integrated else "NO",
        "image_path": img_data['path']
    })

# Save mapping
mapping_file = "image_to_folio_mapping.json"
with open(mapping_file, 'w') as f:
    json.dump(mapping_data, f, indent=2)

print(f"✓ Saved mapping to: {mapping_file}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total images downloaded:        {len(image_mapping)}")
print(f"Unique folio labels in images:  {len(image_labels)}")
print(f"Expected folios in dataset:     {len(expected_labels)}")
print(f"Matching:                       {len(images_in_expected)}")
print(f"Images without matching folio:  {len(images_not_in_expected)}")
print(f"Expected folios without image:  {len(expected_not_in_images)}")
print(f"Foldout images detected:        {len(foldout_images)}")
print("=" * 80)
