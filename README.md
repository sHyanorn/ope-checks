# ope-checks

[![CI](https://github.com/sHyanorn/ope-checks/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sHyanorn/ope-checks/actions/workflows/ci.yml?query=branch%3Amain)

Pre-registered checks of published off-policy evaluation results. The first study, `obd`, starts from the standard benchmark on the [Open Bandit Dataset](https://research.zozo.com/data.html). On the Men's campaign, the click rate of the Bernoulli Thompson sampling (BTS) policy estimated from the uniform random logs is about 0.89 of the click rate of the BTS logs. The study asks how much of that gap comes from the evaluation target, since the published prior is not the policy that was deployed in the logged week. On the two confirmatory campaigns, All and Women's, IPS of BTS under the published prior pooled over both is 0.974 of the on-policy click rate, with a 95% interval of 0.915 to 1.036. The registered rule labels it, and each campaign alone, "no shortfall shown" (H3). Men's, the campaign with the published gap, is the development campaign and enters no verdict.

## Results

Registered results from one run of commit `11e9340` (`python -m obd.run all women`, numpy 2.5.3), stored in [`obd/results/`](obd/results/) by commit `d6a1594`. Intervals are the 2.5th and 97.5th percentiles of 10,000 replicates that resample ten-minute blocks.

| | Statistic | All | Women's | Pooled (0.54, 0.46) | Label |
|---|---|---|---|---|---|
| H1 | `D` against noise floor `D0` | 0.526 against 0.136 | 0.527 against 0.115 | | inconsistent |
| H2 | mean `M` of `S` | 0.973 (0.957 to 0.990) | 0.967 (0.955 to 0.980) | | undetermined |
| H3 | IPS over on-policy | 0.948 (0.867 to 1.033) | 1.004 (0.917 to 1.099) | 0.974 (0.915 to 1.036) | no shortfall shown |
| H3 | SNIPS over on-policy | 0.948 (0.867 to 1.032) | 1.004 (0.917 to 1.099) | 0.974 (0.914 to 1.036) | no shortfall shown |
| H4 | `rho` at 3 hours | 1.031 (0.932 to 1.128) | 1.062 (0.974 to 1.158) | 1.045 (0.978 to 1.114) | not distinguishable from the on-policy value |
| H4 | `d` = `rho` - IPS ratio | 0.083 (-0.019 to 0.182) | 0.058 (-0.031 to 0.147) | 0.072 (0.002 to 0.139) | no change shown on All and Women's; raises the estimate when pooled |
| H4 | reading | | | | shortfall not established; gap not read |
| H5 | hour after minus hour before | 0.099 (0.033 to 0.166) | 0.076 (0.022 to 0.130) | | frequencies after a row are associated with clicks in the random log |
| H6 | IPS of the uniform policy over the random log's click rate | 0.990 (0.918 to 1.070) | 0.956 (0.897 to 1.019) | | consistent |
| H6 | SNIPS of the same | 0.950 (0.855 to 1.050) | 0.920 (0.819 to 1.014) | | consistent |

- H2 is undetermined because All has 3 eligible cells, fewer than the five the rule needs, and on Women's `M` lies outside [0.98, 1.02] and inside [0.95, 1.05].
- H3 shows no shortfall in any confirmatory unit, as the registration expected, so H4 reads no gap.
- H7 has no rule. The exploratory item gives no verdict: -0.013 (-0.092 to 0.063) on All and 0.050 (-0.033 to 0.132) on Women's.
- No pooled label carries the flag "campaigns differ". No quantity was undefined in any replicate.

Men's, the development campaign, from commit `581b29d` ([`men.json`](obd/results/men.json)), enters no verdict: IPS ratio 0.891 (0.790 to 1.005); `D` 0.437 against `D0` 0.109; `M` 1.005 (0.997 to 1.013) over 12 cells; `rho` 0.992 (0.853 to 1.114) and `d` 0.100 (-0.010 to 0.190) at 3 hours.

[docs/obd-results.md](docs/obd-results.md) has the full tables, `rho` and `d` at every width, and the reading of each label.

### Post hoc

Fixed after the results above were known; descriptive, with no verdict, and no registered label changes. Tables: [`obd/posthoc/`](obd/posthoc/README.md).

- Resampling unit: on Men's the H3 intervals from rows and from impressions lie below 1, and the one from ten-minute blocks contains 1. On All and Women's all three contain 1.
- Block length, with lengths committed first (`72df47d`): with blocks of 5, 10, 20, 30, 60 and 180 minutes, every H3 interval contains 1 on All, Women's and the pooled unit.
- The user feature that amendment 7 left unmatched: each log has one value of it on exactly the rows that the other three features mark. With those two values taken as one, the joint distance of the user features is 0.007 (All) and 0.009 (Women's). The registered H7 numbers stand.
- H2: `M` is below 1 with an interval that excludes 1 on 27 and 29 November on both confirmatory campaigns, and contains 1 on the other five days. The cause is not identified.

## How it works

[`obd/PREREGISTRATION.md`](obd/PREREGISTRATION.md) fixes the propositions, statistics and decision rules. It was committed before any outcome of a confirmatory campaign was computed (`08ab8da`). [`obd/AMENDMENTS.md`](obd/AMENDMENTS.md) holds readings fixed afterwards, each before any such outcome; a record of an interrupted run; and one correction written after the results, which changes no proposition, rule or result.

H1 asks whether the published prior is the deployed policy; H2 whether the BTS log's propensities are internally consistent; H3 how large the shortfall is under the fixed prior. H4, the primary proposition, matches the two logs' click rates by item, position and period, and reads the gap only where H3 finds one. H5 to H7 are secondary.

`obd/tables.py` sums both logs by ten-minute block. A bootstrap replicate rescales those tables by the blocks' multiplicities, so every frequency, count, coverage and fallback is recomputed. Each result file records the commit that produced it. The write-up is [obd/report.pdf](obd/report.pdf).

## Run it

```
pip install -e .
python -m obd.run men          # development campaign, about 4 minutes
python -m obd.run all women    # confirmatory campaigns and the pooled unit
python -m obd.posthoc.run      # post hoc analyses
python -m obd.run --check all women   # only the stop checks, which read no click
```

The first run downloads the dataset archive (413 MB) and the prior file to `~/.cache/ope-checks/obd` (`--data-dir` to change) and verifies their SHA-256. In a reproduction made outside the repository, the committed results reproduce byte for byte with numpy 2.5.3 and pandas 3.0.5; with pandas 3.1.1 some values of the development campaign differ in the last digit, and no printed number or label changes ([details](docs/obd-results.md#reproducing-with-other-pandas-versions)). `pip install -e ".[dev]"` adds `pytest` and `ruff`; the tests use synthetic logs only. `pip install -e ".[figures]"` and `python -m obd.figures.make` redraw the figures.

## Limits

- Men's, where the published gap was seen, enters no verdict. All is not a clean hold-out from it: all 34 pairs of Beta parameters of Men's occur among the 80 of All (post hoc, from the prior file).
- The intervals rest on ten-minute blocks. The post hoc analyses do not separate dependence beyond ten minutes from change over the week.
- The pooled "raises the estimate" rests on a lower end near 0, within two Monte Carlo standard errors of 0 with blocks of 20, 30 and 60 minutes (post hoc).
- `M` is below 1 on both campaigns, and Section 8 of the registration lists a downward bias of `S` in eligible cells.
- On Men's the registration quotes an IPS interval of 0.791 to 0.994 from 1,000 replicates of another random stream. The registered stream with 10,000 replicates puts the upper end above 1.
- H5 is descriptive: it cannot separate BTS learning from clicks of the random bucket from demand shared by both buckets.
- H7 cannot be read as a difference in the users of the two logs: feature 2 on All and feature 3 on Women's are still compared as written in each file. On Men's all four features were matched. The distances that the registration reports from 10,000 rows per log (0.006 to 0.018) are not reproduced when values are compared as written.
- Section 8 of the registration says `V_M` is too high if BTS learned from clicks of both buckets or follows demand that both share. A calculation written after the results, with the same click probability for the users of both logs and equal traffic profiles, finds it too low under shared demand. H5 is positive under both mechanisms, so the direction of the bias is not established. The registration is unchanged.
- Bootstrap replicates of H4 use more fallback than the estimate they surround.
- A first confirmatory run was cut off by a host restart before it produced output ("Interrupted run" in `obd/AMENDMENTS.md`).
- Before the registration, three public repositories had already estimated the BTS click rate against targets built from the BTS logs. The registration says no public source measured how much of the gap the target accounts for, and does not list them; a correction in `obd/AMENDMENTS.md` records both, and [docs/obd-results.md](docs/obd-results.md#earlier-public-work-on-the-evaluation-target) summarises what they report.
- The technical report is not peer-reviewed.

[docs/obd-results.md](docs/obd-results.md) gives the detail of each limit.

## obd_coverage

[`obd_coverage/`](obd_coverage/README.md) is a semi-synthetic study of the intervals used above: the logs keep their rows, get clicks from a known process, and the coverage of nominal 95% intervals is counted by resampling unit and kind of dependence. It changes no registered file, result or label of `obd`.

## obd_rescore

[`obd_rescore/`](obd_rescore/README.md) re-scores two published estimator comparisons on the dataset against `R_IPS`, the IPS of the evaluated target on the whole random log, which is unbiased for the target's value, as well as against `V_on`. The registration was committed before any code of the published comparisons was run on the dataset and before any estimate, reference or interval of the study was computed from it (`78c077a`); the results come from one run of commit `d30353f`. Both replications are "reproduced". Primary labels: MIPS (w/ SLOPE) against IPS on All, with ten-minute blocks and the target applied to its own (item, position) pairs, "flips" against `R_IPS` (MIPS (w/ SLOPE) closer in 91 of 500 runs); on Men's the interval of `BLUE - IPS` over 2,000 block replicates, 0.000107 to 0.000898, excludes 0, so "BLUE remains unbiased" is "contradicted" at the full size of the data, with the reward model and the target fixed. It changes no registered file, result or label of `obd`.

## Layout

`obd/` holds the study: `data.py` (download, checksums, stop checks), `tables.py`, `estimators.py` (H1 to H7 and the exploratory item), `verdicts.py` (the decision rules) and `run.py` (bootstrap, labels, result files). `obd/posthoc/` holds the post hoc analyses. `obd_rescore/` holds the re-scoring: `setup.sh` and `locks/` (the three environments), `adapters/` (one per published code), `rules.py` (the decision rules) and `run.py` (the run and its result files). MIT licence.
