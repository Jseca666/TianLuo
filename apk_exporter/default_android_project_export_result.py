from dataclasses import dataclass
from typing import Any, Dict

from .default_android_project_export_summary import DefaultAndroidProjectExportSummary


@dataclass
class DefaultAndroidProjectExportResult:
    summary: DefaultAndroidProjectExportSummary
    deep_validation: Any
    package_report_path: str
    default_report_path: str
    metadata: Dict[str, Any]
