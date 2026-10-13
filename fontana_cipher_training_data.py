"""
Fontana Cipher System - Training Data Generator & ML Framework
Generates synthetic training data from documented cipher rules
Can be augmented with manual annotations from PDF extraction
"""

import json
import csv
from pathlib import Path
import numpy as np

# ============================================================================
# PART 1: DOCUMENTED CIPHER RULES (From Fontana PDF analysis)
# ============================================================================

VOWEL_CIPHER = {
    'a': 'O_W',      # Circle + West mark
    'e': 'O_N',      # Circle + North mark
    'i': 'O',        # Plain circle
    'o': 'O_S',      # Circle + South mark
    'u': 'O_E',      # Circle + East mark
}

CONSONANT_CIPHER = {
    'b': 'B_L',      # Loop-Stem mirrored left
    'c': 'C_O',      # Open curve, left-facing
    'd': 'D_R',      # Loop-Stem mirrored right
    'f': 'F_D',      # Hook form pointing down
    'g': 'G_C',      # Curved form with cross
    'h': 'H_1',      # Stem with 1 notch
    'j': 'J_H',      # Hook-curl form
    'k': 'K_2',      # Stem with 2 notches
    'l': 'L_A',      # Long stem with right angle
    'm': 'M_3',      # Stem with 3 notches
    'n': 'N_X',      # Stem with diagonal cross
    'p': 'P_T',      # Top loop form
    'q': 'Q_B',      # Bottom loop form
    'r': 'R_A',      # Angled form with curve
    's': 'S_2',      # Double curve S-shape
    't': 'T_H',      # Horizontal cross with stem
    'v': 'V_A',      # Angle-V form
    'w': 'W_2',      # Double angle-W form
    'x': 'X_C',      # Cross-X form
    'y': 'Y_J',      # Y-junction form
    'z': 'Z_Z',      # Zigzag-Z form
}

CIPHER_MAP = {**VOWEL_CIPHER, **CONSONANT_CIPHER}

# ============================================================================
# PART 2: SYNTHETIC TRAINING DATA GENERATOR
# ============================================================================

