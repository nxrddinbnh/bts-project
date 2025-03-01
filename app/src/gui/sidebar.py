from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from constants import BG_100, BG_200, PRIMARY

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {BG_200}; border-radius: 20px")
        self.is_expanded = False
        self.labeled_buttons = []
        self.setup_ui()

    def setup_ui(self):
        """Sets up the sidebar layout"""
        layout = QVBoxLayout()
        nav_layout = QVBoxLayout()
        icons = ["home", "brightness", "lighting", "energy", "motor", "correction", "cansniffer"]

        # Hamburger button
        hamb_button = self.create_button("hamburger.svg", "Menu", hide_text=True)
        hamb_button.clicked.connect(self.toggle_sidebar)
        layout.addWidget(hamb_button)
        self.add_style(hamb_button)
        self.labeled_buttons.append(hamb_button)

        # Spacer between hamb button and nav buttons
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Create buttons dynamically using the `icons` list
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
                width: 50px;
                height: 50px;
                background-color: {BG_100};
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY};
            }}
        """)

        layout.addWidget(login_button)
        self.labeled_buttons.append(login_button)
        self.setLayout(layout)

    def create_button(self, icon_file, text=None, hide_text=False):
        """Create buttons"""
        button = QPushButton()
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout = QHBoxLayout()

        icon_label = QLabel()
        icon_label.setPixmap(QIcon(f"assets/icons/{icon_file}").pixmap(QSize(18, 18)))
        icon_label.setStyleSheet("background-color: none;")
        button_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        if text:
            text_label = QLabel(text)
            text_label.setVisible(self.is_expanded)
            text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
       
            button_layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignLeft)
            button.text_label = text_label

            # To align the hamb icon with the other icons
            if hide_text : text_label.setStyleSheet("background-color: none; color: transparent")
            else : text_label.setStyleSheet("background-color: none; margin-left: 5px")

        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button.setLayout(button_layout)
        return button

    def add_style(self, button):
        """Define button stylesheet"""
        button.setStyleSheet(f"""
            QPushButton {{
                width: 50px;
                height: 50px;
                background-color: transparent;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {BG_100};
            }}
        """)

    def toggle_sidebar(self):
        """Toggles the sidebar between expanded and collapsed states"""
        self.is_expanded = not self.is_expanded
        parent_layout = self.parentWidget().layout()

        # Toggle the visibility of the text button
        for button in self.labeled_buttons:
            button.text_label.setVisible(self.is_expanded)

        # Toggle the width of the sidebar
        if isinstance(parent_layout, QGridLayout):
            parent_layout.setColumnStretch(0, 2 if self.is_expanded else 1)
            parent_layout.update()
