/**
 * ============================================================
 * MIVIVA - WooCommerce YouTube Product Video
 * SHOPWELL - FINAL STABLE VERSION
 * ============================================================
 */


/* ============================================================
 * 1. YOUTUBE URL FIELD
 * ============================================================ */

add_action(
    'woocommerce_product_options_general_product_data',
    function () {

        woocommerce_wp_text_input(
            array(
                'id'          => '_miviva_youtube_video',
                'label'       => 'YouTube Produktvideo',
                'placeholder' => 'https://youtu.be/RsuvaK6LNNI',
                'description' => 'YouTube URL für das Produktvideo.',
                'desc_tip'    => true,
                'type'        => 'url',
            )
        );

    }
);


/* ============================================================
 * 2. SAVE YOUTUBE URL
 * ============================================================ */

add_action(
    'woocommerce_admin_process_product_object',
    function ( $product ) {

        if (
            isset(
                $_POST['_miviva_youtube_video']
            )
        ) {

            $url = esc_url_raw(
                wp_unslash(
                    $_POST['_miviva_youtube_video']
                )
            );

            $product->update_meta_data(
                '_miviva_youtube_video',
                $url
            );

        }

    }
);


/* ============================================================
 * 3. GET YOUTUBE VIDEO ID
 * ============================================================ */

function miviva_get_youtube_id_final( $url ) {

    if ( empty( $url ) ) {
        return '';
    }

    $patterns = array(

        '~youtu\.be/([A-Za-z0-9_-]{11})~',

        '~youtube\.com/watch\?v=([A-Za-z0-9_-]{11})~',

        '~youtube\.com/shorts/([A-Za-z0-9_-]{11})~',

        '~youtube\.com/embed/([A-Za-z0-9_-]{11})~',

        '~youtube-nocookie\.com/embed/([A-Za-z0-9_-]{11})~',

    );

    foreach ( $patterns as $pattern ) {

        if (
            preg_match(
                $pattern,
                $url,
                $matches
            )
        ) {

            return $matches[1];

        }

    }

    return '';

}


/* ============================================================
 * 4. CSS
 * ============================================================ */

add_action(
    'wp_head',
    function () {

        if ( ! is_product() ) {
            return;
        }

        ?>

        <style>

/* ============================================================
   VIDEO SLIDE
   ============================================================ */

.woocommerce-product-gallery
.miviva-video-slide {

    position: relative !important;

    float: left !important;

    display: block !important;

    margin: 0 !important;

    padding: 0 !important;

    box-sizing: border-box !important;

    overflow: hidden !important;

}


/* ============================================================
   VIDEO INNER
   ============================================================ */

.miviva-video-inner {

    position: relative !important;

    width: 100% !important;

    height: 100% !important;

    margin: 0 !important;

    padding: 0 !important;

    background: #000 !important;

    overflow: hidden !important;

}


/* ============================================================
   VIDEO PREVIEW
   ============================================================ */

.miviva-video-preview {

    position: absolute !important;

    inset: 0 !important;

    width: 100% !important;

    height: 100% !important;

    margin: 0 !important;

    padding: 0 !important;

    background: #000 !important;

    overflow: hidden !important;

    cursor: pointer !important;

}


/* ============================================================
   PREVIEW IMAGE
   ============================================================ */

.miviva-video-preview img {

    position: absolute !important;

    inset: 0 !important;

    width: 100% !important;

    height: 100% !important;

    max-width: none !important;

    max-height: none !important;

    margin: 0 !important;

    padding: 0 !important;

    display: block !important;

    object-fit: cover !important;

}


/* ============================================================
   MAIN PLAY BUTTON
   ============================================================ */

.miviva-video-play {

    position: absolute !important;

    top: 50% !important;

    left: 50% !important;

    transform:
        translate(-50%, -50%) !important;

    z-index: 20 !important;

    width: 70px !important;

    height: 70px !important;

    margin: 0 !important;

    padding: 0 !important;

    border: 3px solid #fff !important;

    border-radius: 50% !important;

    background:
        rgba(0,0,0,.78) !important;

    color: #fff !important;

    font-size: 27px !important;

    line-height: 64px !important;

    text-align: center !important;

    cursor: pointer !important;

    box-sizing: border-box !important;

}


/* ============================================================
   YOUTUBE IFRAME
   ============================================================ */

.miviva-video-inner iframe {

    position: absolute !important;

    top: 0 !important;

    left: 0 !important;

    width: 100% !important;

    height: 100% !important;

    min-width: 0 !important;

    min-height: 0 !important;

    max-width: none !important;

    max-height: none !important;

    margin: 0 !important;

    padding: 0 !important;

    border: 0 !important;

    display: block !important;

}


/* ============================================================
   VIDEO THUMBNAIL
   ============================================================ */

.flex-control-thumbs
.miviva-video-thumb {

    position: relative !important;

    padding: 0 !important;

    overflow: hidden !important;

    box-sizing: border-box !important;

    cursor: pointer !important;

}


/* ============================================================
   THUMBNAIL IMAGE
   ============================================================ */

.flex-control-thumbs
.miviva-video-thumb img {

    width: 100% !important;

    height: 100% !important;

    max-width: none !important;

    max-height: none !important;

    margin: 0 !important;

    padding: 0 !important;

    display: block !important;

    object-fit: cover !important;

}


/* ============================================================
   PERMANENT PLAY ICON
   ============================================================ */

.flex-control-thumbs
.miviva-video-thumb
.miviva-thumb-play-icon {

    position: absolute !important;

    top: 50% !important;

    left: 50% !important;

    transform:
        translate(-50%, -50%) !important;

    width: 26px !important;

    height: 26px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    border-radius: 50% !important;

    background:
        rgba(0,0,0,.82) !important;

    color: #fff !important;

    font-size: 10px !important;

    line-height: 26px !important;

    text-align: center !important;

    z-index: 999 !important;

    pointer-events: none !important;

    opacity: 1 !important;

    visibility: visible !important;

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 767px) {

    .miviva-video-play {

        width: 62px !important;

        height: 62px !important;

        font-size: 23px !important;

        line-height: 56px !important;

    }

}

        </style>

        <?php

    }
);


