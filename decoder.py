"""
Astronomical-domain analysis tools for the Voynich corpus.

This module measures whether token carriers are unusually associated
with astronomical/zodiac manuscript sections.

It does NOT infer zodiac identities or claim semantic decipherment.
"""

import numpy as np
import pandas as pd


class ZodiacDeciphermentOracle:
    """
    Exploratory statistical tools for astronomical-domain analysis.

    Zodiac labels and clock positions are only used when explicit
    metadata exists. They are never fabricated from token structure.
    """

    CANONICAL_ZODIAC = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]

    def __init__(self, corpus_df):
        self.df = corpus_df.copy()

        # Normalize carrier naming so this module works with
        # both older and rebuilt parser output.
        if (
            "carrier" not in self.df.columns
            and "carrier_core" in self.df.columns
        ):
            self.df["carrier"] = self.df["carrier_core"]

        if (
            "carrier_core" not in self.df.columns
            and "carrier" in self.df.columns
        ):
            self.df["carrier_core"] = self.df["carrier"]

        if "carrier_core" not in self.df.columns:
            raise ValueError(
                "Corpus DataFrame requires a "
                "'carrier_core' or 'carrier' column."
            )

        # Derive only broad astronomical-domain membership.
        if "is_astro" not in self.df.columns:
            if "section" in self.df.columns:
                section_text = (
                    self.df["section"]
                    .fillna("")
                    .astype(str)
                    .str.lower()
                )

                self.df["is_astro"] = section_text.str.contains(
                    "astronom|zodiac",
                    regex=True,
                )
            else:
                self.df["is_astro"] = False

        # These fields remain unknown unless the source data
        # explicitly provides them.
        if "zodiac_sign" not in self.df.columns:
            self.df["zodiac_sign"] = None

        if "clock_pos" not in self.df.columns:
            self.df["clock_pos"] = None

    def get_zodiac_carrier_matrix(self, min_freq=1):
        """
        Build a carrier-by-zodiac matrix only when explicit
        zodiac-sign metadata exists.

        No zodiac sign is guessed from folio number or token form.
        """

        explicit = self.df[
            self.df["zodiac_sign"].notna()
        ].copy()

        if explicit.empty:
            return pd.DataFrame()

        explicit = explicit[
            explicit["carrier_core"].notna()
            &
            (explicit["carrier_core"] != "EMPTY")
        ]

        if explicit.empty:
            return pd.DataFrame()

        matrix = pd.crosstab(
            explicit["carrier_core"],
            explicit["zodiac_sign"],
        )

        matrix = matrix[
            matrix.sum(axis=1) >= min_freq
        ]

        if matrix.empty:
            return pd.DataFrame()

        return matrix.sort_index()

    def compute_carrier_astronomical_specificity(
        self,
        min_occurrences=2,
    ):
        """
        Calculate PMI-like specificity between carrier forms and
        broad corpus domains:

            Astronomical
            General_Prose

        Positive values indicate that a carrier occurs more often
        in that domain than expected under independence.
        """

        working = self.df[
            self.df["carrier_core"].notna()
            &
            (self.df["carrier_core"] != "EMPTY")
        ].copy()

        if working.empty:
            return pd.DataFrame()

        working["domain"] = np.where(
            working["is_astro"].fillna(False),
            "Astronomical",
            "General_Prose",
        )

        contingency = pd.crosstab(
            working["carrier_core"],
            working["domain"],
        )

        contingency = contingency[
            contingency.sum(axis=1)
            >= min_occurrences
        ]

        if contingency.empty:
            return pd.DataFrame()

        total = contingency.to_numpy().sum()

        p_carrier = (
            contingency.sum(axis=1).to_numpy()
            / total
        )

        p_domain = (
            contingency.sum(axis=0).to_numpy()
            / total
        )

        p_joint = (
            contingency.to_numpy()
            / total
        )

        expected = np.outer(
            p_carrier,
            p_domain,
        )

        pmi = np.log2(
            (p_joint + 1e-12)
            /
            (expected + 1e-12)
        )

        return pd.DataFrame(
            pmi,
            index=contingency.index,
            columns=contingency.columns,
        ).round(3)

    def top_astronomical_carriers(self, limit=30):
        """
        Return the most frequent carrier forms in rows marked as
        astronomical-domain material.
        """

        astro = self.df[
            self.df["is_astro"].fillna(False)
            &
            self.df["carrier_core"].notna()
            &
            (self.df["carrier_core"] != "EMPTY")
        ].copy()

        if astro.empty:
            return pd.DataFrame(
                columns=[
                    "carrier_core",
                    "occurrences",
                ]
            )

        counts = (
            astro["carrier_core"]
            .value_counts()
            .head(limit)
            .rename_axis("carrier_core")
            .reset_index(name="occurrences")
        )

        return counts