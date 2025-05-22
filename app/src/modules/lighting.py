from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGridLayout, QSlider
from PyQt6.QtCore import Qt
from base import set_module_style, title_label, create_label, create_button
from constants import BG_100, PRIMARY, TEXT_100, FONT_BODY, FONT_VALUES, RADIUS_100, CMD_LIGHT

class Lighting(QFrame):
    def __init__(self, serial_com):
        """
        Initializes the Lighting widget
        :serial_com: SerialCommunication instance for handling communication
        """
        super().__init__()
        self.serial_com = serial_com
        self.buttons = {}
        set_module_style(self)
        self.setup_ui()
        self.send_command()

    def setup_ui(self):
        """Setup UI layout for the lighting module"""
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title_label("lighting")) # Title label
        layout  = QGridLayout()

        # Slider Frame
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 15)
        self.slider.setValue(7)
        self.slider.setStyleSheet(self.set_slider_style(True))
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.slider.valueChanged.connect(self.send_command)
        layout.addWidget(self.slider, 0, 0, 2, 1)

        # Slider icon label
        icon_slider = create_label("", FONT_BODY, f"color: {TEXT_100}; padding: 0; background: none;", icon_path="assets/icons/sun.svg")
        layout.addWidget(icon_slider, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.button_states = {name: False for name in ["1", "2", "3", "4", "All"]}
        button_positions = [
            (0, 1, 1, 1, "1"), (0, 2, 1, 1, "2"),
            (0, 4, 1, 1, "4"), (0, 3, 1, 1, "3"),
            (1, 1, 1, 4, "All")
        ]

        for row, col, row_span, col_span, name in button_positions:
            button = create_button(name, FONT_VALUES, self.set_button_style(False), lambda _, n=name: self.toggle_button(n))
            self.buttons[name] = button
            layout.addWidget(button, row, col, row_span, col_span)

        main_layout.addLayout(layout)
        self.setLayout(main_layout)

    def set_slider_style(self, is_disabled):
        """
        Returns the stylesheet for the slider based on its state
        :param is_disabled: Disable the slider if the "all" button is not active
        """
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
    
    def set_button_style(self, is_active):
        """
        :param is_active: Boolean to indicate the status of the button
        :return: Stylesheet for the button based on its state
        """
        color = PRIMARY if is_active else BG_100
        return f"background-color: {color}; color: {TEXT_100}; border-radius: {RADIUS_100}px;"

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
    