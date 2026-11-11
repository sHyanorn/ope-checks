# Extension of the coverage study: measured dependence, a drift the logs do not share, sensitivity

Registration. This file is committed before any code of the extension and before any number of it exists. The results of the coverage study (`README.md`, `results/`) and of the `obd` study were known when it was written. Before it was written, the user features of the logs were counted without reading a click: a log holds 345 to 474 distinct combinations of the four hashed user features, the largest holds 23% to 35% of its rows, and one over the sum of squared shares is 7.3 (All), 10.2 (Men's) and 13.6 (Women's).

`PREREGISTRATION.md`, `results/calibration.json`, `results/coverage.json` and `results/cells.md` stay as they are. Nothing here changes a registered file, result or label of the `obd` study, and nothing here is a verdict on it.

## 1. Questions

The coverage study left three things open (its README, "What the study cannot show").

1. Its strengths were solved from three published summaries, and the nesting of the model cut several of them back. What do the real clicks show of the dependence when it is measured directly, and does a model fitted to those measurements change the coverage?
2. On Women's the intervals of the real logs widen with the block length by more than the short-range scenario produces. Dependence that reaches beyond ten minutes is one explanation, a click rate that moves differently in the two logs another. Which observable tells them apart, and where do the real logs fall?
3. A session of 5.5 impressions, a long group of three sessions and the on/off shape of the group factor were choices. Do the three main results depend on them?

The three main results, on the IPS ratio on All and Women's (`results/coverage.json`, reading):

- R1. In M, rows and impressions under-cover.
- R2. In M, every block length from 5 to 180 minutes is adequate.
- R3. In H, ten-minute blocks under-cover.

## 2. Direct measurements on the real clicks

These read the real clicks. With respect to the `obd` study they are post hoc and descriptive, and none of them is read as a verdict on it. They are computed once, by the code committed after this file, on every campaign and log.

`q(a, k)` is the click rate of item `a` at position `k` as in `results/calibration.json`. A user type is a combination of the four user features as written in the file of a log.

- D1, double clicks. `N2` is the number of pairs of clicked rows that share an impression; `E0` is the sum over impressions of the sum of `q_i q_j` over its pairs of rows. `e_I^ = N2 / E0 - 1` estimates the excess of Section 3 of the registration within an impression. Interval: 2.5th and 97.5th percentiles of `N2 / E0 - 1` over 2,000 resamples of the 1,008 ten-minute blocks of the log.
- D2, variance ratio by block length. The statistic of `obd.posthoc.units.variance_ratio` at 1, 2, 5, 10, 20, 30, 60 and 180 minutes. Interval: percentiles over 2,000 resamples of the pairs of adjacent blocks that the statistic keeps. At 1, 10 and 60 minutes the values must equal the published ones.
- D3, block residuals by log and user type. For a block length `L` (5 to 180 minutes) and block `b`, the residual of user type `u` in the random log is the sum over its rows in the block of `w_i (c_i - r_u q_i)`, over the sum of `w_i c_i` over the log; in the BTS log the same with weights 1. `r_u` is the type's sum of `w_i c_i` over its sum of `w_i q_i`, so that the residuals of a type add to zero over the week. The residual of a log in a block is the sum over its types, and the residual of the ratio is that of the random log minus that of the BTS log. `V(L)` is the sum over blocks of the squared residual of the ratio, `W(L)` the sum over blocks, logs and types of the squared residuals by type, and `G(L) = 1 - W(L) / V(L)`. Reported per length: `V`, `W`, `G`, `V(L) / V(10)`, `W(L) / W(10)`; the same within each log on its own; and the sum over blocks of the product of the two logs' residuals over the square root of the product of their sums of squares.

What D3 is for. `V` is what a block bootstrap of the ratio sees of the clicks. `G` is the share of it that comes from pairs of rows of different user types or of different logs. If such rows are independent given the click rates, these pairs add nothing to the expectation of `V`, however far the dependence within a user type reaches in time, and `G` is near 0. A click rate that moves in one log against the other, for all user types alike, adds to `V` through exactly these pairs, and `G` grows with the block length. A movement that both logs share enters the two residuals alike and leaves the ratio. `G` is a lower reading of a movement the logs do not share (the pairs within a type and log are left out; with the shares counted above they are 7% to 14% of the pairs of a log by rows) and an upper reading if users change type, or if clicks of different types or logs depend on each other for another reason. Within one log `G` also rises with a movement that both logs share.

