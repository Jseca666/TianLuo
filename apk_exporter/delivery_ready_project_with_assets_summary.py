from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DeliveryReadyProjectWithAssetsSummary:
    project_root: str
    assets_root: str
    task_count: int = 0
    task_ids: List[str] = field(default_factory=list)
    asset_file_count: int = 0
    validation_ok: bool = False
    files: Dict[str, str] = field(default_factory=dict)
