from dataclasses import dataclass, field
from typing import List


@dataclass
class RuntimeBehaviorStageStatusItem:
    stage_key: str
    status: str
    reason: str
    evidence: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)


@dataclass
class RuntimeBehaviorStageStatusSummary:
    overall_status: str
    items: List[RuntimeBehaviorStageStatusItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
