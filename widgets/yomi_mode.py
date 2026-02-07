from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QLineEdit
)
from PySide6.QtCore import Qt
from src.database_helpers import get_goi_by_grades

class YomiMode(QWidget):
    def __init__(self, end_quiz):
        super().__init__()

        self.grade_conv_dict = {
            "１級": 1.0, "1.5級": 1.5, "2級": 2.0, "2.5級": 2.5, "3級": 3.0, 
            "4級": 4.0, "5級": 5.0, "6級": 6.0, "7級": 7.0, "8級": 8.0, "9級": 9.0, "10級": 10.0
        }

        self.questions_total = 0
        self.current_question = 1
        self.questions_correct = 0

        self.question_df = None
        self.question_row = None

        self.showing_answer = False

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("読みクイズ"))

        self.question_number_label = QLabel("問題 1 / 10")
        layout.addWidget(self.question_number_label)

        self.questions_correct_label = QLabel("正解: ")
        layout.addWidget(self.questions_correct_label)

        self.question_label = QLabel("")
        layout.addWidget(self.question_label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("答え給え...")
        self.input.returnPressed.connect(self.handle_input_finish)
        layout.addWidget(self.input)

        self.end_quiz_button = QPushButton()
        self.end_quiz_button.setText("諦める。。。")
        self.end_quiz_button.clicked.connect(end_quiz)
        layout.addWidget(self.end_quiz_button)

    def generate_question_set(self, questions, grades, kanji_only, jukugo_only):
        self.questions_total = questions
        print(f"Generating quesions with grades {grades}")
        gf = [self.grade_conv_dict[g] for g in grades]
        print(gf)
        df = get_goi_by_grades(gf, kanji_only=kanji_only, jukugo_only=jukugo_only)
        print(df.head())
        self.question_df = df.sample(frac=1)
        self.next_question()

    def next_question(self):
        self.question_number_label.setText(f"問題 {self.current_question} / {self.questions_total}")
        self.questions_correct_label.setText(f"正解: {self.questions_correct}")
        self.question_row = self.question_df.iloc[self.current_question-1, :]
        print(self.question_row)
        self.question_label.setText(f"{self.question_row["text"]}")

    def handle_input_finish(self):
        print(self.input.text())
        self.input.clear()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.current_question += 1
            self.next_question()