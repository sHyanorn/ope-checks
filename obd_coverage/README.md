# obd_coverage: do the bootstrap intervals cover?

A semi-synthetic study of the intervals used in [`obd`](../README.md). The logs of the Open Bandit Dataset keep their rows (timestamps, items, positions, impressions) and get clicks from a known process, so the value of every quantity is known and the coverage of a nominal 95% interval can be counted, by resampling unit and by the kind of dependence among clicks.

- [`PREREGISTRATION.md`](PREREGISTRATION.md): the click model, the scenarios, the calibration rule, the number of data sets and the reading, committed before any code (`f507c89`).
- `results/calibration.json`: the parameters, the true values and the predicted coverage of every cell, committed before any click was generated (`90f9a44`, from code `f4cddc3`).
- `results/coverage.json`: every cell and the reading; `results/cells.md`: one line per cell.
- [`EXTENSION.md`](EXTENSION.md): an extension registered afterwards (`af7e615`); its results are in [`results/extension/`](results/extension/README.md) and summarised below.

The registration was written with the results of `obd` known. Its calibration uses numbers published in `obd/posthoc/results/`, and the click rates by item and position and the drift of scenario D are fitted to the real clicks.

## Design in brief

Scenarios: A independent clicks; I dependence within an impression; M impressions and synthetic sessions of one or two minutes, at the strength solved from the published statistics; D independent clicks with a click rate that moves over the week in both logs alike; H as M with groups of sessions spanning 60 minutes; U as M with groups spanning 24 hours. Every row has the same marginal click probability in every scenario without drift.

Units: rows; impressions; clock blocks of 5 to 180 minutes with the multiplicities of `obd`. Each cell rests on 4,000 data sets and intervals of 2,000 replicates. A coverage near 0.95 has a Monte Carlo standard error of 0.003, one near 0.85 of 0.006. Coverages are printed to three decimals, one more than that error carries; the third is uncertain.

Labels, from the Wilson 95% interval of a coverage: adequate if it lies within 0.925 to 0.975, under-covers (-) if below 0.925, over-covers (+) if above 0.975, unresolved (?) otherwise. A cell can be adequate while its interval excludes 0.95: 83 of the 576 cells are. `results/cells.md` says for every cell whether the interval contains 0.95.

## Calibration

| Campaign | `e_I` | `T` random | `e_S` random | `T` BTS | `e_S` BTS | `e_L` 60 min | `e_L` 24 h | true IPS ratio |
|---|---|---|---|---|---|---|---|---|
| All | 40.9 | 1 | 33.6 | 2 | 25.5 | 13.7 | 25.5 (solved 88.8) | 0.9907 |
| Women's | 24.7 | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) | 24.7 (solved 29.6) | 24.7 (solved 172.8) | 1.0017 |
| Men's | 16.2 | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) | 0.5 | 3.5 | 0.9215 |

`e` is the excess probability that two rows are both clicked: within an impression (`e_I`), within a session (`e_S`), within a long group (`e_L`). `T` is the session span in minutes. A strength that would have exceeded the next narrower one was cut back to it, as registered; the table gives the solved value in brackets and `calibration.json` lists every case under `notes`. Where a strength was cut back the scenario is weaker than the published number it was solved from: M on Women's and Men's, H on Women's, U on All and Women's. A campaign has one `e_L` and two `e_S`; `e_L` was cut back to the smaller of the two.

M gives all of the published variance ratio to dependence. The ratio does not separate dependence from a click rate that moves between blocks, so M is an upper reading of short-range dependence (Section 5 of the registration).

Four departures from the wording of the registration in this section; the fourth is in the next paragraph. The calibration file does not hold the numbers of labels and sub-labels; they follow from the span and the number of impressions (`model.groupings`): 8 and 135 labels on All (random, BTS), 10 and 90 on Women's, 5 and 46 on Men's, which puts 5.3 to 5.9 impressions in a label's window. The expected variance of a bootstrap over rows or impressions includes the squared expected contribution of each unit, which the registered wording leaves out; without it `e_I` on Men's would be 16.0 instead of 16.2. The variance ratios at 60 minutes below rest on 200 data sets and have a Monte Carlo standard error of 0.01 to 0.04, those at ten minutes of at most 0.011.

