from dataclasses import dataclass, field
from typing import Dict

from .export_models import ExportedTaskModel


@dataclass
class TaskExportResult:
    tasks: Dict[str, str] = field(default_factory=dict)
    registry: str = ""
    models: Dict[str, ExportedTaskModel] = field(default_factory=dict)
