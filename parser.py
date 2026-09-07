"""
Voynich corpus ingestion and morphology parser.
Produces the shared DataFrame schema used by all analysis modules.
"""

from __future__ import annotations

import io
import os
import re
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

CORPUS_URLS = (
    "https://raw.githubusercontent.com/matthewdgreen/cipher_benchmark/main/benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt",
    "https://www.voynich.nu/data/ZL3b-n.txt",
    "http://www.voynich.nu/data/ZL3b-n.txt",
)
CORPUS_URL = CORPUS_URLS[0]
CORPUS_PATH = os.path.join("data", "ZL3b-n.txt")
MIN_CORPUS_BYTES = 50_000


def infer_section(folio: str) -> str:
    f = str(folio).lower().replace("f", "").strip()
    match = re.match(r"(\d+)", f)

    if not match:
        return "Cosmological" if "ros" in f else "General"

    n = int(match.group(1))

    if 1 <= n <= 66:
        return "Herbal"
    if 67 <= n <= 74:
        return "Astronomical/Zodiac"
    if 75 <= n <= 84:
        return "Biological"
    if 85 <= n <= 86:
        return "Cosmological"
    if 87 <= n <= 102:
        return "Pharmaceutical"
    if 103 <= n <= 116:
        return "Stars/Recipes"

    return "General"


def ensure_full_corpus(path: str = CORPUS_PATH) -> str:
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    needs_download = (
        not path_obj.exists()
        or path_obj.stat().st_size < MIN_CORPUS_BYTES
    )

    if not needs_download:
        return str(path_obj)

    errors = []

    for url in CORPUS_URLS:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
        except Exception as exc:
            errors.append(f"{url}: {exc}")
            continue

        if len(data) < MIN_CORPUS_BYTES:
            errors.append(
                f"{url}: downloaded only {len(data)} bytes"
            )
            continue

        path_obj.write_bytes(data)
        return str(path_obj)

    details = " | ".join(errors)
    raise RuntimeError(
        "The local Voynich corpus is missing/truncated and all automatic "
        f"download sources failed. {details}"
    )


class VoynichParser:
    CONTROL_PREFIXES = ("qk", "dk", "q", "k", "d")

    REALIZATION_PORTS = (
        "aiiin",
        "aiin",
        "ain",
        "ar",
        "al",
        "am",
        "m",
        "y",
    )

    KNOWN_CARRIERS = (
        "otcheod",
        "oteod",
        "otod",
        "cheod",
        "opair",
        "pch",
        "ch",
        "ot",
        "t",
    )

    E_PATTERN = re.compile(r"e+")

    @classmethod
    def clean_token(cls, raw: str) -> str:
        token = str(raw)

        token = re.sub(
            r"\[([^:]+):[^\]]+\]",
            r"\1",
            token,
        )

        token = re.sub(r"[{}\[\]<!>]", "", token)
        token = re.sub(r"@[0-9]+;", "", token)
        token = re.sub(r"[@\d;%+=*?$,^~\-]", "", token)

        return token.strip().lower()

    @classmethod
    def decompose_morphology(cls, raw_token: str) -> Dict[str, object]:
        token = cls.clean_token(raw_token)

        if not token:
            return {
                "token": raw_token,
                "raw": raw_token,
                "clean": "",
                "valid": False,
            }

        remainder = token
        control = "NONE"

        for prefix in cls.CONTROL_PREFIXES:
            if remainder.startswith(prefix):
                control = prefix
                remainder = remainder[len(prefix):]
                break

        exit_port = "BARE"

        for port in cls.REALIZATION_PORTS:
            if remainder.endswith(port):
                exit_port = port
                remainder = remainder[:-len(port)]
                break

        e_matches = cls.E_PATTERN.findall(remainder)
        e_grade = max(
            (len(match) for match in e_matches),
            default=0,
        )

        carrier = remainder if remainder else "EMPTY"

        for known in cls.KNOWN_CARRIERS:
            if known in remainder:
                carrier = known
                break

        return {
            "token": raw_token,
            "raw": raw_token,
            "clean": token,
            "valid": True,
            "control": control,
            "carrier_core": carrier,
            "carrier": carrier,
            "e_grade": e_grade,
            "internal_o": "o" in remainder,
            "exit_port": exit_port,
            "is_terminal_m": bool(
                re.search(r"(am|(?<![ai])m)$", token)
            ),
        }

    @staticmethod
    def map_macrostate(token_clean: str) -> str:
        if not token_clean:
            return "?"

        if re.search(r"(am|(?<![ai])m)$", token_clean):
            return "R"

        if re.search(r"(eedy|edy|eey|ey|dy)$", token_clean):
            return "C"

        if re.search(r"(ain|aiin|aiiin|or|ar)$", token_clean):
            return "L"

        if (
            re.search(r"(y|ol|al)$", token_clean)
            or token_clean in {"ol", "al", "y"}
        ):
            return "P"

        return "?"


