# Extension of the coverage study: results

The extension of [`obd_coverage`](../../README.md) registered in [`EXTENSION.md`](../../EXTENSION.md) (`af7e615`), which was committed before any of its code. It measures the dependence of the real clicks directly, fits a scenario to those measurements, sets dependence beyond ten minutes against a drift that the two logs do not share, and varies three choices of the registered scenarios.

- `calibration.json`: the direct measurements on the real clicks, every parameter, the true values and the predicted coverage of every cell, committed before any click was generated (`2e4eee4`, from code `c7609da`).
- `coverage.json`: every cell, the fit of F, the block residuals of every scenario and the registered reading; `cells.md`: one line per cell, and the cells whose prediction missed; `residuals.md`: D3 by block length.
- `posthoc.json`: written after the reading, descriptive and no part of the registration: the sessions that the rule of Section 3 forms at every size and span, and the impression with the most double clicks of each log.

The direct measurements read real clicks. With respect to `obd` they are post hoc and descriptive, and nothing here is a verdict on it. No registered file, result or label of `obd` or of the coverage study changes.

The three results of the coverage study that the extension tests, on the IPS ratio on All and Women's: R1, in M rows and impressions under-cover; R2, in M every block length from 5 to 180 minutes is adequate; R3, in H ten-minute blocks under-cover. Labels, band and units are those of the coverage study; each cell rests on 4,000 data sets.

## In brief

- R1, R2 and R3 are robust by the registered criterion: every label is the registered one in every variant on both campaigns.
- In F, the scenario fitted to the direct measurements, every block length is adequate on both campaigns (R2). Rows and impressions under-cover on All, at 0.905 and 0.910 against 0.866 and 0.880 in M. On Women's they are unresolved, at 0.922 and 0.928 against 0.846 and 0.860 in M: R1 has another label there, which the registration counts against it.
- F is not a close description of the logs. It reproduces 16 of 25 statistics on All and 11 on Women's, and on no campaign the published ratio of ten-minute blocks to rows (1.37, 1.45 and 1.47, against 97.5th percentiles of 1.26, 1.21 and 1.26 in F). Its coverage with rows is that of a scenario whose intervals widen less from rows to blocks than those of the logs, and whose sessions in the random logs hold 1.5 to 2.0 impressions on average.
- With dependence across an hour built on F (FH), ten-minute blocks under-cover: 0.914 on All and 0.830 on Women's (R3).
- Dependence beyond ten minutes and a drift that the logs do not share are not separated on either campaign: the real `G(180)`, 0.199 on All and 0.315 on Women's, lies inside both registered ranges. On Women's this label rests on one scenario: the real value lies above the 97.5th percentile of FH (0.311) and of FD (0.310) and below that of FU (0.342), which was cut back; with FH and FD alone the label would have been "more like a drift". The two scenarios that match the widening on Women's imply different things for its ten-minute blocks, a coverage of 0.830 with dependence across an hour (FH) and of 0.960 with a drift in the BTS log (FS), and the extension does not say which holds.
- By D3 the groupings of the registered M and H, on which R1 to R3 rest, differ from the logs: their sessions join clicks of different user types, and the real `G` at ten minutes, 0.079 on All and -0.010 on Women's, lies below its range in each of their six variants (2.5th percentiles of 0.150 and above). `G` was not computed for M and H themselves; the two variants with the two-level factor have their groupings and strengths.

## Direct measurements on the real clicks

D1, double clicks. `N2` is the number of pairs of clicked rows in one impression, `E0` the number expected from the click rates by item and position, `e_I^ = N2 / E0 - 1`. The interval is over resamples of the 1,008 ten-minute blocks.

| Campaign | Log | `N2` | `E0` | `e_I^` (95% interval) | registered `e_I` |
|---|---|---|---|---|---|
| All | random | 306 | 21.2 | 13.4 (9.9 to 17.3) | 40.9 |
| All | bts | 5530 | 480.5 | 10.5 (9.4 to 12.0) | 40.9 |
| Women's | random | 270 | 22.4 | 11.1 (7.9 to 14.6) | 24.7 |
| Women's | bts | 4041 | 392.1 | 9.3 (8.3 to 10.3) | 24.7 |
| Men's | random | 274 | 13.7 | 19.1 (12.8 to 26.6) | 16.2 |
| Men's | bts | 4730 | 246.4 | 18.2 (10.9 to 29.2) | 16.2 |

The registered `e_I`, one per campaign, was solved from the published ratio of standard deviations between impressions and rows. On All and Women's it is 2.2 to 3.9 times the measured excess and lies above the interval of either log; on Men's it lies inside both. In the BTS log of Men's one impression of 50 rows with 48 clicks gives 1,128 of the 4,730 pairs (24%), and without it `e_I^` is 13.6; in the other five logs the largest impression gives at most 3.6% of the pairs (`posthoc.json`, not registered):

| Campaign | Log | rows | clicks | pairs | share of `N2` | `e_I^` | without it |
|---|---|---|---|---|---|---|---|
| All | random | 10 | 4 | 6 | 2.0% | 13.4 | 13.1 |
| All | bts | 12 | 11 | 55 | 1.0% | 10.5 | 10.4 |
| Women's | random | 6 | 4 | 6 | 2.2% | 11.1 | 10.8 |
| Women's | bts | 10 | 8 | 28 | 0.7% | 9.3 | 9.2 |
| Men's | random | 7 | 5 | 10 | 3.6% | 19.1 | 18.3 |
| Men's | bts | 50 | 48 | 1128 | 23.8% | 18.2 | 13.6 |

D2, the variance ratio of `obd.posthoc.units` by block length, with intervals over resamples of the pairs of adjacent blocks:

| Campaign | Log | 1 min | 2 min | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|---|
| All | random | 1.29 (1.11 to 1.50) | 1.25 (1.10 to 1.44) | 1.50 (1.28 to 1.69) | 1.89 (1.52 to 2.28) | 1.82 (1.44 to 2.20) | 2.46 (1.65 to 3.35) | 2.10 (1.25 to 2.91) | 1.94 (0.92 to 3.05) |
| All | bts | 1.14 (1.07 to 1.21) | 1.36 (1.25 to 1.47) | 1.59 (1.42 to 1.78) | 1.85 (1.45 to 2.38) | 1.97 (1.60 to 2.38) | 2.35 (1.79 to 2.99) | 2.61 (1.81 to 3.54) | 5.03 (2.03 to 9.80) |
| Women's | random | 1.13 (1.04 to 1.24) | 1.24 (1.09 to 1.42) | 1.69 (1.37 to 2.04) | 1.92 (1.54 to 2.32) | 1.69 (1.31 to 2.13) | 2.06 (1.52 to 2.65) | 2.07 (1.41 to 2.78) | 2.95 (2.07 to 3.95) |
| Women's | bts | 1.16 (1.05 to 1.27) | 1.52 (1.21 to 1.91) | 1.62 (1.37 to 1.87) | 2.23 (1.79 to 2.71) | 2.52 (1.77 to 3.40) | 2.88 (1.65 to 4.80) | 3.33 (1.79 to 5.05) | 3.56 (2.12 to 5.77) |
| Men's | random | 1.18 (1.08 to 1.28) | 1.43 (1.17 to 1.81) | 2.00 (1.42 to 2.88) | 2.45 (1.60 to 3.45) | 2.14 (1.41 to 2.99) | 2.14 (1.44 to 2.87) | 2.07 (1.33 to 2.87) | 1.68 (0.91 to 2.70) |
| Men's | bts | 1.20 (1.11 to 1.29) | 1.30 (1.20 to 1.43) | 1.70 (1.54 to 1.88) | 2.08 (1.80 to 2.38) | 2.17 (1.75 to 2.53) | 2.02 (1.55 to 2.67) | 2.02 (1.47 to 2.78) | 4.24 (2.09 to 6.81) |

