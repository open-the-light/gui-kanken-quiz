from __future__ import annotations

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QPixmap, QImage
from PySide6.QtCore import Qt, QPoint, QSize


class DrawingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFixedSize(QSize(384, 384))

        self.im_size = QSize(384, 384)
        self.image: QImage | None = None
        self._last_point: QPoint | None = None

        self._pen = QPen(Qt.black, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

    # Helps layouts choose a reasonable default size
    def sizeHint(self) -> QSize:
        return QSize(600, 300)

    def minimumSizeHint(self) -> QSize:
        return QSize(200, 120)

    def _ensure_canvas(self):
        """Create the backing pixmap the first time we have a real size."""
        if self.image is None and self.width() > 0 and self.height() > 0:
            self.image = QImage(self.im_size, QImage.Format_ARGB32)
            self.image.fill(Qt.white)

    def paintEvent(self, event):
        self._ensure_canvas()

        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)  # in case canvas is not ready yet
        if self.image is not None:
            painter.drawImage(0, 0, self.image)

    def resizeEvent(self, event):
        # Preserve existing drawing when the widget is resized.
        if self.image is None:
            self._ensure_canvas()
            return

        if event.size().width() <= 0 or event.size().height() <= 0:
            return

        new_canvas = QImage(
            self.im_size,
            QImage.Format_ARGB32
        )
        new_canvas.fill(Qt.white)

        painter = QPainter(new_canvas)
        painter.drawImage(0, 0, self.image)

        self.image = new_canvas

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._ensure_canvas()
            self._last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._last_point is not None and self.image is not None:
            painter = QPainter(self.image)
            painter.setPen(self._pen)

            current = event.position().toPoint()
            painter.drawLine(self._last_point, current)

            self._last_point = current
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._last_point = None

    # Convenience API your larger app can call:
    def clear(self):
        self._ensure_canvas()
        if self.image is not None:
            self.image.fill(Qt.white)
            self.update()

    def set_pen_width(self, width: int):
        self._pen.setWidth(max(1, width))
