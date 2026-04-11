from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MainExportComparisonSummary:
    baseline_project_root: str
    quality_project_root: str
    baseline_todo_count: int = 0
    quality_todo_count: int = 0
    baseline_unsupported_count: int = 0
    quality_unsupported_count: int = 0
    baseline_asset_file_count: int = 0
    quality_asset_file_count: int = 0
    baseline_validation_ok: bool = False
    quality_validation_ok: bool = False
    files: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
