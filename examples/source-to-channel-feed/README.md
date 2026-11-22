# Where did the pack quantity change?
A merchant sees a case of six in a channel feed. The supplier may have approved six, or a later rule may have changed twelve to six. The following three fictional, same-release exports show how to locate the first observed difference before assigning work to a catalog owner or feed specialist.

The [approved supplier reference](approved.csv) is the expected listing for this exercise. The [merchant export](merchant.csv) is the input to the channel transformation. The [proposed channel feed](channel.csv) is the file to be published. All three use the same SKU, selling unit and pack-quantity definitions. Keep the four-digit identifiers as text.

| SKU | Approved | Merchant | Channel | Evidence and action |
| --- | --- | --- | --- | --- |
| 0017 | Case of 6 | Case of 4 | Case of 4 | The first difference is present in the merchant export. Ask the catalog owner to reconcile its pack quantity with the approved record. Both comparisons use data record 1. |
| 0018 | Case of 12 | Case of 12 | Case of 6 | The first difference appears between the merchant and channel files. Ask the feed operator for the transformation or override that produced record 2. |
| 0019 | Case of 10 | Each | Case of 10 | The channel agrees with the reference, but merchant record 3 differs. Ask whether there is an approved channel override before changing either layer. |
| 0020 | Each | Each | Each | All three record 4 values agree. |
| 0021 | Case of 4 | Case, quantity blank | Case of 4 **and** each | Merchant record 5 has an unknown quantity. Channel records 5 and 6 share the same key. Hold the match until the owner supplies the intended variant identifiers and quantity. |

## Reproduce the findings
Run these from the repository root with Python 3.8 or later. Record numbers count data records after the header.

```sh
python3 review.py examples/source-to-channel-feed/approved.csv examples/source-to-channel-feed/merchant.csv
python3 review.py examples/source-to-channel-feed/merchant.csv examples/source-to-channel-feed/channel.csv
```

The first command reports three changed keys. The second reports two changed keys and one ambiguous key. For record 3, inspect both the selling unit and pack quantity. The commands run locally and leave the inputs intact.

To use this with a real release, first confirm which reference the buyer approved, the timestamp of each export, the channel's intended selling unit and whether channel-specific overrides exist. The files identify where values first differ. The change history and rule owner establish why. A data-only review needs authorized exports, not access to a live store.

[Request a managed review for one product family](https://hunterworkflowconsulting.com/data-audits#catalog).
