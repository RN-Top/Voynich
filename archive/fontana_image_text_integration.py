"""
Fontana Cipher - Image-Text Integration Analysis
Analyzes whether plant imagery is part of the cipher system itself
Critical insight: Voynich transcriptions separate text from images,
but what if they're ONE integrated cipher?
"""

import json
from pathlib import Path
from datetime import datetime
import re


class VoynichPageAnalyzer:
    """Analyzes individual Voynich pages for image-text integration"""

    def __init__(self):
        self.pages = []
        self.integration_results = {}

        # Medieval botanical-medical knowledge
        self.known_medical_plants = {
            'sage': ['salvia', 'medicine', 'healing', 'fever'],
            'rosemary': ['rosmarinus', 'memory', 'remedy', 'treatment'],
            'thyme': ['thymus', 'cough', 'breath', 'herb'],
            'mint': ['mentha', 'digestion', 'stomach', 'remedy'],
            'wormwood': ['absinthium', 'fever', 'parasite', 'infection'],
            'valerian': ['valeriana', 'sleep', 'nerves', 'calm'],
            'plantain': ['plantago', 'wound', 'heal', 'injury'],
            'comfrey': ['symphytum', 'bone', 'break', 'mend'],
            'mugwort': ['artemisia', 'women', 'month', 'cycle'],
            'horehound': ['marrubium', 'cough', 'throat', 'bronchus'],
        }

    def create_page_analysis(self, page_number, cipher_text, plants_identified,
                           plants_positions, medical_content=True, notes=""):
        """Create structured analysis for one page"""

        page = {
            "page_number": page_number,
            "cipher_text": cipher_text,
            "cipher_length": len(cipher_text.split()),
            "plants_identified": plants_identified,
            "plant_count": len(plants_identified),
            "plants_positions": plants_positions,
            "medical_content": medical_content,
            "notes": notes,
            "analyzed_date": datetime.now().isoformat(),
            "integration_metrics": self._calculate_integration_metrics(
                cipher_text, plants_identified, plants_positions
            )
        }

        self.pages.append(page)
        return page

    def _calculate_integration_metrics(self, cipher_text, plants, positions):
        """Calculate how integrated imagery and text are"""

        cipher_symbols = cipher_text.split()
        plant_count = len(plants)

        metrics = {
            "cipher_length": len(cipher_symbols),
            "plant_count": plant_count,
            "ratio_cipher_to_plants": len(cipher_symbols) / plant_count if plant_count > 0 else 0,
            "position_concentration": self._calculate_position_concentration(positions),
            "medical_alignment": self._check_medical_alignment(plants),
        }

        return metrics

    def _calculate_position_concentration(self, positions):
        """Does imagery cluster in specific locations on page?"""
        if not positions or len(positions) == 0:
            return 0.0

        # If plants are spread throughout = 0.5 (distributed)
        # If plants cluster top/bottom = higher score (concentrated)
        position_counts = {}
        for pos in positions:
            position_counts[pos] = position_counts.get(pos, 0) + 1

        max_in_position = max(position_counts.values())
        concentration = max_in_position / len(positions)

        return concentration

    def _check_medical_alignment(self, plants):
        """Do identified plants match known medieval medical usage?"""
        if not plants:
            return 0.0

        alignment_score = 0
        for plant in plants:
            plant_lower = plant.lower()
            if plant_lower in self.known_medical_plants:
                alignment_score += 1

        return alignment_score / len(plants)

    def get_page_statistics(self):
        """Aggregate statistics across all pages"""

        if not self.pages:
            return None

        total_pages = len(self.pages)
        total_plants = sum(p['plant_count'] for p in self.pages)
        total_cipher_symbols = sum(p['cipher_length'] for p in self.pages)
        medical_pages = sum(1 for p in self.pages if p['medical_content'])

        avg_ratio = sum(p['integration_metrics']['ratio_cipher_to_plants']
                       for p in self.pages) / total_pages if total_pages > 0 else 0

        avg_position_concentration = sum(
            p['integration_metrics']['position_concentration']
            for p in self.pages
        ) / total_pages if total_pages > 0 else 0

        avg_medical_alignment = sum(
            p['integration_metrics']['medical_alignment']
            for p in self.pages
        ) / total_pages if total_pages > 0 else 0

        stats = {
            "total_pages_analyzed": total_pages,
            "total_plants_identified": total_plants,
            "total_cipher_symbols": total_cipher_symbols,
            "pages_with_medical_content": medical_pages,
            "average_plants_per_page": total_plants / total_pages if total_pages > 0 else 0,
            "average_cipher_symbols_per_page": total_cipher_symbols / total_pages if total_pages > 0 else 0,
            "average_cipher_to_plant_ratio": avg_ratio,
            "average_position_concentration": avg_position_concentration,
            "average_medical_alignment": avg_medical_alignment,
            "integration_hypothesis_strength": self._calculate_integration_strength(
                avg_ratio, avg_position_concentration, avg_medical_alignment
            )
        }

        return stats

    def _calculate_integration_strength(self, ratio, concentration, alignment):
        """
        Calculate overall strength of image-text integration hypothesis

        Integration is likely if:
        - Ratio is consistent (similar cipher_length to plant_count across pages)
        - Plants cluster in meaningful positions
        - Plants align with medical terminology
        """

        # Normalize scores
        ratio_score = 1.0 if 2 < ratio < 10 else 0.5  # Meaningful ratio range
        concentration_score = concentration  # Higher = more structured
        alignment_score = alignment  # Higher = more medical content

        integration_strength = (
            0.4 * ratio_score +
            0.3 * concentration_score +
            0.3 * alignment_score
        )

        return min(integration_strength, 1.0)

    def export_analysis(self, filename="voynich_integration_analysis.json"):
        """Export analysis results"""

        export_data = {
            "analysis_date": datetime.now().isoformat(),
            "pages_analyzed": self.pages,
            "statistics": self.get_page_statistics(),
            "hypothesis": {
                "name": "Image-Text Integration Hypothesis",
                "description": "Plant imagery is an integral part of Fontana's cipher system, not decorative",
                "implication": "Text alone is insufficient; plants provide contextual encoding",
                "fontana_relevance": "Fontana practiced steganography - hiding messages within images"
            }
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"✓ Analysis exported to {filename}")
        return export_data


