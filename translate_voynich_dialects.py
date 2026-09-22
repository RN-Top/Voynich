"""
VOYNICH DUAL-DIALECT TRANSLATOR & PROCEDURAL ENGINE
Translates the Voynich token stream into:
1. Venetian Trade Apothecary (Zenzovero tradition, c. 1420)
2. Early New High German Distillation (Brunschwig tradition, c. 1430)

Produces a 4-layer interlinear translation:
ORIGINAL -> STRUCTURAL GLOSS -> VENETIAN -> EARLY GERMAN -> OPERATIONAL ENGLISH
"""

import os
import re
import pandas as pd

# ---------------------------------------------------------
# HISTORICAL DIALECT MAPPINGS (COMPOUNDING & DISTILLATION)
# ---------------------------------------------------------

VENETIAN_LEXICON = {
    # Operators (Process Verbs)
    "qokedy": ("coci", "cook / boil [OPE]"),
    "qokeey": ("mescola", "mix / stir [OPE]"),
    "okedy": ("bogia", "let it boil [OPE]"),
    "qokal": ("destilla", "distill / drip [OPE]"),
    "qotedy": ("scalda", "warm / heat [OPE]"),
    "qoted": ("scalda", "heat [OPE]"),
    "qor": ("circola", "circulate [OPE]"),
    "okeedy": ("incorpora", "blend in [OPE]"),
    # Operands (Substances & Parts)
    "daiin": ("agva", "water / menstruum [NOM]"),
    "shedy": ("radise", "rootstock [NOM]"),
    "chedy": ("erba", "plant / herb [NOM]"),
    "chedaiin": ("decocto d'erba", "herb decoction [NOM]"),
    "cheocthedy": ("fraturo de erba", "plant fraction [NOM]"),
    "chedar": ("fiori d'erba", "herb flowers [NOM]"),
    "otcheod": ("stella", "celestial coordinate [NOM]"),
    "otcheodaiin": ("licore de stella", "celestial menstruum [NOM]"),
    "otcheed": ("segno", "celestial sector [NOM]"),
    "otcheody": ("vaso", "receiver vessel [NOM]"),
    "shedaiin": ("bagno d'agva", "bath menstruum [NOM]"),
    "lkaiin": ("stillicidio", "condensate [NOM]"),
    "fachys": ("faza / principio", "incipit / phase [NOM]"),
    "ykal": ("tolli", "take / measure [NOM]"),
    "ar": ("spicco", "vehicle [NOM]"),
    "ataiin": ("menstruo", "base fluid [NOM]"),
    # Modifiers (Temperaments)
    "shol": ("caldo", "warm [MOD]"),
    "shory": ("secco", "dry [MOD]"),
    "chol": ("caldo", "hot [MOD]"),
    "chor": ("asciutto", "desiccated [MOD]"),
    # Terminal Closures & Flushes
    "chdam": ("saldo / serra", "seal vessel [TER]"),
    "shedam": ("serra bagno", "seal bath port [TER]"),
    "qopairam": ("spandi / cola", "evacuate distillate [TER]"),
    "oror": ("fin / saldo", "closure seal [TER]"),
    "sheey": ("stasi", "rest-state [TER]"),
    "ydaraishy": ("fatto da l'auctor", "composed by author [NOM]"),
    "ytchas": ("scritto da lo scriptor", "written by scribe [NOM]")
}

GERMAN_LEXICON = {
    # Operators (Process Verbs)
    "qokedy": ("sied", "seethe / boil [OPE]"),
    "qokeey": ("mische", "mix / blend [OPE]"),
    "okedy": ("las sieden", "let seethe [OPE]"),
    "qokal": ("brenne", "distill [OPE]"),
    "qotedy": ("waerme", "heat / warm [OPE]"),
    "qoted": ("waerme", "warm [OPE]"),
    "qor": ("treibe umb", "circulate [OPE]"),
    "okeedy": ("menge", "compound / blend [OPE]"),
    # Operands (Substances & Parts)
    "daiin": ("wazzer", "water menstruum [NOM]"),
    "shedy": ("wurtz", "rootstock [NOM]"),
    "chedy": ("krut", "herb / plant [NOM]"),
    "chedaiin": ("krutwazzer", "herb water extract [NOM]"),
    "cheocthedy": ("kruttheil", "plant fraction [NOM]"),
    "chedar": ("bluemen", "plant blossoms [NOM]"),
    "otcheod": ("sternort", "celestial sector [NOM]"),
    "otcheodaiin": ("sternauszug", "celestial extract [NOM]"),
    "otcheed": ("sternzaichen", "celestial sign [NOM]"),
    "otcheody": ("kolben", "receiver vessel [NOM]"),
    "shedaiin": ("badwazzer", "bath menstruum [NOM]"),
    "lkaiin": ("tropfwazzer", "distillate drips [NOM]"),
    "fachys": ("anfang", "incipit / beginning [NOM]"),
    "ykal": ("nimb", "take / measure [NOM]"),
    "ar": ("glid", "vehicle [NOM]"),
    "ataiin": ("grundwazzer", "base fluid [NOM]"),
    # Modifiers (Temperaments)
    "shol": ("warm", "warm [MOD]"),
    "shory": ("trucken", "dry [MOD]"),
    "chol": ("heiss", "hot [MOD]"),
    "chor": ("gedoert", "desiccated [MOD]"),
    # Terminal Closures & Flushes
    "chdam": ("beschliess", "seal vessel [TER]"),
    "shedam": ("schliess bad", "close bath port [TER]"),
    "qopairam": ("lass auslauffen", "flush distillate [TER]"),
    "oror": ("ende / bschluss", "terminal closure [TER]"),
    "sheey": ("ruhe", "rest-state [TER]"),
    "ydaraishy": ("gemacht von meister", "composed by author [NOM]"),
    "ytchas": ("geschriben vom schreiber", "written by scribe [NOM]")
}

