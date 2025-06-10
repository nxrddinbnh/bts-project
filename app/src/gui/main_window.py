from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from services.serial_config import SerialConfig
from modules.brightness import Brightness
from services.serial_com import SerialCommunication
from gui.sidebar import Sidebar
from modules.lighting import Lighting
from modules.general import General
from modules.energy import Energy
from modules.correction import Correction
from modules.motor import Motor
from gui.home_page import HomePage
from gui.search_page import SearchPage
from base import load_fonts
from constants import BG_300

class MainWindow(QMainWindow):
    def __init__(self):
        """Initialize the main window and its components"""
        super().__init__()
        self.serial_config = SerialConfig()
        self.brightness = Brightness()
        self.energy = Energy()
        self.serial_com = SerialCommunication(self.serial_config, self.brightness, self.energy)
        self.serial_com.connect()

        # Initialize modules
        self.lighting = Lighting(self.serial_com)
        self.general = General(self.serial_com, self.serial_config)
        self.correction = Correction(self.serial_com, self)
        self.serial_com.correction_mod = self.correction
        self.motor = Motor(self.serial_com, self)
        self.serial_com.motor_mod = self.motor

        # Sidebar and stacked pages
        self.sidebar = Sidebar()
        self.stack = QStackedWidget()
        self.pages = {}

        load_fonts()
        self.setup_ui()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        QTimer.singleShot(0, self.center_window)

    def setup_ui(self):
        """Configure the UI layout of the main window"""
        self.setWindowTitle("SunHub")
        self.setStyleSheet(f"background-color: {BG_300};")
        self.setWindowIcon(QIcon("assets/logo.svg"))

        # Main layout
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QHBoxLayout()

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)
        layout.setStretch(0, 1)
        layout.setStretch(1, 10)
        widget.setLayout(layout)

        # Connect sidebar navigation
        self.sidebar.navigate.connect(self.show_page)
        self.init_pages()
        self.show_page("home")

    def init_pages(self):
        """Initialize pages and add them to the stack"""
        self.pages["home"] = HomePage(
            self.brightness, self.lighting, self.energy,
            self.correction, self.motor, self.general
        )
        self.pages["search"] = SearchPage()

        for page in self.pages.values():
            self.stack.addWidget(page)

    def show_page(self, name):
        """
        Set the current page by name if it exists
        :param name: The name of the page"""
        if name in self.pages:
            self.stack.setCurrentWidget(self.pages[name])

    def center_window(self):
        """Sets the size and position of the window in the center of the screen"""
        screen = QApplication.primaryScreen()
        if screen: 
            screen_geometry = screen.geometry()
            width, height = 1280, 720
            x = (screen_geometry.width() - width) // 2
            y = (screen_geometry.height() - height) // 2
            self.setGeometry(x, y, width, height)
            