# Scoring

Seven metrics, one touching count, and every common mean, so the ranking can be
read against the thing that produced it. Regenerate with `node tools/gen_scoring.js`.

## What is scored

* **box/block** — less is better
* **cross area** — less is better
* **pieces/block** — less is better
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
| coil_3x3_51 | 0 | 0.8866 | 1 | 0.8948 | 1 | 0.9024 | 1 | 0.9092 | 1 | 0.9154 | 1 | 0.9399 | 2 | 0.8225 | 1 | 0.9161 | 2 |
| coil_3x3_54 | 0 | 0.8505 | 2 | 0.8655 | 2 | 0.8786 | 2 | 0.8900 | 2 | 0.8999 | 2 | 0.9137 | 3 | 0.7757 | 2 | 0.9016 | 4 |
| coil_3x3_56_2 | 0 | 0.1128 | 11 | 0.5791 | 3 | 0.7705 | 3 | 0.8192 | 3 | 0.8458 | 3 | 0.8625 | 5 | 0.5050 | 12 | 0.8710 | 7 |
| coil_3x3_56 | 0 | 0.1128 | 10 | 0.5788 | 4 | 0.7698 | 4 | 0.8185 | 4 | 0.8451 | 4 | 0.8625 | 4 | 0.5050 | 11 | 0.8703 | 8 |
| coil_3x3_59 | 0 | 0.1124 | 12 | 0.5645 | 5 | 0.7518 | 5 | 0.8022 | 5 | 0.8311 | 6 | 0.8625 | 6 | 0.5050 | 13 | 0.8560 | 10 |
| coil_3x4_68 | 0 | 0.1063 | 13 | 0.4727 | 6 | 0.6786 | 6 | 0.7560 | 8 | 0.8000 | 8 | 0.7525 | 11 | 0.5050 | 14 | 0.8423 | 11 |
| coil_3x4_68_4 | 0 | 0.1063 | 14 | 0.4727 | 7 | 0.6786 | 7 | 0.7560 | 9 | 0.8000 | 9 | 0.7525 | 12 | 0.5050 | 17 | 0.8423 | 12 |
| coil_3x4_68_2 | 0 | 0.1057 | 16 | 0.4635 | 8 | 0.6696 | 8 | 0.7499 | 10 | 0.7960 | 10 | 0.7571 | 9 | 0.5050 | 15 | 0.8398 | 13 |
| coil_3x4_68_3 | 0 | 0.1057 | 17 | 0.4635 | 9 | 0.6696 | 9 | 0.7499 | 11 | 0.7960 | 11 | 0.7571 | 10 | 0.5050 | 16 | 0.8398 | 14 |
| coil_3x4_79 | 0 | 0.1060 | 15 | 0.4472 | 10 | 0.6390 | 12 | 0.7232 | 12 | 0.7769 | 13 | 0.6700 | 15 | 0.5050 | 18 | 0.8186 | 15 |
| coil_3x3_47 | 7 | 0.2585 | 3 | 0.3881 | 11 | 0.5395 | 15 | 0.6399 | 17 | 0.6988 | 18 | 0.6700 | 14 | 0.5625 | 3 | 0.7590 | 20 |
| coil_3x3_48 | 8 | 0.2364 | 4 | 0.3775 | 12 | 0.5476 | 13 | 0.6547 | 16 | 0.7141 | 16 | 0.7235 | 13 | 0.5556 | 4 | 0.7827 | 17 |
| coil_4x4_50 | 0 | 0.0583 | 22 | 0.3433 | 13 | 0.6506 | 10 | 0.7617 | 7 | 0.8163 | 7 | 0.8058 | 7 | 0.5050 | 21 | 0.8917 | 5 |
| coil_3x9_18 | 13 | 0.1601 | 5 | 0.3051 | 14 | 0.5125 | 18 | 0.6395 | 18 | 0.7084 | 17 | 0.6644 | 18 | 0.5357 | 5 | 0.7979 | 16 |
| coil_4x9_18 | 13 | 0.1509 | 8 | 0.2916 | 15 | 0.5283 | 16 | 0.6780 | 15 | 0.7550 | 15 | 0.6700 | 16 | 0.5357 | 7 | 0.8701 | 9 |
| coil_4x8_18 | 13 | 0.1566 | 6 | 0.2903 | 16 | 0.4907 | 19 | 0.6194 | 19 | 0.6901 | 19 | 0.6475 | 19 | 0.5357 | 6 | 0.7820 | 18 |
| coil_5x7_18 | 13 | 0.1517 | 7 | 0.2773 | 17 | 0.4768 | 20 | 0.6093 | 20 | 0.6824 | 20 | 0.5825 | 20 | 0.5357 | 8 | 0.7786 | 19 |
| coil_3x8_20 | 15 | 0.1414 | 9 | 0.2766 | 18 | 0.4738 | 21 | 0.5974 | 21 | 0.6691 | 21 | 0.4927 | 21 | 0.5313 | 9 | 0.7532 | 21 |
| coil_2x2_134 | 0 | 0.0410 | 23 | 0.2721 | 19 | 0.6412 | 11 | 0.7756 | 6 | 0.8372 | 5 | 1.0000 | 1 | 0.5050 | 10 | 0.9382 | 1 |
| coil_5x8_18 | 13 | 0.0731 | 18 | 0.2406 | 20 | 0.5204 | 17 | 0.6796 | 14 | 0.7592 | 14 | 0.6700 | 17 | 0.5050 | 24 | 0.8876 | 6 |
| coil_4x7_20 | 15 | 0.0677 | 19 | 0.1859 | 21 | 0.3760 | 22 | 0.5053 | 22 | 0.5831 | 22 | 0.3400 | 22 | 0.5050 | 22 | 0.6789 | 24 |
| coil_3x7_22 | 17 | 0.0635 | 20 | 0.1657 | 22 | 0.3469 | 23 | 0.4862 | 23 | 0.5772 | 23 | 0.2390 | 23 | 0.5050 | 19 | 0.6813 | 22 |
| coil_3x7_22_2 | 17 | 0.0635 | 21 | 0.1657 | 23 | 0.3469 | 24 | 0.4862 | 24 | 0.5772 | 24 | 0.2390 | 24 | 0.5050 | 20 | 0.6813 | 23 |
| coil_5x5_50 | 0 | 0.0255 | 24 | 0.1542 | 24 | 0.5460 | 14 | 0.7071 | 13 | 0.7792 | 12 | 0.8058 | 8 | 0.5050 | 23 | 0.9158 | 3 |

