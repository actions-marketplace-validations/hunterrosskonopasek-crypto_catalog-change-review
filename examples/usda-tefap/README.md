# Which fruit catalog rows need a decision?

A distributor updating its reference data may see a long list of edits when a publisher changes how it writes units. We ran Catalog Change Review 1.0.0 on the complete fruit sections of USDA's fiscal 2026 and 2027 TEFAP Foods Available lists, joining on the USDA WBSCM material identifier.

| Check | Result | Reviewer's disposition |
| --- | --- | --- |
| Source pack field, exact text | All 32 continuing fruit identifiers were flagged. | Inspect a representative difference. Empire apples changed from “40 lb case” to “40-pound case.” |
| Pack field after standardizing written pounds, ounces, and dash variants | All 32 continuing identifiers agreed. | Keep the pack values. Quantities, ranges and container types were retained. |
| Roster membership | The 2026 list had 33 fruit identifiers and the 2027 list had 32. Material 100523, Braeburn apples, appeared only in the older list. | Review the current ordering system before changing availability. A change in the annual list does not establish discontinuation. |

## Reproduce the comparison

From the repository root, run each command with the two included extracts. The first uses the original pack text. The second uses the comparable pack field supplied alongside it.

```sh
python3 review.py examples/usda-tefap/fy26-fruit.csv examples/usda-tefap/fy27-fruit.csv --key wbscm_id --field source_pack
python3 review.py examples/usda-tefap/fy26-fruit.csv examples/usda-tefap/fy27-fruit.csv --key wbscm_id --field comparable_pack
```

The CSVs preserve source order. The comparable field changes a number followed by a space or hyphen and “ounce” or “oz” to a number followed by “ oz”, with the same rule for “pound” and “lb”. It also uses a standard dash character in numeric ranges and standardizes whitespace and case. No conversion of numeric values or selling units was performed.

USDA published the FY2026 table in August 2025. The 2026 pack data here were transcribed from the search-indexed original USDA PDF. Its former direct download returned a missing-page response on November 20, 2026. The May 2026 government notice independently lists the 33 fruit entries, including Braeburn apples. FY2027 rows came from the corresponding USDA table retrieved on November 20, 2026. These are public reference data. USDA has not commissioned or endorsed this exercise.

[USDA FY2026 official food list](https://www.fna.usda.gov/tefap/fr-051926) · [FY2026 PDF source address](https://fns-prod.azureedge.us/sites/default/files/resource-files/tefap-fal-fy26.pdf) · [USDA FY2027 food list](https://www.fna.usda.gov/tefap/foods-available)
