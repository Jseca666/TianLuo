from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DeliveryReadyCompilableRuntimeProjectReportSummary:
    project_root: str
    task_count: int = 0
    task_ids: List[str] = field(default_factory=list)
    validation_ok: bool = False
    todo_count: int = 0
    unsupported_count: int = 0
    files: Dict[str, str] = field(default_factory=dict)
