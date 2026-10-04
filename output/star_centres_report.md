# Star-centre test (f68r)

Pre-registration: `analyses/star_centres_prereg.md`. Data: hand readings of
`uploads/yale_hires/f68r_foldout_recto.jpg`.

## Confirmatory: f68r2 + f68r3, ring or dot

```
panel  stars  marked  matches  observed  expected
f68r2     23       6        3         0  0.782609
f68r3      1       0        1         0  0.000000
```

Observed 0 matching labels on marked stars; exact P(X >= 0) = 1.000.

## Secondary: f68r2 + f68r3, ring only

```
panel  stars  marked  matches  observed  expected
f68r2     23       6        3         0  0.782609
f68r3      1       0        1         0  0.000000
```

Observed 0 matching labels on marked stars; exact P(X >= 0) = 1.000.

## Secondary: all three panels (includes discovery data), ring or dot

```
panel  stars  marked  matches  observed  expected
f68r1     29      10        5         3  1.724138
f68r2     23       6        3         0  0.782609
f68r3      1       0        1         0  0.000000
```

Observed 3 matching labels on marked stars; exact P(X >= 3) = 0.486.

## Verdict

**NOT SUPPORTED** (registered threshold p < 0.05).

## Where the plant-matching labels are

| Label | Panel | Star (x, y px) | Centre |
|---|---|---|---|
| okoaly | f68r1 | 297, 367 | plain |
| otydy | f68r1 | 250, 453 | ring |
| chocfhy | f68r1 | 393, 387 | plain |
| @167oeeodchy | f68r1 | 600, 613 | ring |
| otochedy | f68r1 | 590, 720 | ring |
| o@167olchchy | f68r2 | 1003, 353 | plain |
| oydchy | f68r2 | 1143, 537 | plain |
| opocphor | f68r2 | 997, 760 | plain |
| otydg | f68r3 | 1802, 725 | plain |

Other notes:
- On f68r3, `doaro` and `dchol,day` label the tight star cluster that is often read as the Pleiades.
- See the amendments in the pre-registration for deviations.
