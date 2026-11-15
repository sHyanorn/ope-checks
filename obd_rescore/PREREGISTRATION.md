# Pre-registration: published estimator comparisons on the Open Bandit Dataset against a reference unbiased for the evaluated target

## 1. Question

Published off-policy estimators are compared on the Open Bandit Dataset (OBD) by estimating the click rate of the Bernoulli Thompson sampling (BTS) policy from the uniform random log and scoring each estimate against the on-policy value `V_on`, the click rate of the BTS log. The evaluated target is built from the published Beta prior, and the registered study `obd` of this repository found that this target is not the policy that produced the BTS log (H1). On uniform random logs the IPS of a fixed target is unbiased for that target's value. With the target applied to its own (item, position) pairs, the ratio of its IPS to `V_on` is 0.948 on All, 0.891 on Men's and 1.004 on Women's (`obd`, H3). The code of C1 applies the target to other pairs (Section 2.1); the ratio of its IPS to `V_on` has not been computed. An error that IPS and another estimator share through the target is invisible in error relative to IPS, and an estimator closer to `V_on` can be further from the value of the policy it evaluates.

For each published comparison re-scored here, this study asks whether it holds when:

- (a) besides `V_on`, the reference is the value of the evaluated target: the IPS of the same target on the whole random log, which is unbiased for it, and on Men's also its SNIPS;
- (b) samples are drawn as ten-minute time blocks: in C1 in place of the published rows, in C2 as this study's resampling;
- (c) all three campaigns are used.

It does not ask which estimator is better in general, or why the deployed policy differs from the prior.

## 2. Claims

### 2.1 C1: MIPS (w/ SLOPE) against IPS

- Source: Saito and Joachims (2022), arXiv 2202.06317v2, Section 4.2 and Figure 7; appendix "Experimental Procedure to Evaluate OPE Estimators on Real-World Bandit Data".
- Claim: "MIPS (w/ SLOPE) outperforms IPS in about 80% of the simulation runs". The same sentence goes on to say that the other estimators, MIPS (w/o SLOPE) among them, "work similarly to IPS"; that part has no number and is reported without a label.
- Protocol, from the paper and from `usaito/icml2022-mips` at `08d65ce` (`src/real/main.py`, `src/real/ope.py`, MIT licence):
  - campaign All; the random log is the logging data;
  - a run draws 100,000 rows of the random log with replacement, with `numpy.random.RandomState(t)` for run `t`, from the rows in obp's order after it sorts the log by timestamp; 150 runs, `t = 0` to 149;
  - an action is an (item, position) pair, 240 in all; the action embedding is `item_feature_1` to `item_feature_3`, label-encoded, and the position;
  - target: `obp.policy.BernoulliTS(n_actions=80, len_list=3, random_state=12345, is_zozotown_prior=True, campaign="all")`; each run computes its action distribution anew with `compute_batch_action_dist` (100,000 Monte Carlo draws), so the target of run `t` comes from the `t`-th block of draws of one random stream;
  - error of an estimator in run `t`: its squared distance from `V_on` of the whole BTS log, divided by that of IPS;
  - MIPS (w/ SLOPE) is `MIPS().estimate_policy_value(..., feature_pruning="exact")` of `src/real/ope.py`.
- The default configuration of the repository has 10,000 rows per run; the paper's 100,000 is set by overriding it.
- The code reshapes the action distribution from items by positions to 240 actions and divides it by 3 (`main.py` line 168). The reshape numbers item `a` at position `k` as `3a + k`, while the logged action is numbered `80k + a` (line 70), positions counted from 0. obp's IPS (`ope/estimators.py` line 334 of obp 0.5.5) reads the array at the logged action, and the code's MIPS (`ope.py` lines 39 and 65) reads it at every action, numbered as the logged actions are (lines 68 to 70), so 238 of the 240 actions get the probability of another (item, position) pair; only (item 0, position 0) and (item 79, position 2) keep their own. For example, the rows with item 23 at the third position are weighted by the probability of item 61 at the first, about 0.198 under the prior. The published code evaluates this rearranged distribution, not the BTS distribution. From the prior alone (1,000,000 Monte Carlo draws), the rearranged distribution puts 0.14, 0.30 and 0.56 of its mass on the three logged positions, and its total variation distance from the BTS distribution over the 240 pairs is 0.76. Both lines are unchanged since the commit that added the code (`9286853`).
- Two targets are evaluated, both from the same action distribution of each run (Sections 5 and 7.1): the published target, the rearranged distribution as the code applies it, and the own-pair target, which puts each probability on its own (item, position) pair. The published target carries the replication (Section 8.5) and is the target the published comparison used. The own-pair target gives the primary label.
- Read here as: MIPS (w/ SLOPE) is closer to the reference than IPS in most runs. The substance of the claim is the comparison with IPS; "about 80%" is its size, checked on its own as part of the replication and not entering the label.

### 2.2 C2: BLUE against the estimators reported with it

