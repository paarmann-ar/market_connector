<?php
/**
 * Plugin Name: Rank Math REST API Support
 * Description: Save Rank Math fields from WooCommerce REST API.
 * Version: 1.1
 */
if (!defined('ABSPATH')) {
    exit;
}

add_action('woocommerce_rest_insert_product_object', function ($product, $request, $creating) {

    $meta_data = $request->get_param('meta_data');

    if (empty($meta_data) || !is_array($meta_data)) {
        return;
    }

    foreach ($meta_data as $meta) {

        if (empty($meta['key'])) {
            continue;
        }

        switch ($meta['key']) {

            case 'rank_math_title':
            case 'rank_math_description':
            case 'rank_math_focus_keyword':
            case 'rank_math_canonical_url':

                update_post_meta(
                    $product->get_id(),
                    $meta['key'],
                    $meta['value']
                );

                break;
        }
    }
}, 20, 3);
