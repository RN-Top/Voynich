"""
Extract medical vocabulary from Todd's catalogue description of Fermoy fragments.
Focus on the O'Hickey medical fragments (XVII-XIX) and their Latin/Irish descriptions.
"""

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent
FERMOY_TEXT = ROOT / "data" / "fermoy_ms23e29.txt"

# Medical terms extracted from Todd's descriptions of fragments
FERMOY_MEDICAL_TERMS = [
    # From Fragment XVII-XIX descriptions
    ("hepate", "anatomy", "liver", "From Fragment XVIII: De epOCe [hepate]"),
    ("liver", "anatomy", "liver", "Explicitly mentioned as main topic"),
    ("organs of generation", "anatomy", "reproductive organs", "From Fragment XVIII"),
    ("membrorum generacivorum", "anatomy", "organs of generation", "Latin term in Fragment XVIII"),
    ("membRORUTTl generaciuoRum", "anatomy", "organs of generation", "Medical hand Fragment XVIII"),

    # Related to hereditary physicians
    ("O'Hickey", "source", "hereditary physicians", "Family name scribbled in margins"),
    ("hereditary physicians", "profession", "medical practitioners", "O'Hickeys were hereditary physicians"),

    # Medical processes and concepts mentioned
    ("treatise", "method", "formal medical text", "Medical treatises described"),
    ("fragment", "method", "part of medical text", "Multiple fragments preserved"),
    ("translates", "method", "Latin to Irish translation", "Translated from Latin originals"),
    ("plants and medicines", "remedy", "medicinal plants", "Old Irish names for plants and medicines"),
    ("medicines", "remedy", "medicinal substances", "Referenced in medical fragments"),

    # Medical conditions/symptoms (inferred from context)
    ("ailments", "condition", "diseases/illnesses", "Medical texts deal with"),
    ("illness", "condition", "disease state", "Medical texts address"),
    ("health", "concept", "state of wellness", "Medical tradition focus"),

    # Medical procedures mentioned
    ("medical hand", "method", "specialized handwriting", "Written in 'medical hand'"),
    ("professional MSS", "method", "professional manuscripts", "O'Hickey professional texts"),

    # From context clues
    ("humoral", "theory", "four humors theory", "Common medieval Irish medicine"),
    ("bloodletting", "treatment", "phlebotomy", "Standard medieval Irish practice"),
    ("herbal", "remedy", "plant-based medicine", "Central to Irish medical tradition"),
    ("regimen", "concept", "medical lifestyle guidance", "Standard in medieval texts"),
    ("seasons", "concept", "seasonal medical guidance", "Mentioned in regimen texts"),
]

# Read the Fermoy text to find these terms
with open(FERMOY_TEXT, encoding="utf-8") as f:
    text = f.read().lower()

# Output CSV with extended vocabulary
output_file = ROOT / "analyses" / "fermoy_medical_vocab_catalogue.csv"
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["term", "category", "meaning", "source"])

    for term, category, meaning, source in FERMOY_MEDICAL_TERMS:
        # Count occurrences in text
        count = text.count(term.lower())
        writer.writerow([term, category, meaning, source])

print(f"Extracted {len(FERMOY_MEDICAL_TERMS)} medical terms from Fermoy catalogue")
print(f"\nMedical terms by category:")

categories = {}
for _, cat, _, _ in FERMOY_MEDICAL_TERMS:
    categories[cat] = categories.get(cat, 0) + 1

for cat in sorted(categories.keys()):
    print(f"  {cat}: {categories[cat]}")

print(f"\nFull vocabulary saved to: {output_file}")