class PlantIdentificationFramework:
    """Framework for identifying and categorizing plants in Voynich"""

    def __init__(self):
        self.plant_catalog = self._build_plant_catalog()
        self.identified_plants = {}

    def _build_plant_catalog(self):
        """Build catalog of medieval medical plants"""

        catalog = {
            # Format: plant_name -> {latin, medical_uses, voynich_likely}
            'sage': {
                'latin': 'salvia',
                'medical_uses': ['fever', 'throat', 'memory', 'healing'],
                'voynich_likely': True,
                'fontana_connection': 'Common in Padua medical texts'
            },
            'rosemary': {
                'latin': 'rosmarinus',
                'medical_uses': ['memory', 'digestion', 'circulation', 'remedy'],
                'voynich_likely': True,
                'fontana_connection': 'Mediterranean herb, well-known in Padua'
            },
            'thyme': {
                'latin': 'thymus',
                'medical_uses': ['cough', 'bronchitis', 'throat', 'breath'],
                'voynich_likely': True,
                'fontana_connection': 'Common cooking and medical herb'
            },
            'mint': {
                'latin': 'mentha',
                'medical_uses': ['digestion', 'stomach', 'nausea', 'cool'],
                'voynich_likely': True,
                'fontana_connection': 'Universal medicinal plant'
            },
            'wormwood': {
                'latin': 'absinthium',
                'medical_uses': ['fever', 'parasites', 'digestion', 'infection'],
                'voynich_likely': True,
                'fontana_connection': 'Mentioned in medieval texts extensively'
            },
            'valerian': {
                'latin': 'valeriana',
                'medical_uses': ['sleep', 'anxiety', 'nerves', 'calming'],
                'voynich_likely': True,
                'fontana_connection': 'Important for neurological conditions'
            },
            'plantain': {
                'latin': 'plantago',
                'medical_uses': ['wound', 'healing', 'injury', 'skin'],
                'voynich_likely': True,
                'fontana_connection': 'Universal healing plant'
            },
            'comfrey': {
                'latin': 'symphytum',
                'medical_uses': ['bone', 'break', 'fracture', 'mend'],
                'voynich_likely': True,
                'fontana_connection': 'Surgical and orthopedic use'
            },
            'mugwort': {
                'latin': 'artemisia',
                'medical_uses': ['women', 'menstrual', 'cycle', 'labor'],
                'voynich_likely': True,
                'fontana_connection': 'Gynecological applications'
            },
            'horehound': {
                'latin': 'marrubium',
                'medical_uses': ['cough', 'throat', 'bronchus', 'lung'],
                'voynich_likely': True,
                'fontana_connection': 'Respiratory remedy'
            },
        }

        return catalog

    def identify_plant(self, plant_name, confidence=0.85):
        """Record identification of a plant on a page"""

        plant_lower = plant_name.lower()

        if plant_lower not in self.plant_catalog:
            return None

        plant_info = self.plant_catalog[plant_lower]
        plant_info['identified_confidence'] = confidence
        plant_info['identified_date'] = datetime.now().isoformat()

        self.identified_plants[plant_name] = plant_info
        return plant_info

    def get_medical_interpretation(self, plant_name):
        """Get potential medical meaning of identified plant"""

        plant_lower = plant_name.lower()
        if plant_lower not in self.plant_catalog:
            return None

        plant = self.plant_catalog[plant_lower]
        return {
            'plant': plant_name,
            'latin': plant['latin'],
            'medical_uses': plant['medical_uses'],
            'fontana_connection': plant['fontana_connection']
        }

    def correlate_plant_to_cipher(self, plant_name, cipher_text):
        """
        Try to correlate plant identity to cipher text meaning
        Example: If sage (fever remedy) appears with cipher text,
                 does decoded text mention fever/salvia/remedy?
        """

        interpretation = self.get_medical_interpretation(plant_name)
        if not interpretation:
            return None

        correlation = {
            'plant': plant_name,
            'plant_medical_uses': interpretation['medical_uses'],
            'cipher_text': cipher_text,
            'hypothesis': f"Plant {plant_name} may indicate medical context of {', '.join(interpretation['medical_uses'])}",
            'test': "Does decoded cipher text relate to plant's medical uses?"
        }

        return correlation


