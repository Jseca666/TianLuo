from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SemanticQualityStageStatusItem:
    stage_key: str
    status: str
    reason: str
    evidence: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)


@dataclass
class SemanticQualityStageStatusSummary:
    overall_status: str
    items: List[SemanticQualityStageStatusItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)
