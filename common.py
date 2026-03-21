import logging
from enum import StrEnum
from typing import Any

logger = logging.getLogger("pricheta")

type RAW_CONFIG = dict[str, Any]


class WidgetName(StrEnum):
    BUTTON_MENU = "Button Menu"