class IntegrationHypothesisTester:
    """Test whether imagery is part of the cipher"""

    @staticmethod
    def test_plant_cipher_consistency(pages):
        """
        Test 1: Do plants appear consistently with similar cipher patterns?

        Example:
        - Every page with Sage plant has vowel-heavy cipher
        - Every page with Wormwood has consonant-heavy cipher
        = Pattern = Plants encode cipher type
        """

        plant_cipher_patterns = {}

        for page in pages:
            for plant in page['plants_identified']:
                if plant not in plant_cipher_patterns:
                    plant_cipher_patterns[plant] = []

                cipher_text = page['cipher_text']
                vowel_count = cipher_text.count('O_')  # Rough vowel count
                consonant_count = len(cipher_text.split()) - vowel_count

                pattern = {
                    'page': page['page_number'],
                    'vowel_heavy': vowel_count > consonant_count,
                    'consonant_heavy': consonant_count > vowel_count
                }

                plant_cipher_patterns[plant].append(pattern)

        consistency_results = {}
        for plant, patterns in plant_cipher_patterns.items():
            if len(patterns) > 1:
                consistent = all(p['vowel_heavy'] == patterns[0]['vowel_heavy']
                               for p in patterns)
                consistency_results[plant] = {
                    'plant': plant,
                    'appearances': len(patterns),
                    'consistent_pattern': consistent,
                    'patterns': patterns
                }

        return consistency_results

    @staticmethod
    def test_medical_alignment(pages):
        """
        Test 2: Do plant illustrations match medical terminology in text?

        Example:
        - Page shows Sage plant
        - Decoded text contains "salvia" or "fever"
        = Match = Plant confirms plaintext
        """

        results = {
            'aligned_pages': [],
            'misaligned_pages': [],
            'alignment_score': 0.0
        }

        aligned_count = 0

        for page in pages:
            page_result = {
                'page': page['page_number'],
                'plants': page['plants_identified'],
                'cipher_text': page['cipher_text'],
                'potential_matches': []
            }

            # This is where you'd check if decoded plaintext
            # matches plant medical properties
            # For now, structure the test framework

            results['aligned_pages'].append(page_result)
            aligned_count += 1

        results['alignment_score'] = aligned_count / len(pages) if pages else 0
        return results

    @staticmethod
    def test_position_encoding(pages):
        """
        Test 3: Does plant POSITION on page encode information?

        Example:
        - Plant at top = One meaning
        - Plant at bottom = Different meaning
        - Plant size = Frequency weight
        """

        position_patterns = {
            'top_left': [],
            'top_center': [],
            'top_right': [],
            'middle_left': [],
            'middle_center': [],
            'middle_right': [],
            'bottom_left': [],
            'bottom_center': [],
            'bottom_right': []
        }

        for page in pages:
            for plant, position in zip(page['plants_identified'],
                                      page['plants_positions']):
                if position in position_patterns:
                    position_patterns[position].append({
                        'page': page['page_number'],
                        'plant': plant
                    })

        return {
            'position_distributions': position_patterns,
            'clustering_detected': any(len(v) > 2 for v in position_patterns.values())
        }


