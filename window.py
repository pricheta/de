from typing import Type

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from pydantic import BaseModel

from common import WidgetName, RAW_CONFIG, logger
from widgets.base import PrichetaWidget
from widgets.button_menu import ButtonMenu

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


class Window(QWidget):
    def __init__(self, config: WindowConfig):
        super().__init__()
        self.config = config

        self.setWindowTitle(self.config.TITLE)
        self.setGeometry(
            self.config.X, self.config.Y, self.config.WIDTH, self.config.HEIGHT
        )

        self.__build_widgets()

    def __build_widgets(self) -> None:
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        for widget_config in self.config.WIDGETS:
            widget_type = WIDGET_NAME_TO_TYPE_MAP[widget_config.NAME]
            widget = widget_type(widget_config.CONFIG)
            main_layout.addLayout(widget)

    def closeEvent(self, event):
        self.hide()
        event.ignore()


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
