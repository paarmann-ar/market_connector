
add_shortcode('miviva_category_menu', function () {

    $terms = get_terms([
        'taxonomy'   => 'product_cat',
        'hide_empty' => false,
        'orderby'    => 'name',
        'order'      => 'ASC',
    ]);

    if (is_wp_error($terms) || empty($terms)) {
        return '<!-- No product categories found -->';
    }

    $children = [];

    foreach ($terms as $term) {

        $name = strtolower(trim($term->name));

        // حذف دسته‌های ناخواسته
        if (
            $name === 'uncategorized' ||
            $name === 'uncategorised' ||
            $name === 'unkategorisiert'
        ) {
            continue;
        }

        $parent = (int) $term->parent;

        if (!isset($children[$parent])) {
            $children[$parent] = [];
        }

        $children[$parent][] = $term;
    }

    $render = function ($parent_id = 0) use (&$render, &$children) {

        if (empty($children[$parent_id])) {
            return '';
        }

        $html = '';

        foreach ($children[$parent_id] as $term) {

            $id = (int) $term->term_id;

            $url = get_term_link($term, 'product_cat');

            if (is_wp_error($url)) {
                continue;
            }

            $has_children = !empty($children[$id]);

            $html .= '<li class="' . ($has_children ? 'miviva-has-children' : '') . '">';

            $html .= '<a href="' . esc_url($url) . '">';
            $html .= esc_html($term->name);

            if ($has_children) {
                $html .= ' <span class="miviva-arrow">⌄</span>';
            }

            $html .= '</a>';

            if ($has_children) {
                $html .= '<ul class="miviva-submenu">';
                $html .= $render($id);
                $html .= '</ul>';
            }

            $html .= '</li>';
        }

        return $html;
    };

    return '
        <div class="miviva-menu-wrapper">
            <ul class="miviva-header-dynamic-menu">
                ' . $render(0) . '
            </ul>
        </div>
    ';
});