Section 5 chooses `T` by the ratio at one minute that the solution for `e_S` brings; the code takes that ratio with `e_S` cut back. Taken at the solved `e_S`, the ratios choose the same `T` on five of the six logs. On the random log of Men's `T` would be 3 minutes where the code took 2, with `e_S` still cut back to 16.2 (solved 34.2 instead of 31.0); the sessions of that log, `e_L` on Men's and every cell of M, H and U on Men's would change, all descriptive in this study. The closest case is the BTS log of Women's, where the ratios at the solved `e_S` lie 0.0465 (2 minutes) and 0.0471 (3 minutes) from the published 1.156. The extension chooses the span of F the same way; what taking the ratios at the solved `e_S` would change there is in [`results/extension/README.md`](results/extension/README.md).

What the simulated data sets show of the statistics they were solved from (mean over data sets; variance ratios at 1, 10 and 60 minutes on the first 200):

| Campaign |  | random 1 | 10 | 60 | BTS 1 | 10 | 60 | impressions / rows | blocks / rows |
|---|---|---|---|---|---|---|---|---|---|
| All | A | 1.00 | 1.00 | 0.99 | 1.00 | 1.00 | 1.05 | 1.000 | 1.02 |
| All | M | 1.34 | 1.89 | 1.97 | 1.14 | 1.84 | 1.95 | 1.046 | 1.32 |
| All | H | 1.33 | 1.90 | 2.60 | 1.14 | 1.83 | 2.74 | 1.046 | 1.36 |
| All | U | 1.34 | 1.89 | 1.98 | 1.15 | 1.84 | 1.97 | 1.046 | 1.33 |
| All | published | 1.29 | 1.89 | 2.10 | 1.14 | 1.85 | 2.61 | 1.046 | 1.37 |
| Women's | A | 1.01 | 1.00 | 1.01 | 1.00 | 1.00 | 1.03 | 1.000 | 1.02 |
| Women's | M | 1.15 | 1.87 | 1.98 | 1.18 | 2.07 | 2.23 | 1.034 | 1.35 |
| Women's | H | 1.13 | 1.82 | 3.35 | 1.16 | 2.04 | 3.94 | 1.034 | 1.45 |
| Women's | U | 1.16 | 1.89 | 1.98 | 1.17 | 2.08 | 2.20 | 1.034 | 1.36 |
| Women's | published | 1.13 | 1.92 | 2.07 | 1.16 | 2.23 | 3.33 | 1.034 | 1.45 |
| Men's | A | 1.00 | 0.99 | 1.00 | 1.00 | 1.01 | 0.99 | 1.000 | 1.01 |
| Men's | M | 1.17 | 1.76 | 1.87 | 1.17 | 1.90 | 2.02 | 1.025 | 1.30 |
| Men's | H | 1.17 | 1.77 | 1.89 | 1.17 | 1.90 | 2.04 | 1.025 | 1.30 |
| Men's | U | 1.18 | 1.75 | 1.87 | 1.17 | 1.90 | 2.02 | 1.025 | 1.30 |
| Men's | published | 1.18 | 2.45 | 2.07 | 1.20 | 2.08 | 2.02 | 1.025 | 1.47 |

M reproduces the published ratio of impressions to rows on every campaign and the ten-minute variance ratios on All; at one minute the random log of All gives 1.34 against 1.29. On Women's its ten-minute ratios are 1.87 and 2.07 against 1.92 and 2.23, on Men's 1.76 and 1.90 against 2.45 and 2.08. With ten-minute blocks over rows it gives 1.32, 1.35 and 1.30 against the published 1.37, 1.45 and 1.47.

## Results: the IPS ratio

Simulated coverage, its label if not adequate, and after the slash the coverage predicted in the calibration file.

All:

