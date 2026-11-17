"""
Author, colophon, and marginalia audit tools for the Voynich corpus.

This module searches for possible author/scribe-related annotations
and structurally unusual manuscript-end loci.

It does not claim that any detected token is a verified author name.
"""

import re

import pandas as pd


class AuthorSignatureAuditor:
    """
    Lightweight audit helper for possible signature, scribe,
    colophon, and marginalia evidence.
    """

    def __init__(self, filepath="data/ZL3b-n.txt"):
        self.filepath = filepath
        self.lines = self._load_lines()

    def _load_lines(self):
        """
        Read the corpus file safely.
        """

        with open(
            self.filepath,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as handle:
            return handle.readlines()

    def audit_marginalia_and_comments(self):
        """
        Search IVTFF comment lines for author/scribe-related terms.

        This only reports textual annotations already present
        in the transcription/comments.
        """

        keywords = (
            "signature",
            "author",
            "jacobus",
            "tepenecz",
            "name",
            "hand",
            "latin",
            "roman",
        )

        findings = []

        for line_number, raw_line in enumerate(
            self.lines,
            start=1,
        ):
            line = raw_line.strip()

            if not line.startswith("###"):
                continue

            lower = line.lower()

            matched_keywords = [
                keyword
                for keyword in keywords
                if keyword in lower
            ]

            if matched_keywords:
                findings.append(
                    {
                        "line_number": line_number,
                        "matched_keywords": ", ".join(
                            matched_keywords
                        ),
                        "comment": line,
                    }
                )

        return findings

    def find_structural_signature_slots(self):
        """
        Find structurally unusual short text loci that may deserve
        manual inspection as possible colophon/signature candidates.

        Detection is intentionally conservative.
        """

        rows = []

        token_line_pattern = re.compile(
            r"^<([^>]+)>\s*(.*)$"
        )

        for line_number, raw_line in enumerate(
            self.lines,
            start=1,
        ):
            line = raw_line.rstrip("\n")

            match = token_line_pattern.match(line)

            if not match:
                continue

            locus = match.group(1).strip()
            text = match.group(2).strip()

            cleaned_text = re.sub(
                r"\{[^}]*\}",
                " ",
                text,
            )

            cleaned_text = re.sub(
                r"<[^>]*>",
                " ",
                cleaned_text,
            )

            cleaned_text = re.sub(
                r"[\[\](),;]",
                " ",
                cleaned_text,
            )

            tokens = [
                token
                for token in re.split(
                    r"[.\s]+",
                    cleaned_text,
                )
                if token
            ]

            locus_lower = locus.lower()

            is_colophon_locus = (
                "pc" in locus_lower
                or "pt" in locus_lower
            )

            is_short_tail = (
                len(tokens) <= 2
                and locus.startswith(("+", "="))
            )

            if not (
                is_colophon_locus
                or is_short_tail
            ):
                continue

            rows.append(
                {
                    "line_number": line_number,
                    "locus": locus,
                    "token_count": len(tokens),
                    "tokens": " ".join(tokens),
                    "raw_text": text,
                    "reason": (
                        "colophon-like locus"
                        if is_colophon_locus
                        else "short terminal locus"
                    ),
                }
            )

        if not rows:
            return pd.DataFrame(
                columns=[
                    "line_number",
                    "locus",
                    "token_count",
                    "tokens",
                    "raw_text",
                    "reason",
                ]
            )

        return pd.DataFrame(rows)

    def cross_check_vocabulary_isolation(
        self,
        candidate_tokens,
    ):
        """
        Count candidate token occurrences across the full corpus.

        Very low-frequency forms can be flagged for manual inspection,
        but rarity alone is not evidence of authorship.
        """

        corpus_text = "\n".join(self.lines).lower()

        results = []

        for candidate in candidate_tokens:
            token = str(candidate).strip().lower()

            if not token:
                continue

            pattern = re.compile(
                rf"(?<![a-z]){re.escape(token)}(?![a-z])"
            )

            count = len(
                pattern.findall(corpus_text)
            )

            results.append(
                {
                    "token": token,
                    "occurrences": count,
                    "isolated_hapax": count <= 2,
                }
            )

        return pd.DataFrame(results)


if __name__ == "__main__":
    auditor = AuthorSignatureAuditor()

    print(
        "\n=== Marginalia / Comment Evidence ==="
    )

    notes = auditor.audit_marginalia_and_comments()

    if notes:
        for item in notes:
            print(
                f'Line {item["line_number"]}: '
                f'{item["comment"]}'
            )
    else:
        print(
            "No matching author/scribe-related "
            "comment annotations found."
        )

    print(
        "\n=== Structural Candidate Loci ==="
    )

    slots = auditor.find_structural_signature_slots()

    if slots.empty:
        print(
            "No structural signature/colophon "
            "candidates detected."
        )
    else:
        print(
            slots.to_string(index=False)
        )