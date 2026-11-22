# Check an Akeneo import for identifier collisions

[Run the browser check](https://hunterworkflowconsulting.com/akeneo-identifier-check?utm_source=github&utm_medium=readme&utm_campaign=catalog_change_review). Choose a proposed product CSV and, optionally, a current product export from the same PIM. Select the delimiter and identifier column used in both files. Each file can contain up to 5 MiB.

Akeneo documents case-insensitive identifier matching. A supplier's `BX-17` can update a product that the merchant calls `bx-17`. The tool lists the proposed and existing records involved so the owner can check the source before import. It also flags blank keys, repeated keys, edge whitespace and identifiers requiring review beyond ASCII. [Akeneo import guide](https://help.akeneo.com/import-your-data)

The six-row example holds four rows. One proposed key differs in case from an existing key, two proposed rows repeat a key, and one is blank. The other two include an exact update and a new identifier. Download the row decisions as a CSV to send back to the supplier.

For offline use, download this directory and open `preflight.html` beside both JavaScript files. Files are read locally. A report identifies only affected row numbers and reasons. Each finding displays up to ten matching existing rows and the full number of matches. A clean result covers only these identity checks against the supplied files.

Run the regression suite with `node --test akeneo/identity-check.test.js` from the repository root.
