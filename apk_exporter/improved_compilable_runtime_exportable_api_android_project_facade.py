from pathlib import Path
from typing import Iterable

from .android_studio_project_summary import AndroidStudioProjectSummary
from .improved_compilable_runtime_android_studio_project_export_workflow import ImprovedCompilableRuntimeAndroidStudioProjectExportWorkflow
from task_exporters.runtime_exportable_api_task_builder import RuntimeExportableApiTaskBuilder


class ImprovedCompilableRuntimeExportableApiAndroidProjectFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.task_builder = RuntimeExportableApiTaskBuilder()

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject") -> dict:
        tasks = []
        for spec in task_specs:
            tasks.append(
                self.task_builder.build(
                    task_id=str(spec.get("task_id", "generated_task")),
                    display_name=str(spec.get("display_name", "Generated Task")),
                    api_calls=spec.get("api_calls", []),
                )
            )
        export_result = ImprovedCompilableRuntimeAndroidStudioProjectExportWorkflow(self.repo_root).run(
            tasks=tasks,
            output_root=output_root,
            project_name=project_name,
        )
        write_result = export_result.write_result
        summary = AndroidStudioProjectSummary(
            project_root=export_result.project_root,
            task_count=len(write_result.task_files),
            task_ids=list(write_result.task_files.keys()),
            files={**write_result.task_files, "registry": write_result.registry_file},
        )
        return {
            "export_result": export_result,
            "summary": summary,
        }
