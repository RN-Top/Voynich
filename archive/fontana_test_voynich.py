"""
Fontana Cipher System - Voynich Manuscript Testing
Uses trained model to test cipher against Voynich pages
"""

import json
import numpy as np
from pathlib import Path

def load_trained_model():
    """Load the trained cipher model"""
    try:
        import joblib
        model = joblib.load('fontana_cipher_model.pkl')
        le = joblib.load('fontana_cipher_label_encoder.pkl')
        print("✓ Loaded scikit-learn model")
        return model, le
    except (ImportError, FileNotFoundError):
        print("scikit-learn model not found, trying TensorFlow...")
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model('fontana_cipher_model_tf.h5')
            print("✓ Loaded TensorFlow model")
            return model, None
        except:
            print("✗ No trained model found")
            return None, None


def load_cipher_mapping():
    """Load the documented Fontana cipher mapping"""
    with open('fontana_cipher_mapping.json', 'r') as f:
        return json.load(f)


def reverse_cipher_mapping(cipher_map):
    """Create reverse mapping: cipher → plaintext"""
    reverse_map = {}
    for plaintext, cipher in cipher_map['complete_mapping'].items():
        reverse_map[cipher] = plaintext
    return reverse_map


def test_cipher_on_latin_words():
    """Test the cipher by encoding known Latin medical words"""
    print("\n" + "=" * 70)
    print("CIPHER VALIDATION: Encoding Known Latin Words")
    print("=" * 70)

    cipher_map = load_cipher_mapping()

    medical_words = [
        'medicina',
        'febris',
        'curatio',
        'herba',
        'aqua',
        'remedium',
        'dolorem',
    ]

    print("\nEncoding Latin medical terms using Fontana cipher:\n")

    for word in medical_words:
        ciphertext = ""
        for char in word:
            if char in cipher_map['complete_mapping']:
                ciphertext += cipher_map['complete_mapping'][char] + " "

        print(f"  {word:15} → {ciphertext}")


def analyze_voynich_page(page_text, model=None, le=None):
    """
    Analyze a Voynich page and try to decode it

    page_text: Raw text from Voynich page
    model: Trained cipher model (optional)
    le: Label encoder for cipher forms
    """

    cipher_map = load_cipher_mapping()
    reverse_map = reverse_cipher_mapping(cipher_map)

    # Extract cipher symbols from page
    # Look for circle symbols (O) and geometric patterns

    decoded_attempts = []

    # Try simple reverse mapping
    print(f"\nAnalyzing Voynich content...")
    print(f"Page length: {len(page_text)} characters")

    # Count cipher symbol types
    circle_count = page_text.count('O')
    geometric_count = len([c for c in page_text if c in 'LRSDHKMNBCFGJPQTVWXYZ_'])

    if circle_count + geometric_count > 0:
        ratio = circle_count / (circle_count + geometric_count)
        print(f"Circle symbols: {circle_count}")
        print(f"Geometric symbols: {geometric_count}")
        print(f"Ratio: {ratio:.2f}:1")
        print(f"Expected Fontana ratio: 9:1")
        print(f"Match: {'✓ YES' if abs(ratio - 9) < 2 else '✗ NO'}")

    return decoded_attempts


def create_test_case():
    """Create a test case: encode a known word and verify decoding"""
    print("\n" + "=" * 70)
    print("TEST CASE: Encode & Verify Round Trip")
    print("=" * 70)

    cipher_map = load_cipher_mapping()
    reverse_map = reverse_cipher_mapping(cipher_map)

    # Test word
    test_word = "medicina"

    # Encode
    print(f"\nOriginal word: '{test_word}'")

    encoded = ""
    encoding_steps = []
    for char in test_word:
        if char in cipher_map['complete_mapping']:
            cipher_char = cipher_map['complete_mapping'][char]
            encoded += cipher_char + " "
            encoding_steps.append(f"  '{char}' → '{cipher_char}'")

    print(f"\nEncoding process:")
    for step in encoding_steps:
        print(step)

    print(f"\nEncoded text: '{encoded.strip()}'")

    # Decode
    decoded = ""
    decoding_steps = []
    cipher_forms = encoded.split()

    for cipher_form in cipher_forms:
        if cipher_form in reverse_map:
            plaintext_char = reverse_map[cipher_form]
            decoded += plaintext_char
            decoding_steps.append(f"  '{cipher_form}' → '{plaintext_char}'")
        else:
            decoding_steps.append(f"  '{cipher_form}' → '?'")

    print(f"\nDecoding process:")
    for step in decoding_steps:
        print(step)

    print(f"\nDecoded text: '{decoded}'")
    print(f"Match original: {'✓ YES' if decoded == test_word else '✗ NO'}")

    return decoded == test_word


def generate_test_results_report():
    """Generate a summary report"""

    print("\n" + "=" * 70)
    print("CIPHER SYSTEM TEST REPORT")
    print("=" * 70)

    cipher_map = load_cipher_mapping()

    report = {
        "cipher_completeness": {
            "vowels": len([c for c in cipher_map['vowels']]),
            "consonants": len([c for c in cipher_map['consonants']]),
            "total_chars": len(cipher_map['complete_mapping']),
        },
        "cipher_characteristics": {
            "vowel_encoding": "Circles with directional marks (N/S/E/W)",
            "consonant_encoding": "Geometric patterns with logical forms",
            "cipher_ratio": "9:1 (circles:geometric)",
        },
        "validation_status": {
            "round_trip_test": "PENDING",
            "voynich_ratio_test": "PENDING",
            "character_mapping_test": "READY",
        }
    }

    print("\n" + json.dumps(report, indent=2))

    return report


if __name__ == "__main__":
    print("=" * 70)
    print("FONTANA CIPHER - VOYNICH TESTING FRAMEWORK")
    print("=" * 70)

    # Load model (if available)
    model, le = load_trained_model()

    # Load cipher mapping
    cipher_map = load_cipher_mapping()
    print(f"✓ Loaded cipher mapping ({len(cipher_map['complete_mapping'])} characters)")

    # Test 1: Validate cipher on known words
    test_cipher_on_latin_words()

    # Test 2: Round trip test
    success = create_test_case()

    # Test 3: Generate report
    generate_test_results_report()

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("""
1. Extract actual Voynich cipher symbols from manuscript pages
2. Run them through reverse_cipher_mapping to find plaintext
3. Verify Latin words appear in decoded output
4. If 80%+ of decoded text = valid Latin medical terms → STRONG EVIDENCE

When you extract more plaintext↔ciphertext pairs from the PDF:
- Use ManualAnnotationCollector in fontana_cipher_training_data.py
- Retrain model with real examples
- Accuracy will improve significantly
    """)
