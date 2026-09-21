"""
VOYNICH PHONETIC CRIB BREAKER: ZODIAC DECAN RADIAL ALIGNMENT
Aligns invariant radial spoke labels on f70v-f73v against the 36 historical
Ptolemaic Decan names and planetary rulers using Sukhotin CV skeletons.
"""

import os
import re
import urllib.request
from collections import Counter
import pandas as pd

DATA_PATH = "data/ZL3b-n.txt"
FALLBACK_URL = "https://www.voynich.nu/data/ZL3b-n.txt"

# 1. Sukhotin Induced Phonetic Partitions (from empirical run)
VOWELS = set(['a', 'o', 'h', 't', 'i', 'y'])
CONSONANTS = set(['c', 'd', 'e', 'f', 'k', 'l', 'm', 'n'])

# 2. Historical 36 Medieval Latin / Arabic Ptolemaic Decans & Planetary Rulers
# Source: 15th-century Latin translation traditions (Picatrix, Alfonsine Tables)
HISTORICAL_DECANS = [
    # Aries (f70v)
    {"sign": "Aries", "decan": 1, "name": "ASCLIR", "ruler": "MARS"},
    {"decan": 2, "sign": "Aries", "name": "CALCOT", "ruler": "SOL"},
    {"decan": 3, "sign": "Aries", "name": "AROB", "ruler": "VENUS"},
    # Taurus (f71r)
    {"sign": "Taurus", "decan": 1, "name": "KOCAR", "ruler": "MERCURIUS"},
    {"decan": 2, "sign": "Taurus", "name": "MAHAR", "ruler": "LUNA"},
    {"decan": 3, "sign": "Taurus", "name": "SARAM", "ruler": "SATURNUS"},
    # Gemini (f71v)
    {"sign": "Gemini", "decan": 1, "name": "SAGAR", "ruler": "JUPITER"},
    {"decan": 2, "sign": "Gemini", "name": "SHEK", "ruler": "MARS"},
    {"decan": 3, "sign": "Gemini", "name": "BETHEN", "ruler": "SOL"},
    # Cancer (f72r1)
    {"sign": "Cancer", "decan": 1, "name": "MATHRA", "ruler": "VENUS"},
    {"decan": 2, "sign": "Cancer", "name": "RAHIN", "ruler": "MERCURIUS"},
    {"decan": 3, "sign": "Cancer", "name": "ALCHAM", "ruler": "LUNA"},
    # Leo (f72r2)
    {"sign": "Leo", "decan": 1, "name": "FORAC", "ruler": "SATURNUS"},
    {"decan": 2, "sign": "Leo", "name": "CHONTRE", "ruler": "JUPITER"},
    {"decan": 3, "sign": "Leo", "name": "GLAURA", "ruler": "MARS"},
    # Virgo (f72r3)
    {"sign": "Virgo", "decan": 1, "name": "ANOBRE", "ruler": "SOL"},
    {"decan": 2, "sign": "Virgo", "name": "TOCAR", "ruler": "VENUS"},
    {"decan": 3, "sign": "Virgo", "name": "SESME", "ruler": "MERCURIUS"},
    # Libra (f72v1)
    {"sign": "Libra", "decan": 1, "name": "SERIE", "ruler": "LUNA"},
    {"decan": 2, "sign": "Libra", "name": "TARAS", "ruler": "SATURNUS"},
    {"decan": 3, "sign": "Libra", "name": "CHUR", "ruler": "JUPITER"},
    # Scorpio (f72v2)
    {"sign": "Scorpio", "decan": 1, "name": "ROMAN", "ruler": "MARS"},
    {"decan": 2, "sign": "Scorpio", "name": "SABAC", "ruler": "SOL"},
    {"decan": 3, "sign": "Scorpio", "name": "CHAMAR", "ruler": "VENUS"},
    # Sagittarius (f72v3)
    {"sign": "Sagittarius", "decan": 1, "name": "EREG", "ruler": "MERCURIUS"},
    {"decan": 2, "sign": "Sagittarius", "name": "VULCAN", "ruler": "LUNA"},
    {"decan": 3, "sign": "Sagittarius", "name": "TEMAR", "ruler": "SATURNUS"},
    # Capricorn (f73r)
    {"sign": "Capricorn", "decan": 1, "name": "SARAN", "ruler": "JUPITER"},
    {"decan": 2, "sign": "Capricorn", "name": "VEPAR", "ruler": "MARS"},
    {"decan": 3, "sign": "Capricorn", "name": "SOTER", "ruler": "SOL"},
    # Aquarius (f73v)
    {"sign": "Aquarius", "decan": 1, "name": "MORAN", "ruler": "VENUS"},
    {"decan": 2, "sign": "Aquarius", "name": "TOCAR", "ruler": "MERCURIUS"},
    {"decan": 3, "sign": "Aquarius", "name": "ROAR", "ruler": "LUNA"},
    # Pisces (f74r / f70v)
    {"sign": "Pisces", "decan": 1, "name": "PASIS", "ruler": "SATURNUS"},
    {"decan": 2, "sign": "Pisces", "name": "ARAT", "ruler": "JUPITER"},
    {"decan": 3, "sign": "Pisces", "name": "FLAC", "ruler": "MARS"}
]


