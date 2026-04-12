from .semantic_quality_stage_status_summary import SemanticQualityStageStatusItem, SemanticQualityStageStatusSummary


class SemanticQualityStageStatusBuilder:
    def build(self, suite_result: dict) -> SemanticQualityStageStatusSummary:
        items = []
        notes = []

        parameter_comparison = suite_result.get("parameter_comparison", {})
        runtime_comparison = suite_result.get("runtime_semantic_comparison", {})
        semantic_gap = suite_result.get("semantic_gap_backlog", {}).get("backlog") if isinstance(suite_result.get("semantic_gap_backlog"), dict) else None
        runtime_gap = suite_result.get("runtime_semantic_gap_backlog", {}).get("backlog") if isinstance(suite_result.get("runtime_semantic_gap_backlog"), dict) else None

        quality_semantic = parameter_comparison.get("quality_semantic") if isinstance(parameter_comparison, dict) else None
        runtime_semantic_runtime = runtime_comparison.get("runtime_semantic_runtime") if isinstance(runtime_comparison, dict) else None

        items.append(self._parameter_stage(quality_semantic))
        items.append(self._semantic_gap_stage(semantic_gap))
        items.append(self._runtime_contract_stage(runtime_semantic_runtime))
        items.append(self._runtime_behavior_stage(runtime_gap))

        status_rank = {"unstarted": 0, "partial": 1, "stable": 2}
        overall_status = "stable"
        for item in items:
            if status_rank[item.status] < status_rank[overall_status]:
                overall_status = item.status
            notes.extend(item.evidence)

        if overall_status == "stable":
            notes.append("Current semantic quality suite indicates the tracked stages are stable on the benchmark scope")
        elif overall_status == "partial":
            notes.append("Current semantic quality suite indicates the project is in a partial transition state across tracked stages")
        else:
            notes.append("Current semantic quality suite indicates at least one tracked stage has not started on the benchmark scope")

        files = {
            "parameter_suite": "parameter_comparison",
            "runtime_suite": "runtime_semantic_comparison",
            "semantic_gap_backlog": "semantic_gap_backlog",
            "runtime_gap_backlog": "runtime_semantic_gap_backlog",
        }
        return SemanticQualityStageStatusSummary(
            overall_status=overall_status,
            items=items,
            notes=notes,
            files=files,
        )

    def _parameter_stage(self, quality_semantic) -> SemanticQualityStageStatusItem:
        evidence = []
        next_actions = []
        if quality_semantic is None:
            return SemanticQualityStageStatusItem(
                stage_key="parameter_propagation",
                status="unstarted",
                reason="missing semantic parameter readiness summary",
                next_actions=["Run semantic parameter comparison workflow before judging parameter propagation stage"],
            )
        expected = (
            getattr(quality_semantic, "expected_threshold_steps", 0)
            + getattr(quality_semantic, "expected_mask_steps", 0)
            + getattr(quality_semantic, "expected_use_color_steps", 0)
        )
        resolved = (
            getattr(quality_semantic, "propagated_threshold_count", 0)
            + getattr(quality_semantic, "propagated_mask_name_count", 0)
            + getattr(quality_semantic, "propagated_use_color_count", 0)
        )
        evidence.append(f"expected parameter propagation count: {expected}")
        evidence.append(f"resolved parameter propagation count: {resolved}")
        if expected == 0:
            status = "unstarted"
            reason = "no semantic benchmark steps currently require tracked propagation parameters"
            next_actions.append("Add benchmark tasks with tracked propagation parameters before judging this stage")
        elif resolved >= expected:
            status = "stable"
            reason = "tracked parameter propagation is covered for the current benchmark scope"
            next_actions.append("Expand benchmark scope to additional task patterns and keep propagation stable")
        else:
            status = "partial"
            reason = "tracked parameter propagation is only partially covered"
            next_actions.append("Continue improving step mapper and renderer parameter normalization")
        return SemanticQualityStageStatusItem(
            stage_key="parameter_propagation",
            status=status,
            reason=reason,
            evidence=evidence,
            next_actions=next_actions,
        )

    def _semantic_gap_stage(self, semantic_gap) -> SemanticQualityStageStatusItem:
        evidence = []
        next_actions = []
        if semantic_gap is None:
            return SemanticQualityStageStatusItem(
                stage_key="semantic_gap_management",
                status="unstarted",
                reason="missing semantic gap backlog summary",
                next_actions=["Run semantic gap backlog workflow before judging semantic gap management stage"],
            )
        unresolved = getattr(semantic_gap, "total_unresolved_gap_count", 0)
        evidence.append(f"semantic unresolved gap count: {unresolved}")
        if unresolved == 0:
            status = "stable"
            reason = "tracked semantic gaps are fully resolved for the current benchmark scope"
            next_actions.append("Keep semantic gap backlog empty while expanding benchmark coverage")
        else:
            status = "partial"
            reason = "tracked semantic gaps are visible and managed, but not fully resolved"
            next_actions.append("Use semantic gap backlog priorities to drive the next parameter and OCR work items")
        return SemanticQualityStageStatusItem(
            stage_key="semantic_gap_management",
            status=status,
            reason=reason,
            evidence=evidence,
            next_actions=next_actions,
        )

    def _runtime_contract_stage(self, runtime_semantic_runtime) -> SemanticQualityStageStatusItem:
        evidence = []
        next_actions = []
        if runtime_semantic_runtime is None:
            return SemanticQualityStageStatusItem(
                stage_key="runtime_semantic_contract",
                status="unstarted",
                reason="missing runtime semantic readiness summary",
                next_actions=["Run runtime semantic comparison workflow before judging runtime semantic contract stage"],
            )
        expected = (
            getattr(runtime_semantic_runtime, "expected_kernel_size_steps", 0)
            + getattr(runtime_semantic_runtime, "expected_excluded_number_steps", 0)
        )
        resolved = (
            getattr(runtime_semantic_runtime, "kernel_size_option_count", 0)
            + getattr(runtime_semantic_runtime, "excluded_number_option_count", 0)
        )
        evidence.append(f"expected runtime contract count: {expected}")
        evidence.append(f"resolved runtime contract count: {resolved}")
        if expected == 0:
            status = "unstarted"
            reason = "no benchmark steps currently require tracked runtime semantic OCR options"
            next_actions.append("Add benchmark steps with kernel_size or excluded_number before judging this stage")
        elif resolved >= expected:
            status = "stable"
            reason = "runtime semantic contracts are present in generated code for the current benchmark scope"
            next_actions.append("Move focus from contract propagation to runtime behavior implementation")
        else:
            status = "partial"
            reason = "runtime semantic contracts are only partially propagated"
            next_actions.append("Continue wiring OcrReadOptions through runtime-semantic renderer paths")
        return SemanticQualityStageStatusItem(
            stage_key="runtime_semantic_contract",
            status=status,
            reason=reason,
            evidence=evidence,
            next_actions=next_actions,
        )

    def _runtime_behavior_stage(self, runtime_gap) -> SemanticQualityStageStatusItem:
        evidence = []
        next_actions = []
        if runtime_gap is None:
            return SemanticQualityStageStatusItem(
                stage_key="runtime_semantic_behavior",
                status="unstarted",
                reason="missing runtime semantic gap backlog summary",
                next_actions=["Run runtime semantic gap backlog workflow before judging runtime semantic behavior stage"],
            )
        unresolved_behavior = 0
        for item in getattr(runtime_gap, "items", []) or []:
            gap_key = getattr(item, "gap_key", "")
            if gap_key.endswith("_runtime_behavior"):
                unresolved_behavior += getattr(item, "unresolved_count", 0)
        evidence.append(f"runtime behavior unresolved gap count: {unresolved_behavior}")
        if unresolved_behavior == 0:
            status = "stable"
            reason = "tracked runtime semantic behaviors are resolved for the current benchmark scope"
            next_actions.append("Broaden runtime behavior benchmark coverage beyond the current OCR semantic paths")
        else:
            status = "partial"
            reason = "runtime semantic behavior is visible but not fully implemented"
            next_actions.append("Implement concrete OCR runtime behavior for kernel_size and broaden excluded_number handling")
        return SemanticQualityStageStatusItem(
            stage_key="runtime_semantic_behavior",
            status=status,
            reason=reason,
            evidence=evidence,
            next_actions=next_actions,
        )
