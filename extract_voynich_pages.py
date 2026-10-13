"""
Extract Pages from Voynich PDF
Converts PDF into individual page images for analysis
"""

import os
from pathlib import Path


class VoynichPDFExtractor:
    """Extracts individual pages from Voynich PDF"""

    def __init__(self, pdf_path="VOYNICH_COMPLETE.pdf"):
        self.pdf_path = pdf_path
        self.output_dir = "voynich_manuscript/pages"

    def check_dependencies(self):
        """Check if required libraries are installed"""

        print("=" * 70)
        print("CHECKING DEPENDENCIES")
        print("=" * 70)

        try:
            import pdf2image
            print("✓ pdf2image is installed")
            return True
        except ImportError:
            print("✗ pdf2image not installed")
            print("\nTo extract pages from PDF, install:")
            print("  pip install pdf2image pillow")
            print("\nYou also need poppler-utils:")
            print("  Ubuntu/Debian: sudo apt-get install poppler-utils")
            print("  macOS: brew install poppler")
            print("  Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/")
            return False

    def extract_pages(self):
        """Extract all pages from PDF"""

        if not Path(self.pdf_path).exists():
            print(f"✗ PDF not found: {self.pdf_path}")
            print("\nDownload from Yale Beinecke:")
            print("  https://brbl-dl.library.yale.edu/vufind/Record/3519488")
            return None

        print("\n" + "=" * 70)
        print("EXTRACTING PAGES FROM VOYNICH PDF")
        print("=" * 70)

        try:
            from pdf2image import convert_from_path
            print(f"\n✓ Loading {self.pdf_path}...")

            # Convert PDF to images
            images = convert_from_path(self.pdf_path)

            print(f"✓ Found {len(images)} pages")

            # Create output directory
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)

            # Save each page
            print(f"\nSaving pages to {self.output_dir}/...\n")

            for i, image in enumerate(images):
                page_num = i + 1
                filename = f"{self.output_dir}/voynich_page_{page_num:03d}.png"
                image.save(filename, 'PNG')

                if page_num % 20 == 0:
                    print(f"  ✓ Saved page {page_num}")

            print(f"\n✓ Extraction complete!")
            print(f"  Total pages: {len(images)}")
            print(f"  Location: {self.output_dir}/")

            return len(images)

        except ImportError:
            print("✗ pdf2image not installed")
            print("\nInstall with:")
            print("  pip install pdf2image pillow")
            return None

    def verify_extraction(self):
        """Verify pages were extracted"""

        page_files = list(Path(self.output_dir).glob("voynich_page_*.png"))

        if not page_files:
            print(f"✗ No pages found in {self.output_dir}")
            return False

        print(f"\n✓ Verification:")
        print(f"  Pages extracted: {len(page_files)}")
        print(f"  First page: {page_files[0]}")
        print(f"  Last page: {page_files[-1]}")

        return True


def manual_extraction_instructions():
    """Provide manual extraction instructions if libraries unavailable"""

    print("\n" + "=" * 70)
    print("ALTERNATIVE: MANUAL EXTRACTION")
    print("=" * 70)

    print("\nIf you can't install pdf2image, extract manually:\n")

    print("1. Open VOYNICH_COMPLETE.pdf in Adobe Reader")
    print("2. File → Export As → Images")
    print("3. Select PNG format")
    print("4. Choose folder: voynich_manuscript/pages/")
    print("5. Export all pages")

    print("\nOR use online PDF converter:")
    print("  https://convertio.co/pdf-png/")
    print("  Upload VOYNICH_COMPLETE.pdf")
    print("  Download all PNG files")
    print("  Save to: voynich_manuscript/pages/")

    print("\nOR use command line (if ImageMagick installed):")
    print("  convert VOYNICH_COMPLETE.pdf voynich_manuscript/pages/page-%03d.png")

    print("\n" + "=" * 70)


def main():
    """Main workflow"""

    print("\nVoynich PDF Page Extractor")
    print("=" * 70)

    extractor = VoynichPDFExtractor()

    # Check if PDF exists
    if not Path(extractor.pdf_path).exists():
        print(f"\n✗ {extractor.pdf_path} not found")
        print("\nSteps to get the PDF:")
        print("  1. Go to: https://brbl-dl.library.yale.edu/vufind/Record/3519488")
        print("  2. Click 'Download'")
        print("  3. Select 'PDF' format")
        print("  4. Save as: VOYNICH_COMPLETE.pdf")
        print("  5. Place in: /home/user/Voynich/")
        print("\nThen run this script again.")
        return

    print(f"\n✓ Found {extractor.pdf_path}")

    # Check dependencies
    if not extractor.check_dependencies():
        manual_extraction_instructions()
        return

    # Extract pages
    page_count = extractor.extract_pages()

    if page_count:
        extractor.verify_extraction()

        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("\n✓ Pages extracted and ready for analysis")
        print("\nRun the analyzer:")
        print("  python3 analyze_voynich_automatically.py")
        print("\nThis will:")
        print("  1. Identify plant illustrations")
        print("  2. Extract cipher text")
        print("  3. Create integrated file")
        print("  4. Test hypothesis")
        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
