from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QMovie
from base import set_module_style, title_label, create_label
from constants import BG_200, BG_OPACITY, TEXT_100, TEXT_200, FONT_BODY, FONT_BODY_B, RADIUS_100

class Energy(QFrame):
    def __init__(self):
        """Initializes the Energy widget"""
        super().__init__()
        self.value_labels = {}
        set_module_style(self)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the UI layout for the energy module"""
        layout = QVBoxLayout(self)
        layout.addWidget(title_label("energy")) # Title label

        # Measurement frames
        keys_labels = [
            ("volt_panel", "Panel (V)"),
            ("curr_panel", "Panel (I)"),
            ("volt_batt", "Battery (V)"),
            ("curr_batt", "Battery (I)"),
            ("charging_status", "Charge")
        ]

        for key, label in keys_labels:
            frame = self.create_frame(key, label)
            frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(frame)

        self.setLayout(layout)

    def create_frame(self, key, text):
        """
        Creates a labeled frame with a value container on the right
        :param key: Dictionary key to store value label reference
        :param text: Text for the label
        :return: QFrame with label and value
        """
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {BG_OPACITY}; border-radius: {RADIUS_100}px; padding: 0px 5px;")
        layout = QHBoxLayout(frame)

        # Title label
        text_label = create_label(text, FONT_BODY, f"background-color: none; color: {TEXT_200}; padding: 0px", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(text_label)

        # Value label
        value_container = QFrame()
        value_container.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_100}px; padding: 0px;")
        value_layout = QVBoxLayout(value_container)

        value_label = create_label("0", FONT_BODY_B, f"color: {TEXT_100}; padding: 0px", alignment=Qt.AlignmentFlag.AlignCenter)
        value_layout.addWidget(value_label)
        value_container.setLayout(value_layout)
        
        layout.addWidget(value_container)
        frame.setLayout(layout)

        self.value_labels[key] = value_label
        return frame
    
    def set_charge_gif(self, gif):
        """
        Sets an animated GIF for the charging status
        :param gif: The name of the GIF file to display
        """
        gif_path = f"assets/gif/{gif}"
        movie = QMovie(gif_path)
        label = self.value_labels.get("charging_status")
        movie.setScaledSize(QSize(11, 19))
        label.setMovie(movie)

        # Create a dictionary that maps each GIF filename to a tooltip string.
        tooltips = {
            "charging.gif": "Battery Charging",
            "full_charge.gif": "Battery Full",
            "empty_charge.gif": "Battery Low",
            "error.gif": "Status Unknown",
        }
        label.setToolTip(tooltips.get(gif, "Battery status"))

        movie.start()
  
    def update_values(self, data):
        """
        Updates all displayed values
        :param data: Dictionary containing values
        """
        charge = data.get("charge", 0)
        full_charge = data.get("full_charge", 0)
        empty_charge = data.get("empty_charge", 0)

        # Charge status label
        if full_charge == 1: self.set_charge_gif("full_charge.gif")
        elif charge == 1: self.set_charge_gif("charging.gif")
        elif empty_charge == 1: self.set_charge_gif("empty_charge.gif")
        else: self.set_charge_gif("error.gif")
            
        # Other mesurement labels
        for key, label in self.value_labels.items():
            if key != "charging_status":
                value = data.get(f"{key.lower()}", "0")
                label.setText(str(value))
