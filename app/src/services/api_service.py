import requests
from constants import ALLOWED_KEYS  

class APIService:
    def __init__(self):
        """Initializes the APIService with the base URL and default headers"""
        self.base_url = "http://172.18.199.9/pannelsolar/api/index.php"
        self.headers = {"Content-Type": "application/json"}

    def map_charge_state(self, data, to_api=True):
        """
        Converts between internal charge indicator variables and the API's charge_state field
        :param data: Dictionary containing either internal variables or API data
        :param to_api: Boolean flag, True to convert internal -> API, False for API -> internal
        :return: A new dictionary with the mapped charge state fields
        """
        if to_api:
            # From internal variables to API
            if data.get("charge") == "1": charge_state = "charging"
            elif data.get("full_charge") == "1": charge_state = "full"
            elif data.get("empty_charge") == "1": charge_state = "empty"
            else: charge_state = "unknown"

            result = data.copy()
            for key in ["charge", "full_charge", "empty_charge"]:
                result.pop(key, None)
            result["charge_state"] = charge_state
            return result
        else:
            # From API to internal variables
            charge_state = data.get("charge_state", "unknown")
            charge_map = {
                "charging": ("1", "0", "0"),
                "full": ("0", "1", "0"),
                "empty": ("0", "0", "1"),
            }

            charge, full_charge, empty_charge = charge_map.get(charge_state, ("0", "0", "0"))
            result = data.copy()
            result.pop("charge_state", None)
            result["charge"] = charge
            result["full_charge"] = full_charge
            result["empty_charge"] = empty_charge
            return result

    def send_data(self, data):
        """
        Sends data to the API using a POST request
        :param data: A dictionary containing the data to send to the API
        :return: The API's JSON response or an error message
        """
        try:
            filtered_data = {k: v for k, v in data.items() if k in ALLOWED_KEYS}
            mapped_data = self.map_charge_state(filtered_data, to_api=True)
            response = requests.post(self.base_url, json=mapped_data, headers=self.headers, timeout=0.1)
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
            response = requests.get(self.base_url, headers=self.headers, timeout=0.1)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def get_by_id(self, id):
        """
        Retrieves a specific record by its ID using a GET request
        :param id: The ID of the record to retrieve
        :return: The API's JSON response with the record or an error message
        """
        try:
            response = requests.get(f"{self.base_url}?id={id}", headers=self.headers, timeout=0.1)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
