import serial
import time
from services.serial_config import SerialConfig
from constants import END_FRAME

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

    def connect(self):
        """Establishes a connection to the serial port"""
        try:
            self.serial_connection = serial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                timeout = self.timeout
            )
            print(f"Connected to {self.port} at {self.baudrate} baud")
        except serial.SerialException as e:
            raise Exception(f"Failed to connect to {self.port}: {e}")
        
    def receive_data(self):
        """
        Receives data from the serial port

        :return: Data received (as bytes or bytearray)
        """
        if not self.serial_connection:
            raise Exception("Not connected to any serial port")
        
        try:
            time.sleep(0.1)  # Allow time for data to arrive
            data = self.serial_connection.read_all()
            print(f"Data received: {data}")
            return data
        except serial.SerialException as e:
            raise Exception(f"Failed to receive data: {e}")
        
    def send_command(self, command):
        """
        Sends a command to the device and waits for a response

        :param command: Command to be sent to the device
        :return: Response from the device
        """
        if not self.serial_connection:
            raise Exception("Not connected to any serial port")
        
        try:
            self.serial_connection.write(bytes([command]))
            print(f"Data sent: {command}")
            self.serial_connection.write(bytes([END_FRAME]))
            print(f"End of frame sent: {END_FRAME}")
        except serial.SerialException as e:
            raise Exception(f"Failed to send command: {e}")

        return self.receive_data()
    