## 3. A model fitted to the direct measurements (F)

F is scenario M of the registration with three changes.

- The excess within an impression is one per log, `e_I = max(0, e_I^)` of D1. In M it was one per campaign, solved from a ratio of standard deviations.
- Sessions are formed within a user type: an impression of type `u` gets one of `J_u` labels, `J_u` the number of impressions of the type per `T` minutes over the session size, rounded and at least 1. Offsets, windows and long groups as registered, per (type, label).
- The session size is the smallest of 5.5, 11, 22 and 44 for which the solved `e_S` does not exceed `e_I`. If none does, 44 is used and `e_S` is cut back as registered; the case is reported.

`T` and `e_S` are solved per log as in Section 5 of the registration, from the variance ratios at ten minutes and at one minute (D2 gives the published values with intervals). Everything else is as in M. The groupings use the stream `numpy.random.default_rng([20261111, 10, c, l])`.

What F is compared with. Every statistic below is computed on simulated data sets of F and set beside its real value: `e_I^` (D1) and the variance ratios at the eight lengths (D2), per log, on the first 400 data sets; the standard deviation of the replicates of the IPS ratio with impressions over rows and with ten-minute blocks over rows, and that standard deviation at 5, 20, 30, 60 and 180 minutes over the one at ten, on all data sets (their real values are published in `obd/posthoc/results/`). F reproduces a statistic if the real value lies between the 2.5th and 97.5th percentile over the simulated data sets. The report gives, per campaign, how many of these statistics F reproduces and names every one it does not. The variance ratios at 1 and 10 minutes and `e_I^` are what F was solved from; the others were not used.

## 4. Dependence beyond ten minutes against a drift the logs do not share

FH, FU and FS are built on F so that each matches the same published number, the standard deviation of the replicates of the IPS ratio at 180 minutes over the one at ten (1.134 All, 1.365 Women's, 1.029 Men's), by the expected variances of Section 5 of the registration. S matches it without any dependence. FD is a reference.

| | Built as | Solved |
|---|---|---|
| FH | F with long groups of 60 minutes within a user type | `e_L` |
| FU | F with long groups of 24 hours within a user type | `e_L` |
| FS | F with a drift of the click rate in the BTS log only | amplitude `k` |
| S | independent clicks with the drift in the BTS log only | amplitude `k` |
| FD | F with the drift of scenario D in both logs alike | nothing |

- Long groups hold three sessions on average, or the smallest of 3, 6, 12 and 24 for which the solved `e_L` does not exceed the `e_S` of either log; with 24 a cut back is reported.
- Drift. `m(t)` is the drift of scenario D in `results/calibration.json`, fitted there to the clicks of both logs by day and hour of day. In FS and S the BTS log has `q_i x (1 + k (m(t_i) - 1))`, scaled so that the sum of the click probabilities over its rows is unchanged, and the random log has `q_i`. `k` is found by bisection on `[0, k_max]`, where `k_max` keeps every probability at or above 0. If the target is not reached at `k_max`, `k_max` is used and reported. The run stops if a click probability exceeds 1. The true values are exact sums with the drifted probabilities, as in D.
- For the ratio only the movement of one log against the other counts, so the drift is put in one log. A drift of single items that both logs share, and that their different item weights do not cancel, acts on the ratio in the same way and is not simulated separately.
- S is the scenario with nothing but the drift. FD holds a movement that the logs share and none that they do not.

These scenarios say what each explanation implies for the intervals. The registered H and U gave ten-minute blocks a coverage of 0.85 and 0.83 on Women's. Under a drift the true value moves with the drift, a block bootstrap counts the movement as noise, and blocks are expected to cover at least as often as nominal, more so the longer they are.

Telling them apart. `G(180)` of D3 is computed on the real clicks and on the first 1,000 data sets of FH, FU, FD and FS.