At 1, 10 and 60 minutes the values are the published ones. The lower end of every interval is above 1, except at 180 minutes in the random logs of All and Men's. In the BTS logs of All and Women's the ratio rises at every step of the block length, from 1.14 to 5.03 and from 1.16 to 3.56; on Men's it is 2.0 to 2.2 from 10 to 60 minutes and 4.24 at 180. In the random logs it is 1.7 to 2.5 from 10 to 60 minutes. At 180 minutes a log has 28 pairs of blocks and the intervals are wide.

D3, block residuals by log and user type. `V(L)` is the sum over blocks of the squared residual of the ratio, `W(L)` the sum over blocks, logs and user types of the squared residuals by type, `G(L) = 1 - W(L) / V(L)`; "between the logs" is the correlation of the two logs' block residuals.

| Campaign | Block, minutes | V(L) / V(10) | W(L) / W(10) | G | G within the random log | G within the BTS log | between the logs |
|---|---|---|---|---|---|---|---|
| All | 5 | 0.917 | 0.961 | 0.035 | 0.046 | 0.174 | 0.049 |
| All | 10 | 1.000 | 1.000 | 0.079 | 0.094 | 0.267 | 0.064 |
| All | 20 | 1.049 | 1.087 | 0.045 | 0.077 | 0.381 | 0.121 |
| All | 30 | 1.081 | 1.065 | 0.093 | 0.122 | 0.453 | 0.119 |
| All | 60 | 1.157 | 1.068 | 0.150 | 0.173 | 0.582 | 0.117 |
| All | 180 | 1.277 | 1.112 | 0.199 | 0.268 | 0.715 | 0.243 |
| Women's | 5 | 0.965 | 0.943 | 0.012 | 0.012 | 0.190 | 0.016 |
| Women's | 10 | 1.000 | 1.000 | -0.010 | -0.013 | 0.271 | 0.018 |
| Women's | 20 | 1.125 | 1.087 | 0.024 | 0.017 | 0.387 | 0.020 |
| Women's | 30 | 1.213 | 1.108 | 0.077 | 0.057 | 0.456 | -0.008 |
| Women's | 60 | 1.235 | 1.107 | 0.095 | 0.069 | 0.600 | 0.009 |
| Women's | 180 | 1.724 | 1.169 | 0.315 | 0.267 | 0.740 | -0.033 |
| Men's | 5 | 0.945 | 0.946 | -0.011 | -0.013 | 0.048 | -0.000 |
| Men's | 10 | 1.000 | 1.000 | -0.010 | -0.007 | 0.122 | 0.021 |
| Men's | 20 | 0.956 | 1.023 | -0.081 | -0.044 | 0.182 | 0.108 |
| Men's | 30 | 0.972 | 1.046 | -0.087 | -0.032 | 0.267 | 0.152 |
| Men's | 60 | 1.009 | 1.092 | -0.093 | 0.065 | 0.298 | 0.359 |
| Men's | 180 | 0.992 | 1.174 | -0.196 | 0.077 | 0.605 | 0.491 |

From ten to 180 minutes `V` grows by 28% on All and by 72% on Women's while `W` grows by 11% and 17%, so `G(180)` is 0.199 and 0.315. On Men's `V` does not grow, the residuals of the two logs are correlated at 0.49 and `G(180)` is -0.196. Within the BTS log `G(180)` is 0.605 to 0.740 over the campaigns; within one log `G` also rises with a movement that both logs share (Section 2 of the registration).

## The scenarios

F and the scenarios built on it. The nominal size is the number of impressions that the rule of Section 3 aims at for a session, `T` its span in minutes; a value in brackets was solved and cut back by the nesting, as registered.

| Campaign | Scenario | random: nominal size | `T` | `e_I` | `e_S` | bts: nominal size | `T` | `e_I` | `e_S` | sessions per long group | `e_L` | `k` of `k_max` | true IPS ratio | largest probability |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| All | F | 44 | 1 | 13.4 | 13.4 (solved 24.8) | 22 | 2 | 10.5 | 5.7 |  |  |  | 0.9907 | 0.090 |
| All | FH | 44 | 1 | 13.4 | 13.4 (solved 24.8) | 22 | 2 | 10.5 | 5.7 | 6 | 4.2 |  | 0.9907 | 0.090 |
| All | FU | 44 | 1 | 13.4 | 13.4 (solved 24.8) | 22 | 2 | 10.5 | 5.7 | 24 | 5.7 (solved 6.6) |  | 0.9907 | 0.090 |
| All | FS | 44 | 1 | 13.4 | 13.4 (solved 24.8) | 22 | 2 | 10.5 | 5.7 |  |  | 1.66 of 5.42 | 0.9907 | 0.098 |
| All | S |  |  |  |  |  |  |  |  |  |  | 1.42 of 5.42 | 0.9907 | 0.008 |
| All | FD | 44 | 1 | 13.4 | 13.4 (solved 24.8) | 22 | 2 | 10.5 | 5.7 |  |  | as D | 0.9895 | 0.109 |
| Women's | F | 44 | 1 | 11.1 | 11.1 (solved 58.7) | 22 | 2 | 9.3 | 7.3 |  |  |  | 1.0017 | 0.092 |
| Women's | FH | 44 | 1 | 11.1 | 11.1 (solved 58.7) | 22 | 2 | 9.3 | 7.3 | 12 | 7.1 |  | 1.0017 | 0.092 |
| Women's | FU | 44 | 1 | 11.1 | 11.1 (solved 58.7) | 22 | 2 | 9.3 | 7.3 | 24 | 7.3 (solved 23.3) |  | 1.0017 | 0.092 |
| Women's | FS | 44 | 1 | 11.1 | 11.1 (solved 58.7) | 22 | 2 | 9.3 | 7.3 |  |  | 2.65 of 4.41 | 1.0017 | 0.157 |
| Women's | S |  |  |  |  |  |  |  |  |  |  | 2.39 of 4.41 | 1.0017 | 0.014 |
| Women's | FD | 44 | 1 | 11.1 | 11.1 (solved 58.7) | 22 | 2 | 9.3 | 7.3 |  |  | as D | 1.0000 | 0.124 |
| Men's | F | 44 | 1 | 19.1 | 19.1 (solved 119.7) | 11 | 2 | 18.2 | 14.3 |  |  |  | 0.9215 | 0.173 |
| Men's | FH | 44 | 1 | 19.1 | 19.1 (solved 119.7) | 11 | 2 | 18.2 | 14.3 | 3 | 2.1 |  | 0.9215 | 0.173 |
| Men's | FU | 44 | 1 | 19.1 | 19.1 (solved 119.7) | 11 | 2 | 18.2 | 14.3 | 6 | 6.9 |  | 0.9215 | 0.173 |
| Men's | FS | 44 | 1 | 19.1 | 19.1 (solved 119.7) | 11 | 2 | 18.2 | 14.3 |  |  | 0.47 of 4.22 | 0.9215 | 0.193 |
| Men's | S |  |  |  |  |  |  |  |  |  |  | 0.42 of 4.22 | 0.9215 | 0.010 |
| Men's | FD | 44 | 1 | 19.1 | 19.1 (solved 119.7) | 11 | 2 | 18.2 | 14.3 |  |  | as D | 0.9190 | 0.230 |

