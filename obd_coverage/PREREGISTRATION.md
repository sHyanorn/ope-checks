# Coverage of bootstrap intervals on the Open Bandit Dataset: a semi-synthetic study

Registration. This file is committed before any code of the study and before any simulated interval exists. The results of the `obd` study and of its post hoc analyses were known when it was written, and its calibration uses numbers published there.

## 1. Question

The `obd` study reports 95% percentile intervals from a bootstrap over ten-minute clock blocks. Post hoc, its intervals on All and Women's widen with the block length (`obd/posthoc/README.md`, Section 4). On the real logs the value of a policy is unknown, so the coverage of these intervals cannot be counted.

Here the logs keep their rows and get clicks from a known process. The value of every quantity is then known, and the study counts how often a nominal 95% interval contains it, by resampling unit (rows, impressions, clock blocks of 5 to 180 minutes) and by the kind of dependence among clicks.

## 2. Kept and generated

Kept, per campaign (All, Men's, Women's) and log (random, BTS): every row inside the week with its timestamp, item, position, user features and recorded propensity; the impressions as Section 7 of the `obd` registration defines them (`obd.posthoc.units.impressions`); the fixed-prior target `pi0` with its registered stream. The recorded propensities enter no quantity of this study.

Generated: the click of every row. Nothing else is random between simulated data sets. Clicks do not feed back into the lists.

## 3. Click model

Marginal click probability of row `i`: `q_i = q(a_i, k_i) x m(t_i)`.

- `q(a, k)` is the click rate of item `a` at position `k` in the two real logs of the campaign taken together. Both logs share it.
- `m(t)` is 1 except in scenario D.

Dependence comes from three nested groupings of the rows of a log, fixed per campaign and log by the stream `numpy.random.default_rng([20261111, 0, c, l])` (campaign `c` as in `obd.data.CAMPAIGNS`, log `l`: random 0, BTS 1):

- Impression: as kept.
- Session: every impression gets one of `J` labels, uniformly; label `j` has an offset `o_j`, uniform on `[0, T)`. The session of an impression with label `j` whose first row is at time `t` is `(j, floor((t + o_j) / T))`. `J` is the number of impressions of the log per `T` minutes divided by 5.5 and rounded, so a session holds 5.5 impressions on average. The registration counts 142,227 complete impressions on 25,759 lists in the random log of Men's when repeats of a list within two minutes count as one (Section 3): 5.5 impressions per list. `T` is set in Section 5.
- Long group, of span `T_L` (60 minutes or 24 hours): the sessions of a label are numbered in time; every session gets one of `M` sub-labels, uniformly, and every (label, sub-label) an offset `o'`, uniform on `0 .. T_L / T - 1`. The long group of session number `s` is `(j, sub-label, floor((s + o') / (T_L / T)))`. `M` is `T_L / (3 T)` rounded, so a long group holds three sessions on average. The three is a choice without a measurement behind it; only its product with the strength enters the variance of an estimate.

They are synthetic. The files hold no user identifier, and no group is claimed to be a user.

Every group of each grouping in force is, independently, on with probability `p` and off otherwise. A row whose groups are all on is clicked with probability `q_i` over the product of their `p`, independently of the other rows; any other row is not clicked. The marginal probability is `q_i` exactly, in every scenario, so scenarios with the same `m` share their true values. For two rows `i` and `j`, `P(both clicked) = q_i q_j (1 + e)`, with `e = 0` in different long groups, `e_L` in the same long group and different sessions, `e_S` in the same session and different impressions, `e_I` in the same impression. The on-probabilities are `1 / (1 + e_L)`, `(1 + e_L) / (1 + e_S)` and `(1 + e_S) / (1 + e_I)`. This needs `e_L <= e_S <= e_I` and `(1 + e_I) max q <= 1`. A grouping not in force has the excess of the next wider one (0 beyond the widest).

On/off factors are used because they hold the marginals exactly at any strength that two binary variables allow. Factors of another shape with the same second moments could give other finite-sample results.

## 4. Scenarios

