<?php
require_once __DIR__ . '/../models/CanFrame.php';

// Controller to handle HTTP requests for can_frames
class CanFrameController {
    private $canFrame;

    public function __construct($db) {
        $this->canFrame = new CanFrame($db);
    }

    /**
     * Processing HTTP request: GET, POST, PUT, DELETE
     *
     * @param string $method HTTP Method
     * @param int|null $id Resource ID (optional)
     * @param array|null $data Data received in POST or PUT (optional)
     * @return void
     */
    public function processRequest($method, $id = null, $data = null) {
        header('Content-Type: application/json; charset=utf-8');
        
        switch ($method) {
            case 'GET':
                if ($id) {
                    $result = $this->canFrame->readOne($id);
                    if ($result && $result->num_rows > 0) {
                        http_response_code(200);
                        echo json_encode($result->fetch_assoc());
                    } else {
                        http_response_code(404);
                        echo json_encode(["message" => "Data not found"]);
                    }
                } else {
                    $result = $this->canFrame->readAll();
                    if ($result && $result->num_rows > 0) {
                        $data = [];
                        while ($row = $result->fetch_assoc()) {
                            $data[] = $row;
                        }
                        http_response_code(200);
                        echo json_encode($data);
                    } else {
                        http_response_code(404);
                        echo json_encode(["message" => "Data not found"]);
                    }
                }
                break;

            case 'POST':
                if (!$data) {
                    http_response_code(400);
                    echo json_encode(["message" => "Data not provided"]);
                    return;
                }
                $newId = $this->canFrame->create($data);
                if ($newId) {
                    http_response_code(201);
                    echo json_encode(["message" => "Data created", "id" => $newId]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Error creating data"]);
                }
                break;

            case 'PUT':
                if (!$id || !$data) {
                    http_response_code(400);
                    echo json_encode(["message" => "ID and required data"]);
                    return;
                }
                $updated = $this->canFrame->update($id, $data);
                if ($updated) {
                    http_response_code(200);
                    echo json_encode(["message" => "Updated data", "id" => $id]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Error updating data"]);
                }
                break;

            case 'DELETE':
                if (!$id) {
                    http_response_code(400);
                    echo json_encode(["message" => "ID required to delete"]);
                    return;
                }
                $deleted = $this->canFrame->delete($id);
                if ($deleted) {
                    http_response_code(200);
                    echo json_encode(["message" => "Data removed", "id" => $id]);
                } else {
                    http_response_code(500);
                    echo json_encode(["message" => "Error deleting data"]);
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
