"""
VOYNICH APPARATUS CONTRACT (FROZEN) - CORE CONSTANTS & SCORECARD
Read-only contract specifications. Append-only. Do not retune.
"""

LOCKED_ROLES = {
    "heat": {"prefixes": ["qo", "qok", "ok"], "color": "#FF0000", "label": "heat/start"},
    "medium": {"tokens": ["daiin"], "suffixes": ["aiin", "ain"], "color": "#00FFFF", "label": "medium"},
    "outlet": {"suffixes": ["ol", "al"], "color": "#FFA500", "label": "outlet"},
    "reflux": {"suffixes": ["or", "ar"], "color": "#800080", "label": "reflux"},
    "retain": {"prefixes": ["shed"], "color": "#008000", "label": "retain"},
    "drain": {"tokens": ["chdam", "shedam"], "suffixes": ["am", "m", "dam"], "color": "#000000", "label": "drain/close"},
    "unmapped": {"color": "#808080", "label": "unmapped"}
}

LOCKED_CYCLE = "C (heat) -> L (medium) -> route (outlet|reflux) -> P (retain) -> R (drain)"

CACHED_SCORECARD = {
    "T-zone": {"claim": "wheels suppress heat+drain", "status": "PASSED", "score": "0.0% heat/drain"},
    "T-bath": {"claim": "baths enrich retain+drain", "status": "PASSED", "score": "> 40.0% load"},
    "T-pie": {"claim": "no role > 80%", "status": "PASSED", "score": "34.2% peak single role"},
    "T-split": {"claim": "rings != prose", "status": "PASSED", "score": "Coordinate vs operational prose split"},
    "T-path": {"claim": "cycle appears in running text", "status": "PASSED", "score": "C -> L -> P -> R sequence"},
    "T-internal-key": {"claim": "picture class flips role mix", "status": "PASSED", "score": ">= 8 folios flip"},
    "drainage": {"claim": "-m/-am line-final enrichment", "status": "PASSED", "score": "Odds ratio > 20x (p < 0.001)"}
}

LANGUAGE_STANCE = {
    "BT-3_latin_pharma": "0.0% (confirmed negative result; Latin letter-swap rejected)",
    "BT-1_enhg_probe": "14.3% (stored probe rate only; not decoded words)",
    "BT-2_venetian_probe": "11.8% (stored probe rate only; not decoded words)",
    "name_bans": "Pisis, Mars, Aries, PASIS, LUNA are coordinate anchors, NOT decoded plaintext"
}

PHYSICAL_SPOTS = {
    "FRONT_LOCK": ["f1r", "f1v", "f2r"],
    "MIDDLE_HINGE": {
        "CENTER": "crease / middle rosette",
        "LEFT_WING": "f85v panels",
        "RIGHT_WING": "f86r panels"
    },
    "BACK_LOCK": ["f116r", "f116v"]
}

def q14_safety_check(role_counts: dict):
    tot = sum(role_counts.values())
    if tot == 0:
        return "N=0 (EMPTY)"
    for role, count in role_counts.items():
        if count == tot:
            status = f"100% {role.upper()} (N={tot})"
            if tot < 30:
                status += " [SMALL-N: INVALID BEAK/HUB PROOF]"
            return status
    return f"BALANCED (N={tot})"
