from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SemanticGapBacklogItem:
    gap_key: str
    priority: str
    expected_count: int = 0
    resolved_count: int = 0
    unresolved_count: int = 0
    visibility_count: int = 0
    target_files: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass
class SemanticGapBacklogSummary:
    project_root: str
    total_unresolved_gap_count: int = 0
    items: List[SemanticGapBacklogItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)
