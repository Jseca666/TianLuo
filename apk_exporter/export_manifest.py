from dataclasses import dataclass, field
from typing import List


@dataclass
class ExportManifest:
    locator_files: List[str] = field(default_factory=list)
    template_files: List[str] = field(default_factory=list)
    mask_files: List[str] = field(default_factory=list)
