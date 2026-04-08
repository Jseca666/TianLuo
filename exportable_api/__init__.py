"""V1 可导出通用 API 包。"""

from .types import Point, Rect, Locator, MatchResult, CaptureFrame
from .api import ExportableTaskApi, LocatorRepositoryBase

__all__ = [
    "Point",
    "Rect",
    "Locator",
    "MatchResult",
    "CaptureFrame",
    "ExportableTaskApi",
    "LocatorRepositoryBase",
]
