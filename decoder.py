"""
voynich-state-viewer: Zodiac Topological Grounding Oracle (f70r-f74v)
Aligns stripped carrier stems against the physical circular geometry of the 12 signs.
"""

import math
import re
from collections import Counter
import numpy as np
import pandas as pd


class ZodiacDeciphermentOracle:
    def __init__(self, corpus_df: pd.DataFrame):
        self.df = corpus_df.copy()
        if "clean" not in self.df.columns and "token" in self.df.columns:
            self.df["clean"] = self.df["token"].astype(str)
        if "carrier_core" not in self.df.columns:
            self.df["carrier_core"] = self.df["clean"].apply(self._extract_carrier)

    @staticmethod
    def _extract_carrier(tok: str) -> str:
        s = str(tok).lower().strip()
        for p in ("qk", "dk", "qo", "ch", "sh", "q", "k", "d", "t"):
            if s.startswith(p):
                s = s[len(p):]
                break
        for ep in ("aiiin", "aiin", "ain", "eedy", "edy", "eey", "ey", "al", "ar", "am", "or", "ol", "m", "y"):
            if s.endswith(ep):
                s = s[:-len(ep)]
                break
        return s if s else "core"

    def compute_carrier_astronomical_specificity(self, min_occ: int = 3) -> pd.DataFrame:
        """
        Calculates Pointwise Mutual Information (PMI) of carrier cores in Astronomical/Zodiac
        sections relative to the general corpus.
        """
        valid = self.df[self.df["carrier_core"] != "core"].copy()
        if "section" not in valid.columns:
            return pd.DataFrame()

        total_tokens = len(valid)
        carrier_counts = valid["carrier_core"].value_counts()
        astro_mask = valid["section"].astype(str).str.contains("Astro|Zodiac", case=False, na=False)
        astro_tokens = valid[astro_mask]

        total_astro = len(astro_tokens)
        if total_astro == 0:
            return pd.DataFrame()

        results = []
        for carrier, count in carrier_counts.items():
            if count < min_occ:
                continue
            astro_count = (astro_tokens["carrier_core"] == carrier).sum()
            if astro_count == 0:
                continue

            p_carrier = count / total_tokens
            p_astro = total_astro / total_tokens
            p_joint = astro_count / total_tokens

            pmi = math.log2(p_joint / (p_carrier * p_astro))
            results.append({
                "Carrier Core (Lambda)": carrier,
                "Astro Count": astro_count,
                "Total Count": count,
                "Astronomical PMI": round(pmi, 3)
            })

        res_df = pd.DataFrame(results)
        if not res_df.empty:
            res_df = res_df.sort_values(by="Astronomical PMI", ascending=False).reset_index(drop=True)
        return res_df

    def decode_zodiac_labels(self) -> pd.DataFrame:
        """
        Extracts candidate isolated label strings from folios f70r through f74v.
        """
        zodiac_folios = [f"f{i}r" for i in range(70, 75)] + [f"f{i}v" for i in range(70, 75)]
        zodiac_df = self.df[self.df["folio"].isin(zodiac_folios)].copy()

        if zodiac_df.empty:
            return pd.DataFrame()

        # Labels are typically short lines (1-3 tokens) or ring-annotated loci
        records = []
        group_col = "header" if "header" in zodiac_df.columns else "folio"
        for locus, grp in zodiac_df.groupby(group_col):
            tokens = grp["clean"].tolist()
            if 1 <= len(tokens) <= 3:
                records.append({
                    "Locus / Ring Slot": locus,
                    "Tokens": " ".join(tokens),
                    "Carrier Stems": " ".join(grp["carrier_core"].tolist()),
                    "Token Count": len(tokens)
                })

        label_df = pd.DataFrame(records)
        return label_df.head(25) if not label_df.empty else pd.DataFrame()
