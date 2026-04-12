from .semantic_quality_work_item_plan_summary import SemanticQualityWorkItem, SemanticQualityWorkItemPlanSummary


class SemanticQualityWorkItemPlanBuilder:
    def build(self, stage_status_result: dict) -> SemanticQualityWorkItemPlanSummary:
        stage_status = stage_status_result.get("stage_status")
        if stage_status is None:
            return SemanticQualityWorkItemPlanSummary(
                overall_focus="rebuild-stage-status",
                notes=["Missing stage_status summary; run semantic quality stage status runner first"],
            )

        items = []
        notes = []
        overall_focus = "maintain-stable-state"

        for item in getattr(stage_status, "items", []) or []:
            stage_key = getattr(item, "stage_key", "")
            status = getattr(item, "status", "unstarted")
            if stage_key == "parameter_propagation" and status != "stable":
                overall_focus = "parameter-and-runtime-gap-reduction"
                items.append(
                    SemanticQualityWorkItem(
                        title="Harden parameter normalization and propagation",
                        priority="high",
                        rationale=getattr(item, "reason", "parameter propagation is incomplete"),
                        target_files=[
                            "task_exporters/*step_mapper.py",
                            "task_exporters/*kotlin_step_renderer.py",
                        ],
                    )
                )
            if stage_key == "semantic_gap_management" and status != "stable":
                if overall_focus == "maintain-stable-state":
                    overall_focus = "semantic-gap-reduction"
                items.append(
                    SemanticQualityWorkItem(
                        title="Reduce unresolved semantic gap backlog",
                        priority="high",
                        rationale=getattr(item, "reason", "semantic gaps remain unresolved"),
                        target_files=[
                            "apk_exporter/semantic_gap_backlog_builder.py",
                            "task_exporters/*step_mapper.py",
                            "task_exporters/*kotlin_step_renderer.py",
                        ],
                    )
                )
            if stage_key == "runtime_semantic_contract" and status != "stable":
                overall_focus = "runtime-contract-completion"
                items.append(
                    SemanticQualityWorkItem(
                        title="Complete runtime-semantic OCR option propagation",
                        priority="high",
                        rationale=getattr(item, "reason", "runtime semantic contracts are incomplete"),
                        target_files=[
                            "android_runtime_template/.../ocr/OcrReadOptions.kt",
                            "task_exporters/main_export_quality_runtime_semantic_kotlin_step_renderer.py",
                        ],
                        depends_on=["Harden parameter normalization and propagation"],
                    )
                )
            if stage_key == "runtime_semantic_behavior" and status != "stable":
                overall_focus = "runtime-behavior-implementation"
                items.append(
                    SemanticQualityWorkItem(
                        title="Implement concrete OCR runtime semantic behavior",
                        priority="high",
                        rationale=getattr(item, "reason", "runtime semantic behavior is incomplete"),
                        target_files=[
                            "android_runtime_template/.../ocr/OcrSemanticSupport.kt",
                            "android_runtime_template/.../ocr/SemanticOcrEngine.kt",
                            "runtime OCR implementation classes",
                        ],
                        depends_on=["Complete runtime-semantic OCR option propagation"],
                    )
                )

        if not items:
            notes.append("No immediate high-priority work items were derived; current tracked stages are stable on the benchmark scope")
        else:
            notes.append("Derived work items are ordered to reduce semantic gaps before broadening benchmark scope")

        return SemanticQualityWorkItemPlanSummary(
            overall_focus=overall_focus,
            items=items,
            notes=notes,
        )
