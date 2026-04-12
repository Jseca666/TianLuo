from dataclasses import dataclass, field
from typing import List


@dataclass
class SemanticQualityWorkItem:
    title: str
    priority: str
    rationale: str
    target_files: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)


@dataclass
class SemanticQualityWorkItemPlanSummary:
    overall_focus: str
    items: List[SemanticQualityWorkItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
