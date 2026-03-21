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

class WindowManager:
    def __init__(self, window_configs: dict[str, WindowConfig]):
        self.window_configs = window_configs
        self.active_window = None

    def build_and_show(self, window_name: str, ):
        config = self.window_configs.get(window_name)

        if not config:
            logger.error(f"Window {window_name} not found")
            return

        if self.active_window:
            self.active_window.destroy()

        self.active_window = Window(config)
        self.active_window.show()


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