**The median does not survive the weighting.** It is an order statistic, and weight is
applied by repetition, so touching occupies 5 of the 13 values and can simply *be*
the median. 1 coils tie at exactly 1.0000. Read the median column knowing that;
the power means do not have this problem.

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_134 ranks **1** under one mean
and **23** under another — a swing of 22 places in a field of 24. coil_5x5_50 swings 21.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_134` | rise/360 = 0.010 | #23 | #1 |
| `coil_5x5_50` | box/block = 0.010 | #24 | #3 |
| `coil_5x8_18` | cross area = 0.010 | #18 | #6 |

`coil_2x2_134` is the clearest case: one input on the floor and another at the ceiling.
The mean that punishes weak spots reads it as disqualified; the mean that rewards strong
ones reads it as the best thing here. Both are arithmetically correct — they are
answering different questions. `coil_5x5_50` is the same shape of argument, its weak spot
being box/block.

Harmonic and contraharmonic agree on **1** of 24 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 3, which is
why the geometric mean is the usual choice when no weak spot should be forgiven but
outright disqualification is too strong.

## What survives

`coil_3x3_51` comes first under **6 of the 8 means**, and the reason is visible in the
table above: its worst input is 0.645, where every other contender has something
at 0.01. It does not win by being outstanding anywhere. It wins by having nothing to
punish, which is the one way to be robust to the choice of mean.

If a weak spot is genuinely fatal — a shared wall that will leak, a coil too fat for
the body — use the harmonic mean, or filter and then rank. If the design is allowed one
bad number in exchange for a very good one, use quadratic or cubic. The arithmetic mean
is the choice that declines to say.

## Ranking once, not repeatedly

A tempting variant is to rank, cut the bottom half, and re-rank the survivors. Do not.

* **harmonic, min-max (what SCORING.md uses)** — survivors reordered 8/12, 5/6, 2/3, 0/2 over the rounds (15 moves in total)
* **geometric, min-max** — survivors reordered 10/12, 3/6, 0/3, 0/2 over the rounds (13 moves in total)
* **geometric, pure ratio-to-best** — survivors reordered 0/12, 0/6, 0/3, 0/2 over the rounds (0 moves in total)

The first two reorder coils that did not change, purely because other coils left the
set. `coil_3x3_47` places 3rd of 24 and 1st of the surviving 9; `coil_3x3_51`
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
because a composite is a compromise. `coil_2x2_134` has the narrowest cross-section in
the set and does not survive round 0 of 2 of the 3 runs.

    node tools/iterate.js        # the numbers above
