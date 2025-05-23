<?php
require_once __DIR__ . '/../models/ResetPassword.php';
require_once __DIR__ . '/../models/Login.php';

class ResetPasswordController {
    private $resetPassword;
    private $login;

    public function __construct($db) {
        $this->resetPassword = new ResetPassword($db);
        $this->login = new Login($db);
    }

    public function processRequest($method, $data = null) {
        header('Content-Type: application/json; charset=utf-8');

        switch ($method) {
            case 'POST': // Request password reset token
                if (!$data || !isset($data['email'])) {
                    http_response_code(400);
                    echo json_encode(["message" => "Email required"]);
                    return;
                }

                $email = $data['email'];

                // Validate that the user exists
                $user = $this->login->findByEmail($email);
                if (!$user || $user->num_rows == 0) {
                    http_response_code(404);
                    echo json_encode(["message" => "User not found"]);
                    return;
                }

                // Create token (secure random)
                $token = bin2hex(random_bytes(16));
                $expires_at = date('Y-m-d H:i:s', strtotime('+1 hour'));

                $created = $this->resetPassword->createToken($email, $token, $expires_at);

                if ($created) {
                    // Here you would send the email with the token (out of scope)
                    http_response_code(201);
                    echo json_encode(["message" => "Token created, check your mail", "token" => $token]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Error creating token"]);
                }
                break;

            case 'PUT': // Change password using token
                if (!$data || !isset($data['token']) || !isset($data['new_password'])) {
                    http_response_code(400);
                    echo json_encode(["message" => "Token and new password required"]);
                    return;
                }

                $token = $data['token'];
                $new_password = $data['new_password'];

                // Validate token
                $tokenData = $this->resetPassword->validateToken($token);
                if (!$tokenData || $tokenData->num_rows == 0) {
                    http_response_code(400);
                    echo json_encode(["message" => "Invalid or expired token"]);
                    return;
                }

                $row = $tokenData->fetch_assoc();
                $email = $row['email'];

                // Update password
                $password_hash = password_hash($new_password, PASSWORD_DEFAULT);
                $updated = $this->login->updatePassword($email, $password_hash);

                if ($updated) {
                    // Mark token as used
                    $this->resetPassword->markTokenUsed($token);
                    http_response_code(200);
                    echo json_encode(["message" => "Password updated correctly"]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Error updating password"]);
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