- F. In the random log of every campaign the solved `e_S` exceeds `e_I` at every nominal size, at the span that the one-minute ratio chooses, so 44 is used and `e_S` is cut back to `e_I`. In the BTS logs nothing is cut back.
- FH and FU match the published widening at 180 minutes (1.134, 1.365, 1.029) with long groups of 60 minutes and of 24 hours within a user type. FH is not cut back. FU is cut back on All and Women's with 24 sessions to a long group, and is weaker there than the number it was solved from.
- FS and S match the same number with a drift in the BTS log only, of the shape fitted in the coverage study, FS on top of F and S with independent clicks. The amplitude stays below `k_max` on every campaign.
- FD is F with the drift of scenario D in both logs.

The sessions of F (`posthoc.json`, not registered). "Seen from an impression" is the mean size of the session that an impression is in; the last column is the smallest `e_S` that any size and span solves to.

| Campaign | Log | nominal size | `T` | impressions per session | as seen from an impression | `e_I` | solved `e_S` | one-minute ratio: fitted | real | smallest solved `e_S` (where, its one-minute ratio) |
|---|---|---|---|---|---|---|---|---|---|---|
| All | random | 44 | 1 | 2.03 | 6.4 | 13.4 | 24.8 | 1.38 | 1.29 | 5.3 (size 44, 5 min, 1.02) |
| All | bts | 22 | 2 | 6.81 | 20.9 | 10.5 | 5.7 | 1.13 | 1.14 | 3.2 (size 44, 2 min, 1.17) |
| Women's | random | 44 | 1 | 1.77 | 3.5 | 11.1 | 58.7 | 1.07 | 1.13 | 16.7 (size 22, 5 min, 1.02) |
| Women's | bts | 22 | 2 | 6.80 | 22.8 | 9.3 | 7.3 | 1.19 | 1.16 | 4.3 (size 44, 5 min, 1.04) |
| Men's | random | 44 | 1 | 1.50 | 2.7 | 19.1 | 119.7 | 1.15 | 1.18 | 35.2 (size 22, 5 min, 1.04) |
| Men's | bts | 11 | 2 | 3.78 | 9.6 | 18.2 | 14.3 | 1.17 | 1.20 | 4.6 (size 44, 2 min, 1.34) |

A user type gets at least one label, and in the random logs nearly every type has only one at a span of one minute. The ladder of sizes therefore does not enlarge the sessions there: at one minute the number of sessions and the solved `e_S` are the same at all four nominal sizes on Women's and Men's, and at 11, 22 and 44 on All. The sessions of F hold 2.0, 1.8 and 1.5 impressions on average in the random logs of All, Women's and Men's, and 6.8, 6.8 and 3.8 in the BTS logs. The rule tests the solved `e_S` at the span that the one-minute ratio chooses. Over all sizes and spans, no combination solves to an `e_S` at or below `e_I` in the random log of Women's or Men's (smallest 16.7 against 11.1, and 35.2 against 19.1). On All five do, the nominal sizes 22 and 44 at two minutes (12.5 against 13.4) and 44 at three, five and ten minutes, with one-minute ratios of 1.01 to 1.08 against the real 1.29.

The variants of Section 5, beside the registered M and H:

| Campaign | Scenario | `T` random | `e_S` random | `T` BTS | `e_S` BTS | `e_L` | largest probability |
|---|---|---|---|---|---|---|---|
| All | M | 1 | 33.6 | 2 | 25.5 |  |  |
| All | M.half-sessions | 1 | 40.9 (solved 62.5) | 2 | 40.9 (solved 50.9) |  | 0.260 |
| All | M.double-sessions | 2 | 18.0 | 2 | 12.7 |  | 0.260 |
| All | M.two-level | 1 | 33.6 | 2 | 25.5 |  | 0.698 |
| All | H | 1 | 33.6 | 2 | 25.5 | 13.7 |  |
| All | H.half-long | 1 | 33.6 | 2 | 25.5 | 25.5 (solved 27.6) | 0.260 |
| All | H.double-long | 1 | 33.6 | 2 | 25.5 | 6.9 | 0.260 |
| All | H.two-level | 1 | 33.6 | 2 | 25.5 | 13.7 | 0.994 |
| Women's | M | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) |  |  |
| Women's | M.half-sessions | 2 | 24.7 (solved 50.9) | 2 | 24.7 (solved 56.4) |  | 0.196 |
| Women's | M.double-sessions | 2 | 12.7 | 2 | 14.0 |  | 0.196 |
| Women's | M.two-level | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) |  | 0.383 |
| Women's | H | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) | 24.7 (solved 29.6) |  |
| Women's | H.half-long | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) | 24.7 (solved 58.4) | 0.196 |
| Women's | H.double-long | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) | 15.0 | 0.196 |
| Women's | H.two-level | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) | 24.7 (solved 29.6) | 0.383 |
| Men's | M | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) |  |  |
| Men's | M.half-sessions | 1 | 16.2 (solved 58.3) | 1 | 16.2 (solved 36.8) |  | 0.148 |
| Men's | M.double-sessions | 3 | 16.2 (solved 17.2) | 2 | 9.7 |  | 0.148 |
| Men's | M.two-level | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) |  | 0.287 |
| Men's | H | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) | 0.5 |  |
| Men's | H.half-long | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) | 1.0 | 0.148 |
| Men's | H.double-long | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) | 0.3 | 0.148 |
| Men's | H.two-level | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) | 0.5 | 0.379 |

With half sessions `e_S` is cut back to `e_I` in both logs of every campaign, and with half long groups `e_L` is cut back on All and Women's; these variants are weaker than the published numbers they were solved from. The two-level variants keep the strengths of the registration. The largest click probability of any scenario is 0.994 (All, H with the two-level factor), below the stop of the registration.

## What F reproduces

Each statistic of the real logs beside its 2.5th to 97.5th percentile over the data sets of F: D1 and D2 on the first 400 data sets, the ratios of standard deviations of the replicates of the IPS ratio on all 4,000. "Solved from" marks what F was solved from.

