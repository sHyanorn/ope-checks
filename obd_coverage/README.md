# obd_coverage: do the bootstrap intervals cover?

A semi-synthetic study of the 95% intervals used in [`obd`](../README.md). The logs of the Open Bandit Dataset keep their rows (timestamps, items, positions, impressions) and get clicks from a known process, so the value of every quantity is known and the coverage of a nominal 95% interval can be counted, by resampling unit and by the kind of dependence among clicks.

Result, for the IPS ratio of the fixed-prior target over the on-policy value. With the dependence that the published statistics imply (scenario M, an upper reading of it), intervals that resample rows cover 0.866 on All and 0.846 on Women's, and intervals that resample impressions 0.880 and 0.860. Ten-minute blocks cover 0.951 on both. On Women's the published widening at 180 minutes (1.365 times the ten-minute standard deviation) exceeds what M produces (up to 1.239), so its ten-minute intervals are not shown to cover; if the widening is dependence across an hour (H) or a day (U), ten-minute blocks cover 0.850 or 0.830 there, and on All 0.907 or 0.883. The extension tests these results against variants and a drift that the two logs do not share, and leaves the label of Women's as it is.

Main limit: the strengths of the dependence are solved from published point values, and several were cut back to weaker ones (see Limits).

## Files

- [`PREREGISTRATION.md`](PREREGISTRATION.md): the click model, the scenarios, the calibration rule, the number of data sets and the reading, committed before any code (`f507c89`).
- `results/calibration.json`: the parameters, the true values and the predicted coverage of every cell, committed before any click was generated (`90f9a44`, from code `f4cddc3`).
- `results/coverage.json`: every cell and the reading; `results/cells.md`: one line per cell.
- [`EXTENSION.md`](EXTENSION.md): an extension registered afterwards (`af7e615`); its results are in [`results/extension/`](results/extension/README.md).
- [`DEPARTURES.md`](DEPARTURES.md): where the implementation settles what the registration leaves open, or departs from it.

## Design

Scenarios: A independent clicks; I dependence within an impression; M impressions and synthetic sessions of one or two minutes, at the strength solved from the published statistics; D independent clicks with a click rate that moves over the week in both logs alike; H as M with groups of sessions spanning 60 minutes; U as M with groups spanning 24 hours. Every row has the same marginal click probability in every scenario without drift.

Units: rows; impressions; clock blocks of 5 to 180 minutes with the multiplicities of `obd`. Each cell rests on 4,000 data sets and intervals of 2,000 replicates; the Monte Carlo standard error of a coverage is 0.003 near 0.95 and 0.006 near 0.85, so the third decimal is uncertain.

Labels, from the Wilson 95% interval of a coverage: adequate if it lies within 0.925 to 0.975, under-covers (-) if below 0.925, over-covers (+) if above 0.975, unresolved (?) otherwise. A cell can be adequate while its interval excludes 0.95: 83 of the 576 cells are. `results/cells.md` says for every cell whether the interval contains 0.95.

## Calibration

| Campaign | `e_I` | `T` random | `e_S` random | `T` BTS | `e_S` BTS | `e_L` 60 min | `e_L` 24 h | true IPS ratio |
|---|---|---|---|---|---|---|---|---|
| All | 40.9 | 1 | 33.6 | 2 | 25.5 | 13.7 | 25.5 (solved 88.8) | 0.9907 |
| Women's | 24.7 | 2 | 24.7 (solved 25.6) | 2 | 24.7 (solved 28.2) | 24.7 (solved 29.6) | 24.7 (solved 172.8) | 1.0017 |
| Men's | 16.2 | 2 | 16.2 (solved 31.0) | 2 | 16.2 (solved 19.4) | 0.5 | 3.5 | 0.9215 |

`e` is the excess probability that two rows are both clicked: within an impression (`e_I`), within a session (`e_S`), within a long group (`e_L`). `T` is the session span in minutes. A strength that would have exceeded the next narrower one was cut back to it, as registered; the table gives the solved value in brackets and `calibration.json` lists every case under `notes`. A campaign has one `e_L` and two `e_S`; `e_L` was cut back to the smaller of the two. Departures from the registered wording are in [`DEPARTURES.md`](DEPARTURES.md).

What the simulated data sets show of the statistics they were solved from (mean over data sets; variance ratios at 1, 10 and 60 minutes on the first 200 data sets):

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

Men's is in `results/cells.md`.

## The registered reading

The primary cells are the IPS ratio on All and on Women's; coverage is followed by its Wilson interval.

