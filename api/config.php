<?php
declare(strict_types=1);

require_once __DIR__ . '/env.php';

load_env(dirname(__DIR__) . '/.env');

$host = app_env('DB_HOST', '127.0.0.1');
$user = app_env('DB_USER', 'root');
$pass = app_env('DB_PASS', '');
$dbname = app_env('DB_NAME', 'jarvisai');
$port = (int) app_env('DB_PORT', '3306');

$conn = null;
$dbError = null;

if (app_env('DB_CONNECT', 'false') === 'true') {
    mysqli_report(MYSQLI_REPORT_OFF);
    $conn = @new mysqli($host, $user, $pass, $dbname, $port);
    if ($conn->connect_error) {
        $dbError = $conn->connect_error;
        $conn = null;
    }
}
