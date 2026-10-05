#!/usr/bin/env python3
"""
SOURCE TEXT ANALYZER
====================
Analyzes any medieval medical text for evidence of the
Symptoms→Causes→Cures teaching framework.

This tool will be used to search through historical manuscripts
to find the ORIGIN - the source text that all others derive from.

Usage:
  python3 source_text_analyzer.py <path_to_text>

Returns: Framework score, language characteristics, likely region/tradition
"""

import sys
from pathlib import Path
import re
from collections import Counter

def analyze_text_for_framework(text, text_name="Unknown"):
    """
    Analyze a text for Symptoms→Causes→Cures framework evidence.

    Returns comprehensive analysis of how the text is organized.
    """
    print("\n" + "="*80)
    print(f"ANALYZING: {text_name}")
    print("="*80)

    # Normalize text
    text_lower = text.lower()
    lines = text.split('\n')

    # === LANGUAGE DETECTION ===
    print(f"\n1. LANGUAGE CHARACTERISTICS")
    print("-" * 80)

    # Check for known patterns in different languages
    language_markers = {
        'Latin': ['morbus', 'causa', 'remedium', 'curatio', 'aegrotus', 'materia', 'virtus'],
        'Irish': ['tinn', 'galar', 'leigheas', 'oleum', 'unguentum', 'gréine', 'fir'],
        'Middle English': ['disease', 'cause', 'cure', 'remedy', 'medicine', 'potion', 'herb'],
        'German': ['krankheit', 'ursache', 'heilung', 'arznei', 'kraut', 'mittel'],
        'French/Occitan': ['maladie', 'cause', 'remede', 'guérison', 'herbe', 'potion'],
        'Italian/Spanish': ['malattia', 'causa', 'cura', 'rimedio', 'medicamento', 'erba'],
    }

    lang_scores = {}
    for lang, markers in language_markers.items():
        score = sum(text_lower.count(marker) for marker in markers)
        lang_scores[lang] = score

    detected_lang = max(lang_scores, key=lang_scores.get)
    print(f"Likely language: {detected_lang} (score: {lang_scores[detected_lang]})")

    # === FRAMEWORK DETECTION ===
    print(f"\n2. FRAMEWORK SIGNATURE DETECTION")
    print("-" * 80)

    # Define framework markers in multiple languages
    framework_markers = {
        'symptom': {
            'Latin': ['morbus', 'aegritudo', 'dolor', 'infirmitas', 'passio', 'malum'],
            'Irish': ['tinn', 'galar', 'othar', 'braistid', 'ailech'],
            'English': ['disease', 'pain', 'illness', 'sickness', 'suffering', 'weakness'],
            'General': ['hurt', 'ache', 'fever', 'inflammation', 'wound', 'swelling']
        },
        'causation': {
            'Latin': ['causa', 'ex', 'ab', 'per', 'propter', 'ratione'],
            'Irish': ['o', 'as', 'de', 'ar bhaile', 'do bharr'],
            'English': ['because', 'from', 'caused', 'comes', 'results', 'due to', 'reason'],
            'General': ['makes', 'causes', 'leads to', 'from', 'arise']
        },
        'remedy': {
            'Latin': ['remedium', 'curatio', 'medicina', 'antidotum', 'sanatio', 'unguentum'],
            'Irish': ['leigheas', 'oleum', 'unguentum', 'ointment', 'leactha'],
            'English': ['cure', 'remedy', 'medicine', 'treatment', 'heal', 'use'],
            'General': ['apply', 'take', 'use', 'potion', 'herb', 'plant', 'preparation']
        }
    }

    # Count framework markers
    framework_counts = {}
    for phase, variants in framework_markers.items():
        all_markers = []
        for lang_markers in variants.values():
            all_markers.extend(lang_markers)

        count = sum(text_lower.count(marker) for marker in all_markers)
        framework_counts[phase] = count

    print(f"Symptom markers: {framework_counts['symptom']:6d} occurrences")
    print(f"Causation markers: {framework_counts['causation']:6d} occurrences")
    print(f"Remedy markers: {framework_counts['remedy']:6d} occurrences")

    # Calculate framework strength
    if framework_counts['symptom'] > 0:
        cause_ratio = framework_counts['causation'] / framework_counts['symptom']
        remedy_ratio = framework_counts['remedy'] / framework_counts['symptom']

        print(f"\nRatios (compared to symptoms):")
        print(f"  Causation/Symptoms: {cause_ratio:.2f}")
        print(f"  Remedy/Symptoms:    {remedy_ratio:.2f}")

        # Strong framework signal: balanced ratios
        if 0.3 < cause_ratio < 2.0 and 0.3 < remedy_ratio < 2.0:
            framework_strength = "STRONG"
        elif cause_ratio > 0 and remedy_ratio > 0:
            framework_strength = "MODERATE"
        else:
            framework_strength = "WEAK"

        print(f"\nFramework Strength: {framework_strength}")

    # === STRUCTURAL ORGANIZATION ===
    print(f"\n3. STRUCTURAL ORGANIZATION")
    print("-" * 80)

    # Look for entry structure (entries separated by breaks)
    sections = re.split(r'\n\n+|\n\.\n|\n---', text)
    print(f"Identified sections: {len(sections)}")

    # Analyze entry depth (entries should have internal structure)
    avg_section_length = sum(len(s) for s in sections) / len(sections) if sections else 0
    print(f"Average section length: {avg_section_length:.0f} characters")

    # Look for repeated patterns (sign of teaching material)
    pattern_repetitions = re.findall(r'(.{20,50})', text)
    if pattern_repetitions:
        repeated = Counter(pattern_repetitions)
        top_repeats = repeated.most_common(3)
        print(f"\nMost repeated patterns (signs of teaching structure):")
        for pattern, count in top_repeats:
            if count > 2:
                clean_pattern = ' '.join(pattern.strip().split())[:50]
                print(f"  [{count}x] {clean_pattern}...")

    # === PEDAGOGICAL INDICATORS ===
    print(f"\n4. TEACHING MATERIAL INDICATORS")
    print("-" * 80)

    teaching_markers = {
        'formulaic': r'(here|thus|as follows|it follows|note that|observe|take|use)',
        'explicit_order': r'(first|second|then|next|after|before|finally)',
        'repetition': r'(for example|similarly|likewise|also|again)',
        'measurements': r'(\d+\s*(drops|grains|drams|ounces|parts|portions|amounts))',
        'timing': r'(spring|summer|autumn|winter|morning|evening|night|season)',
    }

    for marker_type, pattern in teaching_markers.items():
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        print(f"{marker_type:20s}: {len(matches):4d} occurrences")

    # === DATING CLUES ===
    print(f"\n5. DATING INDICATORS")
    print("-" * 80)

    dating_clues = {
        'Medieval Latin': ['aqua vitae', 'apothecary', 'bloodletting', 'humors', 'temperaments'],
        'Early Modern': ['distillation', 'distilled', 'quintessence', 'alchemical'],
        'Ancient references': ['Galen', 'Hippocrates', 'Dioscorides', 'Avicenna', 'Rhazes'],
    }

    for period, markers in dating_clues.items():
        count = sum(text_lower.count(m) for m in markers)
        if count > 0:
            print(f"{period}: {count} references")

    # === FINAL ASSESSMENT ===
    print(f"\n" + "="*80)
    print("ASSESSMENT")
    print("="*80)

    # Is this a teaching text?
    teaching_score = (
        (framework_counts['causation'] > 0) * 25 +
        (framework_counts['remedy'] > 0) * 25 +
        (len(sections) > 10) * 15 +
        (avg_section_length > 200) * 15 +
        (any('repeated' in k for k in teaching_markers.keys())) * 20
    ) / 100

    print(f"\nTeaching Material Score: {teaching_score:.0%}")

    if teaching_score > 0.7:
        print("✓ LIKELY A FORMAL TEACHING TEXT")
    elif teaching_score > 0.4:
        print("⚠ POSSIBLY TEACHING MATERIAL (mixed content)")
    else:
        print("✗ UNCLEAR IF TEACHING MATERIAL")

    # Is this possibly the source?
    print(f"\nPossibility of being ORIGINAL SOURCE:")

    if detected_lang == 'Latin' and framework_strength == "STRONG":
        print("✓ VERY HIGH (Latin teaching text with strong framework)")
    elif detected_lang == 'Latin':
        print("⚠ HIGH (Latin text, but framework clarity varies)")
    elif detected_lang == 'Irish':
        print("⚠ MODERATE (Irish adaptation, not original)")
    else:
        print("⚠ UNKNOWN (needs context on language/dating)")

    return {
        'text_name': text_name,
        'language': detected_lang,
        'framework_strength': framework_strength,
        'teaching_score': teaching_score,
        'sections': len(sections),
    }


