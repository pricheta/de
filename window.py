from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from pydantic import BaseModel

from main import FifoReader, FIFO_PATH
from widgets._base import WidgetConfig


class WindowConfig(BaseModel):
    TITLE: str
    X: int
    Y: int
    WIDTH: int
    HEIGHT: int
    WIDGETS: list[WidgetConfig]


class Window(QWidget):
    def __init__(self, config: WindowConfig):
        super().__init__()
        self.config = config

        self.setWindowTitle(self.config.TITLE)
        self.setGeometry(
            self.config.X,
            self.config.Y,
            self.config.WIDTH,
            self.config.HEIGHT
        )

        self.label = QLabel("Hello, PyQt6!", self)
        self.button = QPushButton("Click Me", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_click)

        self.setLayout(layout)

        self.fifo_thread = FifoReader(FIFO_PATH)
        self.fifo_thread.SIGNAL_EMITTER.connect(self.on_message_received)
        self.fifo_thread.start()


    def on_button_click(self):
        self.label.setText("Button clicked!")


    def on_message_received(self, message: str):
        print(f"Received command: {message}")
        if message == "change_text":
            self.label.setText("Text changed via FIFO!")
        elif message == "hide":
            self.hide()