1. Check of the implementation. In A, rows are adequate on both: 0.951 (0.944 to 0.957) and 0.951 (0.944 to 0.958).
2. M. Rows under-cover: 0.866 (0.855 to 0.876) on All and 0.846 (0.834 to 0.856) on Women's. Impressions under-cover: 0.880 (0.870 to 0.890) and 0.860 (0.849 to 0.870). Ten-minute blocks are adequate: 0.951 (0.943 to 0.957) on both.
3. Shortest adequate block. In A, I, M and D it is 5 minutes on both campaigns. In H it is 180 minutes on All, and no length is adequate on Women's. In U no length is adequate on either.
4. H and U. In H ten-minute blocks under-cover, 0.907 (0.898 to 0.916) on All and 0.850 (0.838 to 0.860) on Women's; 180-minute blocks are adequate on All, 0.935 (0.927 to 0.942: the lower end is 0.002 above the bound of 0.925 and the interval excludes 0.95), and unresolved on Women's, 0.931 (0.922 to 0.938). In U ten-minute blocks under-cover, 0.883 (0.873 to 0.893) and 0.830 (0.818 to 0.841), and so do 180-minute blocks, 0.889 (0.879 to 0.899) and 0.854 (0.842 to 0.864).
5. The published widening against M. Standard deviation of the replicates of the IPS ratio over the one at ten minutes, median and 2.5th to 97.5th percentile over the data sets:

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
- A campaign flagged in item 5: Women's. Its registered ten-minute intervals are not shown to cover, and if the widening is dependence, the ten-minute labels of H and U (0.850 and 0.830) say what follows.
- No block length adequate in U: found on both campaigns. By the registration the published statistics then do not exclude a structure in which no interval of this study covers.

What the registration counts for them, ten-minute blocks adequate in M on both campaigns and no campaign flagged, holds in its first half only. H and U were tuned so that the true variance exceeds what ten-minute blocks see, so under-coverage of ten-minute blocks there was expected.

## What this says about the `obd` intervals

- With rows or impressions as resampling units, as in the public computations that `obd` cites, a nominal 95% interval of the IPS ratio covers 0.85 to 0.88 in M: the standard deviation of the replicates is 0.74 to 0.80 of that of the estimate (0.735 to 0.799 over the six cells of M in `results/cells.md`).
- On Women's the ten-minute intervals are not shown to cover. Every H3 label of `obd` is "no shortfall shown" and rests on an interval that contains 1, as do the post hoc intervals at 180 minutes. The labels that rest on an interval excluding a value or on a width (the pooled `d`, H5, the SNIPS half-width of H6) and the pooled unit were not simulated.
- No registered file, result or label of `obd` changes.

## Other results

- For the click rate of the BTS log, rows under-cover under I (0.863 on All) and impressions are adequate.
- A drift that both logs share (D) leaves the IPS ratio adequate under every unit; for the click rate of the BTS log blocks over-cover from ten minutes (0.995 on All). Without a drift (A) they over-cover at 60 and 180 minutes (0.991 and 0.998), because the true value is conditional on the kept rows and the item mix that changes between blocks counts as noise.
- Men's: in M and H every block length is adequate (0.939 to 0.948); in U every length is unresolved (0.928 to 0.933).

The other quantities, the widths and the one-sided shares are in `results/cells.md`.

## The prediction against the simulation

The calibration file predicted every coverage from second moments and a normal approximation before a click was generated. Simulated minus predicted coverage, over all campaigns, scenarios and units:

| Quantity | Cells | Prediction outside the Wilson interval | Mean of simulated minus predicted | Smallest | Largest | Cells more than 0.01 apart |
|---|---|---|---|---|---|---|
| ips_ratio | 144 | 33 | -0.004 | -0.026 | +0.010 | 18 |
| snips_ratio | 144 | 34 | -0.004 | -0.029 | +0.010 | 17 |
| ips | 144 | 38 | -0.004 | -0.027 | +0.008 | 25 |
| v_on | 144 | 42 | -0.002 | -0.018 | +0.016 | 28 |
| all | 576 | 147 | -0.004 | -0.029 | +0.016 | 88 |

