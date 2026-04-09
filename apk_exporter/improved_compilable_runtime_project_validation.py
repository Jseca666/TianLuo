from dataclasses import dataclass, field
from typing import List


@dataclass
class ImprovedCompilableRuntimeProjectValidation:
    is_valid: bool
    missing_files: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
