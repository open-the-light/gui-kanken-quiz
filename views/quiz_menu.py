from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QLabel
)

class QuizMenu(QWidget):
    def __init__(self, start_quiz):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("クイズｎ設定を選べよ"))

        self.gradePicker = QListWidget()
        self.gradePicker.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.gradePicker.addItems(["１級", "1.5級", "2級", "2.5級", "3級", "4級", "5級", "6級", "7級", "8級", "9級", "10級"])
        self.gradePicker.selectionModel().selectionChanged.connect(self.grade_changed)
        layout.addWidget(self.gradePicker)

        self.start_quiz_button = QPushButton()
        self.start_quiz_button.setText("スタート！")
        self.start_quiz_button.clicked.connect(start_quiz)
        layout.addWidget(self.start_quiz_button)

    def grade_changed(self):
        print([i.text() for i in self.gradePicker.selectedItems()])