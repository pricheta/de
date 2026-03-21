from PyQt6.QtWidgets import QWidget, QHBoxLayout
from pydantic import BaseModel

from widgets._base import WidgetConfig, WIDGET_NAME_TO_TYPE_MAP


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
            widget_class = WIDGET_NAME_TO_TYPE_MAP[raw_config.name]

            config = None
            if widget_class.CONFIG_CLASS:
                config = widget_class.CONFIG_CLASS.model_validate(raw_config.config)

            widget = widget_class(self, config)
            self.main_layout.addLayout(widget)
