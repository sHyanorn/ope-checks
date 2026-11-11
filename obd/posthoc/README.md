# Post hoc analyses

Everything in this directory was fixed after the confirmatory results were known. The analyses are descriptive. They give no verdict and they replace or reinterpret no registered label; the registration, its amendments and the files in `obd/results/` are unchanged.

```
python -m obd.posthoc.run
```

writes `results/units.json`, `results/features.json`, `results/propensities.json`, `results/blocks.json`, `results/lengths.json` and `results/distances.json`. The numbers of Sections 1 to 3 come from one run of commit `41969f3` (numpy 2.5.4); Sections 4 to 6 name their own runs. Intervals are 2.5th and 97.5th percentiles of 10,000 replicates. Wherever ten-minute blocks are resampled, the multiplicities are the registered ones.

## 1. Interval width and the resampling unit

The registration resamples ten-minute blocks because lists are reused and clicks cluster, so that neither rows nor impressions are independent (Section 5). How much narrower the intervals from rows or impressions are was measured on Men's only (Section 3). Here the two ratios of H3, IPS and SNIPS of the fixed-prior target over the on-policy value, get an interval under three resampling units on every campaign:

- rows, drawn in each log on its own;
- impressions as Section 7 of the registration defines them, drawn in each log on its own;
- ten-minute blocks, the registered bootstrap. Its columns reproduce the registered intervals.

Rows and impressions use `numpy.random.default_rng([20261110, 2, c, u, l])` with campaign `c` (all 0, men 1, women 2), unit `u` (rows 0, impressions 1) and log `l` (random 0, BTS 1).

| Campaign | Ratio | Estimate | Rows | Impressions | Ten-minute blocks |
|---|---|---|---|---|---|
| Men's | IPS | 0.891 | 0.818 to 0.964 | 0.816 to 0.968 | 0.790 to 1.005 |
| Men's | SNIPS | 0.908 | 0.834 to 0.983 | 0.832 to 0.987 | 0.805 to 1.022 |
| All | IPS | 0.948 | 0.888 to 1.009 | 0.885 to 1.011 | 0.867 to 1.033 |
| All | SNIPS | 0.948 | 0.888 to 1.008 | 0.885 to 1.011 | 0.867 to 1.032 |
| Women's | IPS | 1.004 | 0.942 to 1.068 | 0.941 to 1.071 | 0.917 to 1.099 |
| Women's | SNIPS | 1.004 | 0.942 to 1.067 | 0.941 to 1.070 | 0.917 to 1.099 |

Standard deviation of the replicates:

| Campaign | Ratio | Rows | Impressions | Blocks | Blocks over rows | Blocks over impressions |
|---|---|---|---|---|---|---|
| Men's | IPS | 0.0373 | 0.0382 | 0.0550 | 1.47 | 1.44 |
| Men's | SNIPS | 0.0379 | 0.0389 | 0.0556 | 1.47 | 1.43 |
| All | IPS | 0.0309 | 0.0323 | 0.0424 | 1.37 | 1.31 |
| All | SNIPS | 0.0309 | 0.0322 | 0.0421 | 1.36 | 1.31 |
| Women's | IPS | 0.0322 | 0.0333 | 0.0467 | 1.45 | 1.40 |
| Women's | SNIPS | 0.0321 | 0.0331 | 0.0466 | 1.45 | 1.41 |

- On all three campaigns the standard deviation with blocks is 1.31 to 1.47 times the one with rows or impressions.
- On All and Women's the interval contains 1 under each of the three units. On Men's the intervals from rows and from impressions lie below 1 and the interval from blocks contains 1. The unit decides on which side of 1 the upper end falls only on the development campaign.

The two measures of dependence that Section 3 reports for Men's, on every campaign:

- List reuse: the share of complete impressions that show the same three items in the same order as the complete impression before them, in time order. Under independent uniform draws it would be 0.0002% (All), 0.003% (Men's) and 0.001% (Women's) in the random log.
- Variance ratio: the variance of the difference in click rate between adjacent time blocks, over the variance that difference would have if impressions were independent. Blocks are paired without overlap. The variance of a block's click rate takes impressions as clusters and carries the factor G / (G - 1) for a block of G impressions. In brackets, the same after subtracting from each click the click rate of its (item, position) in the log. The last column drops the factor.

| Campaign | Log | Impressions | Complete | Same list as the one before | 1 min | 10 min | 60 min | 1 min, no factor |
|---|---|---|---|---|---|---|---|---|
| Men's | random | 147,487 | 142,227 | 0.370 | 1.18 (1.17) | 2.45 (2.44) | 2.07 (2.08) | 1.52 |
| Men's | BTS | 1,268,311 | 1,121,295 | 0.307 | 1.20 (1.20) | 2.08 (2.08) | 2.02 (2.00) | 1.23 |
| All | random | 423,896 | 387,225 | 0.346 | 1.29 (1.29) | 1.89 (1.88) | 2.10 (2.13) | 1.40 |
| All | BTS | 3,731,150 | 3,040,555 | 0.299 | 1.14 (1.14) | 1.85 (1.86) | 2.61 (2.52) | 1.15 |
| Women's | random | 280,211 | 268,167 | 0.357 | 1.13 (1.13) | 1.92 (1.89) | 2.07 (2.03) | 1.36 |
| Women's | BTS | 2,482,614 | 2,177,760 | 0.300 | 1.16 (1.16) | 2.23 (2.22) | 3.33 (3.34) | 1.17 |

- The Men's rows reproduce the list reuse of Section 3 (37% and 31%) and its ratio of 2.0 to 2.5 at ten minutes and more.
- Section 3 gives 1.2 to 1.5 at one minute. Only the last column reproduces that (1.52 and 1.23). Without the factor the ratio exceeds 1 for independent impressions when blocks hold few of them, as one-minute blocks do. With the factor the one-minute ratio on Men's is 1.18 and 1.20.
- On All and Women's lists repeat about as often (35% and 36% in the random logs, 30% in the BTS logs). The variance ratio is 1.13 to 1.29 at one minute and 1.85 to 2.23 at ten minutes.
- No ratio carries an interval. The ratio does not separate dependence between impressions from a click rate that drifts from one block to the next, and drift weighs more in long blocks. The sixty-minute ratios rest on 84 pairs of blocks; the differences among them are not interpreted.

