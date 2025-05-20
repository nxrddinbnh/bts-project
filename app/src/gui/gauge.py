from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFontMetrics
from PyQt6.QtCore import QRectF, Qt
from constants import BG_200, TEXT_100, FONT_BODY, FONT_VALUES

class Gauge(QWidget):
    def __init__(self, max_value, base_color):
        """Initializes the semicircular gauge widget"""
        super().__init__()
        self.angle = 0
        self.max_value = max_value
        self.base_color= base_color

    def set_angle(self, angle):
        """Sets the current angle and triggers a redraw"""
        try:
            angle = int(angle)
        except ValueError:
            angle = 0  
        self.angle = max(0, min(angle, self.max_value))
        self.update()

    def paintEvent(self, event):
        """Handles the painting of the semicircular gauge"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        center = rect.center()
        arc_thickness = 14
        radius = min(rect.width(), rect.height()) * 0.45

        # Bounding rectangle for the arc
        arc_rect = QRectF(
            center.x() - radius,
            center.y() - radius + 20,
            2 * radius,
            2 * radius
        )

        flat_cap = Qt.PenCapStyle.FlatCap

        # Background arc
        bg_pen = QPen(QColor(BG_200), arc_thickness)
        bg_pen.setCapStyle(flat_cap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, 180 * 16, -180 * 16)  # From 180° to 0°

        # Foreground arc
        span_angle = int((self.angle / self.max_value) * 180)
        fg_pen = QPen(QColor(self.base_color), arc_thickness)
        fg_pen.setCapStyle(flat_cap)
        painter.setPen(fg_pen)
        painter.drawArc(arc_rect, 180 * 16, -span_angle * 16)

        # Draw the angle value 
        painter.setPen(QColor(TEXT_100))
        painter.setFont(FONT_VALUES)
        metrics = QFontMetrics(FONT_VALUES)
        angle_text = f"{int(self.angle)}"
        text_width = metrics.horizontalAdvance(angle_text)
        text_height = metrics.height()

        painter.drawText(
            center.x() - text_width // 2,
            center.y() + text_height // 4 + 15,
            angle_text
        )

        # Degree symbol
        painter.setFont(FONT_BODY)
        painter.drawText(
            center.x() + text_width // 2,
            center.y() - text_height // 4 + 15,
            "°"
        )