- Source: Jeunen (2025), Meta Off-Policy Estimation, RecSys 2025, arXiv 2508.07914v1, Section 4.2 "Open Bandit Dataset and Pipeline" and Figure 3.
- BLUE combines SNIPS, beta-IPS and DR (notebook cell 44; "we include three (asymptotically) unbiased but complementary estimators", Section 4.2). IPS and DM are shown beside it and are not combined.
- Claims: "BLUE remains unbiased, but with significantly reduced variance"; BLUE "successfully leverages the covariance structure [...] to increase the BLUE estimate and bring it closer to V(π)"; the caption of Figure 3, "Our proposed BLUE approach significantly improves estimation accuracy over existing individual estimators"; results on the other campaigns "were qualitatively similar", "albeit with less pronounced improvements due to already well-performing base estimators", with no numbers. The half "with significantly reduced variance" gets no label; the standard deviations of BLUE and of each estimator reported with it over the replicates are reported without a rule (Section 8.6).
- Numbers: outputs of the notebook `BLUE OPE.ipynb` of `olivierjeunen/meta-ope-recsys-2025` at `f77886a` (MIT licence), Men's, cell 45 (cells counted from 0): BLUE 0.006687691524532561, IPS 0.006010953776252967, SNIPS 0.00612731824047759, beta-IPS 0.006152023858050668, DR 0.006118951440097642, DM 0.005127094504168594; `V(π)` 0.006742727014339116 (cell 42). These are shortest round-trip representations and fix each value exactly.
- DM here is the notebook's mean of the reward model's prediction for the logged item at its logged position (cell 44); cell 29 prints obp's DirectMethod, a different quantity. As a mean of predictions at the actions of the random log, this DM is close to the click rate of that log (2,321 clicks in 452,949 rows, 0.005124, `obd` Sections 2 and 3), the value of the logging policy.
- Protocol, from the notebook:
  - the whole random log of Men's (452,949 rows), one estimate per estimator, no repeated runs;
  - target: `BernoulliTS(..., is_zozotown_prior=True, campaign="men", random_state=12345)` with 1,000,000 Monte Carlo draws (cell 17);
  - reward model: `RegressionModel(n_actions=dataset.n_actions, len_list=dataset.len_list, action_context=dataset.action_context, base_model=RandomForestClassifier(n_estimators=150, max_depth=5, n_jobs=-1, random_state=12345))` of obp, five-fold cross-fitting with `random_state=12345` (cells 22 and 23), shifted by one constant so that the mean of its predictions over all rows, items and positions equals the mean click (cells 25 and 26);
  - the estimates come from the function `BLUE` defined in cell 44, which reads the predictions from the global `estimated_rewards_by_reg_model`.
- The notebook imports a modified obp: cell 1 imports `InverseProbabilityWeightingOptimalBaseline`, which obp 0.5.5 lacks. The evidence points to the obp of `shashankg7/recsys2024_optimal_baseline` at `137cdbe` (Apache-2.0): the README of the notebook's repository acknowledges that repository, and the source line of a warning the notebook prints (`obp/ope/meta.py:754`) and the three values that `summarize_off_policy_estimates` returns in cell 28 match that copy. The obp files on which the outputs of `BLUE` depend (`dataset/real.py`, `policy/contextfree.py`, `policy/base.py`, `ope/regression_model.py`) are identical in obp 0.5.5 and in that copy. The notebook's metadata records Python 3.10.15; the package versions behind its stored outputs are not recorded.
- Read here as two parts:
  - "BLUE remains unbiased" (primary). IPS is unbiased for the value of the target on the uniform random log, so if BLUE is unbiased, `BLUE - IPS` has expectation 0 (Section 8.3).
  - BLUE is closer to the reference than each of the five estimators reported with it, in most resamples of the data (secondary). The published comparison is of one estimate on one data set. On the full data IPS and SNIPS are the references `R_IPS` and `R_SNIPS` (Section 6), so a comparison of single estimates could never show BLUE closer than them. Against `V_on` the comparison of single estimates is reported as it stands (Section 8.6).

### 2.3 Excluded claims

- Gupta, Jeunen, Oosterhuis and de Rijke (2024), arXiv 2405.05736v2, Men's table of `sections/5_Results.tex` (mean relative absolute error: IPS 0.1277, SNIPS 0.1113, DR 0.1144, beta-IPS 0.1078). The paper names no target policy, sample size or number of runs. `shashankg7/recsys2024_optimal_baseline` at `137cdbe` holds no script that produces the table: its `benchmark/ope` configuration names the Men's campaign, but that script runs no beta-IPS and reports root mean squared error. The relative errors of the notebook of Section 2.2 on the whole Men's log (cell 40: IPS 0.1085, SNIPS 0.0913, DR 0.0925, beta-IPS 0.0876) differ from the table, so the table does not come from the notebook's single run on the whole log. The beta-IPS estimator enters C2 as one of BLUE's inputs.
- Felicioni, Benigni and Ferrari Dacrema, AutoOPE, arXiv 2406.18022v2, table "Experimental results on Open Bandit Dataset (OBD)" (relative regret, PAS-IF 4.54 ± 4.47, AutoOPE 0.79). The code is linked only at `https://anonymous.4open.science/r/auto-ope-28F3/`. One request to `https://anonymous.4open.science/r/auto-ope-28F3`, on 2026-11-15 at 03:31:42 UTC, was redirected to `/api/repo/auto-ope-28F3/file/`, which answered HTTP 401 with the body `{"error":"not_connected"}`. The paper states only that the target "is the Bernoulli Thompson Sampling policy", not how it is built. Not reproduced.
- Chandak, Liu and Lee, Context-Action Embedding Learning for Off-Policy Evaluation in Contextual Bandits (CAEL-MIPS), arXiv 2509.00648v2, Section "Real-World Data" (10,000 rows, 30 repetitions, "more than 75% of the runs"). No code is linked.
- Cief et al. (2024), Learning Action Embeddings for Off-Policy Evaluation, arXiv 2305.03954v2, Section "Real-world data" (10,000 rows, 150 runs; "Learned MIPS methods outperform IPS in about 75% of runs", MIPS (w/ SLOPE) "in about 65% of runs"); code `amazon-science/ope-learn-action-embeddings` at `8729659`, Apache-2.0. Its code was not run in this study, so the claim was neither timed nor reproduced. It numbers the logged action and reshapes the target as the code of C1 does (`jobs/utils/dataset.py` line 81, `jobs/real_dataset_job.py` line 71).