## 2. The user feature that amendment 7 left unmatched

Amendment 7 treats two values of a user feature as one if exactly one value occurs only in the random log and exactly one only in the BTS log. Feature 2 on All and feature 3 on Women's did not meet that condition and were compared as written. What the feature columns show (no click is read):

| Campaign | Feature | Log | Value | Rows | Share of the log | Of them marked |
|---|---|---|---|---|---|---|
| All | 2 | random | `3a845d98` | 485,993 | 35.3623% | 485,993 |
| All | 2 | BTS | `1e58eb4f` | 4,362,623 | 35.3043% | 4,362,623 |
| All | 2 | BTS | `77fecf8c` | 30 | 0.0002% | 0 |
| Women's | 3 | random | `9eb4f471` | 195,980 | 22.6675% | 195,980 |
| Women's | 3 | BTS | `f97fde0d` | 1,771,203 | 22.8086% | 1,771,203 |
| Women's | 3 | BTS | `c9dce82b` | 14 | 0.0002% | 0 |

A row is marked if, in each of the three features that amendment 7 did match, it holds the value that occurs in its log only. There are 485,993 and 4,362,623 marked rows on All and 195,980 and 1,771,203 on Women's: in each log the three matched values sit on the same rows.

- The condition failed because the BTS log holds a second value that the random log lacks: 30 rows on All and 14 on Women's, none of them marked.
- The other value of each log sits on exactly the marked rows. This is the pattern amendment 7 found in the features it matched.

Taking those two values as one, H7 is recomputed by the registered code on a random log in which the value is written as the BTS log writes it. Every quantity outside H7 comes out as registered.

| Quantity | All, registered | All, post hoc | Women's, registered | Women's, post hoc |
|---|---|---|---|---|
| Distance, the unmatched feature | 0.3549 (0.3524 to 0.3581) | 0.0019 (0.0012 to 0.0037) | 0.2282 (0.2269 to 0.2314) | 0.0015 (0.0012 to 0.0040) |
| Joint distance | 0.3599 (0.3594 to 0.3651) | 0.0068 (0.0082 to 0.0106) | 0.2358 (0.2361 to 0.2409) | 0.0092 (0.0102 to 0.0135) |
| BTS rows whose combination is absent from the random log | 0.3531 (0.3505 to 0.3557) | 0.0001 (0.0001 to 0.0002) | 0.2282 (0.2265 to 0.2302) | 0.0001 (0.0002 to 0.0003) |
| Change in `rho` under user weights | -0.058 (-0.136 to 0.013) | 0.001 (-0.003 to 0.005) | -0.116 (-0.178 to -0.063) | -0.001 (-0.014 to 0.005) |

- With the value taken as one, the joint distance between the two logs is 0.007 on All and 0.009 on Women's. The registered reference, the same distance between the odd and the even ten-minute blocks of one log, is 0.006 (BTS) and 0.014 (random) on All and 0.006 and 0.015 on Women's.
- The change in `rho` under user weights is then 0.001 and -0.001, with intervals that contain 0. On Men's, where amendment 7 matched all four features, the registered change is -0.001 (-0.007 to 0.004).
- An estimate of a distance can lie below its own interval, as in the registered results: a distance between two resampled logs is biased upward.
- That the two values are one category is an inference from the rows they sit on, as in amendment 7. The files do not state it. The registered H7 numbers stand as registered; these are shown beside them.

## 3. H2: `M` below 1

On both confirmatory campaigns the mean `M` of `S` over the eligible cells is below 1 (0.973 and 0.967) and H2 is undetermined. Nothing here says why.

`M` at the registered eligibility bound and at two lower ones, with rough sizes of the two biases that Section 8 names:

- Grid bias, upward: to first order, if each recorded propensity is the share of 200,000 Monte Carlo draws. For a cell it is the sum of `(1 - p) / (200,000 p^2)` over its rows, over the rows of its position; the column is its mean over the eligible cells.
- Low hours, downward. Section 8 names a version that gave a cell a smaller propensity and was never chosen there. While such a version serves, the cell is shown less often than the propensities of its recorded rows imply. The hourly `S` of a cell is its sum of 1/propensity in an hour over the rows of its position in that hour. An hour is low if the hourly `S` is under 0.1 (or 0.5), and it then accounts for its share of the position's rows times (1 - hourly `S`) of the distance of `S` from 1. The columns give the sum over the low hours, averaged over the eligible cells.

| Campaign | Bound | Cells | Share of rows | `M` | Grid bias | Low hours, under 0.1 | Low hours, under 0.5 |
|---|---|---|---|---|---|---|---|
| Men's | 0.001 | 12 | 0.514 | 1.005 (0.997 to 1.013) | +0.0002 | 0.002 | 0.007 |
| Men's | 0.0005 | 25 | 0.731 | 0.996 (0.986 to 1.007) | +0.0005 | 0.018 | 0.041 |
| Men's | 0.0001 | 90 | 0.975 | 0.973 (0.961 to 0.986) | +0.0028 | 0.134 | 0.179 |
| All | 0.001 | 3 | 0.079 | 0.973 (0.957 to 0.990) | +0.0002 | 0.033 | 0.039 |
| All | 0.0005 | 16 | 0.248 | 0.984 (0.973 to 0.996) | +0.0006 | 0.026 | 0.048 |
| All | 0.0001 | 135 | 0.856 | 0.950 (0.938 to 0.962) | +0.0040 | 0.161 | 0.207 |
| Women's | 0.001 | 7 | 0.178 | 0.967 (0.955 to 0.980) | +0.0002 | 0.022 | 0.034 |
| Women's | 0.0005 | 22 | 0.434 | 0.978 (0.968 to 0.989) | +0.0005 | 0.030 | 0.049 |
| Women's | 0.0001 | 99 | 0.912 | 0.956 (0.944 to 0.968) | +0.0030 | 0.134 | 0.176 |

