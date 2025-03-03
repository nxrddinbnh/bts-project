from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from constants import BG_200, BG_OPACITY, FONT_TITLE, FONT_BODY, FONT_VALUES, TEXT_200, RADIUS_100, RADIUS_200, PADD_100, PADD_200, DIRECTIONS

class Brightness(QFrame):
    def __init__(self, values):
        """
        Initializes the Brightness widget.
        
        :param values: Dictionary containing sensor values, e.g.:
                       {"north": 211, "south": 210, "east": 194, "west": 218, "average": 208}
        """
        super().__init__()
        self.values = values
        self.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_200}px; padding: {PADD_200}px;")
        self.setup_ui()

    def setup_ui(self):
        """Sets up the UI layout for the brightness module"""
        main_layout = QVBoxLayout(self)

        # Title label
        title_label = QLabel("brightness".upper())
        title_label.setFont(FONT_TITLE)
        title_label.setStyleSheet("padding-left: 0;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(title_label)

        # Sensor frames (North, South, East, West)
        sensor_layout = QHBoxLayout()
        for direction in DIRECTIONS:
            sensor_frame = self.create_sensor_frame(self.values[direction], direction.upper())
            sensor_layout.addWidget(sensor_frame)
            sensor_layout.addSpacing(4)

        # Average sensor
        avg_frame = self.create_sensor_frame(self.values["average"], "average".upper())
        sensor_layout.addWidget(avg_frame, stretch=2)

        main_layout.addLayout(sensor_layout)
        self.setLayout(main_layout)

    def create_sensor_frame(self, value, label):
        """
        Creates a sensor frame with a number above and the label below.
        
        :param value: Sensor value to be displayed.
        :param label: Label for the sensor (e.g., "NORTH", "SOUTH").
        :return: QFrame containing the sensor data.
        """
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {BG_OPACITY}; border-radius: {RADIUS_100}px;")
        
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        # Create and add value label
        value_label = self.create_label(str(value), FONT_VALUES)
        layout.addWidget(value_label)

        # Sensor direction label
        text_label = self.create_label(label, FONT_BODY, color=TEXT_200)
        layout.addWidget(text_label)

        frame.setLayout(layout)
        return frame

    def create_label(self, text, font, color=None):
        """
        Creates a QLabel with the specified text and font.
        
        :param text: The text to be displayed in the label.
        :param font: The font to be applied to the label.
        :param color: (Optional) Text color in CSS format (e.g., "white", "#FF0000").
        :return: A QLabel with the specified properties.
        """
        label = QLabel(text)
        label.setFont(font)
        label.setStyleSheet(f"background-color: transparent; color: {color}; padding: 0px" if color else f"background-color: transparent; padding: {PADD_100}px")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
    