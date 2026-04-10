from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MainExportQualityProjectExportResult:
    project_root: str
    write_result: Any
    readiness: Any
    assets: Dict[str, Any]
    metadata: Dict[str, Any]
