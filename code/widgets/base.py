from PyQt6.QtWidgets import QGridLayout

from code.const import RAW_CONFIG


class PrichetaWidget(QGridLayout):
    def __init__(self, config: RAW_CONFIG | None = None):
        super().__init__()