| Statistic | Solved from | All | Women's | Men's |
|---|---|---|---|---|
| excess within an impression, random | yes | 13.423 (11.631 to 15.262) | 11.075 (9.598 to 12.865) | 19.067 (16.575 to 22.220) |
| variance ratio at 1 minutes, random | yes | 1.290 (1.288 to 1.527) | 1.134 (1.010 to 1.171) | 1.176 (1.082 to 1.250) |
| variance ratio at 2 minutes, random |  | 1.253 (1.339 to 1.562) **no** | 1.239 (1.039 to 1.228) **no** | 1.430 (1.079 to 1.314) **no** |
| variance ratio at 5 minutes, random |  | 1.498 (1.321 to 1.639) | 1.687 (1.042 to 1.297) **no** | 2.000 (1.075 to 1.390) **no** |
| variance ratio at 10 minutes, random | yes | 1.895 (1.250 to 1.719) **no** | 1.918 (1.000 to 1.376) **no** | 2.449 (1.059 to 1.431) **no** |
| variance ratio at 20 minutes, random |  | 1.823 (1.216 to 1.812) **no** | 1.690 (0.917 to 1.451) **no** | 2.139 (0.982 to 1.478) **no** |
| variance ratio at 30 minutes, random |  | 2.459 (1.165 to 1.893) **no** | 2.062 (0.859 to 1.542) **no** | 2.138 (0.918 to 1.554) **no** |
| variance ratio at 60 minutes, random |  | 2.104 (1.037 to 2.054) **no** | 2.067 (0.800 to 1.684) **no** | 2.068 (0.864 to 1.667) **no** |
| variance ratio at 180 minutes, random |  | 1.939 (0.822 to 2.526) | 2.952 (0.609 to 2.034) **no** | 1.679 (0.711 to 2.064) |
| excess within an impression, bts | yes | 10.510 (10.085 to 10.897) | 9.307 (8.904 to 9.756) | 18.199 (17.277 to 19.218) |
| variance ratio at 1 minutes, bts | yes | 1.139 (1.078 to 1.189) | 1.156 (1.132 to 1.260) | 1.202 (1.107 to 1.232) |
| variance ratio at 2 minutes, bts |  | 1.357 (1.395 to 1.580) **no** | 1.518 (1.615 to 1.850) **no** | 1.302 (1.519 to 1.738) **no** |
| variance ratio at 5 minutes, bts |  | 1.594 (1.576 to 1.917) | 1.620 (1.879 to 2.269) **no** | 1.705 (1.781 to 2.136) **no** |
| variance ratio at 10 minutes, bts | yes | 1.851 (1.631 to 2.097) | 2.231 (1.928 to 2.553) | 2.077 (1.834 to 2.343) |
| variance ratio at 20 minutes, bts |  | 1.966 (1.572 to 2.273) | 2.517 (1.907 to 2.719) | 2.171 (1.752 to 2.584) |
| variance ratio at 30 minutes, bts |  | 2.349 (1.515 to 2.352) | 2.879 (1.837 to 2.878) **no** | 2.019 (1.742 to 2.634) |
| variance ratio at 60 minutes, bts |  | 2.610 (1.371 to 2.553) **no** | 3.327 (1.696 to 3.286) **no** | 2.017 (1.591 to 2.853) |
| variance ratio at 180 minutes, bts |  | 5.028 (1.260 to 3.607) **no** | 3.565 (1.518 to 3.916) | 4.239 (1.281 to 3.866) **no** |
| impressions over rows |  | 1.046 (0.970 to 1.063) | 1.034 (0.971 to 1.061) | 1.025 (0.985 to 1.076) |
| blocks over rows |  | 1.373 (1.077 to 1.256) **no** | 1.449 (1.043 to 1.208) **no** | 1.474 (1.074 to 1.260) **no** |
| 5 minutes over ten |  | 0.953 (0.943 to 1.057) | 0.959 (0.939 to 1.053) | 0.982 (0.942 to 1.056) |
| 20 minutes over ten |  | 1.021 (0.938 to 1.072) | 1.053 (0.937 to 1.071) | 0.978 (0.938 to 1.074) |
| 30 minutes over ten |  | 1.054 (0.925 to 1.093) | 1.095 (0.920 to 1.092) **no** | 0.978 (0.922 to 1.091) |
| 60 minutes over ten |  | 1.069 (0.889 to 1.128) | 1.123 (0.888 to 1.132) | 1.007 (0.886 to 1.127) |
| 180 minutes over ten |  | 1.134 (0.802 to 1.221) | 1.365 (0.793 to 1.227) **no** | 1.029 (0.798 to 1.214) |
| reproduced |  | 16 of 25 | 11 of 25 | 15 of 25 |

- F reproduces what it was solved from except the ten-minute variance ratio of the random log, on every campaign: 1.89, 1.92 and 2.45 against upper ends of 1.72, 1.38 and 1.43. This is where `e_S` was cut back.
- It reproduces the published ratio of impressions to rows on every campaign, and on no campaign the published ratio of ten-minute blocks to rows: 1.37, 1.45 and 1.47 against upper ends of 1.26, 1.21 and 1.26 (medians 1.16, 1.12 and 1.16). In the registered M the range held the published ratio on All and Women's (1.23 to 1.43 and 1.26 to 1.46).
- In the BTS logs its variance ratio at two minutes is above the real one on every campaign and its ratio at 60 or 180 minutes below it (All at 60 and 180, Women's at 30 and 60, Men's at 180): sessions of two minutes put the dependence at shorter spans than the logs show.
- On Women's it does not reproduce the published widening at 30 and at 180 minutes (1.095 against 1.092, 1.365 against 1.227), as M did not at 180.
- The ranges of D1 and D2 rest on 400 data sets. Three statistics lie within 0.003 of an end of their range: on Women's the variance ratio of the BTS log at 30 minutes and "30 minutes over ten", both outside, and on All the one-minute variance ratio of the random log, inside. The counts could differ by one or two in another run.

F therefore shows less widening from rows to ten-minute blocks than the logs do, whether that widening in the logs is dependence or a click rate that moves between blocks. Within this click model, where a session cannot be stronger than an impression, the sessions that the registered rule forms in the random logs do not produce the measured ten-minute variance ratio from the measured excess within an impression.

## Results: the IPS ratio

Simulated coverage, its label if not adequate, and after the slash the coverage predicted in the calibration file. M and H are the registered scenarios, from `results/coverage.json`. A cell can be adequate while its Wilson interval excludes 0.95: 99 of the 672 cells of the extension are, and `cells.md` says so for every cell.

All:

| Scenario | rows | impressions | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| M (registered) | 0.866 (-) / 0.862 | 0.880 (-) / 0.879 | 0.948 / 0.949 | 0.951 / 0.951 | 0.953 / 0.952 | 0.953 / 0.952 | 0.951 / 0.953 | 0.950 / 0.954 |
| M.half-sessions | 0.884 (-) / 0.888 | 0.902 (-) / 0.903 | 0.947 / 0.951 | 0.947 / 0.952 | 0.948 / 0.953 | 0.948 / 0.953 | 0.950 / 0.953 | 0.945 / 0.954 |
| M.double-sessions | 0.863 (-) / 0.863 | 0.877 (-) / 0.880 | 0.945 / 0.947 | 0.946 / 0.949 | 0.950 / 0.951 | 0.949 / 0.952 | 0.948 / 0.953 | 0.945 / 0.954 |
| M.two-level | 0.873 (-) / 0.862 | 0.886 (-) / 0.879 | 0.950 / 0.949 | 0.951 / 0.951 | 0.951 / 0.952 | 0.954 / 0.952 | 0.949 / 0.953 | 0.948 / 0.954 |
| F | 0.905 (-) / 0.912 | 0.910 (-) / 0.916 | 0.946 / 0.953 | 0.945 / 0.953 | 0.946 / 0.954 | 0.946 / 0.954 | 0.947 / 0.954 | 0.942 / 0.955 |
| H (registered) | 0.779 (-) / 0.794 | 0.804 (-) / 0.814 | 0.900 (-) / 0.909 | 0.907 (-) / 0.915 | 0.916 (-) / 0.924 | 0.922 (?) / 0.931 | 0.931 (?) / 0.942 | 0.935 / 0.949 |
| H.half-long | 0.799 (-) / 0.798 | 0.821 (-) / 0.818 | 0.912 (-) / 0.911 | 0.915 (-) / 0.918 | 0.921 (?) / 0.926 | 0.929 (?) / 0.932 | 0.939 / 0.942 | 0.940 / 0.949 |
| H.double-long | 0.785 (-) / 0.794 | 0.807 (-) / 0.814 | 0.901 (-) / 0.908 | 0.907 (-) / 0.915 | 0.917 (?) / 0.924 | 0.925 (?) / 0.930 | 0.937 / 0.942 | 0.937 / 0.949 |
| H.two-level | 0.793 (-) / 0.794 | 0.816 (-) / 0.814 | 0.909 (-) / 0.909 | 0.914 (-) / 0.915 | 0.921 (?) / 0.924 | 0.929 (?) / 0.931 | 0.938 / 0.942 | 0.939 / 0.949 |
| FH | 0.848 (-) / 0.852 | 0.856 (-) / 0.858 | 0.909 (-) / 0.911 | 0.914 (-) / 0.917 | 0.925 (?) / 0.925 | 0.932 (?) / 0.932 | 0.940 / 0.942 | 0.942 / 0.950 |
| FS | 0.909 (-) / 0.911 | 0.914 (-) / 0.916 | 0.952 / 0.954 | 0.952 / 0.955 | 0.952 / 0.958 | 0.956 / 0.960 | 0.962 / 0.966 | 0.969 / 0.977 |
| S | 0.952 / 0.951 | 0.952 / 0.951 | 0.954 / 0.956 | 0.956 / 0.957 | 0.959 / 0.959 | 0.960 / 0.962 | 0.963 / 0.967 | 0.973 (?) / 0.978 |

