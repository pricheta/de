import sys
import os
from enum import StrEnum
from typing import Any

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from pydantic import BaseModel

FIFO_PATH = "/tmp/my_fifo"  # You can choose any path that works for you


class FifoReaderThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, fifo_path):
        super().__init__()
        self.fifo_path = fifo_path

    def run(self):
        while True:
            with open(self.fifo_path, "r") as fifo:
                message = fifo.readline().strip()
                if message:
                    self.message_received.emit(message)


class WidgetName(StrEnum):
    BUTTON_MENU = "Button Menu"


class WidgetConfig(BaseModel):
    name: WidgetName


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

        self.fifo_thread = FifoReaderThread(FIFO_PATH)
        self.fifo_thread.message_received.connect(self.on_message_received)
        self.fifo_thread.start()


    def on_button_click(self):
        self.label.setText("Button clicked!")


    def on_message_received(self, message: str):
        print(f"Received command: {message}")
        if message == "change_text":
            self.label.setText("Text changed via FIFO!")
        elif message == "hide":
            self.hide()



if __name__ == "__main__":
    if os.path.exists(FIFO_PATH):
        os.remove(FIFO_PATH)

    os.mkfifo(FIFO_PATH)

    app = QApplication(sys.argv)
    window = Window()
    window.show()

    # Run the app
    sys.exit(app.exec())