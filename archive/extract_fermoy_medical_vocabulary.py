"""
Extract comprehensive medical vocabulary from the Book of Fermoy.

The Fermoy manuscript contains medical fragments in Irish and Latin.
This script extracts medical terms, anatomical vocabulary, treatments,
herbs, and conditions from the full text.
"""

import re
from pathlib import Path
from collections import Counter
import json

# Read the Fermoy manuscript
fermoy_path = Path("data/fermoy_ms23e29.txt")
with open(fermoy_path, 'r', encoding='utf-8', errors='ignore') as f:
    fermoy_text = f.read()

# Known Irish medical terms and patterns to search for
# Based on medical text conventions of the period

medical_indicators = {
    'herbs_plants': [
        'seneccha', 'capaill', 'fiadh', 'lus', 'planta',
        'root', 'herb', 'plant', 'seed', 'leaf',
    ],
    'conditions': [
        'galar', 'tinn', 'othar', 'galair', 'pain', 'ache',
        'fever', 'disease', 'illness', 'sick', 'wound',
        'bruise', 'inflammation', 'swelling', 'weakness',
    ],
    'treatments': [
        'leigheas', 'cure', 'remedy', 'potion', 'drink',
        'poultice', 'salve', 'ointment', 'bandage', 'bleed',
        'purge', 'tincture', 'infusion', 'decoction',
    ],
    'anatomy': [
        'hepate', 'liver', 'head', 'brain', 'heart', 'lung',
        'stomach', 'belly', 'bone', 'blood', 'flesh', 'eye',
        'ear', 'nose', 'throat', 'hand', 'foot', 'organ',
        'membrorurn', 'generacionibus', 'corpore',
    ],
    'practices': [
        'physician', 'doctor', 'healer', 'medicin', 'surgical',
        'treatise', 'formula', 'prescription', 'dosage',
    ]
}

# Extract all words from Fermoy
words = re.findall(r'\b[a-zàáäâèéëêìíïîòóöôùúüûñçœæ]+\b', fermoy_text.lower())

# Focus on medical sections (around the O'Hickey fragments)
medical_section_start = fermoy_text.find("O'Hickey")
medical_sections = []

# Extract text around medical mentions
for match in re.finditer(r'.{0,200}(medical|physician|O.?Hickey|hepate|treatise|cure|remedy).{0,200}',
                         fermoy_text, re.IGNORECASE):
    medical_sections.append(match.group(0))

# Extract words from medical sections
medical_words = []
for section in medical_sections:
    section_words = re.findall(r'\b[a-zàáäâèéëêìíïîòóöôùúüûñçœæ]{2,}\b', section.lower())
    medical_words.extend(section_words)

# Count word frequencies
word_freq = Counter(medical_words)

# Expand medical vocabulary
extracted_vocabulary = set()

# Add words that appear in medical contexts
for word, count in word_freq.most_common(500):
    if count >= 2:  # Words appearing multiple times in medical sections
        extracted_vocabulary.add(word)

# Add known medical terms
for category, terms in medical_indicators.items():
    extracted_vocabulary.update(terms)

# Look for Irish words with medical suffixes
for word in words:
    if any(word.endswith(suffix) for suffix in ['acht', 'tion', 'ness', 'ment', 'ence']):
        if word in medical_words and len(word) > 3:
            extracted_vocabulary.add(word)

# Extract compound terms and phrases
compound_patterns = [
    r'\b([a-z]+)\s+(cure|remedy|potion|treatment)',
    r'\b(liver|heart|head|body)\s+([a-z]+)',
    r'(de|of)\s+([a-z]+)',
]

for pattern in compound_patterns:
    for match in re.finditer(pattern, ' '.join(medical_sections), re.IGNORECASE):
        term = ' '.join(match.groups()).lower()
        if len(term) > 2:
            extracted_vocabulary.add(term)

# Clean and sort
medical_vocabulary = sorted(list(extracted_vocabulary))

# Save to file
output_path = Path("data/fermoy_medical_vocabulary_extracted.txt")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("# Comprehensive Medical Vocabulary Extracted from Book of Fermoy\n")
    f.write(f"# Total terms: {len(medical_vocabulary)}\n\n")
    for term in medical_vocabulary:
        f.write(f"{term}\n")

print(f"Extracted {len(medical_vocabulary)} medical vocabulary terms from Fermoy")
print(f"Saved to {output_path}")

# Also save as JSON for easy processing
with open("data/fermoy_medical_vocabulary.json", 'w', encoding='utf-8') as f:
    json.dump({
        'vocabulary': medical_vocabulary,
        'count': len(medical_vocabulary),
        'categories': {k: list(v)[:10] for k, v in medical_indicators.items()}
    }, f, indent=2, ensure_ascii=False)

print(f"Also saved as JSON to data/fermoy_medical_vocabulary.json")

# Display sample
print(f"\nSample extracted terms:")
for term in sorted(medical_vocabulary)[:50]:
    print(f"  {term}")
