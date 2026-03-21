import subprocess
from typing import Callable

from PyQt6.QtWidgets import QVBoxLayout, QPushButton
from pydantic import BaseModel

from widgets._base import WidgetConfig
from window import Window


class ButtonConfig(BaseModel):
    label: str
    command: str


class ButtonMenuConfig(WidgetConfig):
    BUTTONS: list[ButtonConfig]


class ButtonMenu(QVBoxLayout):
    def __init__(self, window: Window, config: ButtonMenuConfig) -> None:
        super().__init__()
        self.window = window
        self.config = config

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
            self.window.destroy()

        return button_click
