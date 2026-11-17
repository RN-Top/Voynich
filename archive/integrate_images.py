#!/usr/bin/env python3
"""
Integrate Yale image mappings into voynich_integrated.json
Adds image_files list to each folio based on folio_to_images mapping
"""

import json
from pathlib import Path

print("=" * 80)
print("INTEGRATING YALE IMAGES INTO VOYNICH_INTEGRATED.JSON")
print("=" * 80)

# Load files
print("\nLoading data...")
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

with open('folio_to_images.json') as f:
    folio_to_images = json.load(f)

with open('still_unmapped_folios.json') as f:
    still_unmapped = json.load(f)

print(f"✓ Loaded integrated dataset: {len(integrated['folios'])} folios")
print(f"✓ Loaded folio→images mapping: {len(folio_to_images)} folios with images")
print(f"✓ Identified {len(still_unmapped)} folios still unmapped")

# Add image_files to each folio
print("\nIntegrating images into folio entries...")

images_added = 0
folios_with_images = 0

for folio_entry in integrated['folios']:
    folio_id = folio_entry['folio_id']

    if folio_id in folio_to_images:
        image_files = folio_to_images[folio_id]
        folio_entry['image_files'] = image_files

        # Convert to full paths
        full_paths = [f"images/yale/{img}" for img in image_files]
        folio_entry['image_paths'] = full_paths

        images_added += len(image_files)
        folios_with_images += 1
    else:
        # No images for this folio
        folio_entry['image_files'] = []
        folio_entry['image_paths'] = []

print(f"✓ Added image files to {folios_with_images} folios")
print(f"✓ Total image links added: {images_added}")

# Update metadata
integrated['metadata']['folios_with_images'] = folios_with_images
integrated['metadata']['folios_without_images'] = len(integrated['folios']) - folios_with_images
integrated['metadata']['yale_image_coverage'] = f"{100 * folios_with_images / len(integrated['folios']):.1f}%"
integrated['metadata']['total_yale_images_linked'] = images_added

print("\nMetadata updated:")
print(f"  Folios with images: {integrated['metadata']['folios_with_images']}")
print(f"  Folios without images: {integrated['metadata']['folios_without_images']}")
print(f"  Coverage: {integrated['metadata']['yale_image_coverage']}")

# Save updated file
print("\nSaving updated integrated file...")
with open('voynich_integrated.json', 'w') as f:
    json.dump(integrated, f, indent=2, ensure_ascii=False)

print(f"✓ Saved: voynich_integrated.json")

# Show sample entries
print("\n" + "=" * 80)
print("SAMPLE ENTRIES (with images)")
print("=" * 80)

for folio in integrated['folios'][:3]:
    print(f"\n{folio['folio_id']}:")
    print(f"  Type: {folio['type']}")
    print(f"  Images: {folio['image_files']}")
    print(f"  Paths: {folio['image_paths']}")

# Show a folio with multiple images
for folio in integrated['folios']:
    if len(folio.get('image_files', [])) > 1:
        print(f"\n{folio['folio_id']} (multi-image foldout):")
        print(f"  Type: {folio['type']}")
        print(f"  Images: {folio['image_files']}")
        break

# Show a folio without images
for folio in integrated['folios']:
    if not folio.get('image_files', []):
        print(f"\n{folio['folio_id']} (NO IMAGES):")
        print(f"  Type: {folio['type']}")
        print(f"  Has text: {folio['has_text']}")
        break

print("\n" + "=" * 80)
print("INTEGRATION COMPLETE")
print("=" * 80)
print(f"Dataset: {len(integrated['folios'])} folios")
print(f"With images: {folios_with_images} ({integrated['metadata']['yale_image_coverage']})")
print(f"Without images: {integrated['metadata']['folios_without_images']}")
print(f"Total image links: {images_added}")
print("=" * 80)