| | Groupings in force | `m(t)` | Purpose |
|---|---|---|---|
| A | none | 1 | independent clicks: every method should cover |
| I | impression | 1 | dependence within an impression |
| M | impression, session | 1 | clustering over a few minutes, at the strength measured in the logs |
| D | none | drift | a click rate that moves over the week in both logs alike |
| H | impression, session, long group of 60 minutes | 1 | dependence beyond ten minutes |
| U | impression, session, long group of 24 hours | 1 | dependence across a day |

D: `m` is fitted to the real clicks, summed by hour. This step reads real clicks; it is a descriptive calibration, computed and committed with the calibration file before any coverage exists. For day `d` and hour of day `h`, `D_d` and `H_h` are the clicks of both logs in that day (hour of day) over the sum of `q(a, k)` over their rows. `m` at the midpoint of each clock hour is `D_d x H_h`, linear in between and constant before the first and after the last midpoint, then scaled so that the sum of `q_i` over all rows equals that with `m = 1`.

## 5. Calibration

The strengths are solved from numbers already published in `obd/posthoc/results/`, by formulas that use the kept rows and `q` and generate no click. For a linear statistic `X = sum_i a_i c_i` over the rows of one log, and a grouping `G`, let `P_G(a) = sum over groups of [(sum_{i in g} a_i q_i)^2 - sum_{i in g} a_i^2 q_i^2]`. Then

`Var(X) = sum_i a_i^2 q_i (1 - q_i) + e_I P_imp(a) + e_S [P_sess(a) - P_imp(a)] + e_L [P_long(a) - P_sess(a)]`.

For the IPS ratio the coefficients are those of its linearisation: `w_i / sum_R(w q)` on the random log and `-1 / sum_B(q)` on the BTS log. The expected variance of a bootstrap is taken as: rows, the first term; impressions, the first two terms; blocks of length `L`, the sum over blocks of the squared expectation of the block's contribution plus its variance by the formula with the pairs inside the block.

- `e_I`, one per campaign: the published standard deviation of the IPS ratio with impressions over that with rows (`units.json`: 1.046 All, 1.034 Women's, 1.025 Men's) equals the square root of the expected variances' ratio.
- `e_S`, one per campaign and log: the published variance ratio at ten minutes (`units.json`, `variance_ratio.10.clicks`: random 1.90, 1.92, 2.45 and BTS 1.85, 2.23, 2.08 for All, Women's, Men's) equals the expectation of that statistic's numerator over the expectation of its denominator, with the kept change of the item mix between adjacent blocks counted in the numerator. `T` is the one of 1, 2, 3, 5 and 10 minutes whose solution brings the same ratio at one minute closest to the published one.
- `e_L`, one per campaign and span: the published standard deviation of the IPS ratio at 180 minutes over that at ten (`blocks.json`: 1.134 All, 1.365 Women's, 1.029 Men's) equals the square root of the expected block variances' ratio.

If a solution is negative it is set to 0; if it breaks `e_L <= e_S <= e_I` the smaller one is used for both; if `(1 + e_I) max q > 1` the run stops. Each case is reported. The published numbers are point values without intervals, and the variance ratio does not separate dependence from a click rate that moves between blocks; matching all of it by dependence makes M an upper reading of short-range dependence.

The calibration file holds, per campaign: `q`, `m`, `T`, `J`, `M`, the strengths, the true values, and for every scenario, quantity and method the coverage that the expected variances and a normal approximation predict. It is committed before any click is generated for an interval. Nothing is retuned afterwards.

## 6. Quantities, true values, intervals

Quantities, as `obd.posthoc.units.ratios` computes them: the IPS ratio of H3 (primary), the SNIPS ratio, and separately the IPS estimate and the click rate of the BTS log.

True values, exact sums over the kept rows: the click rate of the BTS log is the mean of `q_i` over it; the IPS value is the mean of `w_i q_i` over the random log, `w_i = n_A pi0(a_i | k_i)`; the SNIPS value divides the sum of `w_i q_i` by the sum of `w_i`; a ratio divides by the click rate of the BTS log. They are conditional on the kept rows: which items were shown, and when, is not part of what an interval is asked to cover.

