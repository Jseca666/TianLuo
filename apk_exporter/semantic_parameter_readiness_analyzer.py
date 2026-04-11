from pathlib import Path

from .semantic_parameter_readiness_summary import SemanticParameterReadinessSummary


class SemanticParameterReadinessAnalyzer:
    def analyze(self, task_specs: list[dict], export_payload: dict) -> SemanticParameterReadinessSummary:
        project_root = self._project_root(export_payload)
        task_files = self._task_files(export_payload)
        task_ids = list(task_files.keys())

        expected_threshold_steps = 0
        expected_mask_steps = 0
        expected_use_color_steps = 0
        expected_kernel_size_steps = 0
        expected_excluded_number_steps = 0

        for spec in task_specs:
            for call in spec.get("api_calls", []) or []:
                params = dict(call.get("params", {}) or {})
                if self._has_any(params, ["threshold", "similarity_threshold", "match_threshold"]):
                    expected_threshold_steps += 1
                if self._has_any(params, ["mask_name", "maskName", "mask"]):
                    expected_mask_steps += 1
                if self._has_any(params, ["use_color", "useColor"]):
                    expected_use_color_steps += 1
                if params.get("kernel_size") is not None:
                    expected_kernel_size_steps += 1
                if params.get("excluded_number") is not None:
                    expected_excluded_number_steps += 1

        propagated_threshold_count = 0
        propagated_mask_name_count = 0
        propagated_use_color_count = 0
        semantic_kernel_note_count = 0
        semantic_excluded_number_note_count = 0
        task_file_counts = {}
        notes = []

        for task_id, file_path in task_files.items():
            path = Path(file_path)
            if not path.exists():
                notes.append(f"Task file missing for semantic readiness analysis: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            threshold_count = text.count("threshold = ")
            mask_name_count = text.count("maskName = ")
            use_color_count = text.count("useColor = ")
            kernel_note_count = text.count("semanticNoteKernel")
            excluded_note_count = text.count("semanticNoteExcluded")
            propagated_threshold_count += threshold_count
            propagated_mask_name_count += mask_name_count
            propagated_use_color_count += use_color_count
            semantic_kernel_note_count += kernel_note_count
            semantic_excluded_number_note_count += excluded_note_count
            task_file_counts[task_id] = {
                "threshold": threshold_count,
                "mask_name": mask_name_count,
                "use_color": use_color_count,
                "semantic_kernel_note": kernel_note_count,
                "semantic_excluded_number_note": excluded_note_count,
            }

        if propagated_threshold_count >= expected_threshold_steps and expected_threshold_steps > 0:
            notes.append("Generated code propagates threshold parameters for expected benchmark steps")
        elif expected_threshold_steps > 0:
            notes.append("Generated code does not fully propagate threshold parameters yet")

        if propagated_mask_name_count >= expected_mask_steps and expected_mask_steps > 0:
            notes.append("Generated code propagates mask_name parameters for expected benchmark steps")
        elif expected_mask_steps > 0:
            notes.append("Generated code does not fully propagate mask_name parameters yet")

        if propagated_use_color_count >= expected_use_color_steps and expected_use_color_steps > 0:
            notes.append("Generated code propagates use_color parameters for expected benchmark steps")
        elif expected_use_color_steps > 0:
            notes.append("Generated code does not fully propagate use_color parameters yet")

        if expected_kernel_size_steps > 0:
            if semantic_kernel_note_count >= expected_kernel_size_steps:
                notes.append("Generated code preserves kernel_size gap as semantic notes")
            else:
                notes.append("Generated code does not preserve all kernel_size gaps as semantic notes")

        if expected_excluded_number_steps > 0:
            if semantic_excluded_number_note_count >= expected_excluded_number_steps:
                notes.append("Generated code preserves excluded_number gap as semantic notes")
            else:
                notes.append("Generated code does not preserve all excluded_number gaps as semantic notes")

        return SemanticParameterReadinessSummary(
            project_root=project_root,
            task_count=len(task_ids),
            task_ids=task_ids,
            expected_threshold_steps=expected_threshold_steps,
            expected_mask_steps=expected_mask_steps,
            expected_use_color_steps=expected_use_color_steps,
            expected_kernel_size_steps=expected_kernel_size_steps,
            expected_excluded_number_steps=expected_excluded_number_steps,
            propagated_threshold_count=propagated_threshold_count,
            propagated_mask_name_count=propagated_mask_name_count,
            propagated_use_color_count=propagated_use_color_count,
            semantic_kernel_note_count=semantic_kernel_note_count,
            semantic_excluded_number_note_count=semantic_excluded_number_note_count,
            task_file_counts=task_file_counts,
            files=task_files,
            notes=notes,
        )

    def _has_any(self, params: dict, keys: list[str]) -> bool:
        for key in keys:
            if params.get(key) is not None:
                return True
        return False

    def _project_root(self, export_payload: dict) -> str:
        result = export_payload.get("result")
        if result is not None and getattr(result, "project_root", None):
            return str(getattr(result, "project_root"))
        summary = export_payload.get("summary")
        if summary is not None and getattr(summary, "project_root", None):
            return str(getattr(summary, "project_root"))
        return ""

    def _task_files(self, export_payload: dict) -> dict[str, str]:
        result = export_payload.get("result")
        if result is not None:
            write_result = getattr(result, "write_result", None)
            if write_result is not None:
                task_files = getattr(write_result, "task_files", None)
                if isinstance(task_files, dict):
                    return dict(task_files)
        summary = export_payload.get("summary")
        if summary is not None:
            task_ids = list(getattr(summary, "task_ids", []) or [])
            files = dict(getattr(summary, "files", {}) or {})
            return {task_id: str(files.get(task_id, "")) for task_id in task_ids if files.get(task_id)}
        return {}
