"""
Fontana Cipher - Plant-Cipher Data Extraction Tool
Interactive tool for recording plant-text correlations from manuscript pages
"""

import json
import csv
from pathlib import Path
from datetime import datetime


class PlantCipherDataExtractor:
    """Interactive tool for extracting plant-cipher correlations"""

    def __init__(self, output_file="voynich_plant_cipher_data.json"):
        self.output_file = output_file
        self.extracted_pages = []
        self.load_existing()

    def load_existing(self):
        """Load existing extractions"""
        if Path(self.output_file).exists():
            with open(self.output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.extracted_pages = data.get('pages', [])
                print(f"✓ Loaded {len(self.extracted_pages)} existing extractions")
        else:
            self.extracted_pages = []
            print(f"✓ Starting fresh extraction database")

    def save(self):
        """Save all extractions"""
        output = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_pages_extracted": len(self.extracted_pages),
                "extraction_tool": "PlantCipherDataExtractor"
            },
            "pages": self.extracted_pages
        }

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✓ Saved {len(self.extracted_pages)} pages to {self.output_file}")

    def add_page_interactive(self):
        """Interactive extraction for one page"""

        print("\n" + "=" * 70)
        print("PLANT-CIPHER DATA EXTRACTION")
        print("=" * 70)

        # Get page number
        while True:
            try:
                page_num = int(input("\nPage number (1-155): "))
                if 1 <= page_num <= 155:
                    break
                else:
                    print("  Please enter a number between 1 and 155")
            except ValueError:
                print("  Invalid input. Enter a number.")

        # Check if already extracted
        if any(p['page_number'] == page_num for p in self.extracted_pages):
            print(f"  ⚠ Page {page_num} already extracted. Skipping to avoid duplicates.")
            return

        # Plants on page
        print(f"\nPlants identified on page {page_num}:")
        print("  (Enter plant names, one per line. Type 'done' when finished)")
        plants = []
        while True:
            plant = input("  Plant name (or 'done'): ").strip()
            if plant.lower() == 'done':
                break
            if plant:
                plants.append(plant)

        # Plant positions
        positions = []
        if plants:
            print(f"\nPositions for each plant:")
            for plant in plants:
                position = input(f"  Position for {plant} (top/center/bottom + left/center/right, e.g., 'top_left'): ").strip().lower()
                positions.append(position)

        # Cipher text on page
        has_cipher = input(f"\nDoes page {page_num} have cipher text? (y/n): ").strip().lower() == 'y'

        cipher_text = ""
        if has_cipher:
            print("  Enter cipher text as you see it (symbols separated by spaces)")
            print("  Example: O_N D_R F_C O C_O")
            cipher_text = input("  Cipher text: ").strip()

        # Cipher quality
        cipher_quality = "none"
        if cipher_text:
            print("\n  Cipher text quality:")
            print("    1. Clear (easy to read)")
            print("    2. Partial (some ambiguity)")
            print("    3. Degraded (hard to read)")
            quality_choice = input("  Quality (1-3): ").strip()
            quality_map = {'1': 'clear', '2': 'partial', '3': 'degraded'}
            cipher_quality = quality_map.get(quality_choice, 'unclear')

        # Medical content
        is_medical = input(f"\nDoes page {page_num} appear to be medical content? (y/n): ").strip().lower() == 'y'

        # Integration observations
        print("\nIntegration observations:")
        integration_observations = []

        checks = [
            ("Plant position relates to text position", "position_related"),
            ("Plant type seems to match text topic", "type_matches"),
            ("Multiple plants suggest multiple topics", "multiple_topics"),
            ("Same plant appears elsewhere (noted before)", "recurring_plant"),
            ("Plant size correlates with text amount", "size_correlates"),
        ]

        for check_text, check_key in checks:
            response = input(f"  {check_text}? (y/n): ").strip().lower()
            if response == 'y':
                integration_observations.append(check_key)

        # Confidence in integration
        print(f"\nConfidence that plants & text are INTEGRATED (1=decorative, 10=integrated):")
        while True:
            try:
                confidence = int(input("  Confidence (1-10): "))
                if 1 <= confidence <= 10:
                    break
            except ValueError:
                pass
            print("  Enter a number between 1 and 10")

        # Additional notes
        notes = input(f"\nAny additional observations: ").strip()

        # Create page record
        page_record = {
            "page_number": page_num,
            "plants_identified": plants,
            "plants_positions": positions,
            "has_cipher_text": has_cipher,
            "cipher_text": cipher_text,
            "cipher_text_quality": cipher_quality,
            "medical_content": is_medical,
            "integration_observations": integration_observations,
            "integration_confidence": confidence,
            "notes": notes,
            "extracted_date": datetime.now().isoformat()
        }

        self.extracted_pages.append(page_record)

        print(f"\n✓ Page {page_num} extracted")
        print(f"  Plants: {len(plants)}")
        print(f"  Cipher: {'Yes' if cipher_text else 'No'}")
        print(f"  Medical: {'Yes' if is_medical else 'No'}")
        print(f"  Integration confidence: {confidence}/10")

        # Ask to save
        if input("\nSave changes? (y/n): ").strip().lower() == 'y':
            self.save()

    def bulk_import_csv(self, csv_file):
        """Import from CSV file"""

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                page = {
                    "page_number": int(row['page_number']),
                    "plants_identified": row.get('plants', '').split(';') if row.get('plants') else [],
                    "plants_positions": row.get('positions', '').split(';') if row.get('positions') else [],
                    "has_cipher_text": row.get('has_cipher', '').lower() == 'yes',
                    "cipher_text": row.get('cipher_text', ''),
                    "cipher_text_quality": row.get('cipher_quality', 'unknown'),
                    "medical_content": row.get('medical', '').lower() == 'yes',
                    "integration_observations": row.get('observations', '').split(';') if row.get('observations') else [],
                    "integration_confidence": int(row.get('confidence', '5')),
                    "notes": row.get('notes', ''),
                    "extracted_date": datetime.now().isoformat()
                }

                # Check for duplicates
                if not any(p['page_number'] == page['page_number'] for p in self.extracted_pages):
                    self.extracted_pages.append(page)

        self.save()
        print(f"✓ Imported from {csv_file}")

    def get_statistics(self):
        """Get extraction statistics"""

        if not self.extracted_pages:
            return None

        total_pages = len(self.extracted_pages)
        pages_with_plants = sum(1 for p in self.extracted_pages if p['plants_identified'])
        pages_with_cipher = sum(1 for p in self.extracted_pages if p['has_cipher_text'])
        pages_with_both = sum(1 for p in self.extracted_pages
                            if p['plants_identified'] and p['has_cipher_text'])
        medical_pages = sum(1 for p in self.extracted_pages if p['medical_content'])

        avg_confidence = sum(p['integration_confidence'] for p in self.extracted_pages) / total_pages

        total_plants = sum(len(p['plants_identified']) for p in self.extracted_pages)

        stats = {
            "total_pages_extracted": total_pages,
            "pages_with_plants": pages_with_plants,
            "pages_with_cipher": pages_with_cipher,
            "pages_with_both": pages_with_both,
            "medical_pages": medical_pages,
            "average_integration_confidence": avg_confidence,
            "total_plants_identified": total_plants,
            "coverage": f"{total_pages}/155 pages ({100*total_pages/155:.0f}%)"
        }

        return stats

    def print_statistics(self):
        """Print formatted statistics"""

        stats = self.get_statistics()

        if not stats:
            print("No extractions yet")
            return

        print("\n" + "=" * 70)
        print("EXTRACTION STATISTICS")
        print("=" * 70)
        print(f"\nTotal pages extracted: {stats['total_pages_extracted']}")
        print(f"Coverage: {stats['coverage']}")
        print(f"\nPages with plants: {stats['pages_with_plants']}")
        print(f"Pages with cipher text: {stats['pages_with_cipher']}")
        print(f"Pages with BOTH: {stats['pages_with_both']}")
        print(f"  → {100*stats['pages_with_both']/max(stats['total_pages_extracted'], 1):.0f}% have plants + cipher")

        print(f"\nMedical content: {stats['medical_pages']} pages")
        print(f"Total plants identified: {stats['total_plants_identified']}")
        print(f"Average integration confidence: {stats['average_integration_confidence']:.1f}/10")

        if stats['pages_with_both'] > 5:
            print(f"\n✓ Sufficient data ({stats['pages_with_both']} pages) for integration analysis")
        elif stats['pages_with_both'] > 0:
            print(f"\n◆ Getting good data ({stats['pages_with_both']} pages), continue extraction")


    def preview_page(self, page_num):
        """Show extracted data for a page"""

        page = next((p for p in self.extracted_pages if p['page_number'] == page_num), None)

        if not page:
            print(f"Page {page_num} not extracted yet")
            return

        print(f"\n" + "=" * 70)
        print(f"PAGE {page_num}")
        print("=" * 70)
        print(f"Plants: {', '.join(page['plants_identified']) if page['plants_identified'] else 'None'}")
        print(f"Positions: {', '.join(page['plants_positions']) if page['plants_positions'] else 'N/A'}")
        print(f"Cipher text: {'Yes' if page['has_cipher_text'] else 'No'}")
        if page['cipher_text']:
            print(f"  Text: {page['cipher_text']}")
            print(f"  Quality: {page['cipher_text_quality']}")
        print(f"Medical content: {'Yes' if page['medical_content'] else 'No'}")
        print(f"Integration confidence: {page['integration_confidence']}/10")
        print(f"Observations: {', '.join(page['integration_observations']) if page['integration_observations'] else 'None'}")
        print(f"Notes: {page['notes'] if page['notes'] else 'None'}")

    def export_for_analysis(self, analysis_file="voynich_pages_for_analysis.json"):
        """Export formatted for analysis tool"""

        formatted_pages = []
        for page in self.extracted_pages:
            formatted = {
                "page_number": page['page_number'],
                "cipher_text": page.get('cipher_text', ''),
                "plants_identified": page['plants_identified'],
                "plants_positions": page['plants_positions'],
                "medical_content": page['medical_content'],
                "notes": page['notes'],
                "confidence": page['integration_confidence']
            }
            formatted_pages.append(formatted)

        output = {
            "metadata": {
                "extracted_date": datetime.now().isoformat(),
                "total_pages": len(formatted_pages),
                "ready_for_analysis": True
            },
            "pages": formatted_pages
        }

        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✓ Exported {len(formatted_pages)} pages to {analysis_file}")
        print(f"  Ready for: python3 fontana_image_text_integration.py")


