"""
Statistical evidence tools for Voynich token structure.

These functions measure corpus patterns.
They do not claim semantic decipherment.
"""

import random

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

        if "clean" not in self.df.columns:
            if "token" in self.df.columns:
                self.df["clean"] = self.df["token"].astype(str)
            else:
                self.df["clean"] = self.df["carrier_core"].astype(str)

        if "folio" not in self.df.columns:
            self.df["folio"] = "unknown"

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
                    lambda values: ", ".join(pd.unique(values)[:5]),
                ),
                sections=(
                    "section",
                    lambda values: ", ".join(pd.unique(values)),
                ),
                folios=(
                    "folio",
                    lambda values: ", ".join(pd.unique(values)[:8]),
                ),
            )
            .sort_values("occurrences", ascending=False)
            .reset_index()
        )

        return result

    def compute_carrier_excess_specificity(self, min_occurrences=5):

        valid = self.df[self.df["carrier_core"] != "EMPTY"].copy()
        if valid.empty:
            return pd.DataFrame()

        contingency = pd.crosstab(valid["carrier_core"], valid["section"])
        contingency = contingency[contingency.sum(axis=1) >= min_occurrences]
        if contingency.empty:
            return pd.DataFrame()

        total = contingency.to_numpy().sum()
        p_carrier = contingency.sum(axis=1).to_numpy() / total
        p_section = contingency.sum(axis=0).to_numpy() / total
        p_joint = contingency.to_numpy() / total
        expected = np.outer(p_carrier, p_section)
        pmi = np.log2((p_joint + 1e-12) / (expected + 1e-12))

        return pd.DataFrame(
            pmi,
            index=contingency.index,
            columns=contingency.columns,
        ).round(3)

    def audit_successor_routing(self):

        valid = self.df[
            self.df["exit_port"].isin(["al", "ar", "y", "aiin", "aiiin"])
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

        if "next_state" not in self.df.columns or "state" not in self.df.columns:
            return pd.DataFrame()

        valid = self.df[self.df["next_state"].notna()]
        if valid.empty:
            return pd.DataFrame()

        return pd.crosstab(
            valid["state"],
            valid["next_state"],
            normalize="index",
        ).round(4)

    def top_section_carriers(self, section_name, limit=20):
        valid = self.df[
            (self.df["section"] == section_name)
            &
            (self.df["carrier_core"] != "EMPTY")
        ]
        if valid.empty:
            return pd.DataFrame(columns=["carrier_core", "occurrences"])

        return (
            valid["carrier_core"]
            .value_counts()
            .head(limit)
            .rename_axis("carrier_core")
            .reset_index(name="occurrences")
        )

    def run_null_model(self, n_shuffles=50, min_occurrences=5):
        real_pmi = self.compute_carrier_excess_specificity(min_occurrences=min_occurrences)
        if real_pmi.empty:
            return None

        real_max = float(real_pmi.abs().to_numpy().max())
        carriers = self.df["carrier_core"].tolist()
        shuffled_maxes = []

        for _ in range(n_shuffles):
            shuffled = self.df.copy()
            shuffled["carrier_core"] = random.sample(carriers, len(carriers))
            temp = DeciphermentEngine(shuffled)
            fake = temp.compute_carrier_excess_specificity(min_occurrences=min_occurrences)
            if not fake.empty:
                shuffled_maxes.append(float(fake.abs().to_numpy().max()))

        if not shuffled_maxes:
            return None

        return {
            "real_max_pmi": round(real_max, 3),
            "shuffled_mean": round(float(np.mean(shuffled_maxes)), 3),
            "shuffled_max": round(float(max(shuffled_maxes)), 3),
            "n_shuffles": len(shuffled_maxes),
            "beats_chance": real_max > max(shuffled_maxes),
        }

    def run_folio_holdout(self, holdout_frac=0.2, seed=42, min_occurrences=5):
        folios = sorted(self.df["folio"].dropna().unique().tolist())
        if len(folios) < 5:
            return None

        rng = random.Random(seed)
        shuffled_folios = folios[:]
        rng.shuffle(shuffled_folios)
        cut = max(1, int(len(shuffled_folios) * holdout_frac))
        test_folios = set(shuffled_folios[:cut])
        train_folios = set(shuffled_folios[cut:])

        train_df = self.df[self.df["folio"].isin(train_folios)].copy()
        test_df = self.df[self.df["folio"].isin(test_folios)].copy()
        if train_df.empty or test_df.empty:
            return None

        train_pmi = DeciphermentEngine(train_df).compute_carrier_excess_specificity(min_occurrences=min_occurrences)
        test_pmi = DeciphermentEngine(test_df).compute_carrier_excess_specificity(min_occurrences=max(2, min_occurrences // 2))

        if train_pmi.empty or test_pmi.empty:
            return {
                "train_folios": len(train_folios),
                "test_folios": len(test_folios),
                "holdout_holds": False,
                "note": "Not enough overlapping carriers after the split.",
            }

        shared = sorted(set(train_pmi.index) & set(test_pmi.index))
        train_max = float(train_pmi.abs().to_numpy().max())
        test_max = float(test_pmi.abs().to_numpy().max())

        return {
            "train_folios": len(train_folios),
            "test_folios": len(test_folios),
            "shared_carriers": len(shared),
            "train_max_pmi": round(train_max, 3),
            "test_max_pmi": round(test_max, 3),
            "holdout_holds": test_max >= (train_max * 0.5),
            "note": "Holdout holds if unseen folios keep at least half the train PMI strength.",
        }