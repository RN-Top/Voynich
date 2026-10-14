#!/usr/bin/env python3
"""
Build voynich_integrated.json: unified file with folios in order.
Combines folio ID, image paths, transcribed text (with locus labels),
and classification flags (text-only, image-only, foldout).
"""

import json
import re
from pathlib import Path
from collections import defaultdict

print("=" * 80)
print("BUILDING VOYNICH_INTEGRATED.JSON")
print("=" * 80)

# Expected input: Voynich transcription in format like Takeshi Takahashi
# Format: folio_id transcribed_text_with_locus_labels
# Example: f1r m:<EVA characters> | f1v m:<EVA characters>

TRANSCRIPTION_FILE = "voynich_transcription.txt"
IMAGE_DIR = "voynich_manuscript/pages"

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

# Folio order extracted from actual EVA file (in appearance order, including foldout panels)
# This list includes ONLY the folios that actually exist in the transcription
FOLIO_ORDER = ['f1r', 'f1v', 'f2r', 'f2v', 'f3r', 'f3v', 'f4r', 'f4v', 'f5r', 'f5v', 'f6r', 'f6v', 'f7r', 'f7v', 'f8r', 'f8v', 'f9r', 'f9v', 'f10r', 'f10v', 'f11r', 'f11v', 'f13r', 'f13v', 'f14r', 'f14v', 'f15r', 'f15v', 'f16r', 'f16v', 'f17r', 'f17v', 'f18r', 'f18v', 'f19r', 'f19v', 'f20r', 'f20v', 'f21r', 'f21v', 'f22r', 'f22v', 'f23r', 'f23v', 'f24r', 'f24v', 'f25r', 'f25v', 'f26r', 'f26v', 'f27r', 'f27v', 'f28r', 'f28v', 'f29r', 'f29v', 'f30r', 'f30v', 'f31r', 'f31v', 'f32r', 'f32v', 'f33r', 'f33v', 'f34r', 'f34v', 'f35r', 'f35v', 'f36r', 'f36v', 'f37r', 'f37v', 'f38r', 'f38v', 'f39r', 'f39v', 'f40r', 'f40v', 'f41r', 'f41v', 'f42r', 'f42v', 'f43r', 'f43v', 'f44r', 'f44v', 'f45r', 'f45v', 'f46r', 'f46v', 'f47r', 'f47v', 'f48r', 'f48v', 'f49r', 'f49v', 'f50r', 'f50v', 'f51r', 'f51v', 'f52r', 'f52v', 'f53r', 'f53v', 'f54r', 'f54v', 'f55r', 'f55v', 'f56r', 'f56v', 'f57r', 'f57v', 'f58r', 'f58v', 'f65r', 'f65v', 'f66r', 'f66v', 'f67r1', 'f67r2', 'f67v2', 'f67v1', 'f68r1', 'f68r2', 'f68r3', 'f68v3', 'f68v2', 'f68v1', 'f69r', 'f69v', 'f70r1', 'f70r2', 'f70v2', 'f70v1', 'f71r', 'f71v', 'f72r1', 'f72r2', 'f72r3', 'f72v3', 'f72v2', 'f72v1', 'f73r', 'f73v', 'f75r', 'f75v', 'f76r', 'f76v', 'f77r', 'f77v', 'f78r', 'f78v', 'f79r', 'f79v', 'f80r', 'f80v', 'f81r', 'f81v', 'f82r', 'f82v', 'f83r', 'f83v', 'f84r', 'f84v', 'f85r1', 'f85r2', 'f86v4', 'f86v6', 'f86v5', 'f86v3', 'f87r', 'f87v', 'f88r', 'f88v', 'f89r1', 'f89r2', 'f89v2', 'f89v1', 'f90r1', 'f90r2', 'f90v2', 'f90v1', 'f93r', 'f93v', 'f94r', 'f94v', 'f95r1', 'f95r2', 'f95v2', 'f95v1', 'f96r', 'f96v', 'f99r', 'f99v', 'f100r', 'f100v', 'f101r', 'f101v', 'f102r1', 'f102r2', 'f102v2', 'f102v1', 'f103r', 'f103v', 'f104r', 'f104v', 'f105r', 'f105v', 'f106r', 'f106v', 'f107r', 'f107v', 'f108r', 'f108v', 'f111r', 'f111v', 'f112r', 'f112v', 'f113r', 'f113v', 'f114r', 'f114v', 'f115r', 'f115v', 'f116r', 'f116v']

