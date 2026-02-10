import os
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
from openai import OpenAI
from dotenv import load_dotenv
from widgets.yomi_mode import YomiMode
from widgets.yomi_menu import YomiMenu
from widgets.kaki_mode import KakiMode
from widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("漢検クイズ！")
        self.setFixedSize(QSize(1700, 950))

        self.client = self.generate_openai_client()

        self.main_box = QHBoxLayout()

        self.sidebar = Sidebar(
            self.show_yomi_menu,
            self.show_kaki_menu
        )
        self.stack = QStackedWidget()

        self.main_box.addWidget(self.sidebar, 1)
        self.main_box.addWidget(self.stack, 5)

        self.yomi_menu = YomiMenu(self.yomi_quiz_start)
        self.yomi_mode = YomiMode(self.yomi_quiz_end, self.client)

        self.kaki_mode = KakiMode(self.client)

        self.stack.addWidget(self.yomi_menu)
        self.stack.addWidget(self.yomi_mode)
        self.stack.addWidget(self.kaki_mode)

        layout_widget = QWidget()
        layout_widget.setLayout(self.main_box)
        self.setCentralWidget(layout_widget)
        self.stack.setCurrentIndex(0)

    def generate_openai_client(self) -> OpenAI:
        load_dotenv()
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        return client

    def yomi_quiz_start(self):
        print("starting quiz!")
        self.yomi_mode.generate_question_set(
            self.yomi_menu.questions,
            self.yomi_menu.selected_grades,
            self.yomi_menu.kanji_only,
            self.yomi_menu.jukugo_only,
            self.yomi_menu.selected_difficulty
        )
        self.stack.setCurrentIndex(1)

    def yomi_quiz_end(self):
        print("ending quiz")
        self.yomi_menu.reset_menu_screen()
        self.stack.setCurrentIndex(0)

    def show_yomi_menu(self):
        self.stack.setCurrentIndex(0)
        
    def show_kaki_menu(self):
        self.stack.setCurrentIndex(2)


app = QApplication([])
with open("style.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())
window = MainWindow()
window.show()

app.exec()
