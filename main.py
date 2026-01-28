from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QWidget
)
from PySide6.QtCore import QSize
from widgets.yomi_main import YomiMode
from widgets.yomi_menu import YomiMenu
from widgets.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("漢検クイズ！")
        self.setFixedSize(QSize(1400, 900))

        self.main_box = QHBoxLayout()

        self.sidebar = Sidebar(self.show_yomi_menu)
        self.stack = QStackedWidget()

        self.main_box.addWidget(self.sidebar, 1)
        self.main_box.addWidget(self.stack, 5)

        self.yomi_menu = YomiMenu(self.yomi_quiz_start)

        self.yomi_mode = YomiMode(self.yomi_quiz_end)

        self.stack.addWidget(self.yomi_menu)

        self.stack.addWidget(self.yomi_mode)

        layout_widget = QWidget()
        layout_widget.setLayout(self.main_box)
        self.setCentralWidget(layout_widget)
        self.stack.setCurrentIndex(0)

    def yomi_quiz_start(self):
        print("starting quiz!")
        self.yomi_mode.generate_question_set(self.yomi_menu.selected_grades)
        self.stack.setCurrentIndex(1)

    def yomi_quiz_end(self):
        print("ending quiz")
        self.stack.setCurrentIndex(0)

    def show_yomi_menu(self):
        self.stack.setCurrentIndex(0)

app = QApplication([])
with open("style.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())
window = MainWindow()
window.show()

app.exec()
