from PyQt6.QtWidgets import QApplication
from pydantic import BaseModel

from fifo_reader import FifoReader
from window import WindowConfig, WindowManager


app_config = {
    "FIFO_PATH": "/tmp/pricheta_de",
    "WINDOWS": [
        {
            "TITLE": "pricheta_launcher",
            "X": 0,
            "Y": 0,
            "WIDTH": 1920,
            "HEIGHT": 1080,
            "CSS_FILE_PATH": "/home/pricheta/.config/pricheta_de/launcher/style.css",
            "WIDGETS": [
                {
                    "NAME": "Button Menu",
                    "CONFIG": {
                        "BUTTON_SIZE": 128,
                        "HIDE_WINDOW_AFTER_CLICK": True,
                        "BUTTONS": [
                            {
                                "LABEL": "",
                                "COMMAND": "/home/pricheta/Programs/pycharm/bin/pycharm",
                            },
                            {
                                "LABEL": "",
                                "COMMAND": "/usr/bin/firefox",
                            },
                        ],
                    },
                }
            ],
        },
    ]
}


class AppConfig(BaseModel):
    WINDOWS: list[WindowConfig]
    FIFO_PATH: str


CONFIG_PATH = '/home/pricheta/.config/pricheta_de/pricheta_de.conf'

if __name__ == "__main__":
    config = AppConfig.model_validate(app_config)
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
