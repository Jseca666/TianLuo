from dataclasses import dataclass
from typing import Dict, Any

from .improved_compilable_runtime_project_completion_result import ImprovedCompilableRuntimeProjectCompletionResult
from .improved_compilable_runtime_project_readiness import ImprovedCompilableRuntimeProjectReadiness


@dataclass
class ImprovedCompilableRuntimeProjectDeliveryResult:
    completion: ImprovedCompilableRuntimeProjectCompletionResult
    readiness: ImprovedCompilableRuntimeProjectReadiness
    metadata: Dict[str, Any]
