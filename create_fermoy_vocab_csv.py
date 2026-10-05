"""
Convert extracted medical vocabulary to CSV format for testing.
Categorize terms and provide meanings.
"""

import json
import csv
from pathlib import Path

# Load the extracted vocabulary
with open("data/fermoy_medical_vocabulary_full.json", 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Categorize terms
categories_map = {
    # Anatomical terms
    'caput': 'anatomy', 'oculus': 'anatomy', 'cor': 'anatomy', 'pulmones': 'anatomy',
    'hepar': 'anatomy', 'iecur': 'anatomy', 'stomachus': 'anatomy', 'ventriculus': 'anatomy',
    'intestina': 'anatomy', 'membra': 'anatomy', 'nervi': 'anatomy', 'vasa': 'anatomy',
    'sanguinem': 'anatomy', 'osseum': 'anatomy', 'muscula': 'anatomy', 'hepate': 'anatomy',
    'membrorurn': 'anatomy', 'corpore': 'anatomy', 'uenae': 'anatomy',

    # Conditions/diseases
    'disease': 'condition', 'fever': 'condition', 'febris': 'condition', 'galar': 'condition',
    'galair': 'condition', 'tinn': 'condition', 'othar': 'condition', 'fatal': 'condition',
    'inflammation': 'condition', 'inflammatio': 'condition', 'tumor': 'condition',
    'abscessus': 'condition', 'apostema': 'condition', 'ulcus': 'condition',
    'acutum': 'condition', 'chronicum': 'condition', 'plaga': 'condition',

    # Treatment/cure
    'cure': 'cure', 'remedy': 'cure', 'leigheas': 'cure', 'treatment': 'cure',
    'decoctio': 'cure', 'infusio': 'cure', 'tinctura': 'cure', 'unguentum': 'cure',
    'oleum': 'cure', 'pulvis': 'cure', 'confectio': 'cure', 'electuarium': 'cure',
    'syrupus': 'cure',

    # Herbs and plants
    'herb': 'herb', 'herba': 'herb', 'lus': 'herb', 'seneccha': 'herb',
    'fiadh': 'herb', 'capaill': 'herb', 'folium': 'herb', 'radix': 'herb',
    'semen': 'herb', 'flos': 'herb', 'cortex': 'herb',

    # Medical practice
    'physician': 'practice', 'physicians': 'practice', 'medical': 'practice',
    'hereditary': 'practice', 'draoithe': 'practice',

    # Qualities/operations
    'qualitaibus': 'quality', 'operacionibus': 'quality', 'naturalis': 'quality',
    'dolorem': 'quality', 'circulis': 'quality', 'generacionibus': 'quality',

    # Other medical terms
    'fír': 'symptom', 'fírinne': 'symptom', 'teiched': 'symptom', 'braistid': 'symptom',
    'ill': 'condition', 'bothar': 'condition', 'bruighean': 'condition',
    'biuibicup': 'anatomy', 'uircutep': 'anatomy',
}

# Create CSV rows
rows = []
for term in vocab_data['vocabulary']:
    category = categories_map.get(term, 'medical')
    row = {
        'term': term,
        'category': category,
        'latin_root': '',
        'meaning': ''
    }
    rows.append(row)

# Write CSV
output_path = Path("analyses/fermoy_medical_vocab.csv")
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['term', 'category', 'latin_root', 'meaning'])
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Created {len(rows)} medical vocabulary entries")
print(f"✓ Saved to {output_path}")

# Show distribution
from collections import Counter
cats = [r['category'] for r in rows]
cat_counts = Counter(cats)
print(f"\nVocabulary by category:")
for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")
