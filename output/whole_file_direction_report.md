# The whole integrated file, forwards and backwards

Pre-registration: `analyses/whole_file_direction_prereg.md`. Code: `analyses/whole_file_direction_test.py` (seed 408, 10,000 shuffles).

**Decision: no preference.**

| Score | Copy | Pages | Matches | Mean position (0 = start, 1 = end) | Shuffled mean | p (earlier than shuffled) | Names come first? |
|---|---|---|---|---|---|---|---|
| A: label words in own text | forwards | 27 | 168 | 0.485 | 0.500 | 0.2530 | no |
| A: label words in own text | backwards | 27 | 168 | 0.515 | 0.500 | 0.7523 | no |
| B: topic words, first use | forwards | 15 | 18 | 0.473 | 0.332 | 0.9922 | no |
| B: topic words, first use | backwards | 15 | 18 | 0.222 | 0.333 | 0.0168 | no |

## Same in both copies (check that the flip kept everything together)

| | forwards | backwards |
|---|---|---|
| label words in own text | 79 | 79 |
| neighbour pages same drawing | 200 | 200 |
| pages | 227 | 227 |
| words | 39026 | 39026 |
