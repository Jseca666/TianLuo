from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RuntimeSemanticReadinessSummary:
    project_root: str
    task_count: int = 0
    task_ids: List[str] = field(default_factory=list)
    expected_kernel_size_steps: int = 0
    expected_excluded_number_steps: int = 0
    ocr_read_options_count: int = 0
    kernel_size_option_count: int = 0
    excluded_number_option_count: int = 0
    read_text_semantic_count: int = 0
    read_number_semantic_count: int = 0
    task_file_counts: Dict[str, Dict[str, int]] = field(default_factory=dict)
    files: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
