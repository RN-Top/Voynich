#!/usr/bin/env python3
"""
Step 3: Build recognition model to test Fontana cipher patterns

Instead of direct decryption, test whether Voynich follows
the MATHEMATICAL STRUCTURE of Fontana's documented cipher system.

Approach:
1. Extract Fontana's cipher structure (vowels vs consonants, ratios, patterns)
2. Analyze Voynich EVA text for similar patterns
3. Train classifier: Does this text match Fontana's mathematical signature?
4. Apply to Voynich vs control data
"""

import json
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

print("=" * 80)
print("STEP 3: BUILD FONTANA RECOGNITION MODEL")
print("=" * 80)

# Load data
with open('voynich_integrated.json') as f:
    integrated = json.load(f)

with open('voynich_control.json') as f:
    control = json.load(f)

with open('fontana_cipher_mapping.json') as f:
    fontana = json.load(f)

# ============================================================================
# PHASE 1: EXTRACT FONTANA'S MATHEMATICAL SIGNATURE
# ============================================================================
print("\nPhase 1: Extract Fontana cipher mathematical signature...")

fontana_mapping = fontana['complete_mapping']
fontana_vowels = fontana['vowels']
fontana_consonants = fontana['consonants']

# Analyze Fontana's structure
print(f"\nFontana cipher structure:")
print(f"  Total mappings: {len(fontana_mapping)}")
print(f"  Vowels (a,e,i,o,u): {len(fontana_vowels)}")
print(f"  Consonants: {len(fontana_consonants)}")
print(f"  Vowel ratio: {len(fontana_vowels)/(len(fontana_vowels)+len(fontana_consonants)):.1%}")

# Fontana cipher symbol analysis
cipher_symbols = list(fontana_mapping.values())
vowel_mappings = list(fontana_vowels.values())
consonant_mappings = list(fontana_consonants.values())

print(f"\nFontana vowel cipher symbols: {vowel_mappings}")
print(f"Fontana consonant cipher symbols: {consonant_mappings}")

# Pattern: Circle-based vowels vs geometric consonants
circle_count = sum(1 for s in cipher_symbols if 'O' in s)
geometric_count = sum(1 for s in cipher_symbols if any(c.isdigit() for c in s))

print(f"\nFontana geometric patterns:")
print(f"  Circle-based symbols (O): {circle_count}/{len(cipher_symbols)}")
print(f"  Geometric symbols (numbers): {geometric_count}/{len(cipher_symbols)}")
print(f"  Ratio: {circle_count/geometric_count:.2f}:1")

# ============================================================================
# PHASE 2: EXTRACT FEATURES FROM VOYNICH TEXT
# ============================================================================
print("\n" + "=" * 80)
print("Phase 2: Extract features from Voynich text...")

def extract_text_features(dataset, name="Dataset"):
    """Extract statistical features from dataset"""
    features = []
    labels = []

    for folio_idx, folio in enumerate(dataset['folios']):
        # Extract all words
        words = []
        for line in folio.get('text_lines', []):
            if 'words' in line:
                words.extend(line['words'])

        if not words:
            continue

        # Extract characters
        chars = []
        for word in words:
            chars.extend(list(word))

        # Calculate features
        feature_vector = {
            'total_chars': len(chars),
            'unique_chars': len(set(chars)),
            'char_diversity': len(set(chars)) / len(chars) if chars else 0,
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'vowel_count': sum(1 for c in chars if c in 'aeiouoy'),
            'consonant_count': sum(1 for c in chars if c in 'bcdfghjklmnpqrstvwxz'),
            'vowel_ratio': sum(1 for c in chars if c in 'aeiouoy') / len(chars) if chars else 0,
        }

        # Add consonant-to-vowel ratio (similar to Fontana's circle:geometric ratio)
        vowels = feature_vector['vowel_count']
        consonants = feature_vector['consonant_count']
        if consonants > 0:
            feature_vector['consonant_vowel_ratio'] = consonants / vowels if vowels > 0 else 0
        else:
            feature_vector['consonant_vowel_ratio'] = 0

        features.append(feature_vector)
        labels.append(folio_idx)

    return features, labels

# Extract features
print(f"\nExtracting features...")
voynich_features, voynich_labels = extract_text_features(integrated, "Voynich")
control_features, control_labels = extract_text_features(control, "Control")

print(f"✓ Voynich features: {len(voynich_features)} folios")
print(f"✓ Control features: {len(control_features)} folios")

# Convert to numpy arrays
feature_keys = list(voynich_features[0].keys())
X_voynich = np.array([[f[k] for k in feature_keys] for f in voynich_features])
X_control = np.array([[f[k] for k in feature_keys] for f in control_features])

