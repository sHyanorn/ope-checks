# Pre-registration: the shortfall of off-policy estimates of the BTS click rate on the Open Bandit Dataset

## 1. Question

The Open Bandit Dataset (OBD) holds one week of logs from two policies on ZOZOTOWN, uniform random and Bernoulli Thompson sampling (BTS), in three campaigns. The standard benchmark estimates the BTS click rate from the random logs and compares it with the click rate of the BTS logs. With the BTS target computed the way the Open Bandit Pipeline does it (Monte Carlo draws from the published Beta prior, no updates), the estimate on the full Men's campaign is about 0.89 of the on-policy value. Two public reproductions agree (Section 3). The published Men's intervals exclude 1, but they resample rows or impressions. Clicks cluster in time, and with ten-minute blocks as resampling units the Men's interval is 0.79 to 0.99, its upper end within simulation noise of 1 (Section 3). Whether the shortfall exists on the other two campaigns is therefore part of the question. Issue #208 of the pipeline (October 2026, unanswered) reports that logged propensities of the All campaign do not match the published prior and asks whether the comparison is valid. No public source measures how much of the gap this accounts for.

This study asks how much of the gap comes from the evaluation target: the published prior is not the policy that was deployed during the logged week. It does not ask why the two differ.

## 2. Data and fixed inputs

- Archive: `https://research.zozo.com/data_release/open_bandit_dataset.zip`, 412,931,917 bytes, sha256 `e8ec18196582a5937381a1776382ca940689b90a18d2dcd1fb635be6df614d78`, CC BY 4.0, version file "08/18/2020 Open Bandit Dataset 1.0".
- Six log files, `{random,bts}/{all,men,women}`, used as released. Rows: random 1,374,327 / 452,949 / 864,585; BTS 12,357,200 / 4,077,727 / 7,765,497. Three positions.
- Prior: `obp/policy/conf/prior_bts.yaml` of `st-tech/zr-obp` at commit `8cbd5fa4558b7ad2ba4781546d6604e4cc3e07c4`, sha256 `81a54fbdc184021ccc62ab97de81ec35461c032e3d7f99ccaa0a9745f732d251`. It lists 80 / 34 / 46 items.
- Columns used: `timestamp`, `item_id`, `position`, `click`, `propensity_score`, `user_feature_0` to `user_feature_3`.
- The run of a campaign stops and reports it if a row count differs from the one above, if an item id lies outside 0 to (number of items in the prior) - 1, if a row of the random log has a propensity that differs from 1/(number of items) by more than 1e-9, or if more than 0.1% of the rows of a file lie outside the week.
- The week is 2019-11-24 to 2019-11-30 UTC, the span of the Men's logs. Rows outside it, if any, are counted, reported and left out of every quantity.

## 3. What was seen before this registration

Everything below was known when the rules were written.

Men's campaign, outcomes with impressions as resampling units (`sHyanorn/push-lab`, `results/ope_obd.json` as of commit 823046b; an impression there is a run of rows less than one second apart with the same user features):
- On-policy BTS click rate 0.006743 (0.006649 to 0.006831).
- Fixed-prior target, ratio to on-policy: IPS 0.891 (0.815 to 0.966), SNIPS 0.908 (0.830 to 0.985), DR 0.897 (0.824 to 0.975), DM 0.881 (0.868 to 0.895). The ratio of IPS to SNIPS is the mean weight, 0.981.
- Target equal to the BTS log's whole-week (item, position) frequencies: IPS 0.917 (0.848 to 0.989); paired change from the fixed prior +0.026 (-0.004 to 0.059).
- Earlier exploratory numbers, not reproduced and without committed code: target from the 15 minutes before each row 0.933 (0.844 to 1.022); targets from the same hour or one to two hours later 1.058 to 1.070.

