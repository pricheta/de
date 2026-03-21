from PyQt6.QtWidgets import QHBoxLayout

from configs import RAW_CONFIG


class PrichetaWidget(QHBoxLayout):
    def __init__(self, config: RAW_CONFIG | None = None):
        super().__init__()
        raise NotImplementedError()
