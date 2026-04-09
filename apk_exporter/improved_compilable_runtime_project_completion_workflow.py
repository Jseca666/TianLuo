from pathlib import Path
from typing import Iterable

from .improved_compilable_runtime_android_studio_project_export_workflow import ImprovedCompilableRuntimeAndroidStudioProjectExportWorkflow
from .improved_compilable_runtime_project_completion_result import ImprovedCompilableRuntimeProjectCompletionResult
from .improved_compilable_runtime_project_validator import ImprovedCompilableRuntimeProjectValidator
from task_exporters.export_models import ExportedTaskModel


class ImprovedCompilableRuntimeProjectCompletionWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, tasks: Iterable[ExportedTaskModel], output_root: Path, project_name: str = "GeneratedAndroidProject") -> ImprovedCompilableRuntimeProjectCompletionResult:
        export_result = ImprovedCompilableRuntimeAndroidStudioProjectExportWorkflow(self.repo_root).run(
            tasks=tasks,
            output_root=output_root,
            project_name=project_name,
        )
        validation = ImprovedCompilableRuntimeProjectValidator().validate(export_result)
        return ImprovedCompilableRuntimeProjectCompletionResult(
            export_result=export_result,
            validation=validation,
            metadata={
                "repo_root": str(self.repo_root),
                "output_root": str(output_root),
                "project_name": project_name,
            },
        )
