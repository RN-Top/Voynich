"""
Fontana Cipher - Persistent Training System
Allows continuous data ingestion and model retraining as new evidence arrives
Designed to incorporate data from: manual extractions, Padua archives, other sources
"""

import json
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib


class FontanaTrainingDatabase:
    """Persistent training database that grows over time"""

    def __init__(self):
        self.db_file = "fontana_training_database.json"
        self.load_or_create_database()

    def load_or_create_database(self):
        """Load existing database or create new one"""
        if Path(self.db_file).exists():
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            print(f"✓ Loaded existing database: {len(self.db['training_examples'])} examples")
        else:
            self.db = {
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0",
                    "description": "Persistent Fontana cipher training database"
                },
                "training_examples": [],
                "data_sources": [],
                "model_versions": []
            }
            self.save_database()
            print(f"✓ Created new training database")

    def save_database(self):
        """Save database to disk"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
        self.db['metadata']['last_updated'] = datetime.now().isoformat()

    def add_training_example(self, plaintext_char, cipher_char, word, page,
                            source="manual_extraction", confidence=0.9, notes=""):
        """Add a single training example"""
        example = {
            "plaintext_char": plaintext_char,
            "cipher_char": cipher_char,
            "word": word,
            "page": page,
            "source": source,
            "confidence": confidence,
            "notes": notes,
            "added_date": datetime.now().isoformat()
        }
        self.db['training_examples'].append(example)
        return example

    def add_data_source(self, source_name, source_type, description, data_count):
        """Register a new data source (for tracking)"""
        source = {
            "name": source_name,
            "type": source_type,  # "manual", "padua_archives", "other"
            "description": description,
            "data_count": data_count,
            "added_date": datetime.now().isoformat()
        }
        self.db['data_sources'].append(source)
        return source

    def import_from_json(self, json_file):
        """Import training examples from JSON file"""
        with open(json_file, 'r', encoding='utf-8') as f:
            examples = json.load(f)

        if isinstance(examples, list):
            for example in examples:
                self.db['training_examples'].append(example)

        self.save_database()
        print(f"✓ Imported {len(examples)} examples from {json_file}")

    def import_from_csv(self, csv_file):
        """Import training examples from CSV file"""
        df = pd.read_csv(csv_file)

        for _, row in df.iterrows():
            example = {
                "plaintext_char": row.get('plaintext_char', row.get('plaintext')),
                "cipher_char": row.get('cipher_char', row.get('cipher')),
                "word": row.get('word', ''),
                "page": row.get('page', 0),
                "source": row.get('source', 'csv_import'),
                "confidence": float(row.get('confidence', 0.9)),
                "notes": row.get('notes', ''),
                "added_date": datetime.now().isoformat()
            }
            self.db['training_examples'].append(example)

        self.save_database()
        print(f"✓ Imported {len(df)} examples from {csv_file}")

    def get_statistics(self):
        """Get database statistics"""
        examples = self.db['training_examples']

        stats = {
            "total_examples": len(examples),
            "unique_characters": len(set(e['plaintext_char'] for e in examples)),
            "data_sources": len(self.db['data_sources']),
            "average_confidence": sum(e['confidence'] for e in examples) / len(examples) if examples else 0,
            "pages_covered": len(set(e['page'] for e in examples)),
            "by_source": {}
        }

        # Count by source
        for example in examples:
            source = example['source']
            if source not in stats['by_source']:
                stats['by_source'][source] = 0
            stats['by_source'][source] += 1

        return stats

    def export_training_data(self):
        """Export as DataFrame for model training"""
        return pd.DataFrame(self.db['training_examples'])

    def log_model_version(self, model_name, accuracy, data_count, notes=""):
        """Log a trained model version"""
        version = {
            "model_name": model_name,
            "trained_date": datetime.now().isoformat(),
            "accuracy": accuracy,
            "training_examples_used": data_count,
            "notes": notes
        }
        self.db['model_versions'].append(version)
        self.save_database()
        return version


class TrainingDataValidator:
    """Validates new training data before adding to database"""

    @staticmethod
    def validate_example(plaintext_char, cipher_char, confidence):
        """Validate a single training example"""
        errors = []

        if not plaintext_char or len(plaintext_char) != 1:
            errors.append("plaintext_char must be a single character")

        if not cipher_char or len(cipher_char) < 1:
            errors.append("cipher_char cannot be empty")

        if not (0.0 <= confidence <= 1.0):
            errors.append("confidence must be between 0.0 and 1.0")

        if confidence < 0.8:
            errors.append("WARNING: Low confidence (<0.8) - consider skipping")

        return {"valid": len(errors) == 0, "errors": errors}

    @staticmethod
    def validate_batch(examples):
        """Validate a batch of examples"""
        results = {
            "total": len(examples),
            "valid": 0,
            "invalid": 0,
            "issues": []
        }

        for i, example in enumerate(examples):
            result = TrainingDataValidator.validate_example(
                example.get('plaintext_char'),
                example.get('cipher_char'),
                example.get('confidence', 0.9)
            )

            if result['valid']:
                results['valid'] += 1
            else:
                results['invalid'] += 1
                results['issues'].append({
                    "index": i,
                    "errors": result['errors']
                })

        return results


class ContinuousRetrainingPipeline:
    """Handles retraining with new data"""

    def __init__(self):
        self.db = FontanaTrainingDatabase()

    def prepare_training_data(self):
        """Prepare all data for model training"""
        df = self.db.export_training_data()

        # Combine with synthetic data if it exists
        try:
            synthetic_df = pd.read_csv('fontana_training_data.csv')
            df = pd.concat([synthetic_df, df], ignore_index=True)
            print(f"✓ Combined synthetic ({len(synthetic_df)}) + real ({len(df) - len(synthetic_df)}) = {len(df)} total")
        except FileNotFoundError:
            print(f"✓ Using {len(df)} real examples (no synthetic data found)")

        return df

    def get_retraining_command(self):
        """Generate the retraining command"""
        stats = self.db.get_statistics()

        print("\n" + "=" * 70)
        print("READY TO RETRAIN WITH NEW DATA")
        print("=" * 70)
        print(f"\nDatabase Status:")
        print(f"  - Total examples: {stats['total_examples']}")
        print(f"  - Unique characters: {stats['unique_characters']}/26")
        print(f"  - Pages covered: {stats['pages_covered']}")
        print(f"  - Average confidence: {stats['average_confidence']:.1%}")
        print(f"  - Data sources: {stats['data_sources']}")

        print(f"\nData by Source:")
        for source, count in stats['by_source'].items():
            print(f"  - {source}: {count} examples")

        print(f"\nTo retrain the model with all data:")
        print(f"  python3 fontana_continuous_retrain.py")

        return stats


def example_workflow():
    """Example of how to use the persistent training system"""

    print("=" * 70)
    print("FONTANA CIPHER - PERSISTENT TRAINING SYSTEM EXAMPLE")
    print("=" * 70)

    # Initialize database
    db = FontanaTrainingDatabase()

    # Example 1: Add manual extractions from Padua archives (future data)
    print("\n✓ Example: Adding data from Padua archives")
    db.add_training_example('m', 'M_3', 'medicina', 15,
                           source='padua_archives',
                           confidence=0.98,
                           notes='High quality scan from Padua University collection')
    db.add_training_example('e', 'O_N', 'medicina', 15,
                           source='padua_archives',
                           confidence=0.98)

    # Example 2: Add from manual manuscript extraction
    print("✓ Example: Adding manual extractions from screenshots")
    db.add_training_example('f', 'F_D', 'febris', 20,
                           source='manual_extraction',
                           confidence=0.92,
                           notes='Clear handwriting, distinctive angular forms')

    # Example 3: Register data source
    db.add_data_source(
        source_name="Padua Archives 2026-10-13",
        source_type="padua_archives",
        description="Biological manuscripts and cipher samples from University of Padua archives",
        data_count=50
    )

    # Save database
    db.save_database()

    # Show statistics
    print("\n" + "=" * 70)
    print("DATABASE STATISTICS")
    print("=" * 70)
    stats = db.get_statistics()
    print(f"Total examples: {stats['total_examples']}")
    print(f"Unique characters: {stats['unique_characters']}/26")
    print(f"Average confidence: {stats['average_confidence']:.1%}")

    # Show what comes next
    pipeline = ContinuousRetrainingPipeline()
    pipeline.get_retraining_command()


if __name__ == "__main__":
    print("Fontana Cipher - Persistent Training System")
    print("=" * 70)
    print("\nUsage:")
    print("\n1. INITIALIZE DATABASE:")
    print("   from fontana_persistent_training_system import FontanaTrainingDatabase")
    print("   db = FontanaTrainingDatabase()")

    print("\n2. ADD NEW DATA:")
    print("   # From Padua archives")
    print("   db.add_training_example('m', 'M_3', 'medicina', 15, source='padua_archives')")
    print("   db.save_database()")

    print("\n3. IMPORT BATCH DATA:")
    print("   db.import_from_json('padua_extracted_data.json')")
    print("   db.import_from_csv('padua_extracted_data.csv')")

    print("\n4. CHECK STATUS:")
    print("   stats = db.get_statistics()")

    print("\n5. RETRAIN:")
    print("   python3 fontana_continuous_retrain.py")

    print("\n" + "=" * 70)
    print("Running example workflow...\n")
    example_workflow()
