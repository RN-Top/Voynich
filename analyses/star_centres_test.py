"""Star-centre test (pre-registered in star_centres_prereg.md).

Do star labels that share a root with herbal-page openings sit on stars with a marked
centre (hollow ring or dark dot) more often than other labelled stars? Exact
hypergeometric test per panel, convolved across panels. Data are hand readings of
uploads/yale_hires/f68r_foldout_recto.jpg, stored in the CSVs next to this script.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import hypergeom

HERE = Path(__file__).parent
OUT = HERE.parent / "output" / "star_centres_report.md"


def panel_pmf(df, marked):
    n_stars = len(df)
    k_marked = int(df.centre.isin(marked).sum())
    n_match = int((df.plant_match == "yes").sum())
    obs = int(((df.plant_match == "yes") & df.centre.isin(marked)).sum())
    pmf = hypergeom.pmf(np.arange(n_match + 1), n_stars, k_marked, n_match)
    return dict(stars=n_stars, marked=k_marked, matches=n_match, observed=obs,
                expected=n_match * k_marked / n_stars), pmf


def combined(panels, marked):
    rows, pmf, obs = [], np.array([1.0]), 0
    for name, df in panels.items():
        row, p = panel_pmf(df, marked)
        rows.append(dict(panel=name, **row))
        pmf, obs = np.convolve(pmf, p), obs + row["observed"]
    return pd.DataFrame(rows), obs, float(pmf[obs:].sum())


def main():
    r1 = pd.read_csv(HERE / "star_centres_f68r1.csv").fillna("")
    r23 = pd.read_csv(HERE / "star_centres_f68r2_r3.csv").fillna("")
    confirm = {p: d for p, d in r23.groupby("panel")}
    lines = ["# Star-centre test (f68r)", "",
             "Pre-registration: `analyses/star_centres_prereg.md`. Data: hand readings of",
             "`uploads/yale_hires/f68r_foldout_recto.jpg`.", ""]
    for title, panels, marked in [
        ("Confirmatory: f68r2 + f68r3, ring or dot", confirm, ("ring", "dot")),
        ("Secondary: f68r2 + f68r3, ring only", confirm, ("ring",)),
        ("Secondary: all three panels (includes discovery data), ring or dot",
         {"f68r1": r1, **confirm}, ("ring", "dot")),
    ]:
        tab, obs, p = combined(panels, marked)
        lines += [f"## {title}", "", "```", tab.to_string(index=False), "```", "",
                  f"Observed {obs} matching labels on marked stars; exact P(X >= {obs}) = {p:.3f}.", ""]
    tab, obs, p = combined(confirm, ("ring", "dot"))
    verdict = "SUPPORTED" if p < 0.05 else "NOT SUPPORTED"
    lines += ["## Verdict", "", f"**{verdict}** (registered threshold p < 0.05).", ""]
    allp = pd.concat([r1.assign(panel="f68r1"), r23])
    m = allp[allp.plant_match == "yes"]
    lines += ["## Where the plant-matching labels are", "", "| Label | Panel | Star (x, y px) | Centre |",
              "|---|---|---|---|"]
    lines += [f"| {r.zl_label.split(' ', 1)[1]} | {r.panel} | {r.x}, {r.y} | {r.centre} |" for r in m.itertuples()]
    lines += ["", "Other notes:",
              "- On f68r3, `doaro` and `dchol,day` label the tight star cluster that is often read as the Pleiades.",
              "- See the amendments in the pre-registration for deviations.", ""]
    OUT.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
