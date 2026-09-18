
add_shortcode( 'miviva_dynamic_menu', function() {

    $categories = get_terms( array(
        'taxonomy'   => 'product_cat',
        'hide_empty' => true,
        'parent'     => 0,
        'orderby'    => 'name',
        'order'      => 'ASC',
    ) );

    if ( empty( $categories ) || is_wp_error( $categories ) ) {
        return '';
    }

    $output = '<ul class="miviva-header-dynamic-menu">';

    foreach ( $categories as $category ) {

        $children = get_terms( array(
            'taxonomy'   => 'product_cat',
            'hide_empty' => true,
            'parent'     => $category->term_id,
            'orderby'    => 'name',
            'order'      => 'ASC',
        ) );

        $output .= '<li>';

        $output .= '<a href="' . esc_url( get_term_link( $category ) ) . '">';
        $output .= esc_html( $category->name );

        if ( ! empty( $children ) && ! is_wp_error( $children ) ) {
            $output .= ' <span aria-hidden="true">⌄</span>';
        }

        $output .= '</a>';

        if ( ! empty( $children ) && ! is_wp_error( $children ) ) {

            $output .= '<ul class="miviva-submenu">';

            foreach ( $children as $child ) {

                $output .= '<li>';
                $output .= '<a href="' . esc_url( get_term_link( $child ) ) . '">';
                $output .= esc_html( $child->name );
                $output .= '</a>';
                $output .= '</li>';

            }

            $output .= '</ul>';
        }

        $output .= '</li>';
    }

    $output .= '</ul>';

    return $output;
} );


add_action( 'wp_head', function() {
    ?>
    <style>

        .miviva-header-dynamic-menu {
            display: flex;
            align-items: center;
            gap: 28px;
            margin: 0;
            padding: 0;
            list-style: none;
        }

        .miviva-header-dynamic-menu > li {
            position: relative;
            list-style: none;
        }

        .miviva-header-dynamic-menu > li > a {
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 12px 0;
            text-decoration: none;
            font-weight: 500;
            color: inherit;
            white-space: nowrap;
        }

        .miviva-header-dynamic-menu .miviva-submenu {
            position: absolute;
            top: 100%;
            left: 0;
            min-width: 240px;
            padding: 15px 0;
            margin: 0;
            background: #fff;
            box-shadow: 0 10px 35px rgba(0,0,0,.12);
            border-radius: 8px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(8px);
            transition: all .2s ease;
            z-index: 99999;
            list-style: none;
        }

        .miviva-header-dynamic-menu li:hover > .miviva-submenu {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .miviva-header-dynamic-menu .miviva-submenu li {
            list-style: none;
        }

        .miviva-header-dynamic-menu .miviva-submenu a {
            display: block;
            padding: 9px 20px;
            color: #222;
            text-decoration: none;
            white-space: nowrap;
        }

        .miviva-header-dynamic-menu .miviva-submenu a:hover {
            background: #f7f7f7;
        }

        @media (max-width: 767px) {
            .miviva-header-dynamic-menu {
                display: none;
            }
        }

    </style>
    <?php
} );
