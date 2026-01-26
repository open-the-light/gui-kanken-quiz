from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QLabel
)

class QuizMode(QWidget):
    def __init__(self, end_quiz):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ファイート！"))

        self.end_quiz_button = QPushButton()
        self.end_quiz_button.setText("スタート！")
        self.end_quiz_button.clicked.connect(end_quiz)
        layout.addWidget(self.end_quiz_button)