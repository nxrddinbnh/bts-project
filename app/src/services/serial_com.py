import serial
import time
from services.api_service import APIService
from constants import VARIABLES_NAME, CMD_LIGHT, CMD_MOTOR_ELEV, CMD_MOTOR_AZIM, CMD_CORRECT, REQUEST_DATA, END_FRAME

class SerialCommunication:
    def __init__(self, serial_config, brightness_mod=None, energy_mod=None, correction_mod=None, motor_mod=None):
        """
        Initializes the serial communication using the settings from SerialConfig
        :param serial_config: To get the serial configuration
        :param brightness_mod: To update the module labels
        """
        self.serial_config = serial_config
        self.serial_connection = None
        self.brightness_mod = brightness_mod
        self.energy_mod = energy_mod
        self.correction_mod = correction_mod
        self.motor_mod = motor_mod
        self.api_service = APIService()

    def connect(self):
        """Establishes a connection to the serial port"""
        config = self.serial_config.get_config()
        port = config["port"]
        baudrate = config["baudrate"]
        timeout = config["timeout"]
        
        if not port:
            print("No available serial port found")
            return
        
        if self.serial_connection and self.serial_connection.is_open:
            print(f"Already connected to {port}")
            return True
        
        try:
            self.serial_connection = serial.Serial(
                port=port, baudrate=baudrate, timeout=timeout
            )
        except serial.SerialException as e:
            print(f"Failed to connect to {port}: {e}")
            return False
        
    def disconnect(self):
        """Closes the serial connection if it's open"""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
            except serial.SerialException as e:
                raise Exception(f"Failed to disconnect from {self.serial_connection.port}: {e}")

    def parse_data(self, data, to_api):
        """
        Parse data received from the serial port
        :param data: Raw data received in bytes
        :param to_api: to know if to send it to the api
        :return A dictionary containing values
        """
        try:
            frame = data.decode('ascii').strip()
            # print(f"trame: {frame}")
            
            if frame.startswith('FA') and frame.endswith('0D'):
                filtered_frame = frame[2:-2] # Remove 0xFA and 0x0D
                parsed_data = {}
                index = 0

                # Extract data according to field length
                for key, info in VARIABLES_NAME.items():
                    length = info["length"]
                    value = filtered_frame[index:index + length].strip()
                    parsed_data[key] = value
                    index += length
                    index += info.get("skip", 0)

                self.update_modules(data=parsed_data)
                if to_api: self.api_service.send_data(parsed_data) # Sends the data to the API
                # print(parsed_data)
                return parsed_data
            else:
                print("Incomplete or invalid frame")
                return None
        except Exception as e:
            print(f"Error parsing data: {e}")
            return None
        
    def receive_data(self, to_api):
        """
        Receives data from the serial port
        :param to_api: to know if to send it to the api
        :return: Data received (as bytes) or None if no data is available
        """
        if not self.serial_connection:
            raise Exception("Not connected to any serial port")
        
        try:
            time.sleep(0.1)  # Allow time for data to arrive
            buffer = b""

            # Keep reading while data is available in the buffer
            while self.serial_connection.in_waiting > 0:
                raw_data = self.serial_connection.read(self.serial_connection.in_waiting)
                buffer += raw_data

            # Decode once
            try:
                decoded = buffer.decode("ascii")
            except UnicodeDecodeError:
                print("Failed to decode serial data")
                return None
            
            # Process all complete frames
            while True:
                start = decoded.find("FA")
                end = decoded.find("0D", start)
                if start == -1 or end == -1:
                    break

                # Process one complete frame at a time
                frame = decoded[start:end + 2]
                parsed = self.parse_data(frame.encode("ascii"), to_api)
                return parsed 
            return None
        except serial.SerialException as e:
            raise Exception(f"Failed to receive data: {e}")
        
    def send_command(self, command, values=None, to_api=False):
        """
        Sends a command to the device and waits for a response
        :param command: Command to be sent to the device
        :param values: Values to be sent along with the command (optional)
        :param to_api: to know if to send it to the api (optional)
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
            elif command == CMD_CORRECT:
                mode, threshold, period = values[0], values[1], values[2]
                self.serial_connection.write(bytes([command]))
                self.serial_connection.write(str(mode).zfill(2).encode('ascii'))
                self.serial_connection.write(str(threshold).zfill(2).encode('ascii'))
                self.serial_connection.write(str(period).zfill(2).encode('ascii'))
            elif command == CMD_MOTOR_ELEV:
                direction, duration, park = values[0], values[1], values[2]
                self.serial_connection.write(bytes([command]))
                self.serial_connection.write(str(direction).zfill(2).encode('ascii'))
                self.serial_connection.write(str(duration).zfill(2).encode('ascii'))
                self.serial_connection.write(str(park).zfill(1).encode('ascii'))
            elif command == CMD_MOTOR_AZIM:
                direction, duration, park = values[0], values[1], values[2]
                self.serial_connection.write(bytes([command]))
                self.serial_connection.write(str(direction).zfill(2).encode('ascii'))
                self.serial_connection.write(str(duration).zfill(2).encode('ascii'))
                self.serial_connection.write(str(park).zfill(1).encode('ascii'))
            elif command == REQUEST_DATA:
                self.serial_connection.write(bytes([command]))

            self.serial_connection.write(bytes([END_FRAME]))
        except serial.SerialException as e:
            raise Exception(f"Failed to send command: {e}")

        return self.receive_data(to_api)
    
    def update_modules(self, data):
        """
        Update all system modules based on the latest parsed data
        :param data: Parsed data
        """
        try:
            if self.brightness_mod: self.brightness_mod.update_values(data)
            if self.energy_mod: self.energy_mod.update_values(data)
            if self.correction_mod and "motor_on" in data: 
                self.correction_mod.is_moving = (data["motor_on"] == "01")
            if self.motor_mod: self.motor_mod.update_values(data)
        except Exception as e:
            raise Exception(f"Failed to update modules: {e}")
