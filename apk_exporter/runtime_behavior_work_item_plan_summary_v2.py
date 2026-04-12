from dataclasses import dataclass, field
from typing import List


@dataclass
class RuntimeBehaviorWorkItemV2:
    title: str
    priority: str
    rationale: str
    target_files: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)


@dataclass
class RuntimeBehaviorWorkItemPlanSummaryV2:
    overall_focus: str
    items: List[RuntimeBehaviorWorkItemV2] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
