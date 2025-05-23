<?php
// Model for the can_frames table
class CanFrame {
    private $conn;
    private $table_name = "can_frames";

    // Properties according to the can_frames table
    public $id;
    public $date;
    public $east;
    public $west;
    public $north;
    public $average;
    public $v_panel;
    public $v_battery;
    public $c_panel;
    public $c_battery;
    public $charge_state;
    public $light_on;
    public $light_lvl;
    public $curr_elev;
    public $curr_azim;
    public $angle_azim;
    public $angle_elev;
    public $corr_mode;
    public $corr_interval;
    public $corr_threshold;

    public function __construct($db) {
        $this->conn = $db;
    }

    // Get all the records sorted by descending date
    public function readAll() {
        $sql = "SELECT * FROM " . $this->table_name . " ORDER BY date DESC";
        $result = $this->conn->query($sql);
        return $result;
    }

    // Get a record by ID
    public function readOne($id) {
        $sql = "SELECT * FROM " . $this->table_name . " WHERE id = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("i", $id);
        $stmt->execute();
        return $stmt->get_result();
    }

    // Create a new record
    public function create($data) {
        $sql = "INSERT INTO " . $this->table_name . " (date, east, west, north, average, v_panel, v_battery, c_panel, c_battery, charge_state, light_on, light_lvl, curr_elev, curr_azim, angle_azim, angle_elev, corr_mode, corr_interval, corr_threshold) VALUES (NOW(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) return false;

        $stmt->bind_param(
            "iiiiiiiiiisisiiiii",
            $data['east'], $data['west'], $data['north'], $data['average'], $data['v_panel'], $data['v_battery'], $data['c_panel'], $data['c_battery'], $data['charge_state'], $data['light_on'], $data['light_lvl'], $data['curr_elev'], $data['curr_azim'], $data['angle_azim'], $data['angle_elev'], $data['corr_mode'], $data['corr_interval'], $data['corr_threshold']
        );

        return $stmt->execute() ? $this->conn->insert_id : false;
    }

    // Update an existing record by ID
    public function update($id, $data) {
        $sql = "UPDATE " . $this->table_name . " SET date=NOW(), east=?, west=?, north=?, average=?, v_panel=?, v_battery=?, c_panel=?, c_battery=?, charge_state=?, light_on=?, light_lvl=?, curr_elev=?, curr_azim=?, angle_azim=?, angle_elev=?, corr_mode=?, corr_interval=?, corr_threshold=? WHERE id=?";
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) return false;

        $stmt->bind_param(
            "iiiiiiiiiisisiiiiii",
            $data['east'], $data['west'], $data['north'], $data['average'], $data['v_panel'], $data['v_battery'], $data['c_panel'], $data['c_battery'], $data['charge_state'], $data['light_on'], $data['light_lvl'], $data['curr_elev'], $data['curr_azim'], $data['angle_azim'], $data['angle_elev'], $data['corr_mode'], $data['corr_interval'], $data['corr_threshold'], $id
        );

        return $stmt->execute();
    }

    // Delete a record by ID
    public function delete($id) {
        $sql = "DELETE FROM " . $this->table_name . " WHERE id = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("i", $id);
        return $stmt->execute();
    }
}
?>
