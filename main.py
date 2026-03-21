import sys
import os
import time
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

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


class DE(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Simple App")
        self.setGeometry(100, 100, 300, 200)

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
    window = DE()
    window.show()

    # Run the app
    sys.exit(app.exec())