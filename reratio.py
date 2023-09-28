from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow

app = QApplication([])

aspect_ratio = 4/3

class Win(QMainWindow):
    def paintEvent(self, _event) -> None:
        win_size = self.size()

        if win_size.width() > win_size.height() * aspect_ratio:
            print("redraw w>h")
            height = win_size.height()
            width = int(height * aspect_ratio)
        else:
            print("redraw w<h")
            width = win_size.width()
            height = int(width * (aspect_ratio ** -1))
        x = (win_size.width() - width) // 2
        y = (win_size.height() - height) // 2

        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.rect())
        painter.setPen(QColor(255, 255, 255))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(x, y, width, height)

win = Win()
win.show()
app.exec()
