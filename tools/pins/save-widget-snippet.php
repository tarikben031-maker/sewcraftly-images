/**
 * SewCraftly: Pinterest "Save" photo box for the sidebar + search in the main menu.
 * - [sewcraftly_pin_save] shows, on single posts only, the post's model photo (meta sc_side_photo)
 *   with a Pinterest Save button. The button saves the branded pin image (meta sc_save_media,
 *   falling back to the post's pin 1 from the pin feed, then to the photo itself).
 * - Adds a compact search form at the end of the primary menu.
 */
add_shortcode( 'sewcraftly_pin_save', function () {
	if ( ! is_singular( 'post' ) ) return '';
	$post_id = get_the_ID();
	$photo   = (int) get_post_meta( $post_id, 'sc_side_photo', true );
	$media   = (int) get_post_meta( $post_id, 'sc_save_media', true );
	$title   = '';
	if ( ! $media ) {
		$pins = get_posts( array(
			'post_type' => 'attachment', 'post_status' => 'inherit', 'posts_per_page' => 1,
			'meta_query' => array(
				array( 'key' => '_sc_pin_post', 'value' => $post_id ),
				array( 'key' => '_sc_pin_n', 'value' => 1 ),
			),
		) );
		if ( $pins ) $media = $pins[0]->ID;
	}
	if ( ! $photo ) $photo = $media;
	if ( ! $photo ) return '';
	if ( $media ) $title = get_post_meta( $media, '_sc_pin_title', true );
	if ( ! $title ) $title = get_the_title( $post_id );

	$img_url  = wp_get_attachment_image_url( $photo, 'large' );
	$pin_url  = wp_get_attachment_url( $media ? $media : $photo );
	$alt      = get_post_meta( $photo, '_wp_attachment_image_alt', true ) ?: $title;
	$share    = add_query_arg( array(
		'url'         => rawurlencode( get_permalink( $post_id ) ),
		'media'       => rawurlencode( $pin_url ),
		'description' => rawurlencode( $title ),
	), 'https://www.pinterest.com/pin/create/button/' );
	$icon = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M12 0a12 12 0 0 0-4.37 23.17c-.1-.94-.2-2.4.04-3.44l1.4-5.96s-.35-.72-.35-1.78c0-1.66.97-2.9 2.17-2.9 1.02 0 1.52.77 1.52 1.7 0 1.03-.66 2.58-1 4.01-.28 1.2.6 2.18 1.78 2.18 2.14 0 3.78-2.26 3.78-5.5 0-2.88-2.07-4.9-5.03-4.9-3.42 0-5.43 2.57-5.43 5.22 0 1.03.4 2.14.9 2.74.1.12.11.22.08.34l-.33 1.36c-.05.22-.18.27-.4.16-1.5-.7-2.43-2.89-2.43-4.65 0-3.78 2.75-7.26 7.93-7.26 4.16 0 7.4 2.97 7.4 6.93 0 4.13-2.6 7.46-6.22 7.46-1.21 0-2.36-.63-2.75-1.38l-.75 2.85c-.27 1.04-1 2.35-1.49 3.15A12 12 0 1 0 12 0z"/></svg>';

	return '<div class="sc-widget sc-pin-save">'
		. '<a class="sc-pin-img" href="' . esc_url( $share ) . '" target="_blank" rel="noopener nofollow">'
		. '<img src="' . esc_url( $img_url ) . '" alt="' . esc_attr( $alt ) . '" loading="lazy" />'
		. '<span class="sc-pin-tag">Free PDF pattern</span>'
		. '<span class="sc-pin-hover">' . $icon . 'Save</span>'
		. '<span class="sc-pin-overlay"><strong>Don&#8217;t lose this pattern!</strong><em>Save it for your next make &#9825;</em></span>'
		. '</a>'
		. '<a class="sc-pin-btn" href="' . esc_url( $share ) . '" target="_blank" rel="noopener nofollow">' . $icon . 'Save it on Pinterest</a>'
		. '</div>';
} );

add_filter( 'wp_nav_menu_items', function ( $items, $args ) {
	if ( empty( $args->theme_location ) || 'primary' !== $args->theme_location ) return $items;
	$form = '<li class="menu-item sc-menu-search"><form role="search" method="get" action="' . esc_url( home_url( '/' ) ) . '">'
		. '<label class="screen-reader-text" for="sc-menu-s">Search patterns</label>'
		. '<input id="sc-menu-s" type="search" name="s" placeholder="Search patterns…" value="' . esc_attr( get_search_query() ) . '" />'
		. '<button type="submit" aria-label="Search"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button>'
		. '</form></li>';
	return $items . $form;
}, 10, 2 );

add_action( 'wp_head', function () {
	?>
<style id="sewcraftly-pin-save">
.sc-pin-save{text-align:center}
.sc-pin-save .sc-pin-img{position:relative;display:block;border-radius:14px;overflow:hidden;text-decoration:none!important}
.sc-pin-save .sc-pin-img img{display:block;width:100%;height:auto;transition:transform .35s}
.sc-pin-save .sc-pin-img:hover img{transform:scale(1.03)}
.sc-pin-save .sc-pin-tag{position:absolute;top:12px;left:12px;background:#fff;color:#1a1a1a;font-weight:700;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;padding:6px 11px;border-radius:999px;box-shadow:0 2px 8px rgba(0,0,0,.12)}
.sc-pin-save .sc-pin-hover{position:absolute;top:10px;right:10px;display:inline-flex;align-items:center;gap:6px;background:#e60023;color:#fff;font-weight:700;font-size:.85rem;padding:7px 13px;border-radius:999px;box-shadow:0 2px 8px rgba(0,0,0,.18)}
.sc-pin-save .sc-pin-overlay{position:absolute;left:0;right:0;bottom:0;padding:70px 16px 18px;background:linear-gradient(to top,rgba(0,0,0,.72),rgba(0,0,0,.35) 55%,rgba(0,0,0,0));color:#fff;display:flex;flex-direction:column;gap:4px}
.sc-pin-save .sc-pin-overlay strong{font-size:1.35rem;line-height:1.2;font-weight:800;text-shadow:0 1px 4px rgba(0,0,0,.35)}
.sc-pin-save .sc-pin-overlay em{font-style:normal;font-size:.95rem;opacity:.95}
.sc-pin-save .sc-pin-btn{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:.9rem;background:#e60023;color:#fff!important;font-weight:700;padding:12px 18px;border-radius:999px;text-decoration:none!important}
.sc-pin-save .sc-pin-btn:hover{background:#ad081b}
.site-navigation .sc-menu-search{display:flex;align-items:center;margin-left:auto}
.site-navigation .sc-menu-search form{display:flex;align-items:center;border:1.5px solid rgba(0,0,0,.18);border-radius:999px;overflow:hidden;background:#fff}
.site-navigation .sc-menu-search input{border:0;outline:0;padding:7px 12px;width:170px;font-size:.9rem;background:transparent;box-shadow:none}
.site-navigation .sc-menu-search button{border:0;background:#b35a45;color:#fff;padding:7px 12px;cursor:pointer;display:flex;align-items:center}
@media (max-width:900px){.site-navigation .sc-menu-search{margin:8px 0}.site-navigation .sc-menu-search input{width:100%}.site-navigation .sc-menu-search form{width:100%}}
</style>
	<?php
} );
