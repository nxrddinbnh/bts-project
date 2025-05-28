<?php
class Login {
    private $conn;
    private $table_name = "login";

    public $id;
    public $email;
    public $password;

    public function __construct($db) {
        $this->conn = $db;
    }

    // Create user (registration)
    public function create($email, $password_hash) {
        $sql = "INSERT INTO " . $this->table_name . " (email, password) VALUES (?, ?)";
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) return false;
        $stmt->bind_param("ss", $email, $password_hash);
        return $stmt->execute() ? $this->conn->insert_id : false;
    }

    // Get all users without passwords
    public function getAll() {
        $sql = "SELECT id, email FROM " . $this->table_name;
        $stmt = $this->conn->prepare($sql);
        $stmt->execute();
        return $stmt->get_result();
    }

    // Get user by id without password
    public function findById($id) {
        $sql = "SELECT id, email FROM " . $this->table_name . " WHERE id = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("i", $id);
        $stmt->execute();
        return $stmt->get_result();
    }

    // Get user by email
    public function findByEmail($email) {
        $sql = "SELECT * FROM " . $this->table_name . " WHERE email = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("s", $email);
        $stmt->execute();
        return $stmt->get_result();
    }

    // Update user email and/or password by id
    public function update($id, $email, $password_hash = null) {
        if ($password_hash) {
            $sql = "UPDATE " . $this->table_name . " SET email = ?, password = ? WHERE id = ?";
            $stmt = $this->conn->prepare($sql);
            if (!$stmt) return false;
            $stmt->bind_param("ssi", $email, $password_hash, $id);
        } else {
            $sql = "UPDATE " . $this->table_name . " SET email = ? WHERE id = ?";
            $stmt = $this->conn->prepare($sql);
            if (!$stmt) return false;
            $stmt->bind_param("si", $email, $id);
        }
        return $stmt->execute();
    }

    // Delete user by id
    public function delete($id) {
        $sql = "DELETE FROM " . $this->table_name . " WHERE id = ?";
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) return false;
        $stmt->bind_param("i", $id);
        return $stmt->execute();
    }
}
?>