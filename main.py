import sys
import os

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication
from pydantic import BaseModel

from window import Window


class FifoReaderConfig(BaseModel):
    FIFO_PATH = "/tmp/my_fifo"



class FifoReader(QThread):
    SIGNAL_EMITTER = pyqtSignal(str)

    def __init__(self, config: FifoReaderConfig):
        super().__init__()
        self.config = config

    def run(self):
        if os.path.exists(self.config.FIFO_PATH):
            os.remove(self.config.FIFO_PATH)

        os.mkfifo(self.config.FIFO_PATH)

        while True:
            with open(self.config.FIFO_PATH, "r") as fifo:
                message = fifo.readline().strip()
                if message:
                    self.SIGNAL_EMITTER.emit(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    # Run the app
    sys.exit(app.exec())