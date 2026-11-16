# obd_rescore: published estimator comparisons against a reference unbiased for the evaluated target

Two published comparisons of off-policy estimators on the Open Bandit Dataset score each estimate against `V_on`, the click rate of the BTS log. The target they evaluate is built from the published Beta prior, which the registered study [`obd`](../README.md) found is not the policy that produced the BTS log (H1). This study re-scores both comparisons against `R_IPS`, the IPS of the same target on the whole random log, which is unbiased for the value of the target as applied (on Men's also against its SNIPS, `R_SNIPS`), as well as against `V_on`. It uses ten-minute blocks in place of rows in C1 and as the resampling of C2, and all three campaigns.

- C1, Saito and Joachims (2022): "MIPS (w/ SLOPE) outperforms IPS in about 80% of the simulation runs", on All.
- C2, Jeunen (2025), on Men's: "BLUE remains unbiased, but with significantly reduced variance"; BLUE brings the estimate "closer to V(π)" and "significantly improves estimation accuracy over existing individual estimators".

Both replications are "reproduced". Primary labels: MIPS (w/ SLOPE) against IPS on All, with ten-minute blocks and the target applied to its own (item, position) pairs, "flips" against `R_IPS` (MIPS (w/ SLOPE) closer in 91 of 500 runs); on Men's the interval of `BLUE - IPS` over 2,000 block replicates, 0.000107 to 0.000898, excludes 0, so "BLUE remains unbiased" is "contradicted" at the full size of the data, with the reward model and the target fixed. The labels describe the resampling of each protocol, with the references fixed at their full-data values.

In C1 the published code reshapes the target's distribution so that 238 of the 240 (item, position) pairs are weighted by the probability of another pair. The published target is that distribution as the code applies it; the own-pair target puts each probability on its own pair. The published target carries the replication, the own-pair target the primary label.

[`PREREGISTRATION.md`](PREREGISTRATION.md) fixes the claims, references, resampling and decision rules. It was committed (`78c077a`) before any code of the published comparisons was run on the dataset and before any estimate, reference or interval of this study was computed from it; its Section 4 lists what was seen and computed before. [`AMENDMENTS.md`](AMENDMENTS.md) holds one amendment, fixed before the run: which cells of the notebook of C2 run on the dataset.

## Results

Registered results from one run of commit `d30353f` (`python -m obd_rescore.run`, numpy 2.5.4, pandas 3.1.1), stored in [`results/`](results/) by commit `68419ea`. The run started at 08:18 UTC on 2026-11-15 and wrote its results at 21:43 UTC, with no interruption ([`results/provenance.json`](results/provenance.json), `events`). C1 has 500 runs per campaign, arm and target; C2 has 2,000 replicates of ten-minute blocks per campaign. No run or replicate was removed from any comparison, and no comparison has a tie.

### Replication

Computed before any other estimate, reference or label ([`results/replication.json`](results/replication.json)).

- C1: with the published target, row arm, on All over runs 0 to 149, MIPS (w/ SLOPE) is closer to `V_on` than IPS in 120 runs and IPS in 30: `p` = 0.80 (95% Wilson interval 0.73 to 0.86). Reproduced (`|p - 0.80| <= 0.065`).
- C2: on Men's, IPS, SNIPS, beta-IPS, DR, DM and `V_on` equal the notebook's printed values, and BLUE differs from its printed value by 1.9e-15, a relative 2.8e-13. Reproduced (relative 1e-6).

### Primary labels

| Claim | Cell | Statistic | Label |
|---|---|---|---|
| C1 | All, block arm, own-pair target, against `R_IPS` | MIPS (w/ SLOPE) closer in 91 of 500 runs, IPS in 409; `q` = 0.818 (0.782 to 0.849) | flips |
| C2 | Men's, `BLUE - IPS` over 2,000 replicates | 2.5th to 97.5th percentile 0.000107 to 0.000898 | contradicted |

### C1, every cell

Runs in which MIPS (w/ SLOPE) is closer than IPS, out of 500 (IPS is closer in the others), and the label ([`results/c1.json`](results/c1.json), [`results/labels.json`](results/labels.json)). Against the target, Men's shows `R_IPS` and `R_SNIPS` and their combined label.

| Campaign | Arm | Target | Against `V_on` | Against the target |
|---|---|---|---|---|
| All | rows | published | 400, holds | 213, flips |
| All | blocks | published | 367, holds | 274, holds |
| All | rows | own-pair | 16, flips | 52, flips |
| All | blocks | own-pair | 46, flips | 91, flips |
| Men's | rows | published | 232, undecided | 354 and 355, holds |
| Men's | blocks | published | 227, flips | 356 and 357, holds |
| Men's | rows | own-pair | 9, flips | 81 and 54, flips |
| Men's | blocks | own-pair | 57, flips | 160 and 135, flips |
| Women's | rows | published | 274, holds | 365, holds |
| Women's | blocks | published | 259, undecided | 353, holds |
| Women's | rows | own-pair | 42, flips | 39, flips |
| Women's | blocks | own-pair | 88, flips | 84, flips |

- The mean of `R_IPS,t / V_on` over runs is 0.601 (All), 0.770 (Men's) and 0.775 (Women's) with the published target, and 0.948, 0.891 and 1.005 with the own-pair target.
- On All, row arm, published target, the mean over runs of `(estimate - R_IPS,t) / V_on` is 0.065 for MIPS (w/ SLOPE) and 0.004 for IPS; against `V_on` the same means are -0.334 and -0.395. With the own-pair target they are -0.210 and 0.0005 against `R_IPS,t`, and -0.263 and -0.052 against `V_on`.
- MIPS (w/o SLOPE) in place of MIPS (w/ SLOPE), without a label, and every mean error: `c1.json`, keys `without_slope` and `mean_error_over_v_on`.
- Block runs hold 81,549 to 118,563 rows on All, 89,615 to 110,460 on Men's and 82,773 to 113,244 on Women's.

### C2, every cell

([`results/c2.json`](results/c2.json), [`results/labels.json`](results/labels.json))

| Campaign | `BLUE - IPS`, 2.5th to 97.5th percentile | Label | Distance, against `V_on` | Distance, against the target |
|---|---|---|---|---|
| All | -0.000441 to 0.000585 | not contradicted | flips | flips |
| Men's | 0.000107 to 0.000898 | contradicted | holds | flips |
| Women's | -0.000165 to 0.000362 | not contradicted | flips | flips |

Replicates in which BLUE is closer to the reference than each estimator, out of 2,000 (the estimator is closer in the others), with the label of each comparison:

| Campaign | Reference | IPS | SNIPS | beta-IPS | DR | DM |
|---|---|---|---|---|---|---|
| All | `V_on` | 783, flips | 775, flips | 775, flips | 808, flips | 2,000, holds |
| All | `R_IPS` | 561, flips | 579, flips | 582, flips | 592, flips | 1,999, holds |
| Men's | `V_on` | 1,777, holds | 1,690, holds | 1,663, holds | 1,704, holds | 1,997, holds |
| Men's | `R_IPS` | 424, flips | 340, flips | 327, flips | 338, flips | 1,564, holds |
| Men's | `R_SNIPS` | 618, flips | 518, flips | 510, flips | 520, flips | 1,866, holds |
| Women's | `V_on` | 837, flips | 849, flips | 854, flips | 849, flips | 2,000, holds |
| Women's | `R_IPS` | 883, flips | 896, flips | 895, flips | 897, flips | 2,000, holds |

Estimates on the full data (`c2.json`, `full_data`):

| Campaign | BLUE | IPS | SNIPS | beta-IPS | DR | DM | `V_on` |
|---|---|---|---|---|---|---|---|
| All | 0.0046840 | 0.0046947 | 0.0046945 | 0.0046945 | 0.0046840 | 0.0034722 | 0.0049532 |
| Men's | 0.0066877 | 0.0060110 | 0.0061273 | 0.0061520 | 0.0061190 | 0.0051271 | 0.0067427 |
| Women's | 0.0064155 | 0.0064095 | 0.0064068 | 0.0064064 | 0.0064048 | 0.0048145 | 0.0063794 |

- On the full data of Men's BLUE is closer to `V_on` than each of the five estimates, as published. On All and Women's it is closer than DM only.
- `BLUE - R_IPS` on the full data is -0.0000107 (All), 0.000677 (Men's) and 0.0000060 (Women's); `BLUE - V_on` is -0.000269, -0.000055 and 0.000036.
- `BLUE_i - V_on,i` over the replicates, 2.5th to 97.5th percentile: -0.000844 to 0.000538 (All), -0.001031 to 0.000553 (Men's), -0.000470 to 0.000746 (Women's).
- Standard deviation over the replicates: BLUE 0.000367, 0.000392 and 0.000312 on All, Men's and Women's; IPS, SNIPS, beta-IPS and DR 0.000208 to 0.000210, 0.000362 to 0.000379 and 0.000286 to 0.000288; DM 1.9e-6, 5.0e-6 and 2.6e-6.
- The resampled calls of `BLUE` receive compact inputs (departure 7 of Section 5). On the full data of every campaign, compact and full inputs give the same estimates: the difference is 0.0 for each estimator.

### References

`V_on` and the value of each target as applied, `R_IPS` as a ratio to `V_on`, with the 2.5th and 97.5th percentiles over 10,000 replicates of ten-minute blocks drawn jointly in both logs ([`results/references.json`](results/references.json); the intervals of `R_IPS` and `R_SNIPS` themselves are there too). In C1 the targets are the mean of `pi_t` over the 500 runs.

| Campaign | `V_on` | C1 published | C1 own-pair | C2 |
|---|---|---|---|---|
| All | 0.004953 (0.004876 to 0.005032) | 0.601 (0.546 to 0.661) | 0.948 (0.866 to 1.033) | 0.948 (0.867 to 1.033) |
| Men's | 0.006743 (0.006596 to 0.006893) | 0.770 (0.685 to 0.863) | 0.891 (0.789 to 1.004) | 0.891 (0.790 to 1.005) |
| Women's | 0.006379 (0.006271 to 0.006486) | 0.775 (0.705 to 0.849) | 1.005 (0.917 to 1.099) | 1.005 (0.917 to 1.099) |

On Men's, `R_SNIPS / V_on` is 0.770 (0.685 to 0.862) with the published target of C1, 0.908 (0.804 to 1.022) with the own-pair target and 0.909 (0.805 to 1.023) in C2. obp's on-policy value of Men's equals `V_on` (departure 6 of Section 5; `references.json`, `men.on_policy_value_by_obp`).

### Checks

- The stop checks of the six logs ([`results/checks.json`](results/checks.json)) found the registered row counts, items, positions and week, and stopped nothing.
- `R_IPS` and `R_SNIPS` differ from the IPS and SNIPS that BLUE returns on the full data by at most a relative 1.9e-15 (`references.json`, `stop_check_relative_differences`); the run stops above 1e-9.
- Before writing any label the run checks that obp read every row of each random log, that the rows of every block run and replicate are those of the drawn blocks, and that runs 0 to 149 of the main run repeat the replication; it stops otherwise (`run.py`).
- pandas 3.1.1 uses one converter for every `float_precision` mode. The logs are read with `"round_trip"` as registered, and a check at the start of the run found no value among 2.1 million decimal strings that any of three modes parses differently from Python's `float()` (`provenance.json`, `study.float_parsing`).

## Reading

- Section 4 of the registration expected the distance labels of C2 on Men's to be "flips" against the target and "holds" against `V_on`, which is what the run gives. It expected, before any MIPS estimate was computed, that the published 80% of C1 may hold against both references. With the own-pair target, C1 flips against both references on every campaign and arm.
- A label of "flips" against the target where the label against `V_on` in the same arm is "holds" shows that the published comparison depends on the reference. It does not show that MIPS (w/ SLOPE) is worse in general.
- "Contradicted" means that `BLUE - IPS` lies away from 0 at the 95% level of this resampling at the full size of the data, with the reward model and the target fixed. An asymptotic statement is not tested. "Not contradicted", on All and Women's, does not show that BLUE is unbiased.
- The half "with significantly reduced variance" of C2, and the part of C1 on the other estimators, have no label.

## Run it

```
obd_rescore/setup.sh ~/.cache/ope-checks/rescore    # third-party code and the three environments
~/.cache/ope-checks/rescore/envs/study/bin/python -m obd_rescore.run
```

The run downloads the dataset archive (413 MB) and verifies its SHA-256. With four processes at a time it took 13 h 25 min; the same command resumes a stopped run. `results/provenance.json` records the commits, versions, packages and file hashes it used. The tests (`pytest obd_rescore`) use synthetic logs only.

## Limits

- The labels describe the resampling of each protocol, with the references fixed at their full-data values. How they would change with another week of logs is not estimated.
- `R_IPS` differs from the value of the target by its sampling error, common to all estimators.
- In C2 the reward model is fitted once on the full data, and replicates do not include the variation of its fit.
- Intervals and block runs rest on ten-minute blocks.
- All's prior holds all 34 parameter pairs of Men's in the same order, so, by the inference of Section 7 of `obd/posthoc/`, All is not independent of Men's.

Section 10 of the registration gives every limit.
