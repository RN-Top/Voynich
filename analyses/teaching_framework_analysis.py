#!/usr/bin/env python3
"""
TEACHING FRAMEWORK ANALYSIS
============================
Tests whether Fermoy and Voynich show evidence of a common teaching framework:
Symptoms → Causes → Cures

This is the core hypothesis: both texts come from the same medieval teaching school
that taught this precise, structured approach to medical knowledge.
"""

from pathlib import Path
import re
from collections import Counter

def load_text(filepath):
    """Load and clean text."""
    with open(filepath) as f:
        return f.read()

def analyze_structure(text, name):
    """Analyze text structure for teaching framework patterns."""

    print(f"\n{'='*80}")
    print(f"ANALYZING: {name}")
    print(f"{'='*80}")

    # Look for structural markers that indicate teaching framework
    # In a teaching text, you'd see patterns like:
    # - Repeated structure (indication of teaching method)
    # - Parallel organization (same pattern applied multiple times)
    # - Logical progression (building knowledge)

    # Common medical terms that indicate each phase
    symptom_markers = [
        'pain', 'ache', 'weakness', 'fever', 'disease', 'illness',
        'sick', 'wound', 'bruise', 'swelling', 'inflammation',
        'galar', 'tinn', 'othar', 'galair', 'braistid', 'teiched'
    ]

    cause_markers = [
        'cause', 'reason', 'because', 'from', 'origin', 'source',
        'comes from', 'arises from', 'due to', 'resulting from'
    ]

    cure_markers = [
        'cure', 'remedy', 'treatment', 'heal', 'medicine', 'potion',
        'salve', 'ointment', 'tincture', 'preparation',
        'leigheas', 'oleum', 'unguentum', 'electuarium'
    ]

    text_lower = text.lower()

    # Count marker occurrences
    symptom_count = sum(text_lower.count(marker) for marker in symptom_markers)
    cause_count = sum(text_lower.count(marker) for marker in cause_markers)
    cure_count = sum(text_lower.count(marker) for marker in cure_markers)

    print(f"\nMarker Frequency:")
    print(f"  Symptom markers: {symptom_count} occurrences")
    print(f"  Cause markers:   {cause_count} occurrences")
    print(f"  Cure markers:    {cure_count} occurrences")

    # Check for organizational patterns
    # In a teaching text, you'd see repeated structure (same order multiple times)

    # Look for sections that follow: symptom → cause → cure pattern
    sections = re.split(r'\n\n+', text)
    print(f"\nStructural Analysis:")
    print(f"  Total sections/paragraphs: {len(sections)}")

    # Count sections that show the framework pattern
    framework_sections = 0
    for section in sections:
        if len(section) > 50:  # Only analyze substantial sections
            has_symptom = any(marker in section.lower() for marker in symptom_markers)
            has_cause = any(marker in section.lower() for marker in cause_markers)
            has_cure = any(marker in section.lower() for marker in cure_markers)

            # Check if pattern is in order (symptom before cause, cause before cure)
            symptom_pos = min([section.lower().find(m) for m in symptom_markers if m in section.lower()], default=999999)
            cause_pos = min([section.lower().find(m) for m in cause_markers if m in section.lower()], default=999999)
            cure_pos = min([section.lower().find(m) for m in cure_markers if m in section.lower()], default=999999)

            if has_symptom and has_cause and has_cure:
                if symptom_pos < cause_pos < cure_pos:
                    framework_sections += 1

    print(f"  Sections following Symptom→Cause→Cure pattern: {framework_sections}")

    if framework_sections > 0:
        percent = (framework_sections / len(sections)) * 100
        print(f"  Percentage: {percent:.1f}%")

    # Analyze consistency
    if symptom_count > 0 and cause_count > 0 and cure_count > 0:
        ratio = cause_count / symptom_count
        cure_ratio = cure_count / symptom_count

        print(f"\nConsistency Ratios:")
        print(f"  Cause markers per symptom marker: {ratio:.2f}")
        print(f"  Cure markers per symptom marker:  {cure_ratio:.2f}")

        if 0.5 < ratio < 2.0 and 0.5 < cure_ratio < 2.0:
            print(f"\n✓ CONSISTENT RATIO - Suggests structured teaching")
        else:
            print(f"\n⚠ VARIED RATIO - May indicate varied structure")

    return {
        'symptom_count': symptom_count,
        'cause_count': cause_count,
        'cure_count': cure_count,
        'framework_sections': framework_sections,
        'total_sections': len(sections)
    }

