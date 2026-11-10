# Amendments to the pre-registration

`PREREGISTRATION.md` is unchanged since commit `08ab8da`. Each entry fixes how one of its sentences is read where the text allows two readings or leaves a case open. All entries were fixed before any outcome of a confirmatory campaign (All, Women's) was computed; none is post hoc (Section 9).

## 1. Replicates in which a quantity is undefined

- Text: Section 5, "Intervals are the 2.5th and 97.5th percentiles of the replicates". It does not say what happens when a quantity cannot be computed in a replicate (a zero denominator).
- Reading: such replicates are left out of the percentiles, and the number left out is reported for every quantity. A quantity behind a label that is undefined in more than 1% of the replicates gets no label; it is reported as "not evaluable" with the reason.
- Why: stopping instead would leave the one confirmatory run of Section 4 unfinished after clicks had been read.

## 2. H5, the difference (iii) minus (ii)

- Text: Section 7, "the difference (iii) minus (ii) uses only rows that have both windows".
- Reading: the rows of `R` whose windows (ii) and (iii) both hold a row of `B` at the row's position are selected first. Both estimates are recomputed on these rows, with the weights renormalised over the `(h, k)` that keep a row, and then subtracted. The estimates (ii) and (iii) reported on their own each use their own rows.
- Why: the alternative, subtracting estimates computed on different rows, would mix the effect of the window with the effect of the selection.

## 3. Comparisons of an interval with a value

- Text: the rules of H2 to H6 ("contains", "lies below", "lies above", "excludes", "half-width").
- Reading: an interval `[L, U]` contains `x` if `L <= x <= U`, lies below `x` if `U < x`, lies above `x` if `L > x`, and excludes `x` if it does not contain it. The half-width of H6 is `(U - L) / 2`.
- Why: the literal reading, stated so that boundary cases have one answer.

## 4. H2, rows off the 1/200,000 grid

- Text: Section 6, "the number of rows [...] off the 1/200,000 grid". No tolerance is given.
- Reading: a row is off the grid if `|200,000 p - round(200,000 p)| >= 1e-4`.
- Why: the tolerance behind the 99.96% of Section 3. The count is reported and enters no rule.

## 5. Exploratory item

- Text: Section 7, the paragraph "Exploratory, no verdict".
- Reading:
  - rows outside the week are removed before the rows are sorted;
  - the median of `x` in an (item, position) cell is taken over the rows of complete impressions in that cell;
  - "above the median" means strictly greater;
  - in a replicate the click rate of all rows of complete impressions and the weights of the cells are recomputed, as Section 5 requires of sums and counts.
- Why: `x` is defined only for rows of complete impressions, and Section 2 leaves rows outside the week out of every quantity.

## 6. Section 2, one more stop condition

- Text: Section 2 says "Three positions" and lists the conditions that stop the run of a campaign. A position value other than 1, 2 or 3 is not among them.
- Change: the run of a campaign also stops if a row has a position other than 1, 2 or 3. It is checked with the other conditions, before any click is read.
- Why: every estimator indexes positions 1 to 3; a file that breaks this cannot be analysed as registered.
