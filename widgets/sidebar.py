from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)


class Sidebar(QWidget):
    def __init__(self, show_yomi):
        super().__init__()

        layout = QVBoxLayout(self)

        title_label = QLabel("漢検クイズ")
        title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        yomi_button = QPushButton()
        yomi_button.setText("読み")
        yomi_button.clicked.connect(show_yomi)

        kaki_button = QPushButton()
        kaki_button.setText("書き取り")

        layout.addWidget(title_label)
        layout.addSpacing(40)
        layout.addWidget(yomi_button)
        layout.addWidget(kaki_button)
        layout.addStretch(1)

