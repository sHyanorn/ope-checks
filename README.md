# ope-checks

Pre-registered checks of published off-policy evaluation results. Each study lives in its own directory with its registration, code and results.

## obd: the shortfall on the Open Bandit Dataset

The standard benchmark on the [Open Bandit Dataset](https://research.zozo.com/data.html) estimates the click rate of the Bernoulli Thompson sampling (BTS) policy from the uniform random logs and compares it with the click rate of the BTS logs. On the Men's campaign the estimate is about 0.89 of the on-policy value. This study asks how much of that gap comes from the evaluation target: the published prior is not the policy that was deployed during the logged week.

- [`obd/PREREGISTRATION.md`](obd/PREREGISTRATION.md): the propositions, statistics and decision rules, committed before any result (`08ab8da`).
- [`obd/AMENDMENTS.md`](obd/AMENDMENTS.md): readings of the registration fixed afterwards, each before any outcome of a confirmatory campaign was computed.
- `obd/results/`: one JSON file per campaign, with every statistic, interval and label, the commit that produced it and the numpy version.

Men's is the development campaign; its results enter no verdict. All and Women's are the confirmatory campaigns.

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

- Resampled counts fall below the minimum cell count more often than the full-data counts, so the replicates of H4 use more fallback than the estimate they surround (Section 8 of the registration). The same holds for the fifteen-minute window of H5: a window is empty in a replicate when its blocks are not drawn, which leaves out about a tenth of the random rows there against 0.1% on the full data of Men's.
- A total variation distance between two resampled logs is biased upward, so the estimates of the H7 distances can lie below their own percentile intervals.
- A quantity that cannot be computed in a replicate is left out of its interval and counted under `undefined_replicates` (amendment 1).
- A converted Parquet file found in the data directory is reused; delete it to convert again from the archive.