- At the registered bound the grid bias is +0.0002 on every campaign.
- At the registered bound the low hours account for 0.033 (under 0.1) and 0.039 (under 0.5) on All, where `M` is 0.027 below 1, and for 0.022 and 0.034 on Women's, where `M` is 0.033 below 1. On Men's, where `M` is 1.005, they account for 0.002 and 0.007.
- Low hours are picked by the value of the statistic itself, so some shortfall is found in any log. Men's shows how much on a campaign whose `M` is not below 1.
- The logs show that these hours exist and how much of the distance they hold. They do not show what was served in them, so the cause is not identified.
- With lower bounds `M` does not move one way on the confirmatory campaigns: it is closer to 1 at 0.0005 and further from 1 at 0.0001. At 0.0001 it is below 1, with an interval that excludes 1, on all three campaigns, Men's included.
- Below the registered bound the low-hour columns stop measuring a bias: at a propensity of 0.0001 a cell is expected to have hours without a row.

The eligible cells of the confirmatory campaigns at the registered bound. A low hour here has an hourly `S` under 0.1.

| Campaign | Item | Position | Rows | Smallest propensity | `S` | Low hours | Rows there | Rows of the position there | Distance held there |
|---|---|---|---|---|---|---|---|---|---|
| All | 7 | 2 | 315,716 | 0.001030 | 0.952 | 8 | 94 | 281,402 | 0.068 |
| All | 51 | 3 | 461,227 | 0.001510 | 1.001 | 1 | 13 | 17,779 | 0.004 |
| All | 63 | 2 | 205,080 | 0.002270 | 0.966 | 3 | 40 | 110,533 | 0.027 |
| Women's | 2 | 2 | 233,063 | 0.001005 | 0.939 | 8 | 34 | 180,344 | 0.069 |
| Women's | 26 | 2 | 368,713 | 0.001590 | 0.982 | 4 | 14 | 21,978 | 0.008 |
| Women's | 33 | 3 | 99,385 | 0.001360 | 0.971 | 2 | 8 | 7,537 | 0.003 |
| Women's | 34 | 2 | 197,058 | 0.001955 | 0.980 | 2 | 6 | 48,623 | 0.019 |
| Women's | 34 | 3 | 208,814 | 0.001070 | 0.968 | 1 | 3 | 22,420 | 0.009 |
| Women's | 38 | 1 | 127,294 | 0.001285 | 0.973 | 2 | 12 | 48,614 | 0.019 |
| Women's | 38 | 2 | 150,855 | 0.001290 | 0.959 | 3 | 14 | 67,990 | 0.026 |

- In their low hours the three cells of All have 147 rows among 409,714 rows of their positions, and the seven of Women's have 91 among 397,506. The rows they do have record propensities with a harmonic mean, by cell, of 0.03 to 0.13 (All) and 0.02 to 0.17 (Women's).
- `S` is below 1 in 2 of the 3 cells of All and in all 7 of Women's. On Men's it is below 1 in 6 of 12 cells and ranges from 0.991 to 1.026.
- On both confirmatory campaigns the cell whose smallest propensity is closest to the bound has the lowest `S`, and the cell with the most rows the highest. On Men's the cell closest to the bound has the highest `S` of the twelve. Three and seven cells do not establish a relation.

`M` at the registered bound by UTC day, from the blocks of that day:

| Day | Men's | All | Women's |
|---|---|---|---|
| 24 Nov | 1.010 (0.990 to 1.030) | 1.022 (0.988 to 1.058) | 0.974 (0.945 to 1.003) |
| 25 Nov | 1.004 (0.968 to 1.042) | 1.015 (0.977 to 1.055) | 0.993 (0.956 to 1.030) |
| 26 Nov | 0.994 (0.977 to 1.010) | 1.023 (0.987 to 1.060) | 0.995 (0.973 to 1.017) |
| 27 Nov | 1.004 (0.987 to 1.021) | 0.879 (0.832 to 0.931) | 0.946 (0.922 to 0.973) |
| 28 Nov | 1.006 (0.984 to 1.029) | 0.981 (0.946 to 1.016) | 0.999 (0.971 to 1.028) |
| 29 Nov | 1.006 (0.984 to 1.029) | 0.924 (0.881 to 0.968) | 0.863 (0.816 to 0.908) |
| 30 Nov | 1.007 (0.989 to 1.026) | 0.982 (0.932 to 1.034) | 1.003 (0.976 to 1.031) |

- At the registered bound `M` is below 1, with an interval that excludes 1, on 27 and 29 November on both confirmatory campaigns, and its interval contains 1 on the other five days. On Men's it contains 1 on every day.
- Of the distance held by low hours (under 0.1) at the registered bound, 0.031 of 0.033 on All and 0.021 of 0.022 on Women's falls on these two days.
- The pattern is weaker at the lower bounds (`m_by_day` in `results/propensities.json`). At 0.0005 Women's keeps both days and adds 30 November, while on All 27 November is at 1.000 and the only day whose interval excludes 1 is 25 November. At 0.0001 29 November is the lowest day on All and on Women's, and on Men's the lowest day is 24 November.
- The days were looked at after the results were known, and 63 daily intervals were computed, 21 of them in the table, without any allowance for their number. The table says where in the week the registered `M` falls short. It does not say why.

## 4. Interval width and the block length

The lengths, the random stream and the reading below were committed before this analysis was run; the commit that added them holds no result of it.

The registration resamples ten-minute blocks and says that the width of the intervals is the same for blocks of 5 to 60 minutes. That was measured on the fixed-prior ratios of Men's only, with 1,000 replicates of another random stream (Sections 3 and 8). Here the two ratios of H3 get an interval with clock blocks of 5, 10, 20, 30, 60 and 180 minutes as resampling units, on every campaign and on the pooled unit of Section 4 of the registration.

- A block of `L` minutes is the UTC clock interval of `L` minutes that contains the timestamp, counted from the start of the week. The week holds 2,016, 1,008, 504, 336, 168 and 56 of them.
- As in the registered bootstrap, a replicate draws as many blocks as the week holds, with replacement, a block carries the rows of both logs that fall in it, and the same blocks are drawn on every campaign. `pi0` stays as computed on the full data. Intervals are 2.5th and 97.5th percentiles of 10,000 replicates.
- At ten minutes the multiplicities are the registered ones, and the run stops if an interval differs from the registered one. At every other length the multiplicities of replicate `i` are `numpy.random.default_rng([20261110, 3, L, i]).multinomial(n, numpy.full(n, 1 / n))`, with `n` the number of blocks.
- Reported for each campaign, ratio and length: the interval, the standard deviation of the replicates, and that standard deviation over the one at ten minutes. The pooled unit is `0.54 x (All) + 0.46 x (Women's)`, computed within each replicate.

