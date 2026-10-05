#!/usr/bin/env python3
"""
AUTOMATIC RHAZES MANUSCRIPT FETCHER
Searches and downloads digitized Rhazes manuscripts from public archives.

This tool:
1. Searches Archive.org for Rhazes texts
2. Searches for Irish manuscript MS 10297
3. Downloads available digitized versions
4. Saves to data/ directory
5. Runs analyzer automatically

Usage:
    python3 analyses/fetch_rhazes_manuscripts.py
    python3 analyses/fetch_rhazes_manuscripts.py --search "Rhazes Continens"
    python3 analyses/fetch_rhazes_manuscripts.py --fetch-all
"""

import requests
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import subprocess

class RhazesManuscriptDownloader:
    """Automatically finds and downloads Rhazes manuscripts."""

    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # Archive.org API endpoint
        self.archive_api = "https://archive.org/advancedsearch.php"

        # Manuscripts to search for
        self.targets = [
            {
                "name": "Kitabul Hawi Fi't Tibb (Rhazes Continens)",
                "search_terms": ["Rhazes", "Continens", "Hawi"],
                "priority": "CRITICAL",
                "notes": "Main medical encyclopedia"
            },
            {
                "name": "Rhazes De Variolis et Morbillis",
                "search_terms": ["Rhazes", "variolis", "morbillis"],
                "priority": "HIGH",
                "notes": "Systematic case descriptions"
            },
            {
                "name": "Rhazes Almanazor",
                "search_terms": ["Rhazes", "Almanazor", "Almansori"],
                "priority": "CRITICAL",
                "notes": "Your ancestor translated this"
            },
            {
                "name": "Medical Classics by Rhazes",
                "search_terms": ["Rhazes", "medical", "classics"],
                "priority": "HIGH",
                "notes": "Collection of Rhazes works"
            }
        ]

    def search_archive_org(self, query: str) -> List[Dict]:
        """Search Archive.org for manuscripts."""
        print(f"\n🔍 Searching Archive.org for: {query}")

        try:
            params = {
                "q": query,
                "output": "json",
                "rows": 20,
                "fl": ["identifier", "title", "description", "creator", "date", "format"]
            }

            response = requests.get(self.archive_api, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            docs = data.get("response", {}).get("docs", [])

            if docs:
                print(f"✓ Found {len(docs)} results")
                return docs
            else:
                print(f"✗ No results found")
                return []

        except requests.RequestException as e:
            print(f"✗ Search failed: {e}")
            return []

    def get_archive_download_url(self, identifier: str) -> Optional[str]:
        """Get download URL for an Archive.org item."""
        return f"https://archive.org/download/{identifier}/{identifier}_djvu.txt"

    def download_manuscript(self, identifier: str, title: str) -> Optional[Path]:
        """Download a manuscript from Archive.org."""
        print(f"\n📥 Downloading: {title}")

        try:
            # Try different download formats
            urls = [
                f"https://archive.org/download/{identifier}/{identifier}_djvu.txt",
                f"https://archive.org/download/{identifier}/{identifier}_pdf.txt",
                f"https://archive.org/stream/{identifier}/page/1_djvu.txt",
            ]

            for url in urls:
                try:
                    response = requests.get(url, timeout=15)
                    if response.status_code == 200 and len(response.text) > 100:
                        # Save file
                        filename = self.data_dir / f"rhazes_{identifier}.txt"
                        with open(filename, 'w') as f:
                            f.write(response.text)

                        print(f"✓ Downloaded to: {filename}")
                        print(f"  Size: {len(response.text)} bytes")
                        return filename
                except Exception as e:
                    continue

            print(f"✗ Could not download from any URL")
            return None

        except Exception as e:
            print(f"✗ Download failed: {e}")
            return None

    def analyze_downloaded(self, filepath: Path):
        """Run analyzer on downloaded manuscript."""
        print(f"\n🔬 Analyzing: {filepath.name}")

        try:
            result = subprocess.run(
                [sys.executable, "analyses/source_text_analyzer.py", str(filepath)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                print(f"✓ Analysis complete")
                print(f"\nOutput:\n{result.stdout[-500:]}")  # Last 500 chars
                return True
            else:
                print(f"✗ Analysis failed")
                return False

        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def search_all_targets(self):
        """Search for all target manuscripts."""
        print("\n" + "="*80)
        print("SEARCHING FOR RHAZES MANUSCRIPTS")
        print("="*80)

        all_results = []

        for target in self.targets:
            print(f"\n[{target['priority']}] {target['name']}")
            print(f"Notes: {target['notes']}")

            # Search with different combinations
            for search_term in target['search_terms']:
                results = self.search_archive_org(search_term)
                if results:
                    all_results.extend(results)
                    for result in results:
                        print(f"  - {result.get('title', 'Unknown')}")
                        print(f"    ID: {result.get('identifier')}")

        return all_results

    def fetch_and_analyze(self, max_downloads: int = 3):
        """Find, download, and analyze manuscripts."""
        print("\n" + "="*80)
        print("FETCH & ANALYZE RHAZES MANUSCRIPTS")
        print("="*80)

        # Search
        results = self.search_all_targets()

        if not results:
            print("\n✗ No manuscripts found in Archive.org")
            return

        # Download and analyze top results
        print(f"\n📥 Downloading top {max_downloads} results...")

        downloaded_count = 0
        for i, result in enumerate(results[:max_downloads]):
            if downloaded_count >= max_downloads:
                break

            identifier = result.get('identifier')
            title = result.get('title', 'Unknown')

            if identifier:
                filepath = self.download_manuscript(identifier, title)
                if filepath:
                    self.analyze_downloaded(filepath)
                    downloaded_count += 1

        print(f"\n✓ Downloaded and analyzed {downloaded_count} manuscripts")

    def list_local_rhazes(self):
        """List any Rhazes manuscripts already in data directory."""
        print("\n" + "="*80)
        print("LOCAL RHAZES MANUSCRIPTS")
        print("="*80)

        rhazes_files = list(self.data_dir.glob("rhazes_*.txt"))

        if rhazes_files:
            print(f"\nFound {len(rhazes_files)} local manuscripts:")
            for f in rhazes_files:
                size = f.stat().st_size
                print(f"  - {f.name} ({size:,} bytes)")
        else:
            print("\nNo local Rhazes manuscripts found.")
            print("Run with --fetch-all to download from Archive.org")

        return rhazes_files


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Automatic Rhazes Manuscript Fetcher")
    parser.add_argument("--search", type=str, help="Search for specific manuscript")
    parser.add_argument("--fetch-all", action="store_true", help="Fetch all available manuscripts")
    parser.add_argument("--list", action="store_true", help="List local manuscripts")
    parser.add_argument("--max-downloads", type=int, default=3, help="Maximum manuscripts to download")

    args = parser.parse_args()

    downloader = RhazesManuscriptDownloader()

    if args.list or not any([args.search, args.fetch_all]):
        downloader.list_local_rhazes()

    if args.search:
        results = downloader.search_archive_org(args.search)
        if results:
            print("\nFound results:")
            for result in results:
                print(f"  {result.get('title')}")
                print(f"    ID: {result.get('identifier')}")

    if args.fetch_all:
        downloader.fetch_and_analyze(args.max_downloads)


if __name__ == "__main__":
    main()
