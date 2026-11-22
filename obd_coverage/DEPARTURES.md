# Where the implementation settles what the registration leaves open, or departs from it

These entries were collected from the READMEs of the coverage study and of its extension. Each gives the commit and the date at which it was first recorded. Unlike the `AMENDMENTS.md` files of `obd` and `obd_rescore`, this file is not a record of decisions fixed before the runs they concern. The registered texts are unchanged.

## Coverage study (`PREREGISTRATION.md`)

### Numbers of labels (2026-11-11, `6a276af`)

The calibration file does not hold the numbers of labels and sub-labels; they follow from the span and the number of impressions (`model.groupings`): 8 and 135 labels on All (random, BTS), 10 and 90 on Women's, 5 and 46 on Men's, which puts 5.3 to 5.9 impressions in a label's window.

### Expected variance of a bootstrap over rows or impressions (2026-11-11, `6a276af`)

The expected variance of a bootstrap over rows or impressions includes the squared expected contribution of each unit, which the registered wording leaves out; without it `e_I` on Men's would be 16.0 instead of 16.2.

### Choice of the span `T` (2026-11-14, `3703579`)

Section 5 chooses `T` by the ratio at one minute that the solution for `e_S` brings; the code takes that ratio with `e_S` cut back. Taken at the solved `e_S`, the ratios choose the same `T` on five of the six logs. On the random log of Men's `T` would be 3 minutes where the code took 2, with `e_S` still cut back to 16.2 (solved 34.2 instead of 31.0); the sessions of that log, `e_L` on Men's and every cell of M, H and U on Men's would change, all descriptive in this study. The closest case is the BTS log of Women's, where the ratios at the solved `e_S` lie 0.0465 (2 minutes) and 0.0471 (3 minutes) from the published 1.156. The extension chooses the span of F the same way; its entries "Session sizes" and "Recomputation with the span at the solved `e_S`" below say what taking the ratios at the solved `e_S` would change there, including the labels.

## Extension (`EXTENSION.md`)

### FU (2026-11-11, `09cf611`)

FU. Section 6 says FU is simulated without intervals, and Section 4 asks for the standard deviations of its replicates. Its 1,000 data sets got replicates; only ratios of their standard deviations are reported, and no coverage.

### Session sizes (2026-11-11, `09cf611`; the span rule and its departure 2026-11-14, `3703579`)

Session sizes. The size of a session is chosen per log, as `e_I` and `e_S` are; the size of a long group per campaign. Within each nominal size the span `T` is the one whose one-minute ratio, with `e_S` cut back, is closest to the published one, and the solved `e_S` is tested against `e_I` at that span only. Section 3 of the registration solves `T` as Section 5 of the coverage study does, by these ratios at the solved `e_S`; the choice above departs from that wording. At the solved `e_S` the random logs would take another span at the same size of 44: on All 3 minutes, with `e_S` 9.5 not cut back, instead of 1 minute with `e_S` cut back to 13.4; on Women's 3 minutes, with `e_S` still cut back to 11.1; on Men's 2 minutes. The BTS logs keep theirs.

### Recomputation with the span at the solved `e_S` (2026-11-14, `5e51db1`)

Recomputed after the results, descriptive and no part of the registered reading: F, FH, FU, FS and FD on All and Women's with these spans, the same random streams and the same numbers of data sets, the code changed in this choice only. Two confirmatory labels change: in F on Women's rows and impressions under-cover (0.888 and 0.897) where the registered run leaves them unresolved (0.922 and 0.928), so R1 would have its labels in F on both campaigns. The other labels of the registered reading stay: in F rows and impressions under-cover on All (0.878 and 0.883) and every block length is adequate on both campaigns; ten-minute blocks under-cover in FH (0.915 and 0.829); both campaigns are "not separated". `posthoc_span.json` holds the spans of both readings, every cell of F, FH and FS and the percentiles of `G(180)` beside those of the registered run, and the change to the code.

### Drift (2026-11-11, `09cf611`)

Drift. FD has the drift of scenario D as the coverage study applied it, in both logs and without rescaling, so its true values are those of D. In FS and S the probabilities of the BTS log are rescaled to their sum, as Section 4 says.

### Intervals of D2 (2026-11-11, `09cf611`)

Intervals of D2. Each log has one random stream, used for the eight block lengths in increasing order.

### Stop at a probability above 1 (2026-11-11, `09cf611`)

The stop at a probability above 1 uses an upper bound, the largest click probability of a log times the largest product of its factors, whichever groups are at the high level.

### Check 1 (2026-11-11, `09cf611`)

Check 1. The data sets are compared at a tolerance of 1e-12, because their last digits depend on the number of threads of the linear algebra; item 1 of the reading gives what was found. On the first 250 data sets of A and M on Women's the data sets are identical to the last bit when both codes run with one thread; with the extended code on four threads and the other on one, the largest difference is 1.3e-15. No result file stores this figure; it was first written in the README text added by commit `09cf611`.

### Label of a value inside one range (2026-11-11, `9b4c33b`)

A real value inside exactly one of the two ranges of Section 4 that is labelled "not separated" would be reported as outside both. This did not occur.

### Summaries of `V` and `W` (2026-11-11, `9b4c33b`)

The summaries of `V` and `W` within each log for the simulated scenarios (`ef1b885`) and the code of the tables (`af23a3c`) were committed after the calibration, while the data sets were being simulated and before any of them was read. They touch neither the clicks, the intervals nor the confirmatory reading.

### `posthoc.json` (2026-11-11, `9b4c33b`)

`posthoc.json` (the sessions of F and the largest impressions) was added after the reading. It describes the fit and one measurement and enters no reading.

### The simulation run (2026-11-11, `09cf611`)

The data sets were simulated by commits `2e4eee4` to `af23a3c`, which do not differ in the code that generates or resamples clicks, in 7.8 CPU hours on four cores; the reduction of Section 9 was not used.
