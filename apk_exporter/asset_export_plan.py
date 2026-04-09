from dataclasses import dataclass, field
from typing import List


@dataclass
class AssetCopyItem:
    source_path: str
    target_path: str


@dataclass
class AssetExportPlan:
    items: List[AssetCopyItem] = field(default_factory=list)
