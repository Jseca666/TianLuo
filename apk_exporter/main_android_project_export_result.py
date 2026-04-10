from dataclasses import dataclass
from typing import Any, Dict

from .default_android_project_export_delivery_summary import DefaultAndroidProjectExportDeliverySummary


@dataclass
class MainAndroidProjectExportResult:
    summary: DefaultAndroidProjectExportDeliverySummary
    deep_validation: Any
    readiness: Any
    package_report_path: str
    default_report_path: str
    main_report_path: str
    metadata: Dict[str, Any]
