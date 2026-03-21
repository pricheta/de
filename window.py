from typing import Type

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from pydantic import BaseModel

from const import WidgetName, RAW_CONFIG
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
            self.config.X,
            self.config.Y,
            self.config.WIDTH,
            self.config.HEIGHT
        )

        self.__build_widgets()

    def __build_widgets(self) -> None:
        self.main_layout = QHBoxLayout()

        for raw_config in self.config.WIDGETS:
            widget_type = WIDGET_NAME_TO_TYPE_MAP[raw_config.NAME]
            widget = widget_type(raw_config.CONFIG)
            self.main_layout.addLayout(widget)

    def closeEvent(self, event):
        self.hide()
        event.ignore()
