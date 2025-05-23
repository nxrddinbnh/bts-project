import requests
#172.18.199.9

class APIService:
    def __init__(self):
        """Initializes the APIService with the base URL and default headers"""
        self.base_url = "http://localhost/solarpanel/api/index.php?path=can_frames"
        self.headers = {"Content-Type": "application/json"}
        self.session = requests.Session()
        self.timeout = 1

    def map_charge_state(self, data):
        """
        Converts between internal charge indicator variables and the API's charge_state field
        :param data: Dictionary containing either internal variables or API data
        :return: A new dictionary with the mapped charge state fields
        """
        result = data.copy()
        if data.get("charging") == "1": charge_state = "charging"
        elif data.get("full") == "1": charge_state = "full"
        elif data.get("empty") == "1": charge_state = "empty"
        else: charge_state = "unknown"

        for key in ["charge", "full_charge", "empty_charge"]:
            result.pop(key, None)

        result["charge_state"] = charge_state
        return result
    
    def send_data(self, data):
        """
        Sends data to the API using a POST request
        :param data: A dictionary containing the data to send to the API
        :return: The API's JSON response or an error message
        """
        try:
            mapped_data = self.map_charge_state(data)
            response = self.session.post(self.base_url, json=mapped_data, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
        
    def get_all(self):
        """
        Retrieves all records from the API using a GET request
        :return: The API's JSON response containing the data or an error message
        """
        try:
            response = self.session.get(self.base_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                return {"success": True, "data": data}
            elif isinstance(data, dict) and "data" in data:
                return {"success": True, "data": data["data"]}
            else:
                return {"success": False, "error": "Unexpected data format"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def get_by_id(self, id):
        """
        Retrieves a specific record by its ID using a GET request
        :param id: The ID of the record to retrieve
        :return: The API's JSON response with the record or an error message
        """
        try:
            response = self.session.get(f"{self.base_url}/{id}", headers=self.headers, timeout=self.timeout)
            if response.status_code == 404:
                return {"success": False, "error": "Record not found", "data": None}
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "id" in data:
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": "Unexpected data format", "data": None}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e), "data": None}