## 3. Data and fixed inputs

- Archive: `https://research.zozo.com/data_release/open_bandit_dataset.zip`, 412,931,917 bytes, sha256 `e8ec18196582a5937381a1776382ca940689b90a18d2dcd1fb635be6df614d78`, as in `obd`. It is released under CC BY 4.0 (`obd` Section 2). This study is non-commercial research.
- Files: the six logs `{random,bts}/{all,men,women}` and the item context file of each campaign, as released. Row counts are those of `obd` Section 2; no row of any log lies outside the week (`obd/results/`).
- Before any click is read, the stop checks of `obd` Section 2 and its amendment 6 run on all six logs (`obd.data.check`). A stop ends the run before any outcome is computed.
- Prior: the published codes read the copy of `prior_bts.yaml` packaged with obp 0.5.5 and with the obp of Section 2.2. Both have sha256 `81a54fbdc184021ccc62ab97de81ec35461c032e3d7f99ccaa0a9745f732d251`, the file registered in `obd`.
- Third-party code, fetched at the commits named in Section 2; obp 0.5.5 from its source distribution on the Python Package Index, sha256 `114bff280213cb06bee927afbfb6c81f2d42e846cc570bd0d50115abb3a91aee`. A run verifies each commit and records the sha256 of every file it uses. The code is not copied into this repository.
- Logs are read on this study's side with `pandas.read_csv(..., float_precision="round_trip")` and kept apart from the files of `obd`.

## 4. What was seen before this registration

From this repository:

