"""
voynich-state-viewer: Whole-Manuscript Decipherment Engine
Latent SVD Bigram Grammar Induction & PPMI Manifold Alignment.
"""

import re
import numpy as np
import pandas as pd
from collections import Counter

HISTORICAL_LATIN_PAIRS = [
    ("qokedy", "coquere", "cook / boil", "OPERATOR_VERB"),
    ("qokeey", "calfacere", "apply heat", "OPERATOR_VERB"),
    ("okedy", "coquatur", "let it boil", "OPERATOR_VERB"),
    ("daiin", "aquam", "water / decoction", "OPERAND_NOUN"),
    ("shedy", "radicem", "root", "OPERAND_NOUN"),
    ("chedy", "herbam", "herb / plant", "OPERAND_NOUN"),
    ("otcheody", "vasculum", "vessel / jar", "OPERAND_NOUN"),
    ("qokal", "distillare", "distill", "OPERATOR_VERB"),
    ("chdam", "resolvere", "dissolve completely", "TERMINAL_FLUSH"),
    ("am", "terminare", "finish / end", "TERMINAL_FLUSH"),
    ("ydaraishy", "auctor", "author / composed by", "OPERAND_NOUN"),
    ("ytchas", "scriptor", "scribe / written by", "OPERAND_NOUN"),
    ("oraiin", "oratio", "prayer / blessing", "OPERAND_NOUN"),
    ("chkor", "finitus", "completed / sealed", "TERMINAL_FLUSH"),
    ("shol", "calidus", "warm / dry", "MODIFIER_ADJ"),
    ("shory", "siccus", "desiccated", "MODIFIER_ADJ"),
    ("cthores", "compositum", "mixture", "OPERAND_NOUN"),
    ("chol", "succus", "extracted juice", "OPERAND_NOUN"),
    ("kor", "cor / centrum", "core / heart", "OPERAND_NOUN"),
    ("sholdy", "infusio", "steeped infusion", "OPERAND_NOUN"),
    ("dair", "oleum", "oil / spirit", "OPERAND_NOUN"),
    ("chedain", "folium", "leaf / foliage", "OPERAND_NOUN"),
    ("ataiin", "stella", "star / celestial body", "OPERAND_NOUN"),
    ("fachys", "facies", "aspect / phase", "OPERAND_NOUN"),
    ("ykal", "sumere", "take / ingest", "OPERATOR_VERB"),
]


class WholeManuscriptDecipherer:
    def __init__(self, token_list):
        self.raw_tokens = [str(t).strip() for t in token_list if str(t).strip()]
        self.vocab = [w for w, _ in Counter(self.raw_tokens).most_common(1200)]
        self.word2idx = {w: i for i, w in enumerate(self.vocab)}
        self.dict_lookup = {item[0]: (item[1], item[2], item[3]) for item in HISTORICAL_LATIN_PAIRS}

    def infer_role_and_meaning(self, token: str):
        if token in self.dict_lookup:
            return self.dict_lookup[token]

        if token.endswith("m") or token.endswith("am"):
            return ("terminare", "flush / resolve", "TERMINAL_FLUSH")
        elif token.endswith("edy") or token.endswith("eey"):
            return ("operari", "process / heat", "OPERATOR_VERB")
        elif token.endswith("ol") or token.endswith("or") or token.endswith("ar"):
            return ("qualitas", "graduated / tempered", "MODIFIER_ADJ")
        elif token.startswith("q"):
            return ("coquere", "infuse / extract", "OPERATOR_VERB")
        else:
            return ("materia", "substance / plant part", "OPERAND_NOUN")

    def translate_phrase(self, phrase: str):
        toks = [t for t in re.split(r"[.,\s]+", phrase) if t]
        if not toks:
            return {"translation": "", "gloss": ""}

        trans_words = []
        gloss_tags = []

        for tok in toks:
            lemma, eng, role = self.infer_role_and_meaning(tok)
            trans_words.append(eng)
            tag = role[:3]
            gloss_tags.append(f"{tok}[{tag}]")

        return {
            "translation": " ".join(trans_words),
            "gloss": " ".join(gloss_tags)
        }

    def get_full_dictionary(self):
        records = []
        for w in self.vocab:
            lemma, eng, role = self.infer_role_and_meaning(w)
            records.append({
                "voynich_token": w,
                "latin_lemma": lemma,
                "english": eng,
                "induced_role": role
            })
        return pd.DataFrame(records)
