from .semantic_gap_backlog_summary import SemanticGapBacklogItem, SemanticGapBacklogSummary


class RuntimeBehaviorGapBacklogBuilder:
    def build(self, comparison_result: dict) -> SemanticGapBacklogSummary:
        runtime_behavior = comparison_result.get("runtime_behavior")
        runtime_semantic_behavior = comparison_result.get("runtime_semantic_behavior")
        if runtime_behavior is None:
            return SemanticGapBacklogSummary(project_root="", notes=["Missing runtime_behavior summary for backlog build"])

        items = []
        total_unresolved = 0

        expected_kernel = getattr(runtime_behavior, "expected_kernel_size_steps", 0)
        expected_excluded = getattr(runtime_behavior, "expected_excluded_number_steps", 0)

        items.append(
            self._build_item(
                gap_key="kernel_size_behavior_observability",
                priority="high",
                expected=expected_kernel,
                resolved=getattr(runtime_behavior, "kernel_hint_flag_count", 0),
                visibility=getattr(runtime_behavior, "kernel_hint_flag_count", 0),
                target_files=[
                    "android_runtime_template/.../ocr/OcrSemanticBehaviorSupport.kt",
                    "task_exporters/main_export_quality_runtime_behavior_kotlin_step_renderer.py",
                ],
                success_note="kernel_size behavior observability is present for current benchmark scope",
                gap_note="kernel_size behavior observability is still incomplete",
            )
        )

        items.append(
            self._build_item(
                gap_key="excluded_number_behavior_observability",
                priority="high",
                expected=expected_excluded,
                resolved=getattr(runtime_behavior, "excluded_filtered_flag_count", 0),
                visibility=getattr(runtime_behavior, "excluded_filtered_flag_count", 0),
                target_files=[
                    "android_runtime_template/.../ocr/OcrSemanticBehaviorSupport.kt",
                    "task_exporters/main_export_quality_runtime_behavior_kotlin_step_renderer.py",
                ],
                success_note="excluded_number behavior observability is present for current benchmark scope",
                gap_note="excluded_number behavior observability is still incomplete",
            )
        )

        items.append(
            self._build_item(
                gap_key="semantic_engine_usage_observability",
                priority="medium",
                expected=max(expected_kernel, expected_excluded),
                resolved=getattr(runtime_behavior, "used_semantic_engine_flag_count", 0),
                visibility=getattr(runtime_behavior, "used_semantic_engine_flag_count", 0),
                target_files=[
                    "android_runtime_template/.../ocr/OcrSemanticBehaviorSupport.kt",
                    "task_exporters/main_export_quality_runtime_behavior_kotlin_step_renderer.py",
                ],
                success_note="semantic engine usage observability is present for current benchmark scope",
                gap_note="semantic engine usage observability is still incomplete",
            )
        )

        notes = []
        for item in items:
            total_unresolved += item.unresolved_count
            notes.extend(item.notes)

        if runtime_semantic_behavior is not None:
            if getattr(runtime_behavior, "kernel_hint_flag_count", 0) > getattr(runtime_semantic_behavior, "kernel_hint_flag_count", 0):
                notes.append("Runtime-behavior line improves kernel_size behavior visibility compared with runtime-semantic line")
            if getattr(runtime_behavior, "excluded_filtered_flag_count", 0) > getattr(runtime_semantic_behavior, "excluded_filtered_flag_count", 0):
                notes.append("Runtime-behavior line improves excluded_number behavior visibility compared with runtime-semantic line")
            if getattr(runtime_behavior, "used_semantic_engine_flag_count", 0) > getattr(runtime_semantic_behavior, "used_semantic_engine_flag_count", 0):
                notes.append("Runtime-behavior line improves semantic engine usage visibility compared with runtime-semantic line")

        if total_unresolved == 0:
            notes.append("Current runtime-behavior benchmark scope has no unresolved tracked observability gaps")
        else:
            notes.append("Current runtime-behavior benchmark scope still contains unresolved observability gaps that should guide the next OCR behavior work items")

        return SemanticGapBacklogSummary(
            project_root=str(getattr(runtime_behavior, "project_root", "")),
            total_unresolved_gap_count=total_unresolved,
            items=items,
            notes=notes,
            files={
                "runtime_behavior_report": comparison_result.get("runtime_behavior_quality", {}).get("quality_report_path", "") if isinstance(comparison_result.get("runtime_behavior_quality"), dict) else "",
                "runtime_semantic_report": comparison_result.get("runtime_semantic_quality", {}).get("quality_report_path", "") if isinstance(comparison_result.get("runtime_semantic_quality"), dict) else "",
            },
        )

    def _build_item(self, gap_key: str, priority: str, expected: int, resolved: int, visibility: int, target_files: list[str], success_note: str, gap_note: str) -> SemanticGapBacklogItem:
        unresolved = max(expected - resolved, 0)
        notes = []
        if expected == 0:
            notes.append(f"No benchmark steps currently require {gap_key}")
        elif unresolved == 0:
            notes.append(success_note)
        else:
            notes.append(gap_note)
        if visibility > 0:
            notes.append(f"Current generated code preserves {gap_key} visibility for {visibility} step(s)")
        return SemanticGapBacklogItem(
            gap_key=gap_key,
            priority=priority,
            expected_count=expected,
            resolved_count=resolved,
            unresolved_count=unresolved,
            visibility_count=visibility,
            target_files=target_files,
            notes=notes,
        )
