from dataclasses import dataclass, field
from typing import Dict


@dataclass
class AndroidProjectWriteResult:
    root_dir: str
    task_files: Dict[str, str] = field(default_factory=dict)
    registry_file: str = ""
