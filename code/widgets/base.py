from PyQt6.QtWidgets import QHBoxLayout

from code.const import RAW_CONFIG


class PrichetaWidget(QHBoxLayout):
    def __init__(self, config: RAW_CONFIG | None = None):
        super().__init__()