class FontanaCipherTrainer:
    def __init__(self):
        self.training_data = []
        self.validation_data = []
        self.test_data = []

    def plaintext_to_cipher(self, plaintext):
        """Convert plaintext to cipher using documented rules"""
        ciphertext = ""
        for char in plaintext.lower():
            if char in CIPHER_MAP:
                ciphertext += CIPHER_MAP[char]
            elif char == ' ':
                ciphertext += '|'  # Space separator
            else:
                ciphertext += char  # Keep unknown chars
        return ciphertext

    def generate_synthetic_data(self, num_samples=1000):
        """Generate synthetic training data from documented cipher rules"""
        # Common Latin words from medieval medical texts
        medical_terms = [
            'medicina', 'curatio', 'febris', 'dolorem', 'remedium',
            'herba', 'aqua', 'vinum', 'oleum', 'sal', 'mel', 'cera',
            'infirmitas', 'aegrotus', 'sanitas', 'corpus', 'morbus',
            'causa', 'signum', 'symptoma', 'therapeutica', 'emplastrum'
        ]

        # Generate character-level training examples
        print(f"Generating {num_samples} synthetic training examples...")

        for i in range(num_samples):
            # Choose random word
            word = medical_terms[i % len(medical_terms)]

            # Character-level examples (most useful for learning)
            for j, char in enumerate(word):
                if char in CIPHER_MAP:
                    plaintext_char = char
                    cipher_char = CIPHER_MAP[char]

                    # Create context window
                    context_before = word[max(0, j-2):j]
                    context_after = word[j+1:min(len(word), j+3)]

                    example = {
                        'plaintext_char': plaintext_char,
                        'cipher_char': cipher_char,
                        'context_before': context_before,
                        'context_after': context_after,
                        'word': word,
                        'position_in_word': j,
                        'is_vowel': plaintext_char in VOWEL_CIPHER,
                        'char_type': 'vowel' if plaintext_char in VOWEL_CIPHER else 'consonant',
                    }

                    self.training_data.append(example)

        print(f"Generated {len(self.training_data)} character-level examples")
        return self.training_data

    def create_cipher_mapping_table(self):
        """Create lookup table of character mappings"""
        mapping_table = []
        for plaintext, cipher in CIPHER_MAP.items():
            mapping_table.append({
                'plaintext': plaintext,
                'cipher': cipher,
                'type': 'vowel' if plaintext in VOWEL_CIPHER else 'consonant',
                'cipher_type': 'circle' if plaintext in VOWEL_CIPHER else 'geometric'
            })
        return mapping_table

    def save_training_data_csv(self, filename='fontana_training_data.csv'):
        """Save training data as CSV for ML frameworks"""
        if not self.training_data:
            self.generate_synthetic_data()

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'plaintext_char', 'cipher_char', 'context_before', 'context_after',
                'word', 'position_in_word', 'is_vowel', 'char_type'
            ])
            writer.writeheader()
            writer.writerows(self.training_data)

        print(f"Training data saved to {filename}")

    def save_cipher_mapping_json(self, filename='fontana_cipher_mapping.json'):
        """Save cipher mapping as JSON"""
        mapping = {
            'vowels': VOWEL_CIPHER,
            'consonants': CONSONANT_CIPHER,
            'complete_mapping': CIPHER_MAP,
            'cipher_ratio': {
                'vowels_percent': 100 * len([c for c in CIPHER_MAP if c in VOWEL_CIPHER]) / len(CIPHER_MAP),
                'consonants_percent': 100 * len([c for c in CIPHER_MAP if c in CONSONANT_CIPHER]) / len(CIPHER_MAP),
            }
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

        print(f"Cipher mapping saved to {filename}")


# ============================================================================
# PART 3: NEURAL NETWORK MODEL (TensorFlow/Keras)
# ============================================================================

def create_cipher_model(vocab_size=26, embedding_dim=8, lstm_units=32):
    """
    Create a neural network to learn cipher transformations
    Input: plaintext character (+ context)
    Output: cipher character
    """
    try:
        import tensorflow as tf
        from tensorflow import keras

        model = keras.Sequential([
            keras.layers.Embedding(vocab_size, embedding_dim, input_length=1),
            keras.layers.LSTM(lstm_units, return_sequences=False),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(vocab_size * 10, activation='relu'),  # Output cipher space
            keras.layers.Dense(vocab_size, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        print("Neural network model created (TensorFlow/Keras)")
        return model

    except ImportError:
        print("TensorFlow not available. Using scikit-learn instead...")
        return None


def create_sklearn_model():
    """Create scikit-learn model as fallback"""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        print("Scikit-learn RandomForest model created")
        return model
    except ImportError:
        return None


# ============================================================================
# PART 4: MANUAL ANNOTATION INTERFACE
# ============================================================================

class ManualAnnotationCollector:
    """
    Framework for manually annotating plaintext↔cipher pairs from PDF
    Use this to add real examples as we extract pages
    """

    def __init__(self, filename='fontana_manual_annotations.json'):
        self.filename = filename
        self.annotations = self._load_existing()

    def _load_existing(self):
        """Load previously saved annotations"""
        if Path(self.filename).exists():
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def add_annotation(self, plaintext, ciphertext, page_num, notes=""):
        """Add a manually extracted plaintext↔ciphertext example"""
        annotation = {
            'plaintext': plaintext,
            'ciphertext': ciphertext,
            'page': page_num,
            'notes': notes,
            'source': 'manual_pdf_extraction'
        }
        self.annotations.append(annotation)
        self.save()
        print(f"Added annotation: {plaintext} → {ciphertext}")

    def save(self):
        """Save annotations to file"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.annotations, f, ensure_ascii=False, indent=2)

    def get_all_annotations(self):
        """Get all annotations for training"""
        return self.annotations


# ============================================================================
# PART 5: MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FONTANA CIPHER SYSTEM - TRAINING DATA GENERATION")
    print("=" * 70)

    # Initialize trainer
    trainer = FontanaCipherTrainer()

    # Generate synthetic training data
    trainer.generate_synthetic_data(num_samples=1000)

    # Save training data
    trainer.save_training_data_csv('fontana_training_data.csv')
    trainer.save_cipher_mapping_json('fontana_cipher_mapping.json')

    # Create cipher mapping table
    mapping_table = trainer.create_cipher_mapping_table()
    print(f"\nCipher Mapping Table ({len(mapping_table)} characters):")
    for entry in mapping_table[:10]:
        print(f"  {entry['plaintext']} ({entry['type']}) → {entry['cipher']}")
    print(f"  ... and {len(mapping_table) - 10} more")

    # Show sample training data
    print(f"\nSample Training Examples (first 10):")
    for example in trainer.training_data[:10]:
        print(f"  '{example['plaintext_char']}' ({example['char_type']}) → '{example['cipher_char']}' in word '{example['word']}'")

    # Initialize annotation collector
    print(f"\n✓ Manual annotation framework ready")
    print(f"  Use ManualAnnotationCollector to add real PDF extractions")

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("1. Run this script: python3 fontana_cipher_training_data.py")
    print("2. Train model: python3 fontana_train_model.py")
    print("3. Test on Voynich: python3 fontana_test_voynich.py")
    print("=" * 70)
