from abc import ABC, abstractmethod
from typing import List, Optional

from .types import CaptureFrame, Locator, MatchResult, Point, PointLike


class LocatorRepositoryBase(ABC):
    @abstractmethod
    def get(self, locator_name: str) -> Locator:
        raise NotImplementedError


class ExportableTaskApi(ABC):
    @abstractmethod
    def launch_app(self, package_name: str, activity: Optional[str] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop_app(self, package_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def tap(self, point: PointLike) -> bool:
        raise NotImplementedError

    @abstractmethod
    def tap_locator(
        self,
        locator_name: str,
        threshold: float = 0.8,
        timeout: float = 10.0,
        mask: Optional[str] = None,
        use_color: bool = False,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def tap_area(self, locator_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def swipe(self, start: PointLike, end: PointLike, duration_ms: int = 3000) -> None:
        raise NotImplementedError

    @abstractmethod
    def back(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def sleep(self, seconds: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def capture(self) -> CaptureFrame:
        raise NotImplementedError

    @abstractmethod
    def wait_image(
        self,
        locator_name: str,
        threshold: float = 0.8,
        timeout: float = 10.0,
        mask: Optional[str] = None,
        use_color: bool = False,
    ) -> Optional[MatchResult]:
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        locator_name: str,
        threshold: float = 0.8,
        timeout: float = 1.0,
        mask: Optional[str] = None,
        use_color: bool = False,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def ocr_text(
        self,
        locator_name: str,
        mask: Optional[str] = None,
        kernel_size: Optional[int] = None,
    ) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def ocr_int(
        self,
        locator_name: str,
        mask: Optional[str] = None,
        excluded_number: Optional[int] = None,
        kernel_size: Optional[int] = None,
    ) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    def compare(
        self,
        frame_a: CaptureFrame,
        frame_b: CaptureFrame,
        threshold: float = 0.85,
        mask: Optional[str] = None,
        use_color: bool = False,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def locator(self, locator_name: str) -> Locator:
        raise NotImplementedError

    @abstractmethod
    def center(self, locator_name: str) -> Point:
        raise NotImplementedError
