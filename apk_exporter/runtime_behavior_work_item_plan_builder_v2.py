from .runtime_behavior_work_item_plan_summary_v2 import RuntimeBehaviorWorkItemPlanSummaryV2, RuntimeBehaviorWorkItemV2


class RuntimeBehaviorWorkItemPlanBuilderV2:
    def build(self, stage_status_result: dict) -> RuntimeBehaviorWorkItemPlanSummaryV2:
        stage_status = stage_status_result.get("stage_status")
        if stage_status is None:
            return RuntimeBehaviorWorkItemPlanSummaryV2(
                overall_focus="rebuild-runtime-behavior-stage-status",
                notes=["Missing runtime behavior stage status summary; run runtime behavior stage status runner first"],
            )

        items = []
        notes = []
        overall_focus = "maintain-runtime-behavior-stability"

        for item in getattr(stage_status, "items", []) or []:
            stage_key = getattr(item, "stage_key", "")
            status = getattr(item, "status", "unstarted")
            if stage_key == "behavior_helper_usage" and status != "stable":
                overall_focus = "behavior-helper-adoption"
                items.append(
                    RuntimeBehaviorWorkItemV2(
                        title="Move remaining OCR paths onto behavior helper APIs",
                        priority="high",
                        rationale=getattr(item, "reason", "behavior helper usage is incomplete"),
                        target_files=[
                            "android_runtime_template/.../ocr/OcrSemanticBehaviorSupport.kt",
                            "task_exporters/main_export_quality_runtime_behavior_kotlin_step_renderer.py",
                        ],
                    )
                )
            if stage_key == "behavior_observability" and status != "stable":
                overall_focus = "behavior-observability-expansion"
                items.append(
                    RuntimeBehaviorWorkItemV2(
                        title="Expose remaining runtime behavior observability flags",
                        priority="high",
                        rationale=getattr(item, "reason", "behavior observability is incomplete"),
                        target_files=[
                            "android_runtime_template/.../ocr/OcrSemanticBehaviorResult.kt",
                            "android_runtime_template/.../ocr/OcrSemanticBehaviorSupport.kt",
                            "task_exporters/main_export_quality_runtime_behavior_kotlin_step_renderer.py",
                        ],
                    )
                )
            if stage_key == "behavior_gap_management" and status != "stable":
                if overall_focus == "maintain-runtime-behavior-stability":
                    overall_focus = "behavior-gap-reduction"
                items.append(
                    RuntimeBehaviorWorkItemV2(
                        title="Reduce runtime behavior backlog gaps",
                        priority="high",
                        rationale=getattr(item, "reason", "runtime behavior gaps remain unresolved"),
                        target_files=[
                            "apk_exporter/runtime_behavior_gap_backlog_builder.py",
                            "task_exporters/main_export_quality_runtime_behavior_kotlin_step_renderer.py",
                        ],
                    )
                )

        if not items:
            notes.append("No immediate high-priority runtime-behavior work items were derived; current tracked stages are stable on the benchmark scope")
        else:
            notes.append("Derived runtime-behavior work items prioritize observability before deeper OCR behavior implementation")

        return RuntimeBehaviorWorkItemPlanSummaryV2(
            overall_focus=overall_focus,
            items=items,
            notes=notes,
        )
