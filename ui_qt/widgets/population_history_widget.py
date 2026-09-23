"""PopulationHistoryWidget — courbe legere de l'historique de population."""
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


class PopulationHistoryWidget(QWidget):
    """Trace la population en fonction du temps (Lot E.3)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.values = []
        self.setMinimumHeight(130)

    def set_values(self, values):
        self.values = [int(value) for value in (values or [])]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(25, 29, 42))

        if len(self.values) < 2:
            painter.setPen(QColor(160, 170, 190))
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter,
                "Historique indisponible")
            painter.end()
            return

        rect = self.rect().adjusted(12, 12, -12, -12)
        low = min(self.values)
        high = max(self.values)
        span = max(1, high - low)

        # Axe bas + etiquette min/max
        painter.setPen(QPen(QColor(70, 80, 100), 1))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        painter.setPen(QColor(140, 150, 170))
        painter.drawText(rect.adjusted(0, 0, 0, 2),
                         Qt.AlignmentFlag.AlignBottom
                         | Qt.AlignmentFlag.AlignLeft,
                         str(low))
        painter.drawText(rect.adjusted(0, 0, 0, 2),
                         Qt.AlignmentFlag.AlignBottom
                         | Qt.AlignmentFlag.AlignRight,
                         str(high))

        painter.setPen(QPen(QColor(88, 180, 236), 2))
        previous = None
        for index, value in enumerate(self.values):
            x = rect.left() + rect.width() * index / max(1, len(self.values) - 1)
            y = rect.bottom() - rect.height() * (value - low) / span
            point = QPointF(x, y)
            if previous is not None:
                painter.drawLine(previous, point)
            previous = point

        painter.end()
