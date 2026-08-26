/**
 * WordPress – Unused Media Scanner
 *
 * Safe manual deletion tool.
 *
 * The scanner reports potentially unused images.
 * Nothing is deleted automatically.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}


/**
 * Add scanner to WordPress Tools menu.
 */
add_action( 'admin_menu', function () {

    add_management_page(
        'Unused Media Scanner',
        'Unused Media Scanner',
        'manage_options',
        'unused-media-scanner',
        'pt_unused_media_scanner_page'
    );

} );


/**
 * Check whether an attachment is used.
 */
function pt_media_attachment_is_used( $attachment_id ) {

    global $wpdb;

    $attachment_id = absint( $attachment_id );

    if ( ! $attachment_id ) {
        return true;
    }


    /**
     * Only check image attachments.
     */
    if ( 'attachment' !== get_post_type( $attachment_id ) ) {
        return true;
    }


    /**
     * ---------------------------------------------------------
     * 1. Check Featured Images.
     * ---------------------------------------------------------
     */
    $found = $wpdb->get_var(
        $wpdb->prepare(
            "SELECT post_id
             FROM {$wpdb->postmeta}
             WHERE meta_key = '_thumbnail_id'
             AND meta_value = %d
             LIMIT 1",
            $attachment_id
        )
    );

    if ( $found ) {
        return true;
    }


    /**
     * ---------------------------------------------------------
     * 2. Check WooCommerce Product Gallery.
     * ---------------------------------------------------------
     */
    $gallery_rows = $wpdb->get_results(
        "SELECT post_id, meta_value
         FROM {$wpdb->postmeta}
         WHERE meta_key = '_product_image_gallery'"
    );


    if ( ! empty( $gallery_rows ) ) {

        foreach ( $gallery_rows as $row ) {

            $gallery_ids = array_filter(
                array_map(
                    'absint',
                    explode( ',', $row->meta_value )
                )
            );


            if ( in_array( $attachment_id, $gallery_ids, true ) ) {
                return true;
            }
        }
    }


    /**
     * ---------------------------------------------------------
     * 3. Check post/page/product content for image URL.
     * ---------------------------------------------------------
     */
    $attachment_url = wp_get_attachment_url( $attachment_id );


    if ( $attachment_url ) {

        $url_variations = array_unique(
            array_filter(
                array(
                    $attachment_url,
                    esc_url( $attachment_url ),
                    str_replace( 'https://', 'http://', $attachment_url ),
                    str_replace( 'http://', 'https://', $attachment_url ),
                )
            )
        );


        foreach ( $url_variations as $url ) {

            $found = $wpdb->get_var(
                $wpdb->prepare(
                    "SELECT ID
                     FROM {$wpdb->posts}
                     WHERE post_content LIKE %s
                     LIMIT 1",
                    '%' . $wpdb->esc_like( $url ) . '%'
                )
            );


            if ( $found ) {
                return true;
            }
        }
    }


    /**
     * ---------------------------------------------------------
     * 4. Check attachment ID in post meta.
     * ---------------------------------------------------------
     */
    $found = $wpdb->get_var(
        $wpdb->prepare(
            "SELECT post_id
             FROM {$wpdb->postmeta}
             WHERE meta_value = %s
             LIMIT 1",
            (string) $attachment_id
        )
    );


    if ( $found ) {
        return true;
    }


    /**
     * ---------------------------------------------------------
     * 5. Check serialized/meta references.
     * ---------------------------------------------------------
     */
    $id_string = '"' . $attachment_id . '"';


    $found = $wpdb->get_var(
        $wpdb->prepare(
            "SELECT post_id
             FROM {$wpdb->postmeta}
             WHERE meta_value LIKE %s
             LIMIT 1",
            '%' . $wpdb->esc_like( $id_string ) . '%'
        )
    );


    if ( $found ) {
        return true;
    }


    /**
     * ---------------------------------------------------------
     * 6. Check attachment parent.
     * ---------------------------------------------------------
     */
    $parent_id = wp_get_post_parent_id( $attachment_id );


    if ( $parent_id ) {
        return true;
    }


    /**
     * ---------------------------------------------------------
     * 7. Check filename in post content.
     * ---------------------------------------------------------
     */
    $metadata = wp_get_attachment_metadata( $attachment_id );


    if ( $metadata && ! empty( $metadata['file'] ) ) {

        $file_name = wp_basename( $metadata['file'] );


        if ( $file_name ) {

            $found = $wpdb->get_var(
                $wpdb->prepare(
                    "SELECT ID
                     FROM {$wpdb->posts}
                     WHERE post_content LIKE %s
                     LIMIT 1",
                    '%' . $wpdb->esc_like( $file_name ) . '%'
                )
            );


            if ( $found ) {
                return true;
            }
        }
    }


    /**
     * No usage was found.
     */
    return false;
}


