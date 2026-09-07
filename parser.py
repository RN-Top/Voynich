"""
voynich-state-viewer: Systematic Morphological Parser and State-Space Mapper.
Implements the grounded v4.0-v6.0 structural factorization:
    W = C( [Lambda x N_E x O_I] + rho )
"""

import re
from typing import Dict, List, Optional, Tuple
import pandas as pd


# Operational Macrostate Regimes (C / L / P / R)
STATE_COLORS = {
    "C": "#FF6B6B",  # Transform / Processive (Red)
    "L": "#4D96FF",  # Connect / Relational (Blue)
    "P": "#6BCB77",  # Maintain / Stative (Green)
    "R": "#FFD93D",  # Resolve / Terminal (Yellow)
    "?": "#9E9E9E"   # Unmapped / Residual (Gray)
}

STATE_LABELS = {
    "C": "Transform (Compute/Loop)",
    "L": "Connect (Bus/Junction)",
    "P": "Maintain (Stative Hold)",
    "R": "Resolve (Terminal Flush)",
    "?": "Unmapped"
}


class VoynichParser:
    """Empirical slot-and-feature morphological parser grounded in measurable token dynamics."""

    CONTROL_PREFIXES = ('qk', 'dk', 'q', 'k', 'd')
    REALIZATION_PORTS = ('aiin', 'aiiin', 'ain', 'ar', 'al', 'am', 'm', 'y')
    KNOWN_CARRIERS = ('otcheod', 'oteod', 'otod', 'cheod', 'opair', 'pch', 'ch', 'ot', 't')
    E_PATTERN = re.compile(r'e+')

    @classmethod
    def clean_token(cls, raw: str) -> str:
        """Strips editorial and certainty brackets from EVA/IVTFF tokens."""
        # Resolve alternate readings [a:b] -> pick primary
        t = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', raw)
        # Strip editorial tags, character comments, and inline glyph IDs
        t = re.sub(r'[{}\[\]<!>]', '', t)
        t = re.sub(r'@[0-9]+;', '', t)
        t = re.sub(r'[@\d;%+=*?$,^~-]', '', t)
        return t.strip().lower()

    @classmethod
    def decompose_morphology(cls, raw_token: str) -> Dict[str, object]:
        """
        Decomposes a surface token into C, Lambda, E-grade, internal O, and exit port rho.
        Adheres to the Lexical Stop Rule to avoid artificial over-segmentation.
        """
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

        # 4. Carrier Core (Lambda) with Lexical Stop Rule
        carrier = remainder if remainder else "EMPTY"
        for kc in cls.KNOWN_CARRIERS:
            if kc in remainder:
                carrier = kc
                break

        # Systematic detection of A2 boundary flusher (-m / -am)
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
        """
        Maps a cleaned token to one of the 4 operational macrostates (C/L/P/R).
        Labels represent observed behavioral regimes, not plaintext translations.
        """
        if not token_clean:
            return "?"

        # R: Resolve / Terminal flush (must exclude false matches from -ain / -aiin)
        if re.search(r'(am|(?<![ai])m)$', token_clean):
            return "R"

        # C: Transform / Processive compute loops
        if re.search(r'(eedy|edy|eey|ey|dy)$', token_clean):
            return "C"

        # L: Connect / Relational bus/junction state
        if re.search(r'(ain|aiin|aiiin|or|ar)$', token_clean):
            return "L"

        # P: Maintain / Stative holding state
        if re.search(r'(y|ol|al)$', token_clean) or token_clean in ("ol", "al", "y"):
            return "P"

        return "?"


def parse_zl3b(filepath: str, selected_folios: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Parses an authoritative IVTFF ZL3b transliteration file into a structured DataFrame.
    Accurately tracks line boundaries, Currier operating modes ($L=A vs $L=B), and quires ($Q).
    """
    records = []
    current_currier = "UNKNOWN"
    current_quire = "UNKNOWN"
    wanted = {f.lower() for f in selected_folios} if selected_folios else None

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Extract Currier language ($L=A/B) and Quire ($Q=...) from IVTFF header lines
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

            # Strip inline annotations, comments, and IVTFF locators
            clean_text = re.sub(r'<![^>]*>', '', raw_text)
            clean_text = re.sub(r'\{[^}]*\}', '', clean_text)
            clean_text = re.sub(r'<[%+=*][^>]*>', '', clean_text)

            # Split on standard IVTFF token separators: period, comma, or space
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
        df["next_state"] = df["state"].shift(-1)
        df["next_control"] = df["control"].shift(-1)
        df["next_exit_port"] = df["exit_port"].shift(-1)
        
        # Enforce line buffer resets: transitions cannot cross physical line ends
        df.loc[df["is_line_end"], ["next_state", "next_control", "next_exit_port"]] = None

    return df
