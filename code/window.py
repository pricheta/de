from pathlib import Path
from typing import Type

from PyQt6.QtCore import QFile, QTextStream, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from pydantic import BaseModel

from code.const import WidgetName, RAW_CONFIG, logger
from code.widgets.base import PrichetaWidget
from code.widgets.button_menu import ButtonMenu

WIDGET_NAME_TO_TYPE_MAP: dict[str, Type[PrichetaWidget]] = {
    "Button Menu": ButtonMenu,
}


class WidgetConfig(BaseModel):
    NAME: WidgetName
    CONFIG: RAW_CONFIG | None = None


class WindowConfig(BaseModel):
    TITLE: str
    X: int
    Y: int
    WIDTH: int
    HEIGHT: int
    WIDGETS: list[WidgetConfig]
    CSS_FILE_PATH: Path | None = None


class Window(QWidget):
    def __init__(self, config: WindowConfig):
        super().__init__()
        self.config = config

        self.setWindowTitle(self.config.TITLE)
        self.setGeometry(
            self.config.X, self.config.Y, self.config.WIDTH, self.config.HEIGHT
        )

        self.__build_widgets()

        if self.config.CSS_FILE_PATH:
            from __main__ import CONF_PATH

            css_file_path = CONF_PATH / self.config.CSS_FILE_PATH
            self.__apply_stylesheet(str(css_file_path))

    def __build_widgets(self) -> None:
        background = QWidget(self)
        background.setObjectName("background")
        background_layout = QHBoxLayout(background)

        for widget_config in self.config.WIDGETS:
            widget_type = WIDGET_NAME_TO_TYPE_MAP[widget_config.NAME]
            widget = widget_type(widget_config.CONFIG)
            background_layout.addLayout(widget)

        root_layout = QHBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(background)
        self.setLayout(root_layout)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def __apply_stylesheet(self, file_name: str) -> None:
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        file = QFile(file_name)
        if not file.exists():
            logger.error(f"Style sheet file '{file_name}' does not exist!")
            return

        if not file.open(QFile.OpenModeFlag.ReadOnly):
            logger.error(f"Cannot open style sheet file '{file_name}'")
            return

        try:
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
        finally:
            file.close()


class WindowManager:
    def __init__(self, window_configs: dict[str, WindowConfig]):
        self.window_configs = window_configs
        self.active_window: Window | None = None

    def build_and_show(
        self,
        window_name: str,
    ):
        config = self.window_configs.get(window_name)

        if not config:
            logger.error(f"Window {window_name} not found")
            return

        if self.active_window:
            self.active_window.destroy()

        self.active_window = Window(config)
        self.active_window.show()
