from dataclasses import dataclass
from typing import Any, Dict

from .export_acceptance_report import ExportAcceptanceReport


@dataclass
class ExportCompletionResult:
    acceptance: ExportAcceptanceReport
    report_path: str
    metadata: Dict[str, Any]
