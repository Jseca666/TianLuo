from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MainExportVsQualityComparisonSummary:
    project_roots: Dict[str, str] = field(default_factory=dict)
    task_counts: Dict[str, int] = field(default_factory=dict)
    asset_file_counts: Dict[str, int] = field(default_factory=dict)
    todo_counts: Dict[str, int] = field(default_factory=dict)
    unsupported_counts: Dict[str, int] = field(default_factory=dict)
    validation_ok: Dict[str, bool] = field(default_factory=dict)
    report_paths: Dict[str, str] = field(default_factory=dict)
    task_ids: List[str] = field(default_factory=list)
