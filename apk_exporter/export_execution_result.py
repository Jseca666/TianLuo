from dataclasses import dataclass, field
from typing import Any, Dict, List

from .export_validation import ExportValidationResult


@dataclass
class ExportExecutionResult:
    manifest_path: str
    copied_files: List[str] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    validation: ExportValidationResult | None = None
