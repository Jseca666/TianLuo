from .runtime_behavior_stage_status_summary import RuntimeBehaviorStageStatusItem, RuntimeBehaviorStageStatusSummary


class RuntimeBehaviorStageStatusBuilderV2:
    def build(self, suite_result: dict) -> RuntimeBehaviorStageStatusSummary:
        comparison = suite_result.get("comparison", {})
        backlog_result = suite_result.get("backlog", {})
        runtime_behavior = comparison.get("runtime_behavior") if isinstance(comparison, dict) else None
        backlog = backlog_result.get("backlog") if isinstance(backlog_result, dict) else None

        items = [
            self._helper_usage(runtime_behavior),
            self._observability(runtime_behavior),
            self._gap_management(backlog),
        ]

        rank = {"unstarted": 0, "partial": 1, "stable": 2}
        overall_status = "stable"
        notes = []
        for item in items:
            if rank[item.status] < rank[overall_status]:
                overall_status = item.status
            notes.extend(item.evidence)

        if overall_status == "stable":
            notes.append("Runtime-behavior tracked stages are stable on current benchmark scope")
        elif overall_status == "partial":
            notes.append("Runtime-behavior tracked stages are partial on current benchmark scope")
        else:
            notes.append("Runtime-behavior tracked stages are not started on current benchmark scope")

        return RuntimeBehaviorStageStatusSummary(
            overall_status=overall_status,
            items=items,
            notes=notes,
        )

    def _helper_usage(self, runtime_behavior):
        if runtime_behavior is None:
            return RuntimeBehaviorStageStatusItem(
                stage_key="behavior_helper_usage",
                status="unstarted",
                reason="missing runtime behavior readiness summary",
                next_actions=["Run runtime behavior suite first"],
            )
        helper_count = getattr(runtime_behavior, "read_text_behavior_count", 0) + getattr(runtime_behavior, "read_number_behavior_count", 0)
        evidence = [f"behavior helper call count: {helper_count}"]
        if helper_count == 0:
            return RuntimeBehaviorStageStatusItem(
                stage_key="behavior_helper_usage",
                status="unstarted",
                reason="behavior helper calls are absent",
                evidence=evidence,
                next_actions=["Keep moving OCR paths onto behavior helper APIs"],
            )
        return RuntimeBehaviorStageStatusItem(
            stage_key="behavior_helper_usage",
            status="stable",
            reason="behavior helper calls are present",
            evidence=evidence,
            next_actions=["Preserve helper-backed paths while broadening coverage"],
        )

    def _observability(self, runtime_behavior):
        if runtime_behavior is None:
            return RuntimeBehaviorStageStatusItem(
                stage_key="behavior_observability",
                status="unstarted",
                reason="missing runtime behavior readiness summary",
                next_actions=["Run runtime behavior suite first"],
            )
        expected = max(
            getattr(runtime_behavior, "expected_kernel_size_steps", 0),
            getattr(runtime_behavior, "expected_excluded_number_steps", 0),
        )
        resolved = min(
            getattr(runtime_behavior, "used_semantic_engine_flag_count", 0),
            getattr(runtime_behavior, "kernel_hint_flag_count", 0) + getattr(runtime_behavior, "excluded_filtered_flag_count", 0),
        )
        evidence = [
            f"expected behavior observability count: {expected}",
            f"resolved behavior observability count: {resolved}",
        ]
        if expected == 0:
            return RuntimeBehaviorStageStatusItem(
                stage_key="behavior_observability",
                status="unstarted",
                reason="no current benchmark steps require behavior observability",
                evidence=evidence,
                next_actions=["Add benchmark steps with kernel_size or excluded_number"],
            )
        if resolved >= expected:
            return RuntimeBehaviorStageStatusItem(
                stage_key="behavior_observability",
                status="stable",
                reason="behavior observability is covered",
                evidence=evidence,
                next_actions=["Broaden benchmark coverage while keeping flags visible"],
            )
        return RuntimeBehaviorStageStatusItem(
            stage_key="behavior_observability",
            status="partial",
            reason="behavior observability is only partially covered",
            evidence=evidence,
            next_actions=["Continue exposing behavior flags in generated code"],
        )

    def _gap_management(self, backlog):
        if backlog is None:
            return RuntimeBehaviorStageStatusItem(
                stage_key="behavior_gap_management",
                status="unstarted",
                reason="missing runtime behavior gap backlog summary",
                next_actions=["Run runtime behavior backlog workflow first"],
            )
        unresolved = getattr(backlog, "total_unresolved_gap_count", 0)
        evidence = [f"runtime behavior unresolved gap count: {unresolved}"]
        if unresolved == 0:
            return RuntimeBehaviorStageStatusItem(
                stage_key="behavior_gap_management",
                status="stable",
                reason="runtime behavior gaps are resolved",
                evidence=evidence,
                next_actions=["Expand suite coverage while keeping backlog empty"],
            )
        return RuntimeBehaviorStageStatusItem(
            stage_key="behavior_gap_management",
            status="partial",
            reason="runtime behavior gaps remain visible",
            evidence=evidence,
            next_actions=["Use runtime behavior backlog to drive helper and renderer work"],
        )