Women's:

| Scenario | rows | impressions | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| M (registered) | 0.846 (-) / 0.850 | 0.860 (-) / 0.863 | 0.950 / 0.946 | 0.951 / 0.949 | 0.953 / 0.951 | 0.952 / 0.952 | 0.951 / 0.953 | 0.945 / 0.953 |
| M.half-sessions | 0.903 (-) / 0.895 | 0.911 (-) / 0.907 | 0.951 / 0.949 | 0.954 / 0.951 | 0.955 / 0.952 | 0.955 / 0.953 | 0.954 / 0.954 | 0.946 / 0.954 |
| M.double-sessions | 0.851 (-) / 0.847 | 0.863 (-) / 0.860 | 0.944 / 0.946 | 0.948 / 0.950 | 0.947 / 0.951 | 0.952 / 0.952 | 0.948 / 0.953 | 0.947 / 0.953 |
| M.two-level | 0.849 (-) / 0.850 | 0.864 (-) / 0.863 | 0.943 / 0.946 | 0.944 / 0.949 | 0.948 / 0.951 | 0.949 / 0.952 | 0.949 / 0.953 | 0.944 / 0.953 |
| F | 0.922 (?) / 0.924 | 0.928 (?) / 0.928 | 0.952 / 0.952 | 0.951 / 0.953 | 0.951 / 0.954 | 0.953 / 0.954 | 0.951 / 0.955 | 0.947 / 0.955 |
| H (registered) | 0.680 (-) / 0.679 | 0.696 (-) / 0.695 | 0.830 (-) / 0.829 | 0.850 (-) / 0.851 | 0.876 (-) / 0.879 | 0.893 (-) / 0.897 | 0.919 (?) / 0.925 | 0.931 (?) / 0.943 |
| H.half-long | 0.748 (-) / 0.753 | 0.763 (-) / 0.768 | 0.880 (-) / 0.884 | 0.894 (-) / 0.896 | 0.910 (-) / 0.910 | 0.917 (?) / 0.920 | 0.934 / 0.936 | 0.938 / 0.947 |
| H.double-long | 0.656 (-) / 0.654 | 0.674 (-) / 0.670 | 0.813 (-) / 0.809 | 0.839 (-) / 0.835 | 0.873 (-) / 0.868 | 0.894 (-) / 0.889 | 0.918 (?) / 0.921 | 0.937 / 0.942 |
| H.two-level | 0.687 (-) / 0.679 | 0.701 (-) / 0.695 | 0.830 (-) / 0.829 | 0.852 (-) / 0.851 | 0.876 (-) / 0.879 | 0.890 (-) / 0.897 | 0.921 (?) / 0.925 | 0.934 / 0.943 |
| FH | 0.739 (-) / 0.746 | 0.749 (-) / 0.753 | 0.809 (-) / 0.815 | 0.830 (-) / 0.838 | 0.863 (-) / 0.869 | 0.884 (-) / 0.892 | 0.917 (?) / 0.923 | 0.934 / 0.943 |
| FS | 0.922 (?) / 0.923 | 0.927 (?) / 0.927 | 0.956 / 0.956 | 0.960 / 0.960 | 0.965 / 0.966 | 0.967 / 0.971 | 0.979 (?) / 0.981 | 0.993 (+) / 0.995 |
| S | 0.950 / 0.951 | 0.953 / 0.951 | 0.957 / 0.958 | 0.962 / 0.961 | 0.968 / 0.967 | 0.968 / 0.972 | 0.979 (?) / 0.982 | 0.993 (+) / 0.995 |

Men's (descriptive):

| Scenario | rows | impressions | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| M (registered) | 0.863 (-) / 0.866 | 0.875 (-) / 0.875 | 0.942 / 0.946 | 0.944 / 0.949 | 0.948 / 0.951 | 0.947 / 0.952 | 0.946 / 0.952 | 0.941 / 0.953 |
| F | 0.908 (-) / 0.911 | 0.918 (?) / 0.920 | 0.946 / 0.952 | 0.946 / 0.953 | 0.947 / 0.953 | 0.948 / 0.953 | 0.947 / 0.954 | 0.941 / 0.954 |
| H (registered) | 0.855 (-) / 0.860 | 0.865 (-) / 0.869 | 0.939 / 0.943 | 0.941 / 0.946 | 0.943 / 0.948 | 0.942 / 0.950 | 0.943 / 0.951 | 0.939 / 0.953 |

## The registered reading

Confirmatory, on the IPS ratio on All and Women's. Coverage with its Wilson interval:

| Scenario | Campaign | rows | impressions | 10 min |
|---|---|---|---|---|
| M (registered) | All | 0.866 (0.855 to 0.876) (-) | 0.880 (0.870 to 0.890) (-) | 0.951 (0.943 to 0.957) |
| M (registered) | Women's | 0.846 (0.834 to 0.856) (-) | 0.860 (0.849 to 0.870) (-) | 0.951 (0.943 to 0.957) |
| M.half-sessions | All | 0.884 (0.874 to 0.894) (-) | 0.902 (0.892 to 0.911) (-) | 0.947 (0.940 to 0.954) |
| M.half-sessions | Women's | 0.903 (0.893 to 0.912) (-) | 0.911 (0.902 to 0.920) (-) | 0.954 (0.947 to 0.960) |
| M.double-sessions | All | 0.863 (0.852 to 0.873) (-) | 0.877 (0.867 to 0.887) (-) | 0.946 (0.938 to 0.952) |
| M.double-sessions | Women's | 0.851 (0.840 to 0.862) (-) | 0.863 (0.852 to 0.873) (-) | 0.948 (0.941 to 0.955) |
| M.two-level | All | 0.873 (0.862 to 0.883) (-) | 0.886 (0.876 to 0.896) (-) | 0.951 (0.944 to 0.957) |
| M.two-level | Women's | 0.849 (0.838 to 0.860) (-) | 0.864 (0.853 to 0.874) (-) | 0.944 (0.936 to 0.950) |
| F | All | 0.905 (0.895 to 0.913) (-) | 0.910 (0.900 to 0.918) (-) | 0.945 (0.937 to 0.951) |
| F | Women's | 0.922 (0.914 to 0.930) (?) | 0.928 (0.920 to 0.936) (?) | 0.951 (0.944 to 0.957) |
| H (registered) | All |  |  | 0.907 (0.898 to 0.916) (-) |
| H (registered) | Women's |  |  | 0.850 (0.838 to 0.860) (-) |
| H.half-long | All |  |  | 0.915 (0.906 to 0.924) (-) |
| H.half-long | Women's |  |  | 0.894 (0.884 to 0.903) (-) |
| H.double-long | All |  |  | 0.907 (0.898 to 0.916) (-) |
| H.double-long | Women's |  |  | 0.839 (0.827 to 0.850) (-) |
| H.two-level | All |  |  | 0.914 (0.905 to 0.923) (-) |
| H.two-level | Women's |  |  | 0.852 (0.841 to 0.863) (-) |
| FH | All |  |  | 0.914 (0.905 to 0.922) (-) |
| FH | Women's |  |  | 0.830 (0.818 to 0.841) (-) |

