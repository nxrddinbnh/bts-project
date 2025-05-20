from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy, QGridLayout, QSlider
from PyQt6.QtGui import QIcon, QPixmap, QTransform
from PyQt6.QtCore import Qt
from gui.gauge import Gauge
from gui.toast_notif import ToastNotif
from base import set_module_style, title_label, create_label, create_button
from constants import BG_OPACITY, RADIUS_100, SECONDARY, ACCENT, FONT_VALUES, PRIMARY, FONT_BODY, FONT_BODY_B, TEXT_100, TEXT_200, PADD_100, BG_100, BG_200, CMD_MOTOR_ELEV, CMD_MOTOR_AZIM

class Motor(QFrame):
    def __init__(self, serial_com, main_window):
        """Initializes the Motor widget"""
        super().__init__()
        set_module_style(self)
        self.serial_com = serial_com
        self.main_window = main_window
        self.toast_notif = ToastNotif(main_window)
        self.value_labels = {}
        self.time_value = 1
        self.is_moving = False
        self.setup_ui()

    def setup_ui(self):
        """Setup UI layout for the motor module"""
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title_label("motor"))  # Title label

        content_layout = QHBoxLayout()
        axes_layout = QVBoxLayout()
        ctrl_layout = QVBoxLayout()
        style = f"background-color: {BG_100}; color: {TEXT_100}; border-radius: {RADIUS_100}px;"

        # Elevation & Azimuth
        axes_layout.addLayout(self.create_axis_layout("elevation"))
        axes_layout.addLayout(self.create_axis_layout("azimuth"))

        # Controller section: D-Pad, button, and slider
        ctrl_down = QVBoxLayout()
        ctrl_down.addWidget(create_button("Parking", FONT_BODY, style, lambda: self.send_command(CMD_MOTOR_ELEV, 0, self.time_value, True)))
        ctrl_down.addWidget(self.create_time_slider())
        ctrl_layout.addWidget(self.create_dpad())
        ctrl_layout.addLayout(ctrl_down)

        content_layout.addLayout(axes_layout, stretch=2)
        content_layout.addLayout(ctrl_layout, stretch=1)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def create_axis_layout(self, label):
        """
        Creates a horizontal layout for a motor axis
        Returns: QHBoxLayout Layout with angle and intensity frames
        """
        if label == "azimuth": key = "az"
        elif label == "elevation": key = "el"
        in_key = f"intensity_{key}"

        layout = QHBoxLayout()
        layout.addWidget(self.create_frame(key, label, is_gauge=True), stretch=2)
        layout.addWidget(self.create_frame(in_key, "intensity"), stretch=1)
        return layout

    def create_frame(self, key, text, is_gauge=False):
        """
        Creates a frame with a gauge with angle value, or intensity value above and the label below
        :param text: text for the title label
        :return: QFrame configurated
        """
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {BG_OPACITY}; border-radius: {RADIUS_100}px;")
        layout = QVBoxLayout(frame)

        if is_gauge:
            max_value = 360 if text.upper() == "AZIMUTH" else 90
            color = SECONDARY if text.upper() == "AZIMUTH" else ACCENT
            gauge = Gauge(max_value, color)
            gauge.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(gauge)
            self.value_labels[key] = gauge
        else:
            value_label = create_label("0", FONT_VALUES, f"background-color: transparent; color: {TEXT_100}; padding: {PADD_100}px")
            self.value_labels[key] = value_label

            layout.addStretch(1)
            layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignHCenter)
            layout.addStretch(1)

        # Title label
        text_label = create_label(text.upper(), FONT_BODY, f"background-color: transparent; color: {TEXT_200}; padding: 0px")
        layout.addWidget(text_label)

        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return frame

    def create_dpad(self):
        """
        Creates a D-Pad with directional buttons (up, down, left, right)
        :return: QFrame with the buttons
        """
        frame = QFrame()
        frame.setStyleSheet(f"padding: 0;")
        layout = QGridLayout(frame)
        style = f"background-color: {BG_100}; color: {TEXT_100}; border-radius: {RADIUS_100}px;"
        base_icon = QPixmap("assets/icons/comboDown.svg")

        directions = {
            (0, 1): ("up", base_icon.transformed(QTransform().rotate(180))),
            (1, 0): ("left", base_icon.transformed(QTransform().rotate(90))),
            (1, 2): ("right", base_icon.transformed(QTransform().rotate(-90))),
            (2, 1): ("down", base_icon),
        }

        for (row, col), (dir_name, icon) in directions.items():
            def make_callback(d=dir_name):
                return lambda: self.move_btn(d)

            btn = create_button("", FONT_BODY, style, make_callback())
            btn.setIcon(QIcon(icon))
            btn.setFixedSize(48, 48)
            layout.addWidget(btn, row, col)
        return frame

    def create_time_slider(self):
        """
        Creates a horizontal slider for selecting time in seconds
        :return: QFrame containing the time slider and label
        """
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {BG_OPACITY}; border-radius: {RADIUS_100}px; padding: 0px 5px;")

        grid = QGridLayout(frame)
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 1)

        # Time label
        label = create_label("Time (s)", FONT_BODY, f"background-color: none; color: {TEXT_200}; padding: 0px", alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        grid.addWidget(label, 0, 0)

        # Value container
        value_container = QFrame()
        value_container.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_100}px; padding: 0px;")
        value_layout = QVBoxLayout(value_container)
        self.time_value_label = create_label("5", FONT_BODY_B, f"color: {TEXT_100}; padding: 0px", alignment=Qt.AlignmentFlag.AlignCenter)
        value_layout.addWidget(self.time_value_label)
        value_container.setLayout(value_layout)
        grid.addWidget(value_container, 0, 1, 2, 1)

        # Slider
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setCursor(Qt.CursorShape.PointingHandCursor)
        slider.setMinimum(0)
        slider.setMaximum(10)
        slider.setValue(5)
        slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        grid.addWidget(slider, 1, 0)  

        slider.setStyleSheet(f"""
            QSlider {{ background: transparent; }}
            QSlider::groove:horizontal {{
                background: {PRIMARY};
                border-radius: {RADIUS_100}px;
                height: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {TEXT_100};
                width: {RADIUS_100}px;
                margin: -5px -1px;
                border-radius: 5px;
                border: 1px solid {TEXT_100};
            }}
            QSlider::add-page:horizontal {{ background: {BG_100}; }}
            QSlider::sub-page:horizontal {{ background: {PRIMARY}; }}
        """)
            
        slider.valueChanged.connect(self.update_time_value)
        return frame
    
    def update_time_value(self, val):
        """
        Updates internal time value and label when slider moves
        :param val: value of time (s)
        """
        self.time_value = val
        self.time_value_label.setText(str(val))

    def move_btn(self, direction):
        """
        Handles directional button commands
        :param direction: up, down, left or right
        """
        # Check if it is already in motion and avoid sending new command if so
        if self.is_moving:
            self.toast_notif.show_message("motor_move")
            return

        if direction in ["up", "down"]:
            cmd = CMD_MOTOR_ELEV
            current_angle = self.value_labels["el"].angle
            if direction == "up" and current_angle >= 90:
                self.toast_notif.show_message("max_el")
                return
            if direction == "down" and current_angle <= 0:
                self.toast_notif.show_message("min_el")
                return
        else:
            cmd = CMD_MOTOR_AZIM
            
        if direction in ["up", "right"]: dir_val = 1
        else: dir_val = 2

        self.send_command(cmd, dir_val, self.time_value, False)

    def send_command(self, cmd, direction, duration, park):
        """Send the command to the panel"""
        self.serial_com.send_command(cmd, (direction, duration, int(park)))
    
    def update_values(self, data):
        """
        Updates values
        :param data: Parsed data
        """
        axis_map = {
            "el": ("angle_el", "curr_m1"),
            "az": ("angle_az", "curr_m2"),
        }
            
        for key, (angle_key, intensity_key) in axis_map.items():
            # Update gauge if exists
            if key in self.value_labels:
                self.value_labels[key].set_angle(data.get(angle_key, 0))

            # Update intensity label if exists
            intensity_label_key = f"intensity_{key}"
            if intensity_label_key in self.value_labels:
                overload = data.get(intensity_key, 0)
                self.value_labels[intensity_label_key].setText(str(overload))
                
        # Update self.is_moving
        self.is_moving = bool(data.get("moving", 0))
            