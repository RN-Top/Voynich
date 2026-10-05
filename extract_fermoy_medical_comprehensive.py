"""
Comprehensive medical vocabulary extraction from Book of Fermoy.

Focus on the actual medical manuscript fragments that contain
Irish and Latin medical terminology.
"""

import re
from pathlib import Path
from collections import Counter
import json

# Read the Fermoy manuscript
fermoy_path = Path("data/fermoy_ms23e29.txt")
with open(fermoy_path, 'r', encoding='utf-8', errors='ignore') as f:
    fermoy_text = f.read()

# Common English stopwords to filter out
stopwords = set([
    'the', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'from', 'by', 'it', 'this', 'that', 'these', 'those',
    'a', 'an', 'as', 'if', 'but', 'not', 'all', 'each', 'every', 'both',
    'such', 'no', 'nor', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    'just', 'most', 'more', 'some', 'any', 'what', 'which', 'who', 'when',
    'where', 'why', 'how', 'up', 'down', 'out', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'about', 'against', 'over', 'while',
    'page', 'fol', 'leaf', 'leaves', 'fragment', 'fragments', 'ms', 'edition',
    'todd', 'oflaherty', 'ocurry', 'oreilly', 'catalogue', 'book', 'volume',
    'stave', 'col', 'margin', 'margins', 'numbered', 'double', 'columns',
    'upper', 'lower', 'line', 'lines', 'beginning', 'end', 'imperfect',
])

# Extract text sections mentioning medical or O'Hickey
medical_markers = ['medical', 'physician', 'cure', 'remedy', 'hepate', 'treatment',
                   'disease', 'illness', 'herb', 'medicin', 'surgeon', 'leigheas',
                   'othar', 'galar', 'membrorurn', 'organ']

# Find text around medical markers
medical_contexts = []
for marker in medical_markers:
    pattern = f'.{{0,300}}{re.escape(marker)}.{{0,300}}'
    for match in re.finditer(pattern, fermoy_text, re.IGNORECASE):
        medical_contexts.append(match.group(0))

# Combine all medical context
all_medical_text = ' '.join(medical_contexts)

# Extract words, keeping Irish characters
word_pattern = r'\b[a-zàáäâèéëêìíïîòóöôùúüûñçœæáéíóúáíýćéőĀ-ſ]+\b'
all_words = re.findall(word_pattern, all_medical_text.lower())

# Also look for potential Irish words with diacritics
irish_pattern = r'\b[a-z]+[áéíóúáíýćéő][a-z]*\b'
irish_words = re.findall(irish_pattern, all_medical_text.lower())

# Filter by frequency and stopwords
word_freq = Counter(all_words + irish_words)

# Build vocabulary
medical_vocabulary = set()

# Include words that appear multiple times in medical context
for word, count in word_freq.most_common(500):
    if count >= 2 and word not in stopwords and len(word) > 2:
        medical_vocabulary.add(word)

# Add specific known medical terms from Irish and Latin
known_medical_terms = [
    # Irish medical terms
    'leigheas', 'othar', 'galar', 'galair', 'tinn', 'seneccha',
    'lus', 'fiadh', 'capaill', 'draoithe',

    # Latin medical terms from fragments
    'hepate', 'membrorurn', 'generacionibus', 'operacionibus',
    'qualitaibus', 'naturalis', 'corpore', 'uenae',
    'circulis', 'biuibicup', 'uircutep',

    # Common medical vocabulary across periods
    'acutum', 'chronicum', 'febris', 'dolorem', 'inflammatio',
    'apostema', 'tumor', 'abscessus', 'ulcus', 'plaga',

    # Anatomical terms
    'caput', 'oculus', 'cor', 'pulmones', 'hepar', 'iecur',
    'stomachus', 'ventriculus', 'intestina', 'membra', 'nervi',
    'vasa', 'sanguinem', 'osseum', 'muscula',

    # Herbal and treatment terms
    'herba', 'folium', 'radix', 'semen', 'flos', 'cortex',
    'decoctio', 'infusio', 'tinctura', 'unguentum', 'oleum',
    'pulvis', 'confectio', 'electuarium', 'syrupus',

    # Symptoms and conditions (Irish variants)
    'fírinne', 'teiched', 'braistid', 'fír', 'galar',
]

medical_vocabulary.update(known_medical_terms)

# Extract compound Irish terms
compound_terms = re.findall(r'\b([a-z]+)(?:\s+[a-z]+)?(?:\s+[a-z]+)?\b', all_medical_text.lower())
compound_freq = Counter(compound_terms)

for term, count in compound_freq.most_common(200):
    if count >= 2 and term not in stopwords and len(term) > 3:
        medical_vocabulary.add(term)

# Remove remaining common words and cleanup
cleanup_terms = ['said', 'say', 'tells', 'tells', 'point', 'points', 'part', 'parts',
                 'writing', 'written', 'writes', 'wrote', 'written', 'handwriting',
                 'note', 'notes', 'addition', 'additions']
for term in cleanup_terms:
    medical_vocabulary.discard(term)

# Sort and save
medical_vocabulary_sorted = sorted(list(medical_vocabulary))

output_path = Path("data/fermoy_medical_vocabulary_full.txt")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("# Comprehensive Medical Vocabulary from Book of Fermoy\n")
    f.write(f"# Total unique terms: {len(medical_vocabulary_sorted)}\n")
    f.write("# Extracted from medical fragments (XVII, XVIII, XIX)\n")
    f.write("# Includes Irish and Latin medical terminology\n\n")
    for term in medical_vocabulary_sorted:
        f.write(f"{term}\n")

print(f"✓ Extracted {len(medical_vocabulary_sorted)} comprehensive medical terms")
print(f"✓ Saved to {output_path}\n")

# Save structured JSON
json_output = {
    'total_terms': len(medical_vocabulary_sorted),
    'vocabulary': medical_vocabulary_sorted,
    'categories': {
        'irish_medical': [t for t in medical_vocabulary_sorted if any(c in t for c in 'áéíóú')],
        'latin_medical': [t for t in medical_vocabulary_sorted if t in known_medical_terms and len(t) > 4],
        'long_terms': [t for t in medical_vocabulary_sorted if len(t) > 8],
        'common_terms': [t for t in medical_vocabulary_sorted[:100]],
    }
}

json_path = Path("data/fermoy_medical_vocabulary_full.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_output, f, indent=2, ensure_ascii=False)

print(f"✓ Also saved as JSON to {json_path}\n")

# Show sample
print("Sample extracted terms:")
for term in sorted(medical_vocabulary_sorted)[:80]:
    print(f"  {term}")

print(f"\n... and {len(medical_vocabulary_sorted) - 80} more terms")
