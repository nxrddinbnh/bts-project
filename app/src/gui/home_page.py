from PyQt6.QtWidgets import QWidget, QGridLayout

class HomePage(QWidget):
    def __init__(self, brightness, lighting, energy, correction, motor, general):
        """Initialize the Home page with all module widgets"""
        super().__init__()
        self.brightness = brightness
        self.lighting = lighting
        self.energy = energy
        self.correction = correction
        self.motor = motor
        self.general = general
        self.setup_ui()

    def setup_ui(self):
        """Layout the modules in a grid"""
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.brightness, 0, 0, 1, 3)
        layout.addWidget(self.lighting, 0, 3, 1, 2)
        layout.addWidget(self.energy, 1, 0, 1, 1)
        layout.addWidget(self.correction, 1, 1, 1, 1)
        layout.addWidget(self.motor, 1, 2, 1, 2)
        layout.addWidget(self.general, 1, 4, 1, 1)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 3)
        layout.setColumnStretch(4, 3)

        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)

        self.setLayout(layout)
