"""
voynich-state-viewer: Astronomical Alignment & Grounded Decipherment Oracle
Bridges normalized morphological carriers to the 12-fold celestial zodiac grid.
"""

import numpy as np
import pandas as pd


class ZodiacDeciphermentOracle:
    """Empirical alignment solver between isolated carriers and celestial structures."""

    ZODIAC_CANONICAL = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    def __init__(self, corpus_df: pd.DataFrame):
        self.df = corpus_df.copy()

    def get_zodiac_carrier_matrix(self, min_freq: int = 3) -> pd.DataFrame:
        """
        Cross-tabulates isolated lexical carriers (Lambda) across canonical Zodiac folios.
        Identifies stable celestial nouns vs variable grammatical noise.
        """
        z_df = self.df[self.df["zodiac_sign"].isin(self.ZODIAC_CANONICAL)].copy()
        if z_df.empty:
            return pd.DataFrame()

        # Isolate carriers with sufficient frequency across zodiac folios
        ct = pd.crosstab(z_df["carrier"], z_df["zodiac_sign"])
        ct = ct[ct.sum(axis=1) >= min_freq]

        # Reindex columns in true astronomical order
        ordered_cols = [c for c in self.ZODIAC_CANONICAL if c in ct.columns]
        ct = ct.reindex(columns=ordered_cols)
        return ct

    def compute_carrier_astronomical_specificity(self) -> pd.DataFrame:
        """
        Computes Pointwise Mutual Information (PMI) of carriers in Astronomical folios
        versus the rest of the manuscript.
        High PMI (>1.0) isolates vocabulary specific to celestial clockwork.
        """
        valid = self.df[self.df["carrier"] != "EMPTY"].copy()
        valid["domain"] = np.where(valid["is_astro"], "Astronomical", "General_Prose")

        contingency = pd.crosstab(valid["carrier"], valid["domain"])
        contingency = contingency[contingency.sum(axis=1) >= 5]

        total = contingency.values.sum()
        p_carrier = contingency.sum(axis=1).values / total
        p_domain = contingency.sum(axis=0).values / total
        p_joint = contingency.values / total

        expected = np.outer(p_carrier, p_domain)
        pmi = np.log2((p_joint + 1e-9) / (expected + 1e-9))

        pmi_df = pd.DataFrame(pmi, index=contingency.index, columns=contingency.columns)
        return pmi_df.sort_values(by="Astronomical", ascending=False).round(3)

    def decode_zodiac_labels(self) -> pd.DataFrame:
        """
        Extracts high-confidence astronomical nouns (e.g. OTCHEOD, OEEOD, OPAIR)
        along with their realization parameters and physical clock/ring positions.
        """
        z_df = self.df[self.df["zodiac_sign"].isin(self.ZODIAC_CANONICAL)].copy()
        if z_df.empty:
            return pd.DataFrame()

        # Filter for the conserved astronomical carrier candidates
        key_carriers = ("otcheod", "oeeod", "opair", "oteod", "otod")
        targeted = z_df[z_df["carrier"].isin(key_carriers)].copy()

        summary = targeted[[
            "folio", "zodiac_sign", "clock_pos", "raw", "clean", 
            "carrier", "control", "exit_port"
        ]].drop_duplicates()
        return summary
