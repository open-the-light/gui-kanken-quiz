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
        title_label.setProperty("class", "title")

        yomi_button = QPushButton()
        yomi_button.setText("読み")
        yomi_button.clicked.connect(show_yomi)

        douon_button = QPushButton("同音・同訓異字")
        shikibetsu_button = QPushButton("漢字識別")
        jukugokousei_button = QPushButton("熟語の構成")
        bushu_button = QPushButton("部首")
        tairui_button = QPushButton("対義語・類義語")
        okurigana_button = QPushButton("送り仮名")
        yojijukugo_button = QPushButton("四字熟語")
        gojiteisei_button = QPushButton("誤字訂正")
        kaki_button = QPushButton("書き取り")

        layout.addSpacing(20)
        layout.addWidget(title_label)
        layout.addSpacing(40)
        layout.addWidget(yomi_button)
        layout.addWidget(douon_button)
        layout.addWidget(shikibetsu_button)
        layout.addWidget(jukugokousei_button)
        layout.addWidget(bushu_button)
        layout.addWidget(tairui_button)
        layout.addWidget(okurigana_button)
        layout.addWidget(yojijukugo_button)
        layout.addWidget(gojiteisei_button)
        layout.addWidget(kaki_button)
        layout.addStretch(1)

