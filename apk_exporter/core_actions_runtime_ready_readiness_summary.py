from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CoreActionsRuntimeReadyReadinessSummary:
    project_root: str
    task_count: int = 0
    task_ids: List[str] = field(default_factory=list)
    expected_tap_steps: int = 0
    expected_swipe_steps: int = 0
    expected_back_steps: int = 0
    expected_sleep_steps: int = 0
    generated_tap_count: int = 0
    generated_swipe_count: int = 0
    generated_back_count: int = 0
    generated_delay_count: int = 0
    generated_fail_checks_count: int = 0
    task_file_counts: Dict[str, Dict[str, int]] = field(default_factory=dict)
    files: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
