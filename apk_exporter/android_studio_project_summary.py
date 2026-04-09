from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AndroidStudioProjectSummary:
    project_root: str
    task_count: int = 0
    task_ids: List[str] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)
