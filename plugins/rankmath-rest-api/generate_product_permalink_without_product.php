/**
 * WooCommerce: Remove /product/ or /produkt/ from product URLs
 * + Resolve product URLs without base
 * + 301 redirect old URLs
 * + Rank Math canonical
 */

add_filter( 'post_type_link', function( $url, $post ) {

    if ( 'product' !== $post->post_type ) {
        return $url;
    }

    return home_url( '/' . $post->post_name . '/' );

}, 10, 2 );


/**
 * Allow WordPress to find WooCommerce products
 * when the URL has no /product/ base.
 */
add_action( 'parse_request', function( $wp ) {

    if ( empty( $wp->request ) ) {
        return;
    }

    $path = trim( $wp->request, '/' );

    /*
     * Don't interfere with normal WordPress URLs.
     */
    if ( strpos( $path, '/' ) !== false ) {
        return;
    }

    /*
     * Check if this slug belongs to a WooCommerce product.
     */
    $product = get_page_by_path(
        $path,
        OBJECT,
        'product'
    );

    if ( $product ) {

        $wp->query_vars = array(
            'post_type' => 'product',
            'name'      => $path,
        );
    }

} );


/**
 * Redirect old /product/ and /produkt/ URLs
 * to the new product URL.
 */
add_action( 'template_redirect', function() {

    if ( ! is_404() ) {
        return;
    }

    $path = trim(
        parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ),
        '/'
    );

    $bases = array(
        'product',
        'produkt',
    );

    foreach ( $bases as $base ) {

        if ( strpos( $path, $base . '/' ) !== 0 ) {
            continue;
        }

        $slug = trim(
            substr( $path, strlen( $base ) + 1 ),
            '/'
        );

        if ( ! $slug ) {
            return;
        }

        $product = get_page_by_path(
            $slug,
            OBJECT,
            'product'
        );

        if ( $product ) {

            wp_safe_redirect(
                get_permalink( $product->ID ),
                301
            );

            exit;
        }
    }

} );


/**
 * Rank Math canonical URL.
 */
add_filter( 'rank_math/frontend/canonical', function( $canonical ) {

    if ( is_singular( 'product' ) ) {
        return get_permalink( get_queried_object_id() );
    }

    return $canonical;

} );


/**
 * Fix Rank Math product sitemap URLs
 * Remove /product/ from WooCommerce product URLs.
 */

add_filter( 'rank_math/sitemap/entry', function( $url, $type, $object ) {

    if ( empty( $object ) ) {
        return $url;
    }

    if ( isset( $object->post_type ) && $object->post_type === 'product' ) {

        $url['loc'] = get_permalink( $object->ID );

    }

    return $url;

}, 999, 3 );



/**
 * Force Rank Math Product Sitemap URLs
 * to use WooCommerce product URLs without /product/
 */
add_filter( 'rank_math/sitemap/xml_post_url', function( $url, $post ) {

    if ( ! empty( $post ) && 'product' === $post->post_type ) {
        return home_url( '/' . $post->post_name . '/' );
    }

    return $url;

}, 10, 2 );


/**
 * Disable Rank Math Sitemap caching
 */
add_filter( 'rank_math/sitemap/enable_caching', '__return_false' );