| Scenario | rows | impressions | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| A | 0.951 / 0.951 | 0.952 / 0.951 | 0.955 / 0.955 | 0.953 / 0.955 | 0.953 / 0.955 | 0.955 / 0.956 | 0.952 / 0.956 | 0.950 / 0.957 |
| I | 0.947 / 0.940 | 0.956 / 0.951 | 0.959 / 0.954 | 0.959 / 0.954 | 0.958 / 0.955 | 0.960 / 0.955 | 0.957 / 0.955 | 0.952 / 0.956 |
| M | 0.866 (-) / 0.862 | 0.880 (-) / 0.879 | 0.948 / 0.949 | 0.951 / 0.951 | 0.953 / 0.952 | 0.953 / 0.952 | 0.951 / 0.953 | 0.950 / 0.954 |
| D | 0.947 / 0.951 | 0.947 / 0.951 | 0.948 / 0.954 | 0.948 / 0.955 | 0.950 / 0.955 | 0.952 / 0.956 | 0.947 / 0.956 | 0.944 / 0.957 |
| H | 0.779 (-) / 0.794 | 0.804 (-) / 0.814 | 0.900 (-) / 0.909 | 0.907 (-) / 0.915 | 0.916 (-) / 0.924 | 0.922 (?) / 0.931 | 0.931 (?) / 0.942 | 0.935 / 0.949 |
| U | 0.768 (-) / 0.768 | 0.786 (-) / 0.788 | 0.882 (-) / 0.885 | 0.883 (-) / 0.888 | 0.885 (-) / 0.891 | 0.887 (-) / 0.892 | 0.889 (-) / 0.895 | 0.889 (-) / 0.905 |

Women's:

| Scenario | rows | impressions | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| A | 0.951 / 0.951 | 0.953 / 0.951 | 0.955 / 0.954 | 0.954 / 0.955 | 0.954 / 0.955 | 0.954 / 0.955 | 0.954 / 0.956 | 0.948 / 0.956 |
| I | 0.950 / 0.943 | 0.958 / 0.951 | 0.960 / 0.954 | 0.961 / 0.954 | 0.961 / 0.955 | 0.960 / 0.955 | 0.960 / 0.956 | 0.956 / 0.956 |
| M | 0.846 (-) / 0.850 | 0.860 (-) / 0.863 | 0.950 / 0.946 | 0.951 / 0.949 | 0.953 / 0.951 | 0.952 / 0.952 | 0.951 / 0.953 | 0.945 / 0.953 |
| D | 0.946 / 0.951 | 0.948 / 0.951 | 0.951 / 0.954 | 0.951 / 0.955 | 0.949 / 0.955 | 0.951 / 0.955 | 0.952 / 0.956 | 0.951 / 0.957 |
| H | 0.680 (-) / 0.679 | 0.696 (-) / 0.695 | 0.830 (-) / 0.829 | 0.850 (-) / 0.851 | 0.876 (-) / 0.879 | 0.893 (-) / 0.897 | 0.919 (?) / 0.925 | 0.931 (?) / 0.943 |
| U | 0.701 (-) / 0.710 | 0.718 (-) / 0.726 | 0.821 (-) / 0.844 | 0.830 (-) / 0.851 | 0.835 (-) / 0.855 | 0.837 (-) / 0.858 | 0.839 (-) / 0.864 | 0.854 (-) / 0.879 |

Men's (descriptive):

