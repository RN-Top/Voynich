"""
Published semantic dictionary (glosses) for the workbench.

Kept separate from app.py so validation scripts can import it without
starting Streamlit. These glosses are hypotheses, not validated readings:
see VALIDATION.md.
"""

MASTER_LEXICON = {
    "ydaraishy": {"la": "auctor", "ven": "fatto da l'auctor", "ger": "gemacht von meister", "en": "author / composed by", "role": "OPERAND_NOUN", "domain": "Colophon"},
    "ytchas": {"la": "scriptor", "ven": "scritto da lo scriptor", "ger": "geschriben vom schreiber", "en": "scribe / written by", "role": "OPERAND_NOUN", "domain": "Colophon"},
    "oror": {"la": "finis", "ven": "fin / saldo", "ger": "ende / bschluss", "en": "terminal sign-off marker", "role": "TERMINAL_FLUSH", "domain": "Seal"},
    "daiin": {"la": "aqua / decoctio", "ven": "agva", "ger": "wazzer", "en": "water / liquid vehicle", "role": "OPERAND_NOUN", "domain": "Solvent"},
    "shedy": {"la": "radix", "ven": "radise", "ger": "wurtz", "en": "rootstock / apparatus base", "role": "OPERAND_NOUN", "domain": "Botanical"},
    "chedy": {"la": "herba / planta", "ven": "erba", "ger": "krut", "en": "herb / botanical matter", "role": "OPERAND_NOUN", "domain": "Botanical"},
    "qokedy": {"la": "coque", "ven": "coci", "ger": "sied", "en": "boil / apply heat", "role": "OPERATOR_VERB", "domain": "Compounding"},
    "qokeey": {"la": "misce", "ven": "mescola", "ger": "mische", "en": "mix / blend thoroughly", "role": "OPERATOR_VERB", "domain": "Compounding"},
    "qokal": {"la": "distilla", "ven": "destilla", "ger": "brenne", "en": "distill / drip extract", "role": "OPERATOR_VERB", "domain": "Compounding"},
    "otcheod": {"la": "stella / signum", "ven": "stella", "ger": "sternort", "en": "celestial star sector", "role": "OPERAND_NOUN", "domain": "Astronomical"},
    "otcheodaiin": {"la": "stella [rel.]", "ven": "licore de stella", "ger": "sternauszug", "en": "star sector [buffer hold]", "role": "OPERAND_NOUN", "domain": "Astronomical"},
    "otcheody": {"la": "vas [stat.]", "ven": "vaso", "ger": "kolben", "en": "star sector [receiver vessel]", "role": "OPERAND_NOUN", "domain": "Astronomical"},
    "opairam": {"la": "solve [term.]", "ven": "spandi / cola", "ger": "lass auslauffen", "en": "extract / dissolve [flush]", "role": "TERMINAL_FLUSH", "domain": "Compounding"},
    "qopairam": {"la": "solve [proc.]", "ven": "spandi / cola [proc.]", "ger": "lass auslauffen [proc.]", "en": "extract / dissolve [active]", "role": "TERMINAL_FLUSH", "domain": "Compounding"},
    "chol": {"la": "calidus", "ven": "caldo", "ger": "heiss", "en": "warm / hot property", "role": "MODIFIER_ADJ", "domain": "Humoral"},
    "chor": {"la": "siccus", "ven": "asciutto", "ger": "gedoert", "en": "dry / desiccated property", "role": "MODIFIER_ADJ", "domain": "Humoral"},
    "oteod": {"la": "gradus", "ven": "grado", "ger": "gradzaichen", "en": "degree / sector coordinate", "role": "OPERAND_NOUN", "domain": "Astronomical"},
    "chdam": {"la": "finis", "ven": "saldo / serra", "ger": "beschliess", "en": "complete / terminal flush", "role": "TERMINAL_FLUSH", "domain": "Compounding"},
}
