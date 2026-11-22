# Facilitator guide and worked answers

[Open the 25-minute learner exercise](README.md). Give pairs the two original CSVs. For a group without spreadsheet software, print the files in a fixed-width font or read each row aloud with its record number. Learners can keep the evidence log on paper. The exercise needs no color cues, formulas or sign-in.

At minute 5, ask someone to read the first two identifiers digit by digit. At minute 15, invite a pair to report one changed quantity and another pair to report a repeated identifier. At minute 21, give everyone the missing-value variation. Use the last minute to collect one observation and one unresolved question from each pair.

## Original files

There are **4 data records before and 5 after**. Across both files there are five distinct identifiers. One identifier is unchanged. The Python tool reports **four findings**.

| SKU | Before record(s) and values | After record(s) and values | What the evidence supports |
| --- | --- | --- | --- |
| `0017` | 1 · case, 6 | 1 · case, 8 | The listed case quantity changed from 6 to 8. Request the approved pack specification or supplier change notice before using 8. |
| `17` | 2 · each, 1 | 2 · each, 1 | Both compared fields match. This SKU is distinct from `0017`. It produces no finding. |
| `A-09` | 3 · case, 8 | 3 · case, 8 and 4 · each, 1 | The later file assigns two different selling units to the same identifier. Ask how cases and individual units should be identified before picking a row. |
| `OLD-8` | 4 · each, 1 | Absent | This SKU appears only in the earlier snapshot. Confirm whether it was retired before removing it from a purchasing list. |
| `NEW-2` | Absent | 5 · each, 1 | This SKU appears only in the later snapshot. Confirm its approval or start date before making it available to order. |

A model handoff reads, “Earlier record 3 lists A-09 as a case of 8, while later records 3 and 4 list that SKU as both a case of 8 and an individual item. Which identifiers does your approved item master assign to those two selling units?” Accept different wording when a learner identifies the exact source records and asks a question the files leave open.

## Missing-value variation

In the edited copy, later record 1 still includes SKU `0017` and selling unit `case`. The quantity cell is empty. The earlier file gives 6. The later file provides no quantity. A blank does not establish zero or show whether someone intended to clear the quantity. Ask for the current approved pack count. By contrast, the later file has no record at all for `OLD-8`.

A “removed” finding describes a SKU absent from the supplied later snapshot. Inferring a discontinued product requires outside evidence. A partial export would also make omitted items appear removed. Ask learners how they would confirm coverage before repeating the exercise with workplace files.

## Reproduce the results with Python

Run these commands from the repository root using Python 3.8 or later. The utility uses the standard library and reads the files locally.

```sh
python3 review.py examples/before.csv examples/after.csv
python3 -m unittest -v test_review
```

The command uses `sku` to match rows and compares `selling_unit` and `pack_qty`. The original files yield these machine results in this order.

| Reason in output | Before record(s) | After record(s) | Changed columns |
| --- | --- | --- | --- |
| `changed` | 1 | 1 | `pack_qty` |
| `ambiguous_key` | 3 | 3 and 4 | None listed |
| `removed` | 4 | None | None listed |
| `added` | None | 5 | None listed |

The program returns counts, reason codes, column names and record numbers. Learners must consult the sources to tell 6 from 8. For the variation, save a separate copy as `after-blank.csv` in the repository root and run `python3 review.py examples/before.csv after-blank.csv`. The four reason counts and record references remain the same. Record 1 still produces a `changed` finding for `pack_qty`; this time the later cell is empty. A blank **quantity** on this matched SKU does not produce a `missing_key` finding. That reason concerns an empty SKU.

In a successful handoff, the learner preserves both numeric-looking IDs, finds each record for the repeated ID, and separates a supported observation from a decision that needs the catalog owner.
