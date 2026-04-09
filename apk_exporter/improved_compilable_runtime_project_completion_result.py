from dataclasses import dataclass
from typing import Dict, Any

from .android_studio_project_export_result import AndroidStudioProjectExportResult
from .improved_compilable_runtime_project_validation import ImprovedCompilableRuntimeProjectValidation


@dataclass
class ImprovedCompilableRuntimeProjectCompletionResult:
    export_result: AndroidStudioProjectExportResult
    validation: ImprovedCompilableRuntimeProjectValidation
    metadata: Dict[str, Any]