| Scenario | rows | impressions | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| A | 0.949 / 0.951 | 0.950 / 0.951 | 0.952 / 0.954 | 0.952 / 0.954 | 0.951 / 0.955 | 0.951 / 0.955 | 0.949 / 0.955 | 0.945 / 0.956 |
| I | 0.944 / 0.945 | 0.949 / 0.951 | 0.949 / 0.954 | 0.951 / 0.954 | 0.952 / 0.954 | 0.951 / 0.955 | 0.948 / 0.955 | 0.945 / 0.956 |
| M | 0.863 (-) / 0.866 | 0.875 (-) / 0.875 | 0.942 / 0.946 | 0.944 / 0.949 | 0.948 / 0.951 | 0.947 / 0.952 | 0.946 / 0.952 | 0.941 / 0.953 |
| D | 0.948 / 0.951 | 0.947 / 0.951 | 0.950 / 0.954 | 0.952 / 0.954 | 0.952 / 0.955 | 0.951 / 0.955 | 0.946 / 0.955 | 0.946 / 0.956 |
| H | 0.855 (-) / 0.860 | 0.865 (-) / 0.869 | 0.939 / 0.943 | 0.941 / 0.946 | 0.943 / 0.948 | 0.942 / 0.950 | 0.943 / 0.951 | 0.939 / 0.953 |
| U | 0.843 (-) / 0.836 | 0.856 (-) / 0.846 | 0.928 (?) / 0.927 | 0.928 (?) / 0.930 | 0.932 (?) / 0.933 | 0.933 (?) / 0.934 | 0.932 (?) / 0.935 | 0.930 (?) / 0.938 |

## The registered reading

The primary cells are the IPS ratio on All and on Women's. Coverage is followed by its Wilson interval.

1. Check of the implementation. In A, rows are adequate on both: 0.951 (0.944 to 0.957) and 0.951 (0.944 to 0.958).
2. M. Rows under-cover: 0.866 (0.855 to 0.876) on All and 0.846 (0.834 to 0.856) on Women's. Impressions under-cover: 0.880 (0.870 to 0.890) and 0.860 (0.849 to 0.870). Ten-minute blocks are adequate: 0.951 (0.943 to 0.957) on both.
3. Shortest adequate block. In A, I, M and D it is 5 minutes on both campaigns, and every longer length is adequate. In H it is 180 minutes on All, and no length is adequate on Women's. In U no length is adequate on either. The label on All in H at 180 minutes is a narrow one: see item 4.
4. H and U. In H ten-minute blocks under-cover, 0.907 (0.898 to 0.916) on All and 0.850 (0.838 to 0.860) on Women's; 180-minute blocks are adequate on All, 0.935 (0.927 to 0.942), with an interval that excludes 0.95 and ends 0.002 above the bound, and unresolved on Women's, 0.931 (0.922 to 0.938). In U ten-minute blocks under-cover, 0.883 (0.873 to 0.893) and 0.830 (0.818 to 0.841), and so do 180-minute blocks, 0.889 (0.879 to 0.899) and 0.854 (0.842 to 0.864).
5. The published widening against M. This item is post hoc and descriptive with respect to `obd`; it uses published numbers only and changes no registered label. Standard deviation of the replicates of the IPS ratio over the one at ten minutes, median and 2.5th to 97.5th percentile over the data sets:

| Campaign | Scenario | 60 min: simulated | published | 180 min: simulated | published |
|---|---|---|---|---|---|
| All | M | 1.004 (0.887 to 1.138) | 1.069 | 0.998 (0.805 to 1.217) | 1.134 |
| All | H | 1.093 (0.965 to 1.235) | 1.069 | 1.121 (0.895 to 1.372) | 1.134 |
| All | U | 1.014 (0.891 to 1.143) | 1.069 | 1.027 (0.820 to 1.259) | 1.134 |
| Women's | M | 1.007 (0.885 to 1.136) | 1.123 | 0.995 (0.801 to 1.239) | 1.365 |
| Women's | H | 1.225 (1.081 to 1.385) | 1.123 | 1.293 (1.033 to 1.605) | 1.365 |
| Women's | U | 1.024 (0.904 to 1.159) | 1.123 | 1.050 (0.842 to 1.297) | 1.365 |
| Men's | M | 1.009 (0.889 to 1.144) | 1.007 | 1.002 (0.799 to 1.233) | 1.029 |
| Men's | H | 1.020 (0.897 to 1.151) | 1.007 | 1.017 (0.810 to 1.253) | 1.029 |
| Men's | U | 1.012 (0.894 to 1.146) | 1.007 | 1.014 (0.805 to 1.240) | 1.029 |