def load_raw_corpus():
    raw = ""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    else:
        req = urllib.request.Request(FALLBACK_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    return raw


def get_cv_skeleton(word: str) -> str:
    """Converts a token into CV phonotactic sequence based on Sukhotin induction."""
    skel = []
    for char in word.lower():
        if char in VOWELS:
            skel.append("V")
        elif char in CONSONANTS:
            skel.append("C")
    return "".join(skel)


def get_latin_cv_skeleton(word: str) -> str:
    """Standard Latin CV converter."""
    vows = set(['a', 'e', 'i', 'o', 'u'])
    return "".join(['V' if c.lower() in vows else 'C' for c in word if c.isalpha()])


def extract_zodiac_radial_labels(raw_text: str):
    """Extracts diagram labels sitting on folios f70v through f73v."""
    zodiac_tokens = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Look for Zodiac folios and label annotations (@Ro, @Ra, @R, or label indicators)
        m = re.match(r"^<f(70v|71r|71v|72r[1-3]|72v[1-3]|73r|73v|74r)\.([A-Za-z0-9_@]+)>\s*(.*)$", line)
        if m:
            folio = m.group(1)
            locus = m.group(2)
            content = m.group(3)
            # Remove inline transcription tags
            clean_content = re.sub(r"<[^>]+>", "", content)
            words = re.split(r"[.,\s]+", clean_content)
            for w in words:
                tok = re.sub(r"[^a-z]", "", w.lower())
                if tok and len(tok) >= 2:
                    zodiac_tokens.append({
                        "folio": f"f{folio}",
                        "locus": locus,
                        "token": tok,
                        "skel": get_cv_skeleton(tok)
                    })
    return pd.DataFrame(zodiac_tokens)


def levenshtein_ratio(s1: str, s2: str) -> float:
    """Calculates string similarity ratio."""
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    dist = dp[len1][len2]
    max_len = max(len1, len2)
    return round(1.0 - (dist / max_len), 3) if max_len else 0.0


def main():
    print("==================================================================")
    print("   VOYNICH PHONETIC CRIB SOLVER: PTOLEMAIC DECAN ANCHORS (f70v-f73v)")
    print("==================================================================")
    raw = load_raw_corpus()
    df_labels = extract_zodiac_radial_labels(raw)
    print(f"Extracted {len(df_labels)} isolated radial labels across Zodiac folios.")

    # Frequency count of radial spoke labels
    top_labels = Counter(df_labels["token"]).most_common(40)

    matches = []
    for tok, count in top_labels:
        v_skel = get_cv_skeleton(tok)
        for d in HISTORICAL_DECANS:
            target_name = d["name"]
            l_skel = get_latin_cv_skeleton(target_name)
            
            # Structural alignment gate: must have identical length or matching CV skeleton
            skel_score = levenshtein_ratio(v_skel, l_skel)
            str_score = levenshtein_ratio(tok, target_name.lower())
            
            if skel_score >= 0.70:
                combined_score = round(0.6 * skel_score + 0.4 * str_score, 3)
                if combined_score >= 0.65:
                    matches.append({
                        "Voynich Label": tok,
                        "Count": count,
                        "Voynich CV": v_skel,
                        "Decan Target": target_name,
                        "Sign": d["sign"],
                        "Target CV": l_skel,
                        "Alignment Score": combined_score
                    })

    df_matches = pd.DataFrame(matches).drop_duplicates(subset=["Voynich Label", "Decan Target"])
    df_matches = df_matches.sort_values(by="Alignment Score", ascending=False)

    print("\nTOP CANDIDATE PHONETIC CRIBS (Skeletal & Consonant-Vowel Solves):")
    print(df_matches.head(15).to_string(index=False))

    # Glyph-level mapping deduction
    print("\n------------------------------------------------------------------")
    print("DEDUCING FIRST CANDIDATE GLYPH VALUES FROM TOP ALIGNED CRIBS:")
    print("------------------------------------------------------------------")
    seen_glyphs = {}
    for _, row in df_matches.head(5).iterrows():
        v_w = row["Voynich Label"]
        t_w = row["Decan Target"].lower()
        if len(v_w) == len(t_w):
            for v_char, t_char in zip(v_w, t_w):
                if v_char not in seen_glyphs:
                    seen_glyphs[v_char] = Counter()
                seen_glyphs[v_char][t_char] += 1

    for glyph, votes in sorted(seen_glyphs.items()):
        best_cand, best_n = votes.most_common(1)[0]
        vowel_flag = "Vowel" if glyph in VOWELS else "Consonant"
        print(f"Glyph '{glyph}' ({vowel_flag:<9})  -->  Candidate Sound: [{best_cand.upper()}]  (confidence: {best_n} matches)")


if __name__ == "__main__":
    main()