1. Check. With the registered choices the extended code gives the parameters of `results/calibration.json` on the three campaigns, and on the first 250 data sets of A and M on Women's the estimates and interval ends of the code of the coverage study (commit `6a276af`): the parameters agree within a relative 1e-12, and the data sets are identical to the last bit when both codes run with one thread of the linear algebra; with the extended code on four threads and the other on one, the largest difference is 1.3e-15.
2. Robustness. R1 is robust: rows and impressions under-cover in the three variants of M on both campaigns, at 0.849 to 0.903 and 0.863 to 0.911. R2 is robust: every block length is adequate in them, at 0.943 to 0.955. R3 is robust: ten-minute blocks under-cover in the three variants of H, at 0.907 to 0.915 on All and 0.839 to 0.894 on Women's. No label changed. The variants that were cut back cover more than the registered scenario: with half sessions rows cover 0.884 and 0.903 against 0.866 and 0.846 in M, and with half long groups ten-minute blocks cover 0.915 and 0.894 against 0.907 and 0.850 in H.
3. F and FH. In F every block length is adequate on both campaigns, at 0.942 to 0.953. Rows and impressions under-cover on All and are unresolved on Women's, where both Wilson intervals contain 0.925. In FH ten-minute blocks under-cover on both.
4. The label of each campaign by Section 4:

| Campaign | real `G(180)` | within types | drift | ranges apart | label |
|---|---|---|---|---|---|
| All | 0.199 | -0.550 to 0.297 | -0.313 to 0.412 | no | not separated, inside both ranges |
| Women's | 0.315 | -0.611 to 0.342 | 0.127 to 0.600 | no | not separated, inside both ranges |

Both campaigns are "not separated", with the real value inside both ranges, and on neither are the two ranges apart. On Women's the upper end of the range within types, 0.342, is the 97.5th percentile of FU; those of FH and FD are 0.311 and 0.310. The real value, 0.315, lies above both, 0.028 below that of FU, and below the median under a drift (0.42). FU on Women's is cut back (`e_L` 23.3 to 7.3), and the median of its ratio of standard deviations at 180 minutes is 1.102 against the 1.365 it was solved from. With the range within types taken from FH and FD alone, the real value would lie above it and inside the range under a drift, which Section 4 labels "more like a drift". The registered range includes FU, and the registered label is "not separated".

What the registration counts against the three results:

- R1 or R2 not robust, or with another label in F. Both are robust, and R2 has its labels in F. R1 has them in F on All and not on Women's, where rows and impressions are unresolved. By the registration R1 then depends on a choice of the model or does not hold at the dependence measured directly; this is so on Women's.
- R3 not robust, or ten-minute blocks not under-covering in FH. Neither is found.
- Women's labelled "more like a drift". Not found; item 4 says how near the label is.

What it counts for them, R1 to R3 robust and with the same labels in F and FH, holds for R2 and R3, and for R1 on All. "Not separated" leaves the statement of the coverage study on Women's as it is: its ten-minute intervals are not shown to cover.

Not part of the registered reading: F does not reproduce the published ratio of ten-minute blocks to rows on any campaign ("What F reproduces"), so its labels for rows and impressions are those of a scenario whose intervals widen less from rows to blocks than the published ones.

## Descriptive results

`G` by block length, real and over the first 1,000 data sets of each scenario (median, 2.5th to 97.5th percentile):

