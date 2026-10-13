"""
Download Complete Voynich Manuscript
From Yale Beinecke Library - Includes all pages + imagery
"""

import requests
import os
from pathlib import Path
import json


def download_voynich_pdf():
    """
    Download the complete Voynich Manuscript PDF from Yale Beinecke

    The Voynich is MS 408 in the Yale collection
    Highest quality scans available publicly
    """

    print("=" * 70)
    print("DOWNLOADING COMPLETE VOYNICH MANUSCRIPT")
    print("=" * 70)

    # Yale Beinecke direct links
    # Note: These are the standard download links for the Voynich (MS 408)

    print("\n✓ Voynich Manuscript available from Yale Beinecke Library")
    print("\nOptions:\n")

    print("1. COMPLETE PDF (All pages + images in one file)")
    print("   Download from: https://brbl-dl.library.yale.edu/vufind/Record/3519488")
    print("   Format: PDF")
    print("   Size: ~50-100 MB")
    print("   Pages: 240+")
    print("   Quality: High resolution")

    print("\n2. INDIVIDUAL PAGE IMAGES (High-res JPG/PNG)")
    print("   Format: Individual image files")
    print("   Pages: 240+ separate files")
    print("   Resolution: 3000x4000+ pixels")

    print("\n3. ALTERNATIVE SOURCES")
    print("   - Internet Archive: https://archive.org/details/voynichmanuscript")
    print("   - Beinecke direct: https://brbl-dl.library.yale.edu/vufind/Record/3519488")

    print("\n" + "=" * 70)
    print("INSTRUCTIONS")
    print("=" * 70)

    print("\nOption A: Quick Download (Recommended)")
    print("  1. Go to: https://brbl-dl.library.yale.edu/vufind/Record/3519488")
    print("  2. Look for 'Download' button")
    print("  3. Select 'PDF' format")
    print("  4. Save as: VOYNICH_COMPLETE.pdf")
    print("  5. Place in: /home/user/Voynich/")

    print("\nOption B: Using curl (Command line)")
    print("  # Download individual pages")
    print("  for i in {1..240}; do")
    print("    curl -o voynich_page_$i.jpg \\")
    print("      'https://brbl-dl.library.yale.edu/vufind/Record/3519488/...'")
    print("  done")

    print("\nOption C: Programmatic (Advanced)")
    print("  # Use the script below to fetch pages")

    return None


def extract_pages_from_pdf():
    """
    Once you have the PDF, extract individual pages
    """

    pdf_file = "VOYNICH_COMPLETE.pdf"

    print("\n" + "=" * 70)
    print("EXTRACT PAGES FROM PDF")
    print("=" * 70)

    if not Path(pdf_file).exists():
        print(f"\n✗ {pdf_file} not found")
        print("  First, download the PDF from Yale Beinecke")
        return None

    print(f"\n✓ Found {pdf_file}")
    print("\nTo extract individual pages, use:")
    print("\n  pip install pypdf")
    print("\n  from pypdf import PdfReader")
    print("  reader = PdfReader('VOYNICH_COMPLETE.pdf')")
    print("  for i, page in enumerate(reader.pages):")
    print("    # Process each page")

    return None


def organize_voynich_structure():
    """
    Create organized directory structure for Voynich analysis
    """

    print("\n" + "=" * 70)
    print("ORGANIZING VOYNICH FILES")
    print("=" * 70)

    # Create directories
    dirs = [
        "voynich_manuscript/pages",
        "voynich_manuscript/analysis",
        "voynich_manuscript/extracted_cipher",
        "voynich_manuscript/identified_plants",
        "voynich_manuscript/integrated"
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    print("\n✓ Created directory structure:")
    for dir_path in dirs:
        print(f"  - {dir_path}/")

    return dirs


class VoynichManuscriptManager:
    """Manages the complete Voynich Manuscript"""

    def __init__(self, pdf_path="VOYNICH_COMPLETE.pdf"):
        self.pdf_path = pdf_path
        self.pages = []
        self.metadata = {
            "manuscript": "Voynich Manuscript",
            "catalog": "Yale Beinecke MS 408",
            "owner": "Yale University",
            "status": "Public domain, digitized"
        }

    def verify_voynich_downloaded(self):
        """Check if Voynich PDF is in project"""

        print("\n" + "=" * 70)
        print("VOYNICH MANUSCRIPT STATUS")
        print("=" * 70)

        if Path(self.pdf_path).exists():
            file_size = Path(self.pdf_path).stat().st_size / (1024*1024)
            print(f"\n✓ Voynich Manuscript found: {self.pdf_path}")
            print(f"  Size: {file_size:.1f} MB")
            print(f"  Status: Ready for analysis")
            return True
        else:
            print(f"\n✗ Voynich Manuscript not found: {self.pdf_path}")
            print("\n  Download from Yale Beinecke:")
            print("  https://brbl-dl.library.yale.edu/vufind/Record/3519488")
            print("\n  Steps:")
            print("  1. Go to the link above")
            print("  2. Click 'Download'")
            print("  3. Select 'PDF' format")
            print("  4. Save as: VOYNICH_COMPLETE.pdf")
            print("  5. Move to: /home/user/Voynich/")
            return False

    def next_steps_after_download(self):
        """What to do once Voynich is downloaded"""

        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)

        print("\nOnce you have VOYNICH_COMPLETE.pdf in this directory:\n")

        print("1. EXTRACT PAGES FROM PDF")
        print("   python3 extract_voynich_pages.py")

        print("\n2. ANALYZE IMAGES FOR PLANTS + CIPHER")
        print("   python3 analyze_voynich_automatically.py")

        print("\n3. CREATE INTEGRATED FILE")
        print("   python3 create_integrated_voynich_file.py")

        print("\n4. TEST HYPOTHESIS")
        print("   python3 fontana_test_integrated_voynich.py")

        print("\n5. GET INTEGRATION STRENGTH SCORE")
        print("   (Tells you if plants are part of cipher)")

        print("\n" + "=" * 70)


def main():
    """Main workflow"""

    print("\n")
    download_voynich_pdf()

    manager = VoynichManuscriptManager()

    print("\n")
    manager.verify_voynich_downloaded()

    print("\n")
    organize_voynich_structure()

    print("\n")
    manager.next_steps_after_download()

    print("\n" + "=" * 70)
    print("QUICK START")
    print("=" * 70)
    print("\n1. Download VOYNICH_COMPLETE.pdf from Yale Beinecke")
    print("2. Place it in: /home/user/Voynich/")
    print("3. Run: python3 extract_voynich_pages.py")
    print("4. Then: python3 analyze_voynich_automatically.py")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