- The registered results of `obd` on all three campaigns, among them `V_on` with its interval, the ratios of IPS and SNIPS of the fixed-prior target to `V_on` (All 0.948 and 0.948, Men's 0.891 and 0.908, Women's 1.004 and 1.004) and the mean weight on Men's, 0.981 (0.968 to 0.994). On each campaign, the target of `obd`, the own-pair target of C1 and the target of C2 are Monte Carlo approximations of the same distribution applied to the same pairs, so for them `R_IPS` is known before the run up to their Monte Carlo error. For the published target of C1 it has not been computed.
- Everything `obd` Section 3 lists, among them the ratios to `V_on` on Men's with impressions resampled from `sHyanorn/push-lab`: DR 0.897 (0.824 to 0.975) and DM 0.881 (0.868 to 0.895).
- Sections 1 to 7 of `obd/posthoc/` and `docs/obd-results.md`: the resampling unit, the user feature left unmatched by amendment 7, `M` of H2 below 1, the block length, the other registered intervals by block length, three distances that read no click, and the parameter pairs of the prior file (all 34 pairs of Men's occur among the 80 of All, in the same order). From Section 1, the standard deviation of the IPS ratio when rows are resampled is 0.0309 (All), 0.0373 (Men's) and 0.0322 (Women's). Multiplied by the square root of (rows of the random log / 100,000), it is about 0.115, 0.079 and 0.095 for runs of 100,000 rows, against distances of 0.052, 0.109 and 0.004 between the IPS ratio and 1. These describe the target on its own pairs.
- `obd_coverage/` and its extension: in scenario M, fitted to statistics of OBD, the coverage of nominal 95% intervals is 0.85 to 0.88 with rows or impressions as resampling units and 0.94 to 0.95 with blocks of 5 minutes or more; the registered excess within an impression is 2.2 to 3.9 times the one measured on All and Women's; scenario F reproduces 16 of 25 statistics on All and 11 of 25 on Women's.
- Reruns of `obd` on OBD made outside the repository: 205 to 211 s at 1.6 GB of memory for Men's and 851 s at 2.8 GB for All and Women's; 46 of the 397 values of `men.json` differ in the last digits with pandas 3.1.1; pandas 3.0.5 parses 241,904 of the first 1,000,000 propensities of `bts/men` one unit in the last place off; on data converted with pandas 3.0.5, 1,775 of the 5,645 values of `obd/posthoc/results/propensities.json` differ by about 1e-14.

Computed from OBD before this registration to plan this study:

- A recomputation of Table 9 of the OBD paper: IPS of the fixed-prior target on 200 samples of 300,000 rows of each random log, root mean squared error x 10^3 of 0.404 (All), 0.806 (Men's) and 0.387 (Women's); full-data IPS ratios 0.9477, 0.8913 and 1.0044. On All the standard deviation of the IPS ratio over these samples is 0.0613, about 0.106 at 100,000 rows.
- From the 0.106 above, larger than the distance 0.052 between the IPS ratio and 1 on All, it was expected then, with no MIPS estimate computed, that the published 80% of MIPS (w/ SLOPE) may hold against both references.

Read before this registration:

- The numbers and figures of the papers of Section 2. In Figure 7 of the MIPS paper, the curve of MIPS (w/ SLOPE) crosses a relative error of 1 near 0.8.
- Third-party figures on OBD: `itsnjstyle27/counterfact`, relative error of IPW against `V_on` 5.2%, 10.9% and 0.4% (All, Men's, Women's) with the published prior and 0.9%, 11.3% and 4.7% with a target that replays the logged propensities; IPS ratios to `V_on` with the mean recorded propensity of each (item, position) pair in the BTS log, renormalised per position, as target, computed from the results file of `adeoluo/ad-auction-lab`: All 0.9971 (0.951 to 1.034), Men's 0.8911 (0.831 to 0.942), Women's 0.9678 (0.933 to 1.013); `aghasalim/recsys-offline-online`, All, IPS with the BTS log's whole-week frequencies as target 1.7% above `V_on`, interval 0.00480 to 0.00527; the OBD paper, relative errors of IPW 0.05146, 0.11060 and 0.02827 (version 3) and RMSE x 10^3 of IPW 0.474, 1.298 and 1.645 (version 5, Table 9).
- The printed outputs of the notebook of Section 2.2, among them `V(π)` = 0.006742727014339116, equal in every printed digit to `V_on` of Men's in `obd/results/men.json`.
- The layout of the target in the code of C1 (Section 2.1), found by reading the code after the computations listed above and checked with the prior file alone; no OBD data was used for it.
- On 2026-11-15 a text search over obp 0.5.5's source distribution printed the header lines (column names) of the item context files in the small OBD sample it ships; nothing else from that sample was shown, and nothing was computed from it.

What follows for C2 on Men's. There the target's references are the notebook's IPS (0.006011) and SNIPS (0.006127). On the full data BLUE is 0.000677 above IPS (0.100 of `V_on`) and 0.000560 above SNIPS (0.083 of `V_on`); it is further from each of the two than IPS, SNIPS, beta-IPS and DR are, and closer than DM. The block standard deviation of the IPS ratio is 0.055 (Section 1 of `obd/posthoc/`); if BLUE did not vary, it would be closer to `R_IPS` than IPS in about 7% of replicates (normal approximation). Against `V_on` BLUE is 0.000055 away and the closest of the others, beta-IPS, 0.000591. The distance labels on Men's are therefore expected to be "flips" against the target and "holds" against `V_on`. The interval of `BLUE - IPS` over replicates (Section 8.3) has not been computed.

Resource needs were measured on synthetic logs only (Section 9). No code of Section 2 has been run on OBD by this project, and no estimate, reference or interval of this study has been computed from OBD data.

Earlier public work. `obd` measured how much of the gap between IPS and `V_on` the target accounts for. Three public repositories had estimated the BTS click rate against targets built from the BTS logs (`obd/AMENDMENTS.md`, "Correction"), and others score estimates against `V_on`. A search on 2026-11-15 found no work that re-scores a published estimator comparison against a reference unbiased for the evaluated target. The search covered GitHub repositories matching "open bandit dataset" (12 results) and "icml2022-mips", two web searches, and the repositories of the papers of Section 2.

## 5. Environments and adapters

Let `n_A` be the number of items, so that there are `3 n_A` actions; positions are counted from 0 throughout, as in the code. `pi(a|k)` is the target's probability of item `a` at position `k` as obp's `compute_batch_action_dist` returns it.

Each published code runs in an environment fixed to its own versions. No estimator is rewritten.

- Environment `mips`: Python 3.9.25 and every main package of `poetry.lock` at `08d65ce` at its locked version, among them numpy 1.22.4, pandas 1.3.5, obp 0.5.5, scikit-learn 1.0.2, scipy 1.7.3 and hydra-core 1.0.7.
- Environment `blue`: Python 3.12.2 with numpy 1.26.4, pandas 2.2.1, scikit-learn 1.4.1.post1, scipy 1.12.0, matplotlib 3.8.3, seaborn 0.13.2, pyyaml 6.0.1, tqdm 4.66.2, joblib 1.3.2, threadpoolctl 3.4.0 and IPython 8.23.0, the versions of the environment file shared by both repositories of Section 2.2, and the obp of `137cdbe` on the path. That file is a conda export: numpy, pandas, scikit-learn, scipy, matplotlib, pyyaml, tqdm, IPython and torch were installed from the Python Package Index, and Python, seaborn, joblib and threadpoolctl from conda. This study installs the same versions from the Python Package Index. IPython runs the cells that begin with `%%time`.
- This study's own code runs in a third environment with numpy 2.5, whose random streams are those registered in `obd`.
- Each environment has a lock file with hashes, committed before the run.

Adapters, each run in the environment of its code:

- `mips`: imports `ModifiedOpenBanditDataset` from `src/real/main.py` and `MIPS` from `src/real/ope.py`, and runs the loop of `main` for IPS, MIPS (w/o SLOPE) and MIPS (w/ SLOPE), with both targets on the same rows. For each run, arm (Section 7.1) and target it writes the three estimates and the number of rows.
- `blue`: runs the cells of the notebook on the Open Bandit path in their order, with the campaign set in cell 3, and calls `BLUE` from the source of cell 44 read from the notebook file at `f77886a`, with the global `estimated_rewards_by_reg_model` set to the predictions of the rows of each call.

Departures from the published paths, each covered by a test on synthetic logs:

1. torch is installed as the CPU build of the locked version (1.11.0 in `mips`, 2.2.0 in `blue`). obp imports torch; neither path uses it.
2. The `mips` adapter does not run DR, DM, Switch-DR, MRDR, DRos and DR-λ, which are not part of C1, and fits no reward model. None of them draws random numbers; the reward model they share is fitted in each run with `random_state=12345` for the forest and the fold split, and nothing draws from the target's stream. The action distributions are drawn once per campaign and stored (Section 7.1), where the published loop draws one in each run. T1.
3. The own-pair target: the adapter transposes obp's (rows, items, positions) array to (rows, positions, items) before the published reshape, so that index `k n_A + a` holds `pi(a|k)`. The published target keeps the published reshape. T2.
4. On Men's and Women's the adapter sets the campaign and the number of items where the code has `"all"`, 80 and 240 (`main.py` lines 138, 143, 147, 152, 159, 168 and 174).
5. The block arm (Section 7.1) takes the rows of the drawn blocks with their multiplicities in place of the published draw of rows: the rows in obp's order, each repeated in place as many times as its block is drawn. It builds the run's data from these indices as `sample_bootstrap_bandit_feedback` does from its own. T6.
6. `V_on` is computed as the mean of the click column of the whole BTS log. The published codes load the whole BTS file with obp; on a synthetic log of the size of All this fails in `mips` with 13 GB of address space. T5; on Men's both are computed on OBD and reported.
7. The resampled calls of `BLUE` (Section 7.2) receive equivalent compact inputs: each row carries two actions, the logged one and the rest. The rest's probability is the target's probability of the other items at the row's position, and its prediction is their target-weighted mean prediction, 0 where that probability is 0. Every quantity the function uses (importance weights, rewards, the reward model's value under the target, the prediction for the logged action) is unchanged up to floating-point rounding. A call with the full inputs on resampled rows of the size of All fails in `blue` with 14 GB of address space. T4; on the full OBD data of each campaign both inputs are used and the difference reported. The estimate on the full data uses the full inputs, as published.

