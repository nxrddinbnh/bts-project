from PyQt6.QtWidgets import QLabel, QPushButton, QSizePolicy, QSpinBox, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFontDatabase
from constants import (
    BG_100, BG_200, TEXT_100, PRIMARY, SECONDARY, 
    RADIUS_100, RADIUS_200, PADD_100, PADD_200, FONT_TITLE, FONT_BODY
)

def load_fonts():
    """Load necessary fonts for the application"""
    try:
        fonts = [
            ("assets/fonts/Lato-Black.ttf", "Lato Black"),
            ("assets/fonts/Lato-Bold.ttf", "Lato Bold"),
            ("assets/fonts/Lato-Regular.ttf", "Lato Regular"),
            ("assets/fonts/Lato-Light.ttf", "Lato Light"),
            ("assets/fonts/Lato-Thin.ttf", "Lato Thin"),
        ]

        for font_path, font_name in fonts:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id < 0: 
                print(f"Error: Could not load '{font_name}' font.")

    except Exception as e:
        print(f"An error occurred while loading fonts: {e}")

def create_label(text, font, style, alignment=Qt.AlignmentFlag.AlignCenter, icon_path=None):
    """
    Creates a QLabel
    :param text: Text to be displayed in the label
    :param font: Font style to be applied to the label
    :param style: CSS style string to format the label
    :param alignment: Text alignement (optional)
    :param icon_path: Icon file path (optional)
    :return: A QLabel object with the specified properties
    """
    label = QLabel(text)
    label.setFont(font)
    label.setStyleSheet(style)
    label.setAlignment(alignment)
    if icon_path:
        label.setPixmap(QPixmap(icon_path).scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
    return label

def title_label(text):
    """
    Standardized title label for modules
    :param text: The title text to display
    :return: QLabel with title style, left-aligned
    """
    return create_label(text.upper(), FONT_TITLE, f"padding-left: 0; color: {TEXT_100};", Qt.AlignmentFlag.AlignLeft)

def create_button(text, font, style, action=None):
    """
    QPushButton with the given properties and click behavior
    :param text: The button label text
    :param font: Font to apply to the button text
    :param style: CSS-style string to define the button's appearance
    :param action: Function to connect to the button's click event
    :return: Configured QPushButton instance
    """
    button = QPushButton(text)
    button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setFont(font)
    button.setStyleSheet(style)
    if action is not None:
        button.clicked.connect(action)
    return button

def create_input(min_range, max_range, value):
    """
    Returns a styled QSpinBox (numeric input)
    :param min_range: Minimum value allowed
    :param max_range: Maximum value allowed
    :param value: Initial/default value
    :return: Configured QSpinBox instance
    """
    style = f"""
        QSpinBox {{
            height: 32px;
            background-color: {BG_100};
            border-radius: {RADIUS_100}px;
            padding: {PADD_100}px;
            color: {TEXT_100};
        }}
        QSpinBox::up-button, QSpinBox::down-button {{
            background-color: transparent;
            border: none;
            width: 0px;
            height: 0px;
        }}
        QSpinBox::focus {{
            border: 1px solid {PRIMARY};
        }}
    """

    input = QSpinBox()
    input.setRange(min_range, max_range)
    input.setValue(value)
    input.setStyleSheet(style)
    return input

def create_combo(items, current):
    """
    Returns a styled QComboBox
    :param items: List of items to populate the combo box
    :param current: Currently selected item
    :return: Configured QComboBox instance
    """
    style = f"""
        QComboBox {{
            height: 32px;
            background-color: {BG_100};
            border-radius: {RADIUS_100}px;
            padding: {PADD_100}px;
            color: {TEXT_100};
            margin: 2px 0;
        }}
        QComboBox::drop-down {{
            border: 0px;
        }}
        QComboBox::down-arrow {{
            image: url(assets/icons/comboDown.svg);
            height: 20px;
            width: 20px;
            margin-right: 20px;
        }}
        QComboBox::on {{
            border: 1px solid {PRIMARY};
        }}
        QComboBox QListView {{
            padding: {PADD_100}px;
            background-color: {BG_100};
            outline: none;
            border-radius: 0;
        }}
        QComboBox QListView:item {{
            padding: {PADD_200}px;
            color: {TEXT_100};
        }}
        QComboBox QListView:item:selected {{
            background-color: {BG_200};
            color: {SECONDARY};
            padding: {PADD_100}px;
        }}
    """

    combo = QComboBox()
    combo.addItems([str(item) for item in items])
    combo.setCurrentText(current)
    combo.setCursor(Qt.CursorShape.PointingHandCursor)
    combo.setFont(FONT_BODY)
    combo.setStyleSheet(style)
    return combo

def set_module_style(module):
    """
    Apply default styling for modules
    :param module: The QWidget (QFrame) to apply the style to
    """
    module.setStyleSheet(f"background-color: {BG_200}; border-radius: {RADIUS_200}px; padding: {PADD_200}px;")
