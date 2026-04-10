from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ImprovedCompilableRuntimeProjectReadiness:
    todo_count: int = 0
    unsupported_count: int = 0
    task_file_todo_counts: Dict[str, int] = field(default_factory=dict)
    task_file_unsupported_counts: Dict[str, int] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