| Campaign |  | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|
| All | real | 0.035 | 0.079 | 0.045 | 0.093 | 0.150 | 0.199 |
| All | F | -0.00 (-0.07 to 0.07) | -0.00 (-0.10 to 0.09) | -0.00 (-0.14 to 0.11) | -0.01 (-0.17 to 0.14) | -0.01 (-0.26 to 0.18) | -0.03 (-0.51 to 0.29) |
| All | FH | -0.00 (-0.07 to 0.07) | -0.00 (-0.10 to 0.09) | -0.01 (-0.13 to 0.12) | -0.01 (-0.17 to 0.15) | -0.01 (-0.28 to 0.19) | -0.01 (-0.46 to 0.27) |
| All | FU | 0.00 (-0.07 to 0.07) | 0.00 (-0.09 to 0.09) | 0.00 (-0.13 to 0.12) | 0.00 (-0.17 to 0.15) | -0.00 (-0.25 to 0.19) | -0.01 (-0.55 to 0.30) |
| All | FS | 0.01 (-0.06 to 0.08) | 0.01 (-0.08 to 0.10) | 0.03 (-0.10 to 0.15) | 0.04 (-0.12 to 0.19) | 0.07 (-0.15 to 0.25) | 0.15 (-0.31 to 0.41) |
| All | S | 0.01 (-0.06 to 0.08) | 0.01 (-0.08 to 0.11) | 0.03 (-0.11 to 0.15) | 0.04 (-0.14 to 0.19) | 0.08 (-0.16 to 0.27) | 0.16 (-0.29 to 0.42) |
| All | M.half-sessions | 0.23 (0.16 to 0.30) | 0.24 (0.15 to 0.33) | 0.24 (0.13 to 0.35) | 0.24 (0.11 to 0.36) | 0.24 (0.06 to 0.39) | 0.24 (-0.11 to 0.47) |
| All | M.double-sessions | 0.29 (0.23 to 0.36) | 0.30 (0.22 to 0.38) | 0.31 (0.21 to 0.40) | 0.31 (0.19 to 0.42) | 0.32 (0.14 to 0.46) | 0.31 (0.01 to 0.53) |
| All | M.two-level | 0.31 (0.24 to 0.38) | 0.32 (0.23 to 0.41) | 0.32 (0.20 to 0.43) | 0.32 (0.20 to 0.44) | 0.32 (0.14 to 0.45) | 0.32 (-0.02 to 0.51) |
| All | H.half-long | 0.32 (0.26 to 0.39) | 0.34 (0.27 to 0.42) | 0.37 (0.28 to 0.46) | 0.39 (0.27 to 0.49) | 0.42 (0.27 to 0.53) | 0.44 (0.17 to 0.61) |
| All | H.double-long | 0.32 (0.26 to 0.39) | 0.34 (0.27 to 0.42) | 0.37 (0.28 to 0.46) | 0.39 (0.28 to 0.49) | 0.43 (0.29 to 0.55) | 0.44 (0.19 to 0.61) |
| All | H.two-level | 0.32 (0.23 to 0.41) | 0.34 (0.25 to 0.44) | 0.37 (0.26 to 0.47) | 0.39 (0.26 to 0.50) | 0.43 (0.27 to 0.55) | 0.44 (0.17 to 0.61) |
| All | FD | -0.00 (-0.07 to 0.07) | -0.00 (-0.09 to 0.09) | -0.01 (-0.14 to 0.12) | -0.01 (-0.18 to 0.14) | -0.02 (-0.28 to 0.18) | -0.04 (-0.53 to 0.28) |
| Women's | real | 0.012 | -0.010 | 0.024 | 0.077 | 0.095 | 0.315 |
| Women's | F | -0.00 (-0.07 to 0.07) | 0.00 (-0.11 to 0.10) | 0.00 (-0.15 to 0.13) | -0.00 (-0.19 to 0.17) | -0.00 (-0.30 to 0.21) | -0.02 (-0.59 to 0.31) |
| Women's | FH | -0.00 (-0.08 to 0.08) | -0.00 (-0.12 to 0.10) | -0.00 (-0.17 to 0.14) | -0.01 (-0.22 to 0.16) | -0.01 (-0.33 to 0.22) | -0.02 (-0.59 to 0.31) |
| Women's | FU | -0.00 (-0.08 to 0.07) | -0.01 (-0.11 to 0.10) | -0.00 (-0.16 to 0.13) | -0.01 (-0.20 to 0.15) | -0.01 (-0.30 to 0.22) | -0.00 (-0.56 to 0.34) |
| Women's | FS | 0.03 (-0.05 to 0.09) | 0.05 (-0.04 to 0.14) | 0.10 (-0.04 to 0.21) | 0.14 (-0.03 to 0.28) | 0.24 (0.02 to 0.40) | 0.42 (0.13 to 0.60) |
| Women's | S | 0.03 (-0.04 to 0.10) | 0.05 (-0.04 to 0.15) | 0.10 (-0.03 to 0.21) | 0.14 (-0.01 to 0.27) | 0.23 (0.03 to 0.39) | 0.42 (0.12 to 0.59) |
| Women's | M.half-sessions | 0.22 (0.16 to 0.29) | 0.24 (0.15 to 0.32) | 0.24 (0.13 to 0.35) | 0.24 (0.10 to 0.37) | 0.25 (0.04 to 0.41) | 0.24 (-0.18 to 0.49) |
| Women's | M.double-sessions | 0.37 (0.31 to 0.43) | 0.39 (0.32 to 0.46) | 0.39 (0.30 to 0.48) | 0.39 (0.27 to 0.49) | 0.39 (0.23 to 0.53) | 0.39 (0.07 to 0.60) |
| Women's | M.two-level | 0.36 (0.29 to 0.44) | 0.37 (0.29 to 0.46) | 0.38 (0.28 to 0.48) | 0.39 (0.26 to 0.49) | 0.38 (0.20 to 0.53) | 0.38 (0.03 to 0.59) |
| Women's | H.half-long | 0.38 (0.32 to 0.44) | 0.41 (0.34 to 0.48) | 0.45 (0.36 to 0.54) | 0.48 (0.38 to 0.57) | 0.53 (0.40 to 0.63) | 0.56 (0.31 to 0.70) |
| Women's | H.double-long | 0.40 (0.35 to 0.46) | 0.46 (0.40 to 0.53) | 0.53 (0.45 to 0.60) | 0.57 (0.48 to 0.65) | 0.63 (0.52 to 0.71) | 0.67 (0.49 to 0.77) |
| Women's | H.two-level | 0.39 (0.31 to 0.47) | 0.44 (0.36 to 0.53) | 0.51 (0.40 to 0.60) | 0.54 (0.44 to 0.64) | 0.60 (0.47 to 0.70) | 0.64 (0.43 to 0.76) |
| Women's | FD | -0.00 (-0.07 to 0.07) | -0.00 (-0.11 to 0.09) | -0.01 (-0.15 to 0.13) | -0.01 (-0.18 to 0.15) | -0.01 (-0.28 to 0.21) | -0.04 (-0.61 to 0.31) |

- The drift in one log that matches the published widening has a median `G(180)` of 0.15 on All and 0.42 on Women's (FS). Without a movement of one log against the other the 97.5th percentile of `G(180)` is 0.27 to 0.34 (FH, FU, FD). The ranges overlap on both campaigns, as the registration expected for All and allowed for Women's.
- The registered M and H form sessions without regard to user types, and their variants have a `G` of 0.24 to 0.46 at ten minutes (medians). The real `G(10)`, 0.079 on All and -0.010 on Women's, lies below the 2.5th percentile of every one of these variants (0.150 at the lowest) and inside the range of F, of every scenario built on it and of S; on All it is 0.008 below the upper end of the range of FH (0.088). Under the assumptions of D3 the logs differ in this respect from the six variants, and so from the groupings of the registered M and H.

The standard deviation of the replicates of the IPS ratio over the one at ten minutes (median, 2.5th to 97.5th percentile over the data sets):

| Campaign |  | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|
| All | F | 1.002 (0.938 to 1.072) | 1.003 (0.925 to 1.093) | 1.002 (0.889 to 1.128) | 0.997 (0.802 to 1.221) |
| All | FH | 1.026 (0.961 to 1.096) | 1.052 (0.967 to 1.144) | 1.091 (0.958 to 1.225) | 1.114 (0.889 to 1.361) |
| All | FU | 1.008 (0.945 to 1.080) | 1.017 (0.934 to 1.109) | 1.032 (0.919 to 1.168) | 1.093 (0.858 to 1.345) |
| All | FS | 1.011 (0.947 to 1.083) | 1.023 (0.939 to 1.115) | 1.053 (0.924 to 1.185) | 1.116 (0.885 to 1.368) |
| All | S | 1.011 (0.947 to 1.076) | 1.023 (0.944 to 1.111) | 1.051 (0.936 to 1.174) | 1.119 (0.908 to 1.347) |
| All | M.half-sessions | 1.003 (0.938 to 1.071) | 1.005 (0.923 to 1.092) | 1.003 (0.891 to 1.132) | 0.999 (0.810 to 1.215) |
| All | M.double-sessions | 1.009 (0.944 to 1.077) | 1.011 (0.928 to 1.099) | 1.010 (0.891 to 1.139) | 1.005 (0.798 to 1.226) |
| All | M.two-level | 1.004 (0.941 to 1.073) | 1.007 (0.926 to 1.096) | 1.006 (0.891 to 1.130) | 1.000 (0.800 to 1.220) |
| All | H.half-long | 1.027 (0.961 to 1.101) | 1.049 (0.964 to 1.143) | 1.084 (0.958 to 1.221) | 1.106 (0.881 to 1.358) |
| All | H.double-long | 1.028 (0.962 to 1.100) | 1.050 (0.966 to 1.141) | 1.092 (0.967 to 1.232) | 1.110 (0.897 to 1.363) |
| All | H.two-level | 1.028 (0.960 to 1.104) | 1.049 (0.964 to 1.147) | 1.089 (0.964 to 1.232) | 1.112 (0.892 to 1.364) |
| All | published | 1.021 | 1.054 | 1.069 | 1.134 |
| Women's | F | 1.002 (0.937 to 1.071) | 1.003 (0.920 to 1.092) | 1.004 (0.888 to 1.132) | 0.995 (0.793 to 1.227) |
| Women's | FH | 1.081 (1.014 to 1.150) | 1.147 (1.056 to 1.245) | 1.254 (1.111 to 1.411) | 1.339 (1.062 to 1.653) |
| Women's | FU | 1.012 (0.948 to 1.079) | 1.018 (0.936 to 1.104) | 1.039 (0.918 to 1.166) | 1.102 (0.880 to 1.373) |
| Women's | FS | 1.035 (0.967 to 1.104) | 1.056 (0.971 to 1.144) | 1.138 (1.009 to 1.270) | 1.347 (1.110 to 1.598) |
| Women's | S | 1.033 (0.970 to 1.101) | 1.055 (0.972 to 1.135) | 1.136 (1.011 to 1.263) | 1.352 (1.108 to 1.588) |
| Women's | M.half-sessions | 1.005 (0.937 to 1.073) | 1.006 (0.923 to 1.096) | 1.007 (0.887 to 1.136) | 0.996 (0.801 to 1.230) |
| Women's | M.double-sessions | 1.006 (0.938 to 1.077) | 1.008 (0.923 to 1.098) | 1.010 (0.886 to 1.143) | 0.998 (0.797 to 1.228) |
| Women's | M.two-level | 1.007 (0.941 to 1.080) | 1.008 (0.924 to 1.097) | 1.008 (0.891 to 1.146) | 1.002 (0.800 to 1.233) |
| Women's | H.half-long | 1.044 (0.975 to 1.117) | 1.075 (0.987 to 1.169) | 1.133 (1.001 to 1.281) | 1.167 (0.932 to 1.449) |
| Women's | H.double-long | 1.087 (1.015 to 1.157) | 1.144 (1.050 to 1.243) | 1.256 (1.107 to 1.417) | 1.341 (1.061 to 1.658) |
| Women's | H.two-level | 1.073 (0.999 to 1.148) | 1.124 (1.030 to 1.229) | 1.221 (1.078 to 1.386) | 1.289 (1.019 to 1.611) |
| Women's | published | 1.053 | 1.095 | 1.123 | 1.365 |
| Men's | F | 1.002 (0.938 to 1.074) | 1.006 (0.922 to 1.091) | 1.002 (0.886 to 1.127) | 0.997 (0.798 to 1.214) |
| Men's | published | 0.978 | 0.978 | 1.007 | 1.029 |

