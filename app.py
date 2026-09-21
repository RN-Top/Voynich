"""
VOYNICH & HISTORICAL CONTROL FREQUENCY & ENTROPY COMPARATOR
Module: frequency_analysis.py
Appends character-level, word-level, entropy, and harmonic repetition analysis
comparing the Voynich text against Medieval Latin, Early Tuscan Italian,
and the alchemical Turba Philosophorum.
"""

import math
import re
from collections import Counter
import numpy as np
import pandas as pd

# -------------------------------------------------------------------------
# 1. CORPUS REPOSITORY & HISTORICAL CONTROLS
# -------------------------------------------------------------------------
VOYNICH_SAMPLE = """
fachys ykal ar ataiin shol shory cthores y kor sholdy ydaraishy
daiin chedy qokedy chdam otcheodaiin qokchdy otedal dain aral qokedy
dshedal qoteody choddy otol chedal otain chedol chedain shedy qotched dl
oeos qotcheo odain qotain otar qotchd dol qotchedy choty ol lchdaiin dal
qokedy cheocthedy qoted qotedol chedar qotedy okeedy daiin chedaiin oky
chedy qokeedy okaly cheedain shedy qokedy otcheodaiin qokchdy
otcheed qopairam otcheody lkchedy sory ckhar or y kair chtaiin shar ase cthar cthar dan
syaiir sheky or ykaiin shod cthoary cthes daraiin sy soiin oteey oteo roloty cthiar daiin okaiin or okan
sair y chear cthaiin cphar cfhaiin oror sheey qokedy chdam
ytchas oraiin chkor qokedy qokeey or or or chkorol otey qokedy lkedy chdy qokchdy qokal chdam
otcheod oteodal opairam okeal otcheor dal otol otedy qokedy otcheodaiin qopairam otcheody daiin chedy
"""

MEDIEVAL_LATIN = """
herba artemisia uirtutes habet multas quarum prima est contra uenenum et morsus serpentum.
radix eius trita et cum uino potata uulnera sanat et dolores matricis mitigat.
decoctio quoque illius in aqua calida confert hydropicis et iuncturarum doloribus.
si quis eam secum portauerit nullum malum uenenosum sibi nocere poterit.
colligitur autem mense augusto ante solis ortum et siccatur in umbra uirtute seruata.
pulvis ipsius datus cum lacte calido celeriter expellit uenenum et restaurat uires.
succus foliorum recens expressus uulneribus antiquis prodest et putredinem tollit.
misceatur cum oleo rosaceo et cerusa ad calores sedandos et inflammationes curandas.
"""

EARLY_TUSCAN = """
nel mezzo del cammin di nostra vita mi ritrovai per una selva oscura che la diritta via era smarrita.
ahi quanto a dir qual era e cosa dura esta selva selvaggia e aspra e forte che nel pensier rinova la paura.
tant e amara che poco e piu morte ma per trattar del ben ch i vi trovai diro de l altre cose ch i v ho scorte.
io non so ben ridir com i v intrai tant era pien di sonno a quel punto che la verace via abbandonai.
ma poi ch i fui al pie d un colle giunto la dove terminava quella valle che m avea di paura il cor compunto
guardai in alto e vidi le sue spalle vestite gia de raggi del pianeta che mena dritto altrui per ogne calle.
"""

TURBA_PHILOSOPHORUM = """
scitote o investigatores huius artis quod natura non agit nisi in sua simili et ubi non est calor ibi nihil generatur.
ignis enim noster est unicus et materia una cuius decoctio fit in vase sigillato donec omnia vertantur in liquorem purum.
cumque videritis nigredinem apparere scitote quod spiritus corpori coniunctus est et anima incipit reviviscere.
facite ergo albificationem et postea rubificationem per calorem lentum et continuum non cessantem.
aqua nostra est ignis et ignis aqua et haec est occultatio sapientum quam stulti non intelligunt.
aer enim retinet calorem et terra nutrit aquam et omnia quattuor elementa in unum corpus rediguntur.
"""

# -------------------------------------------------------------------------
# 2. METRIC CALCULATION ENGINE
# -------------------------------------------------------------------------
def clean_corpus(raw_text: str):
    tokens = [re.sub(r'[^a-z]', '', w.lower()) for w in raw_text.split() if w.strip()]
    tokens = [t for t in tokens if t]
    chars = [c for c in "".join(tokens) if c.isalpha()]
    return tokens, chars

def shannon_entropy(elements: list) -> float:
    if not elements:
        return 0.0
    counts = Counter(elements)
    n = len(elements)
    return -sum((cnt / n) * math.log2(cnt / n) for cnt in counts.values())

def compute_corpus_profile(name: str, raw_text: str) -> dict:
    tokens, chars = clean_corpus(raw_text)
    n_tokens = len(tokens)
    n_chars = len(chars)

    # 1. Character distributions & entropy
    h1 = shannon_entropy(chars)
    bigrams = [chars[i] + chars[i + 1] for i in range(n_chars - 1)]
    h2 = shannon_entropy(bigrams)

    # 2. Word-level frequency and repetition metrics
    word_counts = Counter(tokens)
    ttr = len(word_counts) / n_tokens if n_tokens else 0.0
    h_word = shannon_entropy(tokens)

    # Immediate word duplication (w_i == w_{i+1})
    immediate_word_repeats = sum(1 for i in range(n_tokens - 1) if tokens[i] == tokens[i + 1])
    word_repeat_rate = (immediate_word_repeats / (n_tokens - 1)) * 100.0 if n_tokens > 1 else 0.0

    # Geminate characters (c_i == c_{i+1})
    char_repeats = sum(1 for i in range(n_chars - 1) if chars[i] == chars[i + 1])
    char_repeat_rate = (char_repeats / (n_chars - 1)) * 100.0 if n_chars > 1 else 0.0

    # Auto-correlation lag-1 (harmonic lock indicator)
    # Binary vector of matching consecutive words
    lag1_overlap = sum(1 for i in range(n_tokens - 1) if tokens[i] in tokens[i+1:]) / n_tokens if n_tokens else 0.0

    return {
        "Corpus": name,
        "Tokens": n_tokens,
        "Vocabulary": len(word_counts),
        "TTR": round(ttr, 3),
        "Word Entropy (H)": round(h_word, 2),
        "Char H1 (bits)": round(h1, 2),
        "Bigram H2 (bits)": round(h2, 2),
        "Immediate Word Repeats (%)": f"{word_repeat_rate:.2f}%",
        "Geminate Chars (%)": f"{char_repeat_rate:.2f}%",
        "Lag Recurrence": round(lag1_overlap, 3)
    }

# -------------------------------------------------------------------------
# 3. EXECUTION AND TABLE GENERATION
# -------------------------------------------------------------------------
def run_frequency_comparison():
    corpora = [
        ("Voynich Manuscript", VOYNICH_SAMPLE),
        ("Medieval Latin (Herbal)", MEDIEVAL_LATIN),
        ("Early Tuscan Italian", EARLY_TUSCAN),
        ("Turba Philosophorum (Alchemy)", TURBA_PHILOSOPHORUM)
    ]

    metrics = [compute_corpus_profile(label, text) for label, text in corpora]
    df_metrics = pd.DataFrame(metrics)
    return df_metrics

if __name__ == "__main__":
    df = run_frequency_comparison()
    print(df.to_string(index=False))