/**
 * Get all image attachments.
 */
function pt_get_all_image_attachments() {

    return get_posts(
        array(
            'post_type'      => 'attachment',
            'post_status'    => 'inherit',
            'post_mime_type' => 'image',
            'posts_per_page' => -1,
            'fields'         => 'ids',
            'orderby'        => 'ID',
            'order'          => 'ASC',
        )
    );
}


/**
 * Handle selected image deletion.
 */
add_action( 'admin_post_pt_delete_unused_media', function () {

    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'You do not have permission to perform this action.' );
    }


    /**
     * Verify security nonce.
     */
    check_admin_referer( 'pt_delete_unused_media' );


    $ids = isset( $_POST['attachment_ids'] )
        ? array_map( 'absint', (array) $_POST['attachment_ids'] )
        : array();


    $ids = array_unique(
        array_filter( $ids )
    );


    $deleted = 0;
    $skipped = 0;


    foreach ( $ids as $attachment_id ) {


        /**
         * Re-check usage immediately before deletion.
         */
        if ( pt_media_attachment_is_used( $attachment_id ) ) {

            $skipped++;

            continue;
        }


        /**
         * Make sure it is still an attachment.
         */
        if ( 'attachment' !== get_post_type( $attachment_id ) ) {

            $skipped++;

            continue;
        }


        /**
         * Permanently delete attachment and generated files.
         */
        $result = wp_delete_attachment(
            $attachment_id,
            true
        );


        if ( $result ) {
            $deleted++;
        } else {
            $skipped++;
        }
    }


    /**
     * Return to scanner.
     */
    $redirect_url = add_query_arg(
        array(
            'page'    => 'unused-media-scanner',
            'deleted' => $deleted,
            'skipped' => $skipped,
        ),
        admin_url( 'tools.php' )
    );


    wp_safe_redirect( $redirect_url );

    exit;

} );


/**
 * Render scanner page.
 */