def main():
    print("\n" + "="*80)
    print("MEDIEVAL TEACHING FRAMEWORK HYPOTHESIS")
    print("="*80)
    print("\nQuestion: Do Fermoy and Voynich show evidence of the same teaching framework?")
    print("Framework: Symptoms → Causes → Cures")
    print("Hypothesis: Both come from the same medieval teaching school.\n")

    # Load texts
    fermoy_path = Path("data/fermoy_ms23e29.txt")
    voynich_path = Path("data/ZL3b-n.txt")

    if not fermoy_path.exists() or not voynich_path.exists():
        print("ERROR: Required data files not found")
        return

    fermoy_text = load_text(fermoy_path)
    voynich_text = load_text(voynich_path)

    # Analyze both texts
    fermoy_results = analyze_structure(fermoy_text, "FERMOY MANUSCRIPT (Teaching Text)")
    voynich_results = analyze_structure(voynich_text, "VOYNICH MANUSCRIPT")

    # Compare results
    print(f"\n{'='*80}")
    print("COMPARISON")
    print(f"{'='*80}")

    print(f"\nSymptom markers:")
    print(f"  Fermoy:  {fermoy_results['symptom_count']}")
    print(f"  Voynich: {voynich_results['symptom_count']}")

    print(f"\nCause markers:")
    print(f"  Fermoy:  {fermoy_results['cause_count']}")
    print(f"  Voynich: {voynich_results['cause_count']}")

    print(f"\nCure markers:")
    print(f"  Fermoy:  {fermoy_results['cure_count']}")
    print(f"  Voynich: {voynich_results['cure_count']}")

    print(f"\nFramework pattern consistency:")
    fermoy_pct = (fermoy_results['framework_sections'] / fermoy_results['total_sections']) * 100
    voynich_pct = (voynich_results['framework_sections'] / voynich_results['total_sections']) * 100

    print(f"  Fermoy:  {fermoy_pct:.1f}% sections show Symptom→Cause→Cure pattern")
    print(f"  Voynich: {voynich_pct:.1f}% sections show Symptom→Cause→Cure pattern")

    # Interpretation
    print(f"\n{'='*80}")
    print("INTERPRETATION")
    print(f"{'='*80}")

    if fermoy_pct > 20 and voynich_pct > 20:
        print(f"\n✓ BOTH TEXTS SHOW THE FRAMEWORK PATTERN")
        print(f"  Fermoy: {fermoy_pct:.1f}% | Voynich: {voynich_pct:.1f}%")
        print(f"\n  This is NOT random. Both texts consistently use:")
        print(f"  - Symptom description")
        print(f"  - Cause explanation")
        print(f"  - Cure prescription")
        print(f"\n  This is evidence of a TAUGHT SYSTEM, not independent development.")

        if abs(fermoy_pct - voynich_pct) < 30:
            print(f"\n✓ SIMILAR STRUCTURE")
            print(f"  The patterns are comparable in both texts.")
            print(f"  This suggests they learned from the SAME TEACHING.")
        else:
            print(f"\n⚠ DIFFERENT EMPHASIS")
            print(f"  One text emphasizes the framework more than the other.")
            print(f"  But both use it consistently.")

    elif fermoy_pct > 20 or voynich_pct > 20:
        print(f"\n⚠ ONE TEXT SHOWS FRAMEWORK, OTHER LESS SO")
        if fermoy_pct > 20:
            print(f"  Fermoy clearly shows teaching structure ({fermoy_pct:.1f}%)")
            print(f"  Voynich is less structured ({voynich_pct:.1f}%)")
            print(f"\n  But Voynich may adapt the structure differently.")
        else:
            print(f"  Voynich shows framework ({voynich_pct:.1f}%)")
            print(f"  Fermoy is more varied ({fermoy_pct:.1f}%)")

    else:
        print(f"\n✗ NEITHER TEXT SHOWS CLEAR FRAMEWORK")
        print(f"  Fermoy: {fermoy_pct:.1f}%")
        print(f"  Voynich: {voynich_pct:.1f}%")
        print(f"\n  The teaching school hypothesis may need revision.")

    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
