<?php
class Database {
    private $host = "172.18.199.9";
    private $db_name = "solarpanel";
    private $username = "root";
    private $password = "%STS*Mauriacdb";
    public $conn;

    public function getConnection() {
        $this->conn = null;
        mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

        try {
            $this->conn = new mysqli($this->host, $this->username, $this->password, $this->db_name);
            $this->conn->set_charset("utf8");
        } catch (mysqli_sql_exception $e) {
            $message = "Database connection error: " . $e->getMessage();
            error_log($message);
            file_put_contents(__DIR__ . '/../logs/error.log', "[" . date('Y-m-d H:i:s') . "] $message" . PHP_EOL, FILE_APPEND);

            http_response_code(500);
            echo json_encode(["message" => "Database connection error"]);
            exit;
        }
        return $this->conn;
    }
}
?>
