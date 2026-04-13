from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PaddleOcrRuntimeSummary:
    project_root: str
    files: Dict[str, str] = field(default_factory=dict)
    checks: Dict[str, bool] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
