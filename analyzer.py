"""
voynich-state-viewer: Statistical Grounding & Decipherment Engine
Extracts syntactic content slots (Slot Omega) and measures carrier specificity
against illustrated manuscript sections.
"""

import numpy as np
import pandas as pd


class DeciphermentEngine:
    """Statistical alignment tools to evaluate carrier candidates."""

    def __init__(self, corpus_df: pd.DataFrame):
        self.df = corpus_df.copy()

    def find_slot_omega_candidates(self) -> pd.DataFrame:
        """
        Discovers instances of the canonical syntactic frame:
            Q-ACTIVE -> [ X-AIIN ] -> Q-ACTIVE
        Holding the control frame invariant isolates the carrier class X.
        """
        # A token matches Slot Omega if:
        # 1. Previous token starts with Q-control
        # 2. Current token has exit port 'aiin' or 'aiiin'
        # 3. Next token starts with Q-control
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
                occurrences=("token", "count"),
                sample_tokens=("clean", lambda s: ", ".join(s.unique()[:3])),
                sections=("section", lambda s: ", ".join(s.unique())),
                folios=("folio", lambda s: ", ".join(s.unique()[:4]))
            )
            .sort_values(by="occurrences", ascending=False)
            .reset_index()
        )
        return summary

    def compute_carrier_excess_specificity(self, min_occurrences: int = 5) -> pd.DataFrame:
        """
        Calculates Pointwise Mutual Information (PMI) between carrier stems (Lambda)
        and manuscript sections.
        PMI > 0 indicates excess domain specificity above chance.
        """
        df_valid = self.df[self.df["carrier_core"] != "EMPTY"].copy()
        contingency = pd.crosstab(df_valid["carrier_core"], df_valid["section"])

        # Filter low-frequency carriers
        contingency = contingency[contingency.sum(axis=1) >= min_occurrences]
        if contingency.empty:
            return pd.DataFrame()

        # Probabilities
        total = contingency.values.sum()
        p_carrier = contingency.sum(axis=1).values / total
        p_section = contingency.sum(axis=0).values / total
        p_joint = contingency.values / total

        expected = np.outer(p_carrier, p_section)
        # Pointwise Mutual Information
        pmi = np.log2((p_joint + 1e-9) / (expected + 1e-9))

        pmi_df = pd.DataFrame(pmi, index=contingency.index, columns=contingency.columns)
        return pmi_df.round(3)

    def audit_successor_routing(self) -> pd.DataFrame:
        """
        Calculates conditional routing probabilities P(C_{n+1} | rho_n).
        Measures the empirical A4 successor routing effect (-al vs -ar).
        """
        valid = self.df[
            self.df["exit_port"].isin(["al", "ar", "y", "aiin"]) &
            self.df["next_control"].notna()
        ]
        if valid.empty:
            return pd.DataFrame()

        ct = pd.crosstab(valid["exit_port"], valid["next_control"], normalize="index")
        return ct.round(4)
