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
on all 18. What changes with *p* is not the size of the score but how much a single
bad metric is allowed to sink it.

## The table

| spiral | touch | harmonic | # | geometric | # | arithmetic | # | quadratic | # | cubic | # | median | # | midrange | # | contraharmonic | # |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coil_3x3_53_2 | 0 | 0.8794 | 1 | 0.8904 | 1 | 0.9003 | 1 | 0.9091 | 1 | 0.9168 | 1 | 1.0000 | 2 | 0.8053 | 2 | 0.9180 | 3 |
| coil_3x3_53 | 0 | 0.8380 | 2 | 0.8519 | 2 | 0.8649 | 2 | 0.8770 | 2 | 0.8880 | 2 | 0.8958 | 4 | 0.8120 | 1 | 0.8893 | 4 |
| coil_3x3_50 | 8 | 0.2338 | 3 | 0.3656 | 3 | 0.5251 | 9 | 0.6292 | 12 | 0.6892 | 13 | 0.6948 | 8 | 0.5556 | 4 | 0.7540 | 14 |
| coil_3x3_47 | 8 | 0.2330 | 4 | 0.3617 | 4 | 0.5176 | 10 | 0.6212 | 13 | 0.6827 | 14 | 0.6700 | 9 | 0.5556 | 3 | 0.7456 | 15 |
| coil_3x4_74 | 0 | 0.0878 | 10 | 0.3513 | 5 | 0.6182 | 5 | 0.7323 | 7 | 0.7890 | 7 | 0.7377 | 6 | 0.5050 | 13 | 0.8674 | 8 |
| staircase_coil | 0 | 0.0567 | 15 | 0.3376 | 6 | 0.6721 | 3 | 0.7887 | 3 | 0.8421 | 3 | 1.0000 | 3 | 0.5050 | 16 | 0.9257 | 2 |
| coil_3x4_78 | 0 | 0.0582 | 13 | 0.3151 | 7 | 0.5906 | 8 | 0.7072 | 8 | 0.7715 | 8 | 0.6700 | 10 | 0.5050 | 14 | 0.8469 | 9 |
| coil_3x4_73 | 0 | 0.0536 | 16 | 0.2941 | 8 | 0.6135 | 6 | 0.7325 | 6 | 0.7891 | 6 | 0.7263 | 7 | 0.5050 | 11 | 0.8747 | 6 |
| coil_3x4_73_2 | 0 | 0.0517 | 17 | 0.2915 | 9 | 0.6252 | 4 | 0.7454 | 5 | 0.8005 | 5 | 0.7800 | 5 | 0.5050 | 12 | 0.8887 | 5 |
| coil_3x9_18 | 16 | 0.1352 | 6 | 0.2838 | 10 | 0.5091 | 11 | 0.6399 | 11 | 0.7083 | 11 | 0.6197 | 13 | 0.5294 | 6 | 0.8044 | 11 |
| coil_4x9_17 | 14 | 0.1418 | 5 | 0.2754 | 11 | 0.5017 | 12 | 0.6469 | 10 | 0.7235 | 10 | 0.6353 | 11 | 0.5333 | 5 | 0.8343 | 10 |
| coil_4x8_18 | 16 | 0.1326 | 7 | 0.2693 | 12 | 0.4856 | 14 | 0.6185 | 14 | 0.6895 | 12 | 0.6251 | 12 | 0.5294 | 7 | 0.7878 | 12 |
| coil_3x8_20 | 17 | 0.1264 | 9 | 0.2545 | 13 | 0.4496 | 16 | 0.5744 | 16 | 0.6486 | 16 | 0.4500 | 16 | 0.5278 | 9 | 0.7339 | 16 |
| coil_5x7_18 | 16 | 0.1284 | 8 | 0.2501 | 14 | 0.4526 | 15 | 0.5866 | 15 | 0.6617 | 15 | 0.5332 | 14 | 0.5294 | 8 | 0.7602 | 13 |
| coil_2x2_146 | 0 | 0.0393 | 18 | 0.2328 | 15 | 0.6087 | 7 | 0.7593 | 4 | 0.8261 | 4 | 1.0000 | 1 | 0.5050 | 10 | 0.9473 | 1 |
| coil_5x8_17 | 14 | 0.0708 | 11 | 0.2273 | 16 | 0.4990 | 13 | 0.6601 | 9 | 0.7434 | 9 | 0.5040 | 15 | 0.5050 | 15 | 0.8733 | 7 |
| coil_4x7_20 | 18 | 0.0624 | 12 | 0.1660 | 17 | 0.3464 | 17 | 0.4723 | 17 | 0.5499 | 18 | 0.3120 | 17 | 0.5022 | 17 | 0.6439 | 18 |
| coil_3x7_22 | 20 | 0.0578 | 14 | 0.1434 | 18 | 0.3209 | 18 | 0.4672 | 18 | 0.5621 | 17 | 0.1135 | 18 | 0.5019 | 18 | 0.6802 | 17 |

**The median does not survive the weighting.** It is an order statistic, and weight is
applied by repetition, so touching occupies 5 of the 13 values and can simply *be*
the median. 3 coils tie at exactly 1.0000. Read the median column knowing that;
the power means do not have this problem.

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. coil_2x2_146 ranks **1** under one mean
and **18** under another — a swing of 17 places in a field of 18. staircase_coil swings 14.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
| `coil_2x2_146` | rise/360 = 0.010 | #18 | #1 |
| `staircase_coil` | distinct = 0.010 | #15 | #2 |
| `coil_3x3_53_2` | rise/360 = 0.611 | #1 | #3 |

`coil_2x2_146` has the slackest pitch in the set and a 2x2 cross-section: one input at
the floor, another at the ceiling. The harmonic mean reads it as disqualified, the
contraharmonic as the best thing here. Both are arithmetically correct; they are
answering different questions. The staircase coil is the same shape of argument, its
weak spot being distinct.

Harmonic and contraharmonic agree on **0** of 18 placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on 4, which is
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

* **harmonic, min-max (what SCORING.md uses)** — survivors reordered 7/9, 5/5, 3/3, 0/2 over the rounds (15 moves in total)
* **geometric, min-max** — survivors reordered 4/9, 0/5, 0/3, 0/2 over the rounds (4 moves in total)
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
