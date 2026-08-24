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
on all 24. What changes with *p* is not the size of the score but how much a single
bad metric is allowed to sink it.

## The table

| spiral | touch | harmonic | # | geometric | # | arithmetic | # | quadratic | # | cubic | # | median | # | midrange | # | contraharmonic | # |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coil_3x3_38 | 0 | 0.8751 | 1 | 0.8866 | 1 | 0.8972 | 2 | 0.9066 | 2 | 0.9150 | 2 | 1.0000 | 2 | 0.8205 | 1 | 0.9162 | 3 |
| coil_3x3_42 | 0 | 0.8712 | 2 | 0.8864 | 2 | 0.8990 | 1 | 0.9093 | 1 | 0.9178 | 1 | 1.0000 | 3 | 0.7653 | 2 | 0.9197 | 2 |
| coil_3x3_44_2 | 0 | 0.1127 | 10 | 0.5756 | 3 | 0.7656 | 3 | 0.8143 | 3 | 0.8411 | 3 | 0.8464 | 5 | 0.5050 | 12 | 0.8661 | 7 |
| coil_3x3_47 | 0 | 0.1125 | 11 | 0.5690 | 4 | 0.7576 | 4 | 0.8075 | 4 | 0.8355 | 4 | 0.8350 | 6 | 0.5050 | 13 | 0.8606 | 8 |
| coil_3x3_44 | 0 | 0.1124 | 12 | 0.5656 | 5 | 0.7521 | 5 | 0.8015 | 5 | 0.8298 | 6 | 0.8464 | 4 | 0.5050 | 11 | 0.8542 | 11 |
| coil_3x3_36 | 4 | 0.3715 | 3 | 0.4749 | 6 | 0.5876 | 13 | 0.6732 | 15 | 0.7302 | 16 | 0.6410 | 19 | 0.6000 | 3 | 0.7713 | 20 |
| coil_3x4_58 | 0 | 0.1058 | 13 | 0.4450 | 7 | 0.6368 | 10 | 0.7215 | 12 | 0.7757 | 13 | 0.6700 | 14 | 0.5050 | 18 | 0.8175 | 15 |
| coil_3x3_33 | 5 | 0.3252 | 4 | 0.4430 | 8 | 0.5747 | 14 | 0.6692 | 17 | 0.7287 | 17 | 0.6700 | 13 | 0.5833 | 4 | 0.7794 | 19 |
| coil_3x4_56 | 0 | 0.1005 | 14 | 0.4289 | 9 | 0.6539 | 8 | 0.7440 | 10 | 0.7935 | 10 | 0.7582 | 9 | 0.5050 | 14 | 0.8464 | 13 |
| coil_3x4_56_4 | 0 | 0.1005 | 15 | 0.4289 | 10 | 0.6539 | 9 | 0.7440 | 11 | 0.7935 | 11 | 0.7582 | 10 | 0.5050 | 17 | 0.8464 | 14 |
| coil_3x4_56_2 | 0 | 0.0596 | 20 | 0.3668 | 11 | 0.6549 | 6 | 0.7487 | 8 | 0.7967 | 8 | 0.7525 | 11 | 0.5050 | 15 | 0.8559 | 9 |
| coil_3x4_56_3 | 0 | 0.0596 | 21 | 0.3668 | 12 | 0.6549 | 7 | 0.7487 | 9 | 0.7967 | 9 | 0.7525 | 12 | 0.5050 | 16 | 0.8559 | 10 |
| coil_3x9_14 | 9 | 0.2130 | 5 | 0.3508 | 13 | 0.5331 | 17 | 0.6547 | 18 | 0.7247 | 18 | 0.6644 | 17 | 0.5500 | 5 | 0.8041 | 16 |
| coil_4x8_14 | 9 | 0.2072 | 6 | 0.3367 | 14 | 0.5177 | 19 | 0.6430 | 19 | 0.7151 | 19 | 0.6700 | 15 | 0.5500 | 6 | 0.7986 | 17 |
| coil_4x9_14 | 9 | 0.1961 | 8 | 0.3292 | 15 | 0.5332 | 16 | 0.6725 | 16 | 0.7489 | 15 | 0.6700 | 16 | 0.5500 | 7 | 0.8482 | 12 |
| coil_5x7_14 | 9 | 0.1983 | 7 | 0.3188 | 16 | 0.4972 | 20 | 0.6255 | 20 | 0.7006 | 20 | 0.5825 | 20 | 0.5500 | 8 | 0.7868 | 18 |
| coil_4x4_38 | 0 | 0.0567 | 22 | 0.3174 | 17 | 0.6343 | 11 | 0.7548 | 7 | 0.8127 | 7 | 0.8067 | 7 | 0.5050 | 21 | 0.8983 | 5 |
| coil_3x8_16 | 11 | 0.1805 | 9 | 0.3069 | 18 | 0.4762 | 21 | 0.5903 | 21 | 0.6598 | 21 | 0.4927 | 21 | 0.5417 | 9 | 0.7317 | 21 |
| coil_5x8_14 | 9 | 0.0823 | 16 | 0.2712 | 19 | 0.5247 | 18 | 0.6743 | 14 | 0.7539 | 14 | 0.6416 | 18 | 0.5050 | 24 | 0.8665 | 6 |
| coil_2x2_110 | 0 | 0.0315 | 23 | 0.2127 | 20 | 0.6187 | 12 | 0.7667 | 6 | 0.8310 | 5 | 1.0000 | 1 | 0.5050 | 10 | 0.9501 | 1 |
| coil_4x7_16 | 11 | 0.0755 | 17 | 0.2060 | 21 | 0.3779 | 22 | 0.4968 | 22 | 0.5717 | 22 | 0.3400 | 22 | 0.5050 | 22 | 0.6531 | 22 |
| coil_5x5_38 | 0 | 0.0309 | 24 | 0.1830 | 22 | 0.5524 | 15 | 0.7077 | 13 | 0.7793 | 12 | 0.8067 | 8 | 0.5050 | 23 | 0.9066 | 4 |
| coil_3x7_18 | 13 | 0.0701 | 18 | 0.1766 | 23 | 0.3366 | 23 | 0.4669 | 23 | 0.5568 | 23 | 0.2390 | 23 | 0.5050 | 19 | 0.6476 | 23 |
| coil_3x7_18_2 | 13 | 0.0701 | 19 | 0.1766 | 24 | 0.3366 | 24 | 0.4669 | 24 | 0.5568 | 24 | 0.2390 | 24 | 0.5050 | 20 | 0.6476 | 24 |

