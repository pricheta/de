import re
import subprocess

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QLabel, QVBoxLayout, QWidget
from pydantic import BaseModel

from code.const import RAW_CONFIG
from code.widgets.base import PrichetaWidget


class SliderConfig(BaseModel):
    STEP: int = 5
    SINK: str = "@DEFAULT_AUDIO_SINK@"


class Slider(PrichetaWidget):
    def __init__(self, config: RAW_CONFIG) -> None:
        super().__init__()
        self.config = SliderConfig.model_validate(config)

        self.volume_label = QLabel()
        self.volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(self.config.STEP)
        self.slider.setPageStep(self.config.STEP)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)

        self.slider.valueChanged.connect(self.__on_value_changed)

        self.__update_volume_display()

        layout = QVBoxLayout()
        layout.addWidget(self.volume_label)
        layout.addWidget(self.slider)

        container = QWidget()
        container.setLayout(layout)

        self.addWidget(container, 0, 0)

    def __on_value_changed(self, value: int) -> None:
        subprocess.run(
            ["wpctl", "set-volume", self.config.SINK, f"{value}%"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.__update_volume_display()

    def __update_volume_display(self) -> None:
        result = subprocess.run(
            ["wpctl", "get-volume", self.config.SINK],
            capture_output=True,
            text=True,
        )
        output = result.stdout

        match = re.search(r"(\d+(?:\.\d+)?)%", output)
        if match:
            volume = int(float(match.group(1)))
            self.volume_label.setText(f"Volume: {volume}%")
        else:
            self.volume_label.setText("Volume: --")
