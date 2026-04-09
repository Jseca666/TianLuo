from dataclasses import dataclass, field
from typing import List


@dataclass
class ExportValidationResult:
    is_valid: bool
    missing_sources: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