**The median does not survive the weighting.** It is an order statistic, and weight is
applied by repetition, so touching occupies 5 of the 13 values and can simply *be*
the median. 3 coils tie at exactly 1.0000. Read the median column knowing that;
the power means do not have this problem.

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_110 ranks **1** under one mean
and **23** under another — a swing of 22 places in a field of 24. coil_5x5_38 swings 20.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_110` | pieces = 0.010 | #23 | #1 |
| `coil_5x5_38` | box = 0.010 | #24 | #4 |
| `coil_5x8_14` | cross area = 0.010 | #16 | #6 |

`coil_2x2_110` is the clearest case: one input on the floor and another at the ceiling.
The mean that punishes weak spots reads it as disqualified; the mean that rewards strong
ones reads it as the best thing here. Both are arithmetically correct — they are
answering different questions. `coil_5x5_38` is the same shape of argument, its weak spot
being box.

Harmonic and contraharmonic agree on **1** of 24 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 2, which is
why the geometric mean is the usual choice when no weak spot should be forgiven but
outright disqualification is too strong.

## What survives

`coil_3x3_38` comes first under **3 of the 8 means**, and the reason is visible in the
table above: its worst input is 0.641, where every other contender has something
at 0.01. It does not win by being outstanding anywhere. It wins by having nothing to
punish, which is the one way to be robust to the choice of mean.

If a weak spot is genuinely fatal — a shared wall that will leak, a coil too fat for
the body — use the harmonic mean, or filter and then rank. If the design is allowed one
bad number in exchange for a very good one, use quadratic or cubic. The arithmetic mean
is the choice that declines to say.

## Ranking once, not repeatedly

A tempting variant is to rank, cut the bottom half, and re-rank the survivors. Do not.

* **harmonic, min-max (what SCORING.md uses)** — survivors reordered 6/12, 5/6, 2/3, 0/2 over the rounds (13 moves in total)
* **geometric, min-max** — survivors reordered 10/12, 5/6, 0/3, 0/2 over the rounds (15 moves in total)
* **geometric, pure ratio-to-best** — survivors reordered 0/12, 0/6, 0/3, 0/2 over the rounds (0 moves in total)

The first two reorder coils that did not change, purely because other coils left the
set. `coil_3x3_36` places 3rd of 24 and 1st of the surviving 9; `coil_3x3_38`
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
because a composite is a compromise. `coil_2x2_110` has the narrowest cross-section in
the set and does not survive round 0 of 2 of the 3 runs.

    node tools/iterate.js        # the numbers above
