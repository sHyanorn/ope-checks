# Amendments to the pre-registration

`PREREGISTRATION.md` is unchanged since commit `78c077a`. Each entry below was fixed before the run it governs and before any outcome of Section 8 was computed.

## 1. The cells of the notebook run on the Open Bandit Dataset (2026-11-15)

- Text: Section 5, "`blue`: runs the cells of the notebook on the Open Bandit path in their order, with the campaign set in cell 3". The departures listed there do not leave out any cell.
- Change: on the Open Bandit Dataset the adapter runs cells 1, 3, 5, 17, 22, 23, 25, 26, 44 and 45 (counted from 0) in this order. These are the cells that lead from the data to the output of BLUE: the imports, the campaign, the data, the target, the reward model, its shift, the function `BLUE` and its call. Cell 3 sets the campaign. In cell 5 the data path `'./obd/'` is replaced by the directory of the extracted logs; nothing else in it changes. The other code cells are not run:
  - 0, 2, 6, 15, 19, 34 and 38 hold only comments or nothing;
  - 8, 10 to 14, 18, 29, 30, 42 and 53 display values;
  - 28, 31 and 32 compute obp's own estimates with their bootstrap and plot them; BLUE reads nothing they produce;
  - 37 computes `V(π)` with obp from the whole BTS log; departure 6 computes `V_on` in its place;
  - 40 and 41 compare obp's estimates with `V(π)`; 46 and 47 print values of BLUE already computed and repeat it for values of `lambda_`, which BLUE does not use; 48 sets up the plots and 49 holds their colours and labels, 50 draws the paper's figure, 51 defines `BLUE_ablation` and 52 calls it, 54 types in the three values of the ablation, and 55 draws its figure.
- Why: the registration does not say which cells form the path, and departure 6 replaces the value of cell 37. T3 runs cells 0 to 45 in their order on synthetic logs, with only cell 3 changed, and requires every estimate BLUE returns to lie within a relative 1e-9 of the adapter's.
