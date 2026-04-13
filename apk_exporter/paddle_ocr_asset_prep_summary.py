from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PaddleOcrAssetPrepSummary:
    project_root: str
    host_scripts: Dict[str, str] = field(default_factory=dict)
    expected_assets: Dict[str, str] = field(default_factory=dict)
    checks: Dict[str, bool] = field(default_factory=dict)
    commands: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
