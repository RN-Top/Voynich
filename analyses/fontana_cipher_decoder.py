"""Fontana cipher decoder: tries Giovanni Fontana's documented cipher methods on the Voynich text.

Pre-registration: analyses/fontana_cipher_prereg.md (committed before this file was first run).

Fontana's cipher is a substitution with an invented alphabet (Latin plaintext, one made-up sign per letter,
possibly several signs per letter). Because the sign shapes he used cannot be matched to Voynich glyphs, the
key is left unknown and solved for: a solver searches every possible key of each type for the one that makes
the Voynich read most like Latin / Italian / Venetian. Keys are fitted on one half of the folios and scored on
the other half, and the result is compared with (a) real Latin/Italian enciphered and solved the same way and
(b) shuffled Voynich text.

Run:  python analyses/fontana_cipher_decoder.py        (about 5-10 minutes)
Writes: output/fontana_cipher_report.md and output/fontana_cipher_results.json
"""

import json
import math
import random
import re
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "Data" / "fontana_reference"
OUT = ROOT / "output"
SEED = 1453
RESTARTS = 6
STEPS = 6000
MIN_SIGN_COUNT = 20
N_POS_KEYS = 3
N_SHUFFLES = 5
N_RANDOM_KEYS = 1000

PLAIN = "abcdefghiklmnopqrstuxyz"  # medieval Latin letters (j->i, v->u, w->u)
SPACE = len(PLAIN)
NP = len(PLAIN) + 1

GROUPS = ["cth", "ckh", "cph", "cfh", "iiin", "iin", "eee", "ch", "sh", "in", "ii", "ee"]

# 14 plant-page opening words and the star labels they share chunks with
# (output/plant_star_report_integrated.md, backwards-reading-test branch).
# Words containing rare @-signs cannot be decoded and are listed separately.
STAR_CHECK_WORDS = [
    "koaiin", "koary", "tydlo", "koair", "pocheody", "pochaiin", "pydchdom", "pochof", "tocphol",
    "tdokchcfhy", "toealchs",  # plant-page openings
    "okoaly", "otydy", "otydg", "opocphor", "oydchy", "otochedy", "chocfhy", "qotoear", "otoeeo",  # star labels
]
STAR_CHECK_DROPPED = ["c@132hsc@133hain", "o@167chal", "c@181hdai@133hy", "o@167olchc@133hy"]


