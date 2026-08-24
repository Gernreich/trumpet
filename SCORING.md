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
* **touching** — carried the same way as the rest, at weight 5

**Nothing is judged on the bore's mouth and exit.** Every design has those two pieces
and no design chooses them, so every metric here is measured over the interior — the
pieces in between — and the piece and shape counts are counts of those. Blocks and mm,
which only describe, still cover the whole bore.

The metrics are normalized to (0,1] with 1 the best in the set, oriented so bigger is
better, and floored at 0.01 so that one worst-in-set value cannot zero a product.

**Touching is treated differently, on purpose.** A wall the bore shares with itself is
visible in the finished instrument, so it is the heaviest input here at weight 5,
and it is penalized convexly — **1/(1+t)** — rather than fading linearly. The step from
no contact to any contact is far larger than any step after it: 0 contacts scores 1.000,
8 contacts 0.111, 20 contacts 0.048. Nothing but a clean coil can score 1.

That form is also absolute where a linear fade against the set maximum is not. Dropping
the worst coil would move everyone else's touching term under a linear fade; under
1/(1+t) it moves nothing.

Override the weight with `SPIRAL_TOUCH_WEIGHT=8 node tools/score.js`.

### A heavy weight is a preference, not a guarantee

Weighting touching at 5 does not stop a coil with contact from beating a clean one.
Under the harmonic mean the first coil *with* touching places **3rd**, above **6** coils
that have none — because each of those has some other metric sitting on the 0.01 floor,
and the harmonic mean punishes that harder than it punishes 8 contacts.

If no touching walls is a *requirement* rather than a preference, filter:

    node tools/score.js --clean      # ranks only the coils with no touching walls

which is the same advice as everywhere else here — cut on the property, then rank.

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
| median | — | ignores both extremes; see the caveat below |
| midrange | — | only the extremes |
| contraharmonic | — | rewards the strongest harder still |

The first five are the power mean of order *p*, which increases with *p*, so for
every spiral **harmonic ≤ geometric ≤ arithmetic ≤ quadratic ≤ cubic**. Verified here
on all 29. What changes with *p* is not the size of the score but how much a single
bad metric is allowed to sink it.

## The table

