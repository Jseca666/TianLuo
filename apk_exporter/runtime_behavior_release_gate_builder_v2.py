from .runtime_behavior_release_gate_summary_v2 import RuntimeBehaviorReleaseGateItemV2, RuntimeBehaviorReleaseGateSummaryV2


class RuntimeBehaviorReleaseGateBuilderV2:
    def build(self, decision_result: dict) -> RuntimeBehaviorReleaseGateSummaryV2:
        decision = decision_result.get("decision")
        plan_result = decision_result.get("plan_result", {}) if isinstance(decision_result, dict) else {}
        stage_status_result = plan_result.get("stage_status_result", {}) if isinstance(plan_result, dict) else {}
        stage_status = stage_status_result.get("stage_status") if isinstance(stage_status_result, dict) else None

        items = [
            self._helper_gate(stage_status),
            self._observability_gate(stage_status, decision),
            self._promotion_gate(stage_status, decision),
        ]

        rank = {"hold": 0, "partial": 1, "open": 2}
        overall_gate = "open"
        notes = []
        for item in items:
            if rank[item.status] < rank[overall_gate]:
                overall_gate = item.status
            notes.extend(item.evidence)

        if overall_gate == "open":
            notes.append("Runtime-behavior tracked gates are open on current benchmark scope")
        elif overall_gate == "partial":
            notes.append("Runtime-behavior tracked gates are partially open on current benchmark scope")
        else:
            notes.append("At least one runtime-behavior gate remains on hold on current benchmark scope")

        return RuntimeBehaviorReleaseGateSummaryV2(
            overall_gate=overall_gate,
            items=items,
            notes=notes,
        )

    def _helper_gate(self, stage_status):
        if stage_status is None:
            return RuntimeBehaviorReleaseGateItemV2(
                gate_key="helper_adoption",
                status="hold",
                rationale="missing runtime behavior stage status summary",
                unblock_actions=["Run runtime behavior stage status runner first"],
            )
        helper_status = self._stage_status(stage_status, "behavior_helper_usage")
        evidence = [f"behavior_helper_usage={helper_status}"]
        if helper_status == "stable":
            return RuntimeBehaviorReleaseGateItemV2(
                gate_key="helper_adoption",
                status="open",
                rationale="behavior helper usage is stable enough for broader helper-backed adoption",
                evidence=evidence,
            )
        if helper_status == "partial":
            return RuntimeBehaviorReleaseGateItemV2(
                gate_key="helper_adoption",
                status="partial",
                rationale="behavior helper usage exists but is not yet broad enough",
                unblock_actions=["Keep moving remaining OCR paths onto behavior helper APIs"],
                evidence=evidence,
            )
        return RuntimeBehaviorReleaseGateItemV2(
            gate_key="helper_adoption",
            status="hold",
            rationale="behavior helper usage has not started on current benchmark scope",
            unblock_actions=["Introduce helper-backed OCR paths before broader adoption"],
            evidence=evidence,
        )

    def _observability_gate(self, stage_status, decision):
        if stage_status is None:
            return RuntimeBehaviorReleaseGateItemV2(
                gate_key="observability_expansion",
                status="hold",
                rationale="missing runtime behavior stage status summary",
                unblock_actions=["Run runtime behavior stage status runner first"],
            )
        observability_status = self._stage_status(stage_status, "behavior_observability")
        primary_focus = getattr(decision, "primary_focus", "unknown") if decision is not None else "unknown"
        evidence = [f"behavior_observability={observability_status}", f"primary_focus={primary_focus}"]
        if observability_status == "stable":
            return RuntimeBehaviorReleaseGateItemV2(
                gate_key="observability_expansion",
                status="open",
                rationale="behavior observability is stable enough to support deeper OCR behavior implementation",
                evidence=evidence,
            )
        return RuntimeBehaviorReleaseGateItemV2(
            gate_key="observability_expansion",
            status="partial",
            rationale="behavior observability should keep expanding before deeper OCR behavior changes",
            unblock_actions=["Expose remaining runtime behavior flags before deeper behavior churn"],
            evidence=evidence,
        )

    def _promotion_gate(self, stage_status, decision):
        if stage_status is None:
            return RuntimeBehaviorReleaseGateItemV2(
                gate_key="behavior_line_promotion",
                status="hold",
                rationale="missing runtime behavior stage status summary",
                unblock_actions=["Run runtime behavior stage status runner first"],
            )
        helper_status = self._stage_status(stage_status, "behavior_helper_usage")
        observability_status = self._stage_status(stage_status, "behavior_observability")
        primary_focus = getattr(decision, "primary_focus", "unknown") if decision is not None else "unknown"
        evidence = [
            f"behavior_helper_usage={helper_status}",
            f"behavior_observability={observability_status}",
            f"primary_focus={primary_focus}",
        ]
        if helper_status == "stable" and observability_status == "stable":
            return RuntimeBehaviorReleaseGateItemV2(
                gate_key="behavior_line_promotion",
                status="open",
                rationale="runtime-behavior line is stable enough for broader promotion on current benchmark scope",
                evidence=evidence,
            )
        return RuntimeBehaviorReleaseGateItemV2(
            gate_key="behavior_line_promotion",
            status="partial",
            rationale="runtime-behavior line should keep advancing, but broader promotion should remain selective",
            unblock_actions=["Stabilize helper usage and observability before broad promotion"],
            evidence=evidence,
        )

    def _stage_status(self, stage_status, stage_key: str) -> str:
        for item in getattr(stage_status, "items", []) or []:
            if getattr(item, "stage_key", "") == stage_key:
                return getattr(item, "status", "unstarted")
        return "unstarted"
