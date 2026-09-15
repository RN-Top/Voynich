"""
voynich-state-viewer: Astronomical Grounding & Zodiac Decipherment Oracle
Bridges normalized carrier stems to the 12-fold celestial zodiac rotas.
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
        if "carrier_core" not in self.df.columns:
            self.df["carrier_core"] = self.df["clean"].astype(str)

        # Flag astronomical and zodiac folios
        self.df["is_astro"] = self.df["section"].isin(["Astronomical/Zodiac", "Cosmological"])
        self.df["zodiac_sign"] = self.df["folio"].apply(self._infer_zodiac_sign)

    @staticmethod
    def _infer_zodiac_sign(folio: str) -> str:
        f = str(folio).lower().strip()
        z_map = {
            "f70v1": "Aries", "f70v2": "Aries",
            "f71r": "Taurus", "f71v": "Taurus",
            "f72r1": "Gemini", "f72r2": "Cancer", "f72r3": "Cancer",
            "f72v1": "Libra", "f72v2": "Virgo", "f72v3": "Leo",
            "f73r": "Scorpio", "f73v": "Sagittarius",
            "f74r": "Capricorn", "f74v": "Aquarius"
        }
        for k, v in z_map.items():
            if k in f:
                return v
        return "Unknown"

    def get_zodiac_carrier_matrix(self, min_freq: int = 2) -> pd.DataFrame:
        """Cross-tabulates isolated carriers across canonical Zodiac signs."""
        z_df = self.df[self.df["zodiac_sign"].isin(self.ZODIAC_CANONICAL)].copy()
        if z_df.empty:
            return pd.DataFrame()

        ct = pd.crosstab(z_df["carrier_core"], z_df["zodiac_sign"])
        ct = ct[ct.sum(axis=1) >= min_freq]
        ordered_cols = [c for c in self.ZODIAC_CANONICAL if c in ct.columns]
        return ct.reindex(columns=ordered_cols)

    def compute_carrier_astronomical_specificity(self) -> pd.DataFrame:
        """Computes PMI of carriers in Astronomical folios vs general prose."""
        valid = self.df[self.df["carrier_core"] != "EMPTY"].copy()
        valid["domain"] = np.where(valid["is_astro"], "Astronomical", "General_Prose")

        contingency = pd.crosstab(valid["carrier_core"], valid["domain"])
        contingency = contingency[contingency.sum(axis=1) >= 5]
        if contingency.empty:
            return pd.DataFrame()

        total = contingency.values.sum()
        p_c = contingency.sum(axis=1).values / total
        p_d = contingency.sum(axis=0).values / total
        p_joint = contingency.values / total

        expected = np.outer(p_c, p_d)
        pmi = np.log2((p_joint + 1e-9) / (expected + 1e-9))
        pmi_df = pd.DataFrame(pmi, index=contingency.index, columns=contingency.columns)
        return pmi_df.sort_values(by="Astronomical", ascending=False).round(3)

    def decode_zodiac_labels(self) -> pd.DataFrame:
        """Extracts high-confidence astronomical carriers (OTCHEOD, OEEOD, AIR, AL, OTEOD)."""
        z_df = self.df[self.df["zodiac_sign"].isin(self.ZODIAC_CANONICAL)].copy()
        if z_df.empty:
            return pd.DataFrame()

        key_carriers = ("otcheod", "oeeod", "opair", "oteod", "air", "al", "aiir")
        targeted = z_df[z_df["carrier_core"].isin(key_carriers)].copy()
        cols = [c for c in ["folio", "header", "zodiac_sign", "clean", "carrier_core", "control", "exit_port"] if c in targeted.columns]
        return targeted[cols].drop_duplicates()
