from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SemanticParameterReadinessSummary:
    project_root: str
    task_count: int = 0
    task_ids: List[str] = field(default_factory=list)
    expected_threshold_steps: int = 0
    expected_mask_steps: int = 0
    expected_use_color_steps: int = 0
    expected_kernel_size_steps: int = 0
    expected_excluded_number_steps: int = 0
    propagated_threshold_count: int = 0
    propagated_mask_name_count: int = 0
    propagated_use_color_count: int = 0
    semantic_kernel_note_count: int = 0
    semantic_excluded_number_note_count: int = 0
    task_file_counts: Dict[str, Dict[str, int]] = field(default_factory=dict)
    files: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