def main():
    if len(sys.argv) < 2:
        print("""
SOURCE TEXT ANALYZER
====================

This tool searches historical medical texts for the Symptoms→Causes→Cures
teaching framework to identify the ORIGIN of the tradition.

Usage:
  python3 source_text_analyzer.py <path_to_text>

Example:
  python3 source_text_analyzer.py data/fermoy_ms23e29.txt
  python3 source_text_analyzer.py data/ZL3b-n.txt

What it detects:
  ✓ Language characteristics
  ✓ Framework strength (Symptoms→Causes→Cures pattern)
  ✓ Teaching material indicators
  ✓ Dating clues
  ✓ Likelihood of being the original source

HYPOTHESIS:
The original teaching text was likely:
  - Written in LATIN (universal academic language)
  - From ~1300 or earlier
  - From EASTERN EUROPE (per user hypothesis)
  - With clear Symptoms→Causes→Cures structure
  - Evidence of formal teaching institution

All adaptations (Irish, Voynich, others) derive from this original.
""")
        return

    text_path = Path(sys.argv[1])

    if not text_path.exists():
        print(f"ERROR: File not found: {text_path}")
        return

    with open(text_path) as f:
        text = f.read()

    result = analyze_text_for_framework(text, text_path.name)

    print(f"\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("""
To find the ORIGIN:
1. Run this analyzer on known source texts
2. Look for Latin texts with STRONG framework signal
3. Compare dating indicators
4. Find the OLDEST version with the clearest structure
5. That's your source text

Recommended texts to check:
  - Regimen Sanitatis (12th-13th century)
  - Circa Instans (Urso's herbal)
  - Antidotarium Nicolai
  - Medical works from Prague/Krakow universities
  - Herbals from Eastern European medical schools

The SOURCE TEXT will show:
  ✓ Latin language
  ✓ STRONG Symptoms→Causes→Cures framework
  ✓ Teaching structure (repetition, measurements, timing)
  ✓ Dating to ~1200-1300
  ✓ Evidence connecting to regional adaptations
""")


if __name__ == "__main__":
    main()
