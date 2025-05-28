<?php
require_once __DIR__ . '/../models/Login.php';

class LoginController {
    private $login;

    public function __construct($db) {
        $this->login = new Login($db);
    }

    public function processRequest($method, $id = null, $data = null) {
        header('Content-Type: application/json; charset=utf-8');

        // Variables seguras y opcionales
        $email = $data['email'] ?? null;
        $password = $data['password'] ?? null;
        $action = $data['action'] ?? null;

        switch ($method) {
            case 'POST':
                if (!$email || !$password) {
                    http_response_code(400);
                    echo json_encode(["message" => "Email and password are required"]);
                    return;
                }

                if ($action === 'register') {
                    $existingUser = $this->login->findByEmail($email);
                    if ($existingUser && $existingUser->num_rows > 0) {
                        http_response_code(400);
                        echo json_encode(["message" => "Email already exists"]);
                        return;
                    }
                    $password_hash = password_hash($password, PASSWORD_DEFAULT);
                    $newId = $this->login->create($email, $password_hash);
                    if ($newId) {
                        http_response_code(201);
                        echo json_encode(["message" => "User created", "id" => $newId, "email" => $email]);
                    } else {
                        http_response_code(500);
                        echo json_encode(["message" => "Failed to create user"]);
                    }
                } elseif ($action === 'login') {
                    $result = $this->login->findByEmail($email);
                    if ($result && $result->num_rows > 0) {
                        $user = $result->fetch_assoc();
                        if (password_verify($password, $user['password'])) {
                            http_response_code(200);
                            echo json_encode(["success" => true, "message" => "Login successful"]);
                        } else {
                            http_response_code(401);
                            echo json_encode(["success" => false, "message" => "Invalid credentials"]);
                        }
                    } else {
                        http_response_code(404);
                        echo json_encode(["success" => false, "message" => "User not found"]);
                    }
                } else {
                    http_response_code(400);
                    echo json_encode(["message" => "Invalid action"]);
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
                } elseif ($email) {
                    $result = $this->login->findByEmail($email);
                    if ($result && $result->num_rows > 0) {
                        $user = $result->fetch_assoc();
                        unset($user['password']);
                        http_response_code(200);
                        echo json_encode($user);
                    } else {
                        http_response_code(404);
                        echo json_encode(["message" => "User not found"]);
                    }
                } else {
                    $result = $this->login->getAll();
                    $users = [];
                    if ($result && $result->num_rows > 0) {
                        while ($row = $result->fetch_assoc()) {
                            unset($row['password']);
                            $users[] = $row;
                        }
                    }
                    http_response_code(200);
                    echo json_encode($users);
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
