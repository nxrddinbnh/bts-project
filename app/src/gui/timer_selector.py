from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget
from PyQt6.QtCore import Qt
from constants import BG_100, BG_200, RADIUS_100, RADIUS_200, PADD_100, PADD_200, FONT_VALUES, PRIMARY, ACCENT, SECONDARY

class TimerSelectorDialog(QDialog):
    def __init__(self, parent=None, initial_minute="00", initial_second="00"):
        """
        Initializes the Timer Selector dialog with a sliding selector
        
        :param parent: Parent widget of the dialog
        :param initial_minute: Initial selected minute (default "00")
        :param initial_second: Initial selected second (default "00")
        """
        super().__init__(parent)
        self.setWindowTitle("Select Timer")
        self.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_200}px; padding: {PADD_200}px;")
        self.setFixedSize(250, 200)
        self.selected_minute = initial_minute
        self.selected_second = initial_second
        self.setup_ui()

    def setup_ui(self):
        """Sets up the UI layout for the timer selector"""
        layout = QVBoxLayout(self)
        picker_layout = QHBoxLayout()

        # Minutes List
        self.minutes_list = self.create_list_widget(range(60), self.selected_minute, "minute")
        picker_layout.addWidget(self.minutes_list)
        
        # Separator
        separator_label = QLabel(":")
        separator_label.setFont(FONT_VALUES)
        separator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        separator_label.setStyleSheet("color: white;")
        picker_layout.addWidget(separator_label)

        # Seconds List
        self.seconds_list = self.create_list_widget(range(60), self.selected_second, "second")
        picker_layout.addWidget(self.seconds_list)

        layout.addLayout(picker_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.create_button("Accept", PRIMARY, self.accept))
        buttons_layout.addWidget(self.create_button("Cancel", ACCENT, self.reject))

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def create_list_widget(self, range_values, selected_value, time_type):
        """
        Creates a QListWidget with specified range values and selected value

        :param range_values: Values to be displayed (0-59)
        :param selected_value: Selected value for the list
        :param time_type: Either 'minute' or 'second' to specify which time we're updating
        :return: A QListWidget instance
        """
        list_widget = QListWidget(self)
        list_widget.addItems([f"{i:02d}" for i in range_values])
        list_widget.setCurrentRow(int(selected_value))
        list_widget.setStyleSheet(self.get_list_style())
        list_widget.itemClicked.connect(lambda item: self.update_time(item, time_type))
        list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        list_widget.setFrameShape(QFrame.Shape.NoFrame)
        list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        return list_widget

    def create_button(self, text, color, action):
        """
        Creates a QPushButton with specified text, color, and action

        :param text: Button text
        :param color: Background color of the button
        :param action: Function to be executed when the button is clicked
        :return: A QPushButton instance
        """
        button = QPushButton(text, self)
        button.setStyleSheet(self.get_button_style(color))
        button.clicked.connect(action)
        return button

    def get_list_style(self):
        """
        Returns the stylesheet for the QListWidget

        :return: A string containing the stylesheet
        """
        return f"""
        QListWidget {{
            border-radius: {RADIUS_100}px;
            border: none;
            background-color: transparent;
            color: white;
            font-size: 18px;
            padding: {PADD_100}px;
        }}
        QListWidget::item {{
            height: 30px;
        }}
        QListWidget::item:selected {{
            color: {SECONDARY};
            background-color: {BG_100};
            border-radius: 5px;
        }}
        """

    def get_button_style(self, color):
        """
        Returns the stylesheet for the QPushButton

        :param color: Hover background color of the button
        :return: A string containing the stylesheet
        """
        return f"""
        QPushButton {{
            width: 100%;
            height: 40px;
            color: white;
            background-color: {BG_100};
            border-radius: {RADIUS_100}px;
            padding: 0px;
        }}
        QPushButton:hover {{
            background-color: {color};
        }}
        """

    def update_time(self, item, time_type):
        """
        Updates the selected time value (minute or second)
        
        :param item: The clicked item in the list
        :param time_type: 'minute' or 'second' to specify which time to update
        """
        if time_type == 'minute': self.selected_minute = item.text()
        elif time_type == 'second': self.selected_second = item.text()

    def get_selected_time(self):
        """Returns the selected time"""
        return f"{self.selected_minute}:{self.selected_second}"
