"""
voynich-state-viewer: Complete Manuscript Ingestion, Morphotactic Tokenizer, and Parser.
Handles all 220+ folios (~38,000 tokens) from the authoritative IVTFF ZL3b-n stream.
"""

import os
import re
import urllib.request
import pandas as pd
from typing import Dict, List, Optional

CORPUS_URL = "https://www.voynich.nu/data/ZL3b-n.txt"
CORPUS_PATH = os.path.join("data", "ZL3b-n.txt")


def ensure_full_corpus():
    """
    Checks if data/ZL3b-n.txt exists and contains the full manuscript (>200 KB).
    If missing or truncated, automatically downloads the full authoritative corpus.
    """
    os.makedirs("data", exist_ok=True)
    needs_download = False

    if not os.path.exists(CORPUS_PATH):
        needs_download = True
    else:
        # A full IVTFF ZL3b corpus is ~411 KB; test stubs are typically under 5 KB
        if os.path.getsize(CORPUS_PATH) < 50000:
            needs_download = True

    if needs_download:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(CORPUS_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response, open(CORPUS_PATH, 'wb') as out_file:
            out_file.write(response.read())


class VoynichParser:
    CONTROL_PREFIXES = ('qk', 'dk', 'q', 'k', 'd')
    REALIZATION_PORTS = ('aiin', 'aiiin', 'ain', 'ar', 'al', 'am', 'm', 'y')
    KNOWN_CARRIERS = ('otcheod', 'oteod', 'otod', 'cheod', 'opair', 'pch', 'ch', 'ot', 't')
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

        e_matches = cls.E_PATTERN.findall(remainder)
        e_grade = max([len(m) for m in e_matches], default=0)
        has_internal_o = 'o' in remainder

        carrier = remainder if remainder else "EMPTY"
        for kc in cls.KNOWN_CARRIERS:
            if kc in remainder:
                carrier = kc
                break

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


def parse_zl3b(filepath: str = CORPUS_PATH, selected_folios: Optional[List[str]] = None) -> pd.DataFrame:
    ensure_full_corpus()
    records = []
    current_currier = "UNKNOWN"
    current_quire = "UNKNOWN"
    wanted = {f.lower() for f in selected_folios} if selected_folios else None

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
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

            if wanted is not None and folio.lower() not in wanted:
                continue

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
        df.loc[df["is_line_end"], ["next_state", "next_control", "next_exit_port"]] = None

    return df
