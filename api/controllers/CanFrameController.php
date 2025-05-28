<?php
require_once __DIR__ . '/../models/CanFrame.php';

// Controller to handle HTTP requests for can_frames
class CanFrameController {
    private $canFrame;

    public function __construct($db) {
        $this->canFrame = new CanFrame($db);
    }

    public function processRequest($method, $id = null, $data = null) {
        header('Content-Type: application/json; charset=utf-8');
        
        switch ($method) {
            case 'GET':
                if ($id) {
                    $result = $this->canFrame->findById($id);
                    if ($result && $result->num_rows > 0) {
                        http_response_code(200);
                        echo json_encode($result->fetch_assoc());
                    } else {
                        http_response_code(404);
                        echo json_encode(["message" => "Data not found"]);
                    }
                } else {
                    $filters = $_GET;
                    unset($filters['path']);
                    
                    if (count($filters) > 0) {
                        $result = $this->canFrame->findByFilters($filters);
                    } else {
                        $result = $this->canFrame->getAll();
                    }

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

            default:
                http_response_code(405);
                echo json_encode(["message" => "Method not allowed"]);
                break;
        }
    }
}
?>