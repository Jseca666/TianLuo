from pathlib import Path

from .runtime_semantic_readiness_summary import RuntimeSemanticReadinessSummary


class RuntimeSemanticReadinessAnalyzer:
    def analyze(self, task_specs: list[dict], export_payload: dict) -> RuntimeSemanticReadinessSummary:
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

        ocr_read_options_count = 0
        kernel_size_option_count = 0
        excluded_number_option_count = 0
        read_text_semantic_count = 0
        read_number_semantic_count = 0
        task_file_counts = {}
        notes = []

        for task_id, file_path in task_files.items():
            path = Path(file_path)
            if not path.exists():
                notes.append(f"Task file missing for runtime semantic readiness analysis: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            options_count = text.count("OcrReadOptions(")
            kernel_count = text.count("kernelSize = ")
            excluded_count = text.count("excludedNumber = ")
            read_text_count = text.count("readTextSemantic(")
            read_number_count = text.count("readNumberSemantic(")
            ocr_read_options_count += options_count
            kernel_size_option_count += kernel_count
            excluded_number_option_count += excluded_count
            read_text_semantic_count += read_text_count
            read_number_semantic_count += read_number_count
            task_file_counts[task_id] = {
                "ocr_read_options": options_count,
                "kernel_size_option": kernel_count,
                "excluded_number_option": excluded_count,
                "read_text_semantic": read_text_count,
                "read_number_semantic": read_number_count,
            }

        if expected_kernel_size_steps > 0:
            if kernel_size_option_count >= expected_kernel_size_steps:
                notes.append("Generated code carries kernel_size into runtime semantic OCR options for expected benchmark steps")
            else:
                notes.append("Generated code does not fully carry kernel_size into runtime semantic OCR options yet")

        if expected_excluded_number_steps > 0:
            if excluded_number_option_count >= expected_excluded_number_steps:
                notes.append("Generated code carries excluded_number into runtime semantic OCR options for expected benchmark steps")
            else:
                notes.append("Generated code does not fully carry excluded_number into runtime semantic OCR options yet")

        if read_text_semantic_count > 0 or read_number_semantic_count > 0:
            notes.append("Generated code is using runtime semantic OCR helper calls")

        return RuntimeSemanticReadinessSummary(
            project_root=project_root,
            task_count=len(task_ids),
            task_ids=task_ids,
            expected_kernel_size_steps=expected_kernel_size_steps,
            expected_excluded_number_steps=expected_excluded_number_steps,
            ocr_read_options_count=ocr_read_options_count,
            kernel_size_option_count=kernel_size_option_count,
            excluded_number_option_count=excluded_number_option_count,
            read_text_semantic_count=read_text_semantic_count,
            read_number_semantic_count=read_number_semantic_count,
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
