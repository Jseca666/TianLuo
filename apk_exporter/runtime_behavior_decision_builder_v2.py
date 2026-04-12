from .runtime_behavior_decision_summary_v2 import RuntimeBehaviorDecisionItemV2, RuntimeBehaviorDecisionSummaryV2


class RuntimeBehaviorDecisionBuilderV2:
    def build(self, plan_result: dict) -> RuntimeBehaviorDecisionSummaryV2:
        plan = plan_result.get("plan")
        stage_status_result = plan_result.get("stage_status_result", {}) if isinstance(plan_result, dict) else {}
        stage_status = stage_status_result.get("stage_status") if isinstance(stage_status_result, dict) else None

        if plan is None:
            return RuntimeBehaviorDecisionSummaryV2(
                primary_focus="rebuild-runtime-behavior-plan",
                secondary_focus="unknown",
                notes=["Missing runtime behavior work item plan; run runtime behavior work item plan runner first"],
            )

        items = []
        notes = []
        freeze_recommendations = []
        overall_focus = getattr(plan, "overall_focus", "maintain-runtime-behavior-stability")
        primary_focus = overall_focus
        secondary_focus = "behavior-gap-reduction"

        work_item_titles = [getattr(item, "title", "") for item in getattr(plan, "items", []) or []]

        if overall_focus == "behavior-observability-expansion":
            secondary_focus = "behavior-helper-adoption"
        elif overall_focus == "behavior-helper-adoption":
            secondary_focus = "behavior-gap-reduction"

        if any("observability" in title.lower() for title in work_item_titles):
            items.append(
                RuntimeBehaviorDecisionItemV2(
                    lane="behavior_observability",
                    priority="high",
                    decision="advance",
                    rationale="Behavior observability remains the highest-value lane before deeper OCR behavior implementation.",
                    related_work_items=[title for title in work_item_titles if "observability" in title.lower()],
                )
            )
        if any("helper" in title.lower() for title in work_item_titles):
            items.append(
                RuntimeBehaviorDecisionItemV2(
                    lane="behavior_helper_usage",
                    priority="medium",
                    decision="maintain",
                    rationale="Helper-backed paths should keep expanding, but only behind observable behavior signals.",
                    related_work_items=[title for title in work_item_titles if "helper" in title.lower()],
                )
            )

        if stage_status is not None:
            for item in getattr(stage_status, "items", []) or []:
                stage_key = getattr(item, "stage_key", "")
                status = getattr(item, "status", "unstarted")
                if stage_key == "behavior_helper_usage" and status == "stable":
                    freeze_recommendations.append("Avoid large refactors to helper entry points unless they unlock deeper behavior observability")
                if stage_key == "behavior_observability" and status == "partial":
                    notes.append("Behavior observability is still partial, so behavior work should favor additive flags over signature churn")

        if not items:
            items.append(
                RuntimeBehaviorDecisionItemV2(
                    lane="maintenance",
                    priority="medium",
                    decision="hold-steady",
                    rationale="No urgent runtime-behavior lane was derived beyond maintaining current benchmark-backed stability.",
                    related_work_items=work_item_titles,
                )
            )

        notes.append("Runtime-behavior decision summary is derived from stage status and work item plan.")
        return RuntimeBehaviorDecisionSummaryV2(
            primary_focus=primary_focus,
            secondary_focus=secondary_focus,
            freeze_recommendations=freeze_recommendations,
            items=items,
            notes=notes,
        )
