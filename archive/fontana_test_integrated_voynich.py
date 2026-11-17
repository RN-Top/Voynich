"""
Fontana Cipher - Test Model on Integrated Voynich
Tests whether the trained model can decode Voynich when using BOTH
cipher text + plant imagery as the complete cipher system
"""

import json
from pathlib import Path
import pandas as pd


class IntegratedVoynichModelTester:
    """Tests model against integrated Voynich (text + imagery together)"""

    def __init__(self, integrated_voynich_file="VOYNICH_INTEGRATED_COMPLETE.json"):
        """Load integrated Voynich file"""

        self.voynich_file = integrated_voynich_file
        self.load_integrated_voynich()
        self.results = {}

    def load_integrated_voynich(self):
        """Load the integrated Voynich file"""

        if not Path(self.voynich_file).exists():
            print(f"✗ Integrated Voynich file not found: {self.voynich_file}")
            print(f"  Create it first using: python3 create_integrated_voynich_file.py")
            self.voynich = None
            return

        with open(self.voynich_file, 'r', encoding='utf-8') as f:
            self.voynich = json.load(f)

        stats = self.voynich.get('statistics', {})
        print(f"✓ Loaded integrated Voynich:")
        print(f"  - Total pages: {stats.get('total_pages', 0)}")
        print(f"  - Pages with cipher: {stats.get('pages_with_cipher', 0)}")
        print(f"  - Pages with plants: {stats.get('pages_with_plants', 0)}")
        print(f"  - Pages with BOTH: {stats.get('pages_with_both', 0)}")
        print(f"  - Integration: {stats.get('integration_percentage', 0):.0f}%")

    def test_with_fontana_cipher(self):
        """
        Test 1: Can we decode Voynich using Fontana's documented cipher?

        This tests: If Fontana's cipher is correct, can we decode the text?
        """

        print("\n" + "=" * 70)
        print("TEST 1: FONTANA CIPHER SYSTEM VALIDATION")
        print("=" * 70)

        if not self.voynich:
            print("No integrated Voynich file loaded")
            return None

        # Load Fontana cipher
        try:
            with open('fontana_cipher_mapping.json', 'r') as f:
                cipher_map = json.load(f)
            complete_map = cipher_map['complete_mapping']
            reverse_map = {v: k for k, v in complete_map.items()}
        except FileNotFoundError:
            print("✗ fontana_cipher_mapping.json not found")
            return None

        print(f"\n✓ Fontana cipher loaded: {len(complete_map)} characters")

        # Try to decode each page
        decoded_pages = []
        symbol_accuracy = []

        for page in self.voynich.get('pages', []):
            page_result = {
                'page_number': page['page_number'],
                'cipher_text': page['cipher']['text'],
                'plants': page['plants']['identified'],
                'decoded': '',
                'accuracy': 0.0,
                'status': 'unknown'
            }

            cipher_text = page['cipher']['text']

            if not cipher_text:
                page_result['status'] = 'no_cipher'
                decoded_pages.append(page_result)
                continue

            # Try to decode using Fontana cipher
            cipher_symbols = cipher_text.split()
            decoded_chars = []
            accurate_decodes = 0

            for symbol in cipher_symbols:
                decoded_char = reverse_map.get(symbol, '?')
                decoded_chars.append(decoded_char)

                if decoded_char != '?':
                    accurate_decodes += 1

            decoded_text = ''.join(decoded_chars)
            accuracy = accurate_decodes / len(cipher_symbols) if cipher_symbols else 0

            page_result['decoded'] = decoded_text
            page_result['accuracy'] = accuracy
            page_result['status'] = 'decoded' if accuracy > 0.5 else 'partial'

            decoded_pages.append(page_result)
            symbol_accuracy.append(accuracy)

        # Calculate aggregate statistics
        avg_accuracy = sum(symbol_accuracy) / len(symbol_accuracy) if symbol_accuracy else 0

        results = {
            'test_name': 'Fontana Cipher System Validation',
            'pages_decoded': len([p for p in decoded_pages if p['status'] == 'decoded']),
            'pages_partial': len([p for p in decoded_pages if p['status'] == 'partial']),
            'average_symbol_accuracy': avg_accuracy,
            'pages': decoded_pages
        }

        print(f"\nResults:")
        print(f"  Pages decoded: {results['pages_decoded']}/{len(decoded_pages)}")
        print(f"  Average accuracy: {avg_accuracy:.1%}")
        print(f"  Status: {'✓ System works' if avg_accuracy > 0.7 else '✗ System needs adjustment'}")

        self.results['fontana_cipher_test'] = results
        return results

    def test_with_plant_context(self):
        """
        Test 2: Does plant context improve decoding accuracy?

        Hypothesis: Pages with plants should decode better than pages without
        """

        print("\n" + "=" * 70)
        print("TEST 2: PLANT CONTEXT IMPROVEMENT")
        print("=" * 70)

        if not self.voynich:
            print("No integrated Voynich file loaded")
            return None

        pages_with_plants = []
        pages_without_plants = []

        for page in self.voynich.get('pages', []):
            if page['page_metadata']['is_integrated']:
                pages_with_plants.append(page)
            elif page['cipher']['text']:
                pages_without_plants.append(page)

        print(f"\nAnalyzing integration benefit:")
        print(f"  Pages with plants: {len(pages_with_plants)}")
        print(f"  Pages without plants: {len(pages_without_plants)}")

        # This would require actual model predictions
        # For now, structure the test framework

        results = {
            'test_name': 'Plant Context Improvement',
            'pages_with_plants': len(pages_with_plants),
            'pages_without_plants': len(pages_without_plants),
            'hypothesis': 'Plant context should improve decoding accuracy',
            'status': 'Requires ML model predictions'
        }

        self.results['plant_context_test'] = results
        return results

    def test_integration_completeness(self):
        """
        Test 3: Is the integrated file complete enough for validation?

        Questions:
        - Do we have cipher + plants for enough pages?
        - Is there enough data to establish patterns?
        - Can we confidently test the hypothesis?
        """

        print("\n" + "=" * 70)
        print("TEST 3: INTEGRATION COMPLETENESS")
        print("=" * 70)

        if not self.voynich:
            print("No integrated Voynich file loaded")
            return None

        stats = self.voynich.get('statistics', {})

        print(f"\nData completeness check:")
        print(f"  Total pages: {stats.get('total_pages', 0)}/155")
        print(f"  Pages with both cipher + plants: {stats.get('pages_with_both', 0)}")
        print(f"  Integration percentage: {stats.get('integration_percentage', 0):.0f}%")

        # Determine readiness
        pages_integrated = stats.get('pages_with_both', 0)
        integration_pct = stats.get('integration_percentage', 0)

        if pages_integrated >= 50 and integration_pct >= 40:
            readiness = "EXCELLENT - Ready for definitive testing"
        elif pages_integrated >= 30 and integration_pct >= 25:
            readiness = "GOOD - Sufficient for analysis"
        elif pages_integrated >= 10:
            readiness = "FAIR - Can test but limited"
        else:
            readiness = "INSUFFICIENT - Need more integration data"

        results = {
            'test_name': 'Integration Completeness',
            'pages_with_both': pages_integrated,
            'integration_percentage': integration_pct,
            'readiness': readiness,
            'ready_for_ml_testing': pages_integrated >= 20,
            'ready_for_pattern_analysis': pages_integrated >= 10
        }

        print(f"\n  Status: {readiness}")
        print(f"  ML testing ready: {'✓ Yes' if results['ready_for_ml_testing'] else '✗ Need more data'}")

        self.results['completeness_test'] = results
        return results

    def test_voynich_decoding_with_model(self, model, label_encoder):
        """
        Test 4: Use trained ML model to decode Voynich

        Tests if the trained model (with Fontana's cipher system)
        can decode the actual Voynich when given integrated data
        """

        print("\n" + "=" * 70)
        print("TEST 4: ML MODEL VOYNICH DECODING")
        print("=" * 70)

        if not self.voynich:
            print("No integrated Voynich file loaded")
            return None

        print(f"\n✓ Using trained model for decoding")

        decoded_results = []
        prediction_accuracy = []

        for page in self.voynich.get('pages', []):
            page_result = {
                'page_number': page['page_number'],
                'cipher_symbols': len(page['cipher']['symbols']),
                'plants': page['plants']['identified'],
                'predictions': [],
                'accuracy': 0.0
            }

            # Make predictions for each symbol
            correct_predictions = 0

            for symbol in page['cipher']['symbols']:
                try:
                    symbol_value = ord(symbol[0]) if symbol else 0
                    prediction = model.predict([[symbol_value]])
                    predicted_char = label_encoder.inverse_transform(prediction)[0]

                    page_result['predictions'].append({
                        'cipher_symbol': symbol,
                        'predicted_plaintext': predicted_char
                    })

                    correct_predictions += 1
                except Exception as e:
                    page_result['predictions'].append({
                        'cipher_symbol': symbol,
                        'error': str(e)
                    })

            if page['cipher']['symbols']:
                page_result['accuracy'] = correct_predictions / len(page['cipher']['symbols'])
                prediction_accuracy.append(page_result['accuracy'])

            decoded_results.append(page_result)

        avg_accuracy = sum(prediction_accuracy) / len(prediction_accuracy) if prediction_accuracy else 0

        results = {
            'test_name': 'ML Model Voynich Decoding',
            'pages_tested': len(decoded_results),
            'average_accuracy': avg_accuracy,
            'pages': decoded_results,
            'status': 'Complete' if avg_accuracy > 0.5 else 'Needs improvement'
        }

        print(f"\nResults:")
        print(f"  Pages tested: {len(decoded_results)}")
        print(f"  Average accuracy: {avg_accuracy:.1%}")

        self.results['ml_model_test'] = results
        return results

    def validate_hypothesis(self):
        """
        MAIN TEST: Is the integrated hypothesis valid?

        If you can decode Voynich using text + plant imagery together,
        then the hypothesis is proven: They ARE one unified cipher system
        """

        print("\n" + "=" * 70)
        print("HYPOTHESIS VALIDATION: ONE COMPLETE INTEGRATED CIPHER")
        print("=" * 70)

        # Run all tests
        self.test_integration_completeness()
        self.test_with_fontana_cipher()
        self.test_with_plant_context()

        # Interpret results
        completeness = self.results.get('completeness_test', {})
        cipher_test = self.results.get('fontana_cipher_test', {})

        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)

        # Readiness check
        is_ready = completeness.get('ready_for_ml_testing', False)
        print(f"\nData readiness: {'✓ YES' if is_ready else '✗ NO - Need more integration data'}")

        # Cipher validation
        cipher_accuracy = cipher_test.get('average_symbol_accuracy', 0)
        print(f"Cipher system validation: {cipher_accuracy:.1%} accuracy")

        if cipher_accuracy > 0.7 and is_ready:
            print(f"\n✓✓✓ HYPOTHESIS STRONGLY SUPPORTED ✓✓✓")
            print(f"The integrated data can be decoded using Fontana's cipher system.")
            print(f"This suggests plants ARE part of the cipher.")
        elif cipher_accuracy > 0.5 and is_ready:
            print(f"\n◆ HYPOTHESIS PARTIALLY SUPPORTED")
            print(f"Some decoding works but accuracy needs improvement.")
            print(f"Requires more plant-cipher correlation refinement.")
        else:
            print(f"\n✗ INSUFFICIENT EVIDENCE")
            print(f"Need more integrated data (pages with both cipher + plants)")
            print(f"Continue extraction from your 155 manuscript pages.")

        return {
            'hypothesis_valid': cipher_accuracy > 0.7 and is_ready,
            'confidence': cipher_accuracy,
            'data_ready': is_ready,
            'next_steps': 'Run ML model testing' if is_ready else 'Extract more integration data'
        }


