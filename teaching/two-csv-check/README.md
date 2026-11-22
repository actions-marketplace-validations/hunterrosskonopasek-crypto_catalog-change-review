# Which catalog changes can you verify?

**25-minute paired exercise for adult learners.** A supplier has sent a new catalog. Your team must tell the person importing it what changed, what stayed the same, and which questions need an answer first.

You'll use two small fictional CSV files and a spreadsheet. A CSV is a text file with one record per line in these examples and commas between the values. You can run the entire activity offline once you have the files. No Python, account, or prior catalog experience is needed for learners.

## Prepare the two sheets · 5 minutes

1. Download [before.csv](https://raw.githubusercontent.com/hunterrosskonopasek-crypto/catalog-change-review/main/examples/before.csv) and [after.csv](https://raw.githubusercontent.com/hunterrosskonopasek-crypto/catalog-change-review/main/examples/after.csv). If a link shows text, save the page as a CSV. A facilitator can also give learners the two files from the repository's `examples` folder.
2. Open or import the files in Excel or LibreOffice Calc, one sheet or window per file. Use a comma as the separator and keep the `sku` column as **text** in both. In Excel use **Data → From Text/CSV → Transform Data** and set the SKU column to **Text** before loading. If Excel has already added a **Changed Type** step, remove it before setting the text type. In Calc's **Text Import** preview, select the first column and choose **Text** as its column type. Keep the original row order.
3. Check the first two SKU cells in each sheet. One must read `0017` and the other `17`. If they look identical, reopen the original CSV with the text setting. You can also read the original files in a plain-text editor.

The `sku` is the product's identifier. The `selling_unit` tells you whether a buyer orders an individual item or a case. The `pack_qty` is the number of items in that selling unit. Treat the two files as complete snapshots of the same fictional catalog for this exercise.

## Gather the evidence · 10 minutes

Work in pairs. One person reads the earlier file and one reads the later file. On paper or a blank sheet, make columns for **SKU**, **before record(s)**, **after record(s)**, **what you observed**, and **what to ask**. Count the first row below the column names as record 1. You can write “absent” when a file has no row for a SKU.

1. Start with the first SKU in the earlier file. Find **every** exact match in the later file. Inspect the selling unit and pack quantity for each matching record. Repeat for the other earlier SKUs.
2. Work back from the later file now. Add any identifier you have not recorded. For a repeated identifier, record both later record numbers and their values in the same entry.
3. Write a sentence for each identifier. Name the file, record and value that support it. Include one identifier whose selling unit and quantity stayed the same.

## Make a handoff · 6 minutes

Choose one change the catalog owner should review before import. Write a two-sentence note. First say what the files show. Then ask for the specific document or decision you would need to tell which value belongs in the catalog. Trade notes with another pair. Can they find the records using your note alone?

## Try a missing value · 4 minutes

Make a temporary copy of the later sheet. In record 1, clear **only** the `pack_qty` cell. Leave the SKU and selling unit in place. What can you report about that SKU now? Is there a row for it? Is there a known later quantity? Compare your answer with a case where the SKU has no later row. Leave the original CSVs intact.

[Facilitator guide, worked answers and Python cross-check](facilitator-key.md)
