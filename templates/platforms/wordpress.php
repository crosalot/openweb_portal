<?php
/**
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, WordPress Language, and ABSPATH. You can find more information
 * by visiting {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */

define('WP_HOME', 'http://' . $_SERVER['SERVER_NAME']);
define('WP_SITEURL', 'http://' . $_SERVER['SERVER_NAME']);

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', '{{ DB_NAME }}');

/** MySQL database username */
define('DB_USER', '{{ DB_USER }}');

/** MySQL database password */
define('DB_PASSWORD', '{{ DB_PASS }}');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'P-xK&3JfZzMs3`OeSeTU;xuR%)E@+7QUzp~d5D pT=X-nQ`|H=hvw::.Gh4Pz-~O');
define('SECURE_AUTH_KEY',  '+D((y2hL?azt_eb3SX@%&Skd+X*ROTAkqYuz:6S[75m!ruLCVxK2Q7fHZT56<aR:');
define('LOGGED_IN_KEY',    'kUw))t#r(7H$v}Ci08 g+`!G/vF(t+y/za-Qh2I})X5QI+ S.p=d )xps@ySnDoM');
define('NONCE_KEY',        'H^+_9~0q9zvU-EJ7Gq+g{+eWx.zz(Zo/JHyO?KNPy]^,r+YD*W4es;K0u<*ej$XG');
define('AUTH_SALT',        '.^0HXx2.x-Hl[>:u$gDj_>[^RafgdwLJ}B |hAcg|PESXG+fUa!jH-6h*v]AycV*');
define('SECURE_AUTH_SALT', '-)&XzPt^?|,>RE{XnKd#W@fU9+nK*V..7|59F!v(rUR$we$D{+(D kAU$ 3$B1v#');
define('LOGGED_IN_SALT',   '-(SqV+>U5UaE2i@+q6SBR-x#p*B!^O/^C|59D+^dcelnxg2wVc}t!##Qf}|RIJ!V');
define('NONCE_SALT',       'pnc3AdHV}9ae/:7F5Y*VFq{bfN]ib>0h3+6s]rB9KWvl.kqVbMBll#|e|3P)k`dS');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * WordPress Localized Language, defaults to English.
 *
 * Change this to localize WordPress. A corresponding MO file for the chosen
 * language must be installed to wp-content/languages. For example, install
 * de_DE.mo to wp-content/languages and set WPLANG to 'de_DE' to enable German
 * language support.
 */
define('WPLANG', '');

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
