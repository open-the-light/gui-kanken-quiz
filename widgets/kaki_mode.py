from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
import base64
from widgets.drawing_canvas import DrawingCanvas

import timeit

class KakiMode(QWidget):
    def __init__(self, client):
        super().__init__()

        self.client = client
        layout = QVBoxLayout(self)

        self.canvas = DrawingCanvas()

        layout.addStretch(2)
        layout.addWidget(self.canvas, 2, alignment=Qt.AlignCenter)  # stretch=1 so it takes available space
        layout.addStretch(2)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.canvas.clear)
        clear_btn.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(clear_btn, 0)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            print("saving image!!!")
            self.canvas.image.save("./tests/answer.png")
            self.submit_for_grading()

    def submit_for_grading(self):
        with open("./tests/answer.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        response = self.client.responses.create(
            model="gpt-5-mini",
            reasoning={
                "effort": "low"
            },
            input=[{
                "role":"user",
                "content": [
                    {"type": "input_text", "text": "Is this handwritten character the same as 論? Answer yes/no + confidence."},
                    {"type": "input_image",
                     "image_url": f"data:image/png;base64,{encoded_string}"}
                ]
            }]
        )

        print(response)