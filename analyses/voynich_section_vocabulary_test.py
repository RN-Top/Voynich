"""
VOYNICH SECTION-BY-SECTION VOCABULARY TEST

Test Ó hÍceadha medical vocabulary across all major Voynich sections:
- Text pages (f1r-f6v)
- Plant pages (f7r-f49v)
- Astronomical pages (f50r-f66v)
- Astrological wheels (f67r-f73v)
- Bathing/biological (f75r-f84v)
- Recipes/pharmaceutical (f85r-f116v)
"""

import re
from pathlib import Path
from scipy.stats import binomtest
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "ZL3b-n.txt"
OUT = ROOT / "output"
ANALYSES = ROOT / "analyses"

def levenshtein_distance(s1, s2):
    """Calculate edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

# Load Ó hÍceadha medical vocabulary (combined from both sources)
medical_vocab = set()
for csv_file in [ANALYSES / "fermoy_medical_vocab.csv", ANALYSES / "fermoy_medical_vocab_catalogue.csv"]:
    if csv_file.exists():
        with open(csv_file) as f:
            for line in f:
                parts = line.strip().split(',')
                if parts and parts[0] not in ["term", ""]:
                    medical_vocab.add(parts[0].lower().strip('"'))

# Define Voynich sections
sections = {
    "Text pages": (1, 6),           # f1r-f6v
    "Plant pages": (7, 49),         # f7r-f49v
    "Astronomical": (50, 66),       # f50r-f66v
    "Astrological": (67, 73),       # f67r-f73v
    "Bathing": (75, 84),           # f75r-f84v
    "Recipes": (85, 116),          # f85r-f116v
}

# Extract words by folio
folio_words = defaultdict(list)
current_folio = None
with open(DATA) as f:
    for line in f:
        # Match folio markers like <f1r>, <f12v>, etc
        folio_match = re.search(r'<f(\d+)([rv])>', line)
        if folio_match:
            folio_num = int(folio_match.group(1))
            current_folio = folio_num

        # Extract words (anything between dots or commas that looks like text)
        words = re.findall(r'[a-z]+', line.lower())
        if words and current_folio:
            folio_words[current_folio].extend(words)

# Analyze each section
results = {}
for section_name, (start_folio, end_folio) in sections.items():
    section_words = []
    for folio in range(start_folio, end_folio + 1):
        section_words.extend(folio_words[folio])

    section_words = list(set(section_words))  # Unique words

    # Count matches
    levenshtein_matches = 0
    substring_matches = 0

    for voynich_word in section_words:
        for med_term in medical_vocab:
            distance = levenshtein_distance(voynich_word, med_term)
            if distance <= 3:
                levenshtein_matches += 1

            if len(voynich_word) >= 3 and len(med_term) >= 3:
                if voynich_word in med_term or med_term in voynich_word:
                    substring_matches += 1

    results[section_name] = {
        "unique_words": len(section_words),
        "levenshtein": levenshtein_matches,
        "substring": substring_matches
    }

# Output report
report_file = OUT / "voynich_section_vocabulary_report.md"
with open(report_file, "w") as f:
    f.write("# Voynich Section-by-Section Vocabulary Test\n\n")
    f.write("Testing Ó hÍceadha (EEK-kah-duh) medical vocabulary across all major Voynich sections.\n\n")
    f.write(f"**Medical vocabulary size**: {len(medical_vocab)} unique terms\n\n")

    f.write("## Results by Section\n\n")
    f.write("| Section | Unique Words | Levenshtein Matches | Substring Matches |\n")
    f.write("|---|---:|---:|---:|\n")

    for section, data in results.items():
        f.write(f"| {section} | {data['unique_words']} | {data['levenshtein']} | {data['substring']} |\n")

    f.write("\n## Analysis\n\n")
    f.write("Sections with higher match counts show stronger vocabulary connection to Ó hÍceadha medical tradition.\n\n")

    # Find strongest sections
    strongest_lev = max(results.items(), key=lambda x: x[1]['levenshtein'])
    strongest_sub = max(results.items(), key=lambda x: x[1]['substring'])

    f.write(f"**Strongest Levenshtein matches**: {strongest_lev[0]} ({strongest_lev[1]['levenshtein']} matches)\n\n")
    f.write(f"**Strongest substring matches**: {strongest_sub[0]} ({strongest_sub[1]['substring']} matches)\n\n")

print(f"Section-by-section analysis complete")
print(f"Report saved to: {report_file}")
print(f"\nResults:")
for section, data in results.items():
    print(f"  {section}: {data['levenshtein']} Levenshtein + {data['substring']} substring matches")