How it is read:

- It is descriptive. It gives no verdict and changes no registered label.
- Two things are stated from the table for each unit: the lengths at which the interval contains 1, and the range of the standard deviation over the one at ten minutes.
- The standard deviation of 10,000 replicates carries a Monte Carlo error of about 0.7% of its value (normal approximation), and the ratio of two of them about 1%. Lengths whose standard deviations differ by under 2% are not told apart.
- A standard deviation that grows with the length would point to dependence between rows, or to change over the week, that reaches beyond ten minutes. This analysis does not separate the two (Section 8 of the registration). At 180 minutes an interval rests on 56 resampling units.

The numbers below come from one run of commit `7ec1253` (numpy 2.5.3), `python -m obd.posthoc.run blocks`, stored in `results/blocks.json`. The intervals at ten minutes are the registered ones.

| Unit | Ratio | Estimate | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| Men's | IPS | 0.891 | 0.790 to 1.001 | 0.790 to 1.005 | 0.790 to 1.001 | 0.789 to 1.000 | 0.788 to 1.004 | 0.781 to 1.004 |
| Men's | SNIPS | 0.908 | 0.806 to 1.019 | 0.805 to 1.022 | 0.807 to 1.019 | 0.805 to 1.018 | 0.804 to 1.022 | 0.799 to 1.020 |
| All | IPS | 0.948 | 0.870 to 1.028 | 0.867 to 1.033 | 0.866 to 1.033 | 0.863 to 1.037 | 0.863 to 1.040 | 0.856 to 1.044 |
| All | SNIPS | 0.948 | 0.871 to 1.028 | 0.867 to 1.032 | 0.866 to 1.034 | 0.864 to 1.035 | 0.864 to 1.039 | 0.856 to 1.045 |
| Women's | IPS | 1.004 | 0.919 to 1.095 | 0.917 to 1.099 | 0.910 to 1.104 | 0.908 to 1.108 | 0.906 to 1.112 | 0.890 to 1.144 |
| Women's | SNIPS | 1.004 | 0.920 to 1.094 | 0.917 to 1.099 | 0.910 to 1.102 | 0.908 to 1.106 | 0.906 to 1.111 | 0.890 to 1.140 |
| Pooled | IPS | 0.974 | 0.916 to 1.035 | 0.915 to 1.036 | 0.911 to 1.039 | 0.907 to 1.042 | 0.909 to 1.042 | 0.897 to 1.056 |
| Pooled | SNIPS | 0.974 | 0.916 to 1.035 | 0.914 to 1.036 | 0.912 to 1.039 | 0.908 to 1.042 | 0.909 to 1.041 | 0.896 to 1.057 |

Standard deviation of the replicates, and in brackets over the one at ten minutes:

| Unit | Ratio | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|
| Men's | IPS | 0.0540 (0.98) | 0.0550 (1.00) | 0.0538 (0.98) | 0.0538 (0.98) | 0.0554 (1.01) | 0.0567 (1.03) |
| Men's | SNIPS | 0.0546 (0.98) | 0.0556 (1.00) | 0.0544 (0.98) | 0.0548 (0.98) | 0.0560 (1.01) | 0.0563 (1.01) |
| All | IPS | 0.0405 (0.95) | 0.0424 (1.00) | 0.0433 (1.02) | 0.0447 (1.05) | 0.0454 (1.07) | 0.0481 (1.13) |
| All | SNIPS | 0.0401 (0.95) | 0.0421 (1.00) | 0.0432 (1.03) | 0.0441 (1.05) | 0.0449 (1.07) | 0.0479 (1.14) |
| Women's | IPS | 0.0447 (0.96) | 0.0467 (1.00) | 0.0491 (1.05) | 0.0511 (1.09) | 0.0524 (1.12) | 0.0637 (1.36) |
| Women's | SNIPS | 0.0445 (0.95) | 0.0466 (1.00) | 0.0489 (1.05) | 0.0510 (1.09) | 0.0520 (1.12) | 0.0630 (1.35) |
| Pooled | IPS | 0.0300 (0.97) | 0.0310 (1.00) | 0.0323 (1.04) | 0.0338 (1.09) | 0.0343 (1.10) | 0.0406 (1.31) |
| Pooled | SNIPS | 0.0298 (0.96) | 0.0310 (1.00) | 0.0324 (1.05) | 0.0335 (1.08) | 0.0342 (1.11) | 0.0408 (1.32) |

- On All, Women's and the pooled unit the interval of each ratio contains 1 at every length.
- On Men's the SNIPS interval contains 1 at every length. The IPS interval contains 1 at every length but 30 minutes, where its upper end is 0.9997; across the six lengths that upper end lies between 0.9997 and 1.0046.
- The standard deviation over the one at ten minutes ranges from 0.98 to 1.03 (IPS) and 0.98 to 1.01 (SNIPS) on Men's, 0.95 to 1.13 and 0.95 to 1.14 on All, 0.96 to 1.36 and 0.95 to 1.35 on Women's, and 0.97 to 1.31 and 0.96 to 1.32 on the pooled unit.
- On Men's no length is more than 3% from ten minutes. For 5 to 60 minutes the standard deviation of the IPS ratio is 0.054 to 0.055; Section 3 of the registration gives 0.052 to 0.054.
- On All, Women's and the pooled unit the standard deviation is smaller at 5 minutes than at ten and larger at every longer length: 0.95 to 0.97 of the one at ten minutes at 5 minutes, 1.07 to 1.12 at 60 minutes and 1.13 to 1.36 at 180 minutes. Each of these differs from ten minutes by more than the 2% fixed above; the smallest difference is 2.1% (All, IPS, 20 minutes). Between neighbouring lengths the step from 30 to 60 minutes is under 2% on All (IPS, 1.44%), All (SNIPS, 1.95%), the pooled unit (IPS, 1.34%), and by that rule those two lengths are not told apart there.
- The registration measured on Men's a width that does not depend on the block length. That is reproduced on Men's. It is not what the estimates on the confirmatory campaigns show, and whether their rise exceeds sampling error is not tested here.
- As fixed above, a rise points to dependence between rows, or to change over the week, that reaches beyond ten minutes, and the two are not separated. With longer blocks the intervals of the confirmatory units are wider than at ten minutes and still contain 1: the pooled IPS interval is 0.915 to 1.036 at ten minutes, 0.909 to 1.042 at 60 minutes and 0.897 to 1.056 at 180 minutes.
- Not fixed beforehand: a standard deviation estimated from `n` blocks has a sampling error of its own, roughly `1 / sqrt(2 (n - 1))` of its value under a normal approximation: 3.2% at 504 blocks, 3.9% at 336, 5.5% at 168 and 9.5% at 56. The estimates at different lengths come from the same rows, so these errors are not independent, and no interval is given for a ratio between lengths. On All the ratios from 5 to 60 minutes run from 0.95 to 1.07, on Women's from 0.95 to 1.12.
- The registered intervals and labels stand as registered.

