<?php
// Obtener las variables de entorno para la conexión a la base de datos
define('DB_HOST', getenv('DB_HOST') ?: 'localhost');
define('DB_USER', getenv('DB_USER') ?: 'root');
define('DB_PASS', getenv('DB_PASS') ?: '');     
define('DB_NAME', getenv('DB_NAME') ?: 'my_database');
?>