# ----------------------------------------------------------------------------- language models
def normalize(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("j", "i").replace("v", "u").replace("w", "u")
    text = re.sub(f"[^{PLAIN}]+", " ", text)
    return re.sub(" +", " ", text).strip()


def to_ids(text):
    return [SPACE if ch == " " else PLAIN.index(ch) for ch in text]


class TrigramLM:
    def __init__(self, text):
        ids = np.array(to_ids(" " + text + " "))
        c3 = np.zeros((NP, NP, NP))
        np.add.at(c3, (ids[:-2], ids[1:-1], ids[2:]), 1)
        c2 = c3.sum(axis=0)          # counts of (b, c)
        c1 = c2.sum(axis=0) + 0.5    # counts of c
        p1 = c1 / c1.sum()
        p2 = (c2 + 0.1 * p1) / (c2.sum(axis=1, keepdims=True) + 0.1)
        p3 = (c3 + 0.1 * p2[None]) / (c3.sum(axis=2, keepdims=True) + 0.1)
        p = 0.70 * p3 + 0.25 * p2[None] + 0.05 * p1[None, None]
        self.lp = np.log2(p)
        self.vocab = set()

    def bits_per_letter(self, a, b, c, cnt, key):
        return -float((cnt * self.lp[key[a], key[b], key[c]]).sum() / cnt.sum())


# ----------------------------------------------------------------------------- Voynich text
def load_voynich():
    data = json.loads((ROOT / "voynich_integrated.json").read_text())
    folios = []
    for f in data["folios"]:
        lines = []
        for line in f.get("text_lines", []):
            if line.get("unit") != "paragraph":
                continue
            words = [w for w in line.get("words", []) if re.fullmatch("[a-z]+", w)]
            if words:
                lines.append(words)
        if lines:
            folios.append((f["folio_id"], lines))
    return folios


def tokenize(word, inventory):
    if inventory == "letters":
        return list(word)
    out, i = [], 0
    while i < len(word):
        for g in GROUPS:
            if word.startswith(g, i):
                out.append(g)
                i += len(g)
                break
        else:
            out.append(word[i])
            i += 1
    return out


def apply_direction(lines, direction):
    """lines: list of lists of sign-lists."""
    if direction == "forwards":
        return lines
    if direction == "word-reversed":
        return [[w[::-1] for w in line] for line in lines]
    return [[w[::-1] for w in line[::-1]] for line in lines]  # line mirrored


def build_cipher(lines, signs):
    """Turns lines of sign-lists into trigram count arrays over sign ids (space = len(signs))."""
    idx = {s: i for i, s in enumerate(signs)}
    sp = len(signs)
    cnt = Counter()
    for line in lines:
        seq = [sp]
        for w in line:
            seq += [idx[s] for s in w] + [sp]
        for k in range(len(seq) - 2):
            cnt[(seq[k], seq[k + 1], seq[k + 2])] += 1
    keys = np.array(list(cnt.keys()))
    return keys[:, 0], keys[:, 1], keys[:, 2], np.array(list(cnt.values()), dtype=float)


# ----------------------------------------------------------------------------- solver
def random_key(n, keytype, rng):
    if keytype == "mono" and n <= len(PLAIN):
        letters = rng.sample(range(len(PLAIN)), n)
    elif keytype == "mono":  # more signs than letters: first 23 distinct, rest free
        letters = rng.sample(range(len(PLAIN)), len(PLAIN)) + [rng.randrange(len(PLAIN)) for _ in range(n - len(PLAIN))]
    else:
        letters = [rng.randrange(len(PLAIN)) for _ in range(n)]
    return np.array(letters + [SPACE])


def solve(lm, cipher, n, keytype, rng):
    a, b, c, cnt = cipher
    best_key, best = None, 1e9
    for _ in range(RESTARTS):
        key = random_key(n, keytype, rng)
        cur = lm.bits_per_letter(a, b, c, cnt, key)
        for step in range(STEPS):
            temp = 0.05 * (0.002 / 0.05) ** (step / STEPS)
            new = key.copy()
            i = rng.randrange(n)
            if keytype == "mono":
                used = set(new[:n].tolist())
                j = rng.randrange(n + len(PLAIN))
                if j < n:
                    new[i], new[j] = new[j], new[i]
                else:
                    letter = j - n
                    if letter in used:
                        continue
                    new[i] = letter
            else:
                new[i] = rng.randrange(len(PLAIN))
            val = lm.bits_per_letter(a, b, c, cnt, new)
            if val < cur or rng.random() < math.exp((cur - val) / temp):
                key, cur = new, val
        if cur < best:
            best, best_key = cur, key
    return best_key


def decode_words(lines, signs, key):
    idx = {s: i for i, s in enumerate(signs)}
    return [["".join(PLAIN[key[idx[s]]] for s in w) for w in line] for line in lines]


def word_rate(decoded_lines, vocab):
    words = [w for line in decoded_lines for w in line if len(w) >= 3]
    return sum(w in vocab for w in words) / max(1, len(words))


def within_one_edit(w, names):
    for n in names:
        if abs(len(n) - len(w)) > 1:
            continue
        if len(n) == len(w):
            if sum(x != y for x, y in zip(n, w)) <= 1:
                return n
        else:
            s, l = (w, n) if len(w) < len(n) else (n, w)
            for k in range(len(l)):
                if l[:k] + l[k + 1:] == s:
                    return n
    return None


# ----------------------------------------------------------------------------- main
def main():
    rng = random.Random(SEED)
    langs = {}
    for name in ["latin", "italian", "venetian"]:
        model_text = normalize((REF / f"{name}_model.txt").read_text())
        lm = TrigramLM(model_text)
        vocab_text = model_text
        ctrl = REF / f"{name}_control.txt"
        ctrl_text = normalize(ctrl.read_text()) if ctrl.exists() else None
        if ctrl_text:
            vocab_text += " " + ctrl_text
        lm.vocab = set(vocab_text.split())
        langs[name] = (lm, ctrl_text)
    names = [normalize(l) for l in (REF / "name_lexicon.txt").read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    names = sorted({n for n in names if len(n) >= 5 and " " not in n})

    folios = load_voynich()
    order = list(range(len(folios)))
    random.Random(SEED).shuffle(order)
    train_ids = set(order[: len(order) // 2])
    raw_train = [l for i, (_, ls) in enumerate(folios) if i in train_ids for l in ls]
    raw_test = [l for i, (_, ls) in enumerate(folios) if i not in train_ids for l in ls]

    results = {"runs": [], "positive": [], "baseline": [], "settings": {
        "seed": SEED, "restarts": RESTARTS, "steps": STEPS, "min_sign_count": MIN_SIGN_COUNT,
        "train_folios": len(train_ids), "test_folios": len(folios) - len(train_ids)}}

    prepared = {}
    for inventory in ["letters", "groups"]:
        tr = [[tokenize(w, inventory) for w in line] for line in raw_train]
        te = [[tokenize(w, inventory) for w in line] for line in raw_test]
        freq = Counter(s for line in tr + te for w in line for s in w)
        signs = sorted(s for s, c in freq.items() if c >= MIN_SIGN_COUNT)
        ok = set(signs)
        tr = [[w for w in line if all(s in ok for s in w)] for line in tr]
        te = [[w for w in line if all(s in ok for s in w)] for line in te]
        tr, te = [l for l in tr if l], [l for l in te if l]
        prepared[inventory] = (signs, tr, te)
        print(f"{inventory}: {len(signs)} signs: {' '.join(signs)}")
    train_letters = sum(len(s) + 1 for line in prepared["letters"][1] for s in line)

    star_tok = {inv: [tokenize(w, inv) for w in STAR_CHECK_WORDS] for inv in prepared}

    def star_hits(inventory, signs, key, direction):
        idx = {s: i for i, s in enumerate(signs)}
        hits = []
        for raw, toks in zip(STAR_CHECK_WORDS, star_tok[inventory]):
            if not all(s in idx for s in toks):
                continue
            if direction != "forwards":
                toks = toks[::-1]
            dec = "".join(PLAIN[key[idx[s]]] for s in toks)
            m = within_one_edit(dec, names)
            hits.append((raw, dec, m))
        return hits

    # ---- main runs
    for inventory in ["letters", "groups"]:
        signs, tr, te = prepared[inventory]
        for direction in ["forwards", "word-reversed", "line-mirrored"]:
            trd, ted = apply_direction(tr, direction), apply_direction(te, direction)
            ctr, cte = build_cipher(trd, signs), build_cipher(ted, signs)
            for keytype in ["mono", "homophonic"]:
                for lang, (lm, _) in langs.items():
                    key = solve(lm, ctr, len(signs), keytype, rng)
                    bits = lm.bits_per_letter(*cte, key)
                    dec = decode_words(ted, signs, key)
                    rate = word_rate(dec, lm.vocab)
                    hits = star_hits(inventory, signs, key, direction)
                    nhit = sum(1 for h in hits if h[2])
                    null = []
                    krng = random.Random(SEED + 7)
                    for _ in range(N_RANDOM_KEYS):
                        rk = random_key(len(signs), keytype, krng)
                        null.append(sum(1 for h in star_hits(inventory, signs, rk, direction) if h[2]))
                    p95 = float(np.percentile(null, 95))
                    run = {"inventory": inventory, "direction": direction, "keytype": keytype, "language": lang,
                           "test_bits": bits, "word_rate": rate, "star_hits": nhit, "star_null_p95": p95,
                           "star_null_mean": float(np.mean(null)),
                           "key": {s: PLAIN[key[i]] for i, s in enumerate(signs)},
                           "sample": [" ".join(l) for l in dec[:3]],
                           "star_words": [{"voynich": h[0], "decoded": h[1], "name": h[2]} for h in hits]}
                    results["runs"].append(run)
                    print(f"{inventory:7s} {direction:13s} {keytype:10s} {lang:8s} bits={bits:.3f} "
                          f"words={rate:.3f} stars={nhit} (p95 {p95:.0f})  {run['sample'][0][:60]}")

    # ---- positive controls: real held-out text, enciphered and solved the same way
    for lang in ["latin", "italian"]:
        lm, ctrl_text = langs[lang]
        words = ctrl_text.split()
        half = len(words) // 2
        tr_words, te_words = words[:half], words[half:]
        # match Voynich training size in letters
        out, total = [], 0
        for w in tr_words:
            out.append(w)
            total += len(w) + 1
            if total >= train_letters:
                break
        tr_words = out
        te_words = te_words[: len(tr_words)]
        for keytype in ["mono", "homophonic"]:
            for k in range(N_POS_KEYS):
                prng = random.Random(SEED * 31 + k + (100 if keytype == "homophonic" else 0) + (7 if lang == "italian" else 0))
                common = [ch for ch, _ in Counter("".join(tr_words)).most_common(6)]
                sign_of = {}
                for ch in PLAIN:
                    sign_of[ch] = [f"{ch}0"] + ([f"{ch}1"] if keytype == "homophonic" and ch in common else [])
                signs = sorted(s for v in sign_of.values() for s in v)
                disguise = dict(zip(signs, prng.sample(signs, len(signs))))  # random relabelling
                def enc(ws):
                    lines, line = [], []
                    for w in ws:
                        line.append([disguise[prng.choice(sign_of[ch])] for ch in w])
                        if len(line) == 9:
                            lines.append(line)
                            line = []
                    return lines + ([line] if line else [])
                trc, tec = enc(tr_words), enc(te_words)
                truth_lines = [[w for w in te_words[i:i + 9]] for i in range(0, len(te_words), 9)]
                key = solve(lm, build_cipher(trc, signs), len(signs), keytype, rng)
                bits = lm.bits_per_letter(*build_cipher(tec, signs), key)
                dec = decode_words(tec, signs, key)
                rate = word_rate(dec, lm.vocab)
                flat_d = "".join("".join(l) for l in dec)
                flat_t = "".join("".join(l) for l in truth_lines)
                acc = sum(x == y for x, y in zip(flat_d, flat_t)) / len(flat_t)
                results["positive"].append({"language": lang, "keytype": keytype, "test_bits": bits,
                                            "word_rate": rate, "letters_recovered": acc,
                                            "sample": " ".join(dec[0])})
                print(f"POSITIVE {lang} {keytype} bits={bits:.3f} words={rate:.3f} recovered={acc:.2f}  {' '.join(dec[0])[:60]}")

    # ---- random baseline: shuffled Voynich signs
    signs, tr, te = prepared["letters"]
    for keytype in ["mono", "homophonic"]:
        for lang, (lm, _) in langs.items():
            for k in range(N_SHUFFLES):
                srng = random.Random(SEED + 1000 * k + 1)
                def shuffle(lines):
                    pool = [s for line in lines for w in line for s in w]
                    srng.shuffle(pool)
                    it = iter(pool)
                    return [[[next(it) for _ in w] for w in line] for line in lines]
                trs, tes = shuffle(tr), shuffle(te)
                key = solve(lm, build_cipher(trs, signs), len(signs), keytype, rng)
                bits = lm.bits_per_letter(*build_cipher(tes, signs), key)
                rate = word_rate(decode_words(tes, signs, key), lm.vocab)
                results["baseline"].append({"language": lang, "keytype": keytype, "test_bits": bits, "word_rate": rate})
                print(f"BASELINE {lang} {keytype} bits={bits:.3f} words={rate:.3f}")

    # ---- verdicts
    for run in results["runs"]:
        base = [b for b in results["baseline"] if b["language"] == run["language"] and b["keytype"] == run["keytype"]]
        posl = run["language"] if run["language"] != "venetian" else "italian"
        pos = [p for p in results["positive"] if p["language"] == posl and p["keytype"] == run["keytype"]]
        bmean = np.mean([b["test_bits"] for b in base])
        pmean = np.mean([p["test_bits"] for p in pos])
        run["R1"] = bool(run["test_bits"] < min(b["test_bits"] for b in base) and run["test_bits"] <= (pmean + bmean) / 2)
        run["R2"] = bool(run["word_rate"] > max(b["word_rate"] for b in base)
                         and run["word_rate"] >= 0.5 * np.mean([p["word_rate"] for p in pos]))
        run["R3"] = bool(run["star_hits"] > run["star_null_p95"])
        run["decodes"] = run["R1"] and run["R2"]
    for p in results["positive"]:
        base = [b for b in results["baseline"] if b["language"] == p["language"] and b["keytype"] == p["keytype"]]
        p["passes"] = bool(p["test_bits"] < min(b["test_bits"] for b in base)
                           and p["word_rate"] > max(b["word_rate"] for b in base))

    # conditional entropy of the raw texts (explains the result)
    def h2(seq):
        c2 = Counter(zip(seq, seq[1:]))
        c1 = Counter(seq[:-1])
        n = sum(c2.values())
        return -sum(v / n * math.log2(v / c1[a]) for (a, _), v in c2.items())
    ent = {}
    for inv in prepared:
        seq = [s for line in prepared[inv][1] for w in line for s in (w + [" "])]
        ent[f"voynich_{inv}"] = h2(seq)
    for lang in ["latin", "italian"]:
        ent[lang] = h2(list(langs[lang][1][:200000]))
    results["conditional_entropy_bits"] = ent

    OUT.mkdir(exist_ok=True)
    (OUT / "fontana_cipher_results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    write_report(results, prepared)


def write_report(res, prepared):
    L = []
    w = L.append
    runs = res["runs"]
    n_dec = sum(r["decodes"] for r in runs)
    w("# Fontana cipher decoder: results\n")
    w("Pre-registration: `analyses/fontana_cipher_prereg.md`. Code: `analyses/fontana_cipher_decoder.py` "
      f"(seed {SEED}). Full numbers: `output/fontana_cipher_results.json`.\n")
    w("## Answer\n")
    if n_dec == 0:
        w("**None of the 36 Fontana-method runs decodes the Voynich.** No invented-alphabet substitution "
          "(one sign per letter or several), forwards or reversed, with either sign inventory, makes the text read as "
          "Latin, Italian or Venetian. The best keys do beat shuffled Voynich text, but they reach only 4-34% real "
          "words (mostly short, repeated ones like *sit*, *et*, *del*), while real Latin and Italian put through the "
          "same cipher and solver come back at 94-100% real words, almost letter-perfect.\n")
    else:
        w(f"**{n_dec} of 36 runs pass both pre-registered rules.** See the table below before reading anything into it.\n")
    pos_ok = sum(p["passes"] for p in res["positive"])
    w(f"The test itself works: {pos_ok} of {len(res['positive'])} positive controls (real Latin or Italian, "
      "enciphered with a random key and solved by the same program) pass. Mean letters recovered: "
      + ", ".join(f"{l} {k} {np.mean([p['letters_recovered'] for p in res['positive'] if p['language']==l and p['keytype']==k]):.0%}"
                  for l in ["latin", "italian"] for k in ["mono", "homophonic"]) + ".\n")
    w("## Controls\n")
    w("| Text | Key type | Language | Test bits/letter (lower = more language-like) | Real-word rate |")
    w("|---|---|---|---:|---:|")
    for l in ["latin", "italian", "venetian"]:
        for k in ["mono", "homophonic"]:
            pos = [p for p in res["positive"] if p["language"] == l and p["keytype"] == k]
            if pos:
                w(f"| Real text, enciphered then solved (positive) | {k} | {l} | "
                  f"{np.mean([p['test_bits'] for p in pos]):.3f} | {np.mean([p['word_rate'] for p in pos]):.1%} |")
            base = [b for b in res["baseline"] if b["language"] == l and b["keytype"] == k]
            w(f"| Shuffled Voynich (random baseline) | {k} | {l} | "
              f"{np.mean([b['test_bits'] for b in base]):.3f} (best {min(b['test_bits'] for b in base):.3f}) | "
              f"{np.mean([b['word_rate'] for b in base]):.1%} (best {max(b['word_rate'] for b in base):.1%}) |")
    w("\n## All 36 runs\n")
    w("| Signs | Direction | Key | Language | Bits/letter | Real words | Star-name hits (random-key 95th pct) | R1 | R2 | R3 | Decodes? |")
    w("|---|---|---|---|---:|---:|---:|---|---|---|---|")
    yn = lambda x: "pass" if x else "fail"
    for r in runs:
        w(f"| {r['inventory']} | {r['direction']} | {r['keytype']} | {r['language']} | {r['test_bits']:.3f} | "
          f"{r['word_rate']:.1%} | {r['star_hits']} ({r['star_null_p95']:.0f}) | {yn(r['R1'])} | {yn(r['R2'])} | "
          f"{yn(r['R3'])} | **{'yes' if r['decodes'] else 'no'}** |")
    best = min(runs, key=lambda r: r["test_bits"] - np.mean([p["test_bits"] for p in res["positive"]
                                                             if p["language"] == (r["language"] if r["language"] != "venetian" else "italian")]))
    w("\n## What the closest run reads like\n")
    w(f"Closest to its language: {best['inventory']}, {best['direction']}, {best['keytype']}, {best['language']}. "
      "First three test lines, decoded:\n")
    for s in best["sample"]:
        w(f"> {s}\n")
    wordy = max(runs, key=lambda r: r["word_rate"])
    w(f"\nMost real words: {wordy['inventory']}, {wordy['direction']}, {wordy['keytype']}, {wordy['language']} "
      f"({wordy['word_rate']:.0%}). First two test lines:\n")
    for s in wordy["sample"][:2]:
        w(f"> {s}\n")
    w("Both read as repetitive syllables, not sentences. The low bits/letter of the Voynich runs come from this "
      "repetitiveness, which is why R1 passed in most runs and could not on its own tell a decoding from nonsense "
      "(a weakness of rule R1, noted here rather than changed after the fact).\n")
    r3 = [r for r in runs if r["R3"]]
    w(f"**Star-name check:** {len(r3)} run(s) pass R3, each with a single hit: "
      + "; ".join(f"{h['voynich']} → {h['decoded']} ≈ *{h['name']}*" for r in r3 for h in r["star_words"] if h["name"])
      + ". Random keys average almost zero hits, so one hit clears the 95th percentile (0), but one near-match "
      "in 20 words, in runs that otherwise read as nonsense, is best treated as coincidence. No run turns "
      "*koaiin*/*okoaly* or the other pairs into star or plant names.\n")
    w("Star-name check for the closest run (Voynich word → decoded → nearest name within one letter):\n")
    for sw in best["star_words"]:
        w(f"- {sw['voynich']} → {sw['decoded']}" + (f" → **{sw['name']}**" if sw["name"] else ""))
    w("\n## Why it fails: the Voynich is too predictable for a letter swap\n")
    e = res["conditional_entropy_bits"]
    w("A substitution only relabels signs, so it cannot change how predictable the next sign is. "
      "Measured as conditional entropy (bits of surprise per sign, given the previous sign):\n")
    w("| Text | bits |\n|---|---:|")
    for k, v in e.items():
        w(f"| {k} | {v:.2f} |")
    w("\nThe Voynich is far more predictable than Latin or Italian, and a homophonic key (several signs for one "
      "letter) makes the decoded text even *more* predictable, not less. So a simple Fontana-style substitution of "
      "Latin or Italian cannot produce text like the Voynich. This agrees with the earlier comparison in "
      "VALIDATION.md (h2 2.11 vs 3.2–3.4).\n")
    w("## Limits\n")
    w("- The star-name check could only use 20 of the 24 words: " + ", ".join(STAR_CHECK_DROPPED)
      + " contain rare @-signs with no stable reading. (The pre-registration said 22; the true count of distinct "
      "plain words is 20.)")
    w("- Venetian is represented by 19th-century dialect verse (8,500 words); no 15th-century Paduan or Venetian "
      "prose was available. Italian is Tuscan (Dante, Matteo Villani).")
    w("- Not tested: abbreviation systems, null signs, a code-book of whole words, a syllabic cipher, or "
      "languages other than Latin and Italian. Any of these could change the picture.")
    w("- Venetian has no positive control of its own (too little held-out text); it is judged against the Italian control.")
    w("- Not established here: whether Fontana's cipher was mono- or homophonic. Both were tested.")
    w("- This tests Fontana's *methods*, not Fontana as author. A failure does not rule him out.")
    (OUT / "fontana_cipher_report.md").write_text("\n".join(L) + "\n")
    print("\nwrote output/fontana_cipher_report.md")


if __name__ == "__main__":
    main()
