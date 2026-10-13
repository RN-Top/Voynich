"""
Fontana Cipher System - Model Training Script
Trains a neural network on cipher transformation patterns
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

def train_sklearn_model():
    """Train using scikit-learn (simpler, no dependencies)"""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, confusion_matrix
        import joblib

        print("=" * 70)
        print("FONTANA CIPHER - SCIKIT-LEARN MODEL TRAINING")
        print("=" * 70)

        # Load training data
        df = pd.read_csv('fontana_training_data.csv')
        print(f"\nLoaded {len(df)} training examples")

        # Prepare features
        # Simple encoding: convert plaintext character to ordinal
        X = np.array([[ord(char) for char in df['plaintext_char']]])
        X = X.T  # Reshape to (n_samples, 1)

        # Load cipher mapping
        with open('fontana_cipher_mapping.json', 'r') as f:
            cipher_map = json.load(f)

        # Prepare labels (cipher characters)
        cipher_labels = []
        for plaintext in df['plaintext_char']:
            if plaintext in cipher_map['complete_mapping']:
                cipher_labels.append(cipher_map['complete_mapping'][plaintext])
            else:
                cipher_labels.append('UNK')

        # Encode cipher labels as integers
        le = LabelEncoder()
        y = le.fit_transform(cipher_labels)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print(f"Training set: {len(X_train)} examples")
        print(f"Test set: {len(X_test)} examples")
        print(f"Cipher vocabulary: {len(le.classes_)} unique cipher forms")

        # Train model
        print("\nTraining Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\n✓ Model trained!")
        print(f"  Accuracy on test set: {accuracy:.2%}")

        # Save model
        joblib.dump(model, 'fontana_cipher_model.pkl')
        joblib.dump(le, 'fontana_cipher_label_encoder.pkl')
        print(f"\n✓ Model saved:")
        print(f"  - fontana_cipher_model.pkl")
        print(f"  - fontana_cipher_label_encoder.pkl")

        return model, le

    except ImportError as e:
        print(f"scikit-learn not available: {e}")
        print("Install with: pip install scikit-learn")
        return None, None


def train_tensorflow_model():
    """Train using TensorFlow/Keras (more powerful)"""
    try:
        import tensorflow as tf
        from tensorflow import keras
        from sklearn.preprocessing import LabelEncoder

        print("=" * 70)
        print("FONTANA CIPHER - TENSORFLOW/KERAS MODEL TRAINING")
        print("=" * 70)

        # Load training data
        df = pd.read_csv('fontana_training_data.csv')
        print(f"\nLoaded {len(df)} training examples")

        # Load cipher mapping
        with open('fontana_cipher_mapping.json', 'r') as f:
            cipher_map = json.load(f)

        # Encode plaintext
        plaintext_encoder = LabelEncoder()
        X_plaintext = plaintext_encoder.fit_transform(df['plaintext_char'].values)

        # Encode ciphertext
        cipher_labels = []
        for plaintext in df['plaintext_char']:
            if plaintext in cipher_map['complete_mapping']:
                cipher_labels.append(cipher_map['complete_mapping'][plaintext])
            else:
                cipher_labels.append('UNK')

        cipher_encoder = LabelEncoder()
        y_cipher = cipher_encoder.fit_transform(cipher_labels)

        # Reshape for LSTM
        X = X_plaintext.reshape(-1, 1)

        print(f"Plaintext vocabulary: {len(plaintext_encoder.classes_)} characters")
        print(f"Cipher vocabulary: {len(cipher_encoder.classes_)} forms")

        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y_cipher[:split_idx], y_cipher[split_idx:]

        # Build model
        model = keras.Sequential([
            keras.layers.Embedding(len(plaintext_encoder.classes_), 16, input_length=1),
            keras.layers.LSTM(32, return_sequences=False),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(len(cipher_encoder.classes_), activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        print("\nModel architecture:")
        model.summary()

        # Train
        print("\nTraining model...")
        history = model.fit(
            X_train, y_train,
            epochs=20,
            batch_size=32,
            validation_split=0.1,
            verbose=1
        )

        # Evaluate
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"\n✓ Model trained!")
        print(f"  Test accuracy: {test_accuracy:.2%}")

        # Save model
        model.save('fontana_cipher_model_tf.h5')
        print(f"\n✓ Model saved: fontana_cipher_model_tf.h5")

        return model

    except ImportError as e:
        print(f"TensorFlow not available: {e}")
        print("Install with: pip install tensorflow")
        return None


def test_model_predictions(model, label_encoder):
    """Test model predictions on known characters"""
    print("\n" + "=" * 70)
    print("MODEL PREDICTIONS TEST")
    print("=" * 70)

    if model is None or label_encoder is None:
        print("Model not available")
        return

    # Load cipher mapping
    with open('fontana_cipher_mapping.json', 'r') as f:
        cipher_map = json.load(f)

    test_chars = ['a', 'e', 'i', 'o', 'u', 'b', 'c', 'd', 't']

    print("\nTesting predictions:\n")
    for char in test_chars:
        char_code = np.array([[ord(char)]])
        prediction = model.predict(char_code, verbose=0)
        predicted_idx = np.argmax(prediction)
        predicted_cipher = label_encoder.inverse_transform([predicted_idx])[0]
        expected_cipher = cipher_map['complete_mapping'].get(char, 'UNKNOWN')

        match = "✓" if predicted_cipher == expected_cipher else "✗"
        print(f"{match} '{char}' → predicted: '{predicted_cipher}' (expected: '{expected_cipher}')")


if __name__ == "__main__":
    # Try scikit-learn first (simpler)
    model, le = train_sklearn_model()

    if model:
        test_model_predictions(model, le)
    else:
        # Fall back to TensorFlow
        print("\nTrying TensorFlow instead...")
        model = train_tensorflow_model()

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print("\nNext: Use trained model to test on Voynich manuscript")
    print("Run: python3 fontana_test_voynich.py")
