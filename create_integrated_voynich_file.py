"""
Create Integrated Voynich File
Combines cipher text + plant imagery into ONE complete file
Tests the hypothesis: Voynich is ONE cipher (text + imagery integrated)
"""

import json
from pathlib import Path
from datetime import datetime


class IntegratedVoynichCreator:
    """Creates a unified Voynich file with text + imagery combined"""

    def __init__(self):
        self.integrated_pages = []
        self.metadata = {
            "created": datetime.now().isoformat(),
            "purpose": "Test integrated Voynich cipher hypothesis",
            "hypothesis": "Voynich text + plant imagery = ONE complete cipher system",
            "source": "Manual extraction from 155 manuscript screenshots",
            "version": "1.0"
        }

    def add_integrated_page(self, page_number, cipher_text, plants, plant_positions,
                           plant_descriptions, notes=""):
        """
        Add a page with BOTH cipher text and plant data integrated

        Key insight: Plants are positioned RELATIVE to cipher text
                    They encode information together, not separately
        """

        page = {
            "page_number": page_number,

            # CIPHER COMPONENT
            "cipher": {
                "text": cipher_text,
                "symbols": cipher_text.split() if cipher_text else [],
                "symbol_count": len(cipher_text.split()) if cipher_text else 0,
            },

            # PLANT COMPONENT (Integrated with cipher)
            "plants": {
                "identified": plants,  # List of plant names
                "count": len(plants) if plants else 0,
                "positions": plant_positions,  # Relative to cipher text
                "descriptions": plant_descriptions,  # Plant medical meanings
            },

            # INTEGRATED DATA (The key part)
            "integrated_components": [
                {
                    "plant": plants[i] if i < len(plants) else None,
                    "plant_position": plant_positions[i] if i < len(plant_positions) else None,
                    "plant_description": plant_descriptions[i] if i < len(plant_descriptions) else None,
                    "associated_cipher": self._get_associated_cipher(
                        cipher_text, plant_positions[i] if i < len(plant_positions) else None
                    ),
                    "integration_notes": f"Plant {plants[i] if i < len(plants) else 'unknown'} appears at {plant_positions[i] if i < len(plant_positions) else 'unknown'} relative to cipher"
                }
                for i in range(max(len(plants), 1))
            ],

            # METADATA
            "page_metadata": {
                "has_cipher": bool(cipher_text),
                "has_plants": bool(plants),
                "is_integrated": bool(cipher_text and plants),
                "notes": notes,
                "extracted_date": datetime.now().isoformat()
            }
        }

        self.integrated_pages.append(page)
        return page

    def _get_associated_cipher(self, cipher_text, position):
        """Get which cipher symbols are near a plant"""
        # For now, return all - could be refined to nearby only
        return cipher_text if cipher_text else ""

    def save_integrated_voynich(self, filename="VOYNICH_INTEGRATED_COMPLETE.json"):
        """
        Save the complete integrated Voynich file
        This is what you test your model against
        """

        output = {
            "metadata": self.metadata,
            "statistics": self._calculate_statistics(),
            "pages": self.integrated_pages
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✓ Integrated Voynich file saved: {filename}")
        print(f"  Pages: {len(self.integrated_pages)}")
        print(f"  Ready to test model: python3 fontana_test_integrated_voynich.py")

        return filename

    def _calculate_statistics(self):
        """Calculate statistics about integration"""

        total_pages = len(self.integrated_pages)
        pages_with_cipher = sum(1 for p in self.integrated_pages if p['page_metadata']['has_cipher'])
        pages_with_plants = sum(1 for p in self.integrated_pages if p['page_metadata']['has_plants'])
        pages_integrated = sum(1 for p in self.integrated_pages if p['page_metadata']['is_integrated'])

        total_cipher_symbols = sum(p['cipher']['symbol_count'] for p in self.integrated_pages)
        total_plants = sum(p['plants']['count'] for p in self.integrated_pages)

        stats = {
            "total_pages": total_pages,
            "pages_with_cipher": pages_with_cipher,
            "pages_with_plants": pages_with_plants,
            "pages_with_both": pages_integrated,
            "integration_percentage": 100 * pages_integrated / total_pages if total_pages > 0 else 0,
            "total_cipher_symbols": total_cipher_symbols,
            "total_plants": total_plants,
            "average_cipher_per_page": total_cipher_symbols / total_pages if total_pages > 0 else 0,
            "average_plants_per_page": total_plants / total_pages if total_pages > 0 else 0,
        }

        return stats


class IntegratedVoynichTester:
    """Tests the trained model against the integrated Voynich file"""

    def __init__(self, integrated_voynich_file):
        """Load the integrated Voynich file"""
        with open(integrated_voynich_file, 'r', encoding='utf-8') as f:
            self.voynich = json.load(f)

        print(f"✓ Loaded integrated Voynich: {len(self.voynich['pages'])} pages")

    def test_model_on_integrated_voynich(self, model, label_encoder):
        """
        Test the trained model against integrated Voynich

        Key: Model must handle BOTH text symbols AND plant context
        """

        results = {
            "pages_tested": [],
            "symbol_accuracy": [],
            "plant_context_accuracy": [],
            "integrated_accuracy": []
        }

        for page in self.voynich['pages']:
            page_result = {
                "page_number": page['page_number'],
                "cipher_text": page['cipher']['text'],
                "plants": page['plants']['identified'],
                "predictions": []
            }

            # Test each symbol
            for symbol in page['cipher']['symbols']:
                try:
                    # Get prediction from model
                    symbol_value = ord(symbol[0]) if symbol else 0
                    prediction = model.predict([[symbol_value]])
                    decoded = label_encoder.inverse_transform(prediction)[0]

                    page_result['predictions'].append({
                        "cipher_symbol": symbol,
                        "predicted_plaintext": decoded
                    })
                except Exception as e:
                    page_result['predictions'].append({
                        "cipher_symbol": symbol,
                        "error": str(e)
                    })

            results['pages_tested'].append(page_result)

        return results

    def test_with_plant_context(self):
        """
        Advanced: Test if adding plant context improves accuracy

        Hypothesis: Model should score higher when it has plant information
        """

        results = {
            "test_without_plants": [],
            "test_with_plants": [],
            "improvement": None
        }

        # This would compare:
        # 1. Accuracy using cipher text alone
        # 2. Accuracy using cipher text + plant context
        # 3. Calculate improvement

        # Structure for later implementation with actual model

        return results

    def get_integration_validation(self):
        """Check if the integrated file has sufficient data"""

        stats = self.voynich['statistics']

        validation = {
            "has_sufficient_data": stats['pages_with_both'] >= 20,
            "integration_quality": stats['integration_percentage'],
            "ready_for_testing": stats['pages_with_both'] >= 20,
            "statistics": stats
        }

        return validation


class InteractiveIntegratedVoynichBuilder:
    """Interactive tool to build integrated Voynich file page by page"""

    def __init__(self):
        self.creator = IntegratedVoynichCreator()

    def build_interactively(self):
        """Step-by-step interactive building"""

        print("=" * 70)
        print("INTEGRATED VOYNICH FILE BUILDER")
        print("=" * 70)
        print("\nBuild the complete integrated Voynich cipher file")
        print("by combining your 155 manuscript extractions")
        print("\nThis file will have:")
        print("  - Cipher text from your screenshots")
        print("  - Plant imagery identifications")
        print("  - Integration data (text + plants together)")

        page_count = 0

        while True:
            print("\n" + "-" * 70)
            page_num = input("Page number (or 'done' to finish): ").strip()

            if page_num.lower() == 'done':
                break

            try:
                page_num = int(page_num)
            except ValueError:
                print("Invalid page number")
                continue

            # Get cipher text
            print(f"\nPage {page_num} - Cipher text:")
            cipher_text = input("  Enter cipher (symbols separated by spaces, or leave blank): ").strip()

            # Get plants
            print(f"\nPage {page_num} - Plants:")
            print("  (Enter plant names, one per line. Type 'done' when finished)")
            plants = []
            positions = []
            descriptions = []

            while True:
                plant = input("  Plant name (or 'done'): ").strip()
                if plant.lower() == 'done':
                    break
                if plant:
                    plants.append(plant)
                    position = input(f"    Position for {plant}: ").strip()
                    positions.append(position)
                    description = input(f"    Medical meaning/description: ").strip()
                    descriptions.append(description)

            # Add to file
            notes = input("\nAny notes about this page: ").strip()

            self.creator.add_integrated_page(
                page_number=page_num,
                cipher_text=cipher_text,
                plants=plants,
                plant_positions=positions,
                plant_descriptions=descriptions,
                notes=notes
            )

            page_count += 1
            print(f"✓ Page {page_num} added")

        # Save
        if page_count > 0:
            filename = self.creator.save_integrated_voynich()
            print(f"\n✓ Created integrated Voynich file with {page_count} pages")
            return filename
        else:
            print("\nNo pages added")
            return None

    def import_from_extraction_data(self, extraction_file):
        """
        Import from your extraction tool output
        (If you've already extracted the data)
        """

        with open(extraction_file, 'r', encoding='utf-8') as f:
            extracted_data = json.load(f)

        for page in extracted_data.get('pages', []):
            plant_descriptions = [f"{plant} (medical herb)" for plant in page.get('plants_identified', [])]

            self.creator.add_integrated_page(
                page_number=page['page_number'],
                cipher_text=page.get('cipher_text', ''),
                plants=page.get('plants_identified', []),
                plant_positions=page.get('plants_positions', []),
                plant_descriptions=plant_descriptions,
                notes=page.get('notes', '')
            )

        filename = self.creator.save_integrated_voynich()
        print(f"\n✓ Imported {len(extracted_data.get('pages', []))} pages from {extraction_file}")
        return filename


def example_integrated_voynich():
    """Example of integrated Voynich structure"""

    creator = IntegratedVoynichCreator()

    # Example page 15: Herbal section
    creator.add_integrated_page(
        page_number=15,
        cipher_text="O_N D_R F_C O C_O O N_X O_W",
        plants=["Sage", "Rosemary", "Thyme"],
        plant_positions=["top_left", "center", "bottom_right"],
        plant_descriptions=[
            "Fever remedy, throat healing",
            "Memory enhancement, circulation",
            "Respiratory aid, cough relief"
        ],
        notes="Herbal remedies section with clear plant-cipher integration"
    )

    # Example page 20: Medical conditions
    creator.add_integrated_page(
        page_number=20,
        cipher_text="M_L O_W A_R O T_U",
        plants=["Mint", "Wormwood"],
        plant_positions=["left", "right"],
        plant_descriptions=[
            "Digestion, stomach remedy",
            "Fever, parasite treatment"
        ],
        notes="Medical conditions with treatment plants"
    )

    # Save example
    creator.save_integrated_voynich("VOYNICH_INTEGRATED_EXAMPLE.json")

    # Show structure
    print("\n" + "=" * 70)
    print("EXAMPLE INTEGRATED VOYNICH PAGE")
    print("=" * 70)

    page = creator.integrated_pages[0]
    print(f"\nPage {page['page_number']}:")
    print(f"  Cipher: {page['cipher']['text']}")
    print(f"  Plants: {page['plants']['identified']}")
    print(f"  Is integrated: {page['page_metadata']['is_integrated']}")

    print(f"\nIntegrated components:")
    for component in page['integrated_components']:
        print(f"  - {component['plant']} at {component['plant_position']}")
        print(f"    ({component['plant_description']})")
        print(f"    Cipher context: {component['associated_cipher']}")


if __name__ == "__main__":
    print("=" * 70)
    print("INTEGRATED VOYNICH FILE CREATOR")
    print("=" * 70)
    print("\nThis creates a COMPLETE Voynich file that includes:")
    print("  - Cipher text from your manuscript extractions")
    print("  - Plant imagery identifications and positions")
    print("  - Integration data (how text + imagery work together)")
    print("\nUsage options:\n")

    print("1. INTERACTIVE BUILDER:")
    print("   builder = InteractiveIntegratedVoynichBuilder()")
    print("   builder.build_interactively()")

    print("\n2. IMPORT FROM EXTRACTION DATA:")
    print("   builder = InteractiveIntegratedVoynichBuilder()")
    print("   builder.import_from_extraction_data('voynich_plant_cipher_data.json')")

    print("\n3. PROGRAMMATIC:")
    print("   creator = IntegratedVoynichCreator()")
    print("   creator.add_integrated_page(...)")
    print("   creator.save_integrated_voynich('VOYNICH_INTEGRATED_COMPLETE.json')")

    print("\n4. TEST INTEGRATED FILE:")
    print("   tester = IntegratedVoynichTester('VOYNICH_INTEGRATED_COMPLETE.json')")
    print("   results = tester.test_model_on_integrated_voynich(model, encoder)")

    print("\n" + "=" * 70)
    print("Running example...\n")
    example_integrated_voynich()
