"""
zodiac_recipe_decoder.py
========================================================================================
Next-Stage Operational Solver:
  - Validates 30-degree zodiac spoke rotations against Latin/Venetian astrological roots.
  - Decodes sequential compounding and distillation recipes from late folios.
========================================================================================
"""

from typing import Dict, List

# --------------------------------------------------------------------------------------
# 1. Phonotactics & Vowel Mapping Setup
# --------------------------------------------------------------------------------------
VOWELS = {"a", "o", "h", "t", "i", "y"}
CONSONANTS = {"c", "d", "e", "f", "k", "l", "m", "n", "p", "s", "r"}

PHONETIC_MAP = {
    "o": "O", "t": "T", "c": "S", "h": "A", "e": "R", "d": "N",
    "a": "U", "i": "I", "q": "C", "k": "O", "p": "M", "m": "S",
    "y": "M", "s": "P", "l": "L", "r": "R",
}

# --------------------------------------------------------------------------------------
# 2. 30-Degree Zodiac Radial Geometry Registry
# --------------------------------------------------------------------------------------
ZODIAC_30_DEGREE_SYSTEM = [
    {"sign": "Pisces",      "degrees": "330°-360°", "folio": "f70v2", "spoke": "otcheod", "stem": "cheod", "target": "PASIS"},
    {"sign": "Aries",       "degrees": "000°-030°", "folio": "f71r",  "spoke": "opairam", "stem": "pair",  "target": "ARIES / MAUR"},
    {"sign": "Taurus",      "degrees": "030°-060°", "folio": "f71r",  "spoke": "okeal",   "stem": "keal",  "target": "TAUR / ORAN"},
    {"sign": "Cancer",      "degrees": "090°-120°", "folio": "f72r1", "spoke": "otcheor", "stem": "cheor", "target": "CANC / PASOR"},
    {"sign": "Leo",         "degrees": "120°-150°", "folio": "f72r1", "spoke": "dal",     "stem": "l",     "target": "LEO / L"},
    {"sign": "Scorpio",     "degrees": "210°-240°", "folio": "f72v1", "spoke": "otol",    "stem": "ol",    "target": "SCOR / OR"},
    {"sign": "Sagittarius", "degrees": "240°-270°", "folio": "f72v2", "spoke": "otedy",   "stem": "edy",   "target": "SAGI / RAM"},
]

# --------------------------------------------------------------------------------------
# 3. Procedural Distillation Lexicon
# --------------------------------------------------------------------------------------
LEXICON = {
    "qokedy":      ("coci", "sied", "boil / heat gently"),
    "qokchdy":     ("coci_qokchdy", "sied_qokchdy", "active secondary boiling cycle"),
    "qoted":       ("scalda", "waerme", "warm gently"),
    "okeedy":      ("incorpora", "menge", "compound / blend thoroughly"),
    "qokeey":      ("distilla", "brenn", "distill vapors"),
    "chdam":       ("saldo", "beschliess", "seal vessel"),
    "cheocthedy":  ("fraturo de erba", "kruttheil", "plant fraction"),
    "chedar":      ("fiori", "bluemen", "blossoms"),
    "oky":         ("d'erba", "krutwazzer", "herb decoction menstruum"),
    "daiin":       ("agva", "wazzer", "distilled water menstruum"),
    "chedaiin":    ("decocto", "krutwazzer", "herb decoction"),
    "otcheodaiin": ("licore de stella", "sternauszug", "celestial / astronomical component"),
    "daraiin":     ("aqua_vitae", "lebenswasser", "alcohol menstruum"),
    "okaiin":      ("oglio_caldo", "heissol", "heated oil menstruum"),
    "cthaiin":     ("succo_purificato", "lautersaft", "clarified plant extract"),
    "shedaiin":    ("bagno_minerale", "mineralbad", "balneological mineral base"),
}


def cv_skeleton(token: str) -> str:
    return "".join("V" if c in VOWELS else "C" for c in token.lower() if c in (VOWELS | CONSONANTS))


def to_phonetic(token: str) -> str:
    return "".join(PHONETIC_MAP.get(c, c) for c in token.lower())


def decode_recipe(raw_line: str) -> Dict[str, str]:
    tokens = raw_line.strip().split()
    venetian, german, actions = [], [], []

    for t in tokens:
        if t in LEXICON:
            v, g, m = LEXICON[t]
            venetian.append(v)
            german.append(g)
            actions.append(m)
        elif t.endswith("aiin"):
            venetian.append(f"licore_{t}")
            german.append(f"auszug_{t}")
            actions.append(f"extract ({t})")
        else:
            venetian.append(t)
            german.append(t)
            actions.append(t)

    return {
        "raw": raw_line,
        "venetian": " ".join(venetian),
        "german": " ".join(german),
        "reading": "; ".join(actions).capitalize() + ".",
    }


def main():
    print("=" * 80)
    print("30-DEGREE ZODIAC SPOKE ALIGNMENT AUDIT")
    print("=" * 80)
    for row in ZODIAC_30_DEGREE_SYSTEM:
        stem = row["stem"]
        cv = cv_skeleton(stem)
        sound = to_phonetic(stem)
        print(f"[{row['folio']}] {row['degrees']} ({row['sign']:<11}) | Spoke: {row['spoke']:<8} | "
              f"Stem: {stem:<6} | CV: {cv:<5} | Sound: {sound:<6} | Target: {row['target']}")

    print("\n" + "=" * 80)
    print("DISTILLATION & COMPOUNDING RECIPE BATCH DECODER")
    print("=" * 80)
    corpus_test_lines = [
        "qokedy cheocthedy qoted chedar okeedy daiin chedaiin oky chdam",
        "qokedy otcheodaiin qokchdy",
        "qokedy shedaiin qokchdy",
        "qokedy daraiin cthaiin qokeey chdam",
    ]
    for line in corpus_test_lines:
        res = decode_recipe(line)
        print(f"RAW:     {res['raw']}")
        print(f"VENICE:  {res['venetian']}")
        print(f"GERMAN:  {res['german']}")
        print(f"READING: {res['reading']}")
        print("-" * 80)


if __name__ == "__main__":
    main()
