#!/usr/bin/env python3
"""
blind_test.py
-------------
Held-out stem-context test for the Voynich syntax model.

Run from the repo root (same folder as app.py):

    python blind_test.py

What it does
  1. Loads data/ZL3b-n.txt (ZL / IVTFF).
  2. FREEZES the stems already in the published lexicon. Those are "seen".
  3. Holds out a block of folios you did not hand-translate.
  4. On the training folios only, learns:
        - most common neighbor family of each remaining stem
        - most common section
        - predicted role (heat / medium / outlet / other)
  5. On the held-out folios, checks whether those predictions hold.
  6. Writes:
        output/blind_predictions.json   (locked before scoring)
        output/blind_report.txt

A pass is NOT a translation. A pass means: the syntax slot of a stem
is stable on pages the model was not allowed to see.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "data" / "ZL3b-n.txt"
OUTDIR = ROOT / "output"
OUTDIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Frozen published lexicon. Do not edit after the first run.
# These stems are EXCLUDED from the prediction pool — they are already seen.
# ---------------------------------------------------------------------------
SEEN_STEMS = {
    "qokedy",
    "qokchdy",
    "qoted",
    "okeedy",
    "qokeey",
    "chdam",
    "cheocthedy",
    "chedar",
    "oky",
    "daiin",
    "chedaiin",
    "otcheodaiin",
    "shedaiin",
    "daraiin",
    "okaiin",
    "cthaiin",
    "cfhaiin",
    "cfhoaiin",
    "ataiin",
    "chtaiin",
    "ykaiin",
}

# Folios used in the published dossier recipes / cribs. Held-out set avoids these.
SEEN_FOLIOS = {
    "f1r",
    "f9r",
    "f70v2",
    "f71r",
    "f72r1",
    "f72v1",
    "f72v2",
    "f76r",
    "f103r",
    "f114v",
    "f116v",
}

HEAT_PREFIXES = ("qok", "qo", "ok")
MEDIUM_SUFFIXES = ("aiin", "aiiin", "ain")
OUTLET_SUFFIXES = ("edy", "ody", "dy")
RETAIN_STEMS = {"chdam"}

CONTROL_PREFIXES = ("qok", "qk", "dk", "qo", "ok", "q", "k", "d")
EXIT_PORTS = ("aiiin", "aiin", "ain", "edy", "ody", "ar", "al", "am", "dy", "m", "y")


def clean_token(raw: str) -> str:
    t = raw.lower()
    t = re.sub(r"\[.*?\]", "", t)
    t = re.sub(r"\{.*?\}", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[^a-z]", "", t)
    return t


def strip_stem(token: str) -> str:
    s = token
    for p in CONTROL_PREFIXES:
        if s.startswith(p) and len(s) > len(p) + 1:
            s = s[len(p) :]
            break
    for p in EXIT_PORTS:
        if s.endswith(p) and len(s) > len(p):
            s = s[: -len(p)]
            break
    return s or token


def role_of(token: str) -> str:
    if token in RETAIN_STEMS:
        return "retain"
    if token.startswith(HEAT_PREFIXES) and any(token.endswith(s) for s in ("edy", "ey", "ed", "dy")):
        return "heat"
    if any(token.endswith(s) for s in MEDIUM_SUFFIXES):
        return "medium"
    if any(token.endswith(s) for s in OUTLET_SUFFIXES):
        return "outlet"
    if token.endswith("m") or token.endswith("am"):
        return "flush"
    return "other"


def section_of(folio: str) -> str:
    m = re.match(r"f(\d+)", folio)
    if not m:
        return "unknown"
    n = int(m.group(1))
    if n <= 66:
        return "herbal"
    if n <= 73:
        return "zodiac"
    if n <= 84:
        return "baths"
    if n <= 86:
        return "rosettes"
    if n <= 102:
        return "stars"
    return "pharma"


def parse_zl(path: Path):
    if not path.exists():
        sys.exit(f"Missing corpus: {path}\nPut ZL3b-n.txt in data/ and rerun.")
    text = path.read_text(encoding="utf-8", errors="replace")
    folios = {}
    order = []
    current = None
    for raw_line in text.splitlines():
        header = re.match(r"<f(\d+[rv]\d*)(?:\.(\d+))?", raw_line)
        if header and raw_line.startswith("<f") and "." not in raw_line.split(">")[0][1:]:
            fid = "f" + header.group(1)
            current = fid
            if fid not in folios:
                folios[fid] = {"id": fid, "lines": []}
                order.append(fid)
            continue
        loc = re.match(r"<f(\d+[rv]\d*)\.(\d+)", raw_line)
        if loc:
            current = "f" + loc.group(1)
            if current not in folios:
                folios[current] = {"id": current, "lines": []}
                order.append(current)
        if "<%>" not in raw_line and not re.search(r">\s+[a-zA-Z]", raw_line):
            body = raw_line
            if ">" in raw_line and re.match(r"<f\d", raw_line):
                body = raw_line.split(">", 1)[1]
            else:
                continue
        else:
            if "<%>" in raw_line:
                body = raw_line.split("<%>", 1)[1]
            elif ">" in raw_line:
                body = raw_line.split(">", 1)[1]
            else:
                continue
        body = body.split("<$>")[0]
        body = re.sub(r"\[.*?\]", "", body)
        body = re.sub(r"\{.*?\}", "", body)
        body = re.sub(r"<[^>]+>", "", body)
        toks = [clean_token(w) for w in re.split(r"[\s.,;:]+", body)]
        toks = [t for t in toks if t]
        if not toks or current is None:
            continue
        locus = loc.group(0)[1:] if loc else current
        folios[current]["lines"].append({"locus": locus, "tokens": toks})
    return {"folios": folios, "order": order}


def iter_tokens(parsed, folio_ids):
    for fid in folio_ids:
        folio = parsed["folios"].get(fid)
        if not folio:
            continue
        for line in folio["lines"]:
            toks = line["tokens"]
            for i, t in enumerate(toks):
                yield {
                    "folio": fid,
                    "section": section_of(fid),
                    "locus": line["locus"],
                    "token": t,
                    "stem": strip_stem(t),
                    "role": role_of(t),
                    "terminal": t[-1] if t else "",
                    "prev": toks[i - 1] if i else "",
                    "next": toks[i + 1] if i + 1 < len(toks) else "",
                    "line_end": i == len(toks) - 1,
                }


def main():
    parsed = parse_zl(CORPUS)
    all_folios = parsed["order"]
    train_folios = [f for f in all_folios if f not in SEEN_FOLIOS]
    # Hold out the last third of the *unseen* folios so training never touches them.
    cut = max(1, (2 * len(train_folios)) // 3)
    learn_folios = train_folios[:cut]
    hold_folios = train_folios[cut:]

    learn = list(iter_tokens(parsed, learn_folios))
    hold = list(iter_tokens(parsed, hold_folios))

    # Candidate stems: frequent in learn, never in the published lexicon.
    freq = Counter(r["token"] for r in learn)
    pool = [
        w
        for w, c in freq.most_common()
        if w not in SEEN_STEMS and c >= 8 and 3 <= len(w) <= 14
    ][:40]

    models = {}
    for stem in pool:
        rows = [r for r in learn if r["token"] == stem]
        if not rows:
            continue
        neigh = Counter()
        secs = Counter()
        roles = Counter()
        terms = Counter()
        for r in rows:
            if r["prev"]:
                neigh[role_of(r["prev"])] += 1
            if r["next"]:
                neigh[role_of(r["next"])] += 1
            secs[r["section"]] += 1
            roles[r["role"]] += 1
            terms[r["terminal"]] += 1
        models[stem] = {
            "count_train": len(rows),
            "pred_neighbor_role": neigh.most_common(1)[0][0] if neigh else "other",
            "pred_section": secs.most_common(1)[0][0],
            "pred_role": roles.most_common(1)[0][0],
            "pred_terminal": terms.most_common(1)[0][0] if terms else "",
            "neighbor_dist": dict(neigh),
            "section_dist": dict(secs),
        }

    locked = {
        "locked_at": datetime.now(timezone.utc).isoformat(),
        "seen_stems": sorted(SEEN_STEMS),
        "seen_folios": sorted(SEEN_FOLIOS),
        "learn_folios": learn_folios,
        "hold_folios": hold_folios,
        "predictions": models,
    }
    pred_path = OUTDIR / "blind_predictions.json"
    pred_path.write_text(json.dumps(locked, indent=2), encoding="utf-8")

    # Score on hold-out. Predictions are already written — scoring cannot change them.
    results = []
    hits_role = hits_sec = hits_term = hits_neigh = 0
    n_scored = 0
    for stem, pred in models.items():
        rows = [r for r in hold if r["token"] == stem]
        if len(rows) < 3:
            continue
        n_scored += 1
        secs = Counter(r["section"] for r in rows)
        roles = Counter(r["role"] for r in rows)
        terms = Counter(r["terminal"] for r in rows)
        neigh = Counter()
        for r in rows:
            if r["prev"]:
                neigh[role_of(r["prev"])] += 1
            if r["next"]:
                neigh[role_of(r["next"])] += 1
        obs_sec = secs.most_common(1)[0][0]
        obs_role = roles.most_common(1)[0][0]
        obs_term = terms.most_common(1)[0][0]
        obs_neigh = neigh.most_common(1)[0][0] if neigh else "other"
        ok_sec = obs_sec == pred["pred_section"]
        ok_role = obs_role == pred["pred_role"]
        ok_term = obs_term == pred["pred_terminal"]
        ok_neigh = obs_neigh == pred["pred_neighbor_role"]
        hits_sec += int(ok_sec)
        hits_role += int(ok_role)
        hits_term += int(ok_term)
        hits_neigh += int(ok_neigh)
        results.append(
            {
                "stem": stem,
                "n_hold": len(rows),
                "pred_role": pred["pred_role"],
                "obs_role": obs_role,
                "role_ok": ok_role,
                "pred_section": pred["pred_section"],
                "obs_section": obs_sec,
                "section_ok": ok_sec,
                "pred_terminal": pred["pred_terminal"],
                "obs_terminal": obs_term,
                "terminal_ok": ok_term,
                "pred_neighbor": pred["pred_neighbor_role"],
                "obs_neighbor": obs_neigh,
                "neighbor_ok": ok_neigh,
            }
        )

    def pct(h, n):
        return 0.0 if n == 0 else 100.0 * h / n

    # Terminal rank-order stability across sections on the hold-out set.
    term_by_sec = defaultdict(Counter)
    for r in hold:
        if r["terminal"]:
            term_by_sec[r["section"]][r["terminal"]] += 1
    ranks = {sec: [g for g, _ in c.most_common(4)] for sec, c in term_by_sec.items()}

    lines = []
    w = lines.append
    w("VOYNICH BLIND STEM-CONTEXT TEST")
    w(f"locked at {locked['locked_at']}")
    w(f"corpus          {CORPUS}")
    w(f"learn folios    {len(learn_folios)}")
    w(f"hold  folios    {len(hold_folios)}")
    w(f"stems predicted {len(models)}")
    w(f"stems scored    {n_scored}  (need >= 3 hold-out hits)")
    w("")
    w("SCORES (higher = syntax slot survived unseen pages)")
    w(f"  role match      {hits_role}/{n_scored}  ({pct(hits_role, n_scored):.1f}%)")
    w(f"  section match   {hits_sec}/{n_scored}  ({pct(hits_sec, n_scored):.1f}%)")
    w(f"  terminal match  {hits_term}/{n_scored}  ({pct(hits_term, n_scored):.1f}%)")
    w(f"  neighbor-role   {hits_neigh}/{n_scored}  ({pct(hits_neigh, n_scored):.1f}%)")
    w("")
    w("Hold-out terminal rank order by section (y/n/r/l should stay on top if syntax is closed):")
    for sec in sorted(ranks):
        w(f"  {sec:12} {ranks[sec]}")
    w("")
    w("PER-STEM")
    w(f"{'stem':16} {'n':>4}  role              section           term  neigh")
    for r in results:
        flag = lambda ok: "OK" if ok else "NO"
        w(
            f"{r['stem']:16} {r['n_hold']:4}  "
            f"{r['pred_role']:7}->{r['obs_role']:7} {flag(r['role_ok']):2}  "
            f"{r['pred_section']:7}->{r['obs_section']:7} {flag(r['section_ok']):2}  "
            f"{r['pred_terminal']}->{r['obs_terminal']} {flag(r['terminal_ok']):2}  "
            f"{r['pred_neighbor']}->{r['obs_neighbor']} {flag(r['neighbor_ok']):2}"
        )
    w("")
    w("How to read this")
    w("  Role/terminal/neighbor hits mean the stem kept the same SLOT on pages")
    w("  the model was not trained on. That supports syntax, not translation.")
    w("  Section misses are expected if a stem is a general operator (heat, medium).")
    w("  Do not change SEEN_STEMS after this file exists. Rerun only to rescore.")
    report = "\n".join(lines) + "\n"
    (OUTDIR / "blind_report.txt").write_text(report, encoding="utf-8")
    print(report)
    print(f"wrote {pred_path}")
    print(f"wrote {OUTDIR / 'blind_report.txt'}")


if __name__ == "__main__":
    main()