Men's campaign, structure only (the click column was not read):
- BTS log: 99.96% of recorded propensities are multiples of 1/200,000; the smallest is 0.000001; 1,488 rows equal 1/34. About 850 distinct values per (item, position) over the week. Of the changes of value within an (item, position), 59% return to the value before the previous one, within seconds: several parameter versions were served at the same time. Mean of 1/propensity by position: 34.30, 44.19, 33.87 (expected 34); the second is driven by a few rows at 0.000001.
- Impressions: 147,487 in the random log and 1,268,311 in the BTS log; 96% and 88% of them are one row at each of the three positions.
- Served lists are reused. In the random log 37% of consecutive impressions show the same three items in the same order (0.003% expected under independent uniform draws); in the BTS log 31%. Counting repeats of a list less than two minutes apart as one list leaves 25,759 lists for 142,227 impressions (random) and 132,730 for 1,121,295 (BTS). Chi-square over degrees of freedom of the random log's item counts against uniform is 6.9 across hours and 11.0 over the week.
- H1 on Men's: `D = 0.438`. The noise floor is 0.034 from a random half split of impressions and 0.109 from alternating ten-minute blocks. Distance of the first hour by position: 0.147, 0.095, 0.068.
- H2 on Men's: 12 of 102 cells have a smallest propensity of at least 0.001; the mean of `S` over them is 1.005. The share of their intervals that contain 1 is 58% with impressions as resampling units and 100% with ten-minute blocks (300 replicates). With a bound of 0.0001, 90 cells, mean 0.973, 88%.
- H4 coverage on Men's: `C(1) = 0.977` and `C(3) = 1.000` with `m = 1`; 0.949 and 0.999 with `m = 5`; 0.875 and 0.994 with `m = 10`.
- The hourly ratio of BTS rows to random rows ranges from 7.9 to 10.1.

Men's campaign, dependence of clicks (click column read):
- The variance of the difference in click rate between adjacent time blocks, over the variance implied by treating impressions as independent, is 1.2 to 1.5 for one-minute blocks and 2.0 to 2.5 for blocks of ten minutes or more, in both logs, and the same after subtracting each (item, position) click rate.
- In the random log a click is followed by another click with the same user features 20 times per second of delay between 10 and 60 seconds later, against 2.3 at ten minutes and beyond (summed over the 2,321 clicks); in the BTS log 526 against 285. Impressions with the same user features are about 1.5 times as frequent in the ten minutes after a clicked impression as after any impression.
- Fixed-prior ratios with time blocks as resampling units, drawn jointly in both logs (1,000 replicates): IPS 0.891 (0.791 to 0.994), SNIPS 0.908 (0.806 to 1.012), mean weight 0.981 (0.969 to 0.994), on-policy value 0.006743 (0.006588 to 0.006897). The standard deviation of the IPS ratio is 0.052 to 0.054 for blocks of 5, 10, 20, 30 and 60 minutes and 0.038 with impressions; the upper end of the IPS interval is 0.994 to 1.006 across those block lengths. The block length of ten minutes (Section 5) was chosen after seeing these numbers.

All three campaigns: row counts of the six files (Section 2). `bts/all` has 189,116 more rows than Table 1 of the paper; the other five match.