Tests on synthetic logs:

- T1: the squared errors of the adapter's estimates with the published target in the row arm equal, bit for bit, those the published entry point writes (`result_df.csv`, read with round-trip precision), with `main` run through its own configuration and a small number of runs.
- T2: under the published target the weight of a row with item `a` at position `k` is `n_A x pi(j div 3 | j mod 3)` with `j = k n_A + a`, and under the own-pair target `n_A x pi(a|k)`, for every pair, in IPS and in MIPS's weight of each action (`ope.py` line 65).
- T3: the `blue` adapter against the notebook's cells executed in order, within a relative 1e-9 (the forest adds the trees' probabilities across threads in an order that can vary).
- T4: compact and full inputs to `BLUE` give the same outputs within a relative 1e-9.
- T5: `V_on` against obp's function.
- T6: the rows of a block run are those of the drawn blocks, each counted as often as its block is drawn, and the multiplicities are those drawn in this study's environment.
- T7: `R_IPS,t` and `R_SNIPS,t` of each target, from the formulas of Section 6, equal the adapter's IPS with that target and its self-normalised form on the whole random log, and in C2 `R_IPS` and `R_SNIPS` equal the IPS and SNIPS that `BLUE` returns on the full data.
- T8: on a log whose target value is known and whose "on-policy value" is set apart from it, an estimator shifted towards that value is labelled "holds" against `V_on` and "flips" against `R_IPS`; ties and estimates that are not finite are counted as Section 8.1 says.

## 6. References

- `V_on`: the mean click of the whole BTS log.
- Applied probability: a row with item `a` at position `k` is weighted by `pi*(a,k) / pscore`, with `pscore` its recorded propensity, `1/n_A` within 1e-9 (`obd` Section 2). `pi*(a,k) = pi(a|k)` for the own-pair target of C1 and for C2, and `pi*(a,k) = pi(j div 3 | j mod 3)` with `j = k n_A + a` for the published target of C1 (Section 2.1). The code of C1 divides both the action distribution and the recorded propensity by 3 (`main.py` lines 168 and 72), so under either layout its IPS weights a row by exactly `pi*(a,k) / pscore`.
- Value of a target as applied: the expectation of `R_IPS` below on the random log, `sum over (a, k) of s_k x pi*(a,k) x r(a,k)`, where `r(a,k)` is the click probability of item `a` at position `k` in the random log and `s_k` the share of its rows at position `k`, about 1/3. Under the own-pair target it is the target's click rate, positions weighted by `s_k`; under the published target it is the quantity the published code estimates.
- `R_IPS = (1/N) x sum over rows of the random log of click x pi*(a,k) / pscore`, `N` its rows: the IPS of the code with that target on the whole random log, unbiased for the value of the target as applied because the log is uniform.
- `R_SNIPS = sum of click x pi*(a,k) / pscore over sum of pi*(a,k) / pscore`, its self-normalised form, on Men's only, where the mean weight of the target on its own pairs is 0.981 (Section 4). It is consistent for the value divided by `sum over (a, k) of s_k x pi*(a,k)`. Under either layout `pi*` sums to 3 over the pairs, so this divisor is 1 under the own-pair target and 1 under the published target when each `s_k` is 1/3.
- In C1 each run `t` has its own action distribution `pi_t`, and `R_IPS,t` and `R_SNIPS,t` are computed for each of the two targets from it. In C2 the target is the notebook's, and `R_IPS` and `R_SNIPS` from the formulas above equal the IPS and SNIPS that `BLUE` returns on the full data. T7 checks this on synthetic logs; on OBD a relative difference above 1e-9 stops the run before any label.
- These are the values against which errors are scored. They are fixed at their full-data values (Section 7). "Against the target" means against `R_IPS`, and on Men's against `R_IPS` and `R_SNIPS`.
- Reported with each, no rule: its 95% interval and that of its ratio to `V_on` from the 10,000 registered replicates of `obd` Section 5, ten-minute blocks drawn jointly in both logs. In C1 they are computed for each target with the mean of `pi_t` over the 500 runs.

