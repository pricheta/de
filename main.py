import logging

from PyQt6.QtWidgets import QApplication
from pydantic import BaseModel

from fifo_reader import FifoReader, FifoReaderConfig
from window import WindowConfig, WindowManager

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

if __name__ == "__main__":
    config = AppConfig.model_validate(app_config)
    windows_configs = {window_config.TITLE: window_config for window_config in config.WINDOWS}

    window_manager = WindowManager(windows_configs)

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    fifo_reader_config = FifoReaderConfig(FIFO_PATH='/tmp/my_fifo')
    fifo_reader = FifoReader(fifo_reader_config)
    fifo_reader.SIGNAL_EMITTER.connect(window_manager.build_and_show)
    fifo_reader.start()

    app.exec()
