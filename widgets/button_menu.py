import subprocess
from typing import Callable

from PyQt6.QtWidgets import QPushButton
from pydantic import BaseModel

from common import RAW_CONFIG
from widgets.base import PrichetaWidget


class ButtonConfig(BaseModel):
    LABEL: str
    COMMAND: str


class ButtonMenuConfig(BaseModel):
    BUTTONS: list[ButtonConfig]
    HIDE_WINDOW_AFTER_CLICK: bool


class ButtonMenu(PrichetaWidget):
    def __init__(self, config: RAW_CONFIG) -> None:
        super().__init__()
        self.config = ButtonMenuConfig.model_validate(config)

        for button_config in self.config.BUTTONS:
            button = QPushButton(button_config.LABEL)
            button.clicked.connect(self.__get_button_click_func(button_config.COMMAND))
            self.addWidget(button)


    def __get_button_click_func(self, command: str) -> Callable[[], None]:
        def button_click_func() -> None:
            subprocess.Popen(
                command,
                shell=True,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL
            )

            if self.config.HIDE_WINDOW_AFTER_CLICK:
                window = self.parent().parent()
                window.destroy()

        return button_click_func
