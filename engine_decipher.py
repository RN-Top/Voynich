"""
Exploratory lexical hypothesis engine for Voynich tokens.

This module does NOT claim the Voynich manuscript has been deciphered.
It separates curated hypotheses from transparent morphology heuristics
and returns an evidence label plus confidence for every interpretation.
"""

import re
from collections import Counter

import pandas as pd


CURATED_HYPOTHESES = {
    "qokedy": {
        "latin_lemma": "coquere",
        "english_hypothesis": "cook / boil",
        "induced_role": "OPERATOR_VERB",
        "evidence": "curated hypothesis",
        "confidence": 0.35,
    },
    "qokeey": {
        "latin_lemma": "calfacere",
        "english_hypothesis": "apply heat",
        "induced_role": "OPERATOR_VERB",
        "evidence": "curated hypothesis",
        "confidence": 0.30,
    },
    "okedy": {
        "latin_lemma": "coquatur",
        "english_hypothesis": "let it boil",
        "induced_role": "OPERATOR_VERB",
        "evidence": "curated hypothesis",
        "confidence": 0.30,
    },
    "daiin": {
        "latin_lemma": "aquam",
        "english_hypothesis": "water / decoction",
        "induced_role": "OPERAND_NOUN",
        "evidence": "curated hypothesis",
        "confidence": 0.30,
    },
    "shedy": {
        "latin_lemma": "radicem",
        "english_hypothesis": "root",
        "induced_role": "OPERAND_NOUN",
        "evidence": "curated hypothesis",
        "confidence": 0.25,
    },
    "chedy": {
        "latin_lemma": "herbam",
        "english_hypothesis": "herb / plant",
        "induced_role": "OPERAND_NOUN",
        "evidence": "curated hypothesis",
        "confidence": 0.25,
    },
    "otcheody": {
        "latin_lemma": "vasculum",
        "english_hypothesis": "vessel / jar",
        "induced_role": "OPERAND_NOUN",
        "evidence": "curated hypothesis",
        "confidence": 0.25,
    },
    "qokal": {
        "latin_lemma": "distillare",
        "english_hypothesis": "distill",
        "induced_role": "OPERATOR_VERB",
        "evidence": "curated hypothesis",
        "confidence": 0.25,
    },
    "chdam": {
        "latin_lemma": "resolvere",
        "english_hypothesis": "dissolve completely",
        "induced_role": "TERMINAL_FLUSH",
        "evidence": "curated hypothesis",
        "confidence": 0.20,
    },
    "am": {
        "latin_lemma": "terminare",
        "english_hypothesis": "finish / end",
        "induced_role": "TERMINAL_FLUSH",
        "evidence": "curated hypothesis",
        "confidence": 0.20,
    },
    "ydaraishy": {
        "latin_lemma": "auctor",
        "english_hypothesis": "author / composed by",
        "induced_role": "OPERAND_NOUN",
        "evidence": "speculative attribution hypothesis",
        "confidence": 0.10,
    },
    "ytchas": {
        "latin_lemma": "scriptor",
        "english_hypothesis": "scribe / written by",
        "induced_role": "OPERAND_NOUN",
        "evidence": "speculative attribution hypothesis",
        "confidence": 0.10,
    },
    "oraiin": {
        "latin_lemma": "oratio",
        "english_hypothesis": "prayer / blessing",
        "induced_role": "OPERAND_NOUN",
        "evidence": "curated hypothesis",
        "confidence": 0.15,
    },
    "chkor": {
        "latin_lemma": "finitus",
        "english_hypothesis": "completed / sealed",
        "induced_role": "TERMINAL_FLUSH",
        "evidence": "curated hypothesis",
        "confidence": 0.15,
    },
}


