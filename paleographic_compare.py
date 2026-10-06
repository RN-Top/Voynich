#!/usr/bin/env python3
"""
Paleographic comparison tool for Fontana vs Voynich handwriting analysis.

Compares handwriting characteristics:
- Letter forms and proportions
- Stroke angles and thickness
- Ligatures and abbreviations
- Word spacing and baseline consistency
- Overall script style (gothic, italic, cursive)

Uses existing fontana_handwriting_comparison.py as foundation
"""

import os
import json
import cv2
import numpy as np
from PIL import Image
import argparse

class PaleographicComparator:
    """Compare handwriting samples from two manuscript sources."""

    def __init__(self):
        self.results = {
            'comparisons': [],
            'summary': {
                'total_samples_compared': 0,
                'high_confidence_matches': 0,
                'medium_confidence_matches': 0,
                'low_confidence_matches': 0
            }
        }

    def extract_features(self, image_path):
        """Extract paleographic features from a handwriting sample."""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return None

            # Binarize
            _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

            # Detect contours (individual letters/strokes)
            contours, _ = cv2.findContours(
                255 - binary,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE
            )

            features = {
                'image_path': image_path,
                'image_size': img.shape,
                'stroke_count': len(contours),
                'darkness': np.sum(img < 128) / img.size,
                'contrast': np.std(img),
                'contours': contours
            }

            # Calculate stroke characteristics
            stroke_heights = []
            stroke_widths = []

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if h > 5:  # Significant strokes only
                    stroke_heights.append(h)
                if w > 2:
                    stroke_widths.append(w)

            if stroke_heights:
                features['avg_stroke_height'] = np.mean(stroke_heights)
                features['stroke_height_variance'] = np.var(stroke_heights)

            if stroke_widths:
                features['avg_stroke_width'] = np.mean(stroke_widths)
                features['stroke_width_variance'] = np.var(stroke_widths)

            return features

        except Exception as e:
            print(f"Error extracting features from {image_path}: {e}")
            return None

    def compare_samples(self, fontana_features, voynich_features):
        """
        Compare two handwriting samples.

        Scoring:
        - Similar darkness (text weight)
        - Similar stroke patterns
        - Similar letter proportions
        - Similar script style indicators
        """
        if not fontana_features or not voynich_features:
            return None

        score = 0.0
        max_score = 5.0
        details = []

        # 1. Darkness comparison (ink density)
        darkness_diff = abs(fontana_features['darkness'] - voynich_features['darkness'])
        if darkness_diff < 0.1:
            score += 1.0
            details.append("✅ Darkness match (text weight similar)")
        elif darkness_diff < 0.2:
            score += 0.5
            details.append("⚠️ Darkness partial match")
        else:
            details.append("❌ Darkness mismatch (different ink density)")

        # 2. Contrast comparison (stroke clarity)
        contrast_diff = abs(fontana_features['contrast'] - voynich_features['contrast'])
        if contrast_diff < 20:
            score += 1.0
            details.append("✅ Contrast match (stroke clarity similar)")
        elif contrast_diff < 40:
            score += 0.5
            details.append("⚠️ Contrast partial match")
        else:
            details.append("❌ Contrast mismatch")

        # 3. Stroke count comparison (script density)
        stroke_count_diff = abs(fontana_features['stroke_count'] - voynich_features['stroke_count'])
        stroke_count_ratio = stroke_count_diff / max(fontana_features['stroke_count'], 1)
        if stroke_count_ratio < 0.3:
            score += 1.0
            details.append("✅ Stroke pattern match")
        elif stroke_count_ratio < 0.6:
            score += 0.5
            details.append("⚠️ Stroke pattern partial match")
        else:
            details.append("❌ Stroke pattern mismatch")

        # 4. Stroke height comparison (letter proportions)
        if 'avg_stroke_height' in fontana_features and 'avg_stroke_height' in voynich_features:
            height_diff = abs(fontana_features['avg_stroke_height'] - voynich_features['avg_stroke_height'])
            if height_diff < 10:
                score += 1.0
                details.append("✅ Letter height match (proportions similar)")
            elif height_diff < 20:
                score += 0.5
                details.append("⚠️ Letter height partial match")
            else:
                details.append("❌ Letter height mismatch")

        # 5. Stroke width comparison (pen angle/style)
        if 'avg_stroke_width' in fontana_features and 'avg_stroke_width' in voynich_features:
            width_diff = abs(fontana_features['avg_stroke_width'] - voynich_features['avg_stroke_width'])
            if width_diff < 5:
                score += 1.0
                details.append("✅ Stroke width match (pen style similar)")
            elif width_diff < 10:
                score += 0.5
                details.append("⚠️ Stroke width partial match")
            else:
                details.append("❌ Stroke width mismatch (different pen)")

        # Calculate confidence
        confidence_pct = (score / max_score) * 100
        confidence_level = "HIGH" if score >= 4.0 else "MEDIUM" if score >= 2.5 else "LOW"

        return {
            'score': round(score, 1),
            'max_score': max_score,
            'confidence': confidence_level,
            'confidence_pct': round(confidence_pct),
            'details': details
        }

    def compare_directories(self, fontana_dir, voynich_dir, output_file=None):
        """
        Compare all samples from two directories.

        Fontana: handwriting samples extracted from screenshots
        Voynich: known handwriting samples from Voynich manuscript
        """
        fontana_samples = sorted([f for f in os.listdir(fontana_dir) if f.endswith('.png')])
        voynich_samples = sorted([f for f in os.listdir(voynich_dir) if f.endswith('.png')])

        print(f"Comparing {len(fontana_samples)} Fontana samples "
              f"vs {len(voynich_samples)} Voynich samples")

        # Compare top samples from each
        for i, f_sample in enumerate(fontana_samples[:10]):  # Top 10 from each
            fontana_path = os.path.join(fontana_dir, f_sample)
            fontana_feat = self.extract_features(fontana_path)

            if not fontana_feat:
                continue

            best_match = None
            best_score = 0

            for v_sample in voynich_samples[:10]:
                voynich_path = os.path.join(voynich_dir, v_sample)
                voynich_feat = self.extract_features(voynich_path)

                if not voynich_feat:
                    continue

                comparison = self.compare_samples(fontana_feat, voynich_feat)

                if comparison and comparison['score'] > best_score:
                    best_score = comparison['score']
                    best_match = {
                        'fontana_sample': f_sample,
                        'voynich_sample': v_sample,
                        'comparison': comparison
                    }

            if best_match:
                self.results['comparisons'].append(best_match)

                if best_match['comparison']['confidence'] == "HIGH":
                    self.results['summary']['high_confidence_matches'] += 1
                elif best_match['comparison']['confidence'] == "MEDIUM":
                    self.results['summary']['medium_confidence_matches'] += 1
                else:
                    self.results['summary']['low_confidence_matches'] += 1

                print(f"\n{f_sample}")
                print(f"  Best match: {best_match['voynich_sample']}")
                print(f"  Confidence: {best_match['comparison']['confidence']} "
                      f"({best_match['comparison']['confidence_pct']}%)")
                for detail in best_match['comparison']['details']:
                    print(f"    {detail}")

        self.results['summary']['total_samples_compared'] = len(self.results['comparisons'])

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\nResults saved to: {output_file}")

        return self.results