def _read_source(source):
    if hasattr(source, "getvalue"):
        data = source.getvalue()

        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="ignore")

        return io.StringIO(str(data))

    if hasattr(source, "read"):
        data = source.read()

        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="ignore")

        return io.StringIO(str(data))

    return open(
        str(source),
        "r",
        encoding="utf-8",
        errors="ignore",
    )


def parse_zl3b(
    source=CORPUS_PATH,
    selected_folios: Optional[List[str]] = None,
) -> pd.DataFrame:

    if isinstance(source, (str, os.PathLike)):
        source_path = str(source)

        if (
            os.path.normpath(source_path)
            == os.path.normpath(CORPUS_PATH)
        ):
            source_path = ensure_full_corpus(source_path)

        reader = _read_source(source_path)

    else:
        reader = _read_source(source)

    records = []

    current_currier = "UNKNOWN"
    current_quire = "UNKNOWN"

    wanted = (
        {folio.lower() for folio in selected_folios}
        if selected_folios
        else None
    )

    try:
        for line in reader:
            line = str(line).strip()

            if not line:
                continue

            if (
                line.startswith("#")
                or line.startswith("<!")
                or "<f" in line
            ):
                hand_match = re.search(r"\$L=([AB])", line)

                if hand_match:
                    current_currier = hand_match.group(1)

                quire_match = re.search(
                    r"\$Q=([A-Z0-9]+)",
                    line,
                )

                if quire_match:
                    current_quire = quire_match.group(1)

            if line.startswith("#"):
                continue

            match = re.match(
                r"<([^>]+)>\s*(.*)",
                line,
            )

            if not match:
                continue

            header, raw_text = match.groups()
            folio = header.split(".")[0]

            if (
                wanted is not None
                and folio.lower() not in wanted
            ):
                continue

            clean_text = re.sub(
                r"<![^>]*>",
                "",
                raw_text,
            )

            clean_text = re.sub(
                r"\{[^}]*\}",
                "",
                clean_text,
            )

            clean_text = re.sub(
                r"<[%+=*][^>]*>",
                "",
                clean_text,
            )

            raw_tokens = [
                token
                for token in re.split(
                    r"[.,\s]+",
                    clean_text,
                )
                if token
                and not token.startswith("<")
            ]

            total = len(raw_tokens)
            section = infer_section(folio)

            for index, raw_token in enumerate(raw_tokens):
                decomposition = (
                    VoynichParser.decompose_morphology(
                        raw_token
                    )
                )

                if not decomposition.get("valid"):
                    continue

                if not decomposition.get("clean"):
                    continue

                records.append(
                    {
                        "folio": folio,
                        "header": header,
                        "quire": current_quire,
                        "currier": current_currier,
                        "section": section,
                        "token_idx": index,
                        "is_line_start": index == 0,
                        "is_line_end": index == total - 1,
                        "state":
                            VoynichParser.map_macrostate(
                                decomposition["clean"]
                            ),
                        "is_astro":
                            section
                            == "Astronomical/Zodiac",
                        "zodiac_sign": None,
                        "clock_pos": None,
                        **decomposition,
                    }
                )

    finally:
        if hasattr(reader, "close"):
            reader.close()

    df = pd.DataFrame(records)

    if df.empty:
        return df

    for column in (
        "state",
        "control",
        "exit_port",
    ):
        df[f"prev_{column}"] = df[column].shift(1)
        df[f"next_{column}"] = df[column].shift(-1)

    df.loc[
        df["is_line_start"],
        [
            "prev_state",
            "prev_control",
            "prev_exit_port",
        ],
    ] = None

    df.loc[
        df["is_line_end"],
        [
            "next_state",
            "next_control",
            "next_exit_port",
        ],
    ] = None

    return df.reset_index(drop=True)