Small sample (10,000 rows per log, Men's): total variation distance between the two logs of each user feature, 0.006 to 0.018, no test.

Public record on the deployed policy:
- The pipeline describes the prior as the one "used at the start of the data collection period" (`contextfree.py`). Its documentation, and a footnote of versions 2 and 3 of the paper, say that BTS was pre-trained for over a month and "converges to a fixed one"; versions 4 and 5 of the paper do not have the sentence.
- Paper, version 5, footnote 4: the action choice probabilities were computed "by Monte Carlo simulations based on the policy parameters [...] used during the data collection process".
- ZOZO tech blog (2020): parameters of the context-free bandit are updated periodically from aggregated logs and served data are versioned; no interval is given.

Public reports on the confirmatory campaigns:
- Saito et al. (2021), Table 9, RMSE x 10^3 of Random to BTS: All, IPW 0.474, SNIPW 0.468, DM 1.499, DR 0.501; Women's, IPW 1.645, SNIPW 1.585, DM 0.584, DR 1.539. Table 1: BTS click rate 0.50% (All), 0.64% (Women's); random 0.35%, 0.48%.
- `RollinsE/open-bandit-ab-testing` (2026): lowest relative error among its estimators, All 6.7%, Men's 9.3%, Women's 2.2%; the estimated lift is described as below the measured one for All and Men's and as matching it for Women's.
- `lyftium/off-policy-bandit-evaluation` (2026): All, IPW 0.004692 (0.004382 to 0.005022) against 0.004953, 5.3% low; the interval contains the reference.
- Issue #208: on All, the fixed prior gives item 61 a probability of about 0.198 at the first position where the first row records 0.104925; values alternate within seconds; some rows record exactly 1/80.
- Jeunen (2025), notebook `BLUE OPE.ipynb`: Men's, IPW 0.006011 (0.005612 to 0.006472) against 0.006743.

No quantity that uses clicks of the All or Women's logs has been computed by this project. Of those four files only the row counts have been read. On Men's, `V_M` has not been computed at any width.

## 4. Sample roles

