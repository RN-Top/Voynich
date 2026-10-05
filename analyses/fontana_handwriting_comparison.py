#!/usr/bin/env python3
"""
Giovanni Fontana Handwriting Comparison against Voynich Scribal Hands

Methodology: Paleographic analysis comparing Fontana's known manuscripts
to the 5 identified scribal hands in the Voynich manuscript.

Reference: Lisa Fagin Davis, "The Voynich Manuscript: Evidence for Five
Distinct Scribal Hands" (2020)

Usage:
    python3 fontana_handwriting_comparison.py --fontana-dir ./data/fontana \
                                              --voynich-dir ./data/voynich \
                                              --output ./results/comparison.txt
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class PaleographicAnalysis:
    """Systematic comparison of handwriting characteristics."""

    def __init__(self, output_file: str = None):
        self.output_file = output_file
        self.results = []
        self.timestamp = datetime.now().isoformat()

    def analyze_fontana_manuscripts(self, fontana_dir: str) -> Dict:
        """
        Analyze Fontana's known manuscripts for handwriting characteristics.

        Focus areas:
        - Letter formations (a, e, r, s, t)
        - Abbreviations and cipher notation
        - Flourishes and decorative elements
        - Pen angle and pressure variations
        - Word spacing and alignment
        """
        fontana_data = {
            "secretum_de_thesauro": {
                "archive": "Bibliothèque Nationale de France (Paris)",
                "link": "https://gallica.bnf.fr/ark:/12148/btv1b100331057.image",
                "date": "1420s",
                "characteristics": {
                    "letter_formations": "TO BE DOCUMENTED - examine title pages and cipher notation",
                    "abbreviations": "TO BE DOCUMENTED - check medical and mathematical terms",
                    "flourishes": "TO BE DOCUMENTED - note decorative elements",
                    "pen_angle": "TO BE DOCUMENTED - observe from diagonal strokes",
                    "spacing": "TO BE DOCUMENTED - measure word and line spacing"
                }
            },
            "bellicorum_instrumentorum": {
                "archive": "Bayerische Staatsbibliothek (Munich)",
                "link": "https://www.digitale-sammlungen.de/en/details/bsb00013084",
                "date": "1420-1430",
                "characteristics": {
                    "letter_formations": "TO BE DOCUMENTED - examine diagram labels and notes",
                    "abbreviations": "TO BE DOCUMENTED - check technical notation",
                    "flourishes": "TO BE DOCUMENTED - note signature style",
                    "pen_angle": "TO BE DOCUMENTED - observe from drawn lines",
                    "spacing": "TO BE DOCUMENTED - measure margins and alignment"
                }
            }
        }
        return fontana_data

    def identify_voynich_hands(self) -> Dict:
        """
        Document the 5 identified scribal hands in Voynich.

        Reference: Lisa Fagin Davis paleographic analysis (2020)
        """
        voynich_hands = {
            "main_hand": {
                "coverage": "60-70% of manuscript",
                "characteristics": "TO BE DOCUMENTED - dominant scribe",
                "pages": "TO BE DOCUMENTED - specify page ranges",
                "distinctive_features": []
            },
            "hand_b": {
                "coverage": "Moderate presence",
                "characteristics": "TO BE DOCUMENTED - secondary scribe",
                "pages": "TO BE DOCUMENTED - specify page ranges",
                "distinctive_features": []
            },
            "hand_c": {
                "coverage": "Moderate presence",
                "characteristics": "TO BE DOCUMENTED - recipe section possibly",
                "pages": "TO BE DOCUMENTED - specify page ranges",
                "distinctive_features": []
            },
            "hand_d": {
                "coverage": "Minimal presence",
                "characteristics": "TO BE DOCUMENTED - marginal notes/additions",
                "pages": "TO BE DOCUMENTED - specify page ranges",
                "distinctive_features": []
            },
            "hand_e": {
                "coverage": "Rare",
                "characteristics": "TO BE DOCUMENTED - specific pages/colophons",
                "pages": "TO BE DOCUMENTED - specify page ranges",
                "distinctive_features": []
            }
        }
        return voynich_hands

    def compare_handwriting(self, fontana_data: Dict, voynich_hands: Dict) -> List[Dict]:
        """
        Compare Fontana's characteristics to each Voynich hand.

        Scoring: HIGH / MEDIUM / LOW confidence based on:
        - Letter shape matches
        - Abbreviation patterns
        - Flourish styles
        - Spatial organization
        - Cipher notation methods
        """
        comparisons = []

        for manuscript, details in fontana_data.items():
            for hand_name, hand_details in voynich_hands.items():
                comparison = {
                    "fontana_manuscript": manuscript,
                    "voynich_hand": hand_name,
                    "confidence": "PENDING - requires image analysis",
                    "matches": {
                        "letter_formations": "PENDING",
                        "abbreviations": "PENDING",
                        "flourishes": "PENDING",
                        "pen_characteristics": "PENDING",
                        "spatial_patterns": "PENDING"
                    },
                    "notes": "Awaiting high-resolution manuscript images for detailed comparison",
                    "analysis_date": None
                }
                comparisons.append(comparison)

        return comparisons

    def generate_report(self, fontana_data: Dict, voynich_hands: Dict,
                       comparisons: List[Dict]) -> str:
        """Generate structured comparison report."""

        report = []
        report.append("=" * 80)
        report.append("GIOVANNI FONTANA HANDWRITING COMPARISON REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {self.timestamp}")
        report.append("")

        # Section 1: Fontana Manuscripts
        report.append("SECTION 1: FONTANA'S KNOWN MANUSCRIPTS")
        report.append("-" * 80)
        for manuscript, details in fontana_data.items():
            report.append(f"\n{manuscript.upper()}")
            report.append(f"  Archive: {details['archive']}")
            report.append(f"  Link: {details['link']}")
            report.append(f"  Date: {details['date']}")
            report.append("  Characteristics to analyze:")
            for char, status in details['characteristics'].items():
                report.append(f"    - {char}: {status}")

        report.append("\n")

        # Section 2: Voynich Hands
        report.append("SECTION 2: VOYNICH SCRIBAL HANDS (Lisa Fagin Davis 2020)")
        report.append("-" * 80)
        for hand, details in voynich_hands.items():
            report.append(f"\n{hand.upper()}")
            report.append(f"  Coverage: {details['coverage']}")
            report.append(f"  Characteristics: {details['characteristics']}")
            report.append(f"  Pages: {details['pages']}")

        report.append("\n")

        # Section 3: Comparison Matrix
        report.append("SECTION 3: COMPARISON MATRIX")
        report.append("-" * 80)
        report.append("\nFontana vs. Voynich Hands (Confidence Scoring):\n")

        for comp in comparisons:
            report.append(f"{comp['fontana_manuscript']} vs {comp['voynich_hand']}: {comp['confidence']}")
            if comp['notes']:
                report.append(f"  Notes: {comp['notes']}")

        report.append("\n")

        # Section 4: Next Steps
        report.append("SECTION 4: NEXT STEPS")
        report.append("-" * 80)
        report.append("""
