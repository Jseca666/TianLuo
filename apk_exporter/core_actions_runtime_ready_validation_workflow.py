from pathlib import Path

from .core_actions_runtime_ready_readiness_analyzer import CoreActionsRuntimeReadyReadinessAnalyzer
from .main_export_core_actions_runtime_ready_project_export_report_facade import MainExportCoreActionsRuntimeReadyProjectExportReportFacade


class CoreActionsRuntimeReadyValidationWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.export_facade = MainExportCoreActionsRuntimeReadyProjectExportReportFacade(repo_root)
        self.readiness_analyzer = CoreActionsRuntimeReadyReadinessAnalyzer()

    def run(self, task_specs: list[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        export_result = self.export_facade.export(
            task_specs=task_specs,
            output_root=output_root / "project",
            project_name="GeneratedAndroidProjectCoreActionsRuntimeReadyValidated",
            report_output_dir=output_root / "reports",
        )
        readiness = self.readiness_analyzer.analyze(task_specs, export_result)
        notes = []
        notes.extend(getattr(readiness, "notes", []) or [])
        if getattr(readiness, "generated_fail_checks_count", 0) == 0:
            notes.append("Generated code is missing runtime failure checks for core actions")
        return {
            "export_result": export_result,
            "readiness": readiness,
            "notes": notes,
        }