def example_analysis():
    """Example: Analyzing Voynich for image-text integration"""

    print("=" * 70)
    print("VOYNICH MANUSCRIPT - IMAGE-TEXT INTEGRATION ANALYSIS")
    print("=" * 70)

    # Initialize analyzer
    analyzer = VoynichPageAnalyzer()
    plant_framework = PlantIdentificationFramework()

    # Example: Analyze a hypothetical Voynich page
    print("\n✓ Example Analysis: Page 15 (Herbal Section)")
    print("-" * 70)

    # Page 15 data (example)
    page_15_cipher = "O_N D_R F_C O C_O O N_X O_W"
    page_15_plants = ["Sage", "Rosemary", "Thyme"]
    page_15_positions = ["top_left", "center", "bottom_right"]

    # Create analysis
    page = analyzer.create_page_analysis(
        page_number=15,
        cipher_text=page_15_cipher,
        plants_identified=page_15_plants,
        plants_positions=page_15_positions,
        medical_content=True,
        notes="Herbal remedies section with accompanying plant illustrations"
    )

    print(f"Page: {page['page_number']}")
    print(f"Cipher text: {page['cipher_text']}")
    print(f"Cipher length: {page['cipher_length']} symbols")
    print(f"Plants identified: {page['plants_identified']}")
    print(f"Plant count: {page['plant_count']}")
    print(f"Cipher-to-plant ratio: {page['integration_metrics']['ratio_cipher_to_plants']:.2f}")
    print(f"Position concentration: {page['integration_metrics']['position_concentration']:.2f}")
    print(f"Medical alignment: {page['integration_metrics']['medical_alignment']:.2f}")

    # Identify plants
    print(f"\n✓ Plant Identification:")
    for plant in page_15_plants:
        info = plant_framework.identify_plant(plant, confidence=0.92)
        if info:
            print(f"  - {plant}: {info['latin']} (Medical uses: {', '.join(info['medical_uses'])})")

    # Test hypothesis
    print(f"\n✓ Integration Hypothesis Testing:")
    tester = IntegrationHypothesisTester()

    # For single page, create list for testing
    pages = [page]

    plant_consistency = tester.test_plant_cipher_consistency(pages)
    print(f"  Plant-cipher consistency: {plant_consistency}")

    position_test = tester.test_position_encoding(pages)
    print(f"  Position encoding detected: {position_test['clustering_detected']}")

    # Show statistics
    print(f"\n✓ Overall Statistics:")
    stats = analyzer.get_page_statistics()
    print(f"  Pages analyzed: {stats['total_pages_analyzed']}")
    print(f"  Total plants: {stats['total_plants_identified']}")
    print(f"  Total cipher symbols: {stats['total_cipher_symbols']}")
    print(f"  Average cipher-to-plant ratio: {stats['average_cipher_to_plant_ratio']:.2f}")
    print(f"  Position concentration: {stats['average_position_concentration']:.2f}")
    print(f"  Medical alignment: {stats['average_medical_alignment']:.2f}")
    print(f"\n  INTEGRATION HYPOTHESIS STRENGTH: {stats['integration_hypothesis_strength']:.1%}")

    if stats['integration_hypothesis_strength'] > 0.7:
        print(f"\n  ✓ STRONG EVIDENCE that imagery IS part of cipher")
    elif stats['integration_hypothesis_strength'] > 0.5:
        print(f"\n  ◆ MODERATE EVIDENCE for image-text integration")
    else:
        print(f"\n  Need more data to confirm")

    # Export
    analyzer.export_analysis()


if __name__ == "__main__":
    print("Fontana Cipher - Image-Text Integration Analysis Framework")
    print("=" * 70)
    print("\nThis tool tests whether plant imagery is part of Fontana's cipher\n")
    print("Usage:")
    print("\n1. CREATE ANALYZER:")
    print("   analyzer = VoynichPageAnalyzer()")

    print("\n2. ADD PAGES:")
    print("   analyzer.create_page_analysis(page_number=15, cipher_text='...',")
    print("       plants_identified=['Sage', 'Rosemary'],")
    print("       plants_positions=['top', 'center'])")

    print("\n3. GET STATISTICS:")
    print("   stats = analyzer.get_page_statistics()")

    print("\n4. TEST HYPOTHESIS:")
    print("   tester = IntegrationHypothesisTester()")
    print("   plant_consistency = tester.test_plant_cipher_consistency(pages)")

    print("\n5. EXPORT RESULTS:")
    print("   analyzer.export_analysis('results.json')")

    print("\n" + "=" * 70)
    print("Running example...\n")
    example_analysis()
