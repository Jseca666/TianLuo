from pathlib import Path
from typing import Iterable

from .android_studio_project_completion_result import AndroidStudioProjectCompletionResult
from .android_studio_project_export_workflow import AndroidStudioProjectExportWorkflow
from task_exporters.export_models import ExportedTaskModel


class AndroidStudioProjectCompletionWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, tasks: Iterable[ExportedTaskModel], output_root: Path, project_name: str = "GeneratedAndroidProject") -> AndroidStudioProjectCompletionResult:
        export_result = AndroidStudioProjectExportWorkflow(self.repo_root).run(
            tasks=tasks,
            output_root=output_root,
            project_name=project_name,
        )
        return AndroidStudioProjectCompletionResult(
            export_result=export_result,
            metadata={
                "repo_root": str(self.repo_root),
                "output_root": str(output_root),
                "project_name": project_name,
            },
        )
