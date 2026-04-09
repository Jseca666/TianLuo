from pathlib import Path
from typing import Iterable

from .android_studio_project_completion_workflow import AndroidStudioProjectCompletionWorkflow
from task_exporters.exportable_api_task_builder import ExportableApiTaskBuilder


class ExportableApiAndroidProjectExporter:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.task_builder = ExportableApiTaskBuilder()

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject"):
        tasks = []
        for spec in task_specs:
            tasks.append(
                self.task_builder.build(
                    task_id=str(spec.get("task_id", "generated_task")),
                    display_name=str(spec.get("display_name", "Generated Task")),
                    api_calls=spec.get("api_calls", []),
                )
            )
        return AndroidStudioProjectCompletionWorkflow(self.repo_root).run(
            tasks=tasks,
            output_root=output_root,
            project_name=project_name,
        )
