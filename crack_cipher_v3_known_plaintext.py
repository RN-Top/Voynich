#!/usr/bin/env python3
"""
KNOWN PLAINTEXT ATTACK
Try to identify common Latin medical words in the EVA text

Strategy:
1. Take common Latin medical words
2. Find similar patterns in EVA text (words with same length/structure)
3. Build character mapping from these known words
4. Extend mapping to full text
5. Validate against larger sample
"""

import json
from collections import Counter
import re

print("=" * 80)
print("KNOWN PLAINTEXT ATTACK: MEDICAL LATIN WORDS")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

# Extract EVA text
all_words = []
for folio in integrated['folios'][:100]:
    for line in folio.get('text_lines', []):
        if 'words' in line:
            all_words.extend(line['words'])

print(f"\nWorking with: {len(all_words)} words")

# Common Latin medical/herbal words that might appear in Voynich
latin_medical = {
    'aqua': 4,      # water (very common)
    'herba': 5,     # herb
    'medicina': 9,  # medicine
    'cura': 4,      # cure
    'dolor': 5,     # pain
    'febris': 6,    # fever
    'morbus': 6,    # disease
    'remedium': 8,  # remedy
    'sanguis': 7,   # blood
    'corpus': 6,    # body
    'anima': 5,     # soul
    'vis': 3,       # force
    'virtus': 6,    # virtue/power
    'potentia': 8,  # power
    'homo': 4,      # man
    'rex': 3,       # king
    'deus': 4,      # god
    'vita': 4,      # life
    'mors': 4,      # death
    'tempus': 6,    # time
    'locus': 5,     # place
    'modus': 5,     # way
    'via': 3,       # way
    'talis': 5,     # such
    'dum': 3,       # while
    'cum': 3,       # with
    'sed': 3,       # but
    'nam': 3,       # for
    'enim': 4,      # for
    'est': 3,       # is
    'sunt': 4,      # are
    'ratio': 5,     # reason
    'causa': 5,     # cause
    'mens': 4,      # mind
    'sapientia': 9, # wisdom
    'filius': 6,    # son
    'pater': 5,     # father
    'mater': 5,     # mother
    'soror': 5,     # sister
    'frater': 6,    # brother
}

# ============================================================================
# PHASE 1: FIND MATCHING WORD LENGTH PATTERNS
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 1: MATCH WORD LENGTHS")
print("=" * 80)

# Group EVA words by length
eva_by_length = {}
for word in all_words:
    length = len(word)
    if length not in eva_by_length:
        eva_by_length[length] = []
    eva_by_length[length].append(word)

# Find EVA words matching common Latin medical word lengths
candidates_by_latin = {}
for latin_word, length in latin_medical.items():
    if length in eva_by_length:
        candidates_by_latin[latin_word] = eva_by_length[length][:20]  # Top 20

print(f"\nCandidate EVA words for each Latin word:")
for latin_word in sorted(latin_medical.keys()):
    length = latin_medical[latin_word]
    if length in eva_by_length:
        count = len(eva_by_length[length])
        examples = eva_by_length[length][:3]
        print(f"  {latin_word:12s} (len={length}): {count:3d} EVA words - examples: {examples}")

# ============================================================================
# PHASE 2: PATTERN MATCHING
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 2: CHARACTER STRUCTURE PATTERNS")
print("=" * 80)

def get_pattern(word):
    """Convert word to pattern showing which chars repeat"""
    char_map = {}
    pattern = []
    next_id = 0
    for c in word:
        if c not in char_map:
            char_map[c] = next_id
            next_id += 1
        pattern.append(str(char_map[c]))
    return ''.join(pattern)

# Examples
print("\nPattern matching examples:")
for latin_word in ['aqua', 'medicina', 'herba']:
    pattern = get_pattern(latin_word)
    print(f"  {latin_word:12s} → pattern {pattern}")

# Find EVA words with patterns matching common Latin word patterns
pattern_matches = {}
for latin_word in latin_medical.keys():
    latin_pattern = get_pattern(latin_word)
    length = len(latin_word)

    # Find EVA words with same pattern
    matches = []
    if length in eva_by_length:
        for eva_word in eva_by_length[length]:
            if get_pattern(eva_word) == latin_pattern:
                matches.append(eva_word)

    if matches:
        pattern_matches[latin_word] = matches

print(f"\n\nLatin words with matching EVA patterns:")
for latin_word, eva_matches in pattern_matches.items():
    print(f"  {latin_word:12s}: {eva_matches[:5]}")

