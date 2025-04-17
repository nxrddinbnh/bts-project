from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt
from base import set_module_style, title_label, create_label
from constants import BG_OPACITY, RADIUS_100, FONT_VALUES, PADD_100, TEXT_100, TEXT_200, FONT_BODY

class Brightness(QFrame):
    def __init__(self):
        """Initializes the Brightness widget"""
        super().__init__()
        self.value_labels = {}
        set_module_style(self)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the UI layout for the brightness module"""
        layout = QVBoxLayout(self)
        layout.addWidget(title_label("brightness")) # Title label

        # Frames
        sensor_layout = QHBoxLayout()
        for text in ["north", "south", "east", "west", "average"]:
            frame = self.create_frame(0, text.upper())
            sensor_layout.addWidget(frame)

        layout.addLayout(sensor_layout)
        self.setLayout(layout)

    def create_frame(self, value, text):
        """
        Creates a frame with a number above and the label below
        :param value: Value to be displayed
        :param label: Label for the value (e.g., "NORTH", "SOUTH")
        :return: QFrame containing the sensor data.
        """
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {BG_OPACITY}; border-radius: {RADIUS_100}px;")
        layout = QVBoxLayout(frame)

        # Spacer to push widgets to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        # Create and add value label
        value_label = create_label(str(value), FONT_VALUES, f"background-color: transparent; color: {TEXT_100}; padding: {PADD_100}px")
        self.value_labels[text] = value_label
        layout.addWidget(value_label)

        # Title label
        text_label = create_label(text, FONT_BODY, f"background-color: transparent; color: {TEXT_200}; padding: 0px")
        layout.addWidget(text_label)

        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setLayout(layout)
        return frame

    def update_values(self, data):
        """
        Updates sensor values
        :param data: Parsed data
        """
        for key, label in self.value_labels.items():
            value = data.get(f"lum_{key.lower()}")
            label.setText(str(value))