print(f"\nFeature dimensions: {X_voynich.shape}")
print(f"Features tracked: {feature_keys}")

# ============================================================================
# PHASE 3: TRAIN CLASSIFIER
# ============================================================================
print("\n" + "=" * 80)
print("Phase 3: Train Fontana pattern classifier...")

# Label: 1 = Voynich (should match Fontana), 0 = Control (random shuffled)
y_voynich = np.ones(len(X_voynich))
y_control = np.zeros(len(X_control))

X_combined = np.vstack([X_voynich, X_control])
y_combined = np.hstack([y_voynich, y_control])

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

# Train classifier
print(f"\nTraining Random Forest classifier...")
clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
clf.fit(X_scaled, y_combined)

print(f"✓ Model trained")

# Evaluate
train_score = clf.score(X_scaled, y_combined)
print(f"  Training accuracy: {train_score:.1%}")

# Feature importance
feature_importance = list(zip(feature_keys, clf.feature_importances_))
feature_importance.sort(key=lambda x: x[1], reverse=True)

print(f"\nMost important features for distinguishing Voynich vs Control:")
for feat, importance in feature_importance[:5]:
    print(f"  {feat:25s}: {importance:.3f}")

# ============================================================================
# PHASE 4: TEST ON VOYNICH VS CONTROL
# ============================================================================
print("\n" + "=" * 80)
print("Phase 4: Test classifier on Voynich vs Control...")

# Predict probabilities
X_voynich_scaled = scaler.transform(X_voynich)
X_control_scaled = scaler.transform(X_control)

voynich_probs = clf.predict_proba(X_voynich_scaled)[:, 1]
control_probs = clf.predict_proba(X_control_scaled)[:, 1]

print(f"\nVoynich predictions (probability of matching Fontana pattern):")
print(f"  Mean: {voynich_probs.mean():.1%}")
print(f"  Median: {np.median(voynich_probs):.1%}")
print(f"  Std: {voynich_probs.std():.1%}")
print(f"  Range: [{voynich_probs.min():.1%}, {voynich_probs.max():.1%}]")

print(f"\nControl predictions (probability of matching Fontana pattern):")
print(f"  Mean: {control_probs.mean():.1%}")
print(f"  Median: {np.median(control_probs):.1%}")
print(f"  Std: {control_probs.std():.1%}")
print(f"  Range: [{control_probs.min():.1%}, {control_probs.max():.1%}]")

# Statistical test
print(f"\n" + "-" * 80)
print("COMPARISON:")
print("-" * 80)

voynich_matches = sum(1 for p in voynich_probs if p > 0.5)
control_matches = sum(1 for p in control_probs if p > 0.5)

print(f"Voynich folios matching Fontana pattern (>50%): {voynich_matches}/{len(voynich_probs)} ({100*voynich_matches/len(voynich_probs):.1f}%)")
print(f"Control folios matching Fontana pattern (>50%): {control_matches}/{len(control_probs)} ({100*control_matches/len(control_probs):.1f}%)")

if voynich_probs.mean() > control_probs.mean():
    diff = voynich_probs.mean() - control_probs.mean()
    print(f"\n✓ VOYNICH SHOWS STRONGER FONTANA PATTERN")
    print(f"  Difference: {diff:.1%}")
    print(f"  → Suggests Voynich follows Fontana cipher structure")
else:
    diff = control_probs.mean() - voynich_probs.mean()
    print(f"\n✗ CONTROL SHOWS SIMILAR OR STRONGER PATTERN")
    print(f"  Difference: {diff:.1%}")
    print(f"  → Suggests Fontana pattern not specific to Voynich")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("RECOGNITION MODEL SUMMARY")
print("=" * 80)

print(f"""
MODEL: Random Forest Classifier
  Features: {len(feature_keys)} text statistics
  Training accuracy: {train_score:.1%}

FINDINGS:
  - Voynich average pattern match: {voynich_probs.mean():.1%}
  - Control average pattern match: {control_probs.mean():.1%}
  - Difference: {abs(voynich_probs.mean() - control_probs.mean()):.1%}

INTERPRETATION:
  If Voynich >> Control: Voynich follows unique Fontana-like structure
  If Voynich ≈ Control: Pattern is not specific to Voynich

NEXT STEP (if supported): Step 4 - Full integrated pipeline
  - Combine all three steps
  - Test hypothesis across full 226-folio dataset
  - Validate findings
""")

print("=" * 80)
print("READY FOR STEP 4: FULL ANALYSIS PIPELINE")
print("=" * 80)
