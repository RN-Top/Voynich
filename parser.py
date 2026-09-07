"""
voynich-state-viewer: Morphological Parser & Astronomical Ring Extractor
Implements token decomposition W = C([Lambda x N_E x O_I] + rho) and 
extracts angular/clock positions from IVTFF cosmological loci.
"""

import re
from typing import Dict, List, Optional
import pandas as pd

# Functional macrostate mappings for reference
STATE_COLORS = {
    "C": "#FF6B6B",  # Transform / Processive
    "L": "#4D96FF",  # Connect / Relational
    "P": "#6BCB77",  # Maintain / Stative
    "R": "#FFD93D",  # Resolve / Terminal
    "?": "#9E9E9E"   # Unmapped
}


class VoynichMorphology:
    """Isolates invariant lexical carriers (Lambda) and realization ports (rho)."""

    CONTROL_PREFIXES = ('qk', 'dk', 'q', 'k', 'd')
    REALIZATION_PORTS = ('aiin', 'aiiin', 'ain', 'ar', 'al', 'am', 'm', 'y')
    INVARIANT_CORES = ('otcheod', 'oteod', 'oeeod', 'otod', 'cheod', 'opair', 'pch', 'ch', 'ot', 't')
    E_PATTERN = re.compile(r'e+')

    @classmethod
    def clean_token(cls, raw: str) -> str:
        """Strips certainty brackets, line-end markup, and editorial symbols."""
        t = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', raw)
        t = re.sub(r'[{}\[\]<!>]', '', t)
        t = re.sub(r'@[0-9]+;', '', t)
        t = re.sub(r'[@\d;%+=*?$,^~-]', '', t)
        return t.strip().lower()

    @classmethod
    def extract_carrier(cls, raw_token: str) -> Dict[str, object]:
        """Decomposes token W into C, Lambda, E-grade, internal O, and rho."""
        token = cls.clean_token(raw_token)
        if not token:
            return {"raw": raw_token, "clean": "", "valid": False}

        remainder = token

        # 1. Control Header Strip
        control = "NONE"
        for cp in cls.CONTROL_PREFIXES:
            if remainder.startswith(cp):
                control = cp
                remainder = remainder[len(cp):]
                break

        # 2. Exit Port Strip (A2/A4 Successor Routers)
        exit_port = "BARE"
        for rp in cls.REALIZATION_PORTS:
            if remainder.endswith(rp):
                exit_port = rp
                remainder = remainder[:-len(rp)]
                break

        # 3. Internal Registers
        e_grade = len(cls.E_PATTERN.findall(remainder))
        internal_o = 'o' in remainder

        # 4. Lexical Stop Rule: Invariant Carrier Core (Lambda)
        carrier = remainder if remainder else "EMPTY"
        for core in cls.INVARIANT_CORES:
            if core in remainder:
                carrier = core
                break

        is_m = bool(re.search(r'(am|(?<![ai])m)$', token))

        return {
            "raw": raw_token,
            "clean": token,
            "control": control,
            "carrier": carrier,
            "exit_port": exit_port,
            "e_grade": e_grade,
            "internal_o": internal_o,
            "is_terminal_m": is_m,
            "valid": True
        }

    @staticmethod
    def map_macrostate(token_clean: str) -> str:
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


# Canonical Folio Domain Mapping
FOLIO_DOMAIN_MAP = {
    "f70r1": "Aries", "f70r2": "Aries", "f70v1": "Taurus", "f70v2": "Taurus",
    "f71r": "Gemini", "f71v": "Cancer", "f72r1": "Leo", "f72r2": "Virgo",
    "f72r3": "Cancer", "f72v1": "Libra", "f72v2": "Virgo", "f72v3": "Scorpio",
    "f73r": "Sagittarius", "f73v": "Capricorn", "f74r": "Aquarius", "f74v": "Pisces"
}


def parse_zl3b(filepath: str) -> pd.DataFrame:
    """Parses raw IVTFF ZL3b lines into structured morphological and spatial records."""
    records = []
    current_currier = "UNKNOWN"

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith('#') or line.startswith('<!') or '<f' in line:
                l_match = re.search(r'\$L=([AB])', line)
                if l_match:
                    current_currier = l_match.group(1)

            if line.startswith('#'):
                continue

            match = re.match(r'<([^>]+)>\s*(.*)', line)
            if not match:
                continue

            header, raw_text = match.groups()
            folio = header.split('.')[0]

            # Extract angular clock indicators if present (e.g. <!09:30>)
            clock_match = re.search(r'<!(\d{2}:\d{2})>', raw_text)
            clock_pos = clock_match.group(1) if clock_match else "UNKNOWN"

            # Clean annotations
            clean_text = re.sub(r'<![^>]*>', '', raw_text)
            clean_text = re.sub(r'\{[^}]*\}', '', clean_text)
            clean_text = re.sub(r'<[%+=*][^>]*>', '', clean_text)

            raw_tokens = [t for t in re.split(r'[.,\s]+', clean_text) if t and not t.startswith('<')]
            total = len(raw_tokens)

            # Assign Illustrated Zodiac Sign or General Domain
            zodiac_target = FOLIO_DOMAIN_MAP.get(folio, "Non-Zodiac")
            is_astro = (folio.startswith("f67") or folio.startswith("f68") or 
                        folio.startswith("f69") or folio.startswith("f70") or 
                        folio.startswith("f71") or folio.startswith("f72") or 
                        folio.startswith("f73") or folio.startswith("f74"))

            for idx, raw_t in enumerate(raw_tokens):
                decomp = VoynichMorphology.extract_carrier(raw_t)
                if not decomp["valid"] or not decomp["clean"]:
                    continue

                state = VoynichMorphology.map_macrostate(decomp["clean"])
                records.append({
                    "folio": folio,
                    "header": header,
                    "currier": current_currier,
                    "is_astro": is_astro,
                    "zodiac_sign": zodiac_target,
                    "clock_pos": clock_pos,
                    "token_idx": idx,
                    "is_line_start": (idx == 0),
                    "is_line_end": (idx == total - 1),
                    "state": state,
                    **decomp
                })

    df = pd.DataFrame(records)
    if not df.empty:
        df["next_token"] = df["raw"].shift(-1)
        df["next_carrier"] = df["carrier"].shift(-1)
        df["next_control"] = df["control"].shift(-1)
        df.loc[df["is_line_end"], ["next_token", "next_carrier", "next_control"]] = None

    return df
