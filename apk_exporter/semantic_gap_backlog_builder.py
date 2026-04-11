from .semantic_gap_backlog_summary import SemanticGapBacklogItem, SemanticGapBacklogSummary


class SemanticGapBacklogBuilder:
    def build(self, comparison_result: dict) -> SemanticGapBacklogSummary:
        quality_semantic = comparison_result.get("quality_semantic")
        if quality_semantic is None:
            return SemanticGapBacklogSummary(project_root="", notes=["Missing quality_semantic summary for backlog build"])

        items = []
        total_unresolved = 0

        items.append(
            self._build_item(
                gap_key="threshold_propagation",
                priority="high",
                expected=getattr(quality_semantic, "expected_threshold_steps", 0),
                resolved=getattr(quality_semantic, "propagated_threshold_count", 0),
                visibility=getattr(quality_semantic, "propagated_threshold_count", 0),
                target_files=[
                    "task_exporters/*step_mapper.py",
                    "task_exporters/*kotlin_step_renderer.py",
                ],
                success_note="Threshold parameters are already propagated for current benchmark scope",
                gap_note="Threshold propagation is still incomplete for current benchmark scope",
            )
        )

        items.append(
            self._build_item(
                gap_key="mask_name_propagation",
                priority="high",
                expected=getattr(quality_semantic, "expected_mask_steps", 0),
                resolved=getattr(quality_semantic, "propagated_mask_name_count", 0),
                visibility=getattr(quality_semantic, "propagated_mask_name_count", 0),
                target_files=[
                    "task_exporters/*step_mapper.py",
                    "task_exporters/*kotlin_step_renderer.py",
                    "android_runtime_template/runtime/vision/TemplateMatcher.kt",
                    "android_runtime_template/runtime/ocr/OcrEngine.kt",
                ],
                success_note="mask_name parameters are already propagated for current benchmark scope",
                gap_note="mask_name propagation is still incomplete for current benchmark scope",
            )
        )

        items.append(
            self._build_item(
                gap_key="use_color_propagation",
                priority="high",
                expected=getattr(quality_semantic, "expected_use_color_steps", 0),
                resolved=getattr(quality_semantic, "propagated_use_color_count", 0),
                visibility=getattr(quality_semantic, "propagated_use_color_count", 0),
                target_files=[
                    "task_exporters/*step_mapper.py",
                    "task_exporters/*kotlin_step_renderer.py",
                    "android_runtime_template/runtime/vision/TemplateMatcher.kt",
                ],
                success_note="use_color parameters are already propagated for current benchmark scope",
                gap_note="use_color propagation is still incomplete for current benchmark scope",
            )
        )

        items.append(
            self._build_item(
                gap_key="kernel_size_runtime_support",
                priority="medium",
                expected=getattr(quality_semantic, "expected_kernel_size_steps", 0),
                resolved=0,
                visibility=getattr(quality_semantic, "semantic_kernel_note_count", 0),
                target_files=[
                    "android_runtime_template/runtime/ocr/OcrEngine.kt",
                    "task_exporters/*kotlin_step_renderer.py",
                    "apk_exporter/semantic_parameter_readiness_analyzer.py",
                ],
                success_note="kernel_size runtime support is already complete for current benchmark scope",
                gap_note="kernel_size still lacks runtime support and is currently tracked by semantic notes",
            )
        )

        items.append(
            self._build_item(
                gap_key="excluded_number_runtime_support",
                priority="medium",
                expected=getattr(quality_semantic, "expected_excluded_number_steps", 0),
                resolved=0,
                visibility=getattr(quality_semantic, "semantic_excluded_number_note_count", 0),
                target_files=[
                    "android_runtime_template/runtime/ocr/OcrEngine.kt",
                    "task_exporters/*kotlin_step_renderer.py",
                    "apk_exporter/semantic_parameter_readiness_analyzer.py",
                ],
                success_note="excluded_number runtime support is already complete for current benchmark scope",
                gap_note="excluded_number still lacks runtime support and is currently tracked by semantic notes",
            )
        )

        notes = []
        for item in items:
            total_unresolved += item.unresolved_count
            notes.extend(item.notes)

        if total_unresolved == 0:
            notes.append("Current semantic benchmark scope has no unresolved tracked semantic gaps")
        else:
            notes.append("Current semantic benchmark scope still contains unresolved semantic gaps that should drive the next runtime work items")

        return SemanticGapBacklogSummary(
            project_root=str(getattr(quality_semantic, "project_root", "")),
            total_unresolved_gap_count=total_unresolved,
            items=items,
            notes=notes,
            files={
                "semantic_quality_report": comparison_result.get("semantic_quality", {}).get("quality_report_path", "") if isinstance(comparison_result.get("semantic_quality"), dict) else "",
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
        if visibility > 0 and unresolved > 0:
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
