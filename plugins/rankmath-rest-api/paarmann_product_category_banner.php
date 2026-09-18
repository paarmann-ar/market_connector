add_action( 'woocommerce_before_main_content', 'paarmann_product_category_banner', 5 );

function paarmann_product_category_banner() {

    if ( ! is_product_category() ) {
        return;
    }

    $term = get_queried_object();

    $thumbnail_id = get_term_meta( $term->term_id, 'thumbnail_id', true );

    if ( ! $thumbnail_id ) {
        return;
    }

    $image = wp_get_attachment_image_url( $thumbnail_id, 'full' );

    ?>
    <div class="paarmann-category-banner"
         style="background-image:url('<?php echo esc_url($image); ?>');">
        <div class="paarmann-overlay">
            <h1><?php single_term_title(); ?></h1>

            <?php
            $description = term_description();

            if ( $description ) {
                echo '<div class="paarmann-description">'.$description.'</div>';
            }
            ?>
        </div>
    </div>
    <?php
}