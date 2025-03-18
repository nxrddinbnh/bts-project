from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QMenu, QVBoxLayout, QSizePolicy, QSlider, QGridLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QAction, QIcon, QPixmap
from constants import BG_100, BG_200, RADIUS_100, RADIUS_200, PADD_100, PADD_200, FONT_TITLE, FONT_BODY, FONT_VALUES, TEXT_200, PRIMARY, ACCENT
from gui.timer_selector import TimerSelectorDialog

class Lighting(QFrame):
    def __init__(self):
        """Initializes the Lighting widget"""
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_200}px; padding: {PADD_200}px;")
        self.timer_running = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the UI layout for the lighting module"""
        main_layout = QVBoxLayout(self)
        layout  = QGridLayout()

        # Title label
        title_label = self.create_label("lighting", FONT_TITLE, "padding-left: 0; color: white;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(title_label)

        # Effects Frame
        self.effects_frame = self.create_frame("static", "effects", "effects_frame")
        self.effects_frame.mousePressEvent = self.show_effects_menu
        layout.addWidget(self.effects_frame, 0, 0 , 1, 2)

        # Timer Frame
        self.timer_frame = self.create_frame("00:00", "timer", "timer_frame", is_timer=True)
        self.timer_frame.mousePressEvent = self.show_timer_selector
        layout.addWidget(self.timer_frame, 1, 0 , 1, 2)

        # Slider Frame
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.setStyleSheet(self.set_slider_style())
        layout.addWidget(self.slider, 0, 2 , 2, 1)

        # Slider icon label
        icon_slider = self.create_label("", FONT_BODY, "color: white; padding: 0; background: none;", "assets/icons/sun.svg")
        layout.addWidget(icon_slider, 1, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.create_buttons(layout)

        main_layout.addLayout(layout)
        self.setLayout(main_layout)

    def create_frame(self, value, text, frame_id, is_timer=False):
        """
        Creates a frame with a centered label at the bottom and centered value at the middle

        :param value: Text to be displayed inside the frame
        :param text: Text for the description label at the bottom
        :param frame_id: Unique identifier for each frame
        :return: A QFrame widget with a label at the bottom
        """
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {BG_100}; border-radius: {RADIUS_100}px;")
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        # Value label
        value_label = self.create_label(value, FONT_VALUES, "color: white; padding: 0px")
        setattr(self, f"{frame_id}_label", value_label)
        layout.addWidget(value_label)

        # Button play/stop for timer frame
        if is_timer:
            self.play_stop_button = QPushButton()
            self.play_stop_button.setIcon(QIcon("assets/icons/play.svg"))
            self.play_stop_button.setStyleSheet("background: none; padding: 0; border: none;")
            self.play_stop_button.setEnabled(False)
            self.play_stop_button.clicked.connect(self.toggle_timer)

            button_layout = QVBoxLayout()  
            button_layout.addWidget(self.play_stop_button, alignment=Qt.AlignmentFlag.AlignHCenter)
            layout.addLayout(button_layout)

        # Description label
        description_label = self.create_label(text, FONT_BODY, f"color: {TEXT_200}; padding: 0px")

        layout.addStretch()
        layout.addWidget(description_label)
        frame.setLayout(layout)
        return frame
    
    def create_label(self, text, font, style, icon_path=None):
        """
        Creates a QLabel with specified text, font, and style

        :param text: Text to be displayed in the label
        :param font: Font style to be applied to the label
        :param style: CSS style string to format the label
        :param icon_path: Icon file path (optional)
        :return: A QLabel object with the specified properties
        """
        label = QLabel(text.upper())
        label.setFont(font)
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if icon_path:
            icon = QPixmap(icon_path).scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(icon)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return label

    def update_label(self, frame_id, value):
        """
        Updates the label inside the frame
        
        :param frame_id: ID of the frame containing the label
        :param value: New value for the label
        """
        label = getattr(self, frame_id, None)
        if label: label.setText(value.upper())

    def show_effects_menu(self, event):
        """
        Displays a context menu with lighting effects when the user clicks on the frame
        
        :param event: Mouse event that triggers the menu
        """
        effects = ["Static", "Breath", "Wink"]
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {BG_200};
                border-radius: {RADIUS_100}px;
                padding: {PADD_100}px;
            }}
            QMenu::item {{
                padding: 20px 40px;
                color: white;
            }}
            QMenu::item:selected {{
                background-color: {BG_100};
                border-radius: {RADIUS_100}px;
            }}
        """)

        # Create actions for each effect
        for effect in effects:
            action = QAction(effect, self)
            action.triggered.connect(lambda checked, e=effect: self.update_label("effects_frame_label", e))
            menu.addAction(action)

        # Show the menu at the mouse position
        menu.exec(event.globalPosition().toPoint())

    def toggle_timer(self):
        """Starts or stops the timer countdown"""
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False
            self.play_stop_button.setIcon(QIcon("assets/icons/play.svg"))
        else:
            self.timer.start(1000)
            self.timer_running = True
            self.play_stop_button.setIcon(QIcon("assets/icons/stop.svg"))

    def update_timer(self):
        """Updates the timer every second and stops it when 00:00 is reached"""
        if self.remaining_time == QTime(0, 0):
            self.timer.stop()
            self.timer_running = False
            self.play_stop_button.setIcon(QIcon("assets/icons/play.svg"))
            self.play_stop_button.setEnabled(False)
        else:
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.update_label("timer_frame_label", self.remaining_time.toString("mm:ss"))

    def show_timer_selector(self, event):
        """
        Displays a custom dialog with a sliding timer selector
        
        :param event: Mouse event that triggers the dialog
        """
        current_time = getattr(self, "timer_frame_label", None).text() if hasattr(self, "timer_frame_label") else "00:00"
        minutes, seconds = current_time.split(":")
        timer_dialog = TimerSelectorDialog(self, initial_minute=minutes, initial_second=seconds)

        if timer_dialog.exec():
            self.update_label("timer_frame_label", timer_dialog.get_selected_time())
            self.remaining_time = QTime.fromString(timer_dialog.get_selected_time(), "mm:ss")

            # Enables or disables the button according to the new time
            self.play_stop_button.setEnabled(self.remaining_time > QTime(0, 0))


    def set_slider_style(self):
        """Apply style to the slider"""
        return f"""
            QSlider {{
                width: 70px;
                padding: 0;
                border-radius: {RADIUS_100}px;
            }}
            QSlider::groove:vertical {{
                background: {PRIMARY};
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
            (0, 4, "B1"),
            (0, 5, "B2"),
            (1, 4, "B3"),
            (1, 5, "B4")
        ]
        self.button_states = {
            "B1": False,
            "B2": False,
            "B3": False,
            "B4": False
        }

        for row, col, btn_name in button_positions:
            button = QPushButton(btn_name)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFont(FONT_VALUES)
            button.setStyleSheet(f"""
                background-color: {BG_100}; 
                color: white; 
                border-radius: {RADIUS_100}px;
            """)
            button.clicked.connect(lambda _, num=btn_name: self.toggle_button(num))
            self.buttons[btn_name] = button
            layout.addWidget(button, row, col, 1, 1)
    
    def toggle_button(self, button_name):
        """
        Toggles the state of the button between on and off
        
        :param button_name: The name of the button clicked
        """
        self.button_states[button_name] = not self.button_states[button_name]

        if self.button_states[button_name]:
            self.buttons[button_name].setStyleSheet(f"""
                background-color: {PRIMARY}; 
                color: white; 
                border-radius: {RADIUS_100}px;
            """)
        else:
            self.buttons[button_name].setStyleSheet(f"""
                background-color: {BG_100}; 
                color: white; 
                border-radius: {RADIUS_100}px;
            """)