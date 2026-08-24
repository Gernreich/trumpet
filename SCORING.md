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
| coil_3x3_53_2 | 0 | 0.8883 | 1 | 0.8988 | 1 | 0.9081 | 1 | 0.9162 | 1 | 0.9234 | 1 | 1.0000 | 2 | 0.8053 | 2 | 0.9245 | 3 |
| coil_3x3_53 | 0 | 0.8492 | 2 | 0.8619 | 2 | 0.8740 | 2 | 0.8851 | 2 | 0.8952 | 2 | 0.9438 | 4 | 0.8188 | 1 | 0.8963 | 5 |
| staircase_coil | 0 | 0.1037 | 12 | 0.4752 | 3 | 0.7167 | 3 | 0.8044 | 3 | 0.8488 | 3 | 1.0000 | 3 | 0.5050 | 17 | 0.9030 | 4 |
| coil_3x4_74 | 0 | 0.1048 | 11 | 0.4559 | 4 | 0.6660 | 5 | 0.7483 | 7 | 0.7950 | 8 | 0.7377 | 7 | 0.5050 | 13 | 0.8408 | 10 |
| coil_3x4_78 | 0 | 0.1055 | 10 | 0.4443 | 5 | 0.6389 | 7 | 0.7240 | 9 | 0.7776 | 9 | 0.6700 | 11 | 0.5050 | 14 | 0.8205 | 11 |
| coil_3x4_73_2 | 0 | 0.1016 | 14 | 0.4432 | 6 | 0.6732 | 4 | 0.7606 | 5 | 0.8065 | 6 | 0.7800 | 6 | 0.5050 | 12 | 0.8594 | 7 |
| coil_3x4_73 | 0 | 0.1017 | 13 | 0.4381 | 7 | 0.6613 | 6 | 0.7481 | 8 | 0.7953 | 7 | 0.7263 | 8 | 0.5050 | 11 | 0.8463 | 9 |
| coil_3x3_50 | 8 | 0.2349 | 3 | 0.3704 | 8 | 0.5337 | 10 | 0.6385 | 13 | 0.6981 | 14 | 0.6948 | 9 | 0.5556 | 4 | 0.7640 | 15 |
| coil_3x3_47 | 8 | 0.2340 | 4 | 0.3656 | 9 | 0.5242 | 11 | 0.6278 | 15 | 0.6882 | 15 | 0.6700 | 10 | 0.5556 | 3 | 0.7519 | 16 |
| coil_3x9_18 | 16 | 0.1355 | 6 | 0.2872 | 10 | 0.5183 | 12 | 0.6513 | 12 | 0.7200 | 12 | 0.6650 | 15 | 0.5294 | 6 | 0.8184 | 12 |
| coil_4x9_17 | 14 | 0.1424 | 5 | 0.2810 | 11 | 0.5164 | 14 | 0.6636 | 11 | 0.7388 | 11 | 0.6700 | 12 | 0.5333 | 5 | 0.8527 | 8 |
| coil_4x8_18 | 16 | 0.1331 | 7 | 0.2749 | 12 | 0.5009 | 15 | 0.6368 | 14 | 0.7073 | 13 | 0.6698 | 14 | 0.5294 | 7 | 0.8096 | 13 |
| coil_2x2_146 | 0 | 0.0408 | 18 | 0.2650 | 13 | 0.6353 | 8 | 0.7733 | 4 | 0.8359 | 4 | 1.0000 | 1 | 0.5050 | 10 | 0.9413 | 1 |
| coil_3x8_20 | 17 | 0.1271 | 9 | 0.2605 | 14 | 0.4625 | 17 | 0.5882 | 17 | 0.6614 | 17 | 0.4577 | 17 | 0.5278 | 9 | 0.7480 | 17 |
| coil_5x7_18 | 16 | 0.1292 | 8 | 0.2577 | 15 | 0.4724 | 16 | 0.6090 | 16 | 0.6820 | 16 | 0.5889 | 16 | 0.5294 | 8 | 0.7850 | 14 |
| coil_5x8_17 | 14 | 0.0711 | 15 | 0.2339 | 16 | 0.5166 | 13 | 0.6764 | 10 | 0.7555 | 10 | 0.6700 | 13 | 0.5050 | 16 | 0.8857 | 6 |
| coil_5x5_55 | 0 | 0.0316 | 19 | 0.2191 | 17 | 0.6199 | 9 | 0.7572 | 6 | 0.8173 | 5 | 0.8265 | 5 | 0.5050 | 15 | 0.9250 | 2 |
| coil_4x7_20 | 18 | 0.0627 | 16 | 0.1720 | 18 | 0.3654 | 18 | 0.4965 | 18 | 0.5751 | 18 | 0.3400 | 18 | 0.5022 | 18 | 0.6746 | 19 |
| coil_3x7_22 | 20 | 0.0590 | 17 | 0.1533 | 19 | 0.3369 | 19 | 0.4797 | 19 | 0.5727 | 19 | 0.2193 | 19 | 0.5019 | 19 | 0.6830 | 18 |

**The median does not survive the weighting.** It is an order statistic, and weight is
applied by repetition, so touching occupies 5 of the 13 values and can simply *be*
the median. 3 coils tie at exactly 1.0000. Read the median column knowing that;
the power means do not have this problem.

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_146 ranks **1** under one mean
and **18** under another — a swing of 17 places in a field of 19. coil_5x5_55 swings 17.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_146` | rise/360 = 0.010 | #18 | #1 |
| `staircase_coil` | distinct = 0.010 | #12 | #4 |
| `coil_3x3_53_2` | rise/360 = 0.611 | #1 | #3 |

`coil_2x2_146` has the slackest pitch in the set and a 2x2 cross-section: one input at
the floor, another at the ceiling. The harmonic mean reads it as disqualified, the
contraharmonic as the best thing here. Both are arithmetically correct; they are
answering different questions. The staircase coil is the same shape of argument, its
weak spot being distinct.

Harmonic and contraharmonic agree on **0** of 19 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 2, which is
why the geometric mean is the usual choice when no weak spot should be forgiven but
outright disqualification is too strong.

## What survives

`coil_3x3_53_2` comes first under **5 of the 8 means**, and the reason is visible in the
table above: its worst input is 0.611, where every other contender has something
at 0.01. It does not win by being outstanding anywhere. It wins by having nothing to
punish, which is the one way to be robust to the choice of mean.

If a weak spot is genuinely fatal — a shared wall that will leak, a coil too fat for
the body — use the harmonic mean, or filter and then rank. If the design is allowed one
bad number in exchange for a very good one, use quadratic or cubic. The arithmetic mean
is the choice that declines to say.

## Ranking once, not repeatedly

A tempting variant is to rank, cut the bottom half, and re-rank the survivors. Do not.

* **harmonic, min-max (what SCORING.md uses)** — survivors reordered 7/10, 4/5, 3/3, 0/2 over the rounds (14 moves in total)
* **geometric, min-max** — survivors reordered 7/10, 2/5, 2/3, 0/2 over the rounds (11 moves in total)
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
