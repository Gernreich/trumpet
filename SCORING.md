# Scoring

Eight metrics, four ways of combining them, and a touching flag folded in as
specified: **-1 / +1** as a factor in the geometric mean, **-100 / +100** as a term
in the additive one. Regenerate with `node tools/gen_scoring.js`; the table comes
straight out of `tools/score.js`.

## The metrics scored

* **box** — less is better
* **cross area** — less is better
* **pieces** — less is better
* **distinct** — less is better
* **blocks/360** — less is better
* **rise/360** — less is better
* **turns/m** — less is better
* **longest str** — more is better
* **touching** — the flag, handled separately

A mean cannot tell a cost from a benefit, so every metric is first oriented so that
bigger is better. In the raw columns that means taking the reciprocal of the
less-is-better ones; in the normalized columns the normalization does it.

## The four scorings, and two repairs

| spiral | touch | geo raw | # | add raw | # | geo norm | # | add norm | # | geo fix | # | add fix | # |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coil_3x3_53_2 | 0 | 0.1172 | 1 | 11.63 | 1 | 0.7272 | 1 | 11.80 | 1 | 0.7272 | 1 | 0.8341 | 1 |
| coil_3x3_53 | 0 | 0.1127 | 2 | 11.62 | 2 | 0.7245 | 2 | 11.77 | 2 | 0.7245 | 2 | 0.8087 | 2 |
| staircase_coil | 0 | 0.09783 | 6 | 11.62 | 3 | 0.3446 | 3 | 11.63 | 3 | 0.3446 | 9 | 0.6958 | 5 |
| coil_3x4_73_2 | 0 | 0.1000 | 4 | 11.51 | 5 | 0.2487 | 5 | 11.57 | 4 | 0.2487 | 14 | 0.6452 | 6 |
| coil_3x4_73 | 0 | 0.09803 | 5 | 11.51 | 6 | 0.2426 | 6 | 11.55 | 5 | 0.2426 | 15 | 0.6302 | 7 |
| coil_3x4_74 | 0 | 0.09750 | 7 | 11.51 | 7 | 0.2913 | 4 | 11.55 | 6 | 0.2913 | 12 | 0.6279 | 8 |
| coil_2x2_146 | 0 | 0.1083 | 3 | 11.53 | 4 | 0.1525 | 8 | 11.53 | 7 | 0.1525 | 18 | 0.6123 | 9 |
| coil_3x4_78 | 0 | 0.09422 | 8 | 11.51 | 8 | 0.2199 | 7 | 11.48 | 8 | 0.2199 | 17 | 0.5777 | 11 |
| coil_3x3_50 | 8 | -0.1166 | 18 | -10.59 | 15 | -0.7573 | 18 | -10.43 | 9 | 0.5932 | 3 | 0.7177 | 3 |
| coil_3x9_18 | 16 | -0.1156 | 17 | -10.56 | 9 | -0.7312 | 16 | -10.44 | 10 | 0.5338 | 5 | 0.6037 | 10 |
| coil_3x3_47 | 8 | -0.1151 | 16 | -10.60 | 16 | -0.7434 | 17 | -10.45 | 11 | 0.5824 | 4 | 0.7075 | 4 |
| coil_4x8_18 | 16 | -0.1113 | 14 | -10.56 | 10 | -0.6774 | 14 | -10.47 | 12 | 0.4944 | 7 | 0.5755 | 12 |
| coil_3x8_20 | 17 | -0.1129 | 15 | -10.57 | 11 | -0.7165 | 15 | -10.48 | 13 | 0.5197 | 6 | 0.5609 | 14 |
| coil_4x9_17 | 14 | -0.1066 | 12 | -10.57 | 13 | -0.4265 | 12 | -10.52 | 14 | 0.3156 | 10 | 0.5679 | 13 |
| coil_5x7_18 | 16 | -0.1064 | 11 | -10.57 | 12 | -0.6058 | 13 | -10.52 | 15 | 0.4422 | 8 | 0.5393 | 16 |
| coil_5x8_17 | 14 | -0.1045 | 9 | -10.57 | 14 | -0.3175 | 9 | -10.54 | 16 | 0.2350 | 16 | 0.5512 | 15 |
| coil_3x7_22 | 20 | -0.1102 | 13 | -10.68 | 17 | -0.4062 | 10 | -10.60 | 17 | 0.2896 | 13 | 0.4176 | 18 |
| coil_4x7_20 | 18 | -0.1057 | 10 | -10.68 | 18 | -0.4077 | 11 | -10.61 | 18 | 0.2939 | 11 | 0.4333 | 17 |

`geo fix` and `add fix` are the same intent without the traps below.

## Can each metric be normalized?

Yes — and for the additive mean it is not optional. Raw box volume runs in the
hundreds while turns/m runs about 10 to 14, so an unnormalized sum is very nearly a
ranking by box volume alone. Two normalizations are worth separating:

**Ratio to best** (`best / x` for less-is-better) is a pure per-metric rescaling into
(0,1]. **It cannot change a geometric-mean ranking at all** — scaling metric *i* by
*cᵢ* multiplies every spiral's score by the same (∏cᵢ)^(1/n). Measured here: 18/18
ranks identical to raw.

**Min-max** ((x−min)/(max−min)) shifts as well as scales, and a shift is not
scale-invariant, so it does change the geometric ranking — 11/18 ranks move. It also
sends the worst value in each metric to zero, which annihilates a product, so the
floor here is 0.01 rather than 0.

So: normalize for the additive mean because you must; for the geometric mean, know
that a pure rescale buys nothing and a min-max is a real change of question.

## Three things the specified scheme does

**1. In a geometric mean, -1 does not penalize — it flips the sign, and inverts the
order it is applied to.** Magnitude is the quality; the negative sign then sorts the
largest magnitude last. Among the 10 touching spirals, ranking by score and ranking by
|score| are exact mirrors in **10/10** positions. The best touching coil is ranked the
worst touching coil. A multiplicative penalty has to be a factor *below one*: 1 is
the identity, so "+1 for clean" correctly does nothing, but its opposite is 0.5, not
-1.

**2. It depends on how many metrics are in the mean.** With 8 metrics plus the flag
there are 9 values — odd, so a negative product has a real root. Drop one metric
and there are 8, and every touching spiral scores `NaN`: no real even root of a
negative number. The score is one metric away from undefined.

**3. ±100 is not a weight, it is a verdict.** It accounts for **99.4%** of the raw score
range and **98.6%** of the normalized one — the full spread is 22.41 and everything the
other 8 metrics do fits in 0.31 of it. That is a filter written as a mean. If
touching really is disqualifying, filtering on it is clearer and says so; if it is
merely bad, it wants a weight you can turn.

`add fix` puts touching on the same 0..1 scale as the rest with an explicit weight of
3, and `geo fix` uses a factor of 1/(1+touching) — positive, graded by how much contact
there is, and indifferent to how many metrics sit beside it.

## What survives all six

**coil_3x3_53_2** comes first under every one of the six scorings — literal and repaired, raw and normalized. When a ranking is that indifferent to the scheme, the scheme is not what is deciding it.

The repairs do move things. Under the literal scheme every touching spiral sorts below
every clean one, so 8 clean coils take the top 8 places. Under `geo fix` and
`add fix`, `coil_3x3_50` and `coil_3x3_47` climb into the top four on the strength of
everything else — a graded penalty lets a coil be good enough elsewhere to be worth
the contact, and a verdict never does.
