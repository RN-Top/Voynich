#!/usr/bin/env python3
"""
Analyze EVA transcription file to extract actual folio structure
Build folio list from what's actually in the file, in order of appearance
"""

import re
from pathlib import Path
from collections import OrderedDict

print("=" * 80)
print("ANALYZING VOYNICH EVA TRANSCRIPTION STRUCTURE")
print("=" * 80)

EVA_FILE = "Data/Zl3b-n.txt"

if not Path(EVA_FILE).exists():
    print(f"ERROR: {EVA_FILE} not found")
    exit(1)

print(f"\nReading {EVA_FILE}...")

# Track folios in order of appearance
folio_order = []
folio_data = OrderedDict()  # Preserve insertion order
parse_errors = []

with open(EVA_FILE, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        line = line.rstrip()

        # Folio marker: <f1r>, <f116v>, <f67r1>, <f67r2>, etc.
        folio_match = re.match(r'<(f\d+[rv](?:\d)?)>', line)
        if folio_match:
            folio_id = folio_match.group(1)
            if folio_id not in folio_data:
                folio_order.append(folio_id)
                folio_data[folio_id] = {"line_count": 0, "lines": []}
            continue

        # Line content: <f1r.1,@P0> text | <f116v.1,@Lx> text | etc.
        line_match = re.match(r'<(f\d+[rv](?:\d)?)\.\d+,([^>]+)>\s+(.+)', line)
        if line_match:
            folio_id = line_match.group(1)
            locus = line_match.group(2)
            text = line_match.group(3)

            if folio_id not in folio_data:
                folio_order.append(folio_id)
                folio_data[folio_id] = {"line_count": 0, "lines": []}

            folio_data[folio_id]["line_count"] += 1
            folio_data[folio_id]["lines"].append({
                "locus": locus,
                "text": text
            })
            continue

        # Check for unparseable lines with folio markers
        if '<f' in line and '>' in line and not line.startswith('#'):
            # This looks like it might be a folio line we couldn't parse
            parse_attempt = re.search(r'<(f\d+[rv](?:\d)?[^>]*)>', line)
            if parse_attempt:
                parse_errors.append({
                    "line_num": line_num,
                    "attempted_folio": parse_attempt.group(1),
                    "content": line[:80]
                })

print(f"\n✓ Parse complete")
print(f"\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

print(f"\nTotal unique page/panel IDs found: {len(folio_order)}")
print(f"Folios with text lines: {sum(1 for f in folio_data.values() if f['line_count'] > 0)}")
print(f"Folios without text: {sum(1 for f in folio_data.values() if f['line_count'] == 0)}")

total_lines = sum(f['line_count'] for f in folio_data.values())
print(f"Total text lines: {total_lines}")

print(f"\n" + "-" * 80)
print("FOLIO LIST (in order of appearance)")
print("-" * 80)
for i, folio_id in enumerate(folio_order, 1):
    line_count = folio_data[folio_id]["line_count"]
    status = "✓ has text" if line_count > 0 else "✗ no text"
    print(f"{i:3d}. {folio_id:8s} {status:12s} ({line_count:3d} lines)")

if parse_errors:
    print(f"\n" + "-" * 80)
    print(f"PARSE ERRORS ({len(parse_errors)} lines couldn't be parsed)")
    print("-" * 80)
    for err in parse_errors[:10]:  # Show first 10
        print(f"Line {err['line_num']}: <{err['attempted_folio']}> {err['content']}...")
    if len(parse_errors) > 10:
        print(f"... and {len(parse_errors) - 10} more")
else:
    print(f"\n✓ All folio lines parsed successfully")

print(f"\n" + "=" * 80)
print("FOLIO ORDER FOR BUILD SCRIPTS")
print("=" * 80)
print(f"folio_order = {folio_order}")
print("=" * 80)