function pt_unused_media_scanner_page() {

    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'You do not have permission to access this page.' );
    }


    echo '<div class="wrap">';

    echo '<h1>Unused Media Scanner</h1>';


    /**
     * Show deletion result.
     */
    if ( isset( $_GET['deleted'] ) ) {

        $deleted = absint( $_GET['deleted'] );
        $skipped = absint( $_GET['skipped'] );


        echo '<div class="notice notice-success is-dismissible">';

        echo '<p>';

        echo '<strong>';
        echo esc_html( $deleted );
        echo '</strong> image(s) deleted. ';

        if ( $skipped > 0 ) {

            echo '<strong>';
            echo esc_html( $skipped );
            echo '</strong> image(s) were skipped because they appeared to be in use.';

        }

        echo '</p>';

        echo '</div>';
    }


    /**
     * Safety message.
     */
    echo '<div class="notice notice-info">';

    echo '<p>';

    echo '<strong>Safe mode:</strong> ';
    echo 'Images are only deleted when you manually select them.';

    echo '</p>';

    echo '</div>';


    /**
     * Get all images.
     */
    $attachments = pt_get_all_image_attachments();


    if ( empty( $attachments ) ) {

        echo '<div class="notice notice-warning">';
        echo '<p>No image attachments were found.</p>';
        echo '</div>';

        echo '</div>';

        return;
    }


    /**
     * Find potentially unused images.
     */
    $unused = array();


    foreach ( $attachments as $attachment_id ) {

        if ( ! pt_media_attachment_is_used( $attachment_id ) ) {

            $unused[] = $attachment_id;
        }
    }


    echo '<p>';

    echo '<strong>Total product/media images:</strong> ';
    echo esc_html( count( $attachments ) );

    echo '<br>';

    echo '<strong>Potentially unused images:</strong> ';
    echo esc_html( count( $unused ) );

    echo '</p>';


    if ( empty( $unused ) ) {

        echo '<div class="notice notice-success">';

        echo '<p>';
        echo '<strong>No potentially unused images were found.</strong>';
        echo '</p>';

        echo '</div>';

        echo '</div>';

        return;
    }


    /**
     * Delete form.
     */
    echo '<form
        method="post"
        action="' . esc_url( admin_url( 'admin-post.php' ) ) . '"
    >';


    echo '<input type="hidden" name="action" value="pt_delete_unused_media">';


    /**
     * Security nonce.
     */
    wp_nonce_field( 'pt_delete_unused_media' );


    /**
     * Select All checkbox.
     */
    echo '<p style="margin-top:20px;">';

    echo '<label>';

    echo '<input
        type="checkbox"
        id="pt-select-all"
        style="margin-right:6px;"
    >';

    echo '<strong>Select All</strong>';

    echo '</label>';

    echo '</p>';


    /**
     * Results table.
     */
    echo '<table class="widefat striped">';

    echo '<thead>';

    echo '<tr>';

    echo '<th style="width:45px;">Select</th>';
    echo '<th>ID</th>';
    echo '<th>Preview</th>';
    echo '<th>Title</th>';
    echo '<th>File</th>';
    echo '<th>URL</th>';

    echo '</tr>';

    echo '</thead>';

    echo '<tbody>';


    foreach ( $unused as $attachment_id ) {

        $url = wp_get_attachment_url( $attachment_id );

        $title = get_the_title( $attachment_id );

        $file = get_attached_file( $attachment_id );


        echo '<tr>';


        /**
         * Individual checkbox.
         */
        echo '<td>';

        echo '<input
            type="checkbox"
            class="pt-media-checkbox"
            name="attachment_ids[]"
            value="' . esc_attr( $attachment_id ) . '"
        >';

        echo '</td>';


        /**
         * Attachment ID.
         */
        echo '<td>';
        echo esc_html( $attachment_id );
        echo '</td>';


        /**
         * Image preview.
         */
        echo '<td>';

        echo wp_get_attachment_image(
            $attachment_id,
            array( 100, 100 )
        );

        echo '</td>';


        /**
         * Image title.
         */
        echo '<td>';
        echo esc_html( $title );
        echo '</td>';


        /**
         * Physical file path.
         */
        echo '<td>';

        if ( $file ) {
            echo esc_html( $file );
        }

        echo '</td>';


        /**
         * Public URL.
         */
        echo '<td>';

        if ( $url ) {

            echo '<a
                href="' . esc_url( $url ) . '"
                target="_blank"
            >';

            echo 'Open image';

            echo '</a>';
        }

        echo '</td>';


        echo '</tr>';
    }


    echo '</tbody>';

    echo '</table>';


    /**
     * Delete button.
     */
    echo '<p style="margin-top:20px;">';

    echo '<button
        type="submit"
        class="button button-primary"
        id="pt-delete-selected"
    >';

    echo 'Delete Selected';

    echo '</button>';

    echo '</p>';


    echo '</form>';


    /**
     * Select All + confirmation JavaScript.
     */
    ?>

    <script>
    document.addEventListener('DOMContentLoaded', function () {

        const selectAll = document.getElementById('pt-select-all');

        const checkboxes = document.querySelectorAll(
            '.pt-media-checkbox'
        );

        const deleteButton = document.getElementById(
            'pt-delete-selected'
        );


        /**
         * Select / deselect all images.
         */
        if (selectAll) {

            selectAll.addEventListener('change', function () {

                checkboxes.forEach(function (checkbox) {

                    checkbox.checked = selectAll.checked;

                });

            });

        }


        /**
         * Confirm deletion.
         */
        if (deleteButton) {

            deleteButton.addEventListener('click', function (event) {

                let selected = 0;


                checkboxes.forEach(function (checkbox) {

                    if (checkbox.checked) {
                        selected++;
                    }

                });


                if (selected === 0) {

                    event.preventDefault();

                    alert(
                        'Please select at least one image.'
                    );

                    return false;
                }


                const confirmed = confirm(
                    'You are about to permanently delete ' +
                    selected +
                    ' image(s) and their generated thumbnails.\\n\\n' +
                    'Are you sure?'
                );


                if ( ! confirmed ) {

                    event.preventDefault();

                    return false;
                }

            });

        }

    });
    </script>

    <?php

    echo '</div>';
}