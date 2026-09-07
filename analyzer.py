"""
Statistical evidence tools for Voynich token structure.

These functions measure corpus patterns.
They do not claim semantic decipherment.
"""

import numpy as np
import pandas as pd

class DeciphermentEngine:

    def __init__(self, corpus_df):
        self.df = corpus_df.copy()

        required = {
            "carrier_core",
            "section",
            "control",
            "prev_control",
            "next_control",
            "exit_port",
        }

        missing = sorted(
            required - set(self.df.columns)
        )

        if missing:
            raise ValueError(
                "Corpus DataFrame is missing "
                f"required columns: {missing}"
            )

    def find_slot_omega_candidates(self):

        mask = (
            self.df["prev_control"].isin(
                ["q", "qk"]
            )
            &
            self.df["exit_port"].isin(
                ["aiin", "aiiin"]
            )
            &
            self.df["next_control"].isin(
                ["q", "qk"]
            )
        )

        matches = self.df.loc[mask].copy()

        if matches.empty:
            return pd.DataFrame()

        result = (
            matches
            .groupby("carrier_core")
            .agg(
                occurrences=("clean", "count"),

                sample_tokens=(
                    "clean",
                    lambda values:
                    ", ".join(
                        pd.unique(values)[:5]
                    ),
                ),

                sections=(
                    "section",
                    lambda values:
                    ", ".join(
                        pd.unique(values)
                    ),
                ),

                folios=(
                    "folio",
                    lambda values:
                    ", ".join(
                        pd.unique(values)[:8]
                    ),
                ),
            )
            .sort_values(
                "occurrences",
                ascending=False,
            )
            .reset_index()
        )

        return result

    def compute_carrier_excess_specificity(
        self,
        min_occurrences=5,
    ):

        valid = self.df[
            self.df["carrier_core"] != "EMPTY"
        ].copy()

        if valid.empty:
            return pd.DataFrame()

        contingency = pd.crosstab(
            valid["carrier_core"],
            valid["section"],
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

        p_section = (
            contingency.sum(axis=0).to_numpy()
            / total
        )

        p_joint = (
            contingency.to_numpy()
            / total
        )

        expected = np.outer(
            p_carrier,
            p_section,
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

    def audit_successor_routing(self):

        valid = self.df[
            self.df["exit_port"].isin(
                [
                    "al",
                    "ar",
                    "y",
                    "aiin",
                    "aiiin",
                ]
            )
            &
            self.df["next_control"].notna()
        ]

        if valid.empty:
            return pd.DataFrame()

        return pd.crosstab(
            valid["exit_port"],
            valid["next_control"],
            normalize="index",
        ).round(4)

    def state_transition_matrix(self):

        valid = self.df[
            self.df["next_state"].notna()
        ]

        if valid.empty:
            return pd.DataFrame()

        return pd.crosstab(
            valid["state"],
            valid["next_state"],
            normalize="index",
        ).round(4)