| spiral | touch | harmonic | # | geometric | # | arithmetic | # | quadratic | # | cubic | # | median | # | midrange | # | contraharmonic | # |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coil_3x3_53_2 | 0 | 0.8835 | 1 | 0.8918 | 1 | 0.8995 | 1 | 0.9065 | 1 | 0.9129 | 1 | 0.9296 | 3 | 0.8207 | 2 | 0.9136 | 3 |
| coil_3x3_53 | 0 | 0.8606 | 2 | 0.8715 | 2 | 0.8818 | 2 | 0.8913 | 2 | 0.9000 | 2 | 0.9296 | 2 | 0.8231 | 1 | 0.9009 | 4 |
| coil_3x3_58_min | 0 | 0.1127 | 10 | 0.5758 | 3 | 0.7661 | 3 | 0.8151 | 3 | 0.8422 | 3 | 0.8625 | 4 | 0.5050 | 11 | 0.8673 | 8 |
| coil_3x3_59_min | 0 | 0.1127 | 11 | 0.5758 | 4 | 0.7661 | 4 | 0.8151 | 4 | 0.8422 | 4 | 0.8625 | 5 | 0.5050 | 12 | 0.8673 | 9 |
| coil_3x3_64_min | 0 | 0.1127 | 12 | 0.5744 | 5 | 0.7646 | 5 | 0.8141 | 5 | 0.8417 | 5 | 0.8625 | 7 | 0.5050 | 14 | 0.8669 | 10 |
| coil_3x3_61_min | 0 | 0.1123 | 13 | 0.5631 | 6 | 0.7501 | 6 | 0.8008 | 6 | 0.8301 | 7 | 0.8625 | 6 | 0.5050 | 13 | 0.8550 | 12 |
| coil_3x4_74_min | 0 | 0.1061 | 14 | 0.4709 | 7 | 0.6775 | 7 | 0.7555 | 9 | 0.7997 | 9 | 0.7525 | 16 | 0.5050 | 20 | 0.8424 | 15 |
| coil_3x4_74 | 0 | 0.1060 | 16 | 0.4682 | 8 | 0.6741 | 8 | 0.7529 | 10 | 0.7979 | 12 | 0.7525 | 15 | 0.5050 | 19 | 0.8409 | 17 |
| coil_3x4_73_min | 0 | 0.1061 | 15 | 0.4650 | 9 | 0.6689 | 11 | 0.7487 | 13 | 0.7950 | 13 | 0.7525 | 14 | 0.5050 | 17 | 0.8379 | 18 |
| coil_3x4_73_2 | 0 | 0.1046 | 18 | 0.4575 | 10 | 0.6702 | 9 | 0.7522 | 11 | 0.7980 | 10 | 0.7565 | 12 | 0.5050 | 16 | 0.8442 | 13 |
| coil_3x4_73_min_2 | 0 | 0.1046 | 19 | 0.4575 | 11 | 0.6702 | 10 | 0.7522 | 12 | 0.7980 | 11 | 0.7565 | 13 | 0.5050 | 18 | 0.8442 | 14 |
| coil_3x4_73 | 0 | 0.1046 | 20 | 0.4538 | 12 | 0.6643 | 12 | 0.7475 | 14 | 0.7949 | 14 | 0.7565 | 11 | 0.5050 | 15 | 0.8412 | 16 |
| coil_3x4_78 | 0 | 0.1049 | 17 | 0.4365 | 13 | 0.6315 | 15 | 0.7191 | 15 | 0.7746 | 17 | 0.6700 | 18 | 0.5050 | 21 | 0.8188 | 19 |
| coil_3x3_50 | 7 | 0.2584 | 3 | 0.3878 | 14 | 0.5392 | 18 | 0.6396 | 20 | 0.6981 | 21 | 0.6394 | 23 | 0.5625 | 3 | 0.7586 | 24 |
| coil_3x3_47 | 8 | 0.2347 | 4 | 0.3690 | 15 | 0.5305 | 19 | 0.6347 | 21 | 0.6946 | 22 | 0.6700 | 17 | 0.5556 | 4 | 0.7594 | 23 |
| staircase_coil | 0 | 0.0585 | 26 | 0.3457 | 16 | 0.6532 | 13 | 0.7638 | 8 | 0.8180 | 8 | 0.8145 | 8 | 0.5050 | 26 | 0.8933 | 6 |
| coil_3x9_18 | 15 | 0.1425 | 5 | 0.2888 | 17 | 0.5060 | 22 | 0.6346 | 22 | 0.7030 | 20 | 0.6635 | 21 | 0.5313 | 6 | 0.7959 | 20 |
| coil_4x9_17 | 14 | 0.1424 | 6 | 0.2812 | 18 | 0.5175 | 21 | 0.6653 | 19 | 0.7409 | 19 | 0.6700 | 19 | 0.5333 | 5 | 0.8554 | 11 |
| coil_4x8_18 | 15 | 0.1397 | 7 | 0.2754 | 19 | 0.4859 | 23 | 0.6167 | 23 | 0.6869 | 23 | 0.6531 | 22 | 0.5313 | 7 | 0.7828 | 21 |
| coil_2x2_146 | 0 | 0.0410 | 28 | 0.2711 | 20 | 0.6405 | 14 | 0.7755 | 7 | 0.8372 | 6 | 1.0000 | 1 | 0.5050 | 10 | 0.9389 | 1 |
| coil_5x7_18 | 15 | 0.1357 | 8 | 0.2620 | 21 | 0.4688 | 24 | 0.6027 | 24 | 0.6752 | 24 | 0.5741 | 24 | 0.5313 | 8 | 0.7747 | 22 |
| coil_3x8_20 | 17 | 0.1273 | 9 | 0.2619 | 22 | 0.4644 | 25 | 0.5884 | 25 | 0.6596 | 25 | 0.4882 | 25 | 0.5278 | 9 | 0.7454 | 25 |
| coil_5x8_17 | 13 | 0.0731 | 21 | 0.2409 | 23 | 0.5212 | 20 | 0.6802 | 18 | 0.7594 | 18 | 0.6700 | 20 | 0.5050 | 25 | 0.8878 | 7 |
| coil_5x5_55 | 0 | 0.0449 | 27 | 0.2210 | 24 | 0.5571 | 16 | 0.7080 | 16 | 0.7794 | 15 | 0.8135 | 9 | 0.5050 | 24 | 0.8997 | 5 |
| coil_4x7_20 | 17 | 0.0643 | 22 | 0.1761 | 25 | 0.3668 | 26 | 0.4949 | 26 | 0.5712 | 27 | 0.3400 | 26 | 0.4951 | 29 | 0.6679 | 29 |
| coil_3x7_23_min | 18 | 0.0620 | 23 | 0.1622 | 26 | 0.3454 | 27 | 0.4863 | 27 | 0.5784 | 26 | 0.2425 | 29 | 0.5050 | 22 | 0.6845 | 26 |
| coil_3x7_22 | 19 | 0.0605 | 24 | 0.1579 | 27 | 0.3401 | 28 | 0.4788 | 28 | 0.5686 | 28 | 0.2425 | 27 | 0.4956 | 27 | 0.6742 | 27 |
| coil_3x7_22_min | 19 | 0.0605 | 25 | 0.1579 | 28 | 0.3401 | 29 | 0.4788 | 29 | 0.5686 | 29 | 0.2425 | 28 | 0.4956 | 28 | 0.6742 | 28 |
| coil_5x5_52_min | 0 | 0.0255 | 29 | 0.1540 | 29 | 0.5447 | 17 | 0.7057 | 17 | 0.7778 | 16 | 0.7824 | 10 | 0.5050 | 23 | 0.9142 | 2 |

