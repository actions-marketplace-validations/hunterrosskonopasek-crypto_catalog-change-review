# Catalog CSV Review for WordPress

[Try it in WordPress Playground](https://playground.wordpress.net/?blueprint-url=https%3A%2F%2Fraw.githubusercontent.com%2Fhunterrosskonopasek-crypto%2Fcatalog-change-review%2Fmain%2Fwordpress%2Fblueprint.json) or [download version 1.0.1](https://raw.githubusercontent.com/hunterrosskonopasek-crypto/catalog-change-review/c0194ff7236852cfa6b1a6f24fb2b7a122c22a0c/wordpress/hwc-catalog-review.zip) for a WordPress site you administer.

Open **Tools → Catalog CSV Review**. Click **Try a fictional sample**, or choose a UTF-8 CSV containing 1–25 data rows and up to 512 KiB. Select the SKU column and any optional selling-unit, barcode, specification or part-number columns. Download the review worksheet to see the source values and record numbers for each finding. The checker reads the file inside your browser. It makes no product changes and does not upload the CSV to WordPress.

## Install on your site

Under **Plugins → Add Plugin → Upload Plugin**, select the ZIP, install and activate. Administrators and users with the WooCommerce management capability can open the tool. A site can run the checker with or without WooCommerce.

With [WP-CLI](https://developer.wordpress.org/cli/commands/plugin/install/), run the following from the WordPress root:

```sh
wp plugin install https://raw.githubusercontent.com/hunterrosskonopasek-crypto/catalog-change-review/c0194ff7236852cfa6b1a6f24fb2b7a122c22a0c/wordpress/hwc-catalog-review.zip --activate
```

## Build the ZIP

Run `python wordpress/package.py` from this checkout to assemble the plugin PHP, the repository's existing offline checker and its MIT license. The build uses a fixed archive timestamp and normalized text line endings.

[Worked two-file WooCommerce import review](../examples/woocommerce-import/README.md)
