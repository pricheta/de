from PyQt6.QtWidgets import QHBoxLayout

from common import RAW_CONFIG


class PrichetaWidget(QHBoxLayout):
    def __init__(self, config: RAW_CONFIG | None = None):
        super().__init__()
