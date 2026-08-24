# Scoring

Seven metrics, one touching count, and every common mean, so the ranking can be
read against the thing that produced it. Regenerate with `node tools/gen_scoring.js`.

## What is scored

* **box** — less is better
* **cross area** — less is better
* **pieces** — less is better
* **distinct** — less is better
* **rise/360** — less is better
* **turns/m** — less is better
* **longest str** — more is better
* **touching** — carried the same way as the rest, at weight 3

Each is normalized to (0,1] with 1 the best in the set, oriented so bigger is
better, and floored at 0.01 so that one worst-in-set value cannot zero a product.
Touching is not a special case: a graded penalty on the same scale, weighted, which
is what `geo fix` and `add fix` were doing and is now what every mean sees.

**`blocks/360` is deliberately gone.** It is anti-correlated with turns/m by
construction — a tighter spiral has to turn more often — so carrying both let them
cancel, and made the composite quieter about coiling than the columns themselves are.

## The means

| mean | order *p* | what it rewards |
| --- | :-: | --- |
| harmonic | -1 | punishes the weakest input hardest |
| geometric | 0 | |
| arithmetic | 1 | |
| quadratic (RMS) | 2 | |
| cubic | 3 | rewards the strongest input hardest |
| median | — | ignores both extremes |
| midrange | — | only the extremes |
| contraharmonic | — | rewards the strongest harder still |

The first five are the power mean of order *p*, which increases with *p*, so for
every spiral **harmonic ≤ geometric ≤ arithmetic ≤ quadratic ≤ cubic**. Verified here
on all 18. What changes with *p* is not the size of the score but how much a single
bad metric is allowed to sink it.

## The table

