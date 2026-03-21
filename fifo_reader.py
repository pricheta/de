import logging
import os

from PyQt6.QtCore import QThread, pyqtSignal

from common import logger


class FifoReader(QThread):
    SIGNAL_EMITTER = pyqtSignal(str)

    def __init__(self, fifo_path: str):
        super().__init__()
        self.fifo_path = fifo_path

    def run(self):
        if os.path.exists(self.fifo_path):
            os.remove(self.fifo_path)

        os.mkfifo(self.fifo_path)

        while True:
            with open(self.fifo_path, "r") as fifo:
                message = fifo.readline().strip()
                logger.info(f"Message: {message} received")
                self.SIGNAL_EMITTER.emit(message)
