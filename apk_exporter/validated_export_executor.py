from pathlib import Path

from .export_execution_result import ExportExecutionResult
from .export_executor import ExportExecutor
from .export_plan_builder import ExportPlanBuilder
from .export_validator import ExportValidator


class ValidatedExportExecutor:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def execute(self, target_root: Path) -> ExportExecutionResult:
        plan = ExportPlanBuilder(self.repo_root).build()
        validation = ExportValidator().validate(plan)
        raw = ExportExecutor(self.repo_root).execute(target_root)
        return ExportExecutionResult(
            manifest_path=raw.get("manifest_path", ""),
            copied_files=raw.get("copied_files", []),
            summary=raw.get("summary", {}),
            validation=validation,
        )
