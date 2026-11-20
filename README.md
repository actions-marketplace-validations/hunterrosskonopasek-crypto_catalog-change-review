# Catalog Change Review

Catch a case-pack change before a distributor imports its next feed. This tool compares two complete UTF-8 CSV snapshots from the same seller and flags new or removed SKUs, changed pack or selling-unit fields, blank keys, and keys that appear more than once. It runs with Python 3.8 or later using the standard library. Your files stay on the machine where you run it.

## Try the example

```sh
python3 review.py examples/before.csv examples/after.csv
```

The example reports four review items. Before record 1 changes from six units per case to eight. After records 3 and 4 share a key, so that item needs a decision about its selling unit. One item was removed and one added. The tool outputs only record numbers, reason codes, and changed column names. The person reviewing the source decides which changes to approve.

## Use your exports

```sh
python3 review.py approved.csv proposed.csv --key item_id --field unit --field pack_size > review.json
```

The defaults are `sku`, `selling_unit`, and `pack_qty`. Names are case-sensitive. SKU matching preserves case, spaces and leading zeros. Quoted commas and embedded newlines are supported. Record numbers count CSV records after the header, including ignored empty records. Compare complete snapshots with matching coverage. A partial export will mark omitted items as removed.

## Use in GitHub Actions

On a Linux runner with Python 3 and your repository already checked out, add this step. Paths point to the two snapshots in your workflow workspace.

```yaml
- name: Check catalog changes
  uses: hunterrosskonopasek-crypto/catalog-change-review@v1.0.0
  with:
    before: catalog/approved.csv
    after: catalog/proposed.csv
```

The action reports JSON and fails the step on any finding so a reviewer can decide whether to proceed. The local CLI exits successfully with findings unless you add `--fail-on-change`. Exit status 2 indicates invalid input.

Run the test suite with `python3 -m unittest -v`.

[Try a catalog release decision with your team](https://hunter-workflow-consulting.marinegnome.chatgpt.site/catalog-release-rehearsal) or [discuss an HWC catalog diagnostic](https://hunter-workflow-consulting.marinegnome.chatgpt.site/enterprise-catalog). The MIT license applies to the files in this repository.
