import serial.tools.list_ports

class SerialConfig:
    """A class to manage serial connection settings dynamically"""
    def __init__(self, baudrate=9600, timeout=1):
        """
        Initialize the serial configuration with default values

        :param port: Serial port name
        :param baudrate: Baud rate for the serial connection
        :param timeout: Timeout in seconds for serial communication
        """
        self._baudrate = baudrate
        self._timeout = timeout
        self._port = self.find_highest_port()

    def get_available_ports(self):
        """
        Obtain all available COM ports 

        :return: All available ports
        """
        available_ports = []

        # COM port routing from 1 to 256
        for i in range(1, 257):
            port = f"COM{i}"
            try:
                s = serial.Serial(port)
                s.close()
                available_ports.append(port)
            except (OSError, serial.SerialException):
                pass

        return available_ports

    def find_highest_port(self):
        """
        Find the highest available serial port

        :return: The highest numbered serial port
        """
        available_ports = self.get_available_ports()

        # Find the highest COM port
        if available_ports:
            highest_port = max(available_ports, key=lambda p: int(p.replace("COM", "")))
            return highest_port
        else:
            return None

    def set_baudrate(self, baudrate):
        """
        Update the baud rate for the serial connection

        :param baudrate: New baud rate
        """
        self._baudrate = baudrate
    
    def set_timeout(self, timeout):
        """
        Update the timeout value for serial communication

        :param timeout: Timeout in seconds
        """
        self._timeout = timeout

    def set_port(self, port):
        """
        Update the serial port name

        :param port: New serial port name
        """
        self._port = port

    def get_config(self):
        """
        Retrieve the current serial configuration settings

        :return: A dictionary containing 'port', 'baudrate', and 'timeout' values
        """
        return {
            "port": self._port,
            "baudrate": self._baudrate,
            "timeout": self._timeout
        }