- The published ratios at 20, 30, 60 and 180 minutes lie inside the ranges of FH, FU and FS on both campaigns, so the shape of the widening by block length does not separate dependence from drift either. On Women's the published ratio at 60 minutes, 1.123, is at the lower end of FH (1.111 to 1.411) and near the median of FS (1.138).
- Section 4 expected blocks to cover at least as often as nominal under a drift, more so the longer they are. In FS and S, for the IPS ratio, no block length under-covers and 180-minute blocks cover more than five-minute blocks (FS 0.952 and 0.969 on All, 0.956 and 0.993 on Women's; S 0.954 and 0.973, 0.957 and 0.993); the coverage does not rise at every step (FS on All is 0.952 at 5, 10 and 20 minutes). In FS ten-minute blocks cover 0.952 on All and 0.960 on Women's, and 180-minute blocks over-cover on Women's. In S, with independent clicks, rows are adequate (0.952 and 0.950) and 180-minute blocks are unresolved on All (0.973) and over-cover on Women's (0.993). In FS rows cover 0.909 and 0.922, as in F (0.905 and 0.922).
- Men's. In F rows under-cover (0.908), impressions are unresolved (0.918) and every block length is adequate (0.941 to 0.948). The real `G(180)`, -0.196, lies inside the range of F (-0.557 to 0.286).
- The click rate of the BTS log. With the drift in that log, blocks over-cover from ten minutes in FS (0.986 on All, 0.989 on Women's) and from five in S. In FH ten-minute blocks cover 0.758 on All and 0.603 on Women's. `cells.md` has every quantity.

## The prediction against the simulation

The calibration file predicted every coverage before a click was generated. Simulated minus predicted coverage:

| Quantity | Cells | Prediction outside the Wilson interval | Mean of simulated minus predicted | Smallest | Largest | Cells more than 0.01 apart |
|---|---|---|---|---|---|---|
| ips_ratio | 168 | 27 | -0.003 | -0.014 | +0.011 | 5 |
| snips_ratio | 168 | 22 | -0.003 | -0.013 | +0.012 | 6 |
| ips | 168 | 27 | -0.002 | -0.013 | +0.010 | 5 |
| v_on | 168 | 37 | -0.003 | -0.027 | +0.016 | 25 |
| all | 672 | 113 | -0.003 | -0.027 | +0.016 | 41 |

The prediction lies outside the Wilson interval of the simulated coverage in 113 of 672 cells, which `cells.md` lists; the simulated coverage is lower by 0.003 on average. The widest gap is on the click rate of the BTS log on Women's in FH at ten minutes, predicted 0.630 and simulated 0.603; for the IPS ratio it is 0.014 (All, F, 180 minutes, predicted 0.955 and simulated 0.942). In the 72 cells of the confirmatory reading the prediction and the simulated coverage lie on the same side of 0.925; in 12 of them the prediction is outside the Wilson interval, seven of them block lengths in F, where the simulated coverage is lower by 0.007 to 0.014.

## Where the implementation settles what the registration leaves open

- FU. Section 6 says FU is simulated without intervals, and Section 4 asks for the standard deviations of its replicates. Its 1,000 data sets got replicates; only ratios of their standard deviations are reported, and no coverage.
- Session sizes. The size of a session is chosen per log, as `e_I` and `e_S` are; the size of a long group per campaign. Within each nominal size the span `T` is the one whose one-minute ratio, with `e_S` cut back, is closest to the published one, and the solved `e_S` is tested against `e_I` at that span only.
- Drift. FD has the drift of scenario D as the coverage study applied it, in both logs and without rescaling, so its true values are those of D. In FS and S the probabilities of the BTS log are rescaled to their sum, as Section 4 says.
- Intervals of D2. Each log has one random stream, used for the eight block lengths in increasing order.
- The stop at a probability above 1 uses an upper bound, the largest click probability of a log times the largest product of its factors, whichever groups are at the high level.
- Check 1. The data sets are compared at a tolerance of 1e-12, because their last digits depend on the number of threads of the linear algebra; item 1 of the reading gives what was found.
- A real value inside exactly one of the two ranges of Section 4 that is labelled "not separated" would be reported as outside both. This did not occur.
- The summaries of `V` and `W` within each log for the simulated scenarios (`ef1b885`) and the code of the tables (`af23a3c`) were committed after the calibration, while the data sets were being simulated and before any of them was read. They touch neither the clicks, the intervals nor the confirmatory reading.
- `posthoc.json` (the sessions of F and the largest impressions) was added after the reading. It describes the fit and one measurement and enters no reading.
- The data sets were simulated by commits `2e4eee4` to `af23a3c`, which do not differ in the code that generates or resamples clicks, in 7.8 CPU hours on four cores; the reduction of Section 9 was not used.

## What the extension cannot show

Section 7 of the registration. In short: it does not show that the real dependence has the structure of F, and the fit above shows where it has not; it separates a drift from dependence only under the assumptions of D3 (clicks of different user types and of different logs independent given the rates, a drift that moves all user types alike), and on these logs the registered observable does not separate them; a user type is a combination of hashed features and not a user; the drift has one fitted shape; the choices are varied one at a time; the pooled unit, `rho`, `d`, H5 and H6 of `obd` are not simulated; one dataset and one week.
