from pathlib import Path

from base_tool.read_json import json_reader

from .api import LocatorRepositoryBase
from .types import Locator, Point, Rect


class JsonLocatorRepository(LocatorRepositoryBase):
    """基于当前仓库 json_reader 的 PC 侧 locator 适配器。"""

    def __init__(self, json_path):
        self.json_path = Path(json_path)
        self.reader = json_reader(self.json_path)

    def get(self, locator_name: str) -> Locator:
        image_path = self.reader.img_path(locator_name)
        top_left, bottom_right = self.reader.img_areas(locator_name)
        return Locator(
            name=locator_name,
            image_path=str(image_path),
            rect=Rect(
                top_left=Point(int(top_left[0]), int(top_left[1])),
                bottom_right=Point(int(bottom_right[0]), int(bottom_right[1])),
            ),
        )
