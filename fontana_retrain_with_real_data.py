"""
Fontana Cipher - Retrain Model with Real Data
Combines synthetic + real extracted data from manuscripts for better accuracy
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

def combine_training_datasets():
    """Combine synthetic training data with real extracted data"""

    print("=" * 70)
    print("COMBINING SYNTHETIC + REAL TRAINING DATA")
    print("=" * 70)

    # Load synthetic data
    try:
        synthetic_df = pd.read_csv('fontana_training_data.csv')
        print(f"\n✓ Synthetic data: {len(synthetic_df)} examples")
    except FileNotFoundError:
        print("✗ Synthetic data not found. Run fontana_cipher_training_data.py first")
        return None

    # Load real data
    real_data_file = 'fontana_real_training_data.json'
    if Path(real_data_file).exists():
        with open(real_data_file, 'r', encoding='utf-8') as f:
            real_examples = json.load(f)

        real_df = pd.DataFrame(real_examples)
        print(f"✓ Real data: {len(real_df)} examples from {len(real_df['page'].unique())} pages")

        # Combine datasets
        combined_df = pd.concat([synthetic_df, real_df], ignore_index=True)
        print(f"\n✓ Combined dataset: {len(combined_df)} total examples")

        # Save combined
        combined_df.to_csv('fontana_training_data_combined.csv', index=False)
        print(f"✓ Saved to fontana_training_data_combined.csv")

        return combined_df
    else:
        print(f"⚠ No real data found in {real_data_file}")
        print("  Run extraction tool first: python3 fontana_extract_real_data.py")
        return synthetic_df


def retrain_scikit_model():
    """Retrain scikit-learn model with combined data"""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, classification_report
        import joblib

        print("\n" + "=" * 70)
        print("RETRAINING SCIKIT-LEARN MODEL")
        print("=" * 70)

        # Load combined data
        df = combine_training_datasets()
        if df is None:
            return None

        # Prepare features and labels
        X = np.array([[ord(char) for char in df['plaintext_char']]])
        X = X.T

        # Load cipher mapping for reference
        with open('fontana_cipher_mapping.json', 'r') as f:
            cipher_map = json.load(f)

        # Encode cipher labels
        cipher_labels = df['cipher_char'].values
        le = LabelEncoder()
        y = le.fit_transform(cipher_labels)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print(f"\nTraining set: {len(X_train)} examples")
        print(f"Test set: {len(X_test)} examples")
        print(f"Cipher vocabulary: {len(le.classes_)} unique forms")

        # Train model
        print("\nTraining Random Forest (this may take a minute)...")
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\n✓ Model trained!")
        print(f"  Test accuracy: {accuracy:.2%}")

        # Show per-character accuracy
        print(f"\nTop predictions by confidence:")

        # Save model
        joblib.dump(model, 'fontana_cipher_model_retrained.pkl')
        joblib.dump(le, 'fontana_cipher_label_encoder_retrained.pkl')

        print(f"\n✓ Models saved:")
        print(f"  - fontana_cipher_model_retrained.pkl")
        print(f"  - fontana_cipher_label_encoder_retrained.pkl")

        # Compare to original
        try:
            original_model = joblib.load('fontana_cipher_model.pkl')
            original_accuracy = original_model.score(X_test, y_test)
            improvement = (accuracy - original_accuracy) * 100
            print(f"\n📊 IMPROVEMENT FROM RETRAINING:")
            print(f"  Original accuracy: {original_accuracy:.2%}")
            print(f"  New accuracy: {accuracy:.2%}")
            print(f"  Improvement: +{improvement:.2%}")
        except:
            pass

        return model, le

    except ImportError as e:
        print(f"scikit-learn not available: {e}")
        return None, None


def retrain_tensorflow_model():
    """Retrain TensorFlow model with combined data"""
    try:
        import tensorflow as tf
        from tensorflow import keras
        from sklearn.preprocessing import LabelEncoder

        print("\n" + "=" * 70)
        print("RETRAINING TENSORFLOW MODEL")
        print("=" * 70)

        # Load combined data
        df = combine_training_datasets()
        if df is None:
            return None

        # Encode plaintext and ciphertext
        plaintext_encoder = LabelEncoder()
        X_plaintext = plaintext_encoder.fit_transform(df['plaintext_char'].values)

        cipher_encoder = LabelEncoder()
        y_cipher = cipher_encoder.fit_transform(df['cipher_char'].values)

        # Reshape for LSTM
        X = X_plaintext.reshape(-1, 1)

        # Split data
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y_cipher[:split_idx], y_cipher[split_idx:]

        print(f"\nTraining set: {len(X_train)} examples")
        print(f"Test set: {len(X_test)} examples")

        # Build model
        model = keras.Sequential([
            keras.layers.Embedding(len(plaintext_encoder.classes_), 32, input_length=1),
            keras.layers.LSTM(64, return_sequences=True),
            keras.layers.LSTM(32, return_sequences=False),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
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
            epochs=30,
            batch_size=32,
            validation_split=0.1,
            verbose=1
        )

        # Evaluate
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"\n✓ Model trained!")
        print(f"  Test accuracy: {test_accuracy:.2%}")

        # Save model
        model.save('fontana_cipher_model_retrained_tf.h5')
        print(f"\n✓ Model saved: fontana_cipher_model_retrained_tf.h5")

        return model

    except ImportError as e:
        print(f"TensorFlow not available: {e}")
        return None


if __name__ == "__main__":
    print("=" * 70)
    print("FONTANA CIPHER - RETRAIN WITH REAL DATA")
    print("=" * 70)

    # Try scikit-learn first
    model, le = retrain_scikit_model()

    if model is None:
        print("\nTrying TensorFlow...")
        model = retrain_tensorflow_model()

    print("\n" + "=" * 70)
    print("RETRAINING COMPLETE")
    print("=" * 70)

    print("\nNext steps:")
    print("1. Test new model on Voynich: python3 fontana_test_voynich.py")
    print("2. Extract more real data: python3 fontana_extract_real_data.py")
    print("3. Retrain again for even better accuracy")
