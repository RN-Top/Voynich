"""
Fontana Cipher - Continuous Retraining Script
Retrains the model using all data from the persistent training database
Can be run anytime new data is added (from Padua, manual extractions, etc.)
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from fontana_persistent_training_system import FontanaTrainingDatabase, TrainingDataValidator


def continuous_retrain():
    """Main retraining function"""

    print("=" * 70)
    print("FONTANA CIPHER - CONTINUOUS RETRAINING")
    print("=" * 70)

    # Load persistent database
    db = FontanaTrainingDatabase()

    # Get statistics
    stats = db.get_statistics()
    print(f"\n✓ Database loaded:")
    print(f"  - Total examples: {stats['total_examples']}")
    print(f"  - Unique characters: {stats['unique_characters']}/26")
    print(f"  - Average confidence: {stats['average_confidence']:.1%}")
    print(f"  - Pages covered: {stats['pages_covered']}")
    print(f"  - Data sources: {stats['data_sources']}")

    print(f"\nData by source:")
    for source, count in stats['by_source'].items():
        print(f"  - {source}: {count} examples")

    # Validate data quality
    print(f"\n" + "-" * 70)
    print("VALIDATING DATA QUALITY")
    print("-" * 70)

    examples = db.db['training_examples']
    validator = TrainingDataValidator()
    validation = validator.validate_batch(examples)

    print(f"✓ Validation results:")
    print(f"  - Total: {validation['total']}")
    print(f"  - Valid: {validation['valid']} ({100*validation['valid']/validation['total']:.0f}%)")
    print(f"  - Invalid: {validation['invalid']}")

    if validation['invalid'] > 0:
        print(f"\n⚠ Found {validation['invalid']} invalid examples")
        for issue in validation['issues'][:5]:  # Show first 5
            print(f"  - Index {issue['index']}: {issue['errors']}")

    # Prepare training data
    print(f"\n" + "-" * 70)
    print("PREPARING TRAINING DATA")
    print("-" * 70)

    # Get all examples as DataFrame
    real_examples = db.export_training_data()

    # Load synthetic data if available
    synthetic_df = None
    if Path('fontana_training_data.csv').exists():
        synthetic_df = pd.read_csv('fontana_training_data.csv')
        combined_df = pd.concat([synthetic_df, real_examples], ignore_index=True)
        print(f"✓ Combined data:")
        print(f"  - Synthetic: {len(synthetic_df)} examples")
        print(f"  - Real: {len(real_examples)} examples")
        print(f"  - Total: {len(combined_df)} examples")
    else:
        combined_df = real_examples
        print(f"✓ Using real data only:")
        print(f"  - Total: {len(combined_df)} examples")

    # Try to train model
    print(f"\n" + "-" * 70)
    print("ATTEMPTING MODEL TRAINING")
    print("-" * 70)

    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        import joblib

        print("✓ scikit-learn available")

        # Prepare features and labels
        X = combined_df['plaintext_char'].values
        y = combined_df['cipher_char'].values

        # Encode
        X_encoded = []
        for char in X:
            X_encoded.append(ord(char))
        X_encoded = [[val] for val in X_encoded]

        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_encoded, test_size=0.2, random_state=42
        )

        print(f"\n✓ Data prepared:")
        print(f"  - Training set: {len(X_train)} examples")
        print(f"  - Test set: {len(X_test)} examples")
        print(f"  - Cipher vocabulary: {len(le.classes_)} unique forms")

        # Train model
        print(f"\n✓ Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=150,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\n✓ Model trained!")
        print(f"  - Accuracy: {accuracy:.2%}")

        # Save model
        joblib.dump(model, 'fontana_cipher_model_continuous.pkl')
        joblib.dump(le, 'fontana_cipher_label_encoder_continuous.pkl')
        print(f"  - Model saved: fontana_cipher_model_continuous.pkl")

        # Log model version
        db.log_model_version(
            model_name="continuous_random_forest",
            accuracy=accuracy,
            data_count=len(combined_df),
            notes=f"Real: {len(real_examples)}, Synthetic: {len(synthetic_df) if synthetic_df is not None else 0}"
        )
        db.save_database()

        print(f"\n✓ Model version logged")

    except ImportError:
        print("⚠ scikit-learn not available")
        print("   To train locally, install: pip install scikit-learn pandas numpy")
        print("   For now, using cipher system as-is (no ML model)")

    # Summary
    print(f"\n" + "=" * 70)
    print("RETRAINING COMPLETE")
    print("=" * 70)
    print(f"\nNext steps:")
    print(f"  1. Test model on Voynich: python3 fontana_test_voynich.py")
    print(f"  2. Add more data when Padua archives respond")
    print(f"  3. Retrain anytime: python3 fontana_continuous_retrain.py")


def add_new_data_example():
    """Example of adding new data from Padua archives"""

    db = FontanaTrainingDatabase()

    print("=" * 70)
    print("EXAMPLE: Adding data from Padua Archives")
    print("=" * 70)

    # Example: When Padua archives respond with verified cipher examples
    padua_data = [
        {
            "plaintext_char": "m",
            "cipher_char": "M_3",
            "word": "medicina",
            "page": "padua_ms_15",
            "source": "padua_archives",
            "confidence": 0.99,
            "notes": "Verified from Padua University archival collection"
        },
        {
            "plaintext_char": "e",
            "cipher_char": "O_N",
            "word": "medicina",
            "page": "padua_ms_15",
            "source": "padua_archives",
            "confidence": 0.99,
            "notes": "Circle with clear north mark"
        }
    ]

    print(f"\nAdding {len(padua_data)} examples from Padua Archives...")

    for example in padua_data:
        db.add_training_example(
            example['plaintext_char'],
            example['cipher_char'],
            example['word'],
            example['page'],
            source=example['source'],
            confidence=example['confidence'],
            notes=example['notes']
        )

    # Register source
    db.add_data_source(
        source_name="Padua Archives - October 2026",
        source_type="padua_archives",
        description="Verified cipher examples from University of Padua biographical archives",
        data_count=len(padua_data)
    )

    db.save_database()

    print(f"✓ Added {len(padua_data)} examples from Padua Archives")
    print(f"✓ Total in database: {len(db.db['training_examples'])} examples")


if __name__ == "__main__":
    print("Fontana Cipher - Continuous Retraining System")
    print("\nUsage:")
    print("  python3 fontana_continuous_retrain.py")
    print("\nThis script:")
    print("  1. Loads the persistent training database")
    print("  2. Validates all data quality")
    print("  3. Combines real + synthetic data")
    print("  4. Trains a new model with all available data")
    print("  5. Logs model version and performance")
    print("\n" + "=" * 70 + "\n")

    continuous_retrain()
