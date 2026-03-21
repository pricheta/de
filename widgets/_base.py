from pydantic import BaseModel

from const import WidgetName


class WidgetConfig(BaseModel):
    name: WidgetName
