from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple, Union


PointLike = Union["Point", Sequence[int], Tuple[int, int]]


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def as_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


@dataclass(frozen=True)
class Rect:
    top_left: Point
    bottom_right: Point


@dataclass(frozen=True)
class Locator:
    name: str
    image_path: str
    rect: Rect


@dataclass(frozen=True)
class MatchResult:
    locator_name: str
    center: Point
    matches: List[Point]


@dataclass(frozen=True)
class CaptureFrame:
    image_path: Path


def ensure_point(value: PointLike) -> Point:
    if isinstance(value, Point):
        return value
    if len(value) != 2:
        raise ValueError("PointLike 必须包含两个整数坐标")
    return Point(int(value[0]), int(value[1]))
