# Check a kit’s component quantities before a Znode import

A kit calls for four gaskets. The proposed distributor file lists two. Both SKUs exist, and two is a valid number. Finding that discrepancy takes an approved bill of materials. In this fictional example, a 30-kit run would differ by 60 gaskets at the proposed quantity.

## Inspect the result

Open the [editable review CSV](expected-review.csv) for all eight records. Two match the supplied references and six need review.

| Proposal record | What the reviewer sees | Decision |
| --- | --- | --- |
| 1 and 3 | Two different components belong to KIT-710. Each quantity agrees with the approved bill. | Match both. A repeated parent is expected. |
| 2 | KIT-710 requests two GSK-004 gaskets. The approved bill specifies four. | Confirm the quantity with the kit owner. |
| 4 | KIT-710 has no quantity for BRK-030. | Obtain the approved bundle quantity. |
| 5 | The reference contains SKU 00017. The proposal says 17. | Confirm the exact identifier and export coverage. |
| 6 | CLP-100 exists, but the supplied bill associates it with KIT-720. | Request evidence for its proposed use in KIT-710. |
| 7 and 8 | The same parent and child appear twice, with different display orders. | Have the owner choose the intended row. |

## Run or edit the example

Download and extract the [current project ZIP](https://github.com/hunterrosskonopasek-crypto/catalog-change-review/archive/refs/heads/main.zip), or use your existing clone. With Python 3.8 or later, run from the directory containing the top-level README:

~~~sh
python3 examples/znode-bundle-associations/preflight.py
~~~

The command reads the [seven-product snapshot](products.csv), the [kit owner’s approved bill](approved-bom.csv) and the [proposed relationships](proposed.csv). It writes a CSV to standard output. To save your own worksheet, append `> my-review.csv`. Import the SKU columns as **text** when opening CSVs in Excel to retain the leading zeros.

Try changing the proposed GSK-004 quantity from 2 to 4 in a copy of the proposal. That row should switch to MATCH, leaving five rows for review.

~~~sh
python3 examples/znode-bundle-associations/preflight.py --proposed my-proposed.csv
~~~

You can also supply separate UTF-8 files with `--products` and `--bom`. Use the example headers. The reference product file needs unique SKUs, and the approved bill needs a unique parent/child pair per row. Use the `BundleProduct` and `SimpleProduct` product type codes shown in the example. Keep one SKU namespace and use the same kit revision. A missing SKU means the supplied snapshot did not establish the relationship. The component might already exist in a larger catalog.

## Compare component units

When the source files state a unit, include the kit owner's unit column in the bill and the import's unit column in the proposal. For example, use `ApprovedUOM` in the bill and `ProposedUOM` in the proposal. Two cases of twelve and two individual pieces have the same numeric quantity. The checker flags the different units for the kit owner to reconcile.

Each file can use `UOM`, `Unit`, `Units`, `UnitOfMeasure`, `ComponentUOM` or `QuantityUnit`. The bill can also use `ApprovedUnit` or `ApprovedUnitOfMeasure`, and the proposal can use `ProposedUnit` or `ProposedUnitOfMeasure`. Case, spacing and underscores in those headings are interchangeable. Choose one unit column per file. Unit values are case-sensitive because `mW` and `MW` can be different units. Surrounding whitespace is ignored for comparison.

If either file supplies a unit column, the report appends `proposed_uom` and `approved_uom` with the original source values. Missing or different units on a linked pair require review. The checker leaves quantities in their supplied units and makes no conversions. Files without unit columns retain the original report headings. A match then establishes the supplied IDs and numeric quantity only.

## What the check covers

Znode V10 documents one Product Association Import row per relationship. Both SKUs must exist. The file includes display order and a default indicator, and bundled products require component quantity. Review the current template exported from your own environment. [Znode V10 bulk import documentation, Product Association Import](https://support.znode.com/support/solutions/articles/43000757074-bulk-importing-and-updating-data)

This HWC check uses the published field names and adds two independent checks against the kit owner’s bill: proposed quantities and repeated parent/child pairs. Each MATCH applies only to the proposed row and the two files provided. An omitted component stays outside this row-by-row review. The worksheet does not determine which component should be the default or predict an import result. The script runs offline and has no connection to Znode. All SKUs, quantities and relationships here are fictional.

## Scope a distributor pilot

For one product family and up to 500 authorized SKUs, the **$750 catalog pilot** delivers an editable list of findings and five worked examples with source evidence. Send the product family, approximate SKU count and planned import date. HWC confirms scope and file handoff before payment. [Request the $750 pilot](https://hunterworkflowconsulting.com/data-audits?utm_source=github&utm_medium=worked_example&utm_campaign=znode_bundle_associations#catalog)
