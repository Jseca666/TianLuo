from pathlib import Path

from .android_studio_project_export_result import AndroidStudioProjectExportResult
from .improved_compilable_runtime_project_readiness import ImprovedCompilableRuntimeProjectReadiness


class ImprovedCompilableRuntimeProjectReadinessAnalyzer:
    def analyze(self, export_result: AndroidStudioProjectExportResult) -> ImprovedCompilableRuntimeProjectReadiness:
        todo_count = 0
        unsupported_count = 0
        task_file_todo_counts = {}
        task_file_unsupported_counts = {}
        warnings = []

        for task_id, file_path in export_result.write_result.task_files.items():
            path = Path(file_path)
            if not path.exists():
                warnings.append(f"Task file missing for readiness analysis: {path}")
                continue

            text = path.read_text(encoding="utf-8")
            todo_hits = text.count("TODO")
            unsupported_hits = text.count("unsupported")

            todo_count += todo_hits
            unsupported_count += unsupported_hits
            task_file_todo_counts[task_id] = todo_hits
            task_file_unsupported_counts[task_id] = unsupported_hits

        if unsupported_count > 0:
            warnings.append("Generated code still contains unsupported action placeholders")
        if todo_count > 0:
            warnings.append("Generated code still contains TODO placeholders")

        return ImprovedCompilableRuntimeProjectReadiness(
            todo_count=todo_count,
            unsupported_count=unsupported_count,
            task_file_todo_counts=task_file_todo_counts,
            task_file_unsupported_counts=task_file_unsupported_counts,
            warnings=warnings,
        )