class WholeManuscriptDecipherer:
    """
    Builds an exploratory lexical table from corpus vocabulary.

    Known entries use explicitly curated hypotheses.
    Unknown entries receive only conservative morphology-based labels.
    """

    def __init__(self, tokens):
        cleaned = []

        for token in tokens:
            token = str(token).strip().lower()

            if not token:
                continue

            token = re.sub(r"[^a-z]", "", token)

            if token:
                cleaned.append(token)

        self.token_counts = Counter(cleaned)

        self.vocabulary = [
            token
            for token, _ in self.token_counts.most_common(1200)
        ]

        self.lookup = {}

        for token in self.vocabulary:
            self.lookup[token] = self._interpret_token(token)

    def _interpret_token(self, token):
        """
        Return one hypothesis record for a token.
        """

        if token in CURATED_HYPOTHESES:
            row = CURATED_HYPOTHESES[token].copy()
            row["voynich_token"] = token
            return row

        if token.endswith(("am", "m")):
            return {
                "voynich_token": token,
                "latin_lemma": "",
                "english_hypothesis": (
                    "[terminal / closure-like form]"
                ),
                "induced_role": "TERMINAL_FLUSH",
                "evidence": "morphology heuristic",
                "confidence": 0.08,
            }

        if token.endswith(("edy", "eey")):
            return {
                "voynich_token": token,
                "latin_lemma": "",
                "english_hypothesis": (
                    "[process-like form]"
                ),
                "induced_role": "OPERATOR_VERB",
                "evidence": "morphology heuristic",
                "confidence": 0.08,
            }

        if token.endswith(("ol", "or", "ar", "al")):
            return {
                "voynich_token": token,
                "latin_lemma": "",
                "english_hypothesis": (
                    "[modifier-like form]"
                ),
                "induced_role": "MODIFIER_ADJ",
                "evidence": "morphology heuristic",
                "confidence": 0.06,
            }

        if token.startswith("q"):
            return {
                "voynich_token": token,
                "latin_lemma": "",
                "english_hypothesis": (
                    "[q-prefixed operator-like form]"
                ),
                "induced_role": "OPERATOR_VERB",
                "evidence": "morphology heuristic",
                "confidence": 0.06,
            }

        return {
            "voynich_token": token,
            "latin_lemma": "",
            "english_hypothesis": (
                "[unresolved lexical item]"
            ),
            "induced_role": "UNKNOWN",
            "evidence": "no semantic evidence",
            "confidence": 0.00,
        }

    def interpret_token(self, token):
        """
        Interpret one token.

        Tokens outside the top corpus vocabulary are still handled
        using the same conservative rules.
        """

        cleaned = re.sub(
            r"[^a-z]",
            "",
            str(token).strip().lower(),
        )

        if not cleaned:
            return {
                "voynich_token": "",
                "latin_lemma": "",
                "english_hypothesis": "",
                "induced_role": "UNKNOWN",
                "evidence": "empty input",
                "confidence": 0.00,
            }

        if cleaned in self.lookup:
            return self.lookup[cleaned].copy()

        return self._interpret_token(cleaned)

    def interpret_phrase(self, phrase):
        """
        Interpret a sequence of Voynich tokens.

        Returns:
            interpretation: human-readable hypothesis string
            gloss: compact token-by-token gloss
            rows: detailed per-token records
        """

        raw_tokens = str(phrase).split()

        rows = [
            self.interpret_token(token)
            for token in raw_tokens
        ]

        rows = [
            row
            for row in rows
            if row["voynich_token"]
        ]

        if not rows:
            return {
                "interpretation": "",
                "gloss": "",
                "rows": [],
            }

        interpretation = " ".join(
            row["english_hypothesis"]
            for row in rows
        )

        gloss = " | ".join(
            (
                f'{row["voynich_token"]}: '
                f'{row["english_hypothesis"]}'
            )
            for row in rows
        )

        return {
            "interpretation": interpretation,
            "gloss": gloss,
            "rows": rows,
        }

    def translate_phrase(self, phrase):
        """
        Backward-compatible alias.

        The result is still an exploratory interpretation,
        not a validated translation.
        """

        result = self.interpret_phrase(phrase)

        return {
            "translation": result["interpretation"],
            "gloss": result["gloss"],
            "rows": result["rows"],
        }

    def get_full_dictionary(self):
        """
        Return the current corpus vocabulary and hypotheses
        as a DataFrame.
        """

        rows = []

        for token in self.vocabulary:
            row = self.lookup[token].copy()
            row["frequency"] = self.token_counts[token]
            rows.append(row)

        if not rows:
            return pd.DataFrame(
                columns=[
                    "voynich_token",
                    "frequency",
                    "latin_lemma",
                    "english_hypothesis",
                    "induced_role",
                    "evidence",
                    "confidence",
                ]
            )

        df = pd.DataFrame(rows)

        return df[
            [
                "voynich_token",
                "frequency",
                "latin_lemma",
                "english_hypothesis",
                "induced_role",
                "evidence",
                "confidence",
            ]
        ].sort_values(
            ["frequency", "voynich_token"],
            ascending=[False, True],
        ).reset_index(drop=True)