from dataclasses import dataclass, field
from typing import Any, Dict, List

from .export_execution_result import ExportExecutionResult


@dataclass
class ExportAcceptanceReport:
    passed: bool
    checks: Dict[str, bool] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    preview: Dict[str, Any] = field(default_factory=dict)
    execution: ExportExecutionResult | None = None
