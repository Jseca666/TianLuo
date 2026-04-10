from pathlib import Path
from typing import Iterable

from .improved_compilable_runtime_project_completion_workflow import ImprovedCompilableRuntimeProjectCompletionWorkflow
from .improved_compilable_runtime_project_delivery_result import ImprovedCompilableRuntimeProjectDeliveryResult
from .improved_compilable_runtime_project_readiness_analyzer import ImprovedCompilableRuntimeProjectReadinessAnalyzer
from task_exporters.export_models import ExportedTaskModel


class ImprovedCompilableRuntimeProjectDeliveryWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, tasks: Iterable[ExportedTaskModel], output_root: Path, project_name: str = "GeneratedAndroidProject") -> ImprovedCompilableRuntimeProjectDeliveryResult:
        completion = ImprovedCompilableRuntimeProjectCompletionWorkflow(self.repo_root).run(
            tasks=tasks,
            output_root=output_root,
            project_name=project_name,
        )
        readiness = ImprovedCompilableRuntimeProjectReadinessAnalyzer().analyze(
            completion.export_result
        )
        return ImprovedCompilableRuntimeProjectDeliveryResult(
            completion=completion,
            readiness=readiness,
            metadata={
                "repo_root": str(self.repo_root),
                "output_root": str(output_root),
                "project_name": project_name,
            },
        )
