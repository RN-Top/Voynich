#!/usr/bin/env python3
"""Score the whole integrated file forwards and fully flipped (pre-registered in
analyses/whole_file_direction_prereg.md). Writes output/whole_file_direction_report.md.

    python3 analyses/whole_file_direction_test.py          # run
    python3 analyses/whole_file_direction_test.py --save   # also write voynich_integrated_backwards.json
"""
import argparse
import copy
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED, PERMS = 408, 10_000


def flip(data):
    d = copy.deepcopy(data)
    folios = d["folios"][::-1]
    for f in folios:
        f["text_lines"] = f["text_lines"][::-1]
        for ln in f["text_lines"]:
            ln["words"] = [w[::-1] for w in ln["words"][::-1]]
        for lab in f["labels"]:
            lab["words"] = [w[::-1] for w in lab["words"][::-1]]
        f["text_units"] = []  # unit groupings are rebuilt from text_lines by readers if needed
    d["folios"] = folios
    d["metadata"]["direction"] = "backwards: pages, lines, words and letters all reversed"
    return d


def page_words(f):
    return [w for ln in f["text_lines"] if ln["unit"] == "paragraph" for w in ln["words"]]


def positions_A(words, labels):
    n = len(words)
    return [i / (n - 1) for i, w in enumerate(words) if w in labels] if n > 1 else []


def positions_B(words, topic):
    n, seen, out = len(words), set(), []
    for i, w in enumerate(words):
        if w in topic and w not in seen:
            seen.add(w)
            out.append(i / (n - 1))
    return out


def score(folios, kind, rng):
    counts = Counter(w for f in folios for w in page_words(f))
    pages = []
    for f in folios:
        ws = page_words(f)
        if len(ws) < 2:
            continue
        if kind == "A":
            key = {w for lab in f["labels"] for w in lab["words"]}
            fn = positions_A
        else:
            c = Counter(ws)
            key = {w for w, k in c.items() if k >= 2 and counts[w] == k}
            fn = positions_B
        if key and fn(ws, key):
            pages.append((ws, key, fn))
    obs_pos = [p for ws, key, fn in pages for p in fn(ws, key)]
    obs = sum(obs_pos) / len(obs_pos)
    null = []
    for _ in range(PERMS):
        tot = cnt = 0
        for ws, key, fn in pages:
            pp = fn(rng.sample(ws, len(ws)), key)
            tot += sum(pp)
            cnt += len(pp)
        null.append(tot / cnt)
    null_mean = sum(null) / PERMS
    p_low = (sum(x <= obs for x in null) + 1) / (PERMS + 1)
    return dict(pages=len(pages), matches=len(obs_pos), mean=obs, null_mean=null_mean,
                p=p_low, first=p_low < 0.01 and obs < null_mean)


def invariants(folios):
    lab_in_text = 0
    for f in folios:
        labs = {w for lab in f["labels"] for w in lab["words"]}
        lab_in_text += len(labs & set(page_words(f)))
    seq = [f["illustration"]["type"] for f in folios]
    same_next = sum(a == b for a, b in zip(seq, seq[1:]))
    return dict(label_words_in_own_text=lab_in_text, neighbour_pages_same_drawing=same_next,
                pages=len(folios), words=sum(len(ln["words"]) for f in folios for ln in f["text_lines"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true")
    args = ap.parse_args()
    fwd = json.load(open(ROOT / "voynich_integrated.json", encoding="utf-8"))
    bwd = flip(fwd)
    if args.save:
        json.dump(bwd, open(ROOT / "voynich_integrated_backwards.json", "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
    res = {}
    for name, d in (("forwards", fwd), ("backwards", bwd)):
        rng = random.Random(SEED)
        res[name] = {"A": score(d["folios"], "A", rng), "B": score(d["folios"], "B", rng),
                     "inv": invariants(d["folios"])}
    f_first = res["forwards"]["A"]["first"] or res["forwards"]["B"]["first"]
    b_first = res["backwards"]["A"]["first"] or res["backwards"]["B"]["first"]
    if f_first and not b_first:
        verdict = "forwards fits better"
    elif b_first and not f_first:
        verdict = "backwards fits better"
    else:
        verdict = "no preference"

    r = ["# The whole integrated file, forwards and backwards\n",
         "Pre-registration: `analyses/whole_file_direction_prereg.md`. Code: `analyses/whole_file_direction_test.py` "
         f"(seed {SEED}, {PERMS:,} shuffles).\n",
         f"**Decision: {verdict}.**\n",
         "| Score | Copy | Pages | Matches | Mean position (0 = start, 1 = end) | Shuffled mean | p (earlier than shuffled) | Names come first? |",
         "|---|---|---|---|---|---|---|---|"]
    for s, label in (("A", "A: label words in own text"), ("B", "B: topic words, first use")):
        for name in ("forwards", "backwards"):
            x = res[name][s]
            r.append(f"| {label} | {name} | {x['pages']} | {x['matches']} | {x['mean']:.3f} | {x['null_mean']:.3f} | "
                     f"{x['p']:.4f} | {'yes' if x['first'] else 'no'} |")
    r.append("\n## Same in both copies (check that the flip kept everything together)\n")
    r.append("| | forwards | backwards |\n|---|---|---|")
    for k in res["forwards"]["inv"]:
        r.append(f"| {k.replace('_', ' ')} | {res['forwards']['inv'][k]} | {res['backwards']['inv'][k]} |")
    text = "\n".join(r) + "\n"
    (ROOT / "output").mkdir(exist_ok=True)
    (ROOT / "output" / "whole_file_direction_report.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
