/**
 * SewCraftly Pinterest pin feed.
 * - Pins are media attachments marked with meta _sc_pin_post (the post they link to).
 * - POST /wp-json/sewcraftly/v1/pins (admin only) registers uploaded images as pins.
 * - GET  /wp-json/sewcraftly/v1/pins (admin only) lists them.
 * - Public RSS feed for Pinterest auto-publish: https://sewcraftly.com/feed/pins/ (or /?feed=pins)
 *   shows only pins whose release time has passed, newest first.
 */
add_action( 'init', function () {
	add_feed( 'pins', 'sewcraftly_render_pin_feed' );
} );

function sewcraftly_pin_query( $only_released ) {
	$meta = array( array( 'key' => '_sc_pin_post', 'compare' => 'EXISTS' ) );
	if ( $only_released ) {
		$meta[] = array( 'key' => '_sc_pin_release', 'value' => time(), 'compare' => '<=', 'type' => 'NUMERIC' );
	}
	return get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'posts_per_page' => 50,
		'meta_query'     => $meta,
		'meta_key'       => '_sc_pin_release',
		'orderby'        => 'meta_value_num',
		'order'          => 'DESC',
	) );
}

function sewcraftly_pin_link( $pin ) {
	$post_id = (int) get_post_meta( $pin->ID, '_sc_pin_post', true );
	$n       = (int) get_post_meta( $pin->ID, '_sc_pin_n', true );
	return add_query_arg( array(
		'utm_source'   => 'pinterest',
		'utm_medium'   => 'pin',
		'utm_campaign' => 'autopin',
		'utm_content'  => 'pin' . $n,
	), get_permalink( $post_id ) );
}

function sewcraftly_render_pin_feed() {
	header( 'Content-Type: application/rss+xml; charset=' . get_option( 'blog_charset' ), true );
	$pins = sewcraftly_pin_query( true );
	echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
	?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
	<title><?php echo esc_html( get_bloginfo( 'name' ) ); ?> – Free Sewing Patterns</title>
	<link><?php echo esc_url( home_url( '/' ) ); ?></link>
	<atom:link href="<?php echo esc_url( home_url( '/feed/pins/' ) ); ?>" rel="self" type="application/rss+xml" />
	<description>Free sewing patterns PDF and step-by-step sewing guides</description>
	<language>en-US</language>
	<?php foreach ( $pins as $pin ) :
		$post_id = (int) get_post_meta( $pin->ID, '_sc_pin_post', true );
		if ( ! $post_id || 'publish' !== get_post_status( $post_id ) ) continue;
		$img   = wp_get_attachment_url( $pin->ID );
		$file  = get_attached_file( $pin->ID );
		$title = get_post_meta( $pin->ID, '_sc_pin_title', true ) ?: get_the_title( $post_id );
		$desc  = get_post_meta( $pin->ID, '_sc_pin_desc', true );
		$rel   = (int) get_post_meta( $pin->ID, '_sc_pin_release', true );
		$link  = sewcraftly_pin_link( $pin );
		?>
	<item>
		<title><?php echo esc_html( $title ); ?></title>
		<link><?php echo esc_url( $link ); ?></link>
		<guid isPermaLink="false">sewcraftly-pin-<?php echo (int) $pin->ID; ?></guid>
		<pubDate><?php echo esc_html( gmdate( 'D, d M Y H:i:s +0000', $rel ) ); ?></pubDate>
		<description><![CDATA[<img src="<?php echo esc_url( $img ); ?>" alt="<?php echo esc_attr( $title ); ?>" /><p><?php echo esc_html( $desc ); ?></p>]]></description>
		<enclosure url="<?php echo esc_url( $img ); ?>" length="<?php echo $file && file_exists( $file ) ? (int) filesize( $file ) : 0; ?>" type="image/jpeg" />
		<media:content url="<?php echo esc_url( $img ); ?>" medium="image" type="image/jpeg" />
	</item>
	<?php endforeach; ?>
</channel>
</rss>
	<?php
}

add_action( 'rest_api_init', function () {
	$admin = function () { return current_user_can( 'manage_options' ); };

	register_rest_route( 'sewcraftly/v1', '/pins', array(
		array(
			'methods'             => 'POST',
			'permission_callback' => $admin,
			'callback'            => function ( WP_REST_Request $r ) {
				$out = array();
				foreach ( (array) $r->get_param( 'items' ) as $it ) {
					$att  = isset( $it['attachment_id'] ) ? (int) $it['attachment_id'] : 0;
					$post = isset( $it['post_id'] ) ? (int) $it['post_id'] : 0;
					if ( ! $att || 'attachment' !== get_post_type( $att ) || ! $post || 'post' !== get_post_type( $post ) ) {
						return new WP_Error( 'bad_item', 'Invalid attachment_id or post_id', array( 'status' => 400 ) );
					}
					$rel = isset( $it['release'] ) && is_numeric( $it['release'] ) ? (int) $it['release'] : time();
					update_post_meta( $att, '_sc_pin_post', $post );
					update_post_meta( $att, '_sc_pin_n', isset( $it['n'] ) ? (int) $it['n'] : 1 );
					update_post_meta( $att, '_sc_pin_title', sanitize_text_field( isset( $it['title'] ) ? $it['title'] : '' ) );
					update_post_meta( $att, '_sc_pin_desc', sanitize_textarea_field( isset( $it['description'] ) ? $it['description'] : '' ) );
					update_post_meta( $att, '_sc_pin_release', $rel );
					$out[] = array( 'attachment_id' => $att, 'post_id' => $post, 'release' => gmdate( 'c', $rel ) );
				}
				return $out;
			},
		),
		array(
			'methods'             => 'GET',
			'permission_callback' => $admin,
			'callback'            => function () {
				$out = array();
				foreach ( sewcraftly_pin_query( false ) as $pin ) {
					$out[] = array(
						'attachment_id' => $pin->ID,
						'post_id'       => (int) get_post_meta( $pin->ID, '_sc_pin_post', true ),
						'n'             => (int) get_post_meta( $pin->ID, '_sc_pin_n', true ),
						'title'         => get_post_meta( $pin->ID, '_sc_pin_title', true ),
						'release'       => gmdate( 'c', (int) get_post_meta( $pin->ID, '_sc_pin_release', true ) ),
						'image'         => wp_get_attachment_url( $pin->ID ),
						'link'          => sewcraftly_pin_link( $pin ),
					);
				}
				return $out;
			},
		),
	) );
} );
