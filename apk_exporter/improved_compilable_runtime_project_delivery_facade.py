from pathlib import Path
from typing import Iterable

from .android_studio_project_summary import AndroidStudioProjectSummary
from .improved_compilable_runtime_project_completion_writer import ImprovedCompilableRuntimeProjectCompletionWriter
from .improved_compilable_runtime_project_delivery_workflow import ImprovedCompilableRuntimeProjectDeliveryWorkflow
from task_exporters.improved_runtime_exportable_api_task_builder import ImprovedRuntimeExportableApiTaskBuilder


class ImprovedCompilableRuntimeProjectDeliveryFacade:
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
        delivery = ImprovedCompilableRuntimeProjectDeliveryWorkflow(self.repo_root).run(
            tasks=tasks,
            output_root=output_root,
            project_name=project_name,
        )
        report_path = ImprovedCompilableRuntimeProjectCompletionWriter().write(
            delivery.completion,
            Path(report_output_dir or output_root),
        )
        write_result = delivery.completion.export_result.write_result
        summary = AndroidStudioProjectSummary(
            project_root=delivery.completion.export_result.project_root,
            task_count=len(write_result.task_files),
            task_ids=list(write_result.task_files.keys()),
            files={**write_result.task_files, "registry": write_result.registry_file, "completion_report": report_path},
        )
        return {
            "delivery": delivery,
            "summary": summary,
            "report_path": report_path,
        }