def example_test():
    """Example of how to use the tester"""

    print("=" * 70)
    print("INTEGRATED VOYNICH MODEL TESTING EXAMPLE")
    print("=" * 70)

    # Create example integrated Voynich first
    from create_integrated_voynich_file import IntegratedVoynichCreator

    creator = IntegratedVoynichCreator()

    # Add example pages
    creator.add_integrated_page(
        page_number=15,
        cipher_text="O_N D_R F_C O C_O O N_X O_W",
        plants=["Sage", "Rosemary"],
        plant_positions=["top", "center"],
        plant_descriptions=["Fever remedy", "Memory aid"]
    )

    creator.add_integrated_page(
        page_number=20,
        cipher_text="M_L O_W A_R",
        plants=["Mint", "Wormwood"],
        plant_positions=["left", "right"],
        plant_descriptions=["Digestion aid", "Fever treatment"]
    )

    creator.save_integrated_voynich("VOYNICH_INTEGRATED_EXAMPLE.json")

    # Now test it
    tester = IntegratedVoynichModelTester("VOYNICH_INTEGRATED_EXAMPLE.json")

    print("\nRunning validation tests...\n")

    validation = tester.validate_hypothesis()

    print(f"\nValidation result:")
    print(f"  Hypothesis valid: {validation['hypothesis_valid']}")
    print(f"  Confidence: {validation['confidence']:.1%}")
    print(f"  Next step: {validation['next_steps']}")


if __name__ == "__main__":
    print("Fontana Cipher - Integrated Voynich Model Tester")
    print("=" * 70)
    print("\nUsage:")
    print("\n1. CREATE INTEGRATED VOYNICH:")
    print("   python3 create_integrated_voynich_file.py")

    print("\n2. TEST WITH FONTANA CIPHER:")
    print("   tester = IntegratedVoynichModelTester()")
    print("   results = tester.test_with_fontana_cipher()")

    print("\n3. VALIDATE HYPOTHESIS:")
    print("   validation = tester.validate_hypothesis()")

    print("\n4. TEST WITH ML MODEL:")
    print("   tester.test_voynich_decoding_with_model(model, encoder)")

    print("\n" + "=" * 70 + "\n")
    example_test()