def main():
    """Interactive menu"""

    extractor = PlantCipherDataExtractor()

    while True:
        print("\n" + "=" * 70)
        print("PLANT-CIPHER DATA EXTRACTION TOOL")
        print("=" * 70)
        print("\nOptions:")
        print("  1. Extract one page (interactive)")
        print("  2. View statistics")
        print("  3. Preview extracted page")
        print("  4. Import from CSV")
        print("  5. Export for analysis")
        print("  6. Quit")

        choice = input("\nChoice (1-6): ").strip()

        if choice == '1':
            extractor.add_page_interactive()

        elif choice == '2':
            extractor.print_statistics()

        elif choice == '3':
            page_num = int(input("Page number to preview: "))
            extractor.preview_page(page_num)

        elif choice == '4':
            csv_file = input("CSV file path: ").strip()
            if Path(csv_file).exists():
                extractor.bulk_import_csv(csv_file)
            else:
                print(f"File not found: {csv_file}")

        elif choice == '5':
            extractor.export_for_analysis()

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    print("=" * 70)
    print("FONTANA CIPHER - PLANT-CIPHER DATA EXTRACTION")
    print("=" * 70)
    print("\nThis tool helps you extract plant-cipher correlations")
    print("from your 155 Voynich manuscript screenshots.\n")
    print("Usage:")
    print("  python3 extract_plant_cipher_data.py")
    print("\nOr programmatic use:")
    print("  extractor = PlantCipherDataExtractor()")
    print("  extractor.add_page_interactive()")
    print("  extractor.print_statistics()")
    print("  extractor.export_for_analysis()")
    print("\n" + "=" * 70 + "\n")

    main()