## 7. Resampling

The published protocols score each estimate against a value computed once on the full data. Within the resampling of a protocol, the value of the target is `R_IPS` of the full data: IPS on a sample of rows is unbiased for it, on a sample of blocks nearly so (a ratio whose denominator varies), and `V_on` is not. So both references are kept at their full-data values. The sampling error of a reference does not enter the comparison of estimators within one resampling. How the labels would change with another week of logs is not estimated (Section 10).

### 7.1 C1

Each run is drawn in two ways, the arms:

- Rows: the published sampling, 100,000 rows with `RandomState(t)`.
- Blocks: `b` ten-minute blocks drawn with replacement; the rows of the random log in a block drawn `m` times count `m` times. `b = round(1008 x 100,000 / N)`: 73 (All), 223 (Men's), 117 (Women's), so that a run holds about 100,000 rows (99,530, 100,206 and 100,354 expected). The multiplicities of run `t` on campaign `c` (all 0, men 1, women 2) are `numpy.random.default_rng([20261115, 0, c, t]).multinomial(b, numpy.full(1008, 1/1008))`, element `u` belonging to block `u`, a ten-minute clock interval of the week as in `obd` Section 5. They are drawn in this study's environment and passed to the adapter.

Runs `t = 0` to 499 on each campaign, in each arm, with each target. Runs 0 to 149 of the row arm on All with the published target are the published runs.

For each campaign, the 500 action distributions `pi_t` are drawn once, in the order of `t`, from one `BernoulliTS` object created with `random_state=12345` as in the published loop, and stored. Every arm, process and resumed run reads them. The published and the own-pair target of run `t` are two layouts of `pi_t`, so run `t` has the same `pi_t` in both arms and with both targets.

On Men's and Women's the campaign and its number of items, 34 and 46 (102 and 138 actions), are the only settings changed. The published layout keeps its rearrangement there: only (item 0, position 0) and (item `n_A - 1`, position 2) keep their own probability, and the total variation distance from the BTS distribution over the pairs is 0.65 (Men's) and 0.72 (Women's) from the prior alone.

### 7.2 C2

Replicates `i = 0` to 1,999 of the registered stream of `obd` Section 5: replicate `i` draws the 1,008 ten-minute blocks of the week with replacement, with multiplicities `numpy.random.default_rng([20261110, 0, i]).multinomial(1008, numpy.full(1008, 1/1008))`, the same on every campaign, and resamples both logs together; blocks are the UTC ten-minute intervals numbered from 0 at 2019-11-24 00:00. The multiplicities are drawn in this study's environment and passed to the adapter. In a replicate `BLUE` and the estimators it returns are computed on the resampled random log, and `V_on,i` on the resampled BTS log. The reward model and the target stay as fitted and computed on the full data, as in obp's own bootstrap: each drawn row keeps its shifted full-data prediction, and the predictions of the drawn rows are passed to `BLUE` as `estimated_rewards_by_reg_model`; neither the fit nor the shift is redone.

On All and Women's only the campaign of cell 3 changes: the target is that campaign's, with 1,000,000 Monte Carlo draws, and the reward model is fitted on that campaign's random log and shifted as in the notebook, with the same seeds.

### 7.3 Block length

Ten minutes is the registered unit of `obd`. There, on Men's, the standard deviation of the IPS ratio is within 3% of its ten-minute value for blocks of 5 to 60 minutes; on All and Women's it is 1.07 and 1.12 times that value at 60 minutes (Section 4 of `obd/posthoc/`). No other length is used.

## 8. Statistics and decision rules

### 8.1 Comparisons

A comparison of a claimed estimator `Y` with another estimator `X` against a reference `V`, over a set of runs or replicates:

- A run or replicate in which `Y`, `X` or `V` is not finite is removed from this comparison only, and counted.
- `p` is the share of the runs or replicates kept in which `Y` is strictly closer to `V` than `X`, `|Y - V| < |X - V|`; `q` the share in which `X` is strictly closer. A tie, the two absolute errors equal in float64, counts in the denominator of both shares and is reported.
- `[p_L, p_U]` and `[q_L, q_U]` are the 95% Wilson score intervals of `p` and `q`, with z = 1.959964.
- Label: "not evaluable" if the comparison removes more than 1% of its runs or replicates (as amendment 1 of `obd`); otherwise "holds" if `p_L > 0.5`, "flips" if `q_L > 0.5`, and "undecided" if neither, meaning that the runs show neither that `Y` is closer in most runs nor that `X` is. With 500 and 2,000 runs, `p_L > 0.5` needs at least 272 and 1,044 runs in which `Y` is closer.

### 8.2 C1

