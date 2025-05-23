from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from base import set_module_style, title_label, create_label, create_combo, create_input
from constants import TEXT_200, FONT_BODY, REQUEST_DATA

class General(QFrame):
    def __init__(self, serial_com, serial_config):
        """
        Initializes the General widget
        :param serial_com: The serial communication object for sending commands
        :param serial_config: The serial configuration object
        """
        super().__init__()
        self.serial_com = serial_com
        self.serial_config = serial_config
        set_module_style(self)
        self.setup_ui()

        # Timer to request data from the panel
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.make_request)
        self.update_period(5000)

    def setup_ui(self):
        """Set up the layout and UI components for the general module"""
        layout = QVBoxLayout(self)
        layout.addWidget(title_label("general")) # Title label
        grid = QGridLayout()

        # ComboBox for available ports
        port_label = create_label("Port", FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        available_ports = [self.serial_config.get_config()["port"]] + self.serial_config.get_available_ports()
        available_ports.sort(key=lambda p: int(p.replace("COM", "")))  # Order the ports numerically
        port_combo = create_combo(available_ports, self.serial_config.get_config()["port"])
        port_combo.currentTextChanged.connect(self.update_port)

        # ComboBox for baudrates
        baud_label = create_label("Baud Rate" , FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        baudrates = [115200, 57600, 38400, 19200, 9600, 1200, 300]
        baud_combo = create_combo(baudrates, "9600")
        baud_combo.currentTextChanged.connect(self.update_baudrate)

        # Input for Timeout
        timeout_label = create_label("Timeout (ms)" , FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        timeout_input = create_input(0, 60000, 1000)
        timeout_input.valueChanged.connect(self.update_timeout)

        # Input for Period of Measurement
        period_label = create_label("Period (s)" , FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        period_input = create_input(1, 60, 5)
        period_input.valueChanged.connect(self.update_period)

        # Add widgets to grid layout
        grid.addWidget(port_label, 0, 0)
        grid.addWidget(port_combo, 1, 0)
        grid.addWidget(baud_label, 2, 0)
        grid.addWidget(baud_combo, 3, 0)
        grid.addWidget(timeout_label, 4, 0)
        grid.addWidget(timeout_input, 5, 0)
        grid.addWidget(period_label, 6, 0)
        grid.addWidget(period_input, 7, 0)

        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def update_port(self, port):
        """
        Updates the port in the serial configuration
        :param port: The new port to set
        """
        self.serial_config.set_port(port)
        self.reconnect()
    
    def update_baudrate(self, baudrate):
        """
        Updates the baudrate in the serial configuration
        :param baudrate: The new baudrate to set
        """
        self.serial_config.set_baudrate(int(baudrate))
        self.reconnect()

    def update_timeout(self, timeout):
        """
        Updates the timeout value in the serial configuration
        :param timeout: The new timeout value to set
        """
        self.serial_config.set_timeout(timeout // 1000)
        self.reconnect()

    def update_period(self, period):
        """
        Updates the measurement period in the serial configuration and sets the timer interval
        :param period: The period value for the measurement
        """
        self.timer.setInterval(period * 1000)
        self.timer.start()

    def reconnect(self):
        """Reconnects the serial communication with updated settings"""
        try:
            self.serial_com.disconnect()
            self.serial_com.connect()
        except Exception as e:
            print(f"Error during reconnection: {e}")

    def make_request(self):
        """Request data from the panel depending on the period"""
        try:
            self.serial_com.send_command(REQUEST_DATA)
        except Exception as e:
            print(f"Error during request: {e}")
