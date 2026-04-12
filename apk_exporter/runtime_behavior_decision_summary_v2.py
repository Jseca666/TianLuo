from dataclasses import dataclass, field
from typing import List


@dataclass
class RuntimeBehaviorDecisionItemV2:
    lane: str
    priority: str
    decision: str
    rationale: str
    related_work_items: List[str] = field(default_factory=list)


@dataclass
class RuntimeBehaviorDecisionSummaryV2:
    primary_focus: str
    secondary_focus: str
    freeze_recommendations: List[str] = field(default_factory=list)
    items: List[RuntimeBehaviorDecisionItemV2] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
