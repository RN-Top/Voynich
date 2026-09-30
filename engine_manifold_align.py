"""
VOYNICH CROSS-LINGUAL CO-OCCURRENCE MANIFOLD ALIGNER
Solves the Unsupervised Orthogonal Procrustes alignment between high-density
Voynich carrier cores and 15th-century historical Latin/German technical corpora.
Uses pure NumPy/Pandas (zero external C-library crashes on Streamlit Cloud).
"""

import re
import os
from collections import Counter
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


# -----------------------------------------------------------------------------
# 1. HISTORICAL TARGET CORPORA
# -----------------------------------------------------------------------------
# An earlier version of this module generated the "historical" target
# manifolds with np.random.randn() and attached Latin lemma labels to them.
# Aligning to random geometry cannot show resemblance to any real text, and
# with 10 anchors in 16 dimensions an orthogonal map fits almost any target,
# so the reported 99.79% congruence was an artefact. That claim is withdrawn.
#
# Target spaces must now be built from real, tokenised historical text
# (e.g. a transcription of Macer Floridus), passed in by the caller.
MIN_ANCHORS_PER_DIM = 3

# -----------------------------------------------------------------------------
# 2. PURE NUMPY ORTHOGONAL PROCRUSTES SOLVER
# -----------------------------------------------------------------------------
def orthogonal_procrustes(A: np.ndarray, B: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Finds orthogonal rotation matrix W minimizing ||A W - B||_F.
    Returns optimal rotation W and normalized squared disparity d^2.
    """
    A_cen = A - np.mean(A, axis=0)
    B_cen = B - np.mean(B, axis=0)

    norm_A = np.linalg.norm(A_cen)
    norm_B = np.linalg.norm(B_cen)

    if norm_A == 0 or norm_B == 0:
        return np.eye(A.shape[1]), 1.0

    A_norm = A_cen / norm_A
    B_norm = B_cen / norm_B

    M = np.dot(B_norm.T, A_norm)
    U, s, Vt = np.linalg.svd(M)
    W = np.dot(U, Vt)

    if np.linalg.det(W) < 0:
        Vt[-1, :] *= -1
        s[-1] *= -1
        W = np.dot(U, Vt)

    trace_s = np.sum(s)
    d2 = max(0.0, 1.0 - (trace_s ** 2))
    return W, d2


# -----------------------------------------------------------------------------
# 3. HIGH-DIMENSIONAL PPMI EMBEDDING GENERATOR
# -----------------------------------------------------------------------------
def clean_stem(token: str) -> str:
    w = re.sub(r"[{}\\[\\]<!>]", "", str(token).lower().strip())
    w = re.sub(r"^(qk|dk|qok|qot|qop|qo|ok|ot|op|da|ch|sh)", "", w)
    w = re.sub(r"(aiiin|aiin|ain|eedy|edy|eey|ey|al|ar|am|or|ol|m|y)$", "", w)
    return w if w else token

def build_ppmi_space(tokens: List[str], max_vocab: int = 200, dim: int = 16, window: int = 3):
    """Constructs a Positive Pointwise Mutual Information continuous vector space."""
    clean_tokens = [clean_stem(t) for t in tokens if str(t).strip()]
    counts = Counter(clean_tokens)
    vocab = [w for w, c in counts.most_common(max_vocab) if len(w) >= 2]
    w2i = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)

    if V < 5:
        raise ValueError(f"Corpus too small for a PPMI space ({V} usable types).")

    cooc = np.zeros((V, V), dtype=np.float32)
    for idx, w in enumerate(clean_tokens):
        if w not in w2i:
            continue
        left = max(0, idx - window)
        right = min(len(clean_tokens), idx + window + 1)
        for c_idx in range(left, right):
            if c_idx != idx and clean_tokens[c_idx] in w2i:
                cooc[w2i[w], w2i[clean_tokens[c_idx]]] += 1.0

    # Smooth co-occurrences
    cooc += 1e-4
    total = cooc.sum()
    p_row = cooc.sum(axis=1, keepdims=True)
    p_col = cooc.sum(axis=0, keepdims=True)
    expected = np.outer(p_row, p_col) / total
    ppmi = np.maximum(0, np.log2(cooc / expected))

    # Low-rank projection via Truncated SVD
    u, s, _ = np.linalg.svd(ppmi, full_matrices=False)
    eff_dim = min(dim, V)
    vecs = u[:, :eff_dim] * np.sqrt(s[:eff_dim])
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    vecs = np.divide(vecs, norms, out=np.zeros_like(vecs), where=norms > 0)

    return vocab, vecs, w2i


# -----------------------------------------------------------------------------
# 4. CROSS-LINGUAL ALIGNMENT PIPELINE
# -----------------------------------------------------------------------------
class CrossLingualManifoldAligner:
    """Procrustes alignment of the Voynich PPMI space against REAL target corpora.

    Anchors are paired by frequency rank (an explicit, weak assumption). The
    observed disparity is compared with a null in which the target anchor rows
    are shuffled, so a good fit only counts if it beats arbitrary pairings.
    """

    def __init__(self, token_list: List[str], dim: int = 8, n_anchors: int = 40):
        self.tokens = token_list
        self.dim = dim
        self.n_anchors = n_anchors
        self.vocab, self.vectors, self.w2i = build_ppmi_space(self.tokens, max_vocab=150, dim=self.dim)

    def run_alignment_benchmark(
        self,
        target_corpora: Optional[Dict[str, List[str]]] = None,
        n_perms: int = 1000,
        seed: int = 42,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if not target_corpora:
            return pd.DataFrame([{
                "Historical Control Corpus": "none supplied",
                "Status": "not computed: pass real tokenised historical text as target_corpora",
            }]), pd.DataFrame()

        rng = np.random.default_rng(seed)
        records = []
        for name, target_tokens in target_corpora.items():
            t_vocab, t_vecs, _ = build_ppmi_space(target_tokens, max_vocab=150, dim=self.dim)
            n = min(self.n_anchors, len(self.vocab), len(t_vocab))
            if n < MIN_ANCHORS_PER_DIM * self.dim:
                records.append({
                    "Historical Control Corpus": name,
                    "Status": f"not computed: {n} anchors for {self.dim} dimensions "
                              f"(need >= {MIN_ANCHORS_PER_DIM * self.dim})",
                })
                continue
            src, tgt = self.vectors[:n], t_vecs[:n]
            _, d2 = orthogonal_procrustes(src, tgt)
            null = np.array([orthogonal_procrustes(src, tgt[rng.permutation(n)])[1] for _ in range(n_perms)])
            p = float((np.sum(null <= d2) + 1) / (n_perms + 1))
            records.append({
                "Historical Control Corpus": name,
                "Anchors": n,
                "Procrustes Disparity (d^2)": round(float(d2), 4),
                "Shuffled-anchor d^2 (mean)": round(float(null.mean()), 4),
                "Empirical p (d^2 <= null)": round(p, 4),
                "Status": "computed",
            })
        return pd.DataFrame(records), pd.DataFrame()
