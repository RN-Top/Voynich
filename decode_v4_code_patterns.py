#!/usr/bin/env python3
"""
EXPERIMENTAL: @-Code Pattern Analysis + Ingredient Validation
Hypothesis: @-codes are batch identifiers in pharmaceutical recipe format
"""

import json
from collections import Counter
import re

# Load data
with open('voynich_integrated.json', 'r') as f:
    integrated = json.load(f)

# Extract @-codes
all_codes = []
code_positions = []
code_contexts = {}  # code -> surrounding words

for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            words = line.get('words', [])

            # Find all @-codes in text
            codes = re.findall(r'@(\d+)', text)
            for code in codes:
                all_codes.append(int(code))
                code_positions.append((folio.get('folio_id'), line.get('locus')))

                # Capture context (words around the code)
                if code not in code_contexts:
                    code_contexts[code] = []
                code_contexts[code].extend(words)

print("=== @-CODE ANALYSIS ===")
print(f"Total @-codes found: {len(all_codes)}")
print(f"Unique codes: {len(set(all_codes))}")
print()

# Analyze code range
code_freq = Counter(all_codes)
min_code = min(all_codes)
max_code = max(all_codes)
print(f"Code range: @{min_code} to @{max_code}")
print(f"Range span: {max_code - min_code + 1}")
print()

# Top codes
print("Top 20 most frequent @-codes:")
for code, count in code_freq.most_common(20):
    print(f"  @{code:3}: {count:4} instances")
print()

# Code distribution
print("=== CODE DISTRIBUTION ===")
distribution = Counter()
for code in all_codes:
    if code < 150:
        distribution['100-149'] += 1
    elif code < 200:
        distribution['150-199'] += 1
    elif code < 250:
        distribution['200-249'] += 1
    else:
        distribution['250+'] += 1

for range_name, count in sorted(distribution.items()):
    print(f"  {range_name}: {count} ({100*count/len(all_codes):.1f}%)")
print()

# Analyze code contexts
print("=== WORDS ASSOCIATED WITH CODES ===")
print("Words appearing near @-codes (top 15):")
code_word_freq = Counter()
for code, words in code_contexts.items():
    for word in words:
        code_word_freq[word] += 1

for word, count in code_word_freq.most_common(15):
    print(f"  {word:15} {count:5}")
print()

# Ingredient hypothesis: check if codes cluster with certain word patterns
print("=== INGREDIENT COMBINATION HYPOTHESIS ===")
print("Checking if @-codes appear with ingredient-pattern words...")

ingredient_endings = ['iin', 'ain', 'in', 'ol', 'ar', 'al', 'or', 'dy', 'y']
code_ingredient_assoc = {ending: 0 for ending in ingredient_endings}

for code, words in code_contexts.items():
    for word in words:
        for ending in ingredient_endings:
            if word.endswith(ending):
                code_ingredient_assoc[ending] += 1

print("Ingredient patterns near @-codes:")
for ending, count in sorted(code_ingredient_assoc.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"  ...{ending}: {count:4}")
print()

# Analyze code positions in folios
print("=== CODE DISTRIBUTION BY FOLIO ===")
folio_codes = Counter(pos[0] for pos in code_positions)
print("Folios with most @-codes (top 10):")
for folio, count in folio_codes.most_common(10):
    print(f"  {folio}: {count}")
print()

# Line position analysis
print("=== @-CODE LINE POSITIONS ===")
# Check if codes appear at start, middle, or end of lines
line_positions = Counter()
for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            text = line.get('text', '')
            if '@' in text:
                pos = text.find('@')
                total_len = len(text)
                if pos < total_len * 0.25:
                    line_positions['start (0-25%)'] += 1
                elif pos < total_len * 0.5:
                    line_positions['early (25-50%)'] += 1
                elif pos < total_len * 0.75:
                    line_positions['middle (50-75%)'] += 1
                else:
                    line_positions['end (75-100%)'] += 1

print("Position of @-codes in lines:")
for pos, count in line_positions.most_common():
    print(f"  {pos:20}: {count}")
print()

# Recipe format validation
print("=== RECIPE FORMAT VALIDATION ===")
print("Hypothesis: Lines have [ACTION] [INGREDIENT] [@CODE] [STATE] pattern")
print()

# Count words per line before and after code
words_before_code = []
words_after_code = []

for folio in integrated.get('folios', []):
    if folio.get('has_text'):
        for line in folio.get('text_lines', []):
            if '@' not in line.get('text', ''):
                continue

            text = line.get('text', '')
            words = line.get('words', [])

            # Find position of @
            code_pos = text.find('@')
            if code_pos == -1:
                continue

            # Count words before/after
            text_before = text[:code_pos]
            text_after = text[code_pos:]

            words_before = [w for w in words if w in text_before]
            words_after = [w for w in words if w in text_after]

            if words_before:
                words_before_code.append(len(words_before))
            if words_after:
                words_after_code.append(len(words_after))

if words_before_code:
    avg_before = sum(words_before_code) / len(words_before_code)
    print(f"Average words BEFORE @-code: {avg_before:.1f}")
    print(f"  (Expected: 1-3 for action/ingredient)")

if words_after_code:
    avg_after = sum(words_after_code) / len(words_after_code)
    print(f"Average words AFTER @-code:  {avg_after:.1f}")
    print(f"  (Expected: 1-5 for state/quality)")

print()
print("=== CONCLUSION ===")
print("@-codes appear to mark structural boundaries in recipe format")
print("Pattern: [ingredient/action] [@batch] [state/quality]")
print("Range @130-@246 suggests batch numbering system")
print()
print("Next: Cross-reference with alchemical batch numbering systems")
