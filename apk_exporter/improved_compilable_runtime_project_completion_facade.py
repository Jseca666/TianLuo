from pathlib import Path
from typing import Iterable

from .android_studio_project_summary import AndroidStudioProjectSummary
from .improved_compilable_runtime_project_completion_workflow import ImprovedCompilableRuntimeProjectCompletionWorkflow
from .improved_compilable_runtime_project_completion_writer import ImprovedCompilableRuntimeProjectCompletionWriter
from task_exporters.improved_runtime_exportable_api_task_builder import ImprovedRuntimeExportableApiTaskBuilder


class ImprovedCompilableRuntimeProjectCompletionFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.task_builder = ImprovedRuntimeExportableApiTaskBuilder()

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        tasks = []
        for spec in task_specs:
            tasks.append(
                self.task_builder.build(
                    task_id=str(spec.get("task_id", "generated_task")),
                    display_name=str(spec.get("display_name", "Generated Task")),
                    api_calls=spec.get("api_calls", []),
                )
            )
        completion = ImprovedCompilableRuntimeProjectCompletionWorkflow(self.repo_root).run(
            tasks=tasks,
            output_root=output_root,
            project_name=project_name,
        )
        report_path = ImprovedCompilableRuntimeProjectCompletionWriter().write(
            completion,
            Path(report_output_dir or output_root),
        )
        write_result = completion.export_result.write_result
        summary = AndroidStudioProjectSummary(
            project_root=completion.export_result.project_root,
            task_count=len(write_result.task_files),
            task_ids=list(write_result.task_files.keys()),
            files={**write_result.task_files, "registry": write_result.registry_file, "completion_report": report_path},
        )
        return {
            "completion": completion,
            "summary": summary,
            "report_path": report_path,
        }
