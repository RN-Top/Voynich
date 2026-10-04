#!/usr/bin/env python3
"""Bath-section text vs spring zodiac labels (analyses/bath_spring_prereg.md)."""
import itertools, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(ROOT),str(ROOT/"analyses")]
from parser import CORPUS_PATH, parse_zl3b
from root_dictionary_test import root_of
from zodiac_days_test import zodiac_labels

def main():
    df=parse_zl3b(CORPUS_PATH)
    bath=set(df[(df.section=="Biological")&(df.locus_type=="P")&(df.clean.str.len()>0)].clean.map(root_of))
    signs=zodiac_labels(); keys=list(signs)
    hit={k:np.array([root_of(w) in bath for w in signs[k]["labels"]]) for k in keys}
    spring=[k for k in keys if any(s in signs[k]["name"] for s in ("Pisces","Aries","Taurus"))]
    def D(sp):
        a=np.concatenate([hit[k] for k in sp]); b=np.concatenate([hit[k] for k in keys if k not in sp])
        return a.mean()-b.mean()
    obs=D(spring); null=[D(c) for c in itertools.combinations(keys,len(spring))]
    p=sum(v>=obs-1e-12 for v in null)/len(null)
    L=["# Bath-section text vs spring zodiac labels","","Pre-registration: `analyses/bath_spring_prereg.md`.","",
       "| Sign | Labels | Share whose root occurs in bath text |","|---|---:|---:|"]
    L+=[f"| {signs[k]['name']}{' (spring)' if k in spring else ''} | {len(hit[k])} | {hit[k].mean():.0%} |" for k in keys]
    L+=["",f"Spring minus rest: **{obs:+.3f}**; exact p over {len(null)} sign splits = {p:.3f} → **{'SUPPORTED' if p<0.05 else 'NOT SUPPORTED'}**",""]
    r="\n".join(L)+"\n"; (ROOT/"output"/"bath_spring_report.md").write_text(r); print(r)
if __name__=="__main__": main()
