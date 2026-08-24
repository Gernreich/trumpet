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
* **mean plate** — more is better
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
| coil_3x3_53_2 | 0 | 0.8605 | 1 | 0.8718 | 1 | 0.8822 | 1 | 0.8916 | 1 | 0.9000 | 1 | 0.8958 | 1 | 0.8053 | 2 | 0.9011 | 3 |
| coil_3x3_53 | 0 | 0.8140 | 2 | 0.8274 | 2 | 0.8404 | 2 | 0.8528 | 2 | 0.8643 | 2 | 0.8625 | 2 | 0.8120 | 1 | 0.8653 | 4 |
| coil_3x3_50 | 8 | 0.7066 | 3 | 0.7204 | 3 | 0.7348 | 3 | 0.7495 | 3 | 0.7643 | 7 | 0.6959 | 7 | 0.7629 | 4 | 0.7646 | 13 |
| coil_3x3_47 | 8 | 0.6983 | 4 | 0.7114 | 4 | 0.7260 | 4 | 0.7416 | 5 | 0.7580 | 8 | 0.6948 | 8 | 0.7708 | 3 | 0.7576 | 14 |
| coil_4x9_17 | 14 | 0.4161 | 6 | 0.5405 | 5 | 0.6463 | 5 | 0.7199 | 7 | 0.7693 | 6 | 0.6700 | 12 | 0.5600 | 9 | 0.8020 | 9 |
| coil_3x9_18 | 16 | 0.4304 | 5 | 0.5332 | 6 | 0.6317 | 7 | 0.7030 | 9 | 0.7503 | 10 | 0.7983 | 3 | 0.6040 | 5 | 0.7824 | 11 |
| coil_4x8_18 | 16 | 0.4007 | 7 | 0.5012 | 7 | 0.6039 | 9 | 0.6799 | 11 | 0.7304 | 13 | 0.7047 | 6 | 0.6040 | 6 | 0.7656 | 12 |
| coil_5x7_18 | 16 | 0.3586 | 8 | 0.4591 | 8 | 0.5648 | 10 | 0.6456 | 14 | 0.7012 | 15 | 0.6005 | 14 | 0.5737 | 8 | 0.7380 | 15 |
| coil_3x8_20 | 17 | 0.3463 | 9 | 0.4468 | 9 | 0.5493 | 12 | 0.6288 | 16 | 0.6864 | 16 | 0.5861 | 15 | 0.5793 | 7 | 0.7198 | 16 |
| coil_5x8_17 | 14 | 0.0930 | 10 | 0.4308 | 10 | 0.6432 | 6 | 0.7340 | 6 | 0.7901 | 4 | 0.6700 | 13 | 0.5050 | 15 | 0.8376 | 6 |
| coil_3x4_74 | 0 | 0.0753 | 12 | 0.2904 | 11 | 0.5488 | 13 | 0.6723 | 13 | 0.7359 | 12 | 0.6700 | 11 | 0.5050 | 13 | 0.8235 | 8 |
| staircase_coil | 0 | 0.0484 | 14 | 0.2771 | 12 | 0.6124 | 8 | 0.7439 | 4 | 0.8062 | 3 | 0.7678 | 4 | 0.5050 | 16 | 0.9037 | 2 |
| coil_3x4_78 | 0 | 0.0497 | 13 | 0.2554 | 13 | 0.5161 | 16 | 0.6397 | 15 | 0.7120 | 14 | 0.5447 | 16 | 0.5050 | 14 | 0.7930 | 10 |
| coil_4x7_20 | 18 | 0.0781 | 11 | 0.2495 | 14 | 0.4152 | 17 | 0.5154 | 17 | 0.5817 | 18 | 0.3400 | 17 | 0.5022 | 17 | 0.6397 | 18 |
| coil_3x4_73 | 0 | 0.0457 | 15 | 0.2354 | 15 | 0.5432 | 14 | 0.6725 | 12 | 0.7361 | 11 | 0.6700 | 10 | 0.5050 | 11 | 0.8327 | 7 |
| coil_3x4_73_2 | 0 | 0.0441 | 16 | 0.2330 | 16 | 0.5571 | 11 | 0.6891 | 10 | 0.7516 | 9 | 0.7263 | 5 | 0.5050 | 12 | 0.8523 | 5 |
| coil_2x2_146 | 0 | 0.0334 | 17 | 0.1786 | 17 | 0.5376 | 15 | 0.7068 | 8 | 0.7854 | 5 | 0.6893 | 9 | 0.5050 | 10 | 0.9294 | 1 |
| coil_3x7_22 | 20 | 0.0262 | 18 | 0.1145 | 18 | 0.3604 | 18 | 0.5069 | 18 | 0.5942 | 17 | 0.3302 | 18 | 0.5019 | 18 | 0.7131 | 17 |

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_146 ranks **1** under one mean
and **17** under another — a swing of 16 places in a field of 18. staircase_coil swings 14.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_146` | rise/360 = 0.010 | #17 | #1 |
| `staircase_coil` | distinct = 0.010 | #14 | #2 |
| `coil_3x3_53_2` | rise/360 = 0.611 | #1 | #3 |

`coil_2x2_146` has the slackest pitch in the set and a 2x2 cross-section: one input at
the floor, another at the ceiling. The harmonic mean reads it as disqualified, the
contraharmonic as the best thing here. Both are arithmetically correct; they are
answering different questions. The staircase coil is the same shape of argument, its
weak spot being distinct.

Harmonic and contraharmonic agree on **0** of 18 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 13, which is
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

## Ranking once, not repeatedly

A tempting variant is to rank, cut the bottom half, and re-rank the survivors. Do not.

* **harmonic, min-max (what SCORING.md uses)** — survivors reordered 7/9, 4/5, 2/3, 0/2 over the rounds (13 moves in total)
* **geometric, min-max** — survivors reordered 5/9, 2/5, 0/3, 0/2 over the rounds (7 moves in total)
* **geometric, pure ratio-to-best** — survivors reordered 0/9, 0/5, 0/3, 0/2 over the rounds (0 moves in total)

The first two reorder coils that did not change, purely because other coils left the
set. `coil_3x3_50` places 3rd of 18 and 1st of the surviving 9; `coil_3x3_53_2`
places 1st and then 4th. Nothing about either was measured again.

The cause is that min-max reads its lo and hi off whoever is present, so dropping
alternatives rescales every metric by a different factor. That is an
independence-of-irrelevant-alternatives failure, and it is the reason to cut on a
property fixed in advance — touching > 0, or a cross-section that will not fit —
rather than on composite score.

The other end of it is just as decisive. Under a pure ratio-to-best normalization with
a geometric mean, nothing depends on which coils are present, and the whole procedure
is a **no-op: 0 moves in every round**. So iterating either changes the order for a
reason that has nothing to do with the coils, or changes nothing at all.

The winner here survives all three, so nothing practical turns on it — but the order
below the top is meaningless under iteration, and should not be read.

One more cost: a cut on composite score removes whatever is best at a single thing,
because a composite is a compromise. `coil_2x2_146` is the only 2x2 cross-section in
the set and does not survive round 0 of 2 of the 3 runs.

    node tools/iterate.js        # the numbers above