- The range "within types" is from the smallest 2.5th percentile to the largest 97.5th percentile of `G(180)` in FH, FU and FD.
- The range "drift" is from the 2.5th to the 97.5th percentile in FS.
- A campaign is separated if the two ranges do not overlap.
- Label of a campaign: "more like a drift" if the real `G(180)` lies above the range within types and not below the range drift; "more like dependence" if it lies below the range drift and not above the range within types; otherwise "not separated", with the position stated (inside both, or outside both).

The power of this reading is limited, and that is known beforehand. With 56 blocks, `G(180)` without a movement between the logs has a standard deviation of about `sqrt(2 / 56) = 0.19`. A drift that accounts for the published widening puts it near 0.4 on Women's and near 0.2 on All. On Women's the two ranges may overlap; on All they are expected to. Where the real value falls inside both, the report says that this observable does not separate the two explanations, and gives the ranges.

Also reported, descriptive: `V(L) / V(10)`, `W(L) / W(10)` and `G(L)` at every length, for the ratio and within each log, on the real clicks and in each scenario; the published standard deviations at 20, 30 and 60 minutes over the one at ten beside their simulated ranges in FH, FU and FS.

## 5. Sensitivity of the registered scenarios

One choice of the registration is changed at a time in M and in H, and the scenario is solved again by the rule of Section 5 of the registration from the same published numbers. Groupings as registered (not within user types), with the registered streams.

| Variant | Change | Scenarios |
|---|---|---|
| half sessions | 2.75 impressions per session | M |
| double sessions | 11 impressions per session | M |
| half long groups | 1.5 sessions per long group | H |
| double long groups | 6 sessions per long group | H |
| two-level factor | a group is never off | M, H |

The two-level factor. In the registration a group is on with probability `p` and its rows click with probability `q / p`, or it is off. Here a group has the factor `1/2` or `1/2 + 1 / (2 p')`, the second with probability `p' = 1 / (1 + 4 v)`, where `1 + v` is the registered ratio `1 / p` of that grouping; a row is clicked with probability `q_i` times the product of the factors of its groups. The factor has mean 1 and variance `v`, so every marginal probability and every probability that two rows are both clicked is the registered one, and the calibration and the predicted coverage are unchanged. At each grouping about half of the clicks then come from groups at the low level. The largest probability this gives, computed from `results/calibration.json` before this file was committed, is 0.994 (All, H, BTS log); the run stops if a probability exceeds 1.

A result is robust if its labels are the registered ones in each of its variants on both campaigns: R1 and R2 in the three variants of M, R3 in the three variants of H. Otherwise it is not robust, and the cells whose label changed are reported with their coverage. A variant whose strength was cut back by the nesting is a weaker scenario than the registered one; that is reported beside its label.

Session size is not varied in H, long groups are not varied beyond a factor of two, and U is not varied. The choices are varied one at a time from the registered scenario, which costs six scenarios where the full crossing would cost ten; what two changes do together is not explored.

## 6. Simulation and reading

Units, quantities, intervals, replicates, labels and the band are those of the registration (Sections 6 and 9). Each scenario and campaign gets 4,000 data sets. Clicks of data set `s` of scenario `x` on campaign `c`: `[20261111, 11, c, x, s]`; replicates drawn afresh: `[20261111, 12, c, x, s]`; the impressions of the random log as registered, `[20261111, 3, c]`. `x`: F 0, FH 1, FU 2, FS 3, S 4, half sessions 5, double sessions 6, two-level M 7, half long groups 8, double long groups 9, two-level H 10, FD 11. Resamples of D1 and D2: `[20261111, 13, c, l, d]`, `d` 1 or 2.

Intervals are simulated for F on all three campaigns, and for FH, FS, S and the six variants of Section 5 on All and Women's. FU and FD are simulated without intervals, 1,000 data sets, for Section 4. Every scenario is solved on all three campaigns.

The calibration of the extension (the direct measurements, every parameter, every true value, the predicted coverage of every cell) is committed before any click is generated.

Confirmatory, on the IPS ratio on All and Women's:

1. Check: with the registered choices the extended code gives the parameters of `results/calibration.json` and, on the first 250 data sets of A and M on Women's, the estimates and interval ends that the code of the coverage study gives (commit `6a276af`).
2. Robustness of R1, R2 and R3 by Section 5.
3. In F: the labels of rows, impressions and the six block lengths. In FH: the label of ten-minute blocks.
4. The label of each campaign by Section 4.

