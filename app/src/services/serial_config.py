import serial.tools.list_ports

class SerialConfig:
    """A class to manage serial connection settings dynamically"""
    def __init__(self, port=None, baudrate=9600, timeout=1):
        """
        Initialize the serial configuration with default values

        :param port: Serial port name
        :param baudrate: Baud rate for the serial connection
        :param timeout: Timeout in seconds for serial communication
        """
        self._port = port if port else self.find_highest_port()
        self._baudrate = baudrate
        self._timeout = timeout

    def find_highest_port(self):
        """
        Find the highest available serial port

        :return: The highest numbered serial port
        """
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if not ports:
            raise Exception("No available serial ports found")
        
        try:
            highest_port = max(ports, key=lambda p: int(''.join(filter(str.isdigit, p))) if any(c.isdigit() for c in p) else 0)
        except ValueError:
            highest_port = ports[-1]  # If no numerical sorting possible, take the last one

        print(f"Auto-detected highest available port: {highest_port}")
        return highest_port

    def set_port(self, port):
        """
        Update the serial port name

        :param port: New serial port name
        """
        self._port = port

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
