import subprocess
from math import sqrt
from typing import Callable

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QPushButton
from pydantic import BaseModel

from code.const import RAW_CONFIG
from code.widgets.base import PrichetaWidget


class ButtonConfig(BaseModel):
    LABEL: str
    COMMAND: str


class ButtonMenuConfig(BaseModel):
    BUTTONS: list[ButtonConfig]
    HIDE_WINDOW_AFTER_CLICK: bool
    BUTTON_SIZE: int
    SPACING: int


class ButtonMenu(PrichetaWidget):
    def __init__(self, config: RAW_CONFIG) -> None:
        super().__init__()
        self.config = ButtonMenuConfig.model_validate(config)
        self.setSpacing(self.config.SPACING)

        buttons_amount = len(self.config.BUTTONS)
        max_columns = int(sqrt(buttons_amount)) + 1

        for index, button_config in enumerate(self.config.BUTTONS):
            button = QPushButton(button_config.LABEL)
            button.clicked.connect(self.__get_button_click_func(button_config.COMMAND))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFixedSize(self.config.BUTTON_SIZE, self.config.BUTTON_SIZE)

            button_row = index // max_columns
            button_col = index % max_columns

            self.addWidget(button, button_row, button_col)

    def __get_button_click_func(self, command: str) -> Callable[[], None]:
        from code.window import Window

        def button_click_func() -> None:

            subprocess.Popen(
                command,
                shell=True,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )

            if self.config.HIDE_WINDOW_AFTER_CLICK:
                window = __get_window(self)
                window.destroy()

        def __get_window(obj: QObject) -> Window:
            current: QObject | None = obj

            while current is not None:
                if isinstance(current, Window):
                    return current
                current = current.parent()

            raise RuntimeError("Window not found in parents hierarchy")

        return button_click_func
