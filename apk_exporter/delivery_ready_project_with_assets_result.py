from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class DeliveryReadyProjectWithAssetsResult:
    delivery: Dict[str, Any]
    assets: Dict[str, Any]
    metadata: Dict[str, Any]