/* ============================================================
 * 5. JAVASCRIPT
 * ============================================================ */

add_action(
    'wp_footer',
    function () {

        if ( ! is_product() ) {
            return;
        }

        global $product;

        if ( ! $product ) {
            return;
        }

        $url = get_post_meta(
            $product->get_id(),
            '_miviva_youtube_video',
            true
        );

        $video_id =
            miviva_get_youtube_id_final(
                $url
            );

        if ( ! $video_id ) {
            return;
        }

        ?>

        <script>

        (function () {

            'use strict';


            /* ==================================================
               CONFIG
               ================================================== */

            var VIDEO_ID =
                <?php
                echo wp_json_encode(
                    $video_id
                );
                ?>;


            var THUMBNAIL =
                'https://img.youtube.com/vi/' +
                VIDEO_ID +
                '/hqdefault.jpg';


            /* ==================================================
               GET GALLERY
               ================================================== */

            function getGallery() {

                return document.querySelector(
                    '.woocommerce-product-gallery'
                );

            }


            /* ==================================================
               GET WRAPPER
               ================================================== */

            function getWrapper() {

                var gallery =
                    getGallery();

                if ( ! gallery ) {
                    return null;
                }

                return gallery.querySelector(
                    '.woocommerce-product-gallery__wrapper'
                );

            }


            /* ==================================================
               CREATE PREVIEW
               ================================================== */

            function createPreview( inner ) {

                if ( ! inner ) {
                    return;
                }


                if (
                    inner.querySelector(
                        '.miviva-video-preview'
                    )
                ) {

                    return;

                }


                var preview =
                    document.createElement(
                        'div'
                    );


                preview.className =
                    'miviva-video-preview';


                var image =
                    document.createElement(
                        'img'
                    );


                image.src =
                    THUMBNAIL;


                image.alt =
                    'Produktvideo';


                image.draggable =
                    false;


                var button =
                    document.createElement(
                        'button'
                    );


                button.type =
                    'button';


                button.className =
                    'miviva-video-play';


                button.setAttribute(
                    'aria-label',
                    'Produktvideo abspielen'
                );


                button.innerHTML =
                    '▶';


                preview.appendChild(
                    image
                );


                preview.appendChild(
                    button
                );


                inner.appendChild(
                    preview
                );

            }


            /* ==================================================
               CREATE VIDEO SLIDE
               ================================================== */

            function createVideoSlide() {

                var wrapper =
                    getWrapper();

                if ( ! wrapper ) {
                    return null;
                }


                var existing =
                    wrapper.querySelector(
                        '.miviva-video-slide'
                    );


                if ( existing ) {

                    return existing;

                }


                /*
                 * Find normal image slides.
                 */

                var normalSlides =
                    wrapper.querySelectorAll(
                        '.woocommerce-product-gallery__image:not(.miviva-video-slide)'
                    );


                if ( ! normalSlides.length ) {
                    return null;
                }


                /*
                 * Get exact width from first image.
                 */

                var first =
                    normalSlides[0];


                var rect =
                    first.getBoundingClientRect();


                var width =
                    rect.width;


                if ( width < 100 ) {
                    return null;
                }


                /*
                 * EXACT 600 x 800.
                 */

                var height =
                    width *
                    800 /
                    600;


                /*
                 * Create slide.
                 */

                var slide =
                    document.createElement(
                        'div'
                    );


                slide.className =
                    'woocommerce-product-gallery__image miviva-video-slide';


                slide.setAttribute(
                    'data-thumb',
                    THUMBNAIL
                );


                slide.setAttribute(
                    'data-thumb-alt',
                    'Produktvideo'
                );


                slide.setAttribute(
                    'data-video-id',
                    VIDEO_ID
                );


                slide.style.width =
                    width + 'px';


                slide.style.height =
                    height + 'px';


                slide.style.marginRight =
                    '0px';


                slide.style.float =
                    'left';


                slide.style.display =
                    'block';


                /*
                 * Inner container.
                 */

                var inner =
                    document.createElement(
                        'div'
                    );


                inner.className =
                    'miviva-video-inner';


                createPreview(
                    inner
                );


                slide.appendChild(
                    inner
                );


                wrapper.appendChild(
                    slide
                );


                console.log(
                    'MIVIVA: Video slide created'
                );


                return slide;

            }


            /* ==================================================
               REMOVE ALL YOUTUBE DUPLICATES
               ================================================== */

            function removeDuplicateVideoThumbs() {

                var gallery =
                    getGallery();

                if ( ! gallery ) {
                    return;
                }


                var thumbs =
                    gallery.querySelector(
                        '.flex-control-thumbs'
                    );

                if ( ! thumbs ) {
                    return;
                }


                var items =
                    thumbs.querySelectorAll(
                        'li'
                    );


                items.forEach(
                    function (li) {

                        /*
                         * Never remove our own thumbnail.
                         */

                        if (
                            li.classList.contains(
                                'miviva-video-thumb'
                            )
                        ) {

                            return;

                        }


                        var image =
                            li.querySelector(
                                'img'
                            );


                        if ( ! image ) {
                            return;
                        }


                        var src =
                            image.getAttribute(
                                'src'
                            ) || '';


                        var dataThumb =
                            li.getAttribute(
                                'data-thumb'
                            ) || '';


                        var isVideo =
                            src.indexOf(
                                'img.youtube.com/vi/' +
                                VIDEO_ID
                            ) !== -1
                            ||
                            dataThumb.indexOf(
                                'img.youtube.com/vi/' +
                                VIDEO_ID
                            ) !== -1;


                        if ( isVideo ) {

                            li.remove();

                        }

                    }
                );

            }


            /* ==================================================
               CREATE VIDEO THUMBNAIL
               ================================================== */

            function createVideoThumbnail() {

                var gallery =
                    getGallery();

                if ( ! gallery ) {
                    return;
                }


                var thumbs =
                    gallery.querySelector(
                        '.flex-control-thumbs'
                    );

                if ( ! thumbs ) {
                    return;
                }


                /*
                 * Remove duplicates first.
                 */

                removeDuplicateVideoThumbs();


                /*
                 * Check our thumbnail.
                 */

                var existing =
                    thumbs.querySelector(
                        '.miviva-video-thumb'
                    );


                /*
                 * Find normal thumbnail.
                 */

                var reference =
                    thumbs.querySelector(
                        'li:not(.miviva-video-thumb)'
                    );


                if ( ! reference ) {

                    return;

                }


                var rect =
                    reference.getBoundingClientRect();


                if (
                    rect.width < 5 ||
                    rect.height < 5
                ) {

                    return;

                }


                /*
                 * If already exists,
                 * update exact dimensions.
                 */

                if ( existing ) {

                    existing.style.width =
                        rect.width + 'px';


                    existing.style.height =
                        rect.height + 'px';


                    return;

                }


                /*
                 * Copy spacing from ShopWell.
                 */

                var style =
                    window.getComputedStyle(
                        reference
                    );


                /*
                 * Create thumbnail LI.
                 */

                var li =
                    document.createElement(
                        'li'
                    );


                li.className =
                    'miviva-video-thumb';


                li.style.width =
                    rect.width + 'px';


                li.style.height =
                    rect.height + 'px';


                li.style.marginTop =
                    style.marginTop;


                li.style.marginRight =
                    style.marginRight;


                li.style.marginBottom =
                    style.marginBottom;


                li.style.marginLeft =
                    style.marginLeft;


                /*
                 * Thumbnail image.
                 */

                var img =
                    document.createElement(
                        'img'
                    );


                img.src =
                    THUMBNAIL;


                img.alt =
                    'Produktvideo';


                img.draggable =
                    false;


                li.appendChild(
                    img
                );


                /*
                 * PERMANENT PLAY ICON.
                 */

                var playIcon =
                    document.createElement(
                        'span'
                    );


                playIcon.className =
                    'miviva-thumb-play-icon';


                playIcon.innerHTML =
                    '▶';


                playIcon.setAttribute(
                    'aria-hidden',
                    'true'
                );


                li.appendChild(
                    playIcon
                );


                /*
                 * Add exactly ONE.
                 */

                thumbs.appendChild(
                    li
                );


                console.log(
                    'MIVIVA: Video thumbnail created'
                );

            }


            /* ==================================================
               STOP YOUTUBE
               ================================================== */

            function stopVideo() {

                var gallery =
                    getGallery();

                if ( ! gallery ) {
                    return;
                }


                var slide =
                    gallery.querySelector(
                        '.miviva-video-slide'
                    );

                if ( ! slide ) {
                    return;
                }


                var inner =
                    slide.querySelector(
                        '.miviva-video-inner'
                    );

                if ( ! inner ) {
                    return;
                }


                /*
                 * Remove iframe.
                 *
                 * Removing iframe completely guarantees
                 * that YouTube stops playing.
                 */

                var iframe =
                    inner.querySelector(
                        'iframe'
                    );


                if ( iframe ) {

                    iframe.remove();

                    console.log(
                        'MIVIVA: YouTube STOP'
                    );

                }


                /*
                 * Restore preview.
                 */

                createPreview(
                    inner
                );

            }


            /* ==================================================
               OPEN VIDEO SLIDE
               ================================================== */

            function openVideoSlide() {

                var gallery =
                    getGallery();

                if ( ! gallery ) {
                    return;

                }


                var wrapper =
                    getWrapper();

                if ( ! wrapper ) {
                    return;

                }


                var slide =
                    wrapper.querySelector(
                        '.miviva-video-slide'
                    );

                if ( ! slide ) {
                    return;
                }


                /*
                 * Get slide index.
                 */

                var slides =
                    Array.prototype.slice.call(
                        wrapper.children
                    );


                var index =
                    slides.indexOf(
                        slide
                    );


                if ( index < 0 ) {
                    return;
                }


                /*
                 * Try ShopWell FlexSlider.
                 */

                if (
                    window.jQuery
                ) {

                    var flexslider =
                        gallery.querySelector(
                            '.flexslider'
                        );


                    if ( flexslider ) {

                        var instance =
                            jQuery(
                                flexslider
                            ).data(
                                'flexslider'
                            );


                        if (
                            instance &&
                            typeof instance.flexAnimate ===
                            'function'
                        ) {

                            instance.flexAnimate(
                                index
                            );

                            return;

                        }

                    }


                    /*
                     * Try gallery itself.
                     */

                    var galleryInstance =
                        jQuery(
                            gallery
                        ).data(
                            'flexslider'
                        );


                    if (
                        galleryInstance &&
                        typeof galleryInstance.flexAnimate ===
                        'function'
                    ) {

                        galleryInstance.flexAnimate(
                            index
                        );

                        return;

                    }

                }

            }


            /* ==================================================
               PLAY VIDEO
               ================================================== */

            function playVideo( button ) {

                var slide =
                    button.closest(
                        '.miviva-video-slide'
                    );


                if ( ! slide ) {
                    return;
                }


                var inner =
                    slide.querySelector(
                        '.miviva-video-inner'
                    );


                if ( ! inner ) {
                    return;
                }


                /*
                 * Don't create iframe twice.
                 */

                if (
                    inner.querySelector(
                        'iframe'
                    )
                ) {

                    return;

                }


                /*
                 * Remove preview.
                 */

                var preview =
                    inner.querySelector(
                        '.miviva-video-preview'
                    );


                if ( preview ) {

                    preview.remove();

                }


                /*
                 * Create iframe.
                 */

                var iframe =
                    document.createElement(
                        'iframe'
                    );


                iframe.src =
                    'https://www.youtube-nocookie.com/embed/' +
                    VIDEO_ID +
                    '?autoplay=1' +
                    '&playsinline=1' +
                    '&rel=0';


                iframe.title =
                    'Produktvideo';


                iframe.allow =
                    'autoplay; encrypted-media; picture-in-picture; web-share';


                iframe.setAttribute(
                    'allowfullscreen',
                    ''
                );


                iframe.frameBorder =
                    '0';


                inner.appendChild(
                    iframe
                );


                console.log(
                    'MIVIVA: YouTube START'
                );

            }


            /* ==================================================
               THUMBNAIL CLICK
               ================================================== */

            document.addEventListener(
                'click',
                function (event) {

                    var thumb =
                        event.target.closest(
                            '.miviva-video-thumb'
                        );


                    if ( ! thumb ) {
                        return;
                    }


                    event.preventDefault();

                    event.stopPropagation();


                    openVideoSlide();

                },
                true
            );


            /* ==================================================
               MAIN PLAY BUTTON CLICK
               ================================================== */

            document.addEventListener(
                'click',
                function (event) {

                    var button =
                        event.target.closest(
                            '.miviva-video-play'
                        );


                    if ( ! button ) {
                        return;
                    }


                    event.preventDefault();

                    event.stopPropagation();


                    playVideo(
                        button
                    );

                },
                true
            );


            /* ==================================================
               NORMAL IMAGE THUMBNAIL CLICK
               ================================================== */

            document.addEventListener(
                'click',
                function (event) {

                    var thumb =
                        event.target.closest(
                            '.flex-control-thumbs li'
                        );


                    if ( ! thumb ) {
                        return;
                    }


                    /*
                     * Video thumbnail itself.
                     */

                    if (
                        thumb.classList.contains(
                            'miviva-video-thumb'
                        )
                    ) {

                        return;

                    }


                    /*
                     * STOP BEFORE SHOPWELL
                     * CHANGES THE SLIDE.
                     */

                    stopVideo();

                },
                true
            );


            /* ==================================================
               WATCH GALLERY MOVEMENT
               ================================================== */

            var previousTransform =
                '';


            function watchGallery() {

                var wrapper =
                    getWrapper();

                if ( ! wrapper ) {
                    return;
                }


                var transform =
                    wrapper.style.transform ||
                    '';


                if (
                    transform ===
                    previousTransform
                ) {

                    return;

                }


                previousTransform =
                    transform;


                setTimeout(
                    function () {

                        var gallery =
                            getGallery();


                        if ( ! gallery ) {
                            return;
                        }


                        var video =
                            gallery.querySelector(
                                '.miviva-video-slide'
                            );


                        if ( ! video ) {
                            return;
                        }


                        /*
                         * If no iframe,
                         * nothing is playing.
                         */

                        if (
                            ! video.querySelector(
                                'iframe'
                            )
                        ) {

                            return;

                        }


                        var videoRect =
                            video.getBoundingClientRect();


                        var galleryRect =
                            gallery.getBoundingClientRect();


                        /*
                         * Is video visible?
                         */

                        var visible =
                            videoRect.right >
                            galleryRect.left
                            &&
                            videoRect.left <
                            galleryRect.right;


                        if ( ! visible ) {

                            stopVideo();

                        }

                    },
                    40
                );

            }


            /* ==================================================
               INITIALIZATION
               ================================================== */

            var attempts =
                0;


            function init() {

                attempts++;


                var slide =
                    createVideoSlide();


                if ( slide ) {

                    createVideoThumbnail();

                }


                /*
                 * ShopWell may initialize slowly.
                 */

                if (
                    attempts < 40
                ) {

                    setTimeout(
                        init,
                        400
                    );

                }

            }


            setTimeout(
                init,
                500
            );


            /* ==================================================
               CONTINUOUS GALLERY WATCH
               ================================================== */

            setInterval(
                watchGallery,
                100
            );


            /* ==================================================
               RESIZE
               ================================================== */

            window.addEventListener(
                'resize',
                function () {

                    setTimeout(
                        function () {

                            createVideoSlide();

                            createVideoThumbnail();

                        },
                        300
                    );

                }
            );


            /* ==================================================
               MUTATION OBSERVER
               ================================================== */

            var observer =
                new MutationObserver(
                    function () {

                        setTimeout(
                            function () {

                                createVideoSlide();

                                createVideoThumbnail();

                            },
                            150
                        );

                    }
                );


            setTimeout(
                function () {

                    var gallery =
                        getGallery();


                    if ( gallery ) {

                        observer.observe(
                            gallery,
                            {
                                childList: true,
                                subtree: true
                            }
                        );

                    }

                },
                1500
            );


        })();

        </script>

        <?php

    }
);