| spiral | touch | harmonic | # | geometric | # | arithmetic | # | quadratic | # | cubic | # | median | # | midrange | # | contraharmonic | # |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coil_3x3_53_2 | 0 | 0.8789 | 1 | 0.8897 | 1 | 0.8992 | 1 | 0.9076 | 1 | 0.9149 | 1 | 0.9479 | 1 | 0.8053 | 2 | 0.9160 | 2 |
| coil_3x3_53 | 0 | 0.8396 | 2 | 0.8511 | 2 | 0.8620 | 2 | 0.8724 | 2 | 0.8819 | 2 | 0.8791 | 3 | 0.8188 | 1 | 0.8828 | 4 |
| coil_3x3_50 | 8 | 0.7317 | 3 | 0.7434 | 3 | 0.7557 | 3 | 0.7683 | 4 | 0.7811 | 5 | 0.7023 | 9 | 0.8020 | 4 | 0.7812 | 12 |
| coil_3x3_47 | 8 | 0.7191 | 4 | 0.7311 | 4 | 0.7444 | 4 | 0.7587 | 5 | 0.7737 | 7 | 0.6953 | 11 | 0.8020 | 3 | 0.7733 | 14 |
| coil_3x9_18 | 16 | 0.4176 | 5 | 0.5252 | 5 | 0.6329 | 6 | 0.7108 | 8 | 0.7610 | 9 | 0.8118 | 5 | 0.6040 | 5 | 0.7983 | 10 |
| coil_4x9_17 | 14 | 0.3958 | 6 | 0.5165 | 6 | 0.6258 | 7 | 0.7054 | 9 | 0.7601 | 10 | 0.6526 | 12 | 0.5600 | 9 | 0.7952 | 11 |
| coil_4x8_18 | 16 | 0.3868 | 7 | 0.4903 | 7 | 0.6017 | 10 | 0.6852 | 13 | 0.7394 | 13 | 0.7515 | 7 | 0.6040 | 6 | 0.7802 | 13 |
| coil_3x8_20 | 17 | 0.3429 | 9 | 0.4536 | 8 | 0.5658 | 15 | 0.6482 | 16 | 0.7048 | 16 | 0.5892 | 15 | 0.5793 | 7 | 0.7426 | 16 |
| coil_5x7_18 | 16 | 0.3472 | 8 | 0.4523 | 9 | 0.5680 | 14 | 0.6558 | 15 | 0.7141 | 15 | 0.6353 | 13 | 0.5737 | 8 | 0.7572 | 15 |
| coil_5x8_17 | 14 | 0.0853 | 10 | 0.3960 | 10 | 0.6075 | 9 | 0.7018 | 12 | 0.7621 | 8 | 0.5870 | 16 | 0.5050 | 15 | 0.8108 | 9 |
| staircase_coil | 0 | 0.0786 | 11 | 0.3863 | 11 | 0.6727 | 5 | 0.7802 | 3 | 0.8322 | 3 | 0.8839 | 2 | 0.5050 | 16 | 0.9050 | 3 |
| coil_3x4_74 | 0 | 0.0751 | 12 | 0.3313 | 12 | 0.5959 | 11 | 0.7047 | 11 | 0.7597 | 12 | 0.7038 | 8 | 0.5050 | 13 | 0.8333 | 7 |
| coil_3x4_73_2 | 0 | 0.0462 | 14 | 0.2858 | 13 | 0.6098 | 8 | 0.7226 | 7 | 0.7758 | 6 | 0.7532 | 6 | 0.5050 | 12 | 0.8564 | 5 |
| coil_3x4_73 | 0 | 0.0461 | 15 | 0.2796 | 14 | 0.5933 | 12 | 0.7052 | 10 | 0.7599 | 11 | 0.6982 | 10 | 0.5050 | 11 | 0.8384 | 6 |
| coil_3x4_78 | 0 | 0.0461 | 16 | 0.2584 | 15 | 0.5450 | 16 | 0.6671 | 14 | 0.7342 | 14 | 0.6073 | 14 | 0.5050 | 14 | 0.8166 | 8 |
| coil_4x7_20 | 18 | 0.0726 | 13 | 0.2440 | 16 | 0.4255 | 17 | 0.5315 | 17 | 0.5976 | 18 | 0.4630 | 17 | 0.5022 | 17 | 0.6637 | 18 |
| coil_2x2_146 | 0 | 0.0311 | 17 | 0.1850 | 17 | 0.5788 | 13 | 0.7403 | 6 | 0.8107 | 4 | 0.8446 | 4 | 0.5050 | 10 | 0.9469 | 1 |
| coil_3x7_22 | 20 | 0.0243 | 18 | 0.1146 | 18 | 0.3851 | 18 | 0.5305 | 18 | 0.6133 | 17 | 0.3448 | 18 | 0.5019 | 18 | 0.7308 | 17 |

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_146 ranks **1** under one mean
and **17** under another — a swing of 16 places in a field of 18. staircase_coil swings 14.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_146` | rise/360 = 0.010 | #17 | #1 |
| `staircase_coil` | distinct = 0.010 | #11 | #3 |
| `coil_3x3_53_2` | rise/360 = 0.611 | #1 | #2 |

`coil_2x2_146` has the slackest pitch in the set and a 2x2 cross-section: one input at
the floor, another at the ceiling. The harmonic mean reads it as disqualified, the
contraharmonic as the best thing here. Both are arithmetically correct; they are
answering different questions. The staircase coil is the same shape of argument, its
weak spot being distinct.

Harmonic and contraharmonic agree on **0** of 18 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 12, which is
why the geometric mean is the usual choice when no weak spot should be forgiven but
outright disqualification is too strong.

## What survives

`coil_3x3_53_2` comes first under **6 of the 8 means**, and the reason is visible in the
table above: its worst input is 0.611, where every other contender has something
at 0.01. It does not win by being outstanding anywhere. It wins by having nothing to
punish, which is the one way to be robust to the choice of mean.

If a weak spot is genuinely fatal — a shared wall that will leak, a coil too fat for
the body — use the harmonic mean, or filter and then rank. If the design is allowed one
bad number in exchange for a very good one, use quadratic or cubic. The arithmetic mean
is the choice that declines to say.