- Men's is the development campaign. Code is written and checked on it. Its results enter no verdict.
- All and Women's are the confirmatory campaigns. Verdicts come from them only. Nothing is computed from their four files, beyond the row counts and the checks of Section 2, until the code for every proposition of Sections 6 and 7 has been run on Men's and committed. The confirmatory results of all propositions come from one run of that commit.
- No setting is tuned after registration. Three settings were fixed from click-free quantities of Men's (Section 3): coverage threshold `tau = 0.99` and minimum cell count `m = 5` in H4, eligibility bound `p_min = 0.001` in H2. The block length of the bootstrap and the thresholds of H1 were fixed with the Men's results of Section 3 in view.
- Verdict units: All and Women's for every proposition; for H3 and H4 also the two pooled. A pooled quantity is `0.54 x (All) + 0.46 x (Women's)`, applied to ratios to the on-policy value and to their differences. The weights are the shares of expected clicks in the two random logs computed from Table 1 of the paper (0.35% x 1,374,327 and 0.48% x 864,585). The pooled labels are primary, and the labels of each campaign are always shown with them. A pooled label carries the flag "campaigns differ" if the interval of All minus Women's excludes 0 for the quantity behind it: the IPS or SNIPS ratio for H3, `rho` or `d` (defined in H4) for H4. No flag does not show that the campaigns agree. A campaign that is not evaluable for H4 gets no H4 label or reading, and then there is no pooled H4 label; H3 labels are unaffected.

## 5. Definitions

- `n_A`: number of items. `k`: position. `h`: the UTC clock hour of a row's timestamp, 168 in the week. Ten-minute block: the UTC clock interval of ten minutes containing the timestamp, 1,008 in the week, numbered from 0 at 2019-11-24 00:00.
- `R`, `B`: the random and BTS logs of a campaign. `N_B(.)`, `N_R(.)`: row counts in a cell.
- On-policy value: `V_on = mean click over B`.
- Fixed-prior target `pi0(a|k)`: 1,000,000 draws; each draw samples every item's `Beta(alpha, beta)` from the prior file, and the items with the largest, second and third largest samples go to positions 1, 2 and 3. `pi0(a|k)` is the share of draws that put item `a` at position `k`. It is computed once per campaign.
- Bootstrap: 10,000 replicates. The resampling units are the 1,008 ten-minute blocks. A replicate draws 1,008 blocks with replacement, and a block carries the rows of every log that fall in it: `R` and `B` are resampled together, and so are All and Women's in a pooled quantity. A row in a block drawn `c` times counts `c` times in every sum and count, including the counts compared with `m`, and keeps its timestamp, hour and period (H4). Everything is recomputed from the resampled logs: frequencies of `B`, counts, coverage, fallbacks, estimates and `V_on`. These stay as fixed on the full data: `pi0`, the width `W` of H4, the eligible cells of H2, and the impressions and medians of the exploratory item.
- Why blocks: lists are reused across impressions for up to a few minutes and clicks cluster over a few minutes (Section 3), so neither rows nor impressions are independent. On Men's the width of the intervals is the same for blocks of 5 to 60 minutes. The data have no user id.
- Intervals are the 2.5th and 97.5th percentiles of the replicates (linear interpolation). A difference between two estimates is computed within each replicate.
- Random streams. Block multiplicities of replicate `i` (0 to 9,999), the same for every campaign: `numpy.random.default_rng([20261110, 0, i]).multinomial(1008, numpy.full(1008, 1/1008))`. Prior draws of campaign `c` (all 0, men 1, women 2): `numpy.random.default_rng([20261110, 1, c]).beta(alpha, beta, size=(1_000_000, n_A))`, rows in order. Element `j` of a multiplicity vector belongs to block `j`. The numpy version is recorded with the results.

## 6. Main propositions

### H1. The published prior is not the deployed policy

- Statistic: `D = sum over (h, k) of [N_B(h,k)/N_B] x TV(f_h(.|k), pi0(.|k))`, where `f_h(a|k) = N_B(h,a,k)/N_B(h,k)` and TV is half the L1 distance over the `n_A` items.
- Noise floor `D0`: the same sum with `pi0` replaced by the frequencies of the rows of `B` in the first, third and fifth ten-minute blocks of the hour and `f_h` by those of the second, fourth and sixth. An `(h, k)` with no row in one of the halves is left out of `D` and `D0` alike and the weights renormalised; the share left out is reported. Whole blocks are split because lists are reused: a random split of rows or impressions puts copies of one list in both halves and understates the noise.
- Under a fixed policy equal to `pi0`, `D` is about half of `D0`: `D0` compares two half samples, `D` one full sample with a fixed distribution.
- Rule: "inconsistent" if `D > 0.10` and `D > 2 x D0`; "not distinguishable from variation within the hour" if `D <= D0`; otherwise "undetermined". The middle label is not a finding that the prior was the deployed policy.
- Also reported, no rule: TV between `pi0` and the frequencies of hour 0 of the week, since the pipeline describes the prior as the one used at the start of collection; and `D` and `D0` of the random log against the uniform distribution, a case where the policy is known.
- Uses no clicks.

### H2. The recorded propensities of the BTS log are internally consistent

- Identity: if a row's recorded propensity is the probability with which its item was chosen at its position, then for every (item, position) `S(a,k) = [sum over rows of B with item a at position k of 1/propensity] / N_B(k)` has expectation 1. In a replicate both the sum and `N_B(k)` are recomputed.
- Eligible cells: the (item, position) cells that have at least one row in the full log and no row there with a recorded propensity below `p_min = 0.001`, so that no single row dominates.
- Rule, with `n` eligible cells and `M` the mean of `S(a,k)` over them: "undetermined" if `n < 5`. Otherwise "consistent" if `M` lies in [0.98, 1.02] and at least `ceil(0.9 n)` cells have an interval containing 1; "inconsistent" if `M` lies outside [0.95, 1.05] and the interval of `M` has no point in [0.98, 1.02]; otherwise "undetermined".
- Reported with it: the number of eligible cells and their share of rows, the unrestricted mean of 1/propensity per position, the number of rows below 0.00001 and of rows off the 1/200,000 grid.
- Uses no clicks.

### H3. Size of the shortfall under the fixed prior

- Estimators on `R` with weights `w = n_A x pi0(a|k)`: IPS `mean(w x click)` and SNIPS `sum(w x click)/sum(w)`. Ratio: estimate over `V_on`.
- Rule per unit and estimator: "low" if the interval of the ratio lies below 1; "high" if above; otherwise "no shortfall shown".
- Reported with it, no rule: the mean weight `mean(w)` with its interval. It is 1 in expectation if the random log is uniform, and it is the ratio of IPS to SNIPS.
- From the public numbers of Section 3, "no shortfall shown" is the likely result in every confirmatory unit. That was known at registration.
- DR is not run on All or Women's (cost of an outcome model over 80 items); the Men's DR result above stands as it is.

### H4. Aligning the target with the deployed policy (primary)

- Periods: runs of `W` clock hours aligned to UTC midnight, `W` in {1, 3, 6, 24}, and above them the whole week. A cell is a period `b`, an item and a position.
- Matched estimate: `V_M = sum over cells (b, a, k) of [N_B(b,a,k)/N_B] x c_R(b,a,k)`, where `c_R` is the click rate of the rows of `R` with the same item and position in the same period. It uses no propensity. When every cell is covered, `V_on - V_M` equals the sum over cells of the BTS share times the difference between the two logs' click rates in that cell.
- Coverage: a cell is covered if `N_R(b,a,k) >= m`, with `m = 5`. `C(W)` is the share of the rows of `B` in covered cells. The width used is the smallest `W` with `C(W) >= tau = 0.99`, compared without rounding, or 24 if none reaches it; it is chosen per campaign from the full data. Coverage is computed from counts only.
- Fallback: a cell that is not covered at the width used takes `c_R` from the narrowest wider level (3, 6, 24 hours, whole week) whose period containing it has at least `m` rows of `R` with its item and position. A cell with fewer than `m` such rows in the whole week is dropped and the shares renormalised over the cells kept. The run reports `C(W)` for every width and the share of BTS rows resolved at each level and dropped. If more than 0.1% of the rows of `B` are dropped on the full data, the campaign is "not evaluable" for H4.
- In a bootstrap replicate the width stays as chosen on the full data; counts, coverage and the fallback are recomputed from the resampled logs. A cell with no row of `B` in the replicate has no weight.
- Quantities: `rho = V_M / V_on` with interval `[L, U]`; `d = rho - (IPS ratio of H3)` with interval `[dL, dU]`.
- Two labels per unit, whatever H3 found:
  - Alignment: "raises the estimate" if `dL > 0`; "lowers the estimate" if `dU < 0`; otherwise "no change shown". It compares two estimates: `V_M` does not depend on how often the random log shows each item, IPS does.
  - Level: "below the on-policy value" if `U < 1`; "above the on-policy value" if `L > 1`; otherwise "not distinguishable from the on-policy value". Below or above means: matched on item, position and period, the two logs' click rates differ by `1 - rho` of the on-policy value, stated with its interval.
- Reading of the gap, only in a unit where H3 found IPS "low" (for the pooled unit, the pooled IPS ratio); elsewhere "shortfall not established; gap not read":

| Alignment | Level | Reading |
|---|---|---|
| raises | not distinguishable | Gap shrinks; the residual `1 - rho` cannot be told from zero and is at most `1 - L`. Never "fully explained" |
| raises | below | Gap shrinks; a residual remains |
| no change shown or lowers | below | Alignment is not shown to reduce the gap |
| any | above | Aligned estimate exceeds the on-policy value |
| no change shown or lowers | not distinguishable | Cannot be determined; interval widths and the gap that could have been detected are stated |

- A pooled statement names the width used in each campaign.
- Reported with it, no rule, so that the path from the fixed prior to the aligned target is shown in steps:
  - `rho` and `d` at every width, each with the fallback applied from that width, with intervals; `rho` minus the SNIPS ratio; the median of the replicates of `rho` and the mean share of rows of `B` resolved by fallback in replicates;
  - the same target in IPS form, `sum over (b, k) of [N_B(b,k)/N_B] x mean over rows of R in (b, k) of n_A x f_b(a|k) x click`, with `f_b(a|k) = N_B(b,a,k)/N_B(b,k)` at the width used; a `(b, k)` with no row of `R` or of `B` is left out and the weights renormalised;
  - IPS with the whole-week frequencies of `B` as target, `mean over R of n_A x N_B(a,k)/N_B(k) x click`.

## 7. Secondary propositions

Verdict units: All and Women's.

- H5, direction in time. The IPS form of H4 at one hour, `sum over (h, k) of [N_B(h,k)/N_B] x mean over rows of R in (h, k) of n_A x g(a|k) x click`, where the frequencies `g` of `B` at position `k` are taken from (i) the fifteen-minute clock interval before the one that contains the row, (ii) the clock hour before the row's hour, (iii) the clock hour after it. A row whose window holds no row of `B` at its position is left out of that estimate; the difference (iii) minus (ii) uses only rows that have both windows; an `(h, k)` left without rows is dropped and the weights renormalised. Estimates are reported as ratios to `V_on`, with the shares of rows left out on the full data. Rule: "frequencies after a row are associated with clicks in the random log" if the interval of (iii) minus (ii) lies above 0; "the reverse" if it lies below; otherwise "not shown". This cannot separate BTS learning from clicks of the random bucket from demand shared by both buckets, and is descriptive.
- H6, reverse direction. From `B` with recorded propensities `p` and weights `w = 1/(n_A x p)`, IPS `mean(w x click)` and SNIPS `sum(w x click)/sum(w)` of the uniform policy, as ratios to the click rate of `R`. Rule per estimator: "off" if the interval of the ratio excludes 1; "consistent" if it contains 1 and its half-width is at most 0.10; otherwise "undetermined". Kish's effective sample size `(sum w)^2 / sum(w^2)`, the largest weight, and the shares of `sum(w)` and of `sum(w x click)` that come from rows with `p < 0.001` are reported. A row with a very large weight enters IPS only if it was clicked and enters the denominator of SNIPS either way, so "off" on the low side can occur with correct propensities and is not read as evidence against them; H2 is the test of the recorded propensities.
- H7, comparability of the logs. TV distance between `R` and `B` of each user feature and of their joint distribution, and of the hourly shares of rows, with intervals. A TV distance is positive by construction, so each is shown with the same distance between the odd and the even ten-minute blocks of `B`, and of `R`. Then H4 with each row of `R` given the weight `v`, the ratio of the shares of its combination of the four user features in `B` and in `R`, not clipped and recomputed in each replicate: `c_R = sum(v x click)/sum(v)`, and a cell with `sum(v) = 0` takes the unweighted `c_R`; width, coverage, fallback and drops are those of H4 from unweighted counts. Reported as the change in `rho` with its interval, with the share of rows of `B` whose combination is absent from `R`.
- Exploratory, no verdict: in `R`, whether the click on an item depends on the two other items shown with it. Impressions are identified once on the full log: sort the rows by timestamp, keeping file order among equal timestamps; an impression is a maximal run of consecutive rows with the same four user features, each less than one second after the one before, and it is complete if it has exactly three rows holding positions 1, 2 and 3 once each. For a row of a complete impression, `x` is the mean of `alpha/(alpha + beta)` of the other two items. Within each (item, position), the click rate of rows with `x` above the median of `x` in that cell on the full log minus that of the other rows; reported as the average of these differences weighted by the cell's rows, as a share of the click rate of all rows of complete impressions, with its interval. In a replicate a row keeps its impression, its `x` and its side of the median; a cell with no row on one side is left out and the weights renormalised.

## 8. Limits

What these data cannot show:
- The Beta parameters in force at any time, the update interval, whether updates pooled clicks of the random bucket, and which version served a row.
- The joint probability of the three items of an impression under the deployed policy, so the effect of dependence between positions cannot be attributed.
- What the extra 189,116 rows of `bts/all` are.
- If the aligned estimate ends below the on-policy value, the cause among user mix, effects within an impression and logging differences. H6, H7 and the exploratory item narrow it; they do not identify it.

Limits of the method:
- The Men's results shaped the rules. All has as many items as Men's and Women's together (80 = 34 + 46); whether they are the same items cannot be told from the data, so All may not be independent of the development campaign.
- `V_M` estimates the value of the deployed policy only if the BTS shares within a period do not depend on the random log's clicks in that period. If BTS learned from clicks of both buckets, or follows demand that both buckets share, the shares and `c_R` move together and `V_M` is too high, more so at small `W`. A reading of "gap shrinks" or "exceeds" is therefore read together with H5 and with `rho` at every width.
- Intervals do not include the Monte Carlo error of `pi0` or dependence that reaches beyond a ten-minute block, such as visits of one user spread over the day. Pairs of dependent rows that straddle a block boundary are lost. That the interval width does not depend on the block length was measured on the fixed-prior ratios of Men's only.
- Resampling blocks treats differences between blocks as noise. For a quantity whose expectation varies over the day and does not cancel in a ratio, the interval is wider than it should be.
- Resampled counts fall below `m` more often than the full-data counts, so replicates of `V_M` use more fallback than the estimate they surround.
- `D0` of H1 contains real change of the policy within the hour as well as noise, which makes "inconsistent" harder to reach and the middle label easier. Lists that straddle a block boundary appear in both halves and lower it slightly.
- H2: a cell stays eligible when a version with a smaller propensity was served and never chosen, which biases `S` downward; recorded propensities are Monte Carlo estimates on a grid of 1/200,000, which biases the mean of 1/propensity upward by about 0.5% at 0.001. With 12 to 25 cells, "at least 90% of intervals contain 1" fails about one time in eight when the identity holds exactly, and with 5 to 9 cells, where every interval must contain 1, about one time in three; that gives "undetermined", not "inconsistent".
- H3 and the IPS forms take the random log's propensity to be `1/n_A` as recorded. The IPS form of H4 leaves out the cells without rows of `R` and is low by about their share.

## 9. Amendments and reporting

- Any change after registration is an amendment commit that states what changed and why. Changes made after a confirmatory outcome has been computed are reported as post hoc and do not replace a registered verdict.
- The checks of Section 2 run on all four confirmatory files before a click of either campaign is read. If either campaign stops, no outcome of either is computed; the stop is resolved by an amendment, which is then not post hoc, and the one run of Section 4 is the run after it.
- Every verdict is reported as it comes out, with the statistic, its interval, the commit that produced it and the command that reruns it.

## 10. Sources

- Saito, Aihara, Matsutani, Narita (2021). Open Bandit Dataset and Pipeline. NeurIPS 2021 Datasets and Benchmarks. https://arxiv.org/abs/2008.07146 (version 5: Tables 1 and 9, footnote 4; versions 2 and 3: the footnote on a converged policy).
- `st-tech/zr-obp` at 8cbd5fa: `obp/policy/contextfree.py`, `obp/policy/conf/prior_bts.yaml`, `docs/about.rst`. Issue #208, https://github.com/st-tech/zr-obp/issues/208 (no replies on 2026-11-10).
- Dataset archive and its README.
- Jeunen (2025). Meta Off-Policy Estimation. RecSys 2025. https://arxiv.org/abs/2508.07914 ; notebook outputs in https://github.com/olivierjeunen/meta-ope-recsys-2025 at f77886a. The paper shows the Men's result in a figure and does not comment on the gap.
- https://github.com/RollinsE/open-bandit-ab-testing at a5fd178 ; https://github.com/lyftium/off-policy-bandit-evaluation at 2f36227.
- ZOZO tech blog (2020-11-06), https://techblog.zozo.com/entry/zozoresearch-bandit-overviews (in Japanese).
- `sHyanorn/push-lab`, https://github.com/sHyanorn/push-lab.
