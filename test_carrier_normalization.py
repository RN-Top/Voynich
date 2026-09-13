"""
VOYNICH VERIFICATION TEST: STEP 2 - CARRIER NORMALIZATION & LEXICAL METRICS
Implements the canonical morphological decomposition:
    W = C( [Lambda x N_E x O_I] + rho )

Evaluates:
1. Lexical compression ratio (Raw types -> Normalized Lambda types).
2. Zipfian rank-frequency alpha fit (Raw surface tokens vs. Normalized carriers).
3. Bigram transition entropy of the carrier stream.
4. Top surviving domain-specific carrier anchors (OTCHEOD, OTEOD, OTOD, etc.).
"""

import math
import os
import re
from collections import Counter
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


class CarrierNormalizer:
    """Isolates invariant lexical carrier stems (Lambda) under the Lexical Stop Rule."""

    CONTROL_PREFIXES = ('qk', 'dk', 'q', 'k', 'd')
    REALIZATION_PORTS = ('aiin', 'aiiin', 'ain', 'ar', 'al', 'am', 'm', 'y')
    INVARIANT_CORES = ('otcheod', 'oteod', 'otod', 'cheod', 'opair', 'pch', 'ch', 'ot', 't')
    E_PATTERN = re.compile(r'e+')

    @classmethod
    def clean_token(cls, raw: str) -> str:
        """Strips certainty brackets, line artifacts, and editorial markup."""
        t = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', raw)
        t = re.sub(r'[{}\[\]<!>]', '', t)
        t = re.sub(r'@[0-9]+;', '', t)
        t = re.sub(r'[@\d;%+=*?$,^~-]', '', t)
        return t.strip().lower()

    @classmethod
    def extract_carrier(cls, raw_token: str) -> Dict[str, object]:
        token = cls.clean_token(raw_token)
        if not token:
            return {"raw": raw_token, "valid": False}

        remainder = token

        # 1. Control Header Strip (C)
        control = "NONE"
        for cp in cls.CONTROL_PREFIXES:
            if remainder.startswith(cp):
                control = cp
                remainder = remainder[len(cp):]
                break

        # 2. Exit Port Strip (rho)
        exit_port = "BARE"
        for rp in cls.REALIZATION_PORTS:
            if remainder.endswith(rp):
                exit_port = rp
                remainder = remainder[:-len(rp)]
                break

        # 3. Internal Registers: E-grade multiplicity & internal O
        e_matches = cls.E_PATTERN.findall(remainder)
        e_grade = max([len(m) for m in e_matches], default=0)
        has_internal_o = 'o' in remainder

        # 4. Lexical Stop Rule: Conserved Core Detection
        carrier = remainder if remainder else "EMPTY"
        for core in cls.INVARIANT_CORES:
            if core in remainder:
                carrier = core
                break

        return {
            "raw": raw_token,
            "token": token,
            "carrier": carrier,
            "control": control,
            "exit_port": exit_port,
            "e_grade": e_grade,
            "internal_o": has_internal_o,
            "valid": True
        }


