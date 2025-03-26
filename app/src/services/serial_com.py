import serial
import time
from services.serial_config import SerialConfig
from constants import DATA_VARIABLES_NAME, CMD_LIGHT, CMD_MOTOR_ELEV, CMD_MOTOR_AZIM, CMD_CORRECT, REQUEST_DATA, END_FRAME
from modules.brightness import Brightness

class SerialCommunication:
    """
    A class to handle serial communication with the solar panel control system
    This class provides methods to send and receive data over the serial connection
    """
    def __init__(self):
        """Initializes the serial communication using the settings from SerialConfig"""
        config = SerialConfig().get_config()
        self.port = config["port"]
        self.baudrate = config["baudrate"]
        self.timeout = config["timeout"]
        self.serial_connection = None

        # Modules
        self.brightness_mod = Brightness({})

    def connect(self):
        """Establishes a connection to the serial port"""
        if not self.port:
            print("No available serial port found")
            return

        if self.serial_connection is None or not self.serial_connection.is_open:
            try:
                self.serial_connection = serial.Serial(
                    port = self.port,
                    baudrate = self.baudrate,
                    timeout = 10
                )
                print(f"Connected to {self.port} at {self.baudrate} baud")
            except serial.SerialException as e:
                raise Exception(f"Failed to connect to {self.port}: {e}")
        else:
            print(f"Already connected to {self.port}")
        
    def parse_data(self, data):
        """
        Parse data received from the serial port

        :param data: Raw data received in bytes
        :return A dictionary containing values
        """
        try:
            data_str = data.decode('utf-8').strip()
            filtered_data = data_str[1:-1] # Remove the first (0xFA) and last (0x0D) bytes
            data_values = [int(h, 16) for h in filtered_data.split()]
            
            parsed_data = {DATA_VARIABLES_NAME[i]: data_values[i] if i < len(data_values) else 0 for i in range(len(DATA_VARIABLES_NAME))}
            
            self.update_modules(data=parsed_data)
            return parsed_data
        except Exception as e:
            print(f"Error parsing data: {e}")

    def receive_data(self):
        """
        Receives data from the serial port

        :return: Data received (as bytes) or None if no data is available
        """
        if not self.serial_connection:
            raise Exception("Not connected to any serial port")
        
        try:
            time.sleep(0.05)  # Allow time for data to arrive
            bytes_available = self.serial_connection.in_waiting
            if bytes_available > 0:
                raw_data = self.serial_connection.read(bytes_available)
                print(f"Received: {raw_data}")
                return self.parse_data(raw_data)
            return None
        except serial.SerialException as e:
            raise Exception(f"Failed to receive data: {e}")
        
    def send_command(self, command, values=None):
        """
        Sends a command to the device and waits for a response

        :param command: Command to be sent to the device
        :param values: Values to be sent along with the command (optional)
        :return: Response from the device
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            raise Exception("Not connected to any serial port")
        
        try:
            if command == CMD_LIGHT:
                if values and len(values) >= 2:
                    button_command, brightness_level = values[0], values[1]
                    self.serial_connection.write(bytes([command]))
                    self.serial_connection.write(str(button_command).zfill(2).encode('ascii'))
                    self.serial_connection.write(str(brightness_level).zfill(2).encode('ascii'))
            elif command == REQUEST_DATA:
                self.serial_connection.write(bytes([command]))

            self.serial_connection.write(bytes([END_FRAME]))
        except serial.SerialException as e:
            raise Exception(f"Failed to send command: {e}")

        return self.receive_data()
    
    def update_modules(self, data):
        """
        Update all system modules based on the latest parsed data
        
        :param data: Parsed data
        """
        brightness_values = {
            "lum_north": data.get("lum_north"),
            "lum_south": data.get("lum_south"),
            "lum_east": data.get("lum_east"),
            "lum_west": data.get("lum_west"),
            "lum_avg": data.get("lum_avg")
        }

        self.brightness_mod.update_values(brightness_values)
