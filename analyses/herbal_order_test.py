#!/usr/bin/env python3
"""Voynich plant order vs alphabetical Latin order (analyses/herbal_order_prereg.md)."""
import csv, itertools
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def tau(x):
    n=len(x); s=sum((x[j]>x[i])-(x[j]<x[i]) for i in range(n) for j in range(i+1,n)); return s/(n*(n-1)/2)

def main():
    agreed=[r["folio"] for r in csv.DictReader(open(ROOT/"analyses"/"plant_ids_agreed.csv"))]
    first={r["folio"]:r["names"].split("|")[0] for r in csv.DictReader(open(ROOT/"analyses"/"plant_names.csv"))}
    key=lambda f:(int(''.join(c for c in f[1:] if c.isdigit())), f[-1])
    book=sorted(agreed,key=key)
    alpha=sorted(book,key=lambda f:first[f])
    rank=[alpha.index(f) for f in book]
    t=tau(rank); null=[tau(p) for p in itertools.permutations(range(len(book)))]
    p=sum(v>=t-1e-12 for v in null)/len(null)
    L=["# Voynich plant order vs alphabetical Latin herbal","","Pre-registration: `analyses/herbal_order_prereg.md`.","",
       "| Book order | Page | Latin name | Alphabetical rank |","|---:|---|---|---:|"]
    L+=[f"| {i+1} | {f} | {first[f]} | {rank[i]+1} |" for i,f in enumerate(book)]
    L+=["",f"Kendall τ = **{t:+.3f}**; exact one-sided p = {p:.3f} → **{'SUPPORTED' if p<0.05 else 'NOT SUPPORTED'}**",""]
    r="\n".join(L)+"\n"; (ROOT/"output"/"herbal_order_report.md").write_text(r); print(r)

if __name__=="__main__": main()
