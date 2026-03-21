import logging

from PyQt6.QtWidgets import QApplication
from pydantic import BaseModel

from fifo_reader import FifoReader, FifoReaderConfig
from window import Window, WindowConfig

logger = logging.getLogger(__name__)


class AppConfig(BaseModel):
    WINDOWS: list[WindowConfig]


widget_config = {
    "NAME": "Button Menu",
    "CONFIG": {
        "BUTTONS": [
            {
                "LABEL": "test",
                "COMMAND": "test_command",
            },
        ],
    },
}

window_config = {
    "TITLE": 'test',
    "X": 10,
    "Y": 10,
    "WIDTH": 100,
    "HEIGHT": 100,
    "WIDGETS": [widget_config],
}

app_config = {"WINDOWS": [window_config]}


def show_window(window_name: str, windows: dict[str, Window]):
    window = windows.get(window_name)

    if not window:
        logger.error(f"Window {window_name} not found")
        return

    window.show()


if __name__ == "__main__":
    config = AppConfig.model_validate(app_config)
    windows = {}

    app = QApplication([])
    for window_config in config.WINDOWS:
        window = Window(window_config)
        windows[window_config.TITLE] = window

    fifo_reader_config = FifoReaderConfig(FIFO_PATH='/tmp/my_fifo')
    fifo_reader = FifoReader(fifo_reader_config, windows)
    fifo_reader.SIGNAL_EMITTER.connect(lambda window_name: show_window(window_name, windows))
    fifo_reader.start()

    app.exec()
