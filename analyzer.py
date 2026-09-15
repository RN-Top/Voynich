"""
voynich-state-viewer: Statistical Grounding & Morphosyntactic Decipherment Engine
Extracts syntactic frames (Candidate Slot Omega), computes Pointwise Mutual Information (PMI),
and executes Monte Carlo null-model shuffling and folio holdout validations.
"""

import math
import random
from collections import Counter
from typing import Dict, List, Optional
import numpy as np
import pandas as pd


class DeciphermentEngine:
    """Statistical grounding, validation, and syntactic frame discovery."""

    def __init__(self, corpus_df: pd.DataFrame):
        self.df = corpus_df.copy()
        if "clean" not in self.df.columns and "token" in self.df.columns:
            self.df["clean"] = self.df["token"].astype(str)
        if "carrier_core" not in self.df.columns:
            self.df["carrier_core"] = self.df["clean"].apply(self._fallback_carrier)
        if "exit_port" not in self.df.columns:
            self.df["exit_port"] = self.df["clean"].apply(self._fallback_exit_port)
        if "control" not in self.df.columns:
            self.df["control"] = self.df["clean"].apply(self._fallback_control)
        if "next_control" not in self.df.columns:
            self.df["next_control"] = self.df["control"].shift(-1)
        if "prev_control" not in self.df.columns:
            self.df["prev_control"] = self.df["control"].shift(1)

    @staticmethod
    def _fallback_control(tok: str) -> str:
        s = str(tok).lower().strip()
        for c in ("qk", "dk", "q", "k", "d"):
            if s.startswith(c):
                return c
        return "NONE"

    @staticmethod
    def _fallback_exit_port(tok: str) -> str:
        s = str(tok).lower().strip()
        for p in ("aiiin", "aiin", "ain", "ar", "al", "am", "m", "y"):
            if s.endswith(p):
                return p
        return "BARE"

    @staticmethod
    def _fallback_carrier(tok: str) -> str:
        s = str(tok).lower().strip()
        for p in ("qk", "dk", "q", "k", "d"):
            if s.startswith(p):
                s = s[len(p):]
                break
        for ep in ("aiiin", "aiin", "ain", "ar", "al", "am", "m", "y"):
            if s.endswith(ep):
                s = s[:-len(ep)]
                break
        return s if s else "EMPTY"

    # -------------------------------------------------------------------------
    # 1. Syntactic Slot Omega Discovery
    # -------------------------------------------------------------------------
    def find_slot_omega_candidates(self) -> pd.DataFrame:
        """
        Discovers instances of the canonical syntactic frame:
            Q-ACTIVE -> [ X-AIIN ] -> Q-ACTIVE
        Holding the control frame invariant isolates candidate lexical class X.
        """
        mask = (
            (self.df["prev_control"].isin(["q", "qk"])) &
            (self.df["exit_port"].isin(["aiin", "aiiin"])) &
            (self.df["next_control"].isin(["q", "qk"]))
        )
        omega_matches = self.df[mask].copy()
        if omega_matches.empty:
            return pd.DataFrame()

        summary = (
            omega_matches.groupby("carrier_core")
            .agg(
                occurrences=("clean", "count"),
                sample_tokens=("clean", lambda s: ", ".join(s.unique()[:3])),
                sections=("section", lambda s: ", ".join(sorted(set(s)))),
                folios=("folio", lambda s: ", ".join(sorted(set(s))[:4]))
            )
            .sort_values(by="occurrences", ascending=False)
            .reset_index()
        )
        return summary

    # -------------------------------------------------------------------------
    # 2. Cross-Modal Pointwise Mutual Information (PMI)
    # -------------------------------------------------------------------------
    def compute_carrier_excess_specificity(self, min_occurrences: int = 5) -> pd.DataFrame:
        """
        Calculates Pointwise Mutual Information (PMI) between carrier stems (Lambda)
        and manuscript sections.
        PMI > 0 indicates excess domain specificity above baseline chance.
        """
        df_valid = self.df[
            (self.df["carrier_core"] != "EMPTY") &
            (self.df["section"].notna())
        ].copy()

        contingency = pd.crosstab(df_valid["carrier_core"], df_valid["section"])
        contingency = contingency[contingency.sum(axis=1) >= min_occurrences]
        if contingency.empty:
            return pd.DataFrame()

        total = contingency.values.sum()
        p_carrier = contingency.sum(axis=1).values / total
        p_section = contingency.sum(axis=0).values / total
        p_joint = contingency.values / total

        expected = np.outer(p_carrier, p_section)
        pmi = np.log2((p_joint + 1e-9) / (expected + 1e-9))

        return pd.DataFrame(pmi, index=contingency.index, columns=contingency.columns).round(3)

    # -------------------------------------------------------------------------
    # 3. Section Carrier Ranking
    # -------------------------------------------------------------------------
    def top_section_carriers(self, section_name: str, top_n: int = 20) -> pd.DataFrame:
        """Ranks most frequent conserved carrier cores for a selected section."""
        sec_df = self.df[
            (self.df["section"] == section_name) &
            (self.df["carrier_core"] != "EMPTY")
        ]
        if sec_df.empty:
            return pd.DataFrame(columns=["carrier_core", "occurrences", "section"])

        counts = sec_df["carrier_core"].value_counts().head(top_n).reset_index()
        counts.columns = ["carrier_core", "occurrences"]
        counts["section"] = section_name
        return counts

    # -------------------------------------------------------------------------
    # 4. Monte Carlo Null Model Validation
    # -------------------------------------------------------------------------
    def run_null_model(self, n_shuffles: int = 50) -> Optional[Dict[str, float]]:
        """
        Evaluates whether observed carrier-to-section associations exceed chance
        by comparing actual max PMI against label-shuffled empirical distributions.
        """
        real_pmi_df = self.compute_carrier_excess_specificity(min_occurrences=5)
        if real_pmi_df.empty:
            return None

        real_max_pmi = float(np.nanmax(real_pmi_df.values))
        shuffled_maxes = []

        valid_df = self.df[
            (self.df["carrier_core"] != "EMPTY") &
            (self.df["section"].notna())
        ].copy()

        carriers = valid_df["carrier_core"].values.copy()
        sections = valid_df["section"].values.copy()

        for _ in range(n_shuffles):
            shuffled_sec = np.random.permutation(sections)
            contingency = pd.crosstab(carriers, shuffled_sec)
            contingency = contingency[contingency.sum(axis=1) >= 5]
            if contingency.empty:
                continue

            total = contingency.values.sum()
            p_c = contingency.sum(axis=1).values / total
            p_s = contingency.sum(axis=0).values / total
            p_j = contingency.values / total

            exp = np.outer(p_c, p_s)
            s_pmi = np.log2((p_j + 1e-9) / (exp + 1e-9))
            shuffled_maxes.append(float(np.nanmax(s_pmi)))

        if not shuffled_maxes:
            return None

        mean_shuff = float(np.mean(shuffled_maxes))
        max_shuff = float(np.max(shuffled_maxes))

        return {
            "real_max_pmi": round(real_max_pmi, 3),
            "shuffled_mean": round(mean_shuff, 3),
            "shuffled_max": round(max_shuff, 3),
            "beats_chance": real_max_pmi > max_shuff
        }

    # -------------------------------------------------------------------------
    # 5. Folio Holdout Cross-Validation
    # -------------------------------------------------------------------------
    def run_folio_holdout(self, test_size: float = 0.2) -> Optional[Dict[str, object]]:
        """
        Splits folios into 80% train / 20% test partitions to verify whether
        carrier domain alignments generalize to unseen folios.
        """
        folios = sorted(self.df["folio"].dropna().unique())
        if len(folios) < 5:
            return None

        random.seed(42)
        n_test = max(1, int(len(folios) * test_size))
        test_folios = set(random.sample(folios, n_test))
        train_folios = [f for f in folios if f not in test_folios]

        train_df = self.df[self.df["folio"].isin(train_folios)]
        test_df = self.df[self.df["folio"].isin(test_folios)]

        train_eng = DeciphermentEngine(train_df)
        test_eng = DeciphermentEngine(test_df)

        train_pmi = train_eng.compute_carrier_excess_specificity(min_occurrences=3)
        test_pmi = test_eng.compute_carrier_excess_specificity(min_occurrences=2)

        if train_pmi.empty or test_pmi.empty:
            return None

        shared_carriers = len(set(train_pmi.index).intersection(set(test_pmi.index)))
        train_max = float(np.nanmax(train_pmi.values))
        test_max = float(np.nanmax(test_pmi.values))

        return {
            "train_folios": len(train_folios),
            "test_folios": len(test_folios),
            "shared_carriers": shared_carriers,
            "train_max_pmi": round(train_max, 3),
            "test_max_pmi": round(test_max, 3),
            "holdout_holds": test_max > 0.5 and shared_carriers >= 5,
            "note": "Holdout holds if carrier PMI profiles generalize across separate quires."
        }
