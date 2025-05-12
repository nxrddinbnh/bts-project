from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from base import set_module_style, title_label, create_input, create_label, create_button
from constants import FONT_BODY, PRIMARY, BG_100, TEXT_100, TEXT_200, RADIUS_100, CMD_CORRECT, VARIABLES_NAME

class Correction(QFrame):
    def __init__(self, serial_com):
        """
        Initializes the Correction widget
        :serial_com: SerialCommunication instance for handling communication
        """
        super().__init__()
        self.serial_com = serial_com
        self.button_states = {"auto": False, "manual": False}
        self.buttons = {}
        set_module_style(self)
        self.setup_ui()

        correction_on = VARIABLES_NAME.index("correction_on")
        self.toggle_button("auto" if correction_on else "manual")

    def setup_ui(self):
        """Setup UI layout for the correction module"""
        layout = QVBoxLayout(self)
        layout.addWidget(title_label("correction")) # Title label

        # Input for Period
        period_label = create_label("Period (min)" , FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        self.period_input = create_input(0, 15, 15)
        self.period_input.valueChanged.connect(self.send_command)
        layout.addWidget(period_label)
        layout.addWidget(self.period_input)

        # Input for Lum Threshold
        lum_thres_label = create_label("Lum Threshold" , FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        self.lum_thres_input = create_input(0, 100, 4)
        self.lum_thres_input.valueChanged.connect(self.send_command)
        layout.addWidget(lum_thres_label)
        layout.addWidget(self.lum_thres_input)

        # Manual correction button
        manual_btn = create_button("Manual Correction", FONT_BODY, self.set_button_style(False), lambda _, n="manual": self.toggle_button(n))
        self.buttons["manual"] = manual_btn
        layout.addWidget(manual_btn)

        # Automatic correction button
        automatic_btn = create_button("Auto Correction", FONT_BODY, self.set_button_style(False), lambda _, n="auto": self.toggle_button(n))
        self.buttons["auto"] = automatic_btn
        layout.addWidget(automatic_btn)

        self.setLayout(layout)

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
            return
        
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

        self.send_command()

    def get_mode(self):
        """
        Returns the current correction mode based on button state
        :return: 0 if no button is active, 1 if manual is active, 2 if auto is active
        """
        if self.button_states["manual"]: return 0
        elif self.button_states["auto"]: return 2
        else: return 0
    
    def get_threshold(self):
        """
        Returns the current value of the Lum Threshold input
        :return: Integer value of lum_thres_input
        """
        return self.lum_thres_input.value()

    def get_period(self):
        """
        Returns the current value of the Period input
        :return: Integer value of period_input
        """
        return self.period_input.value()

    def send_command(self):
        """Send the command to the panel"""
        mode = self.get_mode()
        threshold = self.get_threshold()
        period = self.get_period()
        self.serial_com.send_command(CMD_CORRECT, (mode, threshold, period))
