"""
voynich-state-viewer: Author Signature & Scribal Colophon Auditor
Searches ZL3b-n.txt for structural signatures, paragraph-final colophons,
and non-Voynich scribal marginalia.
"""

import re
import pandas as pd
from typing import Dict, List


class AuthorSignatureAuditor:
    def __init__(self, filepath: str = "data/ZL3b-n.txt"):
        self.filepath = filepath
        self.lines = []
        self._load_corpus()

    def _load_corpus(self):
        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            self.lines = f.readlines()

    def audit_marginalia_and_comments(self) -> List[Dict[str, str]]:
        """
        Extracts IVTFF comments explicitly referencing signatures, external scripts,
        or author-name candidates (e.g., Jacobus de Tepenecz, marginal alphabets).
        """
        findings = []
        current_folio = "unknown"

        for line in self.lines:
            line_str = line.strip()
            folio_match = re.match(r"<f(\d+[rv]\d*)>", line_str)
            if folio_match:
                current_folio = f"f{folio_match.group(1)}"

            # Detect comments discussing hands, signatures, or Latin/Roman scripts
            if line_str.startswith("###"):
                lower = line_str.lower()
                if any(k in lower for k in ["signature", "author", "jacobus", "tepenecz", "name", "hand"]):
                    findings.append({
                        "folio": current_folio,
                        "type": "CORPUS_COMMENT",
                        "content": line_str.replace("###", "").strip()
                    })
        return findings

    def find_structural_signature_slots(self) -> pd.DataFrame:
        """
        Locates tokens appearing in dedicated structural exit/colophon positions:
        - Line types =Pt (paragraph terminal) or +Pc (closing colophon lines)
        - Standalone indented/right-flushed lines containing 1-3 tokens
        """
        records = []
        token_line_regex = re.compile(r"<f(\d+[rv]\d*)\.(\d+),([@=+*][A-Za-z0-9_]+)>\s*(.*)")

        for line in self.lines:
            m = token_line_regex.match(line.strip())
            if not m:
                continue

            folio = f"f{m.group(1)}"
            line_no = m.group(2)
            locus = m.group(3)
            raw_text = m.group(4)

            # Clean markup to extract raw surface tokens
            clean = re.sub(r"<[%$!@].*?>", "", raw_text)
            clean = re.sub(r"<!.*?>", "", clean)
            tokens = [t for t in re.split(r"[.,\s]+", clean) if t and not t.startswith("<")]

            # Colophon loci (+Pc, =Pt) or ultra-short terminal paragraph lines
            is_colophon_locus = ("Pc" in locus) or ("Pt" in locus)
            is_short_tail = len(tokens) <= 2 and locus.startswith("+")

            if is_colophon_locus or is_short_tail:
                records.append({
                    "folio": folio,
                    "line": line_no,
                    "locus": locus,
                    "token_count": len(tokens),
                    "tokens": " ".join(tokens),
                    "raw_line": raw_text
                })

        return pd.DataFrame(records)

    def cross_check_vocabulary_isolation(self, signature_candidates: List[str]) -> pd.DataFrame:
        """
        Checks whether signature-slot tokens appear anywhere else in running prose.
        True proper names/signatures are far more likely to have extremely low
        prose recurrence (singletons or localized to that specific folio).
        """
        all_text = " ".join(self.lines)
        results = []
        for cand in set(signature_candidates):
            if not cand:
                continue
            # Count exact matches bounded by typical IVTFF separators
            pattern = re.compile(rf"[.,\s<]{re.escape(cand)}[.,\s>]")
            count = len(pattern.findall(all_text))
            results.append({
                "candidate_token": cand,
                "total_manuscript_occurrences": count,
                "is_isolated_hapax": count <= 2
            })
        return pd.DataFrame(results).sort_values(by="total_manuscript_occurrences")


if __name__ == "__main__":
    auditor = AuthorSignatureAuditor()
    print("=== CORPUS EVIDENCE / PROVENANCE NOTES ===")
    for note in auditor.audit_marginalia_and_comments()[:5]:
        print(f"[{note['folio']}] {note['content']}")

    print("\n=== CANDIDATE SIGNATURE / COLOPHON LOCI ===")
    slots_df = auditor.find_structural_signature_slots()
    print(slots_df.head(10)[["folio", "line", "locus", "tokens"]])
