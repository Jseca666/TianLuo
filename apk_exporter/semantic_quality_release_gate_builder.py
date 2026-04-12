from .semantic_quality_release_gate_summary import SemanticQualityReleaseGateItem, SemanticQualityReleaseGateSummary


class SemanticQualityReleaseGateBuilder:
    def build(self, decision_result: dict) -> SemanticQualityReleaseGateSummary:
        decision = decision_result.get("decision")
        plan_result = decision_result.get("plan_result", {}) if isinstance(decision_result, dict) else {}
        stage_status_result = plan_result.get("stage_status_result", {}) if isinstance(plan_result, dict) else {}
        stage_status = stage_status_result.get("stage_status") if isinstance(stage_status_result, dict) else None

        items = []
        notes = []

        items.append(self._main_entry_gate(stage_status))
        items.append(self._runtime_contract_gate(stage_status, decision))
        items.append(self._runtime_behavior_gate(stage_status, decision))
        items.append(self._benchmark_scope_gate(stage_status))

        rank = {"hold": 0, "partial": 1, "open": 2}
        overall_gate = "open"
        for item in items:
            if rank[item.status] < rank[overall_gate]:
                overall_gate = item.status
            notes.extend(item.evidence)

        if overall_gate == "open":
            notes.append("Current tracked gates are open on the benchmark scope")
        elif overall_gate == "partial":
            notes.append("Current tracked gates are only partially open; keep promoting side lines before large merges")
        else:
            notes.append("At least one tracked gate is still on hold; avoid broad mainline convergence")

        return SemanticQualityReleaseGateSummary(
            overall_gate=overall_gate,
            items=items,
            notes=notes,
        )

    def _main_entry_gate(self, stage_status) -> SemanticQualityReleaseGateItem:
        if stage_status is None:
            return SemanticQualityReleaseGateItem(
                gate_key="main_entry_convergence",
                status="hold",
                rationale="missing stage status summary",
                unblock_actions=["Run stage status runner before evaluating main entry convergence"],
            )
        behavior_status = self._stage_status(stage_status, "runtime_semantic_behavior")
        contract_status = self._stage_status(stage_status, "runtime_semantic_contract")
        evidence = [f"runtime_semantic_contract={contract_status}", f"runtime_semantic_behavior={behavior_status}"]
        if contract_status == "stable" and behavior_status == "stable":
            return SemanticQualityReleaseGateItem(
                gate_key="main_entry_convergence",
                status="open",
                rationale="runtime semantic contract and behavior are stable on the benchmark scope",
                evidence=evidence,
            )
        if contract_status == "stable" and behavior_status == "partial":
            return SemanticQualityReleaseGateItem(
                gate_key="main_entry_convergence",
                status="partial",
                rationale="contracts are stable, but behavior is still partial so main entry convergence should remain selective",
                unblock_actions=["Promote helper-backed runtime behavior before broad main export convergence"],
                evidence=evidence,
            )
        return SemanticQualityReleaseGateItem(
            gate_key="main_entry_convergence",
            status="hold",
            rationale="runtime semantic contract is not yet stable enough for broad main entry convergence",
            unblock_actions=["Complete runtime semantic contract propagation before broad mainline convergence"],
            evidence=evidence,
        )

    def _runtime_contract_gate(self, stage_status, decision) -> SemanticQualityReleaseGateItem:
        if stage_status is None:
            return SemanticQualityReleaseGateItem(
                gate_key="runtime_contract_expansion",
                status="hold",
                rationale="missing stage status summary",
                unblock_actions=["Run stage status runner before evaluating runtime contract expansion"],
            )
        contract_status = self._stage_status(stage_status, "runtime_semantic_contract")
        primary_focus = getattr(decision, "primary_focus", "unknown") if decision is not None else "unknown"
        evidence = [f"runtime_semantic_contract={contract_status}", f"primary_focus={primary_focus}"]
        if contract_status == "stable":
            return SemanticQualityReleaseGateItem(
                gate_key="runtime_contract_expansion",
                status="open",
                rationale="runtime semantic contracts are stable enough to support behavior work on the current benchmark scope",
                evidence=evidence,
            )
        return SemanticQualityReleaseGateItem(
            gate_key="runtime_contract_expansion",
            status="partial",
            rationale="runtime semantic contracts exist but still need selective hardening",
            unblock_actions=["Keep OcrReadOptions and renderer propagation stable while expanding helper-backed usage"],
            evidence=evidence,
        )

    def _runtime_behavior_gate(self, stage_status, decision) -> SemanticQualityReleaseGateItem:
        if stage_status is None:
            return SemanticQualityReleaseGateItem(
                gate_key="runtime_behavior_promotion",
                status="hold",
                rationale="missing stage status summary",
                unblock_actions=["Run stage status runner before evaluating runtime behavior promotion"],
            )
        behavior_status = self._stage_status(stage_status, "runtime_semantic_behavior")
        primary_focus = getattr(decision, "primary_focus", "unknown") if decision is not None else "unknown"
        evidence = [f"runtime_semantic_behavior={behavior_status}", f"primary_focus={primary_focus}"]
        if behavior_status == "stable":
            return SemanticQualityReleaseGateItem(
                gate_key="runtime_behavior_promotion",
                status="open",
                rationale="runtime semantic behavior is stable enough for broader promotion on the current benchmark scope",
                evidence=evidence,
            )
        return SemanticQualityReleaseGateItem(
            gate_key="runtime_behavior_promotion",
            status="partial",
            rationale="runtime semantic behavior should advance, but only through helper-backed incremental implementations",
            unblock_actions=["Implement concrete kernel_size behavior and broaden excluded_number helper behavior"],
            evidence=evidence,
        )

    def _benchmark_scope_gate(self, stage_status) -> SemanticQualityReleaseGateItem:
        if stage_status is None:
            return SemanticQualityReleaseGateItem(
                gate_key="benchmark_scope_expansion",
                status="hold",
                rationale="missing stage status summary",
                unblock_actions=["Run stage status runner before evaluating benchmark scope expansion"],
            )
        parameter_status = self._stage_status(stage_status, "parameter_propagation")
        semantic_gap_status = self._stage_status(stage_status, "semantic_gap_management")
        evidence = [f"parameter_propagation={parameter_status}", f"semantic_gap_management={semantic_gap_status}"]
        if parameter_status == "stable" and semantic_gap_status == "stable":
            return SemanticQualityReleaseGateItem(
                gate_key="benchmark_scope_expansion",
                status="open",
                rationale="tracked parameter propagation and semantic gap management are stable enough to broaden the benchmark scope",
                evidence=evidence,
            )
        return SemanticQualityReleaseGateItem(
            gate_key="benchmark_scope_expansion",
            status="partial",
            rationale="benchmark scope can expand selectively, but only while keeping gap tracking visible",
            unblock_actions=["Expand benchmark cases only after preserving semantic gap visibility and parameter stability"],
            evidence=evidence,
        )

    def _stage_status(self, stage_status, stage_key: str) -> str:
        for item in getattr(stage_status, "items", []) or []:
            if getattr(item, "stage_key", "") == stage_key:
                return getattr(item, "status", "unstarted")
        return "unstarted"
