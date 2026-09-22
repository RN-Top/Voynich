You are continuing an existing project. Do not reset, overwrite, or reinitialize anything. Keep Pi, master skeleton, drainage module, apparatus map, frequency modules, Streamlit pages, and GitHub-ready code exactly as they are. Append only.
Add a new module + Streamlit page called heldout_instrument_battery.
Goal: stress-test the alembic / process-log reading on unseen pages only. No new translations. No recipe sentences. No remapping.
LOCKED (do not retune)
Roles:
•  heat/start: qo-, qok-, ok-
•  medium: daiin, -aiin
•  outlet: -ol, -al
•  reflux: -or, -ar
•  retain: shed-
•  drain/close: -m, -am, chdam, shedam
Cycle: C (heat) → L (medium) → route (outlet|reflux) → P (retain) → R (drain)
HOLD OUT Pick pages that were NOT used to build the skeleton, drainage stats, or apparatus map. Required split, as far as unused stock allows:
•  1 herbal running-text folio
•  1 biological / vat / pipe folio
•  1 radial / diagram folio If a class has no unused folio, take the least-used folio in that class and flag it weak_holdout, do not pretend it is clean. Print the exact folio IDs used and why they count as held-out.
WRITE THESE TESTS. All of them. Same locked map.
T1 Path reconstruction
On each held-out folio, convert tagged tokens into apparatus paths.
Score a line:
•  full_cycle if it contains heat/medium → route → retain/drain in order, allowing unmapped tokens in between
•  partial if at least route → drain or retain → drain
•  fail otherwise Report hit rates by folio class.
T2 One-way valve
After a drain token on the same line, count what comes next.
Predict: heat almost never restarts after drain on the same line.
Pass if post-drain heat rate is far below baseline heat rate.
T3 Zone split
On the held-out radial folio, heat and drain must stay suppressed vs that folio’s own token count.
On the held-out bio folio, retain + drain must be enriched.
On the held-out herbal folio, heat + outlet may rise, drain should still prefer line ends.
T4 Line-end drain replication
Recompute drain line-final rate on held-out pages only.
Predict: still >> non-drain line-final rate.
If it collapses, the closer effect was training-set leakage.
T5 Sequence direction
Count forward cycles C→L→route→P→R vs reversed R→P→route→L→C on held-out text only.
Predict: forward >> reverse, same direction as the locked prefix asymmetry.
T6 Unmapped pressure
Report % unmapped tokens on each held-out folio.
If unmapped > 60% and paths still “work,” the map is painting over noise. Flag that.
T7 Control contrast
If control texts are already loaded (Latin / early Italian / Turba), run T1 and T4 on a chunk of each with the same token rules where possible.
Predict: Voynich held-out should show stronger drain-at-end and zone split than plain prose.
If controls look the same, the still-reading is not special.
OUTPUT (Streamlit page + saved files)
Page sections:
1.  Held-out folio list
2.  Path cartoons on the 2D alembic (one panel per folio class)
3.  Scoreboard table: T1–T7 pass / mixed / fail with the raw numbers
4.  Findings report in plain English, required headings:
	•  What survived contact with new pages
	•  What broke
	•  Did the still still look like a still
	•  What I am not allowed to claim
	•  One next cut
5.  Download buttons: event log CSV, scoreboard JSON, figure PNGs
Hard limits
•  Do not change Pi or the skeleton
•  Do not add English glosses
•  Do not use held-out pages to refit roles
•  Fail loudly. A fail is a valid result.
•  Keep imports compatible with the current Streamlit app so this is GitHub + deploy ready
Append only. Do not start over.
At the end print: HELD-OUT BATTERY COMPLETE Pi unchanged: YES/NO Skeleton unchanged: YES/NO Folios tested: [list] Scoreboard: [T1–T7] Verdict: supports / mixed / dead
