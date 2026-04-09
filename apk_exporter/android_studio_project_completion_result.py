from dataclasses import dataclass
from typing import Dict, Any

from .android_studio_project_export_result import AndroidStudioProjectExportResult


@dataclass
class AndroidStudioProjectCompletionResult:
    export_result: AndroidStudioProjectExportResult
    metadata: Dict[str, Any]