1. Download high-resolution images from:
   - Fontana Secretum: https://gallica.bnf.fr/ark:/12148/btv1b100331057.image
   - Fontana Bellicorum: https://www.digitale-sammlungen.de/en/details/bsb00013084
   - Voynich hands: Use Davis paleographic analysis or Beinecke digitized pages

2. Compare letter formations:
   - Focus on common letters (a, e, r, s, t)
   - Note distinctive features (loops, terminals, serifs)
   - Measure x-height and ascender/descender ratios

3. Score each hand match:
   - HIGH: Multiple matching characteristics across multiple samples
   - MEDIUM: Some matching characteristics, inconsistencies present
   - LOW: Few or no matching characteristics

4. Document findings:
   - Update this report with specific page references
   - Include image references/links to supporting evidence
   - Note confidence level for each match

5. Cross-reference with CIPERB database:
   - Find Fontana's enrollment record
   - Identify his classmates (potential collaborators)
   - Look for documented collaborative projects
        """)

        report.append("\n" + "=" * 80)

        return "\n".join(report)

    def save_report(self, report: str):
        """Save report to file if output path specified."""
        if self.output_file:
            Path(self.output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {self.output_file}")
        else:
            print(report)

    def run(self, fontana_dir: str = None, voynich_dir: str = None):
        """Execute full analysis."""
        print("Initializing Fontana Handwriting Comparison Analysis...")

        fontana_data = self.analyze_fontana_manuscripts(fontana_dir)
        voynich_hands = self.identify_voynich_hands()
        comparisons = self.compare_handwriting(fontana_data, voynich_hands)

        report = self.generate_report(fontana_data, voynich_hands, comparisons)
        self.save_report(report)

        # Also save structured data as JSON
        if self.output_file:
            json_output = self.output_file.replace('.txt', '.json')
            data = {
                "timestamp": self.timestamp,
                "fontana": fontana_data,
                "voynich_hands": voynich_hands,
                "comparisons": comparisons
            }
            with open(json_output, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Structured data saved to: {json_output}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare Giovanni Fontana handwriting to Voynich scribal hands"
    )
    parser.add_argument("--fontana-dir", default="./data/fontana",
                       help="Directory containing Fontana manuscript images")
    parser.add_argument("--voynich-dir", default="./data/voynich",
                       help="Directory containing Voynich hand samples")
    parser.add_argument("--output", default="./results/fontana_comparison.txt",
                       help="Output file for comparison report")

    args = parser.parse_args()

    analyzer = PaleographicAnalysis(output_file=args.output)
    analyzer.run(fontana_dir=args.fontana_dir, voynich_dir=args.voynich_dir)


if __name__ == "__main__":
    main()
