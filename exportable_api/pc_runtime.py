import re
import time
from pathlib import Path
from typing import List, Optional

from base_tool.AndroidDevice import AndroidDevice
from base_tool.projection_root import find_project_root

from .api import ExportableTaskApi
from .pc_locator_repository import JsonLocatorRepository
from .types import CaptureFrame, MatchResult, Point, ensure_point


class ExportablePcTaskApi(ExportableTaskApi):
    """基于当前 PC + ADB 能力层的 V1 API 适配器。"""

    def __init__(self, device: AndroidDevice, locator_repo: JsonLocatorRepository):
        self.device = device
        self.locator_repo = locator_repo

    @classmethod
    def from_json(cls, adb_path: str, device_address: str, json_path: str):
        device = AndroidDevice(adb_path=adb_path, device_address=device_address)
        project_root = find_project_root()
        device.img_path_abs = project_root / 'tool'
        device.connect_device()
        locator_repo = JsonLocatorRepository(json_path)
        return cls(device=device, locator_repo=locator_repo)

    def launch_app(self, package_name: str, activity: Optional[str] = None) -> None:
        self.device.launch_app(package_name, activity)

    def stop_app(self, package_name: str) -> None:
        self.device.stop_app(package_name)

    def tap(self, point) -> bool:
        point = ensure_point(point)
        return bool(self.device.tap_on_screen(point.as_tuple()))

    def tap_locator(self, locator_name: str, threshold: float = 0.8, timeout: float = 10.0, mask: Optional[str] = None, use_color: bool = False) -> bool:
        match = self.wait_image(locator_name, threshold=threshold, timeout=timeout, mask=mask, use_color=use_color)
        if match is None:
            return False
        return self.tap(match.center)

    def tap_area(self, locator_name: str) -> bool:
        return self.tap(self.center(locator_name))

    def swipe(self, start, end, duration_ms: int = 3000) -> None:
        start_point = ensure_point(start)
        end_point = ensure_point(end)
        self.device.swipe_on_screen(start_point.as_tuple(), end_point.as_tuple(), duration=duration_ms)

    def back(self) -> bool:
        self.device.press_back_button()
        return True

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def capture(self) -> CaptureFrame:
        image_path = self.device.capture_screenshot()
        if image_path is None:
            raise RuntimeError('截图失败')
        return CaptureFrame(image_path=Path(image_path))

    def wait_image(self, locator_name: str, threshold: float = 0.8, timeout: float = 10.0, mask: Optional[str] = None, use_color: bool = False) -> Optional[MatchResult]:
        locator = self.locator(locator_name)
        matches = self.device.wait_for_image(locator.image_path, timeout=timeout, threshold=threshold, mask_name=mask, use_color=use_color)
        if matches == [0] or not matches:
            return None
        points = [Point(int(x), int(y)) for x, y in matches]
        return MatchResult(locator_name=locator_name, center=points[0], matches=points)

    def exists(self, locator_name: str, threshold: float = 0.8, timeout: float = 1.0, mask: Optional[str] = None, use_color: bool = False) -> bool:
        return self.wait_image(locator_name, threshold=threshold, timeout=timeout, mask=mask, use_color=use_color) is not None

    def ocr_text(self, locator_name: str, mask: Optional[str] = None, kernel_size: Optional[int] = None) -> List[str]:
        locator = self.locator(locator_name)
        result = self.device.get_text_from_screen(
            locator.rect.top_left.as_tuple(),
            locator.rect.bottom_right.as_tuple(),
            mask_name=mask,
            kernel_size=kernel_size,
        )
        if result is None:
            return []
        if isinstance(result, list):
            return [str(x) for x in result if x is not None]
        return [str(result)]

    def ocr_int(self, locator_name: str, mask: Optional[str] = None, excluded_number: Optional[int] = None, kernel_size: Optional[int] = None) -> Optional[int]:
        texts = self.ocr_text(locator_name, mask=mask, kernel_size=kernel_size)
        numbers = []
        for text in texts:
            numbers.extend(re.findall(r'\d+', text))
        for num in numbers:
            if excluded_number is not None and num == str(excluded_number):
                continue
            return int(num)
        return None

    def compare(self, frame_a: CaptureFrame, frame_b: CaptureFrame, threshold: float = 0.85, mask: Optional[str] = None, use_color: bool = False) -> bool:
        return bool(self.device.compare_images(str(frame_a.image_path), str(frame_b.image_path), threshold=threshold, mask_name=mask, use_color=use_color))

    def locator(self, locator_name: str):
        return self.locator_repo.get(locator_name)

    def center(self, locator_name: str) -> Point:
        locator = self.locator(locator_name)
        x = int((locator.rect.top_left.x + locator.rect.bottom_right.x) / 2)
        y = int((locator.rect.top_left.y + locator.rect.bottom_right.y) / 2)
        return Point(x, y)
