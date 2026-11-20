# Five product codes from a grocery supplier table

Two chocolate-chip entries list the same flavor, 5.1-ounce weight and six-bar count. Their identifiers differ. A distributor that merges these rows by description would lose a source identifier.

[Download the five-row CSV](packaged-goods-identifier-sample.csv). Import the raw identifier and normalized GTIN columns as **text** to preserve leading zeroes.

| Rows | Import decision |
|---|---|
| F01 | Keep the 14-digit value on the 63-bar package row. |
| F02 and F03 | Keep each identifier on its own source row. Left-pad F02 for a 14-character comparison key and retain both leading zeroes in F03. The source owner can resolve whether the rows represent variants, aliases or another relationship. |
| F04 | Preserve the alphanumeric code for a future crosswalk. Its identifier scheme needs confirmation. |
| F05 | The source’s identifier column contains a package description. Keep the raw cell, leave the normalized key empty and ask the supplier for the identifier. |

The three numeric entries passed a GS1 modulo-10 check. Starting immediately left of the check digit, alternate weights of three and one moving left. The check digit brings the weighted sum to a multiple of ten. A passing digit checks the arithmetic. Product assignment and ownership need separate evidence. The 14-character key here is a storage format. A distributor’s internal SKU would come from its own item master. [GS1 on GTIN representation](https://support.gs1.org/support/solutions/articles/43000734355-what-is-the-required-format-of-gtin-in-gs1-edi-standards-)

**Source and scope.** Riverside Natural Foods identified the brand as MadeGood in its December 9, 2024 announcement, published by FDA on December 10. The sample selects five historical table rows for catalog import training. Current stock, lot and date eligibility, and recall decisions are outside its scope. Each CSV row links to the original notice. [Riverside announcement hosted by FDA](https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/riverside-natural-foods-inc-issues-voluntary-recall-select-madegood-granola-bar-products-over)

## Apply the same checks to a supplier feed

HWC’s $750 fixed-price normalization pilot covers up to 500 authorized source rows and the fields agreed in writing. Send the product family, row count and deadline to get a written scope and available start date. The signed order and cleared payment precede delivery. [Pilot terms and order form](https://hunter-workflow-consulting.marinegnome.chatgpt.site/enterprise-catalog#normalization) · [Request a written scope](https://form.jotform.com/263065301224041?q4_textarea2=I%20found%20the%20five%20grocery%20identifier%20rows%20on%20GitHub.%20I%20would%20like%20a%20written%20scope%20for%20the%20%24750%20supplier-file%20normalization%20pilot.%20Product%20family%2C%20row%20count%2C%20fields%20and%20deadline%3A%20)