On All the published ratios, 1.069 at 60 minutes and 1.134 at 180, lie below the 97.5th percentile of M (1.138 and 1.217). On Women's the ratio at 60 minutes, 1.123, lies below it (1.136) and the ratio at 180 minutes, 1.365, lies above it (1.239). Women's is flagged.

What the registration counts against the ten-minute intervals of `obd`:

- Ten-minute blocks under-cover in M: not found on either campaign.
- A campaign flagged in item 5: Women's. The widening of its intervals up to 180 minutes is more than the short-range dependence of M produces, and its registered ten-minute intervals are not shown to cover. If the widening is dependence, the ten-minute labels of H and U say what follows: coverage of 0.850 in H and 0.830 in U.
- No block length adequate in U: found on both campaigns. By the registration the published statistics then do not exclude a structure in which no interval of this study covers.

What the registration counts for them, ten-minute blocks adequate in M on both campaigns and no campaign flagged, holds in its first half only.

H and U were tuned so that the true variance exceeds what ten-minute blocks see. That ten-minute blocks under-cover there was expected and is no finding by itself.

Not part of the registered reading: how well H and U fit the published numbers they were not solved from. On Women's, H was cut back; its ratio of standard deviations at 180 minutes spans 1.033 to 1.605 over the data sets, which contains the published 1.365, but at 60 minutes its median is 1.225 against the published 1.123, and its variance ratios at 60 minutes are 3.35 and 3.94 against the published 2.07 and 3.33. H therefore overstates the dependence within the hour on Women's. U was cut back on All and Women's; its ratio at 180 minutes spans 0.820 to 1.259 on All, which contains the published 1.134, and 0.842 to 1.297 on Women's, which does not reach 1.365. On All the published variance ratio of the BTS log at 60 minutes, 2.61, is above the 1.95 of M and close to the 2.74 of H. None of the scenarios reproduces every published statistic of a campaign.

## What this says about the `obd` intervals

- With rows or impressions as resampling units, as in the public computations that `obd` cites, a nominal 95% interval of the IPS ratio covers 0.85 to 0.88 in M: the standard deviation of the replicates is 0.74 to 0.80 of that of the estimate. M is an upper reading of short-range dependence; if part of the published variance ratio is a moving click rate, rows and impressions cover more than this.
- On All no registered criterion against ten-minute blocks is met other than the statement on U.
- On Women's the ten-minute intervals are not shown to cover. Every H3 label of `obd` is "no shortfall shown" and rests on an interval that contains 1; the post hoc intervals at 180 minutes contain 1 as well. The labels of `obd` that rest on an interval excluding a value or on a width (the pooled `d`, H5, the SNIPS half-width of H6) and the pooled unit were not simulated here.
- No registered file, result or label of `obd` changes.

## Descriptive results

