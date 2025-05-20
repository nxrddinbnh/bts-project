import serial
import time
from constants import VARIABLES_NAME, FIELD_LENGTHS, CMD_LIGHT, CMD_MOTOR_ELEV, CMD_MOTOR_AZIM, CMD_CORRECT, REQUEST_DATA, END_FRAME

class SerialCommunication:
    def __init__(self, serial_config, brightness_mod=None, energy_mod=None, motor_mod=None):
        """
        Initializes the serial communication using the settings from SerialConfig
        :param serial_config: To get the serial configuration
        :param brightness_mod: To update the module labels
        """
        self.serial_config = serial_config
        self.serial_connection = None
        self.brightness_mod = brightness_mod
        self.energy_mod = energy_mod
        self.motor_mod = motor_mod

    def connect(self):
        """Establishes a connection to the serial port"""
        self.config = self.serial_config.get_config()
        self.port = self.config["port"]
        self.baudrate = self.config["baudrate"]
        self.timeout = self.config["timeout"]
        
        if not self.port:
            print("No available serial port found")
            return
        
        if self.serial_connection is None or not self.serial_connection.is_open:
            try:
                self.serial_connection = serial.Serial(
                    port = self.port,
                    baudrate = self.baudrate,
                    timeout = self.timeout
                )
            except serial.SerialException as e:
                raise Exception(f"Failed to connect to {self.port}: {e}")
        else:
            print(f"Already connected to {self.port}")

    def disconnect(self):
        """Closes the serial connection if it's open"""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
            except serial.SerialException as e:
                raise Exception(f"Failed to disconnect from {self.port}: {e}")
        else:
            print(f"No active connection to {self.port} to disconnect")

    def parse_data(self, data):
        """
        Parse data received from the serial port
        :param data: Raw data received in bytes
        :return A dictionary containing values
        """
        try:
            frame = data.decode('ascii').strip()

            if frame.startswith('FA') and frame.endswith('0D'):
                filtered_frame = frame[2:-2] # Remove 0xFA and 0x0D
                data_values = []
                index = 0

                # Extract data according to field length
                for length in FIELD_LENGTHS:
                    field_value = filtered_frame[index:index + length].strip()
                    data_values.append(field_value)
                    index += length

                parsed_data = {VARIABLES_NAME[i]: data_values[i] for i in range(len(VARIABLES_NAME))}
                self.update_modules(data=parsed_data)
                return parsed_data
            else:
                print("Incomplete or invalid frame")
                return None
        except Exception as e:
            print(f"Error parsing data: {e}")
            return None
        
    def receive_data(self):
        """
        Receives data from the serial port
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
                parsed = self.parse_data(frame.encode("ascii"))
                return parsed 
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

        return self.receive_data()
    
    def update_modules(self, data):
        """
        Update all system modules based on the latest parsed data
        :param data: Parsed data
        """
        try:
            self.brightness_mod.update_values(data)
            self.energy_mod.update_values(data)
            self.motor_mod.update_values(data)
        except Exception as e:
            raise Exception(f"Failed to update modules: {e}")
