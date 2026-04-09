from dataclasses import dataclass, field
from typing import Any, Dict

from .export_execution_result import ExportExecutionResult


@dataclass
class ExportSessionResult:
    preview: Dict[str, Any] = field(default_factory=dict)
    execution: ExportExecutionResult | None = None
