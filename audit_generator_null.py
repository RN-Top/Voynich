"""
voynich-state-viewer: Clean-Room Generator Null Falsification Engine
Benchmarks real manuscript transition constraints (A3/A4) against
Timm & Schinner self-citation pseudotext models.
"""

import random
from collections import Counter
from typing import Dict, List
import numpy as np
import pandas as pd


class GeneratorNullAudit:
    """Tests if A3/A4 transition rules can be produced by mechanical pseudotext."""

    def __init__(self, corpus_df: pd.DataFrame):
        self.df = corpus_df.copy()

    def run_generator_benchmark(self, n_simulations: int = 50) -> Dict[str, object]:
        """
        Simulates Timm & Schinner self-citation pseudotext and compares
        successor routing specificity P(C_{n+1} | rho_n).
        """
        valid = self.df[
            self.df["exit_port"].isin(["al", "ar"]) &
            self.df["next_control"].notna()
        ].copy()

        if valid.empty:
            return {"error": "Insufficient successor transitions."}

        # Real manuscript transition asymmetry
        real_ct = pd.crosstab(valid["exit_port"], valid["next_control"], normalize="index")
        real_diff = 0.0
        if "al" in real_ct.index and "ar" in real_ct.index:
            real_diff = float(np.abs(real_ct.loc["al"] - real_ct.loc["ar"]).sum())

        # Simulated self-citation null generation
        vocab = self.df["clean"].dropna().tolist()
        sim_diffs = []

        for _ in range(n_simulations):
            memory_pool = vocab[:50]
            pseudo_tokens = []
            for _ in range(len(valid)):
                if random.random() < 0.7 and memory_pool:
                    chosen = random.choice(memory_pool)
                else:
                    chosen = random.choice(vocab)
                    memory_pool.append(chosen)
                    if len(memory_pool) > 100:
                        memory_pool.pop(0)
                pseudo_tokens.append(chosen)

            pseudo_series = pd.Series(pseudo_tokens)
            p_exit = pseudo_series.apply(lambda s: "al" if s.endswith("al") else ("ar" if s.endswith("ar") else "other"))
            p_next = pseudo_series.shift(-1).apply(lambda s: "q" if str(s).startswith("q") else "other")

            df_sim = pd.DataFrame({"exit": p_exit, "next": p_next}).dropna()
            df_sim = df_sim[df_sim["exit"].isin(["al", "ar"])]

            if not df_sim.empty and len(df_sim["exit"].unique()) > 1:
                sim_ct = pd.crosstab(df_sim["exit"], df_sim["next"], normalize="index")
                if "al" in sim_ct.index and "ar" in sim_ct.index:
                    sim_diff = float(np.abs(sim_ct.loc["al"] - sim_ct.loc["ar"]).sum())
                    sim_diffs.append(sim_diff)

        mean_sim = float(np.mean(sim_diffs)) if sim_diffs else 0.0
        max_sim = float(np.max(sim_diffs)) if sim_diffs else 0.0

        return {
            "real_asymmetry_score": round(real_diff, 4),
            "synthetic_mean_score": round(mean_sim, 4),
            "synthetic_max_score": round(max_sim, 4),
            "falsifies_generator": real_diff > max_sim,
            "verdict": "GENUINE SYNTAX" if real_diff > max_sim else "MECHANICAL PSEUDOTEXT"
        }
