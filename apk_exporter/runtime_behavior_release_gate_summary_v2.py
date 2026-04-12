from dataclasses import dataclass, field
from typing import List


@dataclass
class RuntimeBehaviorReleaseGateItemV2:
    gate_key: str
    status: str
    rationale: str
    unblock_actions: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)


@dataclass
class RuntimeBehaviorReleaseGateSummaryV2:
    overall_gate: str
    items: List[RuntimeBehaviorReleaseGateItemV2] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
