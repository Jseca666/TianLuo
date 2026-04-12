from .semantic_quality_decision_summary import SemanticQualityDecisionItem, SemanticQualityDecisionSummary


class SemanticQualityDecisionBuilder:
    def build(self, plan_result: dict) -> SemanticQualityDecisionSummary:
        plan = plan_result.get("plan")
        stage_status_result = plan_result.get("stage_status_result", {})
        stage_status = stage_status_result.get("stage_status") if isinstance(stage_status_result, dict) else None

        if plan is None:
            return SemanticQualityDecisionSummary(
                primary_focus="rebuild-plan",
                secondary_focus="unknown",
                notes=["Missing work item plan; run semantic quality work item plan runner first"],
            )

        items = []
        notes = []
        freeze_recommendations = []

        overall_focus = getattr(plan, "overall_focus", "maintain-stable-state")
        primary_focus = overall_focus
        secondary_focus = "benchmark-expansion"

        work_item_titles = [getattr(item, "title", "") for item in getattr(plan, "items", []) or []]

        if overall_focus == "runtime-behavior-implementation":
            secondary_focus = "runtime-contract-completion"
        elif overall_focus == "runtime-contract-completion":
            secondary_focus = "parameter-and-runtime-gap-reduction"
        elif overall_focus == "semantic-gap-reduction":
            secondary_focus = "parameter-and-runtime-gap-reduction"

        if any("runtime semantic behavior" in title.lower() or "ocr runtime semantic behavior" in title.lower() for title in work_item_titles):
            items.append(
                SemanticQualityDecisionItem(
                    lane="runtime_behavior",
                    priority="high",
                    decision="advance",
                    rationale="Runtime semantic behavior remains the highest-value lane after contracts are visible but still incomplete.",
                    related_work_items=[title for title in work_item_titles if "runtime" in title.lower()],
                )
            )
        if any("parameter" in title.lower() for title in work_item_titles):
            items.append(
                SemanticQualityDecisionItem(
                    lane="parameter_propagation",
                    priority="medium",
                    decision="maintain",
                    rationale="Parameter propagation should keep improving, but it is no longer the only blocker once runtime-semantic work has begun.",
                    related_work_items=[title for title in work_item_titles if "parameter" in title.lower()],
                )
            )
        if any("gap backlog" in note.lower() for note in getattr(plan, "notes", []) or []):
            notes.append("Backlog health should remain visible while implementation work advances.")

        if stage_status is not None:
            for item in getattr(stage_status, "items", []) or []:
                stage_key = getattr(item, "stage_key", "")
                status = getattr(item, "status", "unstarted")
                if stage_key == "parameter_propagation" and status == "stable":
                    freeze_recommendations.append("Avoid large parameter-mapping refactors unless they unblock runtime behavior work")
                if stage_key == "runtime_semantic_contract" and status == "stable":
                    freeze_recommendations.append("Keep runtime-semantic OCR contracts stable while implementing behavior behind them")
                if stage_key == "runtime_semantic_behavior" and status == "partial":
                    notes.append("Runtime semantic behavior is still partial, so new OCR semantics should prefer helper-backed paths over direct expansion")

        if not items:
            items.append(
                SemanticQualityDecisionItem(
                    lane="maintenance",
                    priority="medium",
                    decision="hold-steady",
                    rationale="No urgent lane was derived beyond maintaining the current benchmark-backed stability.",
                    related_work_items=work_item_titles,
                )
            )

        notes.append("Decision summary is derived from stage status and work item plan, not from manual judgment alone.")
        return SemanticQualityDecisionSummary(
            primary_focus=primary_focus,
            secondary_focus=secondary_focus,
            freeze_recommendations=freeze_recommendations,
            items=items,
            notes=notes,
        )
