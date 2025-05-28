<?php
require_once 'config/Database.php';
require_once 'controllers/CanFrameController.php';
require_once 'controllers/LoginController.php';
require_once 'controllers/ResetPasswordController.php';

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Content-Type: application/json; charset=utf-8");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

function logError($message) {
    $logFile = __DIR__ . '/logs/error.log';
    $date = date('Y-m-d H:i:s');
    file_put_contents($logFile, "[$date] $message" . PHP_EOL, FILE_APPEND);
}

try {
    $dbConnection = (new Database())->getConnection();

    $path = isset($_GET['path']) ? $_GET['path'] : '';
    $method = $_SERVER['REQUEST_METHOD'];

    $pathParts = explode('/', trim($path, '/'));
    $resource = isset($pathParts[0]) ? $pathParts[0] : null;
    $id = isset($pathParts[1]) && is_numeric($pathParts[1]) ? (int)$pathParts[1] : null;

    $inputJSON = file_get_contents('php://input');
    $input = json_decode($inputJSON, true);

    switch ($resource) {
        case 'can_frames':
            $controller = new CanFrameController($dbConnection);
            $controller->processRequest($method, $id, $input);
            break;

        case 'login':
            $controller = new LoginController($dbConnection);
            $controller->processRequest($method, $id, $input);
            break;

        case 'reset_password':
            $controller = new ResetPasswordController($dbConnection);
            $controller->processRequest($method, $input);
            break;

        default:
            http_response_code(404);
            echo json_encode(["message" => "Resource not found"]);
            break;
    }
} catch (Exception $e) {
    logError("Fatal error: " . $e->getMessage());
    http_response_code(500);
    echo json_encode(["message" => "Internal server error"]);
}