def load_raw_corpus(filepath: str) -> List[Dict[str, str]]:
    """Loads tokens and line structure from IVTFF transliteration."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Corpus not found at {filepath}. Ensure data/ZL3b-n.txt is uploaded.")

    records = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            match = re.match(r'<([^>]+)>\s*(.*)', line)
            if not match:
                continue

            header, raw_text = match.groups()
            folio = header.split('.')[0]

            clean_text = re.sub(r'<![^>]*>', '', raw_text)
            clean_text = re.sub(r'\{[^}]*\}', '', clean_text)
            clean_text = re.sub(r'<[%+=*][^>]*>', '', clean_text)

            tokens = [t for t in re.split(r'[.,\s]+', clean_text) if t and not t.startswith('<')]
            for idx, tok in enumerate(tokens):
                records.append({
                    "folio": folio,
                    "header": header,
                    "raw_token": tok,
                    "is_line_end": (idx == len(tokens) - 1)
                })
    return records


def calculate_zipf_alpha(frequencies: List[int]) -> float:
    """Estimates Zipfian power-law exponent (alpha) via linear log-log regression."""
    ranks = np.arange(1, len(frequencies) + 1)
    log_ranks = np.log(ranks)
    log_freqs = np.log(frequencies)
    slope, _ = np.polyfit(log_ranks, log_freqs, 1)
    return float(-slope)


def calculate_entropy(sequence: List[str]) -> float:
    """Calculates Shannon bigram conditional entropy: H(W_{i+1} | W_i)."""
    bigrams = Counter(zip(sequence[:-1], sequence[1:]))
    unigrams = Counter(sequence)
    total_bigrams = sum(bigrams.values())

    h = 0.0
    for (w1, w2), count in bigrams.items():
        p_w1_w2 = count / total_bigrams
        p_w2_given_w1 = count / unigrams[w1]
        h -= p_w1_w2 * math.log2(p_w2_given_w1)
    return round(h, 3)


def run_stage_two_test(corpus_path: str = "data/ZL3b-n.txt"):
    print("=" * 70)
    print("RUNNING STEP 2: CARRIER NORMALIZATION & LEXICAL BEHAVIOR AUDIT")
    print("=" * 70)

    raw_records = load_raw_corpus(corpus_path)
    normalizer = CarrierNormalizer()

    parsed = []
    for r in raw_records:
        decomp = normalizer.extract_carrier(r["raw_token"])
        if decomp["valid"] and decomp["carrier"] != "EMPTY":
            parsed.append({
                "raw": decomp["token"],
                "carrier": decomp["carrier"],
                "is_line_end": r["is_line_end"]
            })

    raw_tokens = [p["raw"] for p in parsed]
    carrier_tokens = [p["carrier"] for p in parsed]

    raw_counts = Counter(raw_tokens)
    carrier_counts = Counter(carrier_tokens)

    # 1. Type-Token Compression
    print(f"\n[1] TYPE-TOKEN COMPRESSION:")
    print(f"  Total Processed Tokens:       {len(parsed):,}")
    print(f"  Surface Word Types:           {len(raw_counts):,}")
    print(f"  Normalized Carrier Types:     {len(carrier_counts):,}")
    compression = (1.0 - (len(carrier_counts) / len(raw_counts))) * 100
    print(f"  Vocabulary Compression:       {compression:.2f}% reduction")

    # 2. Zipf's Law Exponent
    raw_alpha = calculate_zipf_alpha(sorted(raw_counts.values(), reverse=True))
    carrier_alpha = calculate_zipf_alpha(sorted(carrier_counts.values(), reverse=True))
    print(f"\n[2] ZIPF POWER-LAW FIT (ALPHA):")
    print(f"  Raw Surface Tokens Alpha:     {raw_alpha:.3f}")
    print(f"  Normalized Carriers Alpha:    {carrier_alpha:.3f}  (Natural language target ~ 1.00)")

    # 3. Bigram Entropy
    raw_entropy = calculate_entropy(raw_tokens)
    carrier_entropy = calculate_entropy(carrier_tokens)
    print(f"\n[3] SEQUENTIAL BIGRAM ENTROPY:")
    print(f"  Surface Token Entropy:        {raw_entropy:.3f} bits/token")
    print(f"  Carrier Stream Entropy:       {carrier_entropy:.3f} bits/token")

    # 4. Top Normalized Lexical Stems
    print(f"\n[4] TOP 15 NORMALIZED CARRIER STEMS (LAMBDA):")
    for stem, count in carrier_counts.most_common(15):
        pct = (count / len(parsed)) * 100
        print(f"  {stem.ljust(15)} : {count:5d} ({pct:.2f}%)")

    print("\n" + "=" * 70)
    print("VERDICT / FALSIFICATION CHECK:")
    if carrier_alpha > 0.85 and compression > 40.0:
        print("  PASS: Carrier normalization preserves Zipfian lexical stability")
        print("        while eliminating redundant surface morphological variants.")
    else:
        print("  CAUTION: Vocabulary distribution deviates from standard lexical models.")
    print("=" * 70)


if __name__ == "__main__":
    run_stage_two_test()