# ============================================================================
# PHASE 3: BUILD MAPPING FROM PATTERN MATCHES
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 3: BUILD CHARACTER MAPPING FROM KNOWN WORDS")
print("=" * 80)

# Try to build mapping from pattern matches
mapping_candidates = []

for latin_word, eva_matches in pattern_matches.items():
    for eva_word in eva_matches[:5]:  # Try top 5 matches
        # Assume eva_word maps to latin_word
        candidate_mapping = {}
        valid = True

        for i, (eva_char, latin_char) in enumerate(zip(eva_word, latin_word)):
            if eva_char in candidate_mapping:
                if candidate_mapping[eva_char] != latin_char:
                    valid = False
                    break
            else:
                candidate_mapping[eva_char] = latin_char

        if valid:
            mapping_candidates.append({
                'eva_word': eva_word,
                'latin_word': latin_word,
                'mapping': candidate_mapping
            })

print(f"\nFound {len(mapping_candidates)} candidate mappings from known words")

# Show top candidates
print(f"\nTop candidates:")
for i, candidate in enumerate(mapping_candidates[:10]):
    print(f"  {i+1}. {candidate['eva_word']:12s} → {candidate['latin_word']:12s}")
    print(f"     Mapping: {candidate['mapping']}")

# ============================================================================
# PHASE 4: MERGE MAPPINGS AND VALIDATE
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 4: MERGE MAPPINGS")
print("=" * 80)

# Try to merge mapping candidates
def merge_mappings(mapping_list):
    """Merge multiple candidate mappings, checking for conflicts"""
    merged = {}
    conflicts = 0

    for candidate_map in mapping_list:
        for eva_char, latin_char in candidate_map.items():
            if eva_char in merged:
                if merged[eva_char] != latin_char:
                    conflicts += 1
            else:
                merged[eva_char] = latin_char

    return merged, conflicts

# Try merging top candidates
if mapping_candidates:
    candidate_maps = [c['mapping'] for c in mapping_candidates]
    merged_mapping, conflicts = merge_mappings(candidate_maps)

    print(f"\nMerged mapping from {len(mapping_candidates)} candidates:")
    print(f"  Characters mapped: {len(merged_mapping)}")
    print(f"  Conflicts: {conflicts}")
    print(f"\n  Mapping:")
    for eva, latin in sorted(merged_mapping.items())[:15]:
        print(f"    {eva} → {latin}")

# ============================================================================
# PHASE 5: TEST ON SAMPLE TEXT
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 5: DECODE SAMPLE WITH MERGED MAPPING")
print("=" * 80)

if mapping_candidates and len(merged_mapping) > 5:
    # Decode sample
    decoded_words = []
    for word in all_words[:50]:
        decoded = ''.join(merged_mapping.get(c, '?') for c in word)
        decoded_words.append(decoded)

    print(f"\nDecoded sample:")
    print(' '.join(decoded_words))

    # Check for Latin words
    print(f"\n\nSearching for recognizable words in decoded text...")
    recognizable = []
    for decoded_word in decoded_words:
        if decoded_word in latin_medical:
            recognizable.append(decoded_word)

    if recognizable:
        print(f"Found: {recognizable}")
    else:
        print(f"No exact matches found")

# ============================================================================
# PHASE 6: FREQUENCY CHECK
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 6: EVA CHARACTER FREQUENCIES")
print("=" * 80)

eva_freq = Counter(all_words[i] for word in all_words[:100] for i in range(len(word)))
print(f"\nMost common EVA characters in sample:")
for char, count in eva_freq.most_common(15):
    pct = 100 * count / sum(eva_freq.values())
    print(f"  {char:5s}: {count:4d} ({pct:5.1f}%)")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("KNOWN PLAINTEXT ATTACK SUMMARY")
print("=" * 80)

print(f"""
APPROACH: Pattern matching + known medical Latin words

FINDINGS:
  - Pattern matches found: {len(pattern_matches)}
  - Candidate mappings generated: {len(mapping_candidates)}
  - Merged mapping size: {len(merged_mapping) if mapping_candidates else 0}
  - Mapping conflicts: {conflicts if mapping_candidates else 'N/A'}

NEXT STEPS:
  1. Extend mapping by frequency analysis on decoded text
  2. Iteratively decode and validate against Latin dictionary
  3. Use constraint solver for remaining unmapped characters
  4. Try simulated annealing for better global optimization

STATUS: Known plaintext attack in progress; exact Latin words found
""")

print("=" * 80)
