"""
EXPANDED FERMOY VOCABULARY COMPARISON TEST
Combining 42 original terms + 22 catalogue-extracted terms = 64 terms
Testing against Voynich closing words for Levenshtein and substring matches.

Pre-registration summary:
- Prediction: ≥8 Levenshtein matches (distance ≤3) AND ≥5 substring matches
- Original result: 26 Levenshtein + 27 substring (SUPPORTED)
- Expanded result: Testing with 64 medical terms
"""

import csv
from pathlib import Path
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parent.parent
ANALYSES = ROOT / "analyses"
OUTPUT = ROOT / "output"

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

# Load Voynich closing words from table
closing_words = []
with open(OUTPUT / "recipe_closing_report.md") as f:
    lines = f.readlines()
    in_table = False
    for line in lines:
        if line.startswith("|") and not in_table:
            in_table = True
            continue
        if in_table and line.startswith("|"):
            parts = line.split("|")
            if len(parts) > 1:
                word = parts[1].strip()
                if word and word not in ["Word", "---"] and word.replace("-", "").isalpha():
                    closing_words.append(word)

closing_words = list(set(closing_words))[:44]  # Get up to 44 unique words

# Load expanded medical vocabulary (combined)
medical_terms = []

# Original 42 terms
with open(ANALYSES / "fermoy_medical_vocab.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("term"):
            medical_terms.append(row["term"].lower())

# New catalogue-based 22 terms
with open(ANALYSES / "fermoy_medical_vocab_catalogue.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("term"):
            term = row["term"].lower()
            if term not in medical_terms:
                medical_terms.append(term)

medical_terms = list(set(medical_terms))

# Test: Levenshtein distance ≤ 3
levenshtein_matches = []
for voy_word in closing_words:
    for med_term in medical_terms:
        distance = levenshtein_distance(voy_word.lower(), med_term.lower())
        if distance <= 3:
            levenshtein_matches.append({
                "voynich": voy_word,
                "fermoy": med_term,
                "distance": distance
            })

# Test: Substring overlap
substring_matches = []
for voy_word in closing_words:
    voy_lower = voy_word.lower()
    for med_term in medical_terms:
        med_lower = med_term.lower()
        if len(voy_lower) >= 3 and len(med_lower) >= 3:
            if voy_lower in med_lower or med_lower in voy_lower:
                substring_matches.append({
                    "voynich": voy_word,
                    "fermoy": med_term,
                    "type": "substring"
                })

# Binomial test (null: expected by chance)
# 25 Voynich words × 64 medical terms = 1600 comparisons
# Random expected Levenshtein match rate: ~5-7%
# Random expected substring match rate: ~2-3%
n_comparisons = len(closing_words) * len(medical_terms)
expected_levenshtein_rate = 0.06
expected_substring_rate = 0.025

levenshtein_expected = int(n_comparisons * expected_levenshtein_rate)
substring_expected = int(n_comparisons * expected_substring_rate)

# Binomial test
lev_result = binomtest(len(levenshtein_matches), n_comparisons, expected_levenshtein_rate)
sub_result = binomtest(len(substring_matches), n_comparisons, expected_substring_rate)

# Output report
report_file = OUTPUT / "fermoy_vocab_comparison_report_expanded.md"
with open(report_file, "w") as f:
    f.write("# Fermoy Vocabulary Comparison Test (EXPANDED)\n\n")
    f.write(f"**Test Date**: October 2026\n")
    f.write(f"**Vocabulary Size**: {len(medical_terms)} medical terms (42 original + 22 catalogue)\n")
    f.write(f"**Closing Words**: {len(closing_words)} Voynich closing vocabulary words\n")
    f.write(f"**Comparisons**: {n_comparisons} total pairs\n\n")

    f.write("## Results\n\n")
    f.write(f"**Levenshtein Matches (distance ≤3)**: {len(levenshtein_matches)}\n")
    f.write(f"  - Expected by chance: ~{levenshtein_expected}\n")
    f.write(f"  - Actual: {len(levenshtein_matches)}\n")
    f.write(f"  - Binomial p-value: {lev_result.pvalue:.6f}\n\n")

    f.write(f"**Substring Matches**: {len(substring_matches)}\n")
    f.write(f"  - Expected by chance: ~{substring_expected}\n")
    f.write(f"  - Actual: {len(substring_matches)}\n")
    f.write(f"  - Binomial p-value: {sub_result.pvalue:.6f}\n\n")

    f.write("## Hypothesis Test\n\n")
    f.write("**Pre-registration**: ≥8 Levenshtein matches AND ≥5 substring matches\n\n")

    if len(levenshtein_matches) >= 8 and len(substring_matches) >= 5:
        f.write("**Result**: ✓ SUPPORTED\n\n")
        f.write(f"The expanded vocabulary test confirms the original finding:\n")
        f.write(f"- {len(levenshtein_matches)} Levenshtein matches (exceeds ≥8 prediction)\n")
        f.write(f"- {len(substring_matches)} substring matches (exceeds ≥5 prediction)\n")
    else:
        f.write("**Result**: ✗ NOT SUPPORTED\n\n")

    f.write(f"\n## Levenshtein Matches (Top 20)\n\n")
    for match in sorted(levenshtein_matches, key=lambda x: x["distance"])[:20]:
        f.write(f"- {match['voynich']} ↔ {match['fermoy']} (distance: {match['distance']})\n")

    f.write(f"\n## Substring Matches (Top 20)\n\n")
    for match in substring_matches[:20]:
        f.write(f"- {match['voynich']} ↔ {match['fermoy']}\n")

print(f"Expanded vocabulary test complete")
print(f"Report saved to: {report_file}")
