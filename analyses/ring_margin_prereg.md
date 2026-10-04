# Pre-registration: the f66r margin column vs the f57v ring, and a golden-number check

Date: 2026-10-04. Written before the code for these tests exists.

**Disclosure:** both sequences were printed earlier in this session (`analyses/f57v_ring_notes.md`), so I have
already seen them. This test is not blind.

## Data

- **Ring:** the 17-symbol unit of `f57v.3`:

  `o l d r v x k m f @169v t r @170 @171 y c @172` (cyclic).

  Variants count as the same position: `d`/`j` at 3, `f`/`p` at 9, `c`/`I` at 16. `@169v` is treated as `@169`.
- **Margin column:** the single-symbol labels `f66r.16`–`.49`, in transcription order (34 entries).

## Test A: does the margin column follow the ring's order?

- **Statistic:** H = the number of adjacent margin pairs (a, b) where b is the ring's next symbol after a.
- **Null:** shuffle the margin column order, 10,000 times, seed 20261007.
- **Threshold:** one-sided p < 0.05.

## Test B: is the margin column a golden-number column? (19, the Moon)

In medieval calendars, the "golden numbers" I–XIX of the 19-year lunar cycle were written in a column beside the days
to mark new moons. Within one month, each golden number appears **at most once**, about 19 entries in 30 days.

- **Prediction if it is a golden-number column:** no symbol repeats within any run of 19 consecutive entries, and
  there are about 19 different symbols.
- **Statistic:** R = the number of entries that repeat a symbol already seen among the previous 18 entries; and the
  number of distinct symbols.
- **Decision:** a golden-number column needs R ≤ 2, allowing for transcription errors. If R > 2, the idea is
  rejected.
