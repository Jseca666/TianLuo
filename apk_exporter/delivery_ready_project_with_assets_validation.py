from dataclasses import dataclass, field
from typing import List


@dataclass
class DeliveryReadyProjectWithAssetsValidation:
    is_valid: bool
    missing_paths: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
