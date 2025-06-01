from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon
from base import set_module_style
from constants import BG_100, PRIMARY, TEXT_100, FONT_BODY, RADIUS_100

class Sidebar(QFrame):
    navigate = pyqtSignal(str)

    def __init__(self):
        """Initializes the Sidebar widget"""
        super().__init__()
        self.is_expanded = False
        self.labeled_buttons = []
        set_module_style(self)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the sidebar layout and buttons"""
        layout = QVBoxLayout()
        nav_layout = QVBoxLayout()
        icons = ["home", "search"]

        # Hamburger button
        hamb_button = self.create_button("hamburger.svg", "Menu", hide_text=True)
        hamb_button.clicked.connect(self.toggle_sidebar)
        layout.addWidget(hamb_button)
        self.labeled_buttons.append(hamb_button)

        # Spacer between hamb button and nav buttons
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Navigation buttons
        for icon in icons:
            button = self.create_button(f"{icon}.svg", icon.capitalize())
            button.clicked.connect(lambda checked, name=icon: self.navigate.emit(name))
            nav_layout.addWidget(button)
            self.labeled_buttons.append(button)
        layout.addLayout(nav_layout)

        # Spacer between navigation buttons and login button
        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Login button
        login_button = self.create_button("login.svg", "Login", is_login=True)
        layout.addWidget(login_button)
        self.labeled_buttons.append(login_button)

        self.setLayout(layout)

    def create_button(self, icon_file, text=None, hide_text=False, is_login=False):
        """
        Button with an optional label
        :param icon_file: Path to the icon file
        :param text: Label text for the button (Optional)
        :param hide_text: Boolean to hide the text label (Optional)
        :param is_login: Special styles for login button (Optional)
        :return: Configured QPushButton instance
        """
        button = QPushButton()
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(self.set_button_style(is_login))
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft if self.is_expanded else Qt.AlignmentFlag.AlignCenter)

        # Icon label
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(f"assets/icons/{icon_file}").pixmap(QSize(18, 18)))
        icon_label.setStyleSheet(f"padding: 0 5px; background-color: transparent; color: {TEXT_100};")
        button_layout.addWidget(icon_label)

        # Text label
        if text:
            text_label = QLabel(text)
            text_label.setVisible(self.is_expanded)
            text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            text_label.setStyleSheet(f"background-color: none; padding: 0px; color: {TEXT_100};" 
                                     if not hide_text else "background-color: none; color: transparent;") # Align the hamb icon with the other icons
            text_label.setFont(FONT_BODY)
            button_layout.addWidget(text_label)
            button.text_label = text_label

        button.setLayout(button_layout)
        return button
    
    def set_button_style(self, is_login=False):
        """
        Apply common button styles, with special styles for login button
        :param is_login: Special styles for login button (Optional)
        :return: Stylesheet for the button 
        """
        if is_login: 
            bg_color = BG_100
            bg_hover_color = PRIMARY
        else:
            bg_color = "transparent"
            bg_hover_color = BG_100

        return f"""
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
        """

    def toggle_sidebar(self):
        """Expand or collapse sidebar and show/hide button labels"""
        self.is_expanded = not self.is_expanded

        # Toggle the visibility of the text button
        for button in self.labeled_buttons:
            button.text_label.setVisible(self.is_expanded)
