<?php
// Template for reset_password table
class ResetPassword {
    private $conn;
    private $table_name = "reset_password";

    public $id;
    public $email;
    public $token;
    public $created_at;
    public $expires_at;
    public $used;

    public function __construct($db) {
        $this->conn = $db;
    }

    // Create a password reset token
    public function createToken($email, $token, $expires_at) {
        $sql = "INSERT INTO " . $this->table_name . " (email, token, expires_at) VALUES (?, ?, ?)";
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) return false;
        $stmt->bind_param("sss", $email, $token, $expires_at);
        return $stmt->execute() ? $this->conn->insert_id : false;
    }

    // Validate active token (not used and not expired)
    public function validateToken($token) {
        $sql = "SELECT * FROM " . $this->table_name . " WHERE token = ? AND used = 0 AND expires_at > NOW()";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("s", $token);
        $stmt->execute();
        return $stmt->get_result();
    }

    // Mark token as used
    public function markTokenUsed($token) {
        $sql = "UPDATE " . $this->table_name . " SET used = 1 WHERE token = ?";
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) return false;
        $stmt->bind_param("s", $token);
        return $stmt->execute();
    }
}
?>
