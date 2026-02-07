from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QLineEdit
)
from PySide6.QtCore import Qt
from concurrent.futures import ThreadPoolExecutor
from jaconv import hira2kata, kata2hira, alphabet2kana
from src.database_helpers import get_goi_by_grades, get_example_sentences_for_kanji

class YomiMode(QWidget):
    def __init__(self, end_quiz, client):
        super().__init__()

        self.grade_conv_dict = {
            "１級": 1.0, "1.5級": 1.5, "2級": 2.0, "2.5級": 2.5, "3級": 3.0, 
            "4級": 4.0, "5級": 5.0, "6級": 6.0, "7級": 7.0, "8級": 8.0, "9級": 9.0, "10級": 10.0
        }
        self.difficulty_conv_dict = {
            "簡単": 200, "普通": 25, "難しい": 8, "激難しい": 1
        }

        self.end_quiz = end_quiz
        self.client = client
        self.ex = ThreadPoolExecutor(2)
        self.sentence_task = None

        self.questions_total = 0
        self.current_question = 1
        self.questions_correct = 0

        self.question_df = None
        self.question_row = None

        self.showing_answer = False

        layout = QVBoxLayout(self)

        title = QLabel("読みクイズ")
        title.setProperty("class", "title")
        
        self.question_number_label = QLabel("問題 1 / 10")
        self.question_number_label.setProperty("class", "info")

        self.questions_correct_label = QLabel("正解: ")
        self.questions_correct_label.setProperty("class", "info")

        self.question_label = QLabel("")
        self.question_label.setProperty("class", "question")

        self.response_label = QLabel("")

        self.input = QLineEdit()
        self.input.setPlaceholderText("答え給え...")
        self.input.returnPressed.connect(self.handle_input_finish)

        self.answer_label = QLabel("")
        self.answer_label.setProperty("class", "info")

        self.sentences_label = QLabel("")
        self.sentences_label.setProperty("class", "info")

        self.end_quiz_button = QPushButton()
        self.end_quiz_button.setText("諦める...")
        self.end_quiz_button.clicked.connect(end_quiz)

        layout.addWidget(title, 2)
        layout.addWidget(self.question_number_label, 1)
        layout.addWidget(self.questions_correct_label, 1)
        layout.addWidget(self.question_label, 4)
        layout.addWidget(self.response_label, 1)
        layout.addWidget(self.input, 6)
        layout.addWidget(self.answer_label, 3)
        layout.addWidget(self.sentences_label, 5)
        layout.addSpacing(20)
        layout.addWidget(self.end_quiz_button, 1)
        layout.addStretch()

    def generate_question_set(self, questions, grades, kanji_only, jukugo_only, difficulty):
        self.questions_total = questions
        self.current_question = 1
        self.questions_correct = 0
        gf = [self.grade_conv_dict[g] for g in grades]
        df = get_goi_by_grades(gf, self.difficulty_conv_dict[difficulty], kanji_only=kanji_only, jukugo_only=jukugo_only)
        self.question_df = df.sample(frac=1)
        self.next_question()

    def next_question(self):
        self.answer_label.setText("")
        self.response_label.setText("")
        self.sentences_label.setText("")
        self.question_number_label.setText(f"問題 {self.current_question} / {self.questions_total}")
        self.update_correct_answer_label(0)
        self.question_row = self.question_df.iloc[self.current_question-1, :]
        text = self.question_row["text"]
        self.sentence_task = self.ex.submit(get_example_sentences_for_kanji, text, self.client)
        self.question_label.setText(f"{text}")

    def handle_input_finish(self):
        pass

    def update_correct_answer_label(self, score):
        self.questions_correct += score
        self.questions_correct_label.setText(f"正解: {self.questions_correct}")

    def show_answer(self):
        given = alphabet2kana(self.input.text()).replace(" ", "")
        self.input.clear()
        main_answer = kata2hira(self.question_row["main_reading"])
        possible_answers = set([kata2hira(x) for x in self.question_row["readings"].split(",")])
        if given in possible_answers:
            self.update_correct_answer_label(1)
            self.response_label.setText("正解！")
            self.response_label.setStyleSheet("color: green; font-size: 20px; qproperty-alignment: AlignCenter;")
        else:
            self.response_label.setText("残念...")
            self.response_label.setStyleSheet("color: red; font-size: 20px; qproperty-alignment: AlignCenter;")
        answer_text = f"正解は '{main_answer}'"
        if len(possible_answers) > 1:
            answer_text += f"\n全ての正解： {", ".join([f"'{x}'" for x in possible_answers])}"
        self.answer_label.setText(answer_text)

        try:
            sentences = self.sentence_task.result()
            text = "例文：\n\n"
            for e in sentences.itertuples():
                text += e.sentence + "\n" + e.translation + "\n\n"
            self.sentences_label.setText(text)
        except Exception as e:
            print(e)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.showing_answer:
                if self.current_question == self.questions_total:
                    self.end_quiz()
                else:
                    self.current_question += 1
                    self.showing_answer = False
                    self.next_question()
            else:
                self.show_answer()
                self.showing_answer = True
        