from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from constants import BG_100, BG_200, PRIMARY, PADD_100, RADIUS_100, RADIUS_200

class Sidebar(QFrame):
    def __init__(self):
        """Initializes the Sidebar widget"""
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_200}px; padding: {PADD_100}px")
        self.is_expanded = False
        self.labeled_buttons = []
        self.setup_ui()

    def setup_ui(self):
        """Sets up the sidebar layout and buttons"""
        layout = QVBoxLayout()
        nav_layout = QVBoxLayout()
        icons = ["home", "brightness", "lighting", "energy", "motor", "correction", "cansniffer"]

        # Hamburger button
        hamb_button = self.create_button("hamburger.svg", "Menu", hide_text=True)
        hamb_button.clicked.connect(self.toggle_sidebar)
        self.add_style(hamb_button)
        layout.addWidget(hamb_button)
        self.labeled_buttons.append(hamb_button)

        # Spacer between hamb button and nav buttons
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Create navigation buttons dynamically
        for icon in icons:
            button = self.create_button(f"{icon}.svg", icon.capitalize())
            self.add_style(button)
            nav_layout.addWidget(button)
            self.labeled_buttons.append(button)
        layout.addLayout(nav_layout)

        # Spacer between navigation buttons and login button
        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Login button
        login_button = self.create_button("login.svg", "Login")
        login_button.setStyleSheet(f"""
            QPushButton {{
                width: 100%;
                height: 50px;
                background-color: {BG_100};
                border-radius: {RADIUS_100}px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY};
            }}
        """)

        layout.addWidget(login_button)
        self.labeled_buttons.append(login_button)
        self.setLayout(layout)

    def create_button(self, icon_file, text=None, hide_text=False):
        """
        Create a button with an optional label

        :param icon_file: Path to the icon file
        :param text: (Optional) Label text for the button
        :param hide_text: (Optional) Boolean to hide the text label
        :return: Configured QPushButton instance
        """
        button = QPushButton()
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft if self.is_expanded else Qt.AlignmentFlag.AlignCenter)

        # Icon label
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(f"assets/icons/{icon_file}").pixmap(QSize(18, 18)))
        icon_label.setStyleSheet("padding: 0 5px; background-color: transparent;")
        button_layout.addWidget(icon_label)

        # Text label
        if text:
            text_label = QLabel(text)
            text_label.setVisible(self.is_expanded)
            text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            text_label.setStyleSheet("background-color: none; padding: 0px;" if not hide_text else "background-color: none; color: transparent;") # Align the hamb icon with the other icons
            button_layout.addWidget(text_label)
            button.text_label = text_label

        button.setLayout(button_layout)
        return button
    
    def add_style(self, button, is_login=False):
        """
        Apply common button styles, with special styles for login button

        :param button: QPushButton to style
        :param is_login: Special styles for login button
        """
        if is_login: 
            bg_color = BG_100
            bg_hover_color = PRIMARY
        else:
            bg_color = "transparent"
            bg_hover_color = BG_100

        button.setStyleSheet(f"""
            QPushButton {{
                width: 100%;
                height: 50px;
                background-color: {bg_color};
                border-radius: {RADIUS_100}px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {bg_hover_color};
            }}
        """)

    def toggle_sidebar(self):
        """Expand or collapse sidebar and show/hide button labels"""
        self.is_expanded = not self.is_expanded
        parent_layout = self.parentWidget().layout()

        # Toggle the visibility of the text button
        for button in self.labeled_buttons:
            button.text_label.setVisible(self.is_expanded)

        # Adjust sidebar width dynamically
        if isinstance(parent_layout, QGridLayout):
            parent_layout.setColumnStretch(0, 2 if self.is_expanded else 1)
            parent_layout.update()
