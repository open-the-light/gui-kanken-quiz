from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel
)
from src.database_helpers import get_goi_by_grades

class YomiMode(QWidget):
    def __init__(self, end_quiz):
        super().__init__()

        self.grade_conv_dict = {
            "１級": 1.0, "1.5級": 1.5, "2級": 2.0, "2.5級": 2.5, "3級": 3.0, 
            "4級": 4.0, "5級": 5.0, "6級": 6.0, "7級": 7.0, "8級": 8.0, "9級": 9.0, "10級": 10.0
        }

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ファイート！"))

        self.end_quiz_button = QPushButton()
        self.end_quiz_button.setText("諦める。。。")
        self.end_quiz_button.clicked.connect(end_quiz)
        layout.addWidget(self.end_quiz_button)

    def generate_question_set(self, grades):
        print(f"Generating quesions with grades {grades}")
        gf = [self.grade_conv_dict[g] for g in grades]
        print(gf)
        df = get_goi_by_grades(gf)
        print(df)