# Foldout pages (known multi-page spreads)
FOLDOUTS = {
    'f67r1', 'f67r2', 'f67r3',  # Famous 6-page foldout
    'f75r', 'f76r'              # Other known foldouts
}

print("\nPhase 1: Load transcription data...")
transcription_text = {}

if Path(TRANSCRIPTION_FILE).exists():
    with open(TRANSCRIPTION_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse transcription (format: folio_id: text with locus labels)
    # Example line: f1r: m: <text> | l: <text> | r: <text>
    lines = content.strip().split('\n')
    for line in lines:
        if ':' in line:
            folio_id, text = line.split(':', 1)
            folio_id = folio_id.strip()
            transcription_text[folio_id] = text.strip()

    print(f"✓ Loaded transcriptions for {len(transcription_text)} folios")
else:
    print(f"⚠ No {TRANSCRIPTION_FILE} found")
    print("  To generate integrated file, provide Voynich transcription.")
    print("  Format: folio_id: line1_locus: text | line2_locus: text")

print("\nPhase 2: Match folios with images and text...")

stats = defaultdict(int)
matched_folios = 0

for folio_id in FOLIO_ORDER:
    # Find image file (multiple image formats possible)
    image_paths = []
    for pattern in [f"{folio_id}.png", f"{folio_id}.jpg", f"*{folio_id}*"]:
        matches = list(Path(IMAGE_DIR).glob(pattern)) if Path(IMAGE_DIR).exists() else []
        image_paths.extend([str(m) for m in matches])

    # Remove duplicates and sort
    image_paths = sorted(list(set(image_paths)))

    # Classify folio
    has_text = folio_id in transcription_text
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

    if has_text or has_image:
        matched_folios += 1

    # Parse text into lines with locus labels
    text_lines = []
    if has_text:
        raw_text = transcription_text[folio_id]
        # Parse format: "m: <text> | l: <text> | r: <text>"
        # Where m=main, l=left, r=right
        parts = raw_text.split('|')
        for part in parts:
            part = part.strip()
            if ':' in part:
                locus, text = part.split(':', 1)
                text_lines.append({
                    "locus": locus.strip(),
                    "text": text.strip()
                })
            else:
                text_lines.append({
                    "locus": "unknown",
                    "text": part
                })

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

print(f"✓ Processed {len(FOLIO_ORDER)} folios")
print(f"  - Integrated (text + image): {stats['integrated']}")
print(f"  - Text-only: {stats['text_only']}")
print(f"  - Image-only: {stats['image_only']}")
print(f"  - Foldout: {stats['foldout']}")
print(f"  - Unmatched: {stats['unmatched']}")
print(f"  - Total matched: {matched_folios}")

# Update metadata
integrated_data['metadata']['folios_total'] = len(integrated_data['folios'])
integrated_data['metadata']['integrated_count'] = stats['integrated']
integrated_data['metadata']['text_only_count'] = stats['text_only']
integrated_data['metadata']['image_only_count'] = stats['image_only']
integrated_data['metadata']['foldout_count'] = stats['foldout']
integrated_data['metadata']['unmatched_count'] = stats['unmatched']

print("\nPhase 3: Save integrated file...")
with open('voynich_integrated.json', 'w', encoding='utf-8') as f:
    json.dump(integrated_data, f, indent=2, ensure_ascii=False)

print("✓ Saved: voynich_integrated.json")

print("\n" + "=" * 80)
print("OUTPUT SUMMARY")
print("=" * 80)
print(f"Folios processed:        {integrated_data['metadata']['folios_total']}")
print(f"Integrated (text+image): {integrated_data['metadata']['integrated_count']}")
print(f"Text-only:               {integrated_data['metadata']['text_only_count']}")
print(f"Image-only:              {integrated_data['metadata']['image_only_count']}")
print(f"Foldouts:                {integrated_data['metadata']['foldout_count']}")
print(f"Unmatched:               {integrated_data['metadata']['unmatched_count']}")
print("=" * 80)
