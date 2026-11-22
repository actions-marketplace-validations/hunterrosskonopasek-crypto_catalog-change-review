# Review selling units before an OroCommerce product import

A distributor sells labels individually and in cartons. It maps a single label to Oro’s `item` unit and a carton to `set`. The proposed product file changes a carton from 24 labels to 12. The USD price list still offers a set for $30 when a buyer orders at least five sets.

**Buying 120 labels as sets would cost $300 instead of $150.** Five approved sets × $30 cover 120 labels. The proposed conversion requires ten sets × $30 for the same 120. This calculation assumes the same effective price list, no intervening tier or promotion, and a buyer who selects sets. Oro prices each unit separately. It does not turn an order for 120 individual labels into an order for sets. [Oro product units and pricing](https://doc.oroinc.com/user/back-office/products/products/product-units/)

## Reproduce the comparison

The [approved units](approved-units.csv) and [proposed units](proposed-units.csv) are five fictional products projected onto the unit fields in Oro’s product CSV template. The [price-list extract](price-list.csv) uses the separate price-list headers and stays fixed in this exercise. These are review inputs. For a real import, obtain the target instance’s full template and use Oro’s **Validate** step. [Product import template](https://doc.oroinc.com/user/back-office/products/products/import-products/) · [Price-list import template](https://doc.oroinc.com/user/back-office/sales/price-lists/import/)

From the repository root, run

```sh
sample=examples/orocommerce-product-units
compare_units() {
  python3 review.py "$sample/approved-units.csv" "$1" \
  --field 'primaryUnitPrecision.unit.code' \
  --field 'primaryUnitPrecision.precision' \
  --field 'primaryUnitPrecision.conversionRate' \
  --field 'primaryUnitPrecision.sell' \
  --field 'additionalUnitPrecisions:0:unit:code' \
  --field 'additionalUnitPrecisions:0:precision' \
  --field 'additionalUnitPrecisions:0:conversionRate' \
  --field 'additionalUnitPrecisions:0:sell'
}
compare_units "$sample/proposed-units.csv" | diff -u "$sample/expected-findings.json" -
compare_units "$sample/reviewed-units.csv"
```

The first report matches [the checked output](expected-findings.json). Record numbers count data rows starting at 1 and exclude the header. The second report compares [the reviewed file](reviewed-units.csv) with the baseline and leaves one documented change, on record 4.

| Record / SKU | Proposed change | Evidence and decision |
| --- | --- | --- |
| 1 · LABEL-24 | Set conversion 24 → 12 items | The distributor’s fictional carton specification still says 24. Restore 24. The five-set tier applies to sets ordered, so the price file alone cannot catch this discrepancy. |
| 2 · CLIP-12 | Primary `item` sell flag 1 → 0 | The distributor still accepts individual orders. Restore 1. A $0.60 item price can remain in a list even when the product’s Sell setting hides that unit. |
| 3 · CAP-06 | Set quantity precision 0 → 1 | The warehouse ships sealed sets of six. Restore 0. A precision of 1 permits quantities in tenths, including 0.5 set. It does not mean there is one item per set. |
| 4 · RING-08 | Set conversion 8 → 10 items | The fictional signed packing revision approves ten rings per set and the existing $15 set price. Keep 10. Retain that approval with the import. |
| 5 · TRAY-04 | Unit fields unchanged | The supplied list shows only an item price. Check the customer’s effective price for a set before promising that price or concluding it is missing. |

For a customer review, verify the approved packaging revision, account, website, effective price list, currency, tiers and exact order unit. The CLI compares the product fields you pass. It does not look up the live store, compute prices or approve changes. The example has one additional unit per SKU. When source products have several, match them by unit code across exports before interpreting a difference in an indexed column such as `additionalUnitPrecisions:0:conversionRate`.

For one distributor, HWC’s $750 managed pilot reviews an authorized category of up to 500 SKUs and returns an editable findings file plus five worked examples with source evidence. [Scope the $750 pilot](https://hunterworkflowconsulting.com/data-audits?utm_source=github&utm_medium=worked_example&utm_campaign=oro_product_unit_review#catalog)
