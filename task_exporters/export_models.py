from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ExportedTaskStep:
    action: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExportedTaskModel:
    task_id: str
    display_name: str
    steps: List[ExportedTaskStep] = field(default_factory=list)
