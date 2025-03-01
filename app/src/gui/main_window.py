from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QFrame
from PyQt6.QtGui import QIcon
from constants import BG_300, BG_200
from gui.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.create_bentogrid()

    def setup_ui(self):
        """Configure the UI layout of the main window"""
        self.setWindowTitle("")

        width, height = 1280, 720
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2

        self.setGeometry(x, y, width, height)
        self.setStyleSheet(f"background-color: {BG_300};")
        self.setWindowIcon(QIcon("assets/logo.svg"))

    def create_bentogrid(self):
        """Create the bentogrid design"""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        sidebar = Sidebar()

        def create_block():
            block = QFrame()
            block.setStyleSheet(f"background-color: {BG_200}; border-radius: 20px;")
            return block
        
        # Create and position blocks
        block1 = create_block()
        block2 = create_block()
        block3 = create_block()
        block4 = create_block()
        block5 = create_block()
        block6 = create_block()

        # Add widgets to the grid layout
        layout.addWidget(sidebar, 0, 0, 2, 1)
        layout.addWidget(block1, 0, 1, 1, 3)
        layout.addWidget(block2, 0, 4, 1, 2)
        layout.addWidget(block3, 1, 1, 1, 1)
        layout.addWidget(block4, 1, 2, 1, 1)
        layout.addWidget(block5, 1, 3, 1, 2)
        layout.addWidget(block6, 1, 5, 1, 1)

        layout.setColumnStretch(0, 1)  # Sidebar (más estrecho)
        layout.setColumnStretch(1, 3)  # Bloques grandes
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 3)
        layout.setColumnStretch(4, 3)
        layout.setColumnStretch(5, 3)

        central_widget.setLayout(layout)