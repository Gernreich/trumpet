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
on all 19. What changes with *p* is not the size of the score but how much a single
bad metric is allowed to sink it.

## The table

| spiral | touch | harmonic | # | geometric | # | arithmetic | # | quadratic | # | cubic | # | median | # | midrange | # | contraharmonic | # |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coil_3x3_53_2 | 0 | 0.8830 | 1 | 0.8911 | 1 | 0.8987 | 1 | 0.9056 | 1 | 0.9119 | 1 | 0.9231 | 3 | 0.8237 | 2 | 0.9126 | 3 |
| coil_3x3_53 | 0 | 0.8597 | 2 | 0.8705 | 2 | 0.8807 | 2 | 0.8902 | 2 | 0.8989 | 2 | 0.9231 | 2 | 0.8261 | 1 | 0.8998 | 4 |
| coil_3x4_74 | 0 | 0.1047 | 10 | 0.4561 | 3 | 0.6675 | 3 | 0.7501 | 5 | 0.7966 | 6 | 0.7525 | 8 | 0.5050 | 13 | 0.8428 | 10 |
| coil_3x4_73_2 | 0 | 0.1023 | 12 | 0.4422 | 4 | 0.6633 | 4 | 0.7495 | 6 | 0.7967 | 5 | 0.7565 | 7 | 0.5050 | 12 | 0.8469 | 8 |
| coil_3x4_73 | 0 | 0.1023 | 13 | 0.4380 | 5 | 0.6570 | 5 | 0.7448 | 7 | 0.7937 | 7 | 0.7565 | 6 | 0.5050 | 11 | 0.8443 | 9 |
| coil_3x4_78 | 0 | 0.1043 | 11 | 0.4282 | 6 | 0.6246 | 8 | 0.7156 | 8 | 0.7731 | 9 | 0.6700 | 10 | 0.5050 | 14 | 0.8199 | 11 |
| coil_3x3_50 | 7 | 0.2583 | 3 | 0.3873 | 7 | 0.5382 | 10 | 0.6383 | 12 | 0.6967 | 13 | 0.6452 | 15 | 0.5625 | 3 | 0.7569 | 16 |
| coil_3x3_47 | 8 | 0.2347 | 4 | 0.3686 | 8 | 0.5298 | 11 | 0.6339 | 13 | 0.6937 | 14 | 0.6700 | 9 | 0.5556 | 4 | 0.7584 | 15 |
| staircase_coil | 0 | 0.0580 | 17 | 0.3371 | 9 | 0.6474 | 6 | 0.7615 | 4 | 0.8169 | 4 | 0.8220 | 4 | 0.5050 | 17 | 0.8957 | 5 |
| coil_3x9_18 | 15 | 0.1425 | 5 | 0.2885 | 10 | 0.5052 | 14 | 0.6338 | 14 | 0.7023 | 12 | 0.6603 | 13 | 0.5313 | 6 | 0.7950 | 12 |
| coil_4x9_17 | 14 | 0.1423 | 6 | 0.2808 | 11 | 0.5164 | 13 | 0.6642 | 11 | 0.7400 | 11 | 0.6700 | 11 | 0.5333 | 5 | 0.8543 | 7 |
| coil_4x8_18 | 15 | 0.1397 | 7 | 0.2749 | 12 | 0.4845 | 15 | 0.6151 | 15 | 0.6854 | 15 | 0.6499 | 14 | 0.5313 | 7 | 0.7809 | 13 |
| coil_2x2_146 | 0 | 0.0408 | 18 | 0.2655 | 13 | 0.6356 | 7 | 0.7733 | 3 | 0.8359 | 3 | 1.0000 | 1 | 0.5050 | 10 | 0.9409 | 1 |
| coil_5x7_18 | 15 | 0.1357 | 8 | 0.2613 | 14 | 0.4669 | 16 | 0.6005 | 16 | 0.6734 | 16 | 0.5701 | 16 | 0.5313 | 8 | 0.7724 | 14 |
| coil_3x8_20 | 17 | 0.1273 | 9 | 0.2612 | 15 | 0.4628 | 17 | 0.5869 | 17 | 0.6586 | 17 | 0.4834 | 17 | 0.5278 | 9 | 0.7442 | 17 |
| coil_5x8_17 | 13 | 0.0731 | 14 | 0.2405 | 16 | 0.5201 | 12 | 0.6793 | 10 | 0.7589 | 10 | 0.6700 | 12 | 0.5050 | 16 | 0.8872 | 6 |
| coil_4x7_20 | 17 | 0.0642 | 15 | 0.1754 | 17 | 0.3645 | 18 | 0.4922 | 18 | 0.5688 | 18 | 0.3400 | 18 | 0.4996 | 19 | 0.6647 | 19 |
| coil_3x7_22 | 19 | 0.0605 | 16 | 0.1568 | 18 | 0.3376 | 19 | 0.4772 | 19 | 0.5683 | 19 | 0.2354 | 19 | 0.5001 | 18 | 0.6744 | 18 |
| coil_5x5_55 | 0 | 0.0255 | 19 | 0.1544 | 19 | 0.5467 | 9 | 0.7080 | 9 | 0.7800 | 8 | 0.8140 | 5 | 0.5050 | 15 | 0.9167 | 2 |

**The median does not survive the weighting.** It is an order statistic, and weight is
applied by repetition, so touching occupies 5 of the 13 values and can simply *be*
the median. 1 coils tie at exactly 1.0000. Read the median column knowing that;
the power means do not have this problem.

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_146 ranks **1** under one mean
and **18** under another — a swing of 17 places in a field of 19. coil_5x5_55 swings 17.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_146` | rise/360 = 0.010 | #18 | #1 |
| `staircase_coil` | distinct = 0.010 | #17 | #5 |
| `coil_3x3_53_2` | rise/360 = 0.647 | #1 | #3 |

`coil_2x2_146` has the slackest pitch in the set and a 2x2 cross-section: one input at
the floor, another at the ceiling. The harmonic mean reads it as disqualified, the
contraharmonic as the best thing here. Both are arithmetically correct; they are
answering different questions. The staircase coil is the same shape of argument, its
weak spot being distinct.

Harmonic and contraharmonic agree on **2** of 19 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 3, which is
why the geometric mean is the usual choice when no weak spot should be forgiven but
outright disqualification is too strong.

## What survives

`coil_3x3_53_2` comes first under **5 of the 8 means**, and the reason is visible in the
table above: its worst input is 0.647, where every other contender has something
at 0.01. It does not win by being outstanding anywhere. It wins by having nothing to
punish, which is the one way to be robust to the choice of mean.

If a weak spot is genuinely fatal — a shared wall that will leak, a coil too fat for
the body — use the harmonic mean, or filter and then rank. If the design is allowed one
bad number in exchange for a very good one, use quadratic or cubic. The arithmetic mean
is the choice that declines to say.

## Ranking once, not repeatedly

A tempting variant is to rank, cut the bottom half, and re-rank the survivors. Do not.

* **harmonic, min-max (what SCORING.md uses)** — survivors reordered 5/10, 4/5, 0/3, 0/2 over the rounds (9 moves in total)
* **geometric, min-max** — survivors reordered 8/10, 0/5, 0/3, 0/2 over the rounds (8 moves in total)
* **geometric, pure ratio-to-best** — survivors reordered 0/10, 0/5, 0/3, 0/2 over the rounds (0 moves in total)

The first two reorder coils that did not change, purely because other coils left the
set. `coil_3x3_50` places 3rd of 19 and 1st of the surviving 9; `coil_3x3_53_2`
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
