#!/usr/bin/env python3
"""
Manual mapping of Yale foldout images to dataset folio panels
Uses folio numbers and image descriptions to intelligently assign panels
"""

import json
from pathlib import Path

print("=" * 80)
print("MANUAL FOLDOUT MAPPING")
print("=" * 80)

# Load existing mapping
with open('image_to_folio_detailed.json') as f:
    existing_mapping = json.load(f)

with open('unmapped_images.json') as f:
    unmapped_images = json.load(f)

with open('unmapped_folios.json') as f:
    unmapped_folios = json.load(f)

with open('voynich_integrated.json') as f:
    integrated = json.load(f)

all_folios = {folio['folio_id']: folio for folio in integrated['folios']}

# Parse unmapped images
print(f"\nUnmapped images to process: {len(unmapped_images)}")
print(f"Unmapped folios to match: {len(unmapped_folios)}\n")

additional_mappings = []
unresolvable = []

for img in unmapped_images:
    yale_label = img['yale_label']
    filename = img['image_file']
    page_order = img['page_order']

    folios_for_image = []
    mapping_note = ""

    # Strategy 1: Simple foldout pages (67r, 68v, etc.) that have multi-panel counterparts
    # These are whole pages that in our dataset are split into numbered panels
    import re
    simple_match = re.match(r'^(\d+)([rv])(\s+\(part\))?$', yale_label)

    if simple_match:
        folio_num = simple_match.group(1)
        side = simple_match.group(2)
        is_partial = simple_match.group(3) is not None

        # Find all folios matching this base (e.g., f67r1, f67r2 for 67r)
        base = f"f{folio_num}{side}"
        matching = [f for f in unmapped_folios if f.startswith(base) and len(f) > len(base)]

        if matching:
            folios_for_image = sorted(matching)
            if is_partial:
                mapping_note = f"Part of {base} - maps to all {side} panels"
            else:
                mapping_note = f"Full page {yale_label} - contains all {len(folios_for_image)} panels"

    # Strategy 2: Multi-page foldout spreads (e.g., "85v and 86r (foldout)")
    multipage_foldout = re.match(r'^(\d+)([rv])\s+and\s+(\d+)([rv])\s+\(foldout\)$', yale_label)

    if multipage_foldout and not folios_for_image:
        folio1_num = multipage_foldout.group(1)
        folio1_side = multipage_foldout.group(2)
        folio2_num = multipage_foldout.group(3)
        folio2_side = multipage_foldout.group(4)

        base1 = f"f{folio1_num}{folio1_side}"
        base2 = f"f{folio2_num}{folio2_side}"

        matching1 = [f for f in unmapped_folios if f.startswith(base1) and len(f) > len(base1)]
        matching2 = [f for f in unmapped_folios if f.startswith(base2) and len(f) > len(base2)]

        if matching1 or matching2:
            folios_for_image = sorted(matching1 + matching2)
            mapping_note = f"Foldout spread of {yale_label}"

    # Strategy 3: Partial parts of foldouts (e.g., "89v part")
    if not folios_for_image:
        # These might be one of multiple parts
        # For now, map to the base folio
        simple = re.match(r'^(\d+)([rv])\s+\(part\)$', yale_label)
        if simple:
            folio_num = simple.group(1)
            side = simple.group(2)
            base = f"f{folio_num}{side}"

            # This is tricky - we need to know which part
            # For now, suggest all matching panels
            matching = [f for f in unmapped_folios if f.startswith(base) and len(f) > len(base)]
            if matching:
                folios_for_image = sorted(matching)
                mapping_note = f"Part of {base} - uncertain which panel(s), listing all candidates"

    if folios_for_image:
        additional_mappings.append({
            "page_order": page_order,
            "image_file": filename,
            "yale_label": yale_label,
            "folio_ids": folios_for_image,
            "type": "manual_foldout",
            "notes": mapping_note,
            "confidence": "HIGH" if len(folios_for_image) == 1 else "MEDIUM" if len(folios_for_image) <= 3 else "LOW"
        })

        # Mark these folios as mapped
        for f in folios_for_image:
            unmapped_folios.remove(f)
    else:
        unresolvable.append({
            "page_order": page_order,
            "image_file": filename,
            "yale_label": yale_label,
            "reason": "Could not parse Yale label pattern"
        })

print(f"✓ Manually mapped: {len(additional_mappings)} images")
print(f"⚠ Still unresolvable: {len(unresolvable)} images")
print(f"⚠ Remaining unmapped folios: {len(unmapped_folios)}\n")

# Combine all mappings
all_mappings = existing_mapping + additional_mappings

# Map folios to images
folio_to_images = {}
for m in all_mappings:
    for folio_id in m['folio_ids']:
        if folio_id not in folio_to_images:
            folio_to_images[folio_id] = []
        folio_to_images[folio_id].append(m['image_file'])

# Generate report
print("=" * 80)
print("MAPPING COVERAGE")
print("=" * 80)

mapped_folios = set(folio_to_images.keys())
all_folio_ids = set(all_folios.keys())
still_unmapped = all_folio_ids - mapped_folios

print(f"\nTotal folios in dataset:    {len(all_folio_ids)}")
print(f"Folios with images:         {len(mapped_folios)}")
print(f"Folios still unmapped:      {len(still_unmapped)}")

if still_unmapped:
    print(f"\nRemaining unmapped folios:")
    for f in sorted(still_unmapped)[:30]:
        print(f"  {f}")
    if len(still_unmapped) > 30:
        print(f"  ... and {len(still_unmapped) - 30} more")

# Show confidence distribution
confidence_counts = {}
for m in additional_mappings:
    conf = m['confidence']
    confidence_counts[conf] = confidence_counts.get(conf, 0) + 1

print(f"\nManual mapping confidence:")
for conf in ['HIGH', 'MEDIUM', 'LOW']:
    if conf in confidence_counts:
        print(f"  {conf:10s}: {confidence_counts[conf]:3d}")

# Save complete mapping
print("\n" + "=" * 80)
print("SAVING COMPLETE MAPPING")
print("=" * 80)

with open('image_folio_mapping_complete.json', 'w') as f:
    json.dump(all_mappings, f, indent=2)
print(f"✓ Saved complete mapping: image_folio_mapping_complete.json")

with open('folio_to_images.json', 'w') as f:
    json.dump(folio_to_images, f, indent=2)
print(f"✓ Saved folio→images lookup: folio_to_images.json")

if still_unmapped:
    with open('still_unmapped_folios.json', 'w') as f:
        json.dump(sorted(still_unmapped), f, indent=2)
    print(f"✓ Saved still-unmapped folios: still_unmapped_folios.json ({len(still_unmapped)} folios)")

if unresolvable:
    with open('unresolvable_images.json', 'w') as f:
        json.dump(unresolvable, f, indent=2)
    print(f"✓ Saved unresolvable images: unresolvable_images.json ({len(unresolvable)} images)")

print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print(f"Images with folio mappings:   {len(all_mappings)}")
print(f"Folios with image mappings:   {len(folio_to_images)}")
print(f"Coverage:                     {len(mapped_folios)}/{len(all_folio_ids)} ({100*len(mapped_folios)/len(all_folio_ids):.1f}%)")
print("=" * 80)
