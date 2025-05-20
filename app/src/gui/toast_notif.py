from PyQt6.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QColor
from constants import BG_100, TEXT_100, PADD_200, RADIUS_200, FONT_BODY

class ToastNotif(QLabel):
    # Predefined toast messages
    _messages = {
        "max_el": "Elevation is already at maximum (90°)",
        "min_el": "Elevation is already at minimum (0°)",
        "mode_locked": "Cannot change mode during motor operation",
        "motor_move": "Motor is already moving. Please wait..."
    }

    def __init__(self, main_window):
        """
        Initialize styled toast label
        :param main_window: Parent window where toast should appear
        """
        super().__init__(main_window)
        self.main_window = main_window
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)

        self._current_msg_id = None
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)
        self.hide()

    def show_message(self, msg_id, duration=2500):
        """
        Display toast on top of the main window
        :param msg_id: Message key to display (must exist in _messages)
        :param duration: Time in ms before toast disappears
        """
        if msg_id not in self._messages: return
        if self.isVisible() and msg_id == self._current_msg_id: return
        
        self._current_msg_id = msg_id
        text = self._messages[msg_id]
        self.setText(text)

        font_metrics = self.fontMetrics()
        width = font_metrics.horizontalAdvance(text) + 20 
        height = font_metrics.height() + 20
        self.setMinimumSize(width, height)
        self.adjustSize()

        # Force minimum size if wrong
        if self.width() == 0 or self.height() == 0:
            self.resize(300, 50)

        self.setStyleSheet(f"""
            background-color: {BG_100};
            color: {TEXT_100};
            padding: {PADD_200}px;
            border-radius: {RADIUS_200}px;
        """)
        self.setFont(FONT_BODY)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)

        # Center toast horizontally, top offset vertically
        toast_width, toast_height = self.width(), self.height()
        main_width = self.main_window.width()
        x = (main_width - toast_width) // 2
        y = 25

        # Set position and animation
        self.setGeometry(x, y - 20, toast_width, toast_height)
        self.animation.setStartValue(QRect(x, y - 20, toast_width, toast_height))
        self.animation.setEndValue(QRect(x, y, toast_width, toast_height))
        self.animation.start()

        self.raise_()
        super().show()
        self._timer.stop()
        self._timer.start(duration)
