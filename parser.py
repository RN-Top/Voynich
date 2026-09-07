"""
voynich-state-viewer: Complete Corpus Parser
Ingests the entire manuscript across all folios (f1r through f116v).
"""

import os
import re
import urllib.request
from typing import Dict, Optional
import pandas as pd

DEFAULT_DATA_PATH = os.path.join("data", "ZL3b-n.txt")
FALLBACK_URL = "https://raw.githubusercontent.com/frogging-art/voynich/master/data/ZL3b-n.txt"

STATE_COLORS = {
    "C": "#FF6B6B",
    "L": "#4D96FF",
    "P": "#6BCB77",
    "R": "#FFD93D",
    "?": "#9E9E9E"
}

STATE_LABELS = {
    "C": "Transform", "L": "Connect", "P": "Maintain", "R": "Resolve", "?": "Unmapped"
}


def ensure_corpus_loaded(filepath: str = DEFAULT_DATA_PATH) -> str:
    """Verifies that the full text exists. If it is only the 17-line stub, fetches the full corpus."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Check if the file is missing or contains fewer than 100 lines
    needs_full_text = False
    if not os.path.exists(filepath):
        needs_full_text = True
    else:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            line_count = sum(1 for _ in f)
        if line_count < 100:
            needs_full_text = True

    if needs_full_text:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(FALLBACK_URL, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
                if len(content) > 100000:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
        except Exception:
            pass

    return filepath


class VoynichParser:
    CONTROL_PREFIXES = ('qk', 'dk', 'q', 'k', 'd')
    REALIZATION_PORTS = ('aiin', 'aiiin', 'ain', 'ar', 'al', 'am', 'm', 'y')
    INVARIANT_CORES = ('otcheod', 'oteod', 'oeeod', 'otod', 'cheod', 'opair', 'pch', 'ch', 'ot', 't')
    E_PATTERN = re.compile(r'e+')

    @classmethod
    def clean_token(cls, raw: str) -> str:
        t = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', raw)
        t = re.sub(r'[{}\[\]<!>]', '', t)
        t = re.sub(r'@[0-9]+;', '', t)
        t = re.sub(r'[@\d;%+=*?$,^~-]', '', t)
        return t.strip().lower()

    @classmethod
    def decompose_morphology(cls, raw_token: str) -> Dict[str, object]:
        token = cls.clean_token(raw_token)
        if not token:
            return {"token": raw_token, "clean": "", "valid": False}

        remainder = token
        control = "NONE"
        for cp in cls.CONTROL_PREFIXES:
            if remainder.startswith(cp):
                control = cp
                remainder = remainder[len(cp):]
                break

        exit_port = "BARE"
        for rp in cls.REALIZATION_PORTS:
            if remainder.endswith(rp):
                exit_port = rp
                remainder = remainder[:-len(rp)]
                break

        e_grade = len(cls.E_PATTERN.findall(remainder))
        internal_o = 'o' in remainder

        carrier = remainder if remainder else "EMPTY"
        for core in cls.INVARIANT_CORES:
            if core in remainder:
                carrier = core
                break

        is_m = bool(re.search(r'(am|(?<![ai])m)$', token))

        return {
            "token": raw_token,
            "clean": token,
            "control": control,
            "carrier_core": carrier,
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


def get_section_from_folio(folio: str) -> str:
    f = folio.lower().replace('f', '')
    num_match = re.match(r'(\d+)', f)
    if not num_match:
        return "Cosmological" if 'ros' in f else "General"
    num = int(num_match.group(1))
    if 1 <= num <= 66:
        return "Herbal"
    elif 67 <= num <= 74:
        return "Astronomical/Zodiac"
    elif 75 <= num <= 84:
        return "Biological"
    elif 85 <= num <= 86:
        return "Cosmological"
    elif 87 <= num <= 102:
        return "Pharmaceutical"
    elif 103 <= num <= 116:
        return "Stars/Recipes"
    return "General"


def parse_zl3b(filepath_or_buffer) -> pd.DataFrame:
    records = []
    current_currier = "UNKNOWN"
    current_quire = "UNKNOWN"

    # Support filepath string or Streamlit UploadedFile buffer
    if isinstance(filepath_or_buffer, str):
        filepath = ensure_corpus_loaded(filepath_or_buffer)
        if not os.path.exists(filepath):
            return pd.DataFrame()
        f = open(filepath, 'r', encoding='utf-8', errors='ignore')
    else:
        f = filepath_or_buffer

    try:
        for line in f:
            if isinstance(line, bytes):
                line = line.decode('utf-8', errors='ignore')
            line = line.strip()
            if not line:
                continue

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
    finally:
        if isinstance(filepath_or_buffer, str) and not f.closed:
            f.close()

    df = pd.DataFrame(records)
    if not df.empty:
        df["next_token"] = df["clean"].shift(-1)
        df["next_state"] = df["state"].shift(-1)
        df["next_control"] = df["control"].shift(-1)
        df.loc[df["is_line_end"], ["next_token", "next_state", "next_control"]] = None

    return df
