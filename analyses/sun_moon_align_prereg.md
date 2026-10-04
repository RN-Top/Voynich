# Pre-registration: are the Sun wheel (f67r1) and Moon wheel (f67r2) meant to be read together?

Date: 2026-10-04. Written before the code exists.

## Idea (Erin)

The Sun and Moon work together, which is why the two wheels sit side by side. If sector *i* of the Sun wheel belongs
with moon *i* of the Moon wheel, then for some alignment the paired labels should be more alike than chance.

## Data

- **Sun wheel:** the 12 sector labels `f67r1.8`–`.19` (`@Ri`), in transcription order.
- **Moon wheel:** the 12 moon labels `f67r2.52`–`.63`, in transcription order. Our photo reading confirmed this order
  runs clockwise around the ring (`analyses/moon_months_f67r2.csv`).
- Both lists are taken as running clockwise.
- Commas and dots inside a label are removed.

## Statistic

- **Pair similarity:** the Jaccard index of the two labels' character-bigram sets (with word-boundary marks).
- **Score for a rotation s:** S(s) = mean over i of sim(sun[i], moon[(i+s) mod 12]).
- **Test statistic:** M = max S(s) over the 12 rotations. The starting points of the two transcriptions are not known
  to correspond, so every rotation is allowed.

## Null and threshold

- **Null:** shuffle the order of the moon labels at random (any order), recompute M, 10,000 times, seed 20261009.
- **Threshold:** one-sided p < 0.05.

## Reported

The score at every rotation, the best rotation, and its 12 label pairs.
