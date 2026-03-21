from typing import Type, Any

from PyQt6.QtWidgets import QHBoxLayout
from pydantic import BaseModel

from const import WidgetName
from widgets.button_menu import ButtonMenu
from window import Window


class WidgetConfig(BaseModel):
    name: WidgetName
    config: dict[str, Any] | None = None


class Widget(QHBoxLayout):
    CONFIG_CLASS: WidgetConfig | None


    def __init__(self, window: Window, config: WidgetConfig | None) -> None:
        super().__init__(parent=window)
        self.config = config


WIDGET_NAME_TO_TYPE_MAP: dict[str, Type[Widget]] = {
    "Button Menu": ButtonMenu,
}
