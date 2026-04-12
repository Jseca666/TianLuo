from dataclasses import dataclass, field
from typing import List


@dataclass
class SemanticQualityReleaseGateItem:
    gate_key: str
    status: str
    rationale: str
    unblock_actions: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)


@dataclass
class SemanticQualityReleaseGateSummary:
    overall_gate: str
    items: List[SemanticQualityReleaseGateItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