Intervals: 2.5th and 97.5th percentiles (linear interpolation) of 2,000 replicates, under eight resampling units.

- Rows, and impressions, drawn in each log on its own, as in Section 1 of the post hoc analyses.
- Clock blocks of 5, 10, 20, 30, 60 and 180 minutes, the same blocks in both logs. The multiplicities are the first 2,000 of the streams the `obd` study used: the registered one at ten minutes, `[20261110, 3, L, i]` otherwise.

The `obd` intervals use 10,000 replicates. An end from 2,000 has a standard error of 0.060 standard deviations of the replicates against 0.027; by a normal approximation the coverage with 2,000 is lower by about 0.03 percentage points.

Streams: clicks of data set `s` of scenario `x` (A 0 to U 5) on campaign `c`: `[20261111, 1, c, x, s]`. Replicates drawn afresh per data set (rows; impressions of the BTS log): `[20261111, 2, c, x, s]`. Multiplicities of the impressions of the random log, drawn once per campaign and reused: `[20261111, 3, c]`.

## 7. Number of data sets

4,000 per scenario and campaign, the same data sets for all quantities and units. The Monte Carlo standard error of a coverage `p` is `sqrt(p (1 - p) / 4000)`: 0.34 points at 0.95, 0.47 at 0.90. The number follows from the reading of Section 9: a true coverage 1.5 points on either side of the bound 0.925 is to be labelled correctly with probability 0.9, which needs `p (1 - p) ((1.96 + 1.28) / 0.015)^2` data sets: 3,821 at 0.91 and 2,631 at 0.94.

## 8. Reported

For every scenario, campaign, quantity and unit: coverage with its Wilson 95% interval; the shares of intervals lying above and below the true value; the mean and the median width; the mean standard deviation of the replicates over the standard deviation of the estimate across data sets; the coverage of the mean estimate in place of the true value; the predicted coverage of Section 5. The prediction stands beside the simulated coverage in every cell, the cells in which it fails included; none is left out.

For every scenario and campaign: the distribution over data sets of the standard deviation of the replicates at each block length over that at ten minutes, and with impressions and with blocks over rows; on the first 200 data sets, the variance ratios at 1, 10 and 60 minutes per log (`obd.posthoc.units.variance_ratio`). These are set beside the published values.

## 9. Reading, fixed here

Labels of a cell, from its Wilson interval:

- adequate: the interval lies within 0.925 to 0.975;
- under-covers: it lies below 0.925;
- over-covers: it lies above 0.975;
- unresolved: otherwise.

The band is this study's own: an error rate between half and one and a half times the nominal 5%. Whether the Wilson interval contains 0.95 is reported beside the label.

Primary cells: the IPS ratio on All and on Women's.

1. Check of the implementation: in A, rows must be adequate on both campaigns. If not, the error is found, everything is rerun, and the failure is reported.
2. In M: the labels of rows, impressions and ten-minute blocks.
3. In every scenario: the shortest block length that is adequate, whether every longer one is, or that none is.
4. In H and U: the labels of ten-minute and 180-minute blocks.
5. The published widening against M: for each campaign, whether the published ratio of standard deviations at 60 or at 180 minutes exceeds the 97.5th percentile of the simulated ones in M. With respect to the `obd` study this item is post hoc and descriptive: it uses published numbers only and changes no registered label. With two looks per campaign and no allowance, a campaign is flagged by chance in at most about 5% of cases.

What counts against the ten-minute intervals of the `obd` study:

- Ten-minute blocks under-cover in M on All or on Women's. Then the registered intervals are too narrow even if the dependence in the logs reaches only a few minutes, by the factor reported.
- A campaign is flagged in item 5. Then the widening on that campaign is more than short-range dependence of the measured strength produces, the labels of H and U at ten minutes say what follows if it is dependence, and the registered intervals on that campaign are reported as not shown to cover.
- No block length is adequate in U. Then the published statistics do not exclude a structure in which no interval of this study covers.

