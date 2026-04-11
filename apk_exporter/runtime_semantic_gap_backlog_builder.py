from .semantic_gap_backlog_summary import SemanticGapBacklogItem, SemanticGapBacklogSummary


class RuntimeSemanticGapBacklogBuilder:
    def build(self, comparison_result: dict) -> SemanticGapBacklogSummary:
        runtime_semantic_runtime = comparison_result.get("runtime_semantic_runtime")
        semantic_runtime = comparison_result.get("semantic_runtime")
        if runtime_semantic_runtime is None:
            return SemanticGapBacklogSummary(project_root="", notes=["Missing runtime_semantic_runtime summary for backlog build"])

        items = []
        total_unresolved = 0

        items.append(
            self._build_item(
                gap_key="kernel_size_runtime_contract",
                priority="high",
                expected=getattr(runtime_semantic_runtime, "expected_kernel_size_steps", 0),
                resolved=getattr(runtime_semantic_runtime, "kernel_size_option_count", 0),
                visibility=getattr(runtime_semantic_runtime, "kernel_size_option_count", 0),
                target_files=[
                    "android_runtime_template/.../ocr/OcrReadOptions.kt",
                    "android_runtime_template/.../ocr/SemanticOcrEngine.kt",
                    "task_exporters/main_export_quality_runtime_semantic_kotlin_step_renderer.py",
                ],
                success_note="kernel_size now has a runtime option contract in generated code for current benchmark scope",
                gap_note="kernel_size runtime option contract is still incomplete for current benchmark scope",
            )
        )

        items.append(
            self._build_item(
                gap_key="excluded_number_runtime_contract",
                priority="high",
                expected=getattr(runtime_semantic_runtime, "expected_excluded_number_steps", 0),
                resolved=getattr(runtime_semantic_runtime, "excluded_number_option_count", 0),
                visibility=getattr(runtime_semantic_runtime, "excluded_number_option_count", 0),
                target_files=[
                    "android_runtime_template/.../ocr/OcrReadOptions.kt",
                    "android_runtime_template/.../ocr/SemanticOcrEngine.kt",
                    "task_exporters/main_export_quality_runtime_semantic_kotlin_step_renderer.py",
                ],
                success_note="excluded_number now has a runtime option contract in generated code for current benchmark scope",
                gap_note="excluded_number runtime option contract is still incomplete for current benchmark scope",
            )
        )

        excluded_behavior_resolved = min(
            getattr(runtime_semantic_runtime, "expected_excluded_number_steps", 0),
            getattr(runtime_semantic_runtime, "excluded_number_option_count", 0),
            getattr(runtime_semantic_runtime, "read_number_semantic_count", 0),
        )
        items.append(
            self._build_item(
                gap_key="excluded_number_runtime_behavior",
                priority="high",
                expected=getattr(runtime_semantic_runtime, "expected_excluded_number_steps", 0),
                resolved=excluded_behavior_resolved,
                visibility=getattr(runtime_semantic_runtime, "read_number_semantic_count", 0),
                target_files=[
                    "android_runtime_template/.../ocr/OcrSemanticSupport.kt",
                    "task_exporters/main_export_quality_runtime_semantic_kotlin_step_renderer.py",
                ],
                success_note="excluded_number now has runtime helper behavior coverage for current benchmark scope",
                gap_note="excluded_number runtime behavior is still only partially covered",
            )
        )

        items.append(
            self._build_item(
                gap_key="kernel_size_runtime_behavior",
                priority="medium",
                expected=getattr(runtime_semantic_runtime, "expected_kernel_size_steps", 0),
                resolved=0,
                visibility=getattr(runtime_semantic_runtime, "read_text_semantic_count", 0) + getattr(runtime_semantic_runtime, "read_number_semantic_count", 0),
                target_files=[
                    "android_runtime_template/.../ocr/SemanticOcrEngine.kt",
                    "android_runtime_template/.../ocr/OcrSemanticSupport.kt",
                    "runtime OCR implementation classes",
                ],
                success_note="kernel_size runtime behavior is already fully implemented for current benchmark scope",
                gap_note="kernel_size currently has contract visibility but still lacks concrete runtime behavior",
            )
        )

        notes = []
        for item in items:
            total_unresolved += item.unresolved_count
            notes.extend(item.notes)

        if semantic_runtime is not None and runtime_semantic_runtime is not None:
            if getattr(runtime_semantic_runtime, "kernel_size_option_count", 0) > getattr(semantic_runtime, "kernel_size_option_count", 0):
                notes.append("Runtime-semantic line moves kernel_size from note-only visibility into runtime option propagation")
            if getattr(runtime_semantic_runtime, "excluded_number_option_count", 0) > getattr(semantic_runtime, "excluded_number_option_count", 0):
                notes.append("Runtime-semantic line moves excluded_number from note-only visibility into runtime option propagation")
            if getattr(runtime_semantic_runtime, "read_number_semantic_count", 0) > getattr(semantic_runtime, "read_number_semantic_count", 0):
                notes.append("Runtime-semantic line adds runtime helper behavior entry points for numeric OCR")

        if total_unresolved == 0:
            notes.append("Current runtime-semantic benchmark scope has no unresolved tracked gaps")
        else:
            notes.append("Current runtime-semantic benchmark scope still contains unresolved gaps that should drive the next OCR runtime work items")

        return SemanticGapBacklogSummary(
            project_root=str(getattr(runtime_semantic_runtime, "project_root", "")),
            total_unresolved_gap_count=total_unresolved,
            items=items,
            notes=notes,
            files={
                "runtime_semantic_report": comparison_result.get("runtime_semantic_quality", {}).get("quality_report_path", "") if isinstance(comparison_result.get("runtime_semantic_quality"), dict) else "",
                "semantic_report": comparison_result.get("semantic_quality", {}).get("quality_report_path", "") if isinstance(comparison_result.get("semantic_quality"), dict) else "",
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
