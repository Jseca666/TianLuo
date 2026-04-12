from pathlib import Path

from .runtime_behavior_readiness_summary import RuntimeBehaviorReadinessSummary


class RuntimeBehaviorReadinessAnalyzer:
    def analyze(self, task_specs: list[dict], export_payload: dict) -> RuntimeBehaviorReadinessSummary:
        project_root = self._project_root(export_payload)
        task_files = self._task_files(export_payload)
        task_ids = list(task_files.keys())

        expected_kernel_size_steps = 0
        expected_excluded_number_steps = 0
        for spec in task_specs:
            for call in spec.get("api_calls", []) or []:
                params = dict(call.get("params", {}) or {})
                if params.get("kernel_size") is not None:
                    expected_kernel_size_steps += 1
                if params.get("excluded_number") is not None:
                    expected_excluded_number_steps += 1

        read_text_behavior_count = 0
        read_number_behavior_count = 0
        used_semantic_engine_flag_count = 0
        kernel_hint_flag_count = 0
        excluded_filtered_flag_count = 0
        task_file_counts = {}
        notes = []

        for task_id, file_path in task_files.items():
            path = Path(file_path)
            if not path.exists():
                notes.append(f"Task file missing for runtime behavior readiness analysis: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            text_behavior_count = text.count("readTextSemanticBehavior(")
            number_behavior_count = text.count("readNumberSemanticBehavior(")
            used_flag_count = text.count("usedSemanticEngine")
            kernel_flag_count = text.count("kernelSizeHintApplied")
            excluded_flag_count = text.count("excludedNumberFiltered")
            read_text_behavior_count += text_behavior_count
            read_number_behavior_count += number_behavior_count
            used_semantic_engine_flag_count += used_flag_count
            kernel_hint_flag_count += kernel_flag_count
            excluded_filtered_flag_count += excluded_flag_count
            task_file_counts[task_id] = {
                "read_text_behavior": text_behavior_count,
                "read_number_behavior": number_behavior_count,
                "used_semantic_engine_flag": used_flag_count,
                "kernel_hint_flag": kernel_flag_count,
                "excluded_filtered_flag": excluded_flag_count,
            }

        if read_text_behavior_count > 0 or read_number_behavior_count > 0:
            notes.append("Generated code is using runtime behavior helper calls")
        if expected_kernel_size_steps > 0:
            if kernel_hint_flag_count >= expected_kernel_size_steps:
                notes.append("Generated code exposes kernelSizeHintApplied flags for expected benchmark steps")
            else:
                notes.append("Generated code does not fully expose kernelSizeHintApplied flags yet")
        if expected_excluded_number_steps > 0:
            if excluded_filtered_flag_count >= expected_excluded_number_steps:
                notes.append("Generated code exposes excludedNumberFiltered flags for expected benchmark steps")
            else:
                notes.append("Generated code does not fully expose excludedNumberFiltered flags yet")

        return RuntimeBehaviorReadinessSummary(
            project_root=project_root,
            task_count=len(task_ids),
            task_ids=task_ids,
            expected_kernel_size_steps=expected_kernel_size_steps,
            expected_excluded_number_steps=expected_excluded_number_steps,
            read_text_behavior_count=read_text_behavior_count,
            read_number_behavior_count=read_number_behavior_count,
            used_semantic_engine_flag_count=used_semantic_engine_flag_count,
            kernel_hint_flag_count=kernel_hint_flag_count,
            excluded_filtered_flag_count=excluded_filtered_flag_count,
            task_file_counts=task_file_counts,
            files=task_files,
            notes=notes,
        )

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
