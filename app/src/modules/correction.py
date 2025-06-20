from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from gui.toast_notif import ToastNotif
from base import set_module_style, title_label, create_input, create_label, create_button
from constants import FONT_BODY, PRIMARY, BG_100, TEXT_100, TEXT_200, RADIUS_100, CMD_CORRECT

class Correction(QFrame):
    def __init__(self, serial_com, main_window):
        """
        Initializes the Correction widget
        :serial_com: SerialCommunication instance for handling communication
        """
        super().__init__()
        self.serial_com = serial_com
        self.main_window = main_window
        self.toast_notif = ToastNotif(main_window)
        self.active_mode = None
        self.is_moving = False
        self.buttons = {}
        set_module_style(self)
        self.setup_ui()

        self.toggle_button("auto")
        self.send_command()

    def setup_ui(self):
        """Setup UI layout for the correction module"""
        layout = QVBoxLayout(self)
        layout.addWidget(title_label("correction")) # Title label

        # Input for Period
        period_label = create_label("Period (min)" , FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        self.period_input = create_input(0, 15, 10)
        self.period_input.valueChanged.connect(self.send_command)
        layout.addWidget(period_label)
        layout.addWidget(self.period_input)

        # Input for Lum Threshold
        lum_thres_label = create_label("Lum Threshold" , FONT_BODY, f"padding: 0; color: {TEXT_200};", Qt.AlignmentFlag.AlignLeft)
        self.lum_thres_input = create_input(0, 15, 5)
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
        # Do not change if motor is in motion
        if self.is_moving:
            self.toast_notif.show_message("mode_locked")
            return
        
        # Check if the button is already active
        if self.active_mode == button_name:
            return
        
        # Activate the selected button
        self.active_mode = button_name
        for btn in self.buttons:
            is_active = (btn == self.active_mode)
            self.buttons[btn].setStyleSheet(self.set_button_style(is_active))
            
        self.send_command()

    def get_mode(self):
        """
        Returns the current correction mode based on button state
        :return: 0 if no button is active, 1 if manual is active, 2 if auto is active
        """
        return 0 if self.active_mode == "manual" else 2
    
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
