from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QComboBox, QSpinBox, QGridLayout
from PyQt6.QtCore import Qt, QTimer
from constants import BG_100, BG_200, RADIUS_100, RADIUS_200, PADD_100, PADD_200, FONT_TITLE, FONT_BODY, PRIMARY, TEXT_100, TEXT_200, SECONDARY, REQUEST_DATA

class General(QFrame):
    def __init__(self, serial_com, serial_config):
        """
        Initializes the General widget

        :param serial_com: The serial communication object for sending commands
        :param serial_config: The serial configuration object
        """
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_200}px; padding: {PADD_200}px;")
        self.serial_com = serial_com
        self.serial_config = serial_config
        self.setup_ui()

        # Timer to request data from the panel
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.make_request)
        self.update_period(100)

    def setup_ui(self):
        """Set up the layout and UI components for the general module"""
        main_layout = QVBoxLayout(self)
        grid = QGridLayout()

        # Title label
        title_label = QLabel("general".upper())
        title_label.setFont(FONT_TITLE)
        title_label.setStyleSheet("padding-left: 0; color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(title_label)

        # ComboBox for available ports
        port_label = self.create_label("Port")
        port_combo = QComboBox()
        
        available_ports = [self.serial_config.get_config()["port"]] + self.serial_config.get_available_ports()
        available_ports.sort(key=lambda p: int(p.replace("COM", "")))  # Order the ports numerically
        
        port_combo.addItems(available_ports)
        port_combo.setCurrentText(self.serial_config.get_config()["port"])
        port_combo.setStyleSheet(self.combo_box_style(port_combo))
        port_combo.currentTextChanged.connect(self.update_port)

        # ComboBox for baudrates
        baud_label = self.create_label("Baud Rate")
        baud_combo = QComboBox()
        baudrates = [115200, 57600, 38400, 19200, 9600, 1200, 300]
        baud_combo.addItems([str(rate) for rate in baudrates])
        baud_combo.setCurrentText('9600')
        baud_combo.setStyleSheet(self.combo_box_style(baud_combo))
        baud_combo.currentTextChanged.connect(self.update_baudrate)

        # Input for Timeout
        timeout_label = self.create_label("Timeout (ms)")
        timeout_input = QSpinBox()
        timeout_input.setRange(0, 60000)
        timeout_input.setValue(1000)
        timeout_input.setStyleSheet(self.input_style())
        timeout_input.valueChanged.connect(self.update_timeout)

        # Input for Period of Measurement
        period_label = self.create_label("Period (ms)")
        period_input = QSpinBox()
        period_input.setRange(1000, 10000)
        period_input.setValue(2000)
        period_input.setStyleSheet(self.input_style())
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

        main_layout.addLayout(grid)
        main_layout.addStretch()
        self.setLayout(main_layout)
        

    def create_label(self, text):
        """
        Creates a QLabel with specified text, font, and style

        :param text: Text to be displayed in the label
        :return: A QLabel object with the specified properties
        """
        label = QLabel(text)
        label.setFont(FONT_BODY)
        label.setStyleSheet(f"padding: 0; color: {TEXT_200};")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return label
    
    def combo_box_style(self, combobox):
        """
        Returns the stylesheet for ComboBox

        :param combobox: QComboBox to apply family font
        """
        combobox.setFont(FONT_BODY)
        combobox.setCursor(Qt.CursorShape.PointingHandCursor)
        return f"""
            QComboBox {{
                height: 30px;
                background-color: {BG_100};
                border-radius: {RADIUS_100}px;
                padding: {PADD_100}px;
                color: {TEXT_100};
                margin: 2px 0;
            }}
            QComboBox::drop-down {{
                border: 0px;
            }}
            QComboBox::down-arrow {{
                image: url(assets/icons/comboDown.svg);
                height: 20px;
                width: 20px;
                margin-right: 20px;
            }}
            QComboBox::on {{
                border: 1px solid {PRIMARY};
            }}
            QComboBox QListView {{
                padding: {PADD_100}px;
                background-color: {BG_100};
                outline: none;
                border-radius: 0;
            }}
            QComboBox QListView:item {{
                padding: {PADD_200}px;
                color: {TEXT_100};
            }}
            QComboBox QListView:item:selected {{
                background-color: {BG_200};
                color: {SECONDARY};
                padding: {PADD_100}px;
            }}
        """
    
    def input_style(self):
        """Returns the stylesheet for input fields (QSpinBox)"""
        return f"""
            QSpinBox {{
                height: 30px;
                background-color: {BG_100};
                border-radius: {RADIUS_100}px;
                padding: {PADD_100}px;
                color: {TEXT_100};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: transparent;
                border: none;
                width: 0px;
                height: 0px;
            }}
            QSpinBox::focus {{
                border: 1px solid {PRIMARY};
            }}
        """

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
        self.timer.setInterval(period)
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