## 5. The other registered intervals and the block length

The quantities, the random stream and the reading below were committed before this analysis was run; the commit that added them holds no result of it.

Section 4 varies the block length for the two ratios of H3 only. Two registered labels rest on intervals that end close to the value the rule compares them with: the pooled alignment label of H4, "raises the estimate", with a lower end of `d` at 0.002, and the SNIPS label of H6, "consistent", with half-widths of 0.097 (All) and 0.098 (Women's) against the bound of 0.10. Here the intervals behind the labels of H4, H5 and H6 are computed with the block lengths of Section 4.

- Quantities, as the registration defines them: `rho` and `d` of H4 at the width used (three hours on every campaign); the difference (iii) minus (ii) of H5; the IPS and SNIPS ratios of H6. `rho` and `d` are given for every campaign and for the pooled unit, `0.54 x (All) + 0.46 x (Women's)` within each replicate; H5 and H6 have no pooled unit.
- Blocks, replicates and multiplicities are those of Section 4, so a replicate at a given length draws the same blocks here as there. `pi0` and the width of H4 stay as fixed on the full data; counts, coverage, fallback, windows and the on-policy value are recomputed in every replicate. Intervals are 2.5th and 97.5th percentiles of the replicates in which a quantity is defined.
- The run stops if an interval at ten minutes differs from the registered one, or if the interval of the IPS ratio of H3, which enters `d`, differs at any length from the one in `results/blocks.json`.
- Reported for each unit, quantity and length: the interval, the standard deviation of the replicates and that standard deviation over the one at ten minutes; for H6 also the half-width of the interval.

How it is read:

- It is descriptive. The registered rules are defined for ten-minute blocks; at another length the report says where the interval lies and gives no label. The registered labels stand.
- Stated for each unit: the lengths at which the interval of `d` lies above 0, at which that of `rho` contains 1, at which that of the H5 difference lies above 0, and at which that of an H6 ratio contains 1 and has a half-width of at most 0.10.
- An end of a percentile interval of 10,000 replicates carries a Monte Carlo standard error of about 0.027 times the standard deviation of the replicates, and a half-width about 0.019 times (normal approximation). An end less than two such errors from the value it is compared with, or a half-width less than two of its errors from 0.10, is reported as at that value and counted on neither side.
- The standard deviations are read as in Section 4: lengths whose standard deviations differ by under 2% are not told apart, a rise with the length points to dependence between rows or to change over the week beyond ten minutes, and the two are not separated. At 180 minutes an interval rests on 56 resampling units.
- Twelve intervals per length are compared with a value on the confirmatory units, five on each campaign and two on the pooled unit, at five lengths besides the registered one, without any allowance for their number.

The numbers below come from one run of commit `c5eb6c5` (numpy 2.5.3), `python -m obd.posthoc.run lengths distances`, stored in `results/lengths.json`. Both checks passed, and no replicate left a quantity undefined.

`d` and `rho` of H4 at three hours:

| Unit | Quantity | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|
| Men's | `d` | -0.002 to 0.206 | -0.010 to 0.190 | -0.027 to 0.181 | -0.020 to 0.207 | -0.018 to 0.192 | -0.019 to 0.260 |
| Men's | `rho` | 0.862 to 1.122 | 0.853 to 1.114 | 0.842 to 1.099 | 0.848 to 1.120 | 0.840 to 1.117 | 0.833 to 1.177 |
| All | `d` | -0.016 to 0.184 | -0.019 to 0.182 | -0.025 to 0.192 | -0.023 to 0.199 | -0.025 to 0.186 | -0.005 to 0.165 |
| All | `rho` | 0.932 to 1.134 | 0.932 to 1.128 | 0.927 to 1.134 | 0.925 to 1.145 | 0.923 to 1.133 | 0.934 to 1.126 |
| Women's | `d` | -0.031 to 0.144 | -0.031 to 0.147 | -0.032 to 0.155 | -0.029 to 0.156 | -0.033 to 0.168 | -0.035 to 0.144 |
| Women's | `rho` | 0.975 to 1.151 | 0.974 to 1.158 | 0.969 to 1.168 | 0.967 to 1.175 | 0.960 to 1.190 | 0.959 to 1.180 |
| Pooled | `d` | 0.003 to 0.137 | 0.002 to 0.139 | 0.001 to 0.144 | 0.001 to 0.150 | 0.001 to 0.147 | 0.004 to 0.132 |
| Pooled | `rho` | 0.976 to 1.113 | 0.978 to 1.114 | 0.976 to 1.116 | 0.973 to 1.127 | 0.970 to 1.124 | 0.972 to 1.116 |

The difference (iii) minus (ii) of H5:

| Campaign | Quantity | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|
| Men's | (iii) minus (ii) | 0.075 to 0.210 | 0.072 to 0.218 | 0.066 to 0.224 | 0.054 to 0.245 | 0.010 to 0.304 | 0.039 to 0.221 |
| All | (iii) minus (ii) | 0.035 to 0.165 | 0.033 to 0.166 | 0.025 to 0.171 | 0.012 to 0.184 | -0.022 to 0.220 | 0.023 to 0.169 |
| Women's | (iii) minus (ii) | 0.025 to 0.129 | 0.022 to 0.130 | 0.015 to 0.138 | -0.001 to 0.153 | -0.039 to 0.196 | -0.005 to 0.140 |

The ratios of H6, and after the semicolon the half-width of the interval:

| Campaign | Ratio | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|
| Men's | IPS | 0.946 to 1.111; 0.0825 | 0.942 to 1.114; 0.0861 | 0.940 to 1.115; 0.0872 | 0.938 to 1.123; 0.0922 | 0.940 to 1.121; 0.0905 | 0.938 to 1.126; 0.0940 |
| Men's | SNIPS | 0.745 to 1.101; 0.1779 | 0.743 to 1.100; 0.1786 | 0.742 to 1.101; 0.1791 | 0.740 to 1.111; 0.1854 | 0.734 to 1.111; 0.1885 | 0.741 to 1.117; 0.1881 |
| All | IPS | 0.920 to 1.068; 0.0738 | 0.918 to 1.070; 0.0765 | 0.917 to 1.072; 0.0772 | 0.915 to 1.077; 0.0811 | 0.916 to 1.074; 0.0789 | 0.919 to 1.066; 0.0735 |
| All | SNIPS | 0.858 to 1.043; 0.0927 | 0.855 to 1.050; 0.0974 | 0.856 to 1.051; 0.0977 | 0.854 to 1.053; 0.0995 | 0.855 to 1.052; 0.0985 | 0.858 to 1.045; 0.0938 |
| Women's | IPS | 0.899 to 1.017; 0.0591 | 0.897 to 1.019; 0.0610 | 0.893 to 1.023; 0.0648 | 0.896 to 1.021; 0.0624 | 0.890 to 1.028; 0.0686 | 0.885 to 1.027; 0.0708 |
| Women's | SNIPS | 0.821 to 1.013; 0.0957 | 0.819 to 1.014; 0.0976 | 0.818 to 1.021; 0.1015 | 0.817 to 1.018; 0.1004 | 0.818 to 1.017; 0.0998 | 0.825 to 1.016; 0.0959 |

The ends that lie close to the value they are compared with, to four decimals, and after the semicolon their distance from it in Monte Carlo standard errors (positive: on the side of the registered label):

| Unit | Compared | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|
| Pooled | lower end of `d`, against 0 | 0.0031; 3.3 | 0.0020; 2.1 | 0.0014; 1.5 | 0.0015; 1.5 | 0.0011; 1.1 | 0.0040; 4.6 |
| All | lower end of (iii) minus (ii), against 0 | 0.0345; 38.8 | 0.0333; 36.6 | 0.0253; 25.8 | 0.0125; 10.8 | -0.0218; -13.4 | 0.0229; 23.3 |
| Women's | lower end of (iii) minus (ii), against 0 | 0.0248; 35.4 | 0.0220; 29.7 | 0.0147; 17.2 | -0.0012; -1.1 | -0.0392; -24.7 | -0.0048; -4.9 |
| All | half-width of H6 SNIPS, against 0.10 | 0.0927; 8.3 | 0.0974; 2.8 | 0.0977; 2.5 | 0.0995; 0.6 | 0.0985; 1.6 | 0.0938; 7.0 |
| Women's | half-width of H6 SNIPS, against 0.10 | 0.0957; 4.7 | 0.0976; 2.6 | 0.1015; -1.6 | 0.1004; -0.4 | 0.0998; 0.2 | 0.0959; 4.5 |

Standard deviation of the replicates, and in brackets over the one at ten minutes:

| Unit | Quantity | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|
| Men's | `d` | 0.0535 (1.04) | 0.0513 (1.00) | 0.0528 (1.03) | 0.0584 (1.14) | 0.0538 (1.05) | 0.0713 (1.39) |
| Men's | `rho` | 0.0661 (0.99) | 0.0668 (1.00) | 0.0663 (0.99) | 0.0701 (1.05) | 0.0714 (1.07) | 0.0881 (1.32) |
| Men's | H5 | 0.0345 (0.93) | 0.0371 (1.00) | 0.0404 (1.09) | 0.0487 (1.31) | 0.0750 (2.02) | 0.0469 (1.26) |
| Men's | H6 IPS | 0.0421 (0.96) | 0.0439 (1.00) | 0.0445 (1.01) | 0.0469 (1.07) | 0.0455 (1.04) | 0.0481 (1.10) |
| Men's | H6 SNIPS | 0.0951 (1.00) | 0.0949 (1.00) | 0.0951 (1.00) | 0.0979 (1.03) | 0.0992 (1.05) | 0.1002 (1.06) |
| All | `d` | 0.0508 (0.98) | 0.0517 (1.00) | 0.0558 (1.08) | 0.0569 (1.10) | 0.0532 (1.03) | 0.0436 (0.84) |
| All | `rho` | 0.0511 (1.02) | 0.0503 (1.00) | 0.0525 (1.04) | 0.0558 (1.11) | 0.0539 (1.07) | 0.0486 (0.97) |
| All | H5 | 0.0333 (0.98) | 0.0341 (1.00) | 0.0367 (1.08) | 0.0432 (1.27) | 0.0611 (1.79) | 0.0368 (1.08) |
| All | H6 IPS | 0.0377 (0.96) | 0.0392 (1.00) | 0.0393 (1.00) | 0.0412 (1.05) | 0.0401 (1.02) | 0.0377 (0.96) |
| All | H6 SNIPS | 0.0470 (0.95) | 0.0494 (1.00) | 0.0497 (1.00) | 0.0509 (1.03) | 0.0502 (1.02) | 0.0480 (0.97) |
| Women's | `d` | 0.0447 (0.98) | 0.0455 (1.00) | 0.0479 (1.05) | 0.0473 (1.04) | 0.0519 (1.14) | 0.0456 (1.00) |
| Women's | `rho` | 0.0453 (0.96) | 0.0471 (1.00) | 0.0503 (1.07) | 0.0530 (1.13) | 0.0584 (1.24) | 0.0559 (1.19) |
| Women's | H5 | 0.0262 (0.94) | 0.0278 (1.00) | 0.0319 (1.15) | 0.0391 (1.41) | 0.0594 (2.14) | 0.0369 (1.33) |
| Women's | H6 IPS | 0.0303 (0.97) | 0.0312 (1.00) | 0.0335 (1.07) | 0.0319 (1.02) | 0.0351 (1.12) | 0.0366 (1.17) |
| Women's | H6 SNIPS | 0.0490 (0.97) | 0.0504 (1.00) | 0.0515 (1.02) | 0.0511 (1.01) | 0.0508 (1.01) | 0.0493 (0.98) |
| Pooled | `d` | 0.0343 (0.98) | 0.0349 (1.00) | 0.0367 (1.05) | 0.0380 (1.09) | 0.0370 (1.06) | 0.0330 (0.95) |
| Pooled | `rho` | 0.0348 (1.00) | 0.0348 (1.00) | 0.0359 (1.03) | 0.0387 (1.11) | 0.0394 (1.13) | 0.0365 (1.05) |

- `rho`: the interval contains 1 in every unit at every length.
- `d` on the campaigns: the interval contains 0 on All and on Women's at every length. On Men's it contains 0 at every length but 5 minutes, where its lower end, -0.0025, is at 0.
- `d` on the pooled unit: the lower end lies between 0.0011 and 0.0040 at the six lengths. It lies above 0 at 5, 10 and 180 minutes, by 3.3, 2.1 and 4.6 errors, and at 0 at 20, 30 and 60 minutes (1.5, 1.5 and 1.1 errors). At no length does the interval reach below 0.
- H5: on All the interval lies above 0 at every length but 60 minutes, where it is -0.022 to 0.220. On Women's it lies above 0 at 5, 10 and 20 minutes; at 30 minutes its lower end, -0.0012, is at 0; at 60 and 180 minutes it contains 0 (-0.039 to 0.196 and -0.005 to 0.140). On Men's it lies above 0 at every length.
- H6, IPS: on All and Women's the interval contains 1 at every length and its half-width is 0.059 to 0.081.
- H6, SNIPS: on All and Women's the interval contains 1 at every length. Its half-width is 0.0927 to 0.1015. It is below 0.10 at 5, 10 and 180 minutes on both campaigns and at 20 minutes on All. It is at 0.10 at 30 and 60 minutes on All and at 20, 30 and 60 minutes on Women's; at 20 and 30 minutes on Women's the number itself is above 0.10 (0.1015 and 0.1004). On Men's, where the registered label is "undetermined", the half-width is 0.178 to 0.189.
- Standard deviation over the one at ten minutes: 1.00 to 1.13 for `rho` and 0.95 to 1.09 for `d` on the pooled unit; 0.97 to 1.11 and 0.84 to 1.10 on All; 0.96 to 1.24 and 0.98 to 1.14 on Women's. For the H6 ratios it is 0.95 to 1.05 on All and 0.97 to 1.17 on Women's. As fixed above, the rises are not attributed.
- For the H5 difference the standard deviation is largest at 60 minutes on every campaign, 1.79 (All), 2.14 (Women's) and 2.02 (Men's) times the one at ten minutes, and smaller again at 180 minutes (1.08, 1.33, 1.26).
- Not fixed beforehand: the reading above did not foresee that a block length can interfere with the construction of an estimate. H5 takes its target from the clock hour before and the clock hour after a row and uses only rows that have both. A clock hour is missing from a replicate with probability 0.0024 at ten minutes and 0.05, 0.13 and 0.37 at 20, 30 and 60 minutes, and with 60-minute blocks a replicate holds both neighbours of a given hour with probability 0.40. These figures follow from the multinomial draw and from no data. From 20 to 60 minutes the H5 intervals therefore rest on fewer and fewer rows, and their widening is not read as a sign of dependence. At 180 minutes a block is three hours, so that two of its three hours have a neighbour in another block, and it is one period of H4. How many rows the replicates leave out was not recorded.
- The two registered labels named at the start of this section rest on ends that stay close to their thresholds at every length: the pooled lower end of `d` between 0.0011 and 0.0040, the SNIPS half-width between 0.0927 and 0.1015 against 0.10. At some of the lengths from 20 to 60 minutes each is within simulation error of its threshold.
- The registered intervals and labels stand as registered.

## 6. Three distances that read no click

The quantities and the reading below were committed before this analysis was run; the commit that added them holds no result of it.

H1 finds the published prior "inconsistent" with the hourly frequencies of the BTS log: `D` is 0.526 (All) and 0.527 (Women's) against a noise floor `D0` of 0.136 and 0.115. The label does not say whether the log shows one fixed distribution that is not the prior's, or a distribution that changed during the week. Three further distances are computed from the item, position and timestamp columns of the BTS log and from `pi0`. TV, `f_h`, `N_B` and the weights are those of H1; `f(a|k) = N_B(a,k)/N_B(k)` are the frequencies of the whole week.

- `A`, the prior against the whole week: `sum over k of [N_B(k)/N_B] x TV(f(.|k), pi0(.|k))`. Its reference, since a distance is positive by construction: the same sum between the whole-week frequencies of the rows in the first, third and fifth ten-minute block of every hour and those of the other rows.
- `E`, the hours against the whole week: `sum over (h, k) of [N_B(h,k)/N_B] x TV(f_h(.|k), f(.|k))`, over the `(h, k)` that enter `D`.
- The first hour of the week, by position: the registered distance `TV(f_0(.|k), pi0(.|k))` and its own floor, the distance between the frequencies of the rows of that hour in its first, third and fifth block and in its other blocks, with the number of rows.
- `D` and `D0` are recomputed, and the run stops if they differ from the registered values.
- The same quantities for the random log with the uniform distribution in place of `pi0`: a case in which the policy is fixed and known.

Two relations hold by construction when no `(h, k)` is left out. `A <= D`, because the whole-week frequencies are the row-weighted mean of the hourly ones and TV is convex. `D <= A + E`, by the triangle inequality.

How it is read:

- It is descriptive and gives no verdict. No interval is computed, as for `D` and `D0` in the registration. The registered label of H1 stands.
- The noise reference is `D0`. If the policy is fixed within an hour and the two halves of the hour are independent, the expected distance between an hour's frequencies and the distribution of its policy is at most the expected distance between the halves, and about half of it when counts are large. In the registered results the random log, whose policy is fixed and uniform, has a `D` of 0.53 to 0.55 times its `D0`.
- If the BTS log showed one fixed distribution all week, `E` would hold noise only, and `D - A` would be at most that noise. `E` and `D - A` are therefore set against the two thresholds of the registered rule of H1: at most `D0`, "not distinguishable from variation within the hour"; above `2 x D0` and above 0.10, more than the rule asks for a difference; otherwise between the two, and nothing is said.
- What is stated from the numbers: `A` with its reference; on which side of the two thresholds `E` falls, which says whether the distribution shown changed between hours; on which side `D - A` falls, which says whether that change adds to the distance from the prior beyond what the whole week's distribution already holds; and for each position of the first hour, on which side of its floor and of twice its floor the distance falls. The first hour is one hour and its floor one split.
- TV distances do not add. `A` and `E` bound `D` from both sides; they do not divide it into a part due to a fixed difference and a part due to change. If `E` lies above the upper threshold and `D - A` does not, that is what is reported, and the question how much of `D` is change stays open.
- The distances describe what the log shows. A distribution that changes between hours can come from updated parameters or from servers that hold different versions of them (Section 8 of the registration), and change within an hour is part of `D0`, not of `E`.

The numbers below come from the same run (`results/distances.json`). `D`, `D0` and the first-hour distances reproduce the registered values, and no `(h, k)` is left out.

| Campaign | Log | `D` | `D0` | `A` | Reference of `A` | `E` | `D - A` | `E` over `D0` | `D - A` over `D0` |
|---|---|---|---|---|---|---|---|---|---|
| Men's | BTS | 0.437 | 0.109 | 0.310 | 0.010 | 0.335 | 0.127 | 3.06 | 1.16 |
| Men's | random | 0.202 | 0.366 | 0.018 | 0.029 | 0.202 | 0.185 | 0.55 | 0.50 |
| All | BTS | 0.526 | 0.136 | 0.386 | 0.012 | 0.410 | 0.141 | 3.01 | 1.03 |
| All | random | 0.186 | 0.354 | 0.016 | 0.028 | 0.185 | 0.170 | 0.52 | 0.48 |
| Women's | BTS | 0.527 | 0.115 | 0.413 | 0.010 | 0.394 | 0.115 | 3.44 | 1.00 |
| Women's | random | 0.172 | 0.325 | 0.013 | 0.027 | 0.172 | 0.160 | 0.53 | 0.49 |

The first hour of the week:

| Campaign | Log | Position | Rows | Distance | Floor | Distance over floor |
|---|---|---|---|---|---|---|
| Men's | BTS | 1 | 8,473 | 0.149 | 0.123 | 1.21 |
| Men's | BTS | 2 | 8,480 | 0.096 | 0.107 | 0.89 |
| Men's | BTS | 3 | 8,480 | 0.067 | 0.102 | 0.66 |
| Men's | random | 1 | 961 | 0.174 | 0.313 | 0.56 |
| Men's | random | 2 | 963 | 0.214 | 0.356 | 0.60 |
| Men's | random | 3 | 964 | 0.195 | 0.350 | 0.56 |
| All | BTS | 1 | 25,432 | 0.180 | 0.138 | 1.30 |
| All | BTS | 2 | 25,438 | 0.126 | 0.153 | 0.83 |
| All | BTS | 3 | 25,445 | 0.088 | 0.150 | 0.59 |
| All | random | 1 | 2,822 | 0.166 | 0.345 | 0.48 |
| All | random | 2 | 2,828 | 0.165 | 0.434 | 0.38 |
| All | random | 3 | 2,822 | 0.191 | 0.373 | 0.51 |
| Women's | BTS | 1 | 16,059 | 0.164 | 0.116 | 1.42 |
| Women's | BTS | 2 | 16,065 | 0.098 | 0.118 | 0.83 |
| Women's | BTS | 3 | 16,060 | 0.105 | 0.099 | 1.06 |
| Women's | random | 1 | 1,778 | 0.165 | 0.275 | 0.60 |
| Women's | random | 2 | 1,774 | 0.194 | 0.262 | 0.74 |
| Women's | random | 3 | 1,774 | 0.158 | 0.331 | 0.48 |

- `A` is 0.386 on All and 0.413 on Women's, against references of 0.012 and 0.010: the frequencies of the whole week are not those of the prior. On Men's `A` is 0.310 against 0.010.
- `E` is 0.410 on All and 0.394 on Women's, 3.0 and 3.4 times `D0`. On both it lies above `2 x D0` and above 0.10, the upper threshold: the distribution that the BTS log shows changed between hours. On Men's `E` is 0.335, 3.1 times `D0`.
- `D - A` is 0.141 on All, 0.115 on Women's and 0.127 on Men's. On each campaign it lies between `D0` and `2 x D0` (on Women's it exceeds `D0` by 0.0001), so nothing is said on whether the change between hours adds to the distance from the prior beyond what the whole week's frequencies already hold.
- `A` and `E` are 0.73 and 0.78 of `D` on All and 0.78 and 0.75 on Women's. As fixed above, they bound `D` and do not divide it: how much of `D` is a difference that holds all week and how much is change between hours stays open.
- The random log, whose policy is fixed and uniform: `E` is 0.52 to 0.55 of `D0` and `D - A` 0.48 to 0.50 of it, both under the lower threshold, and `A` (0.013 to 0.018) is below its reference (0.027 to 0.029).
- The first hour, BTS log. At position 1 the distance from the prior lies between the floor and twice the floor on every campaign (1.30, 1.42 and 1.21 times the floor on All, Women's and Men's). At position 2 it is at most the floor on every campaign (0.83, 0.83, 0.89). At position 3 it is at most the floor on All and Men's (0.59, 0.66) and between on Women's (1.06). In no cell does it exceed twice the floor. In the random log the first-hour distance from the uniform distribution is 0.38 to 0.74 of its floor.
- The first hour is closer to the prior than the frequencies of the whole week are (`A`). At five of the nine positions its distance is at most its floor, the threshold under which the registered rule says "not distinguishable from variation within the hour"; at the other four it lies between the two thresholds. This is not a finding that the prior was in force in that hour: it is one hour with one split, and its floor contains whatever change the policy made within the hour.
- The registered label of H1 stands. What these distances add: "inconsistent" covers a whole-week distribution that is not the prior's and a distribution that changed from hour to hour, and the size of each part of `D` is not determined.

## Code

| File | Content |
|---|---|
| `units.py` | impressions, resampling by unit, list reuse, the variance ratio |
| `features.py` | values that occur in one log only, the pairing, H7 from the registered code |
| `propensities.py` | `S` by cell, `M` by bound and by day, the grid bias, low hours |
| `blocks.py` | the ratios of H3 by block length |
| `lengths.py` | `rho`, `d`, the H5 difference and the H6 ratios by block length |
| `distances.py` | the prior, the whole week and the hours of a log |
| `run.py` | the analyses on the full data, result files |

The tests in `tests/` use hand-built and synthetic logs only.
