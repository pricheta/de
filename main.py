import logging

from PyQt6.QtWidgets import QApplication

from fifo_reader import FifoReaderConfig, FifoReader
from window import Window


logger = logging.getLogger(__name__)


def show_window(window_name: str, windows: dict[str, Window]):
    window = windows.get(window_name)

    if not window:
        logger.error(f"Window {window_name} not found")
        return

    window.show()


if __name__ == "__main__":
    app = QApplication([])
    windows = {}

    fifo_reader_config = FifoReaderConfig(FIFO_PATH='/tmp/my_fifo')
    fifo_reader = FifoReader(fifo_reader_config, windows)
    fifo_reader.SIGNAL_EMITTER.connect(lambda window_name: show_window(window_name, windows))

    fifo_reader.start()
    app.exec()