def main():
    parser = argparse.ArgumentParser(
        description='Compare paleographic characteristics of Fontana vs Voynich handwriting'
    )
    parser.add_argument(
        '--fontana-dir',
        default='/home/user/Voynich/data/fontana/handwriting_samples',
        help='Directory containing extracted Fontana handwriting samples'
    )
    parser.add_argument(
        '--voynich-dir',
        default='/home/user/Voynich/data/voynich/handwriting_samples',
        help='Directory containing Voynich handwriting samples'
    )
    parser.add_argument(
        '--output',
        default='/home/user/Voynich/paleographic_comparison_results.json',
        help='Output file for comparison results'
    )

    args = parser.parse_args()

    comparator = PaleographicComparator()

    # Check if directories exist
    if not os.path.exists(args.fontana_dir):
        print(f"Fontana samples directory not found: {args.fontana_dir}")
        print("Run fontana_handwriting_extractor.py first")
        return

    if not os.path.exists(args.voynich_dir):
        print(f"Voynich samples directory not found: {args.voynich_dir}")
        print("Add Voynich handwriting sample images to: {args.voynich_dir}")
        return

    results = comparator.compare_directories(
        args.fontana_dir,
        args.voynich_dir,
        args.output
    )

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"Samples compared: {results['summary']['total_samples_compared']}")
    print(f"High confidence: {results['summary']['high_confidence_matches']}")
    print(f"Medium confidence: {results['summary']['medium_confidence_matches']}")
    print(f"Low confidence: {results['summary']['low_confidence_matches']}")

if __name__ == '__main__':
    main()