For each campaign, arm, target and reference `V` (`V_on`; `R_IPS,t`; on Men's also `R_SNIPS,t`): the comparison of MIPS (w/ SLOPE) with IPS over runs 0 to 499. The threshold is a majority because the substance of the claim is that MIPS (w/ SLOPE) is closer than IPS; the published 80% is its size, checked separately (Section 8.5).

### 8.3 C2

- Primary: on Men's, the interval `[L, U]` of the 2.5th and 97.5th percentiles of `BLUE_i - IPS_i` over the 2,000 replicates of Section 7.2, computed in this study's environment with `numpy.percentile(..., method="linear")`. A replicate in which `BLUE_i` or `IPS_i` is not finite is left out and counted. Label: "not evaluable" if more than 1% of the replicates are left out; otherwise "contradicted" if the interval excludes 0 and "not contradicted" if it contains 0, where it contains 0 if `L <= 0 <= U` (amendment 3 of `obd`), so that an end at exactly 0 gives "not contradicted". IPS is unbiased for the value of the target, so an interval that excludes 0 contradicts "BLUE remains unbiased". The same statistic is reported on All and Women's with its label.
- Secondary, the distance comparisons: for each campaign, reference `V` (`V_on`; `R_IPS`; on Men's also `R_SNIPS`) and estimator `X` among IPS, SNIPS, beta-IPS, DR and DM as `BLUE` returns them, the comparison of BLUE with `X` over the 2,000 replicates. Label for a reference: "flips" if the label against some `X` is "flips"; otherwise "not evaluable" if the label against some `X` is "not evaluable"; otherwise "holds" if the label against every `X` is "holds"; otherwise "undecided".

### 8.4 Labels reported

- Against the target: on All and Women's, the label against `R_IPS`. On Men's, the labels against `R_IPS` and `R_SNIPS` are combined: their common label if they agree, "not evaluable" if either is, otherwise "references differ". In C2 the labels against the five `X` are combined within each reference first (Section 8.3), then the two references.
- Primary labels: C1 with the own-pair target on All, block arm, against the target; C2, the interval of `BLUE - IPS` on Men's.
- Every other cell gets a label by the same rules and is shown with the primary ones: for C1 each campaign, arm and target, against `V_on` and against the target; for C2 the interval of `BLUE - IPS` on All and Women's and the distance labels of each campaign against `V_on` and against the target. The four cells of a campaign and target in C1 give the label under each reference and each resampling unit; no rule attributes a change of label to one or the other.
- Labels are reported for each campaign separately; no label pools campaigns.
- Shown with every label: the counts behind `p` and `q`, the ties, the runs or replicates removed, and the label against each reference and each `X` from which it was combined.

### 8.5 Replication

Both replications are computed before any estimate, reference or label other than theirs and reported as found. A failed check does not stop the run; the labels are reported with it.

- C1: `p` of MIPS (w/ SLOPE) against IPS with the published target, row arm, against `V_on` on All over runs 0 to 149. "Not evaluable" if that comparison removes more than 1% of its runs; otherwise "reproduced" if `|p - 0.80| <= 0.065`, the size of two binomial standard errors at 0.8 with 150 runs, taken as the tolerance of "about" (111 to 129 runs of 150), and "published share not reproduced" if not.
- C2: on Men's, IPS, SNIPS, beta-IPS, DM, DR and BLUE from the full data against cell 45 of the notebook, and `V_on` against `V(π)` of cell 42. "Reproduced" if each lies within a relative 1e-6 of the printed value; otherwise "not reproduced", with the differences. The labels use this study's values.

### 8.6 Reported with them, no rule

- For C1: in every cell, the comparison of Section 8.2 with MIPS (w/o SLOPE) in place of MIPS (w/ SLOPE), its shares and intervals without a label; for each campaign, arm, target, reference and estimator (IPS, MIPS (w/o SLOPE), MIPS (w/ SLOPE)), the mean over runs of `(estimate_t - V) / V_on`, with `V` the reference of run `t` (`V_on`, `R_IPS,t` or `R_SNIPS,t`); the number of rows of block runs; for each target, the mean over runs of `R_IPS,t / V_on`.
- For C2: the full-data estimates; whether, on the full data, BLUE is closer to `V_on` than each `X`, the published comparison as it stands; `BLUE - R_IPS` and `BLUE - V_on` on the full data, with the 2.5th and 97.5th percentiles of `BLUE_i - V_on,i` over the replicates; the standard deviations of `BLUE_i` and of each `X_i` over the replicates.
- The references with their intervals (Section 6).

## 9. The run and its outputs

- One commit, after this registration is committed, computes each claim once, in this order: the stop checks of Section 3, both replications of Section 8.5, then everything else.
- Results go to `obd_rescore/results/`: per-run and per-replicate estimates, references, shares, intervals and labels. They record the commit of the code, the numpy, pandas and pyarrow versions of this study's environment, the installed packages and Python version of each published code's environment, the commits of the third-party code and the sha256 of each file used from it.
- Results are written run by run, so that a stopped run can resume. A resumed run must reproduce what it had written, and any interruption is recorded as in `obd`.
- Resource needs, measured on synthetic logs of the sizes of the random logs, one process at a time:
  - C1: drawing the target of a run takes about 3.6 s on a log of the size of All, 2.3 s on one of Men's and 2.6 s on one of Women's, and the three estimators about 35 s, 14 s and 18.5 s for each arm and target, all of it on one core. A run with both arms and both targets thus takes about 142, 57 and 77 CPU seconds, and the 500 runs of the three campaigns about 38 CPU hours: about 10 hours on four evenly loaded processes. A process holding a log of the size of All needs up to 4.63 GB of memory, of Men's 1.1 GB and of Women's 1.9 GB; four processes of the size of All need up to 18.5 GB.
  - C2: on a log of the size of All, about 7 minutes for the full-data estimate (reading, target, reward model and one call of `BLUE`) with 9.6 GB at its peak; on the size of Men's about 2 minutes, and about 1 s per resampled call with the full inputs. The compact calls and the size of Women's are timed before the run.
- Every verdict is reported as it comes out, with its statistic, interval, commit and the command that reruns it.

## 10. Limits

- The labels describe the resampling of each protocol, in which the full-data `R_IPS` is the target's value. They do not include how the shares would change with another week of logs. Nested resampling, an outer block resampling of the week with the protocol run within each replicate, was considered and not done: at 50 outer replicates of 100 runs it needs about 50 CPU hours on All alone, for one arm and one target. The published claim of C1 rests on the same kind of resampling and carries the same limit; that of C2 rests on one estimate.
- In the real world `R_IPS` differs from the target's value by its sampling error. The block standard deviation of the IPS ratio to `V_on`, both logs resampled together, is 0.042 to 0.055 (Section 1 of `obd/posthoc/`); that of `R_IPS` alone was not computed. This error is common to all estimators and does not enter the labels.
- On Men's the random log's item counts vary more than uniform draws would because lists are reused (`obd` Section 3). IPS and `R_IPS` take the logged propensity as recorded, as the published codes do. On Men's, where the mean weight is furthest from 1, SNIPS is a second reference.
- The targets are the published codes' Monte Carlo approximations, and each reference uses the same one, applied to the same pairs.
- In C2 the reward model is fitted once on the full data. Replicates do not include the variation of its fit.
- Intervals and block runs rest on ten-minute blocks. Dependence or change over the week beyond ten minutes is not separated (`obd` Section 8).
- C2 has no published resampling; its replicates are this study's. No published number exists for C2 on All and Women's, or for C1 on Men's and Women's.
- All's prior holds all 34 parameter pairs of Men's in the same order (Section 7 of `obd/posthoc/`), so, by the inference of that section (the files hold no common item identifier), All is not independent of Men's, the campaign of the published C2 result.
- Block runs vary in size around 100,000 rows, and IPS on them is unbiased for `R_IPS` only up to the bias of a ratio.
- A label of "flips" against the target, where the label against `V_on` in the same arm is "holds", shows that the published comparison depends on the reference. It does not show that the estimator is worse in general. "Contradicted" means that `BLUE - IPS` lies away from 0 at the 95% level of this resampling at the full size of the data, with the reward model and the target fixed; an asymptotic statement is not tested. "Not contradicted" does not show that BLUE is unbiased. The excluded claims of Section 2.3 are not assessed.

## 11. Amendments and reporting

- Any change after this registration is committed is an amendment commit that states what changed and why. A change made after an outcome of Section 8 has been computed is reported as post hoc and does not replace a registered label.
- Labels, shares and intervals are reported as they come out, with the replication of Section 8.5 beside them.

## 12. Sources

- Saito and Joachims (2022). Off-Policy Evaluation for Large Action Spaces via Embeddings. ICML 2022. https://arxiv.org/abs/2202.06317 (v2). Code: https://github.com/usaito/icml2022-mips at `08d65ce`.
- Jeunen (2025). Meta Off-Policy Estimation. RecSys 2025. https://arxiv.org/abs/2508.07914 (v1). Notebook: https://github.com/olivierjeunen/meta-ope-recsys-2025 at `f77886a`.
- Gupta, Jeunen, Oosterhuis and de Rijke (2024). Optimal Baseline Corrections for Off-Policy Contextual Bandits. RecSys 2024. https://arxiv.org/abs/2405.05736 (v2). Code: https://github.com/shashankg7/recsys2024_optimal_baseline at `137cdbe`.
- Felicioni, Benigni and Ferrari Dacrema. Automated Off-Policy Estimator Selection via Supervised Learning. https://arxiv.org/abs/2406.18022 (v2).
- Chandak, Liu and Lee. Context-Action Embedding Learning for Off-Policy Evaluation in Contextual Bandits. https://arxiv.org/abs/2509.00648 (v2).
- Cief, Golebiowski, Schmidt, Abedjan and Bekasov (2024). Learning Action Embeddings for Off-Policy Evaluation. ECIR 2024. https://arxiv.org/abs/2305.03954 (v2). Code: https://github.com/amazon-science/ope-learn-action-embeddings at `8729659`.
- Saito, Aihara, Matsutani and Narita (2021). Open Bandit Dataset and Pipeline: Towards Realistic and Reproducible Off-Policy Evaluation. NeurIPS 2021 Datasets and Benchmarks. https://arxiv.org/abs/2008.07146 (v3 and v5). obp 0.5.5, https://pypi.org/project/obp/0.5.5/.
- https://github.com/itsnjstyle27/counterfact at `b626163`, https://github.com/adeoluo/ad-auction-lab at `c93ab28` and https://github.com/aghasalim/recsys-offline-online at `9abef1e` (`obd/AMENDMENTS.md`, "Correction"); https://github.com/sHyanorn/push-lab at `823046b` (`obd` Section 3).
- `obd/PREREGISTRATION.md`, `obd/AMENDMENTS.md`, `obd/results/`, `obd/posthoc/`, `docs/obd-results.md` and `obd_coverage/` of this repository.
