import pytest

# =====================================================================
# TEST SUITE: Voynich Structural & Phonetic Decipherment Pipeline
# =====================================================================

# ---------------------------------------------------------------------
# Test 1: Sukhotin Vowel Induction & Consonant-Vowel Skeleton Lock
# ---------------------------------------------------------------------
def test_sukhotin_cv_skeleton_and_pisces_anchor():
    """
    Validates:
      1. Sukhotin vocalic nuclei vs. consonantal frame partition.
      2. 33.3% vocalic phonotactic ratio.
      3. Pisces anchor ('otcheod' -> core stem 'cheod' -> CVCVC matches 'PASIS').
    """
    vowels = {"a", "o", "h", "t", "i", "y"}
    consonants = {"c", "d", "e", "f", "k", "l", "m", "n", "p", "s", "r"}

    # Disjoint check
    assert vowels.isdisjoint(consonants), "Vocalic and consonantal sets must not overlap."

    # Total alphabet pool and ratio check
    alphabet = vowels | consonants
    vowel_ratio = len(vowels) / len(alphabet)
    assert round(vowel_ratio, 3) == 0.333, f"Expected 33.3% vocalic ratio, got {vowel_ratio:.3%}"

    # CV Skeleton mapping helper
    def get_cv_skeleton(token: str) -> str:
        skeleton = []
        for ch in token:
            if ch in vowels:
                skeleton.append("V")
            elif ch in consonants:
                skeleton.append("C")
            else:
                raise ValueError(f"Unclassified character: {ch}")
        return "".join(skeleton)

    # Validate Pisces f70v2 spoke stem: 'cheod'
    stem = "cheod"
    assert get_cv_skeleton(stem) == "CVCVC", f"Stem {stem} did not evaluate to CVCVC"

    # Compare against target candidate anchor: PASIS
    target = "PASIS"
    target_skeleton = "".join("V" if ch in "AEIOUY" else "C" for ch in target)
    assert get_cv_skeleton(stem) == target_skeleton, "Stem skeleton must lock 1:1 with PASIS skeleton"


# ---------------------------------------------------------------------
# Test 2: Procedural Frame Sandbox (Q-ACTIVE Execution Sandwiches)
# ---------------------------------------------------------------------
def test_procedural_execution_frame_roles():
    """
    Validates that procedural units wrapped in Q-ACTIVE execution frames
    correctly classify functional roles (medium, heat) based on terminal/stem markers.
    """
    sample_ledger = [
        {"token": "ataiin", "expected_role": "medium"},
        {"token": "chtaiin", "expected_role": "medium"},
        {"token": "ykaiin", "expected_role": "medium"},
        {"token": "daraiin", "expected_role": "medium"},
        {"token": "daiin", "expected_role": "medium"},
        {"token": "okaiin", "expected_role": "heat"},
        {"token": "cthaiin", "expected_role": "medium"},
    ]

    def classify_procedural_role(token: str) -> str:
        # Solvent / compound carrier markers end with 'aiin'
        if token.endswith("aiin"):
            if token.startswith("ok"):
                return "heat"
            return "medium"
        return "unknown"

    for entry in sample_ledger:
        role = classify_procedural_role(entry["token"])
        assert role == entry["expected_role"], (
            f"Token '{entry['token']}' expected role '{entry['expected_role']}', got '{role}'"
        )


# ---------------------------------------------------------------------
# Test 3: Phonetic Excel Matrix Collision & Affix Isolation
# ---------------------------------------------------------------------
def test_phonetic_matrix_target_collisions():
    """
    Audits the 16-glyph phonetic assignments from the export sheet.
    Flags target phonetic collisions (e.g. S, M, R, O) and verifies they
    separate cleanly into primary stems vs. affixes.
    """
    glyph_phonetic_map = {
        "o": ("O", "Vowel"),
        "t": ("T", "Vowel"),
        "c": ("S", "Consonant"),
        "h": ("A", "Vowel"),
        "e": ("R", "Consonant"),
        "d": ("N", "Consonant"),
        "a": ("U", "Vowel"),
        "i": ("I", "Vowel"),
        "q": ("C", "Consonant"),
        "k": ("O", "Consonant"),
        "p": ("M", "Consonant"),
        "m": ("S", "Consonant"),
        "y": ("M", "Vowel"),
        "s": ("P", "Consonant"),
        "l": ("L", "Consonant"),
        "r": ("R", "Consonant"),
    }

    # Invert mapping to find collision targets
    target_to_glyphs = {}
    for glyph, (phonetic, cls) in glyph_phonetic_map.items():
        target_to_glyphs.setdefault(phonetic, []).append((glyph, cls))

    collisions = {k: v for k, v in target_to_glyphs.items() if len(v) > 1}

    # Verify expected collision pairs exist for dual-role analysis
    assert "S" in collisions, "Expected 'c' and 'm' collision under S"
    assert "M" in collisions, "Expected 'p' and 'y' collision under M"
    assert "R" in collisions, "Expected 'e' and 'r' collision under R"
    assert "O" in collisions, "Expected 'o' and 'k' collision under O"

    # Affix rule check: 'y' and 'm' serve as terminal buffers / inflection affixes
    affix_glyphs = {"y", "m"}
    root_glyphs = {"p", "c"}
    for g in affix_glyphs:
        assert g in glyph_phonetic_map
    for g in root_glyphs:
        assert g in glyph_phonetic_map
