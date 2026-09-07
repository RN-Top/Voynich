"""
voynich-state-viewer: Grounded Morphological Parser & Carrier Core Isolator
Implements the canonical structural factorization:
    W = C( [Lambda x N_E x O_I] + rho )
"""

import re
from typing import Dict, List, Optional, Tuple
import pandas as pd

# Canonical macrostate color schemes
STATE_COLORS = {
    "C": "#FF6B6B",  # Transform / Processive
    "L": "#4D96FF",  # Connect / Relational
    "P": "#6BCB77",  # Maintain / Stative
    "R": "#FFD93D",  # Resolve / Terminal
    "?": "#9E9E9E"   # Unmapped
}

STATE_LABELS = {
    "C": "Transform",
    "L": "Connect",
    "P": "Maintain",
    "R": "Resolve",
    "?": "Unmapped"
}


class VoynichParser:
    """Slot-and-feature morphological parser and carrier extractor."""

    CONTROL_PREFIXES = ('qk', 'dk', 'q', 'k', 'd')
    REALIZATION_PORTS = ('aiin', 'aiiin', 'ain', 'ar', 'al', 'am', 'm', 'y')
    INVARIANT_CORES = ('otcheod', 'oteod', 'otod', 'cheod', 'opair', 'pch', 'ch', 'ot', 't')
    E_PATTERN = re.compile(r'e+')

    @classmethod
    def clean_token(cls, raw: str) -> str:
        """Strips editorial tags, line artifacts, and brackets."""
        t = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', raw)
        t = re.sub(r'[{}\[\]<!>]', '', t)
        t = re.sub(r'@[0-9]+;', '', t)
        t = re.sub(r'[@\d;%+=*?$,^~-]', '', t)
        return t.strip().lower()

    @classmethod
    def decompose_morphology(cls, raw_token: str) -> Dict[str, object]:
        """Factorizes token W into C, Lambda, E-grade, internal O, and exit port rho."""
        token = cls.clean_token(raw_token)
        if not token:
            return {"token": raw_token, "clean": "", "valid": False}

        remainder = token

        # 1. Control Header (C)
        control = "NONE"
        for cp in cls.CONTROL_PREFIXES:
            if remainder.startswith(cp):
                control = cp
                remainder = remainder[len(cp):]
                break

        # 2. Exit Port / Successor Router (rho)
        exit_port = "BARE"
        for rp in cls.REALIZATION_PORTS:
            if remainder.endswith(rp):
                exit_port = rp
                remainder = remainder[:-len(rp)]
                break

        # 3. Internal Registers: E-grade multiplicity & Internal O toggle
        e_matches = cls.E_PATTERN.findall(remainder)
        e_grade = max([len(m) for m in e_matches], default=0)
        has_internal_o = 'o' in remainder

        # 4. Conserved Carrier Stem (Lambda) - Enforces Lexical Stop Rule
        carrier = remainder if remainder else "EMPTY"
        for core in cls.INVARIANT_CORES:
            if core in remainder:
                carrier = core
                break

        # Terminal -m flush detection (A2 Effect)
        is_m = bool(re.search(r'(am|(?<![ai])m)$', token))

        return {
            "token": raw_token,
            "clean": token,
            "valid": True,
            "control": control,
            "carrier_core": carrier,
            "e_grade": e_grade,
            "internal_o": has_internal_o,
            "exit_port": exit_port,
            "is_terminal_m": is_m
        }

    @staticmethod
    def map_macrostate(token_clean: str) -> str:
        """Maps cleaned surface tokens to C, L, P, or R functional regimes."""
        if not token_clean:
            return "?"

        if re.search(r'(am|(?<![ai])m)$', token_clean):
            return "R"
        if re.search(r'(eedy|edy|eey|ey|dy)$', token_clean):
            return "C"
        if re.search(r'(ain|aiin|aiiin|or|ar)$', token_clean):
            return "L"
        if re.search(r'(y|ol|al)$', token_clean) or token_clean in ("ol", "al", "y"):
            return "P"

        return "?"


def get_section_from_folio(folio: str) -> str:
    """Categorizes folios into canonical manuscript domains based on catalog records."""
    f = folio.lower().replace('f', '')
    num_match = re.match(r'(\d+)', f)
    if not num_match:
        if 'ros' in f:
            return "Cosmological"
        return "Unknown"

    num = int(num_match.group(1))
    if 1 <= num <= 66:
        return "Herbal"
    elif 67 <= num <= 73:
        return "Astronomical/Zodiac"
    elif 75 <= num <= 84:
        return "Biological"
    elif 85 <= num <= 86:
        return "Cosmological"
    elif 87 <= num <= 102:
        return "Pharmaceutical"
    elif 103 <= num <= 116:
        return "Stars/Recipes"
    return "Unknown"


def parse_zl3b(filepath: str, selected_folios: Optional[List[str]] = None) -> pd.DataFrame:
    """Parses IVTFF transliteration files with locus, section, and morphological tagging."""
    records = []
    current_currier = "UNKNOWN"
    current_quire = "UNKNOWN"
    wanted = {f.lower() for f in selected_folios} if selected_folios else None

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Check for header metadata
            if line.startswith('#') or line.startswith('<!') or '<f' in line:
                l_match = re.search(r'\$L=([AB])', line)
                if l_match:
                    current_currier = l_match.group(1)
                q_match = re.search(r'\$Q=([A-Z0-9]+)', line)
                if q_match:
                    current_quire = q_match.group(1)

            if line.startswith('#'):
                continue

            match = re.match(r'<([^>]+)>\s*(.*)', line)
            if not match:
                continue

            header, raw_text = match.groups()
            folio = header.split('.')[0]

            if wanted is not None and folio.lower() not in wanted:
                continue

            section = get_section_from_folio(folio)

            clean_text = re.sub(r'<![^>]*>', '', raw_text)
            clean_text = re.sub(r'\{[^}]*\}', '', clean_text)
            clean_text = re.sub(r'<[%+=*][^>]*>', '', clean_text)

            raw_tokens = [t for t in re.split(r'[.,\s]+', clean_text) if t and not t.startswith('<')]
            total = len(raw_tokens)

            for idx, raw_t in enumerate(raw_tokens):
                decomp = VoynichParser.decompose_morphology(raw_t)
                if not decomp["valid"] or not decomp["clean"]:
                    continue

                state = VoynichParser.map_macrostate(decomp["clean"])
                records.append({
                    "folio": folio,
                    "header": header,
                    "section": section,
                    "quire": current_quire,
                    "currier": current_currier,
                    "token_idx": idx,
                    "is_line_start": (idx == 0),
                    "is_line_end": (idx == total - 1),
                    "state": state,
                    **decomp
                })

    df = pd.DataFrame(records)
    if not df.empty:
        df["next_token"] = df["token"].shift(-1)
        df["next_state"] = df["state"].shift(-1)
        df["next_control"] = df["control"].shift(-1)
        df["next_exit_port"] = df["exit_port"].shift(-1)
        df["prev_control"] = df["control"].shift(1)

        # Enforce physical line boundaries
        df.loc[df["is_line_end"], ["next_token", "next_state", "next_control", "next_exit_port"]] = None
        df.loc[df["is_line_start"], ["prev_control"]] = None

    return df
