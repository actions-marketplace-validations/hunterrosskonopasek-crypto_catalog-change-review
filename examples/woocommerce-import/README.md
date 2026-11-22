# Review a WooCommerce family before import

A merchant expects black, blue and green tray variations. An agency has prepared a replacement import. These two fictional exports each contain six records. The record counts agree, but one color disappears, a different SKU appears twice and the unit on a surviving variation changes.

Download [the runnable example ZIP](https://codeload.github.com/hunterrosskonopasek-crypto/catalog-change-review/zip/9c8579bf1d57c49e58749821d904039d670dacb9) and extract it. It includes the comparison tool, [source family](source-family.csv) and [proposed import](proposed-import.csv). From the extracted repository folder, run the comparison with the actual WooCommerce header names.

```sh
python3 review.py examples/woocommerce-import/source-family.csv examples/woocommerce-import/proposed-import.csv --key SKU --field Type
```

The command returns one removed key and one ambiguous key. It compares the SKU and Type columns. Check the named unit columns separately because the proposed file stores the unit under a different header.

| Reproduce the observation | Decision for the developer |
|---|---|
| Find TRAY-GREEN in source data record 4. Search the proposed SKU column for the same key. | Ask the merchant whether green should remain available or has an approved replacement identifier. |
| Filter the proposed SKU column to CLIP-10. Records 4 and 5 both match. | Establish which source row each record should represent before updating either item. |
| Compare source record 3, Selling unit, with proposed record 3, Meta: selling_unit. Both represent TRAY-BLUE. | Verify which package a customer receives before approving the change from CASE to EACH. |

Keep 000042 as text. The parent product also has a different numeric ID in each snapshot. Resolve each parent inside its own file and compare its SKU. WooCommerce documents how IDs and SKUs are used during an import. [WooCommerce CSV importer and exporter](https://woocommerce.com/document/product-csv-importer-exporter/)

## Have a merchant import scheduled?

HWC’s $750 prepaid migration QA pilot covers one authorized product family and up to 100 data rows combined across the two files. The agency receives an exceptions CSV, a reproducible check for each finding and a developer handoff. The agency approves changes with its merchant and controls deployment.

Include the family, each file’s row count and the planned import date in your request. The parties confirm permission, timing and a written order before HWC invoices. Keep merchant exports in the agreed private transfer channel. [View the worked findings and request the pilot](https://hunterworkflowconsulting.com/shopify-plus-pim-agency-partner-program?utm_source=github&utm_medium=marketplace&utm_campaign=woocommerce_import_qa#woocommerce-migration-qa)