What counts for them: ten-minute blocks adequate in M on both campaigns and no campaign flagged.

H and U are tuned so that the true variance exceeds what ten-minute blocks see; a ten-minute label of "under-covers" there is expected and is no finding by itself. What is open there is by how much, and whether longer blocks cover.

The five items on the primary cells and the three statements under "What counts against" are all the confirmatory readings of this study. Everything else is descriptive: Men's, the other three quantities, I and D, widths, one-sided shares, the comparison with the prediction. No allowance is made for the number of cells.

Results are not given to more digits than the Monte Carlo error carries.

## 10. What the study cannot show

- That the real dependence has any of these structures. It answers: if the clicks were dependent in this way, would the interval cover.
- Which of M, H, U or a drift that the two logs do not share is behind the widening on All and Women's. D moves both logs alike.
- Anything about a structure not simulated: effects between positions other than a shared factor, users whose click rates differ by item, clicks that change later lists, dependence between the two logs beyond D.
- Coverage for a value that averages over which items are shown. The true values are conditional on the kept rows, and a bootstrap over blocks also counts the change of the item mix between blocks as noise.
- The pooled unit, `rho`, `d`, H5 and H6 of the `obd` study. They are not simulated.
- The strengths are solved from point values without intervals, the session size comes from one log of the development campaign, and the long groups of three sessions are a choice.

No registered file, result or label of the `obd` study changes.

## 11. Order

1. This file.
2. Code and tests. Every generator has a test against a known answer (marginal rate, variance, the pair probabilities of Section 3). With the real clicks and all 10,000 multiplicities the block code must reproduce the intervals of `obd/posthoc/results/blocks.json`.
3. The calibration file.
4. The run, the results, and the reading of Section 9.

## 12. Computing

CPU only. On placeholder arrays of the size of All, one data set takes about 0.3 seconds (clicks 0.1, replicates 0.1, sums and percentiles the rest); the three campaigns together about 0.6 seconds. Six scenarios of 4,000 data sets are then about 4 CPU hours, 1.5 hours on three processes. If a measured rate puts the run beyond 6 hours, the number of data sets is halved for I and D first and then Men's is left out; the primary cells keep 4,000.

## 13. Sources

Read in the parts named; the study borrows the points listed.

- T. P. Morris, I. R. White, M. J. Crowther, "Using simulation studies to evaluate statistical methods", Statistics in Medicine 38(11), 2019 (arXiv 1712.03198, Sections 5.2 to 5.4): the number of repetitions from the Monte Carlo error wanted; the error beside every coverage; coverage of the mean estimate to separate bias from width.
- E. Bakshy, D. Eckles, "Uncertainty in online experiments with dependent data", KDD 2013 (arXiv 1304.7406v4, Sections 3 and 4): simulated clicks with random effects on a fixed layout, 1,000 simulations per setting, Wilson intervals for coverage.
- M. Bertrand, E. Duflo, S. Mullainathan, "How much should we trust differences-in-differences estimates?" (NBER Working Paper 8841, 2002, Sections 3 and 4): placebo interventions on real data; a scenario without dependence as a check of the test bed; a block bootstrap that rejects too often with few blocks.
- A. C. Cameron, D. L. Miller, "A practitioner's guide to cluster-robust inference", Journal of Human Resources 50(2), 2015 (author manuscript, Sections IV and VI): larger and fewer clusters trade bias for variability, with no general rule.
- S. Gonçalves, H. White, "The bootstrap of the mean for dependent heterogeneous arrays" (CIRANO Working Paper 2001s-19, Sections 2 and 4): with means that differ over time the block bootstrap variance carries an extra term from their heterogeneity.
- Open Bandit Pipeline, `obp/dataset/synthetic.py` at tag 0.5.5: clicks as independent Bernoulli draws from a known probability, and the true value as the policy-weighted mean of those probabilities on the realised rows. The pipeline is not a dependency.

A search found no study that counts the coverage of intervals for off-policy estimates on this dataset, compares resampling units on it against a known value, or generates clicks on its kept lists; the search and what it could not read are in the study's README.
