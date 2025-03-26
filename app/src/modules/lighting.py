from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QVBoxLayout, QSizePolicy, QSlider, QGridLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from constants import BG_100, BG_200, RADIUS_100, RADIUS_200, PADD_200, FONT_TITLE, FONT_BODY, FONT_VALUES, PRIMARY, CMD_LIGHT

class Lighting(QFrame):
    def __init__(self, serial_com):
        """
        Initializes the Lighting widget

        :serial_com: SerialCommunication instance for handling communication
        """
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_200}px; padding: {PADD_200}px;")
        self.serial_com = serial_com
        self.setup_ui()

    def setup_ui(self):
        """Setup UI layout for the lighting module"""
        main_layout = QVBoxLayout(self)
        layout  = QGridLayout()

        # Title label
        title_label = self.create_label("lighting", FONT_TITLE, "padding-left: 0; color: white;", alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(title_label)

        # Slider Frame
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 15)
        self.slider.setValue(7)
        self.slider.setStyleSheet(self.set_slider_style(True))
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.slider.valueChanged.connect(self.send_command)
        layout.addWidget(self.slider, 0, 0, 3, 1)

        # Slider icon label
        icon_slider = self.create_label("", FONT_BODY, "color: white; padding: 0; background: none;", "assets/icons/sun.svg")
        layout.addWidget(icon_slider, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.create_buttons(layout)

        main_layout.addLayout(layout)
        self.setLayout(main_layout)

    def create_label(self, text, font, style, icon_path=None, alignment=Qt.AlignmentFlag.AlignCenter):
        """
        Creates a QLabel with specified text, font, and style

        :param text: Text to be displayed in the label
        :param font: Font style to be applied to the label
        :param style: CSS style string to format the label
        :param icon_path: Icon file path (optional)
        :param alignment: Text alignement (optional)
        :return: A QLabel object with the specified properties
        """
        label = QLabel(text.upper())
        label.setFont(font)
        label.setStyleSheet(style)
        label.setAlignment(alignment)
        if icon_path:
            label.setPixmap(QPixmap(icon_path).scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
        return label
    
    def set_slider_style(self, is_disabled):
        """Returns the stylesheet for the slider based on its state"""
        color = "gray" if is_disabled else PRIMARY
        self.slider.setEnabled(not is_disabled)
        return f"""
            QSlider {{
                min-width: 90px;
                padding: 0;
                border-radius: {RADIUS_100}px;
            }}
            QSlider::groove:vertical {{
                background: {color};
                border-radius: {RADIUS_100}px;
            }}
            QSlider::sub-page:vertical {{
                background-color: {BG_100};
            }}
            QSlider::handle:vertical {{
                height: 0px;
                background: none;
            }}
        """
    
    def create_buttons(self, layout):
        """Create buttons to control the panel LEDs"""
        self.buttons = {}
        button_positions = [
            (0, 1, 1, 2, "1"), (0, 3, 2, 1, "2"),
            (1, 1, 2, 1, "4"), (2, 2, 1, 2, "3"),
            (1, 2, 1, 1, "All")
        ]
        self.button_states = {
            "1": False, "2": False, "3": False,
            "4": False, "All": False
        }

        for row, col, row_span, col_span, btn_name in button_positions:
            button = QPushButton(btn_name)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFont(FONT_VALUES)
            button.setStyleSheet(self.set_button_style(False))
            button.clicked.connect(lambda _, num=btn_name: self.toggle_button(num))
            self.buttons[btn_name] = button
            layout.addWidget(button, row, col, row_span, col_span)

    def set_button_style(self, is_active):
        """Returns the stylesheet for the button based on its state"""
        color = PRIMARY if is_active else BG_100
        return f"background-color: {color}; color: white; border-radius: {RADIUS_100}px;"

    def toggle_button(self, button_name):
        """
        Toggles button state and slider status

        :param button_name: The ID of the button clicked
        """
        # Check if the button is already active
        if self.button_states[button_name]:
            self.button_states[button_name] = False
            self.buttons[button_name].setStyleSheet(self.set_button_style(False))
        else:  
            # First deactivate all buttons
            for btn in self.button_states:
                self.button_states[btn] = False
                self.buttons[btn].setStyleSheet(self.set_button_style(False))

            # Activate the selected button
            self.button_states[button_name] = True
            self.buttons[button_name].setStyleSheet(self.set_button_style(True))

            # Update the style of all buttons
            for btn in self.buttons:
                if self.button_states[btn]:
                    self.buttons[btn].setStyleSheet(self.set_button_style(True))
                else:
                    self.buttons[btn].setStyleSheet(self.set_button_style(False))

        # Deactivate the slider if the all button is not activated
        if self.button_states["All"]:
            self.slider.setStyleSheet(self.set_slider_style(False))  # Enable slider
        else:
            self.slider.setStyleSheet(self.set_slider_style(True))  # Disable slider

        self.send_command()

    def send_command(self):
        """Send the command to the panel"""
        brightness_level = int(self.get_brightness_level())
        button_command = self.get_button_command()
        self.serial_com.send_command(CMD_LIGHT, (button_command, brightness_level))

    def get_brightness_level(self):
        """Returns the current brightness level based on the slider"""
        return self.slider.value()
    
    def get_button_command(self):
        """
        Returns the corresponding command based on the activated button

        :return: The command value (0-5)
        """
        if self.button_states["All"]: 
            return 1

        for button, state in self.button_states.items():
            if state and button != "All":
                button_number = int(button)
                return button_number + 1
        return 0
    