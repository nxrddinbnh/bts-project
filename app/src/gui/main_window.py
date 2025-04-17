from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from services.serial_config import SerialConfig
from modules.brightness import Brightness
from services.serial_com import SerialCommunication
from gui.sidebar import Sidebar
from modules.lighting import Lighting
from modules.general import General
from base import load_fonts
from constants import BG_300

class MainWindow(QMainWindow):
    def __init__(self):
        """Initialize the main window and its components"""
        super().__init__()
        self.serial_config = SerialConfig()
        self.brightness = Brightness()
        self.serial_com = SerialCommunication(self.serial_config, self.brightness)
        self.serial_com.connect()

        self.sidebar = Sidebar()
        self.lighting = Lighting(self.serial_com)
        self.general = General(self.serial_com, self.serial_config)
        # self.energy = ""
        # self.correction = ""
        # self.motor = ""

        load_fonts()  
        self.setup_ui()
        self.display_modules()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def setup_ui(self):
        """Configure the UI layout of the main window"""
        self.setWindowTitle("SunHub")
        self.setStyleSheet(f"background-color: {BG_300};")
        self.setWindowIcon(QIcon("assets/logo.svg"))

        # Sets the size and position of the window in the center of the screen
        width, height = 1280, 720
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)

    def display_modules(self):
        """Display modules with a bentogrid design"""
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QGridLayout()
        # layout.setSpacing(10)
        # layout.setContentsMargins(10, 10, 10, 10)

        # Add modules to the grid layout
        layout.addWidget(self.sidebar, 0, 0, 2, 1)
        layout.addWidget(self.brightness, 0, 1, 1, 3)
        layout.addWidget(self.lighting, 0, 4, 1, 2)
        # layout.addWidget(self.energy, 1, 1, 1, 1)
        # layout.addWidget(self.correction, 1, 2, 1, 1)
        # layout.addWidget(self.motor, 1, 3, 1, 2)
        layout.addWidget(self.general, 1, 5, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 3)
        layout.setColumnStretch(4, 3)
        layout.setColumnStretch(5, 3)

        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)

        widget.setLayout(layout)
