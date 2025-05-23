import serial.tools.list_ports
import concurrent.futures

class SerialConfig:
    def __init__(self, baudrate=9600, timeout=1):
        """
        Initialize the serial configuration with default values
        :param baudrate: Baud rate for the serial connection
        :param timeout: Timeout in seconds for serial communication
        """
        self._baudrate = baudrate
        self._timeout = timeout
        self._port = self.find_highest_port()

    def test_port(self, port):
        """
        Test ports 
        :param port: port to test
        :return: the port if it is available
        """
        try:
            s = serial.Serial(port, timeout=0.1)
            s.close()
            return port
        except (OSError, serial.SerialException):
            return None

    def get_available_ports(self):
        """
        Obtain all available COM ports 
        :return: All available ports
        """
        ports = [f"COM{i}" for i in range(1, 51)]
        available_ports = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.test_port, ports)
            for result in results:
                if result is not None: available_ports.append(result)
        return available_ports

    def find_highest_port(self):
        """
        Find the highest available serial port
        :return: The highest numbered serial port
        """
        ports = self.get_available_ports()
        if ports:
            highest = max(ports, key=lambda p: int(''.join(filter(str.isdigit, p)) or 0))
            return highest
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
