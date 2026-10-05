"""
Extract full medical vocabulary from Fermoy manuscript (MS 23 E 29).
Expands from 42 terms (catalogue only) to full text extraction.
"""

import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
FERMOY_TEXT = ROOT / "data" / "fermoy_ms23e29.txt"
OUT = ROOT / "analyses"

# Read Fermoy manuscript
with open(FERMOY_TEXT, encoding="utf-8") as f:
    text = f.read()

# Medical vocabulary patterns (Latin and English)
MEDICAL_TERMS = {
    # Anatomy
    "hepate": "anatomy",
    "liver": "anatomy",
    "spleen": "anatomy",
    "heart": "anatomy",
    "brain": "anatomy",
    "stomach": "anatomy",
    "bladder": "anatomy",
    "kidney": "anatomy",
    "intestin": "anatomy",
    "bone": "anatomy",
    "blood": "anatomy",
    "vein": "anatomy",
    "artery": "anatomy",

    # Conditions/diseases
    "dropsy": "condition",
    "colic": "condition",
    "pox": "condition",
    "leprosy": "condition",
    "ague": "condition",
    "fever": "condition",
    "plague": "condition",
    "flux": "condition",
    "piles": "condition",
    "worm": "condition",
    "gout": "condition",
    "stone": "condition",
    "palsy": "condition",
    "apoplexy": "condition",
    "jaundice": "condition",
    "consumption": "condition",
    "phlegm": "condition",
    "melancholy": "condition",
    "mania": "condition",
    "frenzy": "condition",
    "madness": "condition",

    # Treatments/procedures
    "bloodlet": "treatment",
    "phlebotom": "treatment",
    "purge": "treatment",
    "purgat": "treatment",
    "cleanse": "treatment",
    "bathe": "treatment",
    "bath": "treatment",
    "bleeding": "treatment",
    "lancet": "treatment",
    "plaster": "treatment",
    "poultice": "treatment",
    "compress": "treatment",
    "bandage": "treatment",
    "anoint": "treatment",
    "rub": "treatment",

    # Remedies/substances
    "herb": "remedy",
    "plant": "remedy",
    "root": "remedy",
    "bark": "remedy",
    "leaf": "remedy",
    "flower": "remedy",
    "seed": "remedy",
    "oil": "remedy",
    "unguent": "remedy",
    "balm": "remedy",
    "salve": "remedy",
    "potion": "remedy",
    "draught": "remedy",
    "decoction": "remedy",
    "infusion": "remedy",
    "tincture": "remedy",
    "elixir": "remedy",
    "cordial": "remedy",
    "syrup": "remedy",
    "wine": "remedy",
    "water": "remedy",

    # Humoral theory
    "humor": "theory",
    "choleric": "theory",
    "phlegmatic": "theory",
    "sanguine": "theory",
    "melancholic": "theory",
    "hot": "theory",
    "cold": "theory",
    "moist": "theory",
    "dry": "theory",
    "temperament": "theory",
    "complexion": "theory",

    # Medical concepts
    "regimen": "concept",
    "diet": "concept",
    "season": "concept",
    "air": "concept",
    "sleep": "concept",
    "exercise": "concept",
    "emotion": "concept",
    "symptom": "concept",
    "cause": "concept",
    "cure": "concept",
    "remedy": "concept",
    "medicine": "concept",
    "physician": "concept",
    "doctor": "concept",
    "leech": "concept",
    "apothecary": "concept",
}

# Extract words from text
# Case-insensitive, word boundaries
found_terms = {}
for term, category in MEDICAL_TERMS.items():
    # Find all occurrences (whole word matches)
    pattern = r"\b" + re.escape(term) + r"\w*"
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        found_terms[term] = {
            "category": category,
            "count": len(matches),
            "variants": list(set(matches))
        }

# Sort by frequency
sorted_terms = sorted(found_terms.items(), key=lambda x: x[1]["count"], reverse=True)

# Output CSV
output_file = OUT / "fermoy_medical_vocab_full.csv"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("term,category,count,variants,meaning\n")
    for term, data in sorted_terms:
        variants = "|".join(data["variants"][:5])  # Top 5 variants
        meaning = f"Medical term found {data['count']} times"
        f.write(f'"{term}","{data["category"]}",{data["count"]},"{variants}","{meaning}"\n')

print(f"Extracted {len(found_terms)} unique medical terms from Fermoy manuscript")
print(f"Total term occurrences: {sum(d['count'] for d in found_terms.values())}")
print(f"\nTop 20 terms by frequency:")
for term, data in sorted_terms[:20]:
    print(f"  {term}: {data['count']} occurrences ({data['category']})")
print(f"\nFull vocabulary saved to: {output_file}")