What counts against the three results:

- R1 or R2 is not robust, or has another label in F. Then the result depends on a choice of the model, or does not hold at the dependence measured directly.
- R3 is not robust, or ten-minute blocks do not under-cover in FH.
- Women's is labelled "more like a drift". Then the widening on Women's is not evidence that its ten-minute intervals under-cover, and the statement of the coverage study that they are not shown to cover is read with the coverage of ten-minute blocks in FS beside it. R3 stays a statement about a scenario.

What counts for them: R1 to R3 robust and with the same labels in F and FH. "More like dependence" on Women's supports reading its widening by H; "not separated" leaves the statement of the coverage study as it is.

Everything else is descriptive: Men's, the other quantities, S, the fit of Section 3, the tables of D1 to D3. No allowance is made for the number of cells or looks.

## 7. What the extension cannot show

- That the real dependence has the structure of F. F is fitted to two kinds of second moments of each log; the size of a session is not identified by them, only its product with the strength.
- A drift apart from dependence in general. From one week, a rate that moves and a dependence that reaches across the same span leave the same trace in the second moments of a series. D3 separates them only under its assumptions: clicks of different user types, and of different logs, are independent given the rates, and a drift moves all user types alike. A drift of one user type counts as dependence within it; users who change type, or a dependence between types or between the logs, count as a drift.
- Whether a user type is a user. The features are hashed; several users share a type, and whether a user keeps a type is not known.
- Anything about a drift of another shape than the fitted `m(t)`, beyond what the ranges of Section 4 carry.
- Robustness beyond the variants of Section 5.
- The pooled unit, `rho`, `d`, H5 and H6 of the `obd` study. They are not simulated.
- One dataset and one week.

## 8. Order

1. This file.
2. Code and tests: the direct measurements against small cases with known answers; the groupings within types; the two-level factor (marginal rate and pair probability); the bisection; check 1 of Section 6.
3. The calibration of the extension, with the direct measurements.
4. The run, the results in `results/extension/`, and the reading of Section 6.

## 9. Computing

CPU only. Timed on the registered scenarios A and M with one thread, a data set with intervals takes 0.28 seconds on All and 0.18 on Women's. Ten scenarios with intervals on All and Women's and F on Men's are about 5.3 CPU hours; the variance ratios on 400 data sets of F, the data sets without intervals and the direct measurements about one hour more; on four processes about two hours. If a measured rate puts the run beyond 8 CPU hours, the variants of Section 5 are run with 2,000 data sets first, and then F on Men's is left out.

## 10. Sources

Read in the parts named; the extension borrows the points listed.

