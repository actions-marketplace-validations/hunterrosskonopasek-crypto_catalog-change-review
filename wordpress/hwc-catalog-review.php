<?php
/**
 * Plugin Name: Catalog CSV Review
 * Description: Check up to 25 catalog rows in your browser before a WooCommerce import. Download the findings without uploading the source CSV.
 * Version: 1.0.0
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Author: Hunter & Co. Workflow Consulting
 * License: MIT
 * Update URI: https://github.com/hunterrosskonopasek-crypto/catalog-change-review
 */

defined( 'ABSPATH' ) || exit;

function hwc_catalog_review_capability() {
	return current_user_can( 'manage_woocommerce' ) ? 'manage_woocommerce' : 'manage_options';
}

function hwc_catalog_review_menu() {
	add_management_page(
		'Catalog CSV Review',
		'Catalog CSV Review',
		hwc_catalog_review_capability(),
		'hwc-catalog-review',
		'hwc_catalog_review_page'
	);
}
add_action( 'admin_menu', 'hwc_catalog_review_menu' );

function hwc_catalog_review_page() {
	if ( ! current_user_can( hwc_catalog_review_capability() ) ) {
		wp_die( esc_html__( 'You do not have permission to access this page.' ) );
	}
	$checker = plugins_url( 'catalog-review.html', __FILE__ );
	?>
	<div class="wrap">
		<h1>Catalog CSV Review</h1>
		<p>Before a WooCommerce import, check a small export for duplicate SKUs, missing selling units and identifier problems. Select the columns that match your export. Your file stays in your browser.</p>
		<p><a href="<?php echo esc_url( $checker ); ?>" target="_blank" rel="noopener noreferrer">Open the checker in its own tab</a> &middot; <a href="https://hunterworkflowconsulting.com/shopify-plus-pim-agency-partner-program?utm_source=wordpress&amp;utm_medium=plugin&amp;utm_campaign=woocommerce_import_qa#woocommerce-migration-qa" target="_blank" rel="noopener noreferrer">See a worked WooCommerce import review</a></p>
		<iframe title="Local catalog CSV checker" src="<?php echo esc_url( $checker ); ?>" sandbox="allow-scripts allow-downloads" width="100%" height="900" style="border:0"></iframe>
	</div>
	<?php
}
