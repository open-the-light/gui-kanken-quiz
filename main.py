from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QStackedWidget
)
from PySide6.QtCore import QSize
from views.quiz_main import QuizMode
from views.quiz_menu import QuizMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("漢検クイズ！")
        self.setFixedSize(QSize(1400, 900))

        self.stack = QStackedWidget()

        self.quiz_menu = QuizMenu(self.start_quiz)
        self.quiz_mode = QuizMode(self.end_quiz)

        self.stack.addWidget(self.quiz_menu)
        self.stack.addWidget(self.quiz_mode)

        self.setCentralWidget(self.stack)
        self.stack.setCurrentIndex(0)

    def start_quiz(self):
        print("starting quiz!")
        self.stack.setCurrentIndex(1)

    def end_quiz(self):
        print("ending quiz")
        self.stack.setCurrentIndex(0)

app = QApplication([])
window = MainWindow()
window.show()

app.exec()