The prediction lies outside the Wilson interval of the simulated coverage in 147 of 576 cells; the simulated coverage is lower by 0.004 on average and by up to 0.029 (SNIPS ratio, Women's, U, 180 minutes). In the primary cells of items 1, 2 and 4 the two lie on the same side of 0.925; the widest gaps among them are on Women's in U at 180 minutes (predicted 0.879, simulated 0.854) and in H at 180 minutes (0.943 and 0.931, unresolved).

## Extension

The extension measures the dependence of the real clicks directly, fits a scenario F to the measurements (F reproduces 16 of 25 statistics of the logs on All and 11 on Women's), sets dependence beyond ten minutes against a drift that the two logs do not share, and varies the session size, the long-group size and the group factor. On the IPS ratio on All and Women's ([`results/extension/README.md`](results/extension/README.md)):

- Three results above keep their labels in every variant: rows and impressions under-cover in M, every block length is adequate in M, ten-minute blocks under-cover in H.
- In F every block length is adequate. Rows and impressions under-cover on All (0.905 and 0.910) and are unresolved on Women's (0.922 and 0.928), where M gave 0.846 and 0.860; by the extension's registration the first result then depends on the model or does not hold at the dependence measured directly, and this is so on Women's. With the span of a session chosen at the solved `e_S`, a recomputation made after the results, they under-cover on Women's too (0.888 and 0.897).
- The widening on Women's is not attributed to dependence or to a drift. Its label "not separated" rests on one cut-back scenario; without it the label would be "more like a drift" (post hoc). Ten-minute blocks cover 0.830 under dependence across an hour and 0.960 under a drift in the BTS log, and the extension does not say which holds.
- By the block residuals of D3 the sessions of M and H join clicks of different user types, unlike the logs: the real `G` at ten minutes (0.079 on All, -0.010 on Women's) lies below its range in each of their variants (post hoc).

## Limits

- The study does not show that the real dependence has any of the structures simulated, nor which of them is behind the widening on All and Women's. A drift that the two logs do not share is simulated only in the extension. The true values are conditional on the kept rows.
- M gives all of the published variance ratio to dependence. The ratio does not separate dependence from a click rate that moves between blocks, so M is an upper reading of short-range dependence: if part of the ratio is a moving click rate, rows and impressions cover more than in M (Section 5 of the registration).
- The strengths rest on published point values without intervals, on a session size taken from one log, and on long groups of three sessions chosen without a measurement. Where a strength was cut back the scenario is weaker than the published number it was solved from: M on Women's and Men's, H on Women's, U on All and Women's, and H and U on Men's, which carry the cut-back `e_S` of M.
- No scenario reproduces every published statistic of a campaign. H overstates the dependence within the hour: its variance ratios at 60 minutes are 3.35 and 3.94 on Women's against the published 2.07 and 3.33, and 2.60 against 2.10 for the random log of All. M falls short of the published ratio of the BTS log of All at 60 minutes (1.95 against 2.61). U on Women's spans 0.842 to 1.297 for the ratio at 180 minutes and does not reach the published 1.365.
- Men's is the development campaign and enters no registered reading.
- The registration was written with the results of `obd` known. Its calibration uses numbers published in `obd/posthoc/results/`, and the click rates by item and position and the drift of D are fitted to the real clicks. With respect to `obd` the study is post hoc and descriptive.
- Prior work. A search recorded on 2026-11-11 (`6a276af`) found no study that counts the coverage of intervals for off-policy estimates on this dataset, compares resampling units on it against a known value, or generates clicks on its kept lists. It covered arXiv, the papers that Semantic Scholar lists as citing the dataset paper, OpenAlex, Crossref and the pipeline's issue list; finding nothing does not show that nothing exists. The intervals of the Open Bandit Pipeline resample rows (`obp/utils.py`, tag 0.5.5), and the dataset paper (arXiv 2008.07146v5) reports no coverage. Korovaitceva et al. (Web Conference 2026), read after the study was run, examine this dataset on the All campaign and report no interval, coverage or comparison of resampling units. Lahiri (1999), Politis and Romano (1994), Hall, Horowitz and Jing (1995), Burton et al. (2006) and Bradley (1978) were not obtained in full and are not used. The sources the design borrows from are in Section 13 of the registration.

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

Code: `model.py` (kept rows, groupings, click model, drift), `moments.py` (calibration equations, predicted coverage), `intervals.py` (replicates under the eight units), `reading.py` (coverage, Wilson interval, labels), `run.py` and `tables.py`; for the extension `direct.py` (double clicks, variance ratios, block residuals), `extension.py` and `extension_tables.py`.

The simulation keeps its progress in `~/.cache/ope-checks/coverage` (`--work-dir`) and resumes from it. The results come from one run of commit `df8019a` (numpy 2.5.3); the `code_commit` of `coverage.json` is the commit of the step `read`, and no result file records the commit that drew the data sets. The extension keeps its progress in `~/.cache/ope-checks/coverage/extension`; its data sets come from one run of commits `2e4eee4` to `af23a3c`, which do not differ in the code that generates or resamples clicks (numpy 2.5.3, four processes, one thread each).
