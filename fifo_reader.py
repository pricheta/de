import logging
import os

from PyQt6.QtCore import QThread, pyqtSignal
from pydantic import BaseModel

from window import Window

logger = logging.getLogger(__name__)

class FifoReaderConfig(BaseModel):
    FIFO_PATH: str


class FifoReader(QThread):
    SIGNAL_EMITTER = pyqtSignal(str)


    def __init__(self, config: FifoReaderConfig, windows: dict[str, Window]):
        super().__init__()
        self.config = config
        self.windows = windows


    def run(self):
        if os.path.exists(self.config.FIFO_PATH):
            os.remove(self.config.FIFO_PATH)

        os.mkfifo(self.config.FIFO_PATH)

        while True:
            with open(self.config.FIFO_PATH, "r") as fifo:
                message = fifo.readline().strip()
                logger.info(f"Message: {message} received")
                self.SIGNAL_EMITTER.emit(message)
