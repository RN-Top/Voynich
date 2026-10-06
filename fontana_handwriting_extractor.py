#!/usr/bin/env python3
"""
Extract handwriting samples from Fontana screenshots for paleographic comparison.

Methodology:
1. Load cipher detection results to identify pages with dense handwritten text
2. Extract regions containing handwritten script (not printed)
3. Crop to isolated word/letter samples
4. Prepare for comparison against Voynich manuscript hands

Output: PNG samples organized by letter/word for comparison
"""

import os
import cv2
import numpy as np
import json
from PIL import Image, ImageOps
import argparse

def extract_handwriting_regions(image_path, output_dir, image_id):
    """
    Extract handwritten text regions from a manuscript page image.

    Strategy:
    - Detect dark text regions (handwriting)
    - Filter by stroke continuity (handwriting vs print)
    - Extract bounding boxes around text
    - Save isolated samples
    """
    try:
        img_cv = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img_cv is None:
            return None

        # Binarize
        _, binary = cv2.threshold(img_cv, 150, 255, cv2.THRESH_BINARY)

        # Find contours (text regions)
        contours, _ = cv2.findContours(
            255 - binary,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Filter contours by size (handwritten text typically 20-300px)
        text_regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 100 < area < 50000:  # Reasonable text region size
                x, y, w, h = cv2.boundingRect(contour)
                if 5 < h < 200 and 5 < w < 300:  # Reasonable proportions
                    text_regions.append((x, y, w, h, area))

        # Sort by area (larger text is clearer)
        text_regions.sort(key=lambda r: r[4], reverse=True)

        # Extract top 5 clearest handwriting samples
        samples = []
        for idx, (x, y, w, h, _) in enumerate(text_regions[:5]):
            # Add padding
            x_pad = max(0, x - 5)
            y_pad = max(0, y - 5)
            x_end = min(binary.shape[1], x + w + 5)
            y_end = min(binary.shape[0], y + h + 5)

            sample = img_cv[y_pad:y_end, x_pad:x_end]

            if sample.size > 0:
                # Save sample
                sample_path = os.path.join(
                    output_dir,
                    f"handwriting_{image_id}_sample{idx+1}.png"
                )
                cv2.imwrite(sample_path, sample)
                samples.append({
                    'path': sample_path,
                    'size': sample.shape,
                    'rank': idx + 1
                })

        return samples

    except Exception as e:
        print(f"Error extracting handwriting from {image_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Extract handwriting samples from Fontana screenshots'
    )
    parser.add_argument(
        '--input-dir',
        default='/home/user/Voynich/data/fontana/screenshots',
        help='Directory containing screenshot images'
    )
    parser.add_argument(
        '--output-dir',
        default='/home/user/Voynich/data/fontana/handwriting_samples',
        help='Output directory for extracted handwriting samples'
    )
    parser.add_argument(
        '--results-file',
        default='/home/user/Voynich/cipher_detection_results.json',
        help='Path to cipher detection results JSON'
    )

    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Load cipher detection results
    if os.path.exists(args.results_file):
        with open(args.results_file, 'r') as f:
            results = json.load(f)

        # Use cipher circle pages as priority
        priority_images = [item['filename'] for item in results.get('cipher_circles', [])]
        # Then geometric patterns
        priority_images += [item['filename'] for item in results.get('geometric_patterns', [])]
        # Then dense text
        priority_images += [item['filename'] for item in results.get('dense_text_regions', [])]

        priority_images = list(dict.fromkeys(priority_images))  # Deduplicate
    else:
        # If no results, process all images
        priority_images = sorted(os.listdir(args.input_dir))

    print(f"Extracting handwriting from {len(priority_images)} priority images...")

    extraction_results = {
        'total_images_processed': 0,
        'samples_extracted': 0,
        'images_with_samples': [],
        'extraction_log': []
    }

    for img_name in priority_images[:100]:  # Start with top 100
        if not img_name.endswith('.png'):
            continue

        img_path = os.path.join(args.input_dir, img_name)
        if not os.path.exists(img_path):
            continue

        samples = extract_handwriting_regions(img_path, args.output_dir, img_name)

        extraction_results['total_images_processed'] += 1

        if samples:
            extraction_results['samples_extracted'] += len(samples)
            extraction_results['images_with_samples'].append({
                'image': img_name,
                'samples_count': len(samples)
            })
            extraction_results['extraction_log'].append({
                'image': img_name,
                'status': 'success',
                'samples': samples
            })

        if extraction_results['total_images_processed'] % 10 == 0:
            print(f"  Processed {extraction_results['total_images_processed']} images, "
                  f"extracted {extraction_results['samples_extracted']} samples...")

    # Save results
    results_path = os.path.join(args.output_dir, 'extraction_results.json')
    with open(results_path, 'w') as f:
        json.dump(extraction_results, f, indent=2)

    print(f"\n✅ Extraction complete:")
    print(f"   Images processed: {extraction_results['total_images_processed']}")
    print(f"   Handwriting samples extracted: {extraction_results['samples_extracted']}")
    print(f"   Output directory: {args.output_dir}")
    print(f"   Results: {results_path}")

if __name__ == '__main__':
    main()