def tag_token_role(token: str) -> str:
    """Strict grammatical role assignment."""
    t = re.sub(r"[^a-z]", "", str(token).lower().strip())
    if not t:
        return "unmapped"
    if t.endswith("am") or t.endswith("m") or t in ["chdam", "shedam"] or t.endswith("dam"):
        return "drain[TER]"
    if t.startswith("shed"):
        return "retain[NOM]"
    if t.startswith("qok") or t.startswith("qo") or t.startswith("ok"):
        return "heat[OPE]"
    if t == "daiin" or t.endswith("aiin") or t.endswith("ain"):
        return "medium[NOM]"
    if t.endswith("ol") or t.endswith("al"):
        return "outlet[MOD]"
    if t.endswith("or") or t.endswith("ar"):
        return "reflux[MOD]"
    return "matrix[NOM]"

def translate_token(token: str):
    """Maps token into Venetian, German, and Operational English."""
    t = re.sub(r"[^a-z]", "", str(token).lower().strip())
    role = tag_token_role(t)
    
    # 1. Direct dictionary match
    if t in VENETIAN_LEXICON and t in GERMAN_LEXICON:
        ven_word, eng_desc = VENETIAN_LEXICON[t]
        ger_word, _ = GERMAN_LEXICON[t]
        return ven_word, ger_word, eng_desc, role
        
    # 2. Rule-based morphological decomposition
    if t.endswith("am") or t.endswith("m"):
        return f"saldo_{t}", f"schluss_{t}", f"flush_{t} [TER]", "drain[TER]"
    elif t.startswith("qo") or t.startswith("ok"):
        return f"coci_{t}", f"sied_{t}", f"heat_{t} [OPE]", "heat[OPE]"
    elif t.endswith("aiin") or t.endswith("ain"):
        return f"agva_{t}", f"wazzer_{t}", f"fluid_{t} [NOM]", "medium[NOM]"
    elif t.endswith("ol") or t.endswith("al"):
        return f"colato_{t}", f"auszug_{t}", f"outlet_{t} [MOD]", "outlet[MOD]"
    elif t.endswith("or") or t.endswith("ar"):
        return f"reflusso_{t}", f"widerlauf_{t}", f"reflux_{t} [MOD]", "reflux[MOD]"
    else:
        return f"materia_{t}", f"stoff_{t}", f"substance_{t} [NOM]", "matrix[NOM]"

def translate_line(line_text: str):
    """Translates a full line of Voynich text into both dialects."""
    tokens = [t for t in re.split(r"[.,\s]+", line_text) if t]
    ven_words, ger_words, eng_words, roles = [], [], [], []
    
    for tok in tokens:
        v_w, g_w, e_w, r = translate_token(tok)
        ven_words.append(v_w)
        ger_words.append(g_w)
        eng_words.append(e_w)
        roles.append(f"{tok}[{r.split('[')[-1].replace(']', '')}]")
        
    return {
        "roles": " ".join(roles),
        "venetian": " ".join(ven_words),
        "german": " ".join(ger_words),
        "operational_english": " ".join(eng_words)
    }

# ---------------------------------------------------------
# EXECUTION & CORPUS AUDIT
# ---------------------------------------------------------
def run_dual_translation():
    print("=" * 80)
    print("VOYNICH MANUSCRIPT: DUAL-DIALECT TRANSLATION RUNNER")
    print("Traditions: Venetian Apothecary vs. Early New High German Distillation")
    print("=" * 80)
    
    sample_corpus = [
        ("f114v.4", "Recipe", "qokedy cheocthedy qoted chedar okeedy daiin chedaiin oky chdam"),
        ("f114v.21", "Recipe", "qokedy otcheodaiin qokchdy"),
        ("f114v.29", "Recipe", "otcheed qopairam"),
        ("f114v.31", "Recipe", "otcheody lkchedy"),
        ("f1r.1", "Herbal", "fachys ykal ar ataiin shol shory"),
        ("f1r.6", "Author Locus", "okchoy otchol chocthy ydaraishy chdam"),
        ("f76r.5", "Bath", "shedy shedaiin lkaiin shedam"),
        ("f82v.19", "Bath", "shedaiin lkaiin ol chedy shedam"),
        ("f116v.1", "Codex Seal", "oror sheey")
    ]
    
    rows = []
    for loc, sec, raw_text in sample_corpus:
        res = translate_line(raw_text)
        rows.append({
            "locus": loc,
            "section": sec,
            "voynich_raw": raw_text,
            "grammatical_roles": res["roles"],
            "venetian_translation": res["venetian"],
            "german_translation": res["german"],
            "operational_english": res["operational_english"]
        })
        
        print(f"\n[{loc}] ({sec})")
        print(f"VOYNICH:      {raw_text}")
        print(f"ROLES:        {res['roles']}")
        print(f"VENETIAN:     {res['venetian']}")
        print(f"EARLY GERMAN: {res['german']}")
        print(f"OP. ENGLISH:  {res['operational_english']}")
        
    # Export full ledger
    out_df = pd.DataFrame(rows)
    out_path = "voynich_dual_dialect_translation.csv"
    out_df.to_csv(out_path, index=False)
    print("\n" + "=" * 80)
    print(f"SUCCESS: Exported dual dialect translations to {out_path}")
    print("=" * 80)

if __name__ == "__main__":
    run_dual_translation()
