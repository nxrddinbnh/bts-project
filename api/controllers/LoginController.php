<?php
require_once __DIR__ . '/../models/Login.php';

class LoginController {
    private $login;

    public function __construct($db) {
        $this->login = new Login($db);
    }

    public function processRequest($method, $id = null, $data = null) {
        header('Content-Type: application/json; charset=utf-8');

        switch ($method) {
            case 'POST': // Create user
                if (!$data || !isset($data['email']) || !isset($data['password'])) {
                    http_response_code(400);
                    echo json_encode(["message" => "Email and password are required"]);
                    return;
                }

                $email = $data['email'];
                $password_hash = password_hash($data['password'], PASSWORD_DEFAULT);
                $newId = $this->login->create($email, $password_hash);
                if ($newId) {
                    http_response_code(201);
                    echo json_encode(["message" => "User created", "id" => $newId, "email" => $email]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Failed to create user"]);
                }
                break;

            case 'GET':
                if ($id) {
                    $result = $this->login->findById($id);
                    if ($result && $result->num_rows > 0) {
                        $user = $result->fetch_assoc();
                        http_response_code(200);
                        echo json_encode($user);
                    } else {
                        http_response_code(404);
                        echo json_encode(["message" => "User not found"]);
                    }
                } else {
                    $result = $this->login->getAllUsers();
                    $users = [];
                    while ($row = $result->fetch_assoc()) {
                        $users[] = $row;
                    }
                    http_response_code(200);
                    echo json_encode($users);
                }
                break;

            case 'PUT':
                if (!$id) {
                    http_response_code(400);
                    echo json_encode(["message" => "User ID is required for update"]);
                    return;
                }
                if (!$data || !isset($data['email'])) {
                    http_response_code(400);
                    echo json_encode(["message" => "Email is required for update"]);
                    return;
                }

                $email = $data['email'];
                $password_hash = isset($data['password']) ? password_hash($data['password'], PASSWORD_DEFAULT) : null;

                if ($this->login->update($id, $email, $password_hash)) {
                    http_response_code(200);
                    echo json_encode(["message" => "User updated"]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Failed to update user"]);
                }
                break;

            case 'DELETE':
                if (!$id) {
                    http_response_code(400);
                    echo json_encode(["message" => "User ID is required for deletion"]);
                    return;
                }
                if ($this->login->delete($id)) {
                    http_response_code(200);
                    echo json_encode(["message" => "User deleted"]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Failed to delete user"]);
                }
                break;

            default:
                http_response_code(405);
                echo json_encode(["message" => "Method not allowed"]);
                break;
        }
    }
}
?>