- S. Wu, C. M. Crespi, W. K. Wong, "Comparison of methods for estimating the intraclass correlation coefficient for binary responses in cancer prevention cluster randomized trials", Contemporary Clinical Trials 33(5), 2012 (author manuscript, Methods, Simulation studies, Discussion): estimators of the correlation of binary responses within clusters built from pairs; those that assume one success probability overestimate when the probabilities differ, and a moment estimator from products of residuals takes a mean per observation. D1 divides the pairs of double clicks by the pairs expected from the click probability of each row.
- A. Baddeley, J. Møller, R. Waagepetersen, "Non- and semi-parametric estimation of interaction in inhomogeneous point patterns" (research report of 1998, Sections 1 and 2): second-order statistics with every pair weighted by the inverse product of the intensities; a distinction between large-scale variation of the intensity and interaction needs prior assumptions.
- A. W. Lo, A. C. MacKinlay, "Stock market prices do not follow random walks: evidence from a simple specification test" (NBER Working Paper 2168, 1987, Section 2): a variance ratio is a linear combination of autocorrelation coefficients. Their asymptotic variance is not used; D2 resamples.
- J. M. Loh, "A valid and fast spatial bootstrap for correlation functions" (arXiv 0805.2325, Sections 1 to 5), and J. M. Loh, M. L. Stein, "Bootstrapping a spatial point process", Statistica Sinica 14, 2004 (Sections 1 and 3): for a statistic of pairs, the contribution of each point is computed once and blocks of points are resampled with their contributions. The intervals of D1 and D2 are built this way.
- A. C. Cameron, J. B. Gelbach, D. L. Miller, "Robust inference with multi-way clustering" (NBER Technical Working Paper 327, 2006, Sections 2.2 and 3.2): with errors that are correlated within a unit and within a period, the variance is the part of pairs in one unit plus the part of pairs in one period minus their overlap; the pairs of different units in one period carry the common time component. `G` of D3 is that part, with user types and logs as units and blocks as periods.
- P. J. Diggle, P. Moraga, B. Rowlingson, B. M. Taylor, "Spatial and spatio-temporal log-Gaussian Cox processes: extending the geostatistical paradigm", Statistical Science 28(4), 2013 (arXiv 1312.6536, Sections 1 and 5.2): variation in a heterogeneous environment and interaction can be difficult or impossible to distinguish empirically; a model of several types with a component common to all types.
- I. Berkes, L. Horváth, P. Kokoszka, Q.-M. Shao, "On discriminating between long-range dependence and changes in mean", Annals of Statistics 34(3), 2006 (arXiv math/0607803, Sections 1 and 2); C. W. J. Granger, N. Hyung, "Occasional structural breaks and long memory" (UCSD Discussion Paper 99-14, Sections 1, 2 and 5); F. X. Diebold, A. Inoue, "Long memory and regime switching" (NBER Technical Working Paper 264, 2000, Sections 1, 2 and 5): changes of the mean and long-range dependence produce the same autocorrelations in one series, and a test between them rests on a restriction of the form of the mean. Section 7 rests on this.
- S. Gonçalves, H. White, "The bootstrap of the mean for dependent heterogeneous arrays" (CIRANO Working Paper 2001s-19, Section 2), and K. W. Chan, "Optimal difference-based variance estimators in time series: a general framework" (arXiv 2112.15003, a preprint, Sections 1 to 3): with means that differ over time a block bootstrap variance carries an added non-negative term, which grows with the block length, and estimators built from differences do not. The expectation of Section 4 for blocks under a drift rests on this.
- T. P. Morris, I. R. White, M. J. Crowther, "Using simulation studies to evaluate statistical methods" (arXiv 1712.03198v3, Sections 3 and 8): varying factors together is more informative than one at a time from a base case, at a cost in computing; results hold for the mechanisms run.
- R. Fontana, P. Semeraro, "Characterization of multivariate Bernoulli distributions with given margins" (arXiv 1706.01357, Sections 3 to 5): binary distributions with the same margins and second moments form a family whose members differ in moments of order three and above. The two-level factor is another member of the family that the on/off factor belongs to.
- T. N. Flynn, T. J. Peters, "Use of the bootstrap in analysing cost data from cluster randomised trials: some simulation results", BMC Health Services Research 4:33, 2004 (Methods, Results, Discussion): at the same variance between clusters, the coverage of a bootstrap over clusters differed between normal and lognormal cluster means.
- S. Pawel, L. Kook, K. Reeve, "Pitfalls and potentials in simulation studies" (arXiv 2203.13076v4, Section 2 and recommendations): a changed data-generating process is reported beside the original one, and the changes are fixed beforehand.
- D. Korovaitceva, M. Sheshukova, E. Frolov, S. Samsonov, "Revisiting IPS-based algorithms for off-policy evaluation of contextual bandits", Proceedings of the ACM Web Conference 2026 (full): on the All campaign, the recorded policy of the BTS log changed during the experiment, and the dataset holds no user identifier, so that several users share a feature vector. The paper reports no interval, coverage or resampling unit. The user types of D3 are such feature vectors.

Not obtained in full, and so not used: Ridout, Demétrio and Firth (1999); Künsch (1986); Bhattacharya, Gupta and Waymire (1983); von Neumann (1941); Bartlett (1964); Lunn and Davies (1998); Emrich and Piedmonte (1991); Park, Park and Shin (1996); Qaqish (2003); Burton et al. (2006); the journal versions of Baddeley, Møller and Waagepetersen (2000) and of Lo and MacKinlay (1988). No source read uses a multiplicative group factor as Section 5 does, or reads a week of click logs by user type as D3 does; a search that finds nothing does not show that nothing exists. No new search was made for work on this dataset; the one in the README stands.