- I. For the IPS ratio rows are adequate (0.947 on All, 0.950 on Women's). For the click rate of the BTS log they under-cover (0.863 and 0.899) and impressions are adequate.
- D. A drift that both logs share leaves the IPS ratio adequate under every unit. For the click rate of the BTS log, blocks over-cover: 0.986 at 5 minutes and 0.995 at ten on All, 1.000 from 30 minutes.
- Without any drift (A), blocks over-cover for the click rate of the BTS log at 60 and 180 minutes on All (0.991 and 0.998): the true value is conditional on the kept rows, and the change of the item mix between blocks counts as noise in the bootstrap.
- Men's. In M and H every block length is adequate (0.939 to 0.948); in U every length is unresolved (0.928 to 0.933). M is weaker there than the published ten-minute variance ratio of the random log.

Click rate of the BTS log on All:

| Scenario | rows | impressions | 5 min | 10 min | 20 min | 30 min | 60 min | 180 min |
|---|---|---|---|---|---|---|---|---|
| A | 0.951 / 0.950 | 0.950 / 0.950 | 0.959 / 0.958 | 0.965 / 0.965 | 0.975 (?) / 0.974 | 0.980 (?) / 0.981 | 0.991 (+) / 0.992 | 0.998 (+) / 0.999 |
| I | 0.863 (-) / 0.874 | 0.942 / 0.950 | 0.949 / 0.955 | 0.952 / 0.959 | 0.961 / 0.967 | 0.967 / 0.972 | 0.980 (?) / 0.983 | 0.994 (+) / 0.996 |
| M | 0.627 (-) / 0.637 | 0.751 (-) / 0.756 | 0.933 / 0.941 | 0.940 / 0.949 | 0.948 / 0.954 | 0.948 / 0.958 | 0.957 / 0.966 | 0.970 / 0.981 |
| D | 0.953 / 0.950 | 0.952 / 0.950 | 0.986 (+) / 0.983 | 0.995 (+) / 0.994 | 0.999 (+) / 0.999 | 1.000 (+) / 1.000 | 1.000 (+) / 1.000 | 1.000 (+) / 1.000 |
| H | 0.489 (-) / 0.482 | 0.599 (-) / 0.593 | 0.821 (-) / 0.833 | 0.847 (-) / 0.859 | 0.877 (-) / 0.889 | 0.894 (-) / 0.908 | 0.930 (?) / 0.939 | 0.954 / 0.965 |
| U | 0.446 (-) / 0.439 | 0.553 (-) / 0.544 | 0.781 (-) / 0.775 | 0.794 (-) / 0.790 | 0.804 (-) / 0.804 | 0.814 (-) / 0.814 | 0.833 (-) / 0.838 | 0.874 (-) / 0.892 |

The other quantities, the widths, the one-sided shares and the coverage of the mean estimate are in `results/cells.md`.

## The prediction against the simulation

The calibration file predicted every coverage from second moments and a normal approximation before a click was generated. Simulated minus predicted coverage, over all campaigns, scenarios and units:

| Quantity | Cells | Prediction outside the Wilson interval | Mean of simulated minus predicted | Smallest | Largest | Cells more than 0.01 apart |
|---|---|---|---|---|---|---|
| ips_ratio | 144 | 33 | -0.004 | -0.026 | +0.010 | 18 |
| snips_ratio | 144 | 34 | -0.004 | -0.029 | +0.010 | 17 |
| ips | 144 | 38 | -0.004 | -0.027 | +0.008 | 25 |
| v_on | 144 | 42 | -0.002 | -0.018 | +0.016 | 28 |
| all | 576 | 147 | -0.004 | -0.029 | +0.016 | 88 |

The prediction lies outside the Wilson interval of the simulated coverage in 147 of 576 cells; the simulated coverage is lower by 0.004 on average and by up to 0.029 (SNIPS ratio, Women's, U, 180 minutes). In the primary cells of items 1, 2 and 4 the prediction and the simulated coverage lie on the same side of 0.925. The widest gap among them is on Women's in U at 180 minutes, predicted 0.879 and simulated 0.854; in H at 180 minutes on Women's the prediction is 0.943 and the simulated coverage 0.931, which is unresolved.

## What the study cannot show

Section 10 of the registration. In short: it does not show that the real dependence has any of these structures, nor which of them is behind the widening on Women's; a drift that the two logs do not share was not simulated; the true values are conditional on the kept rows; the strengths rest on published point values without intervals, on a session size taken from one log, and on long groups of three sessions chosen without a measurement.

## Extension

The extension measures the dependence of the real clicks directly, fits a scenario F to those measurements, sets dependence beyond ten minutes against a drift that the two logs do not share, and varies the session size, the size of the long groups and the shape of the group factor. It changes no file, result or label above. On the IPS ratio on All and Women's ([`results/extension/README.md`](results/extension/README.md)):

- Three results above keep their labels in every variant: in M rows and impressions under-cover; in M every block length is adequate; in H ten-minute blocks under-cover.
- In F every block length is adequate. Rows and impressions under-cover on All (0.905 and 0.910) and are unresolved on Women's (0.922 and 0.928), where M gave 0.846 and 0.860; the registration of the extension counts the other label on Women's against the first of the three results. F reproduces 16 of 25 statistics of the logs on All and 11 on Women's, and on no campaign the published ratio of ten-minute blocks to rows.
- The widening on Women's is not attributed. The registered observable does not separate dependence beyond ten minutes from a drift in one log. On Women's its label rests on one scenario that was cut back; without it the label would have been "more like a drift". In the scenario with dependence across an hour (FH) ten-minute blocks cover 0.830 on Women's, and in the one with a drift in the BTS log (FS) 0.960. The statement above that the ten-minute intervals on Women's are not shown to cover stands.
- The sessions of M and H join clicks of different user types. By the block residuals of the extension the logs differ from them in this: the share of the block variance of the ratio that comes from pairs of rows of different user types or logs is 0.079 on All and -0.010 on Women's at ten minutes, below its range in each of the six variants of M and H (2.5th percentiles of 0.150 and above). It was not computed for M and H themselves; the two variants with the two-level factor have their groupings and strengths.

## Earlier work

A search found no study that counts the coverage of intervals for off-policy estimates on this dataset, compares resampling units on it against a known value, or generates clicks on its kept lists. It covered arXiv, the papers that Semantic Scholar lists as citing the dataset paper, OpenAlex and Crossref, and the issue list of the pipeline's repository, with the name of the dataset combined with coverage, bootstrap, resampling unit, block or cluster bootstrap, A/A test, semi-synthetic and i.i.d., and off-policy evaluation combined with clustered, dependent or non-stationary data. The intervals of the Open Bandit Pipeline resample rows (`obp/utils.py`, tag 0.5.5), and the dataset paper (arXiv 2008.07146v5) reports no coverage. The simulations of interval coverage for off-policy estimates that were read draw independent rounds. A search that finds nothing does not show that nothing exists. Korovaitceva et al. (Web Conference 2026), read in full after the study was run, examine this dataset on the All campaign: a recorded propensity of the BTS log that changes during the week, chi-square tests of the random log against uniformity, and the absence of a user identifier. They report no interval for an estimate on the dataset, no coverage and no comparison of resampling units. Not obtained in full, and so not used: Lahiri (1999), Politis and Romano (1994), Hall, Horowitz and Jing (1995), Burton et al. (2006), Bradley (1978). The sources the design borrows from are in Section 13 of the registration.

## Reproduce

```
pip install -e .
python -m obd_coverage.run check       # the block code against the published intervals of obd
python -m obd_coverage.run calibrate   # results/calibration.json
python -m obd_coverage.run simulate    # about 4 CPU hours; --scenarios and a campaign name run a part
python -m obd_coverage.run read        # results/coverage.json
python -m obd_coverage.tables          # the tables above and results/cells.md

python -m obd_coverage.extension check       # the registered parameters, with the extended code
python -m obd_coverage.extension calibrate   # results/extension/calibration.json; reads the clicks
python -m obd_coverage.extension simulate    # about 8 CPU hours; --scenarios and a campaign name run a part
python -m obd_coverage.extension read        # results/extension/coverage.json
python -m obd_coverage.extension posthoc     # results/extension/posthoc.json; descriptive, not registered
python -m obd_coverage.extension_tables      # the tables of results/extension/
```

The simulation keeps its progress in `~/.cache/ope-checks/coverage` (`--work-dir`) and continues from there. The results come from one run of commit `df8019a` (numpy 2.5.3). The extension keeps its progress in `~/.cache/ope-checks/coverage/extension`; its data sets come from one run of commits `2e4eee4` to `af23a3c`, which do not differ in the code that generates or resamples clicks (numpy 2.5.3, four processes with one thread each).

| File | Content |
|---|---|
| `model.py` | kept rows, synthetic groupings, the click model, the drift |
| `moments.py` | second moments: calibration equations and predicted coverage |
| `intervals.py` | replicates under the eight resampling units |
| `reading.py` | coverage, Wilson interval, labels |
| `run.py` | calibration, simulation, the registered reading |
| `tables.py` | tables from the result files |
| `direct.py` | the extension: double clicks, variance ratios with intervals, block residuals by log and user type |
| `extension.py` | the extension: calibration, simulation, the registered reading |
| `extension_tables.py` | the extension: tables from its result files |
