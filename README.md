# ope-checks

Pre-registered checks of published off-policy evaluation results. Each study lives in its own directory with its registration, code and results.

## obd: the shortfall on the Open Bandit Dataset

The standard benchmark on the [Open Bandit Dataset](https://research.zozo.com/data.html) estimates the click rate of the Bernoulli Thompson sampling (BTS) policy from the uniform random logs and compares it with the click rate of the BTS logs. On the Men's campaign the estimate is about 0.89 of the on-policy value. This study asks how much of that gap comes from the evaluation target: the published prior is not the policy that was deployed during the logged week.

- [`obd/PREREGISTRATION.md`](obd/PREREGISTRATION.md): the propositions, statistics and decision rules, committed before any result (`08ab8da`).
- [`obd/AMENDMENTS.md`](obd/AMENDMENTS.md): readings of the registration fixed afterwards, each before any outcome of a confirmatory campaign was computed.
- `obd/results/`: one JSON file per campaign, with every statistic, interval and label, the commit that produced it and the numpy version.

Men's is the development campaign; its results enter no verdict. All and Women's are the confirmatory campaigns.

### Results

Every number below comes from one run of commit `11e9340` (`python -m obd.run all women`, numpy 2.5.3) and is stored in `obd/results/` as written by that run (commit `d6a1594`). Intervals are the 2.5th and 97.5th percentiles of 10,000 replicates that resample ten-minute blocks. A first attempt at the run was cut off by a host restart before it produced any output; see "Interrupted run" in [`obd/AMENDMENTS.md`](obd/AMENDMENTS.md).

| | All | Women's | Pooled (0.54, 0.46) |
|---|---|---|---|
| Items; rows of the random and BTS logs | 80; 1,374,327 and 12,357,200 | 46; 864,585 and 7,765,497 | |
| On-policy click rate of BTS | 0.004953 (0.004876 to 0.005032) | 0.006379 (0.006271 to 0.006486) | |
| **H1** `D`; noise floor `D0` | 0.526; 0.136 | 0.527; 0.115 | |
| H1 label | inconsistent | inconsistent | |
| **H2** eligible cells; with 1 in their interval | 3; 1 | 7; 4 | |
| H2 mean `M` of `S` | 0.973 (0.957 to 0.990) | 0.967 (0.955 to 0.980) | |
| H2 label | undetermined | undetermined | |
| **H3** IPS over on-policy | 0.948 (0.867 to 1.033) | 1.004 (0.917 to 1.099) | 0.974 (0.915 to 1.036) |
| H3 IPS label | no shortfall shown | no shortfall shown | no shortfall shown |
| H3 SNIPS over on-policy | 0.948 (0.867 to 1.032) | 1.004 (0.917 to 1.099) | 0.974 (0.914 to 1.036) |
| H3 SNIPS label | no shortfall shown | no shortfall shown | no shortfall shown |
| **H4** width used; coverage `C(W)` there | 3 hours; 0.9985 | 3 hours; 0.9992 | 3 and 3 hours |
| H4 `rho` | 1.031 (0.932 to 1.128) | 1.062 (0.974 to 1.158) | 1.045 (0.978 to 1.114) |
| H4 level | not distinguishable from the on-policy value | not distinguishable from the on-policy value | not distinguishable from the on-policy value |
| H4 `d` = `rho` - IPS ratio | 0.083 (-0.019 to 0.182) | 0.058 (-0.031 to 0.147) | 0.072 (0.002 to 0.139) |
| H4 alignment | no change shown | no change shown | raises the estimate |
| H4 reading | shortfall not established; gap not read | shortfall not established; gap not read | shortfall not established; gap not read |
| **H5** hour after minus hour before | 0.099 (0.033 to 0.166) | 0.076 (0.022 to 0.130) | |
| H5 label | frequencies after a row are associated with clicks in the random log | frequencies after a row are associated with clicks in the random log | |
| **H6** IPS of the uniform policy over the random log's click rate | 0.990 (0.918 to 1.070), consistent | 0.956 (0.897 to 1.019), consistent | |
| H6 SNIPS | 0.950 (0.855 to 1.050), consistent | 0.920 (0.819 to 1.014), consistent | |

No pooled label carries the flag "campaigns differ". No quantity was undefined in any replicate.

H4 at every width, each with the fallback applied from that width, and the two IPS forms of the aligned target:

| | All | Women's |
|---|---|---|
| `rho`, 1 h | 1.016 (0.911 to 1.106) | 1.083 (0.980 to 1.190) |
| `rho`, 3 h | 1.031 (0.932 to 1.128) | 1.062 (0.974 to 1.158) |
| `rho`, 6 h | 1.028 (0.935 to 1.117) | 1.058 (0.972 to 1.147) |
| `rho`, 24 h | 1.017 (0.944 to 1.091) | 1.018 (0.945 to 1.093) |
| `d`, 1 h | 0.068 (-0.046 to 0.163) | 0.079 (-0.028 to 0.178) |
| `d`, 3 h | 0.083 (-0.019 to 0.182) | 0.058 (-0.031 to 0.147) |
| `d`, 6 h | 0.080 (-0.016 to 0.168) | 0.053 (-0.030 to 0.133) |
| `d`, 24 h | 0.069 (-0.006 to 0.142) | 0.013 (-0.057 to 0.081) |
| `rho` - SNIPS ratio, 1 h | 0.068 (-0.045 to 0.163) | 0.079 (-0.027 to 0.179) |
| `rho` - SNIPS ratio, 3 h | 0.084 (-0.019 to 0.182) | 0.058 (-0.029 to 0.147) |
| `rho` - SNIPS ratio, 6 h | 0.080 (-0.014 to 0.167) | 0.053 (-0.028 to 0.134) |
| `rho` - SNIPS ratio, 24 h | 0.069 (-0.004 to 0.141) | 0.014 (-0.055 to 0.079) |
| IPS form at the width used | 1.047 (0.948 to 1.152) | 1.093 (1.001 to 1.194) |
| IPS with whole-week BTS frequencies | 1.017 (0.949 to 1.087) | 1.006 (0.939 to 1.077) |
| BTS rows resolved by fallback at the width used: full data; mean over replicates | 0.0015; 0.0049 | 0.0008; 0.0033 |
| BTS rows dropped | 0.0000 | 0.0000 |

What the labels say and do not say:

- H1: on both campaigns `D` exceeds 0.10 and twice `D0`. The distance of the first hour of the week by position is 0.180, 0.126, 0.088 (All); 0.164, 0.098, 0.105 (Women's).
- H2: undetermined on both campaigns. All has 3 eligible cells, fewer than the five the rule needs. On Women's `M` lies outside [0.98, 1.02] and inside [0.95, 1.05], and 4 of 7 cell intervals contain 1. `M` is below 1 on both; Section 8 of the registration lists a downward bias of `S` in eligible cells.
- H3: no shortfall is shown in any confirmatory unit, as the registration expected. On the development campaign the IPS ratio is 0.891 (0.790 to 1.005): Section 3 of the registration quotes 0.791 to 0.994 from 1,000 replicates of another random stream; the registered stream and 10,000 replicates put the upper end above 1.
- H4: because H3 found no shortfall, the gap is not read in any unit. The aligned estimate is not distinguishable from the on-policy value in any unit. The paired change from the fixed-prior IPS is positive in every unit and at every width; its interval excludes 0 only in the pooled unit.
- H5: on both campaigns the target built from the hour after a row gives a higher estimate than the one built from the hour before. The registration calls this descriptive: it cannot separate BTS learning from clicks of the random bucket from demand shared by both buckets. Ratios to the on-policy value, fifteen minutes before, hour before, hour after: 1.004, 1.002, 1.101 (All); 1.068, 1.036, 1.124 (Women's).
- H6: estimating the uniform policy from the BTS log with its recorded propensities is consistent with the random log's click rate for both estimators on both campaigns. Kish's effective sample size is 19,910 and 6,009; rows with a propensity below 0.001 carry 39% and 29% of the weight.
- H7 has no rule. Amendment 7 matched the value written differently in the two files for three of the four user features on each campaign; feature 2 on All and feature 3 on Women's did not meet its condition and are compared as written. On these two campaigns the joint distance (0.360, 0.236), the share of BTS rows whose combination is absent from the random log (0.353, 0.228) and the change in `rho` under user weights (-0.058 (-0.136 to 0.013), -0.116 (-0.178 to -0.063)) therefore still contain the difference in how the files write that value. They cannot be read as a difference in the users of the two logs. The distances of the three matched features are 0.001, 0.001, 0.002 (All); 0.001, 0.001, 0.003 (Women's). On Men's all four features were matched and the change in `rho` is -0.001 (-0.007 to 0.004). The distances that Section 3 of the registration reports from 10,000 rows per log (0.006 to 0.018) are not reproduced when values are compared as written.
- Exploratory item, no verdict: -0.013 (-0.092 to 0.063) on All and 0.050 (-0.033 to 0.132) on Women's.

Development campaign (Men's, `obd/results/men.json`, from commit `581b29d`; enters no verdict): `D` 0.437 against `D0` 0.109; H2 `M` 1.005 (0.997 to 1.013) over 12 cells; IPS ratio 0.891 (0.790 to 1.005); `rho` 0.992 (0.853 to 1.114) and `d` 0.100 (-0.010 to 0.190) at 3 hours.

### Post hoc analyses

These were fixed after the results above were known. They are descriptive, give no verdict, and replace or reinterpret no registered label. Code, result files and full tables are in [`obd/posthoc/`](obd/posthoc/README.md); `python -m obd.posthoc.run` reruns them.

- Resampling unit. On all three campaigns the standard deviation of the H3 ratios with ten-minute blocks is 1.31 to 1.47 times the one with rows or impressions as resampling units. On All and Women's the interval of each ratio contains 1 under all three units. On Men's the intervals from rows and from impressions lie below 1 and the one from blocks contains 1. On All and Women's 30% to 36% of complete impressions show the same list as the one before, as on Men's (31%, 37%).
- The feature that amendment 7 left unmatched. On each confirmatory campaign the BTS log holds one more value of that feature that the random log lacks, on 30 rows (All) and 14 rows (Women's). The other value of each log sits on exactly the rows that the matched values of the other three features mark. With those two taken as one value, the joint distance of the user features is 0.007 (All) and 0.009 (Women's), and the change in `rho` under user weights is 0.001 (-0.003 to 0.005) and -0.001 (-0.014 to 0.005). The registered H7 numbers stand as registered.
- H2. At the registered bound `M` is 0.027 (All) and 0.033 (Women's) below 1. The upward bias of `S` that Section 8 names is about +0.0002. Hours in which an eligible cell is shown at under a tenth of the rate its recorded propensities imply hold 0.033 of that distance on All and 0.022 on Women's, against 0.002 on Men's, where `M` is 1.005. On All and Women's nearly all of it falls on 27 and 29 November, the two days on which `M` is below 1 with an interval that excludes 1; on the other five days the interval contains 1. Such hours are what the downward bias of Section 8 would leave. The logs do not show what was served in them, and the cause is not identified.
- Block length. The lengths and the reading were committed before this one was run (`72df47d`). With clock blocks of 5, 10, 20, 30, 60 and 180 minutes as resampling units, the interval of each H3 ratio contains 1 at every length on All, Women's and the pooled unit. On Men's the SNIPS interval contains 1 at every length and the IPS interval at every length but 30 minutes, where its upper end is 0.9997; the standard deviation of the ratios stays within 3% of the one at ten minutes. On All and Women's it is larger at every longer length, at 1.07 and 1.12 times the one at ten minutes at 60 minutes and 1.13 and 1.36 times at 180 minutes (IPS), where an interval rests on 56 blocks. The pooled IPS interval is 0.915 to 1.036 at ten minutes and 0.897 to 1.056 at 180 minutes. The analysis does not separate dependence beyond ten minutes from change over the week.
- Further intervals by block length. The quantities and the reading were committed before this one was run (`02eb3da`). With the same block lengths, the interval of `rho` contains 1 in every unit at every length, and the interval of `d` contains 0 on All and on Women's at every length. The lower end of the pooled `d`, on which the label "raises the estimate" rests, lies between 0.001 and 0.004 at the six lengths; at 20, 30 and 60 minutes it is within two Monte Carlo standard errors of 0. The half-width of the H6 SNIPS interval is 0.093 to 0.102 against the bound of 0.10, and within two of its errors of the bound at 30 and 60 minutes on All and at 20, 30 and 60 minutes on Women's. The H5 difference lies above 0 at 5, 10 and 20 minutes on both campaigns; on Women's its lower end is within two errors of 0 at 30 minutes; its interval contains 0 at 60 minutes on both and at 180 minutes on Women's. A remark made with the results and not part of the reading: with long blocks the replicates leave out rows that H5 needs, to an extent that was not measured. The registered labels stand.
- Three distances that read no click. The quantities and the reading were committed before this one was run (`02eb3da`). The frequencies of the whole week are 0.386 (All) and 0.413 (Women's) from the prior, against a reference of 0.012 and 0.010 between alternate blocks. The hourly frequencies are 0.410 and 0.394 from those of the whole week, 3.0 and 3.4 times `D0`; in the random logs of the three campaigns, whose policy is fixed, the same distance is 0.52 to 0.55 of `D0`. By the thresholds of the registered rule, and without an interval, the hourly frequencies of the BTS log thus differ from those of the whole week. The registered label of H1 stands; the distances bound `D` (0.386 <= 0.526 <= 0.796 on All) and do not say how much of it is change. In the first hour of the week the distance from the prior is at most its own noise floor at five of nine positions over the three campaigns and between the floor and twice the floor at the other four; that hour is one hour with one split.

### Reproduce

```
pip install -e .
python -m obd.run men          # development campaign, about 4 minutes
python -m obd.run all women    # confirmatory campaigns and the pooled unit
```

The first run downloads the dataset archive (413 MB) and the prior file to `~/.cache/ope-checks/obd` (`--data-dir` to change) and verifies their SHA-256. Every run starts with the stop checks of Section 2 of the registration, which read no click; `python -m obd.run --check all women` runs only those.

### Code

| File | Content |
|---|---|
| `obd/data.py` | download, checksums, stop checks, conversion to Parquet |
| `obd/tables.py` | sums over the rows of both logs by ten-minute block |
| `obd/estimators.py` | the fixed-prior target, H1 to H7 and the exploratory item as functions of the tables |
| `obd/verdicts.py` | the decision rules |
| `obd/run.py` | bootstrap over blocks, labels, pooled unit, result files |

A bootstrap replicate rescales the block tables by the multiplicities of the blocks and calls the same estimators, so every frequency, count, coverage and fallback is recomputed in it.

`pip install -e ".[dev]"` adds `pytest` and `ruff`. The tests use synthetic logs only.

### Notes on the bootstrap

These follow from the registered method and are visible in the result files.

- Resampled counts fall below the minimum cell count more often than the full-data counts, so the replicates of H4 use more fallback than the estimate they surround (Section 8 of the registration; the table above gives both shares). The same holds for the fifteen-minute window of H5: a window is empty in a replicate when its blocks are not drawn. On All it leaves out 0.16% of the random rows on the full data and 8.6% to 14.6% in replicates; on Women's 0.15% and 8.5% to 14.6%. That estimate enters no rule.
- A total variation distance between two resampled logs is biased upward, so an estimate of an H7 distance can lie below its own percentile interval. The distance of the hourly shares of rows is 0.0091 (0.0105 to 0.0129) on All and 0.0111 (0.0127 to 0.0159) on Women's.
- A quantity that cannot be computed in a replicate is left out of its interval and counted under `undefined_replicates` (amendment 1).
- A converted Parquet file found in the data directory is reused; delete it to convert again from the archive.

### Figures

`obd/figures/` holds three figures, each for a light and a dark page: the IPS ratio of H3 under three resampling units (post hoc), the registered IPS ratio of H3 and `rho` of H4 on the confirmatory campaigns, and the distances of H1. They are drawn from the result files in `obd/results/` and `obd/posthoc/results/`. To redraw them:

```
pip install -e ".[figures]"
python -m obd.figures.make
```

`python -m obd.figures.make --pdf --out DIR` writes each figure once, as a vector PDF on a white page. The test is skipped where matplotlib is not installed.
