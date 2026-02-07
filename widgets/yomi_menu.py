from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QSpinBox
)
from PySide6.QtCore import Qt

class YomiMenu(QWidget):
    def __init__(self, start_quiz):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("クイズの設定を選べよ"))

        self.questions = 10
        self.selected_grades = None
        self.kanji_only = True
        self.jukugo_only = False
        self.selected_difficulty = None

        self.question_amount = QSpinBox()
        self.question_amount.setMinimum(1)
        self.question_amount.setValue(self.questions)
        self.question_amount.valueChanged.connect(self.question_amount_changed)
        layout.addWidget(self.question_amount)

        self.grade_label = QLabel("少なくとも１つの級を選べ")
        self.gradePicker = QListWidget()
        self.gradePicker.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.gradePicker.addItems(["１級", "1.5級", "2級", "2.5級", "3級", "4級", "5級", "6級", "7級", "8級", "9級", "10級"])
        self.gradePicker.selectionModel().selectionChanged.connect(self.grade_changed)
        layout.addWidget(self.grade_label)
        layout.addWidget(self.gradePicker)

        self.difficulty_label = QLabel("難易度を選べ")
        self.difficulty_picker = QListWidget()
        self.difficulty_picker.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.difficulty_picker.addItems(["簡単", "普通", "難しい", "激難しい"])
        self.difficulty_picker.selectionModel().selectionChanged.connect(self.difficulty_changed)
        layout.addWidget(self.difficulty_label)
        layout.addWidget(self.difficulty_picker)

        self.kanji_only_box = QCheckBox("Only words comprised entirely of kanji will appear")
        self.kanji_only_box.setCheckState(Qt.CheckState.Checked)
        self.kanji_only_box.stateChanged.connect(self.kanji_only_changed)
        layout.addWidget(self.kanji_only_box)

        self.jukugo_only_box = QCheckBox("Only words comprised of exactly two kanji will appear")
        self.jukugo_only_box.setCheckState(Qt.CheckState.Unchecked)
        self.jukugo_only_box.stateChanged.connect(self.jukugo_only_changed)
        layout.addWidget(self.jukugo_only_box)

        self.start_quiz_button = QPushButton()
        self.start_quiz_button.setText("スタート！")
        self.start_quiz_button.clicked.connect(start_quiz)
        layout.addWidget(self.start_quiz_button)

    def question_amount_changed(self, n):
        print(n)
        self.questions = n

    def grade_changed(self):
        grades = [i.text() for i in self.gradePicker.selectedItems()]
        print(grades)
        self.selected_grades = grades

    def kanji_only_changed(self, state):
        self.kanji_only = Qt.CheckState(state) == Qt.CheckState.Checked

    def jukugo_only_changed(self, state):
        self.jukugo_only = Qt.CheckState(state) == Qt.CheckState.Checked

    def difficulty_changed(self):
        self.selected_difficulty = self.difficulty_picker.selectedItems()[0].text()
        print(self.selected_difficulty)

    def reset_menu_screen(self):
        self.selected_grades = None
        self.kanji_only = True
        self.jukugo_only = False

        self.question_amount.setValue(10)
        self.gradePicker.clearSelection()
        self.kanji_only_box.setCheckState(Qt.CheckState.Checked)
        self.jukugo_only_box.setCheckState(Qt.CheckState.Unchecked)

