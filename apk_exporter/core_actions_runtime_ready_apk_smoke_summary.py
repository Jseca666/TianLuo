from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CoreActionsRuntimeReadyApkSmokeSummary:
    project_root: str
    package_name: str
    main_activity: str
    apk_relative_path: str
    host_scripts: Dict[str, str] = field(default_factory=dict)
    checks: Dict[str, bool] = field(default_factory=dict)
    commands: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
