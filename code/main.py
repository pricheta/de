import json
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from pydantic import BaseModel

from code.fifo_reader import FifoReader
from code.window import WindowConfig, WindowManager

CURRENT_PATH = Path(os.path.realpath(__file__)).parent.parent
CONF_PATH = CURRENT_PATH / "conf"


class AppConfig(BaseModel):
    WINDOWS: list[WindowConfig]
    FIFO_PATH: str


if __name__ == "__main__":
    with open(CONF_PATH / "config.json", "r", encoding="utf-8") as file:
        json_config = json.load(file)

    config = AppConfig.model_validate(json_config)
    windows_configs = {
        window_config.TITLE: window_config for window_config in config.WINDOWS
    }
    window_manager = WindowManager(windows_configs)

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    fifo_reader = FifoReader(config.FIFO_PATH)
    fifo_reader.SIGNAL_EMITTER.connect(window_manager.build_and_show)
    fifo_reader.start()

    app.exec()