**The median does not survive the weighting.** It is an order statistic, and weight is
applied by repetition, so touching occupies 5 of the 13 values and can simply *be*
the median. 1 coils tie at exactly 1.0000. Read the median column knowing that;
the power means do not have this problem.

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_146 ranks **1** under one mean
and **28** under another — a swing of 27 places in a field of 29. coil_5x5_52_min swings 27.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_146` | rise/360 = 0.010 | #28 | #1 |
| `staircase_coil` | distinct = 0.010 | #26 | #6 |
| `coil_3x3_53_2` | rise/360 = 0.641 | #1 | #3 |

`coil_2x2_146` has the slackest pitch in the set and a 2x2 cross-section: one input at
the floor, another at the ceiling. The harmonic mean reads it as disqualified, the
contraharmonic as the best thing here. Both are arithmetically correct; they are
answering different questions. The staircase coil is the same shape of argument, its
weak spot being distinct.

Harmonic and contraharmonic agree on **0** of 29 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 3, which is
why the geometric mean is the usual choice when no weak spot should be forgiven but
outright disqualification is too strong.

## What survives

`coil_3x3_53_2` comes first under **5 of the 8 means**, and the reason is visible in the
table above: its worst input is 0.641, where every other contender has something
at 0.01. It does not win by being outstanding anywhere. It wins by having nothing to
punish, which is the one way to be robust to the choice of mean.

If a weak spot is genuinely fatal — a shared wall that will leak, a coil too fat for
the body — use the harmonic mean, or filter and then rank. If the design is allowed one
bad number in exchange for a very good one, use quadratic or cubic. The arithmetic mean
is the choice that declines to say.

## Ranking once, not repeatedly

A tempting variant is to rank, cut the bottom half, and re-rank the survivors. Do not.

* **harmonic, min-max (what SCORING.md uses)** — survivors reordered 12/15, 5/8, 3/4, 0/2 over the rounds (20 moves in total)
* **geometric, min-max** — survivors reordered 9/15, 5/8, 2/4, 0/2 over the rounds (16 moves in total)
* **geometric, pure ratio-to-best** — survivors reordered 0/15, 0/8, 0/4, 0/2 over the rounds (0 moves in total)

The first two reorder coils that did not change, purely because other coils left the
set. `coil_3x3_50` places 3rd of 29 and 1st of the surviving 9; `coil_3x3_53_2`
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
