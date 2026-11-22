# Free 25-SKU diagnostic for offline use

[Download the offline diagnostic (ZIP)](https://github.com/hunterrosskonopasek-crypto/catalog-change-review/raw/refs/heads/main/free-tools/25-sku-diagnostic/HWC-Free-25-SKU-Diagnostic.zip). Extract `HWC-Free-25-SKU-Diagnostic.html` and open it in a current desktop browser with JavaScript enabled. The ZIP contains one file. Once you have it, opening the tool, reading a CSV and saving a report all work offline.

1. Choose a UTF-8 CSV containing a header and 1–25 product rows, up to 512 KiB. A fictional sample and a downloadable CSV template are built in.
2. Select your SKU column if prompted. Under **Match optional columns**, select the barcode, selling unit, specification link and both related-card part-number columns available in your export. Fields you skip are identified in the report.
3. Select **Download report (.txt)** to save record numbers, findings and suggested checks. Record 1 is the first data row. **Clear sample** clears the working data from the page.

The screen flags blank or repeated exact SKUs, GTIN format and check-digit errors, missing selling units, missing or malformed specification addresses, and differences between supplied card and destination part numbers. A correctly formatted address still requires a source check to verify the document and its contents. No raw catalog values are included in the downloaded findings.

## Published files

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| Offline ZIP | 8,039 | `75b3743fdd109f7506749c6b8ebf225961078404345f1809fdde2a1cdc49a29b` |
| Extracted HTML | 21,030 | `22955a4a94054ca2d3cdc37b1103dab224c0226801a7bc564e1668e904a595d8` |

The [single-file HTML source](HWC-Free-25-SKU-Diagnostic.html) also contains its license notice. This free offline edition is distributed under [the repository’s MIT license](../../LICENSE).

## Where the checks come from

HWC adapted its public browser parser, diagnostic and sample template from the [hosted Free 25-SKU diagnostic](https://hunterworkflowconsulting.com/free-25-sku-diagnostic). The standalone edition embeds the code, interface, styles and template in one file. Its content security policy disables network connections. The row checks and report format come from the following first-party assets at the time of packaging.

| Production asset | SHA-256 |
| --- | --- |
| [Shared CSV parser and SKU/GTIN checks](https://hunterworkflowconsulting.com/catalog-file-check.js) | `bd4ef3634f0b7c0fe222de5dfaf01ca8bff128bdc2ccd605a50b7d919d3b49c0` |
| [25-row diagnostic and report](https://hunterworkflowconsulting.com/free-25-sku-diagnostic.js) | `6a6608ccd5faa5c5843fe112a4f67dc844a6c1a7b605847413ec677c715578db` |
| [Sample CSV template](https://hunterworkflowconsulting.com/free-25-sku-template.csv) | `87710436cb49aa3d5c64dfabd4453ce1642d339f8748ffd5552c15af2b64ea5a` |
