import subprocess
from typing import Callable

from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout
from pydantic import BaseModel

from widgets._base import WidgetConfig, Widget
from window import Window


class ButtonConfig(BaseModel):
    label: str
    command: str


class ButtonMenuConfig(WidgetConfig):
    BUTTONS: list[ButtonConfig]


class ButtonMenu(Widget):
    CONFIG_CLASS: ButtonConfig


    def __init__(self, window: Window, config: ButtonMenuConfig) -> None:
        super().__init__(window, config)
        self.window = window

        for button_config in self.config.BUTTONS:
            button = QPushButton(button_config.label)
            button.clicked.connect(self.__get_button_click_func(button_config.command))
            self.addWidget(button)


    def __get_button_click_func(self, command: str) -> Callable[[], None]:
        def button_click() -> None:
            subprocess.Popen(
                command,
                shell=True,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )
            self.window.hide()

